#!/usr/bin/env python3
"""Build the self-contained HTML gallery from catalog + captions + out/ assets."""

from __future__ import annotations

import html
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

VIS = Path(__file__).resolve().parents[1]
LIBRARY = VIS / "library"
GALLERY = VIS / "gallery"
sys.path.insert(0, str(Path(__file__).resolve().parent))

from catalog_lib import load_all_entries, load_catalog  # noqa: E402


CSS = """
:root {
  color-scheme: dark;
  --bg: #0e0e10;
  --surface: #16161a;
  --line: #2a2a30;
  --text: #e8e4d9;
  --muted: #9a9588;
  --gold: #c9a962;
  --gold-bright: #e0c47a;
  --theorem: #c9a962;
  --measured: #7ec8e3;
  --audit: #9a9588;
  --hypothesis: #e0a060;
  --unresolved: #c0c0c0;
  --invalidated: #ff6b5a;
  --legacy: #a090c0;
  --mixed: #d0c090;
  --editorial: #8a9a7a;
}
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--bg); color: var(--text);
  font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif;
  line-height: 1.55;
}
a { color: var(--gold-bright); text-decoration: none; }
a:hover { text-decoration: underline; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 24px 18px 64px; }
header.site {
  border-bottom: 1px solid var(--line);
  background: linear-gradient(180deg, #141416, var(--bg));
  position: sticky; top: 0; z-index: 5;
}
header.site .wrap { display: flex; gap: 16px; align-items: baseline; justify-content: space-between; flex-wrap: wrap; padding-bottom: 14px; padding-top: 14px; }
.brand { font-weight: 700; letter-spacing: 0.02em; color: var(--gold-bright); }
.brand small { display: block; font-weight: 400; color: var(--muted); font-size: 0.8rem; }
nav a { margin-right: 12px; color: var(--muted); font-size: 0.92rem; }
nav a:hover { color: var(--gold-bright); }
h1 { font-size: 1.9rem; margin: 0.2em 0 0.4em; color: var(--gold-bright); }
h2 { font-size: 1.25rem; margin-top: 1.6em; border-bottom: 1px solid var(--line); padding-bottom: 0.3em; }
.lead { color: var(--muted); max-width: 62ch; }
.filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 18px 0 8px; }
.chip {
  border: 1px solid var(--line); background: var(--surface);
  color: var(--muted); border-radius: 999px; padding: 4px 10px; font-size: 0.8rem; cursor: pointer;
}
.chip.active, .chip:hover { border-color: var(--gold); color: var(--gold-bright); }
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 18px;
}
.card {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 10px;
  overflow: hidden;
  display: flex; flex-direction: column;
}
.card img {
  width: 100%; aspect-ratio: 16/10; object-fit: cover; background: #000;
  border-bottom: 1px solid var(--line);
}
.card .body { padding: 12px 14px 14px; display: flex; flex-direction: column; gap: 8px; flex: 1; }
.card h3 { margin: 0; font-size: 1.02rem; }
.meta { font-size: 0.78rem; color: var(--muted); }
.status {
  display: inline-block; font-size: 0.72rem; font-weight: 600;
  letter-spacing: 0.04em; text-transform: uppercase;
  border: 1px solid var(--line); border-radius: 4px; padding: 2px 6px;
}
.status-theorem { color: var(--theorem); border-color: var(--theorem); }
.status-measured { color: var(--measured); border-color: var(--measured); }
.status-audit { color: var(--audit); border-color: var(--audit); }
.status-hypothesis { color: var(--hypothesis); border-color: var(--hypothesis); }
.status-unresolved { color: var(--unresolved); border-color: var(--unresolved); }
.status-invalidated { color: var(--invalidated); border-color: var(--invalidated); }
.status-legacy { color: var(--legacy); border-color: var(--legacy); }
.status-mixed { color: var(--mixed); border-color: var(--mixed); }
.status-editorial { color: var(--editorial); border-color: var(--editorial); }
.figure-frame {
  background: #000; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; margin: 16px 0;
}
.figure-frame img { width: 100%; display: block; }
.prose { max-width: 72ch; }
.prose h2 { font-size: 1.1rem; }
.prose code { background: #1c1c22; padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }
.panel {
  background: var(--surface); border: 1px solid var(--line); border-radius: 8px;
  padding: 12px 14px; margin: 16px 0;
}
.panel dt { color: var(--muted); font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; }
.panel dd { margin: 0 0 10px 0; }
.hidden { display: none !important; }
#filter-empty { margin: 18px 0; color: var(--muted); font-size: 0.92rem; }
.detail { font-size: 0.8rem; color: var(--muted); line-height: 1.35; }
footer { margin-top: 48px; color: var(--muted); font-size: 0.85rem; border-top: 1px solid var(--line); padding-top: 16px; }
.tags span {
  display: inline-block; margin: 0 6px 4px 0; padding: 1px 6px;
  border-radius: 4px; background: #1c1c22; color: var(--muted); font-size: 0.75rem;
}
"""


