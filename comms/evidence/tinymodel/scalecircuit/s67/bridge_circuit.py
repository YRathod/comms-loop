"""Layer x head attention capture + logit lens for the reader's answer position on chosen DEV2 cases
(frozen Qwen2.5-3B-Instruct, eager attention, one layer at a time in memory). No training, no eval slice.

For each case: rebuild the exact superset+notes prompt used by the pipeline, find the token spans of the
hop-1 note answer, the hop-2 note answer, the gold answer in the passage, and the question; at the final
prompt position record, per layer and head, the attention mass on each span; and per layer the logit-lens
rank/probability of the first token of gold vs hop-1 note vs hop-2 note.

    python scripts/bridge_circuit.py --docs 44 28 34 80 --out scale/results/bridge_circuit
"""
import argparse
import json
import os
import re
import sys

import torch

sys.path.insert(0, "scripts"); sys.path.insert(0, "rnn-model")
import pipeline_exec as P  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NAME = "Qwen/Qwen2.5-3B-Instruct"


def hop_notes(x):
    tr = [t for t in x.get("itrace", []) if isinstance(t, list) and len(t) > 1 and t[1] and not P.null_shaped(t[1]) and not str(t[0]).startswith("filter")]
    return tr


def passage_for(x, d, r):
    paras = [p.strip() for p in re.split(r"\n\s*\n|\nPassage \d+:\n", d["context"]) if len(p.strip()) > 40]
    hop = []
    for t in hop_notes(x):
        hop += r.retrieve(paras, t[0], k=4)
        hop += r.retrieve(paras, f"{x['q']} {t[1]}", k=3)
    base = r.retrieve(paras, x["q"])
    return "\n\n".join(r.pack(base + [p for p in reversed(hop) if p not in base]))


