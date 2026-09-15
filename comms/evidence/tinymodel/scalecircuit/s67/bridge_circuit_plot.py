"""Render the layer x head heatmaps (attention mass on the hop-1 note span minus mass on the gold span in the passage,
at the answer position) and the logit-lens rank curves from bridge_circuit.py's capture.json. Matplotlib if
available, else a self-contained SVG.

    python scripts/bridge_circuit_plot.py scale/results/bridge_circuit/capture.json
"""
import json
import math
import os
import sys

path = sys.argv[1]; out_dir = os.path.dirname(path)
cap = json.load(open(path, encoding="utf-8"))
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    n = len(cap)
    fig, axes = plt.subplots(2, n, figsize=(4.6 * n, 8.5), gridspec_kw={"height_ratios": [3, 1.6]})
    if n == 1:
        axes = np.array([[axes[0]], [axes[1]]])
    for j, (doc, c) in enumerate(cap.items()):
        note = np.array(c["mass"]["note1_in_notes"]); gold = np.array(c["mass"]["gold_in_passage"])
        diff = note - gold
        ax = axes[0, j]
        v = max(0.05, float(np.abs(diff).max()))
        im = ax.imshow(diff, aspect="auto", cmap="RdBu_r", vmin=-v, vmax=v, origin="lower")
        ax.set_title(f"doc {doc}: mass(hop-1 note) - mass(gold span)\nanswer={c['answer_now'][:22]!r} gold={c['gold'][:18]!r}", fontsize=9)
        ax.set_xlabel("head"); ax.set_ylabel("layer")
        fig.colorbar(im, ax=ax, fraction=0.046)
        ax2 = axes[1, j]
        for k, rk in c["lens_rank"].items():
            ax2.plot(range(1, len(rk) + 1), [math.log10(r) for r in rk], label=f"{k} ({c['notes'][0][:12] if k == 'note1' else c['notes'][1][:12] if k == 'note2' and len(c['notes']) > 1 else c['gold'][:12]})")
        ax2.set_xlabel("layer"); ax2.set_ylabel("log10 rank of first token"); ax2.invert_yaxis(); ax2.legend(fontsize=7); ax2.set_title("logit lens at the answer position", fontsize=9)
    fig.suptitle("Qwen2.5-3B-Instruct reader, DEV2 cases: where the answer position looks, and when the note overtakes the gold", fontsize=11)
    fig.tight_layout()
    png = os.path.join(out_dir, "bridge_circuit.png"); fig.savefig(png, dpi=130)
    print("saved", png)
except ImportError:
    print("matplotlib not available; no PNG rendered")
