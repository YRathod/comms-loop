"""Causal check: zero the output of chosen attention heads (by hooking o_proj's input) and re-decode the answer for
a DEV2 case, using the same prompt construction as bridge_circuit.py. If the copied note stops being the answer
when the note-attending heads are silenced (and stays when random heads are), the heads carry the copy.

    python scripts/bridge_circuit_ablate.py --doc 44 --heads 29:1 30:3 29:4 --random 3
"""
import argparse
import json
import random
import re
import sys

import torch

sys.path.insert(0, "scripts"); sys.path.insert(0, "rnn-model")
import pipeline_exec as P  # noqa: E402
from bridge_circuit import hop_notes, passage_for, NAME  # noqa: E402
from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", type=int, required=True)
    ap.add_argument("--heads", nargs="+", required=True, help="layer:head pairs to silence")
    ap.add_argument("--random", type=int, default=3, help="number of random head sets of the same size to silence as controls")
    ap.add_argument("--dev-json", default="scale/results/pipeline_dev2_verify.json")
    ap.add_argument("--dev-data", default="data/hotpot_dev2_v1.jsonl")
    a = ap.parse_args()
    tok = AutoTokenizer.from_pretrained(NAME)
    model = AutoModelForCausalLM.from_pretrained(NAME, torch_dtype=torch.bfloat16, attn_implementation="eager").cuda().eval()
    H = model.config.num_attention_heads; D = model.config.hidden_size // H; L = len(model.model.layers)

    class R:
        def __init__(self): self.tok = tok
        retrieve = P.Reader.retrieve; pack = P.Reader.pack
    x = {r["doc"]: r for r in json.load(open(a.dev_json, encoding="utf-8"))["rows"]}[a.doc]
    d = [json.loads(l) for l in open(a.dev_data, encoding="utf-8")][a.doc]
    notes = hop_notes(x); passage = passage_for(x, d, R())
    notes_txt = "\n".join(f"{t[0]} -> {t[1]}" for t in notes)
    msgs = [{"role": "system", "content": "Answer with a short phrase using only the passage. If several entities qualify, list them all."},
            {"role": "user", "content": f"Passage:\n{passage}\n\nNotes from sub-questions (may be wrong):\n{notes_txt}\n\nQuestion: {x['q']}"}]
    ids = tok(tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()

    def decode_with(silenced):
        by_layer = {}
        for l, h in silenced:
            by_layer.setdefault(l, []).append(h)
        hooks = []
        for l, hs in by_layer.items():
            def pre(mod, inp, hs=hs):
                t = inp[0].clone()
                for h in hs:
                    t[..., h * D:(h + 1) * D] = 0
                return (t,)
            hooks.append(model.model.layers[l].self_attn.o_proj.register_forward_pre_hook(pre))
        with torch.no_grad():
            g = model.generate(ids, max_new_tokens=16, do_sample=False)
        for hk in hooks:
            hk.remove()
        return tok.decode(g[0, ids.shape[1]:], skip_special_tokens=True).strip()

    target = [(int(p.split(":")[0]), int(p.split(":")[1])) for p in a.heads]
    print(f"doc {a.doc} | gold {x['gold'][0]!r} | hop-1 note {notes[0][1]!r}")
    print(f"  no ablation            -> {decode_with([])!r}")
    print(f"  silence {target}       -> {decode_with(target)!r}")
    rng = random.Random(0)
    for i in range(a.random):
        rnd = [(rng.randrange(L), rng.randrange(H)) for _ in target]
        print(f"  silence random {rnd} -> {decode_with(rnd)!r}")


if __name__ == "__main__":
    main()