JS = """
(function () {
  const cards = Array.from(document.querySelectorAll('[data-entry]'));
  const chips = Array.from(document.querySelectorAll('[data-filter]'));
  const empty = document.getElementById('filter-empty');
  let status = 'all';
  let tier = 'all';
  function apply() {
    let visible = 0;
    cards.forEach(card => {
      const okStatus = status === 'all' || card.dataset.status === status;
      const okTier = tier === 'all' || card.dataset.tier === tier;
      const show = okStatus && okTier;
      card.classList.toggle('hidden', !show);
      if (show) visible += 1;
    });
    if (empty) {
      empty.classList.toggle('hidden', visible > 0);
      empty.textContent = visible > 0
        ? ''
        : 'No entries match these filters (try status: all and tier: all).';
    }
    chips.forEach(chip => {
      const kind = chip.dataset.filter;
      const val = chip.dataset.value;
      let active = false;
      if (kind === 'status') active = status === val;
      if (kind === 'tier') active = tier === val;
      chip.classList.toggle('active', active);
      chip.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
  }
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const kind = chip.dataset.filter;
      const val = chip.dataset.value;
      if (kind === 'status') status = val;
      if (kind === 'tier') tier = val;
      apply();
    });
  });
  apply();
})();
"""


def inline_md(text: str) -> str:
    """Escape HTML and apply light inline markdown: `code` and **bold**."""
    parts = text.split("`")
    acc: list[str] = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            acc.append(f"<code>{html.escape(part)}</code>")
            continue
        # Bold segments outside code spans.
        segs = part.split("**")
        for j, seg in enumerate(segs):
            esc = html.escape(seg)
            if j % 2 == 1:
                acc.append(f"<strong>{esc}</strong>")
            else:
                acc.append(esc)
    return "".join(acc)


def md_to_html(md: str, *, skip_first_h1: bool = True) -> str:
    """Tiny markdown subset: headings, paragraphs, fenced code, inline code/bold, lists."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    in_code = False
    code_buf: list[str] = []
    para: list[str] = []
    in_list = False
    saw_h1 = False

    def close_list() -> None:
        nonlocal in_list
        if in_list:
            out.append("</ul>")
            in_list = False

    def flush_para() -> None:
        nonlocal para
        if para:
            close_list()
            text = " ".join(para)
            out.append(f"<p>{inline_md(text)}</p>")
            para = []

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                code_buf = []
                in_code = False
            else:
                flush_para()
                close_list()
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue
        if not stripped:
            flush_para()
            close_list()
            continue
        if line.startswith("## "):
            flush_para()
            close_list()
            out.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
            continue
        if line.startswith("# "):
            flush_para()
            close_list()
            if skip_first_h1 and not saw_h1:
                saw_h1 = True
                continue
            saw_h1 = True
            out.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
            continue
        if line.startswith("- "):
            flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline_md(line[2:].strip())}</li>")
            continue
        close_list()
        para.append(stripped)

    flush_para()
    close_list()
    if in_code:
        out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
    return "\n".join(out)


def copy_assets(entries: list[dict]) -> None:
    assets = GALLERY / "assets"
    if assets.exists():
        shutil.rmtree(assets)
    assets.mkdir(parents=True)
    for entry in entries:
        eid = entry["id"]
        src = LIBRARY / "out" / eid / "plot.png"
        dest_dir = assets / eid
        dest_dir.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copy2(src, dest_dir / "plot.png")
        else:
            # placeholder 1x1 will be missing; entry page notes it
            pass


def page_shell(title: str, body: str, *, extra_head: str = "", active: str = "gallery") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="PGS plot library gallery">
  <link rel="stylesheet" href="css/gallery.css">
  {extra_head}
</head>
<body>
  <header class="site">
    <div class="wrap">
      <div class="brand">PGS Plot Library <small>scientific demos + legacy wraps</small></div>
      <nav>
        <a href="index.html">Gallery</a>
        <a href="../library/README.md">Library README</a>
        <a href="../index.html">Visualizations hub</a>
        <a href="../../website/index.html">Educational course</a>
      </nav>
    </div>
  </header>
  <main class="wrap">
{body}
  </main>
  <footer class="wrap">
    Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}.
    Status chips are mandatory. Editorial plates live under <code>website/</code>.
  </footer>
</body>
</html>
"""


