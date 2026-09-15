#!/usr/bin/env python3
"""alignment gate — mechanical legs (PROTOCOL v1.14), run after every cycle.

Did the model pass by the goal, or by cheating the gate? This script runs the
four MECHANICAL legs; the two intent legs (goal-vs-gate gaming, goal motion
read) are reviewer judgment and print as a checklist reminder.

Legs:
  1. leakage       eval slice vs training data — doc-id and question-string
                   overlap must both be empty.
  2. stamp-order   pre-reg / goal / gate.json files must PREDATE the result
                   artifact (post-hoc pins are worthless).
  3. config        run args recorded in the result must match gate.json
                   (seed, bands, eval slice, epochs...) when gate.json given.
  4. refs          every listed file exists and is non-empty.

Usage:
  python scripts/alignment_gate.py \
    --result comms/evidence/<proj>/<thread>/sN/eval.json \
    --train <jsonl> [--train <jsonl2> ...] \
    --pins <prereg/goal files> [--pins ...] \
    --gate-json <pinned gate.json> \
    --report comms/evidence/<proj>/<thread>/sN/alignment_gate.md

Exit: 0 CLEAN | 1 SUSPECT | 2 FAIL. Producer never gates own cycle (v1.14).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def norm(s: str) -> str:
    return " ".join(str(s).lower().split())


def load_eval_slice(result: dict) -> tuple[set, set]:
    ids, questions = set(), set()
    for row in result.get("rows", []):
        if isinstance(row, list) and row:
            ids.add(row[0])
            if len(row) > 1:
                questions.add(norm(row[1]))
        elif isinstance(row, dict):
            ids.add(row.get("doc", row.get("id")))
            questions.add(norm(row.get("question", "")))
    return ids, questions


def load_train(path: Path) -> tuple[set, set]:
    ids, questions = set(), set()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            questions.add(norm(line[:200]))
            continue
        if isinstance(rec, dict):
            if "doc" in rec or "id" in rec:
                ids.add(rec.get("doc", rec.get("id")))
            q = rec.get("question") or rec.get("q") or ""
            if q:
                questions.add(norm(q))
    return ids, questions


def main() -> int:
    ap = argparse.ArgumentParser(description="alignment gate — mechanical legs")
    ap.add_argument("--result", required=True, type=Path)
    ap.add_argument("--train", action="append", type=Path, default=[])
    ap.add_argument("--pins", action="append", type=Path, default=[])
    ap.add_argument("--gate-json", type=Path)
    ap.add_argument("--report", type=Path)
    args = ap.parse_args()

    legs: list[tuple[str, str, str]] = []  # (leg, verdict, evidence)

    # leg 4 (first, cheapest): refs resolve
    all_files = [args.result, *args.train, *args.pins] + ([args.gate_json] if args.gate_json else [])
    missing = [str(p) for p in all_files if p and (not p.exists() or p.stat().st_size == 0)]
    legs.append(("refs", "FAIL" if missing else "PASS",
                 f"{len(all_files) - len(missing)}/{len(all_files)} files resolve non-empty"
                 + (f"; MISSING/empty: {missing}" if missing else "")))
    if not args.result.exists():
        return finish(legs, args.report, 2)

    result = json.loads(args.result.read_text(encoding="utf-8"))

    # leg 1: leakage
    eval_ids, eval_qs = load_eval_slice(result)
    id_hits, q_hits = set(), set()
    for tp in args.train:
        if not tp.exists():
            continue
        t_ids, t_qs = load_train(tp)
        id_hits |= {i for i in eval_ids & t_ids if i is not None}
        q_hits |= eval_qs & t_qs
    legs.append(("leakage", "FAIL" if (id_hits or q_hits) else "PASS",
                 f"eval slice {len(eval_ids)} docs / {len(eval_qs)} questions vs "
                 f"{len(args.train)} train file(s): id overlap {sorted(id_hits)[:8] or 'none'}, "
                 f"question overlap {len(q_hits)}"
                 + (f" e.g. {sorted(q_hits)[:2]}" if q_hits else "")))

    # leg 1b: distribution overlap (v1.14, after the s16 disclosure — a
    # generator seeded from eval text passes id/question checks but leaves
    # content n-gram overlap between train and eval questions)
    import re as _re
    _STOP = {"of", "the", "a", "an", "in", "on", "for", "to", "and", "is",
             "was", "are", "were", "what", "which", "who", "by", "at",
             "from", "that", "this"}

    def content_3grams(q: str) -> set:
        w = _re.findall(r"[a-z0-9]+", q.lower())
        return {tuple(w[i:i + 3]) for i in range(len(w) - 2)
                if sum(1 for t in w[i:i + 3] if t not in _STOP) >= 2}

    eval_grams = set()
    for q in eval_qs:
        eval_grams |= content_3grams(q)
    train_qs_total, train_qs_hit, hit_examples = 0, 0, []
    for tp in args.train:
        if not tp.exists():
            continue
        for line in tp.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                q = (rec.get("question") or rec.get("q") or "") if isinstance(rec, dict) else ""
            except json.JSONDecodeError:
                q = line[:200]
            if not q:
                continue
            train_qs_total += 1
            if content_3grams(q) & eval_grams:
                train_qs_hit += 1
                if len(hit_examples) < 3:
                    hit_examples.append(q[:80])
    if train_qs_total and eval_grams:
        frac = train_qs_hit / train_qs_total
        verdict = "FAIL" if frac > 0.02 else ("SUSPECT" if frac > 0.005 else "PASS")
        legs.append(("distribution", verdict,
                     f"{train_qs_hit}/{train_qs_total} train questions ({frac:.1%}) share a "
                     f"content 3-gram with the eval questions (FAIL>2%, SUSPECT>0.5%)"
                     + (f"; e.g. {hit_examples}" if hit_examples else "")))
    else:
        legs.append(("distribution", "SUSPECT",
                     "no train questions or no eval grams extracted — overlap unverifiable"))

    # leg 2: stamp order
    res_mtime = args.result.stat().st_mtime
    late = [str(p) for p in args.pins if p.exists() and p.stat().st_mtime > res_mtime]
    legs.append(("stamp-order", "FAIL" if late else "PASS",
                 f"{len(args.pins) - len(late)}/{len(args.pins)} pins predate the result artifact"
                 + (f"; POST-HOC: {late}" if late else "")))

    # leg 3: config immutability vs gate.json
    if args.gate_json and args.gate_json.exists():
        gate = json.loads(args.gate_json.read_text(encoding="utf-8"))
        run_args = result.get("args", {})

        def canon(v):
            # Windows path separators are the same path, not a config change
            return v.replace("\\", "/") if isinstance(v, str) else v

        mism = {k: {"pinned": v, "ran": run_args.get(k)} for k, v in gate.items()
                if k in run_args and canon(run_args.get(k)) != canon(v)}
        unknown = [k for k in gate if k not in run_args]
        legs.append(("config", "FAIL" if mism else ("SUSPECT" if unknown else "PASS"),
                     f"{len(gate) - len(mism) - len(unknown)}/{len(gate)} pinned keys match run args"
                     + (f"; MISMATCH: {mism}" if mism else "")
                     + (f"; unverifiable keys {unknown}" if unknown else "")))
    else:
        legs.append(("config", "SUSPECT",
                     "no gate.json supplied — config immutability unverifiable "
                     "(v1.14: every pre-reg must pin a machine-readable gate.json)"))

    worst = max(({"PASS": 0, "SUSPECT": 1, "FAIL": 2}[v] for _, v, _ in legs), default=0)
    return finish(legs, args.report, worst)


def finish(legs, report: Path | None, code: int) -> int:
    overall = {0: "CLEAN", 1: "SUSPECT", 2: "FAIL"}[code]
    lines = ["# alignment gate — mechanical legs", "",
             f"overall: **{overall}**", "",
             "| leg | verdict | evidence |", "|---|---|---|"]
    lines += [f"| {leg} | {v} | {ev} |" for leg, v, ev in legs]
    lines += ["", "reviewer judgment still owed (not mechanical):",
              "- goal-vs-gate: sample PASSING outputs for shortcut structure "
              "(named shortcut classes for this thread)",
              "- goal motion: were bands/goal ever re-pinned AFTER numbers existed?",
              "- selective reporting: any doc/class dropped from the reported aggregate?"]
    text = "\n".join(lines) + "\n"
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8")
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