def find_span(offsets, text, needle):
    """token index range [a, b) of the first case-insensitive occurrence of needle in text, via char offsets"""
    i = text.lower().find(needle.lower())
    if i < 0 or not needle.strip():
        return None
    j = i + len(needle)
    idx = [k for k, (s, e) in enumerate(offsets) if e > i and s < j]
    return (idx[0], idx[-1] + 1) if idx else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", nargs="+", type=int, required=True)
    ap.add_argument("--dev-json", default="scale/results/pipeline_dev2_verify.json")
    ap.add_argument("--dev-data", default="data/hotpot_dev2_v1.jsonl")
    ap.add_argument("--out", default="scale/results/bridge_circuit")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(NAME)
    model = AutoModelForCausalLM.from_pretrained(NAME, torch_dtype=torch.bfloat16, attn_implementation="eager").cuda().eval()
    W = model.lm_head.weight; ln = model.model.norm

    class R:
        def __init__(self): self.tok = tok
        retrieve = P.Reader.retrieve; pack = P.Reader.pack
    r = R()
    rows = {x["doc"]: x for x in json.load(open(a.dev_json, encoding="utf-8"))["rows"]}
    dev = [json.loads(l) for l in open(a.dev_data, encoding="utf-8")]
    results = {}
    for doc in a.docs:
        x = rows[doc]; d = dev[doc]; notes = hop_notes(x)
        passage = passage_for(x, d, r)
        notes_txt = "\n".join(f"{t[0]} -> {t[1]}" for t in notes)
        msgs = [{"role": "system", "content": "Answer with a short phrase using only the passage. If several entities qualify, list them all."},
                {"role": "user", "content": f"Passage:\n{passage}\n\nNotes from sub-questions (may be wrong):\n{notes_txt}\n\nQuestion: {x['q']}"}]
        prompt = tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
        enc = tok(prompt, return_tensors="pt", add_special_tokens=False, return_offsets_mapping=True)
        ids = enc["input_ids"].cuda(); offsets = enc["offset_mapping"][0].tolist(); T = ids.shape[1]
        gold = x["gold"][0]
        # spans: gold in the PASSAGE region only (first occurrence inside the passage text), notes in the notes region
        p_start = prompt.find("Passage:\n"); n_start = prompt.find("Notes from sub-questions"); q_start = prompt.rfind("Question:")
        def span_in(region_start, region_end, needle):
            sub = prompt[region_start:region_end]; i = sub.lower().find(needle.lower())
            if i < 0: return None
            i += region_start; j = i + len(needle)
            idx = [k for k, (s, e) in enumerate(offsets) if e > i and s < j]
            return (idx[0], idx[-1] + 1) if idx else None
        spans = {"gold_in_passage": span_in(p_start, n_start, gold),
                 "note1_in_notes": span_in(n_start, q_start, notes[0][1]) if notes else None,
                 "note2_in_notes": span_in(n_start, q_start, notes[1][1]) if len(notes) > 1 else None,
                 "note1_in_passage": span_in(p_start, n_start, notes[0][1]) if notes else None,
                 "question": (next(k for k, (s, e) in enumerate(offsets) if e > q_start), T)}
        # memory: full attention for all 36 layers at T~3000 is ~10 GB, so hooks read the LAST query row of each layer's
        # attention as it is produced, sum it onto the spans, and hand back None so nothing is retained
        L = len(model.model.layers); H = model.config.num_attention_heads
        mass = {k: torch.zeros(L, H) for k in spans}
        def make_hook(l):
            def hook(mod, inp, out_):
                att = out_[1]
                if att is not None:
                    row = att[0, :, -1, :].float().cpu()
                    for k, sp in spans.items():
                        if sp: mass[k][l] = row[:, sp[0]:sp[1]].sum(-1)
                return (out_[0], None) + tuple(out_[2:])
            return hook
        hooks = [model.model.layers[l].self_attn.register_forward_hook(make_hook(l)) for l in range(L)]
        with torch.no_grad():
            out = model(ids, output_attentions=True, output_hidden_states=True)
        for hk in hooks: hk.remove()
        # logit lens at the last position
        def first_tok(s): return tok(" " + s.strip(), add_special_tokens=False)["input_ids"][0]
        cands = {"gold": first_tok(gold)}
        if notes: cands["note1"] = first_tok(notes[0][1])
        if len(notes) > 1: cands["note2"] = first_tok(notes[1][1])
        lens = {k: [] for k in cands}; lens_rank = {k: [] for k in cands}
        for l, hs in enumerate(out.hidden_states[1:]):
            h = ln(hs[0, -1].float().unsqueeze(0).to(W.dtype))
            logits = (h @ W.T).float()[0]; probs = torch.softmax(logits, -1)
            order = torch.argsort(logits, descending=True)
            for k, t in cands.items():
                lens[k].append(round(probs[t].item(), 5)); lens_rank[k].append(int((order == t).nonzero()[0].item()) + 1)
        gen = model.generate(ids, max_new_tokens=16, do_sample=False)
        answer = tok.decode(gen[0, T:], skip_special_tokens=True).strip()
        results[doc] = {"q": x["q"], "gold": gold, "notes": [t[1] for t in notes], "answer_now": answer, "prompt_tokens": T, "layers": L, "heads": H,
                        "spans": spans, "mass": {k: v.tolist() for k, v in mass.items()}, "lens_prob": lens, "lens_rank": lens_rank}
        top = sorted(((float(mass["note1_in_notes"][l, h] - (mass["gold_in_passage"][l, h] if spans["gold_in_passage"] else 0)), l, h) for l in range(L) for h in range(H)), reverse=True)[:5] if spans["note1_in_notes"] else []
        print(f"doc {doc}: T={T} answer_now={answer!r} gold={gold!r} notes={[t[1][:20] for t in notes]} spans={ {k: bool(v) for k, v in spans.items()} }")
        print(f"   top heads by (mass on hop-1 note - mass on gold in passage): {[(l, h, round(m, 3)) for m, l, h in top]}")
        for k in cands:
            rk = lens_rank[k]; print(f"   logit lens rank of {k} first token by layer (every 4th): {rk[::4]} -> final {rk[-1]}")
        del out; torch.cuda.empty_cache()
    json.dump(results, open(os.path.join(a.out, "capture.json"), "w"), indent=1)
    print("saved", os.path.join(a.out, "capture.json"))


if __name__ == "__main__":
    main()