def build_index(entries: list[dict], cat: dict) -> None:
    statuses = sorted({e["status"] for e in entries})
    chips = [
        '<button class="chip active" type="button" data-filter="status" data-value="all" aria-pressed="true">status: all</button>'
    ]
    for s in statuses:
        chips.append(
            f'<button class="chip" type="button" data-filter="status" data-value="{html.escape(s)}" aria-pressed="false">status: {html.escape(s)}</button>'
        )
    chips.append(
        '<button class="chip active" type="button" data-filter="tier" data-value="all" aria-pressed="true">tier: all</button>'
    )
    chips.append(
        '<button class="chip" type="button" data-filter="tier" data-value="0" aria-pressed="false">tier: 0</button>'
    )
    # Only offer tier:1 when at least one entry uses it.
    if any(int(e.get("tier", 99)) == 1 for e in entries):
        chips.append(
            '<button class="chip" type="button" data-filter="tier" data-value="1" aria-pressed="false">tier: 1</button>'
        )

    cards = []
    for e in entries:
        eid = e["id"]
        img = f"assets/{eid}/plot.png"
        has = (LIBRARY / "out" / eid / "plot.png").is_file()
        img_tag = (
            f'<img src="{img}" alt="{html.escape(e["title"])}" loading="lazy">'
            if has
            else '<div class="meta" style="padding:40px 12px">missing plot.png — run run_all_demos.py</div>'
        )
        tags = "".join(f"<span>{html.escape(t)}</span>" for t in e.get("tags", []))
        detail = html.escape(str(e.get("status_detail", ""))[:180])
        cards.append(
            f"""
<article class="card" data-entry data-status="{html.escape(e['status'])}" data-tier="{int(e.get('tier', 99))}">
  <a href="entry/{html.escape(eid)}.html">{img_tag}</a>
  <div class="body">
    <div><span class="status status-{html.escape(e['status'])}">{html.escape(e['status'])}</span></div>
    <h3><a href="entry/{html.escape(eid)}.html">{html.escape(e['title'])}</a></h3>
    <div class="detail">{detail}</div>
    <div class="meta">tier {int(e.get('tier', 99))} · {html.escape(e.get('kind', ''))}</div>
    <div class="meta">{html.escape(e.get('regime', '')[:140])}</div>
    <div class="tags">{tags}</div>
  </div>
</article>"""
        )

    venv_py = "visualizations/library/.venv/bin/python"
    body = f"""
    <h1>Plot gallery</h1>
    <p class="lead">
      Catalog-first demonstrations of Prime Gap Structure objects: chambers, DNI coordinates,
      bounded-compression envelopes, generator surface posters, and modulus-link schematics.
      Each entry carries an explicit status chip, one-line status detail, and regime.
      Version {html.escape(str(cat.get('version', '')))}.
    </p>
    <div class="panel">
      <dl>
        <dt>Library</dt><dd><code>visualizations/library/</code></dd>
        <dt>Regenerate</dt><dd><code>{venv_py} visualizations/scripts/lint_catalog.py &amp;&amp; {venv_py} visualizations/scripts/run_all_demos.py &amp;&amp; {venv_py} visualizations/scripts/build_gallery.py</code></dd>
        <dt>Asset truth</dt><dd><code>library/out/</code> is demo output; <code>gallery/assets/</code> is a build copy. Do not hand-edit gallery PNGs.</dd>
        <dt>Not this gallery</dt><dd>Public educational plates → <code>website/</code>. Historical plot dumps → <code>visualizations/core-diagrams/</code> (non-catalog).</dd>
      </dl>
    </div>
    <div class="filters" role="group" aria-label="Gallery filters">
      {''.join(chips)}
    </div>
    <p id="filter-empty" class="hidden" role="status"></p>
    <div class="grid">
      {''.join(cards)}
    </div>
    <script src="js/gallery.js"></script>
"""
    (GALLERY / "index.html").write_text(page_shell("PGS Plot Gallery", body), encoding="utf-8")


