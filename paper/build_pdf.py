r"""Build paper/comms-loop-architecture.{html,pdf} from the markdown source.

Stdlib + the `markdown` package + headless Chrome/Edge. No pandoc, no TeX.

  python paper/build_pdf.py

The markdown's first lines (H1 title, bold date line, bold author line, repo line)
are replaced by a typeset title block; everything from "## Abstract" on is rendered
as the body.
"""
from __future__ import annotations

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

HERE = Path(__file__).resolve().parent
SRC = HERE / "comms-loop-architecture.md"
OUT_HTML = HERE / "comms-loop-architecture.html"
OUT_PDF = HERE / "comms-loop-architecture.pdf"

BROWSERS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 2.2cm 2.4cm 2.4cm 2.4cm; }
html { -webkit-print-color-adjust: exact; }
body { font-family: Georgia, 'Times New Roman', serif; font-size: 10.5pt; line-height: 1.45;
       color: #111; max-width: 17cm; margin: 0 auto; }
.titleblock { text-align: center; margin: 0 0 1.6em 0; }
.titleblock h1 { font-size: 19pt; line-height: 1.25; margin: 0 0 0.55em 0; font-weight: bold; }
.titleblock .author { font-size: 12pt; margin: 0.15em 0; }
.titleblock .email { font-size: 10pt; color: #333; margin: 0; font-family: Consolas, 'Courier New', monospace; }
.titleblock .meta { font-size: 9.5pt; color: #444; margin: 0.6em 0 0 0; }
.titleblock .meta a { color: #444; text-decoration: none; }
.titleblock hr { border: 0; border-top: 1px solid #999; margin: 1.1em auto 0 auto; width: 60%; }
h2 { font-size: 12.5pt; margin-top: 1.5em; border-bottom: 1px solid #ccc; padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 11pt; margin-top: 1.2em; page-break-after: avoid; }
h2#abstract { text-align: center; border: 0; font-size: 11.5pt; margin-top: 0; }
h2#abstract + p, h2#abstract + p + p { font-size: 9.8pt; margin-left: 1cm; margin-right: 1cm; text-align: justify; }
p { margin: 0.55em 0; text-align: justify; }
code { font-family: Consolas, 'Courier New', monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2px; }
pre { background: #f4f4f4; padding: 8px 10px; font-size: 8.6pt; line-height: 1.35; overflow-x: hidden;
      white-space: pre-wrap; page-break-inside: avoid; border: 1px solid #e2e2e2; }
pre code { background: none; padding: 0; font-size: inherit; }
table { border-collapse: collapse; width: 100%; font-size: 9.2pt; margin: 0.8em 0; page-break-inside: avoid; }
th, td { border: 1px solid #bbb; padding: 3px 6px; vertical-align: top; text-align: left; }
th { background: #eee; }
ul, ol { margin: 0.4em 0 0.6em 1.4em; padding-left: 0.6em; }
li { margin: 0.2em 0; }
#references + ol { font-size: 9pt; }
#references + ol li { margin: 0.25em 0; }
a { color: #1a3d7c; }
"""


def split_front_matter(text: str) -> tuple[dict, str]:
    """Pull title/date/author/email/repo out of the leading lines; return (meta, body_md)."""
    lines = text.splitlines()
    meta = {"title": "", "date": "", "author": "", "email": "", "repo": "", "repo_note": ""}
    i = 0
    while i < len(lines) and not lines[i].startswith("## "):
        ln = lines[i].strip()
        if ln.startswith("# ") and not meta["title"]:
            meta["title"] = ln[2:].strip()
        elif ln.startswith("**Experience report") or ln.startswith("**Technical report"):
            meta["date"] = ln.strip("*").strip()
        elif re.match(r"^\*\*[^*]+\*\*\s*[·\-—]\s*\S+@\S+", ln):
            m = re.match(r"^\*\*([^*]+)\*\*\s*[·\-—]\s*(\S+@\S+)", ln)
            meta["author"], meta["email"] = m.group(1).strip(), m.group(2).strip()
        elif ln.startswith("System and data:"):
            m = re.search(r"<?(https?://\S+?)>?(\s*\((.*)\))?\s*$", ln)
            if m:
                meta["repo"] = m.group(1)
                meta["repo_note"] = m.group(3) or ""
        i += 1
    return meta, "\n".join(lines[i:])


def render(meta: dict, body_md: str) -> str:
    body_html = markdown.markdown(
        body_md,
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
        output_format="html5",
    )
    e = html.escape
    title_block = f"""
<div class="titleblock">
  <h1>{e(meta['title'])}</h1>
  <p class="author">{e(meta['author'])}</p>
  <p class="email">{e(meta['email'])}</p>
  <p class="meta">{e(meta['date'])}</p>
  <p class="meta">Protocol, ledgers, and the full message archive: <a href="{e(meta['repo'])}">{e(meta['repo'])}</a></p>
  <hr>
</div>
"""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>{e(meta['title'])}</title>
<meta name="author" content="{e(meta['author'])}">
<style>{CSS}</style>
</head><body>
{title_block}
{body_html}
</body></html>
"""


def find_browser() -> str | None:
    for p in BROWSERS:
        if Path(p).exists():
            return p
    return shutil.which("chrome") or shutil.which("msedge")


def main() -> int:
    text = SRC.read_text(encoding="utf-8")
    meta, body = split_front_matter(text)
    missing = [k for k in ("title", "author", "email", "date") if not meta[k]]
    if missing:
        print(f"front matter missing {missing}; check the first lines of {SRC.name}", file=sys.stderr)
        return 1
    OUT_HTML.write_text(render(meta, body), encoding="utf-8")
    print(f"wrote {OUT_HTML.name}")

    browser = find_browser()
    if not browser:
        print("no Chrome/Edge found; HTML written, PDF skipped", file=sys.stderr)
        return 2
    cmd = [
        browser, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri(),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if not OUT_PDF.exists():
        print(r.stderr[-2000:], file=sys.stderr)
        return 3
    print(f"wrote {OUT_PDF.name} ({OUT_PDF.stat().st_size} bytes) via {Path(browser).name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
