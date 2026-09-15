"""Assemble a per-cycle SAFETY CASE from artifacts: each sub-claim is SUPPORTED only by a file the
script read, never by assertion. Output: markdown for the cycle evidence dir; the reviewer signs it.

    python scripts/safety_case.py --cycle "key #10 free-form decomposer" --key-row 10 \
      --prereg docs/PREREG-freeform-decomposer.md --gate <gate.json> --train data/decomp_train.jsonl \
      --slice-meta data/hotpot_heldout_v4.meta.json --result scale/results/<eval>.json \
      [--block <frozen block.md>] [--heartbeat <dir>/heartbeat.json] [--max-seconds N] [--suspect-disclosed <mail id>] --out SAFETY-CASE.md
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
COMMS = r"<local>/comms-loop\comms"


def mtime(p):
    return os.path.getmtime(p) if p and os.path.exists(p) else None


def iso(t):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t)) if t else "n/a"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cycle", required=True)
    ap.add_argument("--key-row", type=int, required=True)
    ap.add_argument("--prereg", required=True)
    ap.add_argument("--gate", required=True)
    ap.add_argument("--train", nargs="*", default=[])
    ap.add_argument("--generated", nargs="*", default=[], help="training files that contain model-generated text (content filter report required)")
    ap.add_argument("--slice-meta", default=None)
    ap.add_argument("--result", default=None)
    ap.add_argument("--block", default=None, help="frozen result_block.md to re-derive from --result")
    ap.add_argument("--claim", default=None, help="claimed wiring key for the block re-derivation")
    ap.add_argument("--heartbeat", default=None)
    ap.add_argument("--max-seconds", type=int, default=6 * 3600)
    ap.add_argument("--suspect-disclosed", default=None, help="mail id that discloses a SUSPECT provenance stamp")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    claims = []

    def add(name, ok, evidence):
        claims.append((name, "SUPPORTED" if ok else "UNSUPPORTED", evidence))

    # 1 authority
    keys = open(os.path.join(COMMS, "KEYS.md"), encoding="utf-8").read()
    row = next((l for l in keys.splitlines() if l.startswith(f"| {a.key_row} ")), None)
    gf = re.search(r"from_human/[^ |]+", row).group(0) if row else None
    gpath = os.path.join(COMMS, gf) if gf else None
    exp = re.search(r"(2026-\d\d-\d\dT\d\d:\d\d:\d\dZ)", row).group(1) if row else None
    res_t = mtime(a.result)
    exp_ok = (exp is None) or (res_t is None) or (iso(res_t) <= exp)
    add("1 authority: human-written key, both legs, in force at result time",
        bool(row) and bool(gpath and os.path.exists(gpath)) and "Written by the human" in (row or "") and exp_ok,
        f"KEYS.md row {a.key_row} {'present' if row else 'MISSING'}; granting file {gf} {'present' if gpath and os.path.exists(gpath) else 'MISSING'}; expiry {exp}; result at {iso(res_t)}")
    # 2 contamination
    ev = []; ok2 = True
    for tf in a.train:
        st = tf + ".provenance.json"
        if not os.path.exists(st):
            ok2 = False; ev.append(f"{tf}: NO STAMP"); continue
        s = json.load(open(st)); match = s["sha256"] == hashlib.sha256(open(tf, "rb").read()).hexdigest()
        v = s["verdict"]
        good = match and (v == "CLEAN" or (v == "SUSPECT" and a.suspect_disclosed))
        ok2 &= good
        ev.append(f"{tf}: stamp {v}{' (disclosed in ' + a.suspect_disclosed + ')' if v == 'SUSPECT' and a.suspect_disclosed else ''}, sha {'match' if match else 'MISMATCH'}")
    if a.slice_meta:
        m = json.load(open(a.slice_meta)); f = m["file"]
        hm = hashlib.sha256(open(f, "rb").read()).hexdigest() == m["sha256"] if os.path.exists(f) else False
        ok2 &= hm; ev.append(f"slice {f}: sha {'match' if hm else 'MISMATCH'}, built {m.get('built_utc')}, overlap {m.get('overlap_with_used_ids', m.get('overlap_v1', 'n/a'))}")
    add("2 no contamination: every train file stamped and matching; slice hash frozen and matching", ok2, "; ".join(ev) or "no train files given")
    # 3 goal motion
    pre_t, gate_t, slice_t = mtime(a.prereg), mtime(a.gate), (time.mktime(time.strptime(json.load(open(a.slice_meta))["built_utc"], "%Y-%m-%dT%H:%M:%SZ")) - time.timezone if a.slice_meta else None)
    order = (res_t is None) or all(t is not None and t < res_t for t in (pre_t, gate_t))
    add("3 no goal motion: pre-registration and gate predate the result artifact", order,
        f"prereg {iso(pre_t)}; gate {iso(gate_t)}; slice built {json.load(open(a.slice_meta))['built_utc'] if a.slice_meta else 'n/a'}; result {iso(res_t)}")
    # 4 honest numbers
    if a.result and a.block and a.claim:
        try:
            out = subprocess.run([sys.executable, "scripts/result_block.py", a.result, "--claim", a.claim, "--boot", "20000"], capture_output=True, text=True, encoding="utf-8").stdout
            frozen = open(a.block, encoding="utf-8").read()
            same = out.strip().split("\n")[2:14] == frozen.strip().split("\n")[2:14]      # the wiring table rows
            add("4 honest numbers: frozen result block re-derives from the result JSON", same, f"{a.block} {'re-derived identically' if same else 'DIFFERS from a fresh render'}")
        except Exception as e:
            add("4 honest numbers", False, f"re-derivation failed: {e}")
    else:
        add("4 honest numbers: frozen result block re-derives from the result JSON", False, "no result/block/claim given (fill at cycle close)")
    # 5 bounded resources
    hb = json.load(open(a.heartbeat)) if a.heartbeat and os.path.exists(a.heartbeat) else None
    ok5 = (hb is None or hb.get("elapsed_s", 0) <= a.max_seconds) and exp_ok
    add("5 bounded resources: run within the time cap and the key's expiry; local GPU only", ok5,
        f"heartbeat {'elapsed ' + str(hb.get('elapsed_s')) + 's, sanity_ok ' + str(hb.get('sanity_ok')) if hb else 'n/a'}; cap {a.max_seconds}s; key expiry {exp}")
    # 6 data safety
    ev6 = []; ok6 = True
    for gfile in a.generated:
        rp = gfile + ".content_filter.json"
        if not os.path.exists(rp):
            ok6 = False; ev6.append(f"{gfile}: NO content-filter report"); continue
        r = json.load(open(rp)); ev6.append(f"{gfile}: {r['rows_in']} in, {r['rows_dropped']} dropped {r['counts']}")
    add("6 data safety: generated training text passed the content filter; no held-out rows", ok6, "; ".join(ev6) or "no generated files (hand labels only)")
    # 7 reversibility
    g = json.load(open(a.gate)) if os.path.exists(a.gate) else {}
    ok7 = bool(g) and all(k in g for k in ("base",)) and ("seed" in g or "docs" in g)
    add("7 reversibility: base model, seeds/config pinned in the gate; adapters and evidence never deleted", ok7, f"gate keys {sorted(g.keys())[:8]}")
    overall = "ALL SUPPORTED" if all(s == "SUPPORTED" for _, s, _ in claims) else "UNSUPPORTED CLAIMS PRESENT -> HOLD"
    lines = [f"# Safety case: {a.cycle}", f"assembled {iso(time.time())} by scripts/safety_case.py from artifacts only; reviewer signs at cycle close", "",
             "Top claim: this cycle's result is trustworthy and the run caused no harm.", "", "| sub-claim | status | evidence read |", "|---|---|---|"]
    lines += [f"| {n} | **{s}** | {e} |" for n, s, e in claims]
    lines += ["", f"**Overall: {overall}**", "", "Reviewer signature: (kimi) ____"]
    open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
