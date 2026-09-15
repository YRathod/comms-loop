"""Single-question demo of the constrained verify step on the frozen 3B reader (no slice, no training).

    python scripts/verify_demo.py
"""
import json
import re
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
NAME = "Qwen/Qwen2.5-3B-Instruct"
tok = AutoTokenizer.from_pretrained(NAME)
model = AutoModelForCausalLM.from_pretrained(NAME, torch_dtype=torch.bfloat16, attn_implementation="sdpa").cuda().eval()


@torch.no_grad()
def ask(system, user, max_new=80):
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]
    ids = tok(tok.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False), return_tensors="pt", add_special_tokens=False)["input_ids"].cuda()
    out = model.generate(ids, max_new_tokens=max_new, do_sample=False)
    return tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True).strip()


QUESTION = "Who was the president of the country where Linus Torvalds was born during 1995?"
NOTES = "Where was Linus Torvalds born? -> Helsinki, Finland"
PASSAGE = (
    "Linus Torvalds\nLinus Benedict Torvalds (born 28 December 1969) is a Finnish-American software engineer who was born in Helsinki, Finland. "
    "He is the creator of the Linux kernel.\n\n"
    "Politics of Finland\nMauno Koivisto served as President of Finland from 1982 to 1994. He was succeeded by Martti Ahtisaari, who served as "
    "President of Finland from 1994 to 2000. Tarja Halonen became president in 2000. Urho Kekkonen was president from 1956 to 1982.\n\n"
    "Helsinki\nHelsinki is the capital of Finland. Its mayor in 1995 was Kari Rahkamo.")

print("Q:", QUESTION)
print("\n== 1. plain read (today's reader prompt, with notes) ==")
plain = ask("Answer with a short phrase using only the passage. If several entities qualify, list them all.",
            f"Passage:\n{PASSAGE}\n\nNotes from sub-questions (may be wrong):\n{NOTES}\n\nQuestion: {QUESTION}", 24)
print("answer:", plain)

print("\n== 2. verify step ==")
constraints = ask("List the hard constraints the correct answer must satisfy, as a JSON list of short strings (roles, dates, places, qualifiers). Output only the JSON list.",
                  f"Notes: {NOTES}\nQuestion: {QUESTION}", 60)
print("constraints:", constraints)
try:
    clist = json.loads(re.search(r"\[.*\]", constraints, re.S).group(0))
except Exception:
    clist = []
YEAR = r"(?<!\d)(1[89]\d\d|20\d\d)(?!\d)"
years = sorted(set(re.findall(YEAR, QUESTION)) | {y for c in clist for y in re.findall(YEAR, c)})   # years from the question itself first; the model's list may format them oddly
print("year constraints (mechanical, from question + list):", years)


def quote_ok(quote):
    """mechanical check: every year constraint must be inside a range or equal to a year stated in the quote"""
    if not years:
        return True, "no year constraint"
    for y in years:
        y = int(y)
        rngs = re.findall(r"(?<!\d)(1[89]\d\d|20\d\d)\s*(?:to|-|–|until)\s*(1[89]\d\d|20\d\d)(?!\d)", quote)
        singles = [int(s) for s in re.findall(YEAR, quote)]
        if any(int(a) <= y <= int(b) for a, b in rngs) or y in singles:
            continue
        return False, f"quote does not cover {y}"
    return True, "year constraints covered by the quote"


cand = ask("Answer the question from the passage. Output exactly two lines: 'ANSWER: <short phrase>' and 'QUOTE: <one sentence copied verbatim from the passage that supports the answer>'.",
           f"Passage:\n{PASSAGE}\n\nNotes:\n{NOTES}\n\nQuestion: {QUESTION}", 90)
print("candidate:\n" + cand)
m = re.search(r"ANSWER:\s*(.+?)\s*\n\s*QUOTE:\s*(.+)", cand, re.S)
ans, quote = (m.group(1).strip(), m.group(2).strip()) if m else (cand, "")
ok, why = quote_ok(quote)
print(f"mechanical check: {ok} ({why})")
final = ans
if not ok:
    # constraint-filtered retrieval: keep only passage sentences whose stated years cover every year constraint,
    # then let the reader choose among those sentences alone (it cannot pick a sentence the check would reject)
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", PASSAGE.replace("\n", " ")) if s.strip()]
    keep = [s for s in sents if quote_ok(s)[0] and re.search(YEAR, s)]
    print("sentences satisfying the year constraint:", keep)
    if keep:
        rev = ask("Answer the question using ONLY the sentences given. Output exactly two lines: 'ANSWER: <short phrase>' and 'QUOTE: <the one sentence, copied verbatim>'.",
                  "Sentences:\n" + "\n".join(f"- {s}" for s in keep) + f"\n\nNotes:\n{NOTES}\n\nQuestion: {QUESTION}", 90)
        print("revision (constraint-filtered):\n" + rev)
        m2 = re.search(r"ANSWER:\s*(.+?)\s*\n\s*QUOTE:\s*(.+)", rev, re.S)
        if m2:
            ok2, why2 = quote_ok(m2.group(2).strip())
            print(f"mechanical check on revision: {ok2} ({why2})")
            final = m2.group(1).strip() if ok2 else ans
    else:
        print("no sentence satisfies the constraint; keeping the original answer")
print("\nFINAL:", final, "| gold: Martti Ahtisaari | plain read was:", plain)
