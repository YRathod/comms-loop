"""End to end on HotpotQA with answers: tagger -> LSTM hops -> one-clause templates -> 3B reader over the
paragraphs, scored by F1 against gold on the held-out docs, next to the single-pass baseline on the
same docs and reader. Two wirings, as in the long-bench campaign:

  chain      answer hop 1, substitute into hop 2, ... (null-shaped answers retried with alternate
             templates; a one-candidate filter passes through)
  retrieval  use every hop question only to gather paragraphs, then ONE read of the original question

    <local>/model-training/.venv/Scripts/python.exe scripts/pipeline_exec.py --adapter models/tagger_lora_0.5b --docs 3-39
"""
import argparse
import collections
import json
import os
import re
import string
import sys

import torch

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "rnn-model"))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from tagger_lora import chat, ROWS, FEWSHOT  # noqa: E402
from tagger3b import KEY, parse  # noqa: E402
from pipeline_demo import to_placeholder  # noqa: E402
from tiny.tasks.decomp import COMPOUNDS  # noqa: E402

ALL_ROWS = [json.loads(l) for l in open(r"C:\dev\research\memory-challange\long-bench\data\data\hotpotqa.jsonl", encoding="utf-8")]

# one clause per hop; several phrasings per relation, tried in order on a null-shaped answer
T = {
    "father": ["Who is the father of {x}?", "Who was {x}'s father?"],
    "mother": ["Who is the mother of {x}?", "Who was {x}'s mother?"],
    "parent": ["Who are the parents of {x}?", "What is {x} derived from or based on?", "What was the source of {x}?"],
    "spouse": ["Who is the spouse of {x}?", "Who was {x} married to?"],
    "child": ["Who is a child of {x}?", "Name a son or daughter of {x}."],
    "brother": ["What came just before {x}?", "Who is the brother of {x}?", "What is the sibling or predecessor of {x}?"],
    "sister": ["Who is the sister of {x}?"],
    "director": ["Who directed {x}?", "Who was the director of {x}?"],
    "writer": ["Who wrote {x}?", "Who is the author of {x}?"],
    "producer": ["What work is {x} known for making or appearing in?", "What film or show did {x} make?", "What was produced by or for {x}?"],
    "employer": ["Who did {x} work for?", "Which team, school or organisation was {x} part of?", "Under whom did {x} serve?", "Which presidents did {x} work with?"],
    "birthplace": ["Where was {x} born?"],
    "home": ["Where is {x} located?", "In what city or place is {x}?", "Which town, region or island is {x} in?"],
    "capital": ["What is the capital of {x}?"],
    "founder": ["Who founded {x}?", "Who was the founder of {x}?"],
    "owner": ["Who owns or holds {x}?", "Who starred in {x}?", "Who is associated with {x}?"],
    "leader": ["Who is the leader, member or main person of {x}?", "Who played for or performed in {x}?", "Who is the person behind {x}?"],
    "composer": ["Who composed {x}?"],
    "publisher": ["What channel, album, series or network carries {x}?", "What is {x} part of?", "What was {x} released or aired on?"],
    "country": ["Which country is {x} in or from?", "What is the destination or nation of {x}?"],
    "attribute": ["What is the notable number, date, rank or position associated with {x}?", "When or how much for {x}?"],
}
FILTER_T = "Which of these is {prop}: {x}?"
STOP = set("the a an of in on at to for and or was were is are that this with by from as what who which when they their it its also did".split())


def words(s):
    return {w for w in re.findall(r"[A-Za-z][A-Za-z'\-]+", s.lower()) if w not in STOP}


def norm(s):
    return " ".join(w for w in re.sub(f"[{re.escape(string.punctuation)}]", " ", s.lower()).split() if w not in {"a", "an", "the"})


