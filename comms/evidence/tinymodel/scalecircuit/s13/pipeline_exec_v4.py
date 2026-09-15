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

    def pack(self, chunks, max_tokens=3000):
        """same paragraph budget for every wiring: keep chunks in the given priority order until max_tokens"""
        out, n = [], 0
        for p in chunks:
            t = len(self.tok(p, add_special_tokens=False)["input_ids"])
            if n + t > max_tokens:
                continue
            out.append(p); n += t
        return out

    @torch.no_grad()
    def ask(self, passage, q, max_new=24, notes=None):
        msgs = [{"role": "system", "content": "Answer with a short phrase using only the passage. If several entities qualify, list them all."},
                {"role": "user", "content": f"Passage:\n{passage}\n\n" + (f"Notes from sub-questions (may be wrong):\n{notes}\n\n" if notes else "") + f"Question: {q}"}]
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
    passage = "\n\n".join(reader.pack(gathered))
    return reader.ask(passage, question)


def run_iterative(reader, paras, hops, ent, question):
    """answer each hop over its own retrieval, feed the answer into the next hop's retrieval query,
    gather every chunk seen, then ONE read of the original question over the gathered chunks
    (same token budget as the baseline). Returns (answer, answer_with_notes, trace)."""
    seen, gathered, notes, trace = set(), [], [], []
    cur = ent
    for rel, prop in hops:
        if rel == "filter" and "," not in cur and " and " not in cur:
            trace.append((f"filter {prop}", cur, "pass-through")); continue
        q = FILTER_T.format(prop=prop, x=cur) if rel == "filter" else T.get(rel, T["attribute"])[0].format(x=cur)
        chunks = reader.retrieve(paras, q, k=4)
        for p in chunks:
            if p not in seen:
                seen.add(p); gathered.append(p)
        a = reader.ask("\n\n".join(chunks), q)
        trace.append((q, a, ""))
        if not null_shaped(a):
            cur = a; notes.append(f"{q} -> {a}")
            for p in reader.retrieve(paras, f"{question} {a}", k=3):      # bridge entity + original question
                if p not in seen:
                    seen.add(p); gathered.append(p)
    final = reader.retrieve(paras, question, k=4)
    ordered = final + [p for p in reversed(gathered) if p not in final]      # question chunks first, then last hop first
    passage = "\n\n".join(reader.pack(ordered))
    return reader.ask(passage, question), reader.ask(passage, question, notes="\n".join(notes) if notes else None), trace, gathered, notes


def verbose(a):
    """gold-free shape check: HotpotQA answers are short spans; a sentence-shaped answer is a miss signal"""
    return len(a.split()) > 6 or a.rstrip().endswith(".")


def run_superset(reader, paras, gathered, notes, question, sp):
    """v3 ordering: the baseline's own top-6 question chunks FIRST (so the wiring never drops what single-pass
    read), then the hop chunks last-hop-first, packed under the same 3000-token budget. Returns
    (answer, answer_with_notes, answer_with_verbosity_fallback_to_single_pass)."""
    base = reader.retrieve(paras, question)                                   # identical to the baseline's chunk list
    ordered = base + [p for p in reversed(gathered) if p not in base]
    passage = "\n\n".join(reader.pack(ordered))
    a = reader.ask(passage, question)
    an = reader.ask(passage, question, notes="\n".join(notes) if notes else None)
    fb = sp if (verbose(a) and not verbose(sp)) else a
    return a, an, fb, passage