def build_entry_pages(entries: list[dict]) -> None:
    entry_dir = GALLERY / "entry"
    entry_dir.mkdir(parents=True, exist_ok=True)
    for e in entries:
        eid = e["id"]
        has = (LIBRARY / "out" / eid / "plot.png").is_file()
        img_block = (
            f'<div class="figure-frame"><img src="../assets/{html.escape(eid)}/plot.png" alt="{html.escape(e["title"])}"></div>'
            if has
            else '<div class="panel">Plot asset missing. Run <code>run_all_demos.py</code>.</div>'
        )
        refs = "".join(f"<li><code>{html.escape(r)}</code></li>" for r in e.get("chapter_refs", []))
        tags = "".join(f"<span>{html.escape(t)}</span>" for t in e.get("tags", []))
        caption_html = md_to_html(e.get("_caption") or "_No caption.md_", skip_first_h1=True)
        repro = f"visualizations/library/.venv/bin/python visualizations/library/entries/{eid}/demo.py"
        body = f"""
    <p class="meta"><a href="../index.html">← Gallery</a></p>
    <p><span class="status status-{html.escape(e['status'])}">{html.escape(e['status'])}</span>
       <span class="meta"> · tier {int(e.get('tier', 99))} · {html.escape(e.get('kind', ''))}</span></p>
    <h1>{html.escape(e['title'])}</h1>
    <p class="lead">{html.escape(e.get('status_detail', ''))}</p>
    {img_block}
    <div class="panel">
      <dl>
        <dt>Regime</dt><dd>{html.escape(e.get('regime', ''))}</dd>
        <dt>Claim language</dt><dd>{html.escape(e.get('claim_language', 'weak'))}{" · has 10^18 surface flag" if e.get("has_10e18_surface") else ""}</dd>
        <dt>Reproduce</dt><dd><code>{html.escape(repro)}</code></dd>
        <dt>Chapter refs</dt><dd><ul>{refs}</ul></dd>
        <dt>Tags</dt><dd class="tags">{tags}</dd>
      </dl>
    </div>
    <div class="prose">
      {caption_html}
    </div>
"""
        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(e['title'])} · PGS Plot Library</title>
  <link rel="stylesheet" href="../css/gallery.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <div class="brand">PGS Plot Library <small>entry</small></div>
      <nav>
        <a href="../index.html">Gallery</a>
        <a href="../../library/README.md">Library README</a>
        <a href="../../index.html">Visualizations hub</a>
        <a href="../../../website/index.html">Educational course</a>
      </nav>
    </div>
  </header>
  <main class="wrap">
{body}
  </main>
  <footer class="wrap">
    Entry id <code>{html.escape(eid)}</code>. Status separation is mandatory.
  </footer>
</body>
</html>
"""
        (entry_dir / f"{eid}.html").write_text(page, encoding="utf-8")


def main() -> int:
    cat = load_catalog()
    entries = load_all_entries()
    GALLERY.mkdir(parents=True, exist_ok=True)
    (GALLERY / "css").mkdir(exist_ok=True)
    (GALLERY / "js").mkdir(exist_ok=True)
    (GALLERY / "css" / "gallery.css").write_text(CSS, encoding="utf-8")
    (GALLERY / "js" / "gallery.js").write_text(JS, encoding="utf-8")
    copy_assets(entries)
    build_index(entries, cat)
    build_entry_pages(entries)
    print(f"Gallery written to {GALLERY / 'index.html'} ({len(entries)} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