def f1(pred, golds):
    best = 0.0
    for g in golds:
        p, g = norm(pred).split(), norm(g).split()
        c = sum((collections.Counter(p) & collections.Counter(g)).values())
        if c:
            pr, rc = c / len(p), c / len(g)
            best = max(best, 2 * pr * rc / (pr + rc))
    return best


def null_shaped(a):
    a = a.strip().lower()
    return a.startswith(("none", "no ", "not ", "the passage", "there is no", "unknown", "cannot")) or len(a) > 80 or a == ""


class Reader:
    def __init__(self, name="Qwen/Qwen2.5-3B-Instruct"):
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(name)
        self.model = AutoModelForCausalLM.from_pretrained(name, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda().eval()

    def retrieve(self, paras, q, k=6, max_tokens=3000):
        qw = words(q)
        out, n = [], 0
        for p in sorted(paras, key=lambda p: -len(qw & words(p)))[:k]:
            t = len(self.tok(p, add_special_tokens=False)["input_ids"])
            if n + t > max_tokens:
                break
            out.append(p)
            n += t
        return out

    @torch.no_grad()
    def ask(self, passage, q, max_new=24):
        msgs = [{"role": "system", "content": "Answer with a short phrase using only the passage. If several entities qualify, list them all."},
                {"role": "user", "content": f"Passage:\n{passage}\n\nQuestion: {q}"}]
        ids = self.tok(self.tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
        out = self.model.generate(ids, max_new_tokens=max_new, do_sample=False)
        return self.tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()


def hops_from_tag(tag, lstm, ltok, ltask):
    """tag -> list of (relation-or-filter, prop) hops via the LSTM, entity restored."""
    ph, ent = to_placeholder(tag)
    if ph is None:
        return None, ent
    ids = torch.tensor([ltok.prompt_ids(ph)], device="cuda")
    gen = lstm.generate(ids, ltask.max_answer_tokens + 1, ltok.eos_id)[0, ids.size(1):].tolist()
    gen = gen[: gen.index(ltok.eos_id)] if ltok.eos_id in gen else gen
    text = ltok.decode(gen)
    hops = []
    for h in text.split(" ? "):
        h = h.strip(" ?")
        if " . " not in h:
            continue
        body = h.split(" . ", 1)[1]
        if body.startswith("which of #"):
            hops.append(("filter", body.split(" is ")[-1]))
        else:
            hops.append((body.split(" of ")[0], None))
    # the tagger's own relation names take precedence over the LSTM's stand-ins (attribute -> owner)
    rels = [r for r in parse(tag)[0]]
    expanded = []
    for r in reversed(rels):
        expanded.extend(COMPOUNDS.get(r, (r,)))
    if len(expanded) == sum(1 for h in hops if h[0] != "filter"):
        k = 0
        fixed = []
        for h in hops:
            if h[0] == "filter":
                fixed.append(h)
            else:
                fixed.append((expanded[k], None)); k += 1
        hops = fixed
    return hops, ent


def run_chain(reader, paras, hops, ent):
    cur = ent
    trace = []
    for rel, prop in hops:
        if rel == "filter":
            if "," not in cur and " and " not in cur:            # one candidate passes through
                trace.append((f"filter {prop}", cur, "pass-through")); continue
            q = FILTER_T.format(prop=prop, x=cur)
            a = reader.ask("\n\n".join(reader.retrieve(paras, q)), q)
            trace.append((q, a, "")); cur = a if not null_shaped(a) else cur
            continue
        a = None
        for form in T.get(rel, T["attribute"]):
            q = form.format(x=cur)
            a = reader.ask("\n\n".join(reader.retrieve(paras, q)), q)
            trace.append((q, a, ""))
            if not null_shaped(a):
                break
        cur = a if a and not null_shaped(a) else cur
    return cur, trace


def run_retrieval(reader, paras, hops, ent, question):
    seen, gathered = set(), []
    cur = ent
    for rel, prop in hops:
        q = FILTER_T.format(prop=prop, x=cur) if rel == "filter" else T.get(rel, T["attribute"])[0].format(x=cur)
        for p in reader.retrieve(paras, q, k=4):
            if p not in seen:
                seen.add(p); gathered.append(p)
    for p in reader.retrieve(paras, question, k=4):
        if p not in seen:
            seen.add(p); gathered.append(p)
    passage = "\n\n".join(gathered[:10])
    return reader.ask(passage, question)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default="models/tagger_lora_0.5b")
    ap.add_argument("--base", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--lstm", default="checkpoints/compare/decomp_filter_lstm.pt")
    ap.add_argument("--docs", default="3-39")
    ap.add_argument("--out", default="scale/results/pipeline_exec.json")
    args = ap.parse_args()
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer
    ttok = AutoTokenizer.from_pretrained(args.base)
    tagger = AutoModelForCausalLM.from_pretrained(args.base, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda()
    tagger = PeftModel.from_pretrained(tagger, args.adapter).eval()
    from probe import load as load_lstm
    lstm, ltok, ltask = load_lstm(args.lstm, "cuda")
    lo, hi = map(int, args.docs.split("-"))
    tags = {}
    for i in range(lo, hi + 1):
        if i in FEWSHOT:
            continue
        ids = ttok(chat(ttok, ALL_ROWS[i]["input"]), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
        with torch.no_grad():
            out = tagger.generate(ids, max_new_tokens=40, do_sample=False, pad_token_id=ttok.pad_token_id)
        tags[i] = ttok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip().split("\n")[0]
    del tagger; torch.cuda.empty_cache()
    reader = Reader()
    res = []
    for i, tag in tags.items():
        r = ALL_ROWS[i]
        paras = [p.strip() for p in re.split(r"\n\s*\n|\nPassage \d+:\n", r["context"]) if len(p.strip()) > 40]
        sp = reader.ask("\n\n".join(reader.retrieve(paras, r["input"])), r["input"])
        hops, ent = (None, None) if tag.strip().upper().startswith("NA") else hops_from_tag(tag, lstm, ltok, ltask)
        if hops:
            ch, trace = run_chain(reader, paras, hops, ent)
            rt = run_retrieval(reader, paras, hops, ent, r["input"])
        else:
            ch, rt, trace = sp, sp, [("single-pass fallback (NA or unusable tag)", sp, "")]
        row = {"doc": i, "q": r["input"], "gold": r["answers"], "tag": tag, "key": KEY[i], "hops": hops, "entity": ent,
               "single_pass": sp, "chain": ch, "retrieval": rt,
               "f1_sp": f1(sp, r["answers"]), "f1_chain": f1(ch, r["answers"]), "f1_retrieval": f1(rt, r["answers"]), "trace": trace}
        res.append(row)
        print(f"doc {i:2d} sp {row['f1_sp']:.2f} chain {row['f1_chain']:.2f} retr {row['f1_retrieval']:.2f} | tag {tag[:40]!r} | {sp[:25]!r} / {ch[:25]!r} / {rt[:25]!r} | gold {r['answers'][0][:25]!r}", flush=True)
    n = len(res)
    summary = {k: sum(x[k] for x in res) / n for k in ("f1_sp", "f1_chain", "f1_retrieval")}
    union = sum(max(x["f1_sp"], x["f1_chain"], x["f1_retrieval"]) for x in res) / n
    summary.update({"n": n, "oracle_union": union,
                    "chain_wins": sum(x["f1_chain"] > x["f1_sp"] + 1e-9 for x in res), "chain_losses": sum(x["f1_chain"] < x["f1_sp"] - 1e-9 for x in res),
                    "retr_wins": sum(x["f1_retrieval"] > x["f1_sp"] + 1e-9 for x in res), "retr_losses": sum(x["f1_retrieval"] < x["f1_sp"] - 1e-9 for x in res)})
    print(json.dumps(summary, indent=1))
    json.dump({"summary": summary, "rows": res}, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