@torch.no_grad()
def judge(reader, passage, q, cand_a, cand_b):
    """order-debiased 2-way verification: which candidate does the passage support? Returns the candidate
    chosen in BOTH orders, or None when the two orders disagree (position bias) or the reply is unparsable."""
    picks = []
    for x, y in ((cand_a, cand_b), (cand_b, cand_a)):
        msgs = [{"role": "system", "content": "You verify answers against a passage. Reply with exactly one character: 1 or 2."},
                {"role": "user", "content": f"Passage:\n{passage}\n\nQuestion: {q}\n\nCandidate 1: {x}\nCandidate 2: {y}\n\nWhich candidate is correct according to the passage? Reply 1 or 2."}]
        ids = reader.tok(reader.tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
        out = reader.model.generate(ids, max_new_tokens=2, do_sample=False)
        r = reader.tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()[:1]
        picks.append(x if r == "1" else y if r == "2" else None)
    return picks[0] if picks[0] is not None and picks[0] == picks[1] else None


def select(reader, passage, q, sp, su):
    """v4 wiring: agree -> that answer; disagree -> debiased judge; judge undecided -> single-pass (never worse by
    default). Returns (answer, how)."""
    if norm(sp) == norm(su):
        return sp, "agree"
    j = judge(reader, passage, q, sp, su)
    return (j, "judge") if j is not None else (sp, "undecided->sp")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--adapter", default="models/tagger_lora_0.5b")
    ap.add_argument("--base", default="Qwen/Qwen2.5-0.5B-Instruct")
    ap.add_argument("--lstm", default="checkpoints/compare/decomp_filter_lstm.pt")
    ap.add_argument("--docs", default="3-39", help="eval 3-39 (few-shot excluded); DEV for wiring work = 160-199 (never labelled, never trained on)")
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
    docs = [i for i in range(lo, hi + 1) if not (i in FEWSHOT and hi <= 39)]     # few-shot docs excluded only in the eval range
    tags = {}
    for i in docs:
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
            it, itn, itrace, gathered, notes = run_iterative(reader, paras, hops, ent, r["input"])
            su, sun, suf, su_passage = run_superset(reader, paras, gathered, notes, r["input"], sp)
            sel, how = select(reader, su_passage, r["input"], sp, suf)
        else:
            ch, rt, it, itn, su, sun, suf, sel, how, trace, itrace = sp, sp, sp, sp, sp, sp, sp, sp, "single-pass", [("single-pass fallback (NA or unusable tag)", sp, "")], []
        row = {"doc": i, "q": r["input"], "gold": r["answers"], "tag": tag, "key": KEY.get(i), "hops": hops, "entity": ent,
               "single_pass": sp, "chain": ch, "retrieval": rt, "iterative": it, "iterative_notes": itn,
               "superset": su, "superset_notes": sun, "superset_fallback": suf, "select": sel, "select_how": how, "f1_select": f1(sel, r["answers"]),
               "f1_sp": f1(sp, r["answers"]), "f1_chain": f1(ch, r["answers"]), "f1_retrieval": f1(rt, r["answers"]),
               "f1_iterative": f1(it, r["answers"]), "f1_iterative_notes": f1(itn, r["answers"]),
               "f1_superset": f1(su, r["answers"]), "f1_superset_notes": f1(sun, r["answers"]), "f1_superset_fallback": f1(suf, r["answers"]),
               "trace": trace, "itrace": itrace}
        res.append(row)
        print(f"doc {i:3d} sp {row['f1_sp']:.2f} chain {row['f1_chain']:.2f} retr {row['f1_retrieval']:.2f} iter {row['f1_iterative']:.2f} iter+n {row['f1_iterative_notes']:.2f} sup {row['f1_superset']:.2f} sup+n {row['f1_superset_notes']:.2f} sup+fb {row['f1_superset_fallback']:.2f} sel {row['f1_select']:.2f}({how[:5]}) | tag {tag[:30]!r} | {sp[:20]!r} / {su[:20]!r} | gold {r['answers'][0][:20]!r}", flush=True)
    n = len(res)
    W = ("f1_sp", "f1_chain", "f1_retrieval", "f1_iterative", "f1_iterative_notes", "f1_superset", "f1_superset_notes", "f1_superset_fallback", "f1_select")
    summary = {k: sum(x[k] for x in res) / n for k in W}
    union = sum(max(x[k] for k in W) for x in res) / n
    summary.update({"n": n, "oracle_union": union})
    for k in W[1:]:
        summary[k.replace("f1_", "") + "_wins"] = sum(x[k] > x["f1_sp"] + 1e-9 for x in res)
        summary[k.replace("f1_", "") + "_losses"] = sum(x[k] < x["f1_sp"] - 1e-9 for x in res)
    print(json.dumps(summary, indent=1))
    json.dump({"summary": summary, "args": dict(vars(args), budget_tokens=3000, retrieve_k=6, wiring_k=4), "rows": res}, open(args.out, "w"), indent=1)


if __name__ == "__main__":
    main()
