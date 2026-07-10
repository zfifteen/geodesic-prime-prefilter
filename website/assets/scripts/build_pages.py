#!/usr/bin/env python3
"""Rebuild atlas HTML pages with saturated editorial plate packs."""

from __future__ import annotations

from pathlib import Path

SITE = Path(__file__).resolve().parents[2]

NAV = """
        <li><a href="index.html">Home</a></li>
        <li><a href="gaps.html">Gaps</a></li>
        <li><a href="mechanism.html">Mechanism</a></li>
        <li><a href="laws.html">Laws</a></li>
        <li><a href="generator.html">Generator</a></li>
        <li><a href="cryptology.html">Cryptology</a></li>
        <li><a href="evidence.html">Evidence</a></li>
        <li><a href="glossary.html">Glossary</a></li>
        <li><a href="about.html">About</a></li>
"""

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400&family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/main.css">
  {extra_head}
</head>
<body>
  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="index.html">
        <span class="brand-mark">Prime Gap Structure</span>
        <span class="brand-sub">Educational course</span>
      </a>
      <button class="nav-toggle" type="button" aria-label="Menu" aria-expanded="false">☰</button>
      <ul class="nav-links">
{nav}
      </ul>
    </div>
  </header>
  <main>
"""

FOOT = """
  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <h4>Prime Gap Structure</h4>
        <p style="color:var(--text-muted);font-size:0.95rem;margin:0">{footer_blurb}</p>
      </div>
      <div>
        <h4>Course</h4>
        <ul>
          <li><a href="gaps.html">Gaps</a></li>
          <li><a href="laws.html">Laws</a></li>
          <li><a href="cryptology.html">Cryptology</a></li>
          <li><a href="evidence.html">Evidence</a></li>
        </ul>
      </div>
      <div>
        <h4>Research source</h4>
        <ul>
          <li><a href="https://github.com/zfifteen/prime-gap-structure" rel="noopener noreferrer" target="_blank">Repository</a></li>
          <li><a href="https://github.com/zfifteen/prime-gap-structure/blob/main/PROOF.md" rel="noopener noreferrer" target="_blank">PROOF.md</a></li>
          <li><a href="https://github.com/zfifteen/prime-gap-structure/blob/main/docs/RESULTS.md" rel="noopener noreferrer" target="_blank">RESULTS.md</a></li>
        </ul>
      </div>
    </div>
    <div class="wrap footer-note">
      Educational surface with saturated visual plates. Theorem status is controlled by PROOF.md.
      Measured tables certify implementations inside stated regimes.
    </div>
  </footer>
  <script src="js/main.js"></script>
  <script src="js/labs.js"></script>
  <script src="js/figures.js"></script>
  {extra_js}
</body>
</html>
"""


def fig(chapter: str, file: str, fig_id: str, caption: str, overlay: str = "scan", wide: bool = False) -> str:
    cls = "figure figure-wide" if wide else "figure"
    return f"""
<figure class="{cls}">
  <div class="figure-frame" data-overlay="{overlay}">
    <img src="assets/plates/{chapter}/{file}" alt="" loading="lazy" width="1600" height="900">
  </div>
  <figcaption class="figure-caption">
    <span class="figure-id">{fig_id}</span>
    {caption}
  </figcaption>
</figure>
"""


def tile_grid(chapter: str, items: list[tuple[str, str, str, str]], cols: int = 3) -> str:
    # items: file, id, caption, overlay
    parts = [f'<div class="figure-tile-grid cols-{cols}">']
    for file, fid, cap, ov in items:
        parts.append(fig(chapter, file, fid, cap, ov))
    parts.append("</div>")
    return "\n".join(parts)


def process_strip(chapter: str, items: list[tuple[str, str, str, str]], steps: int) -> str:
    parts = [f'<div class="figure-process steps-{steps}">']
    for file, fid, cap, ov in items:
        parts.append(fig(chapter, file, fid, cap, ov))
    parts.append("</div>")
    return "\n".join(parts)


def split_block(chapter: str, file: str, fig_id: str, caption: str, prose: str, overlay="scan", flip=False) -> str:
    flip_cls = " figure-split is-flip" if flip else " figure-split"
    return f"""
<div class="{flip_cls.strip()}">
  <div class="figure-split-visual">
    {fig(chapter, file, fig_id, caption, overlay)}
  </div>
  <div class="prose">{prose}</div>
</div>
"""


def page(title, desc, body, footer_blurb, extra_head="", extra_js=""):
    return (
        HEAD.format(title=title, desc=desc, extra_head=extra_head, nav=NAV)
        + body
        + FOOT.format(footer_blurb=footer_blurb, extra_js=extra_js)
    )


def write(name: str, html: str):
    path = SITE / name
    path.write_text(html, encoding="utf-8")
    print("wrote", path.name, "bytes", path.stat().st_size)


def build_home():
    body = f"""
    <section class="hero wrap">
      <p class="kicker rise">A public course in structure, not chance</p>
      <h1 class="rise rise-delay-1">The integers after a prime<br>are not noise.</h1>
      <hr class="gold-rule" style="margin-inline:auto">
      <p class="lead rise rise-delay-2">
        Prime Gap Structure is a research program about what sits between consecutive primes:
        the ordered chamber of composites, the way divisor counts mark that chamber,
        and the deterministic laws that name the next prime.
      </p>
      <div class="hero-actions rise rise-delay-3">
        <a class="btn btn-primary" href="gaps.html">Begin the course</a>
        <a class="btn btn-ghost" href="laws.html">What is proved</a>
      </div>
    </section>

    <section class="wrap">
      {fig("home","01-hero-chamber.png","Fig. 00.01","The course opens on a chamber: two endpoint walls and a field of interior structure between them. The gap is a readable object, not empty space.", "endpoints", True)}
    </section>

    <section class="section-tight wrap">
      <div class="grid-3">
        <article class="card pillar">
          <span class="status status-proved">Proved</span>
          <h3>Next prime from structure</h3>
          <p>Given a known prime, exact divisor counts on the integers after it determine the next prime.</p>
        </article>
        <article class="card pillar">
          <span class="status status-proved">Proved</span>
          <h3>A distinguished composite</h3>
          <p>Inside a nonempty gap, one interior integer is selected by a leftmost minimum-divisor rule.</p>
        </article>
        <article class="card pillar">
          <span class="status status-proved">Proved</span>
          <h3>Bounded compression</h3>
          <p>That selected witness cannot sit arbitrarily far from the left prime. The bound is on the witness offset.</p>
        </article>
      </div>
      {tile_grid("home", [
        ("03-pillar-nextprime.png","Fig. 00.02","Pillar I as a rising order-mark among quieter bars: the first pure two-divisor height after a known prime.","bars"),
        ("04-pillar-maximizer.png","Fig. 00.03","Pillar II as a highlighted interior landmark: the leftmost minimum-divisor composite in the chamber.","witness"),
        ("05-pillar-compression.png","Fig. 00.04","Pillar III as a short gold measuring interval from the left wall: bounded witness offset, not raw gap mythology.","scan"),
      ])}
    </section>

    <section class="section wrap">
      <p class="kicker">How to read this course</p>
      <h2>Two voices, one status discipline</h2>
      <hr class="gold-rule">
      {split_block("home","06-dual-voice.png","Fig. 00.05","Dual depth: a quieter upper field over a denser lattice underneath. The site teaches in two voices without changing what is proved.","<p class='lead' style='max-width:none'>The main text is a museum guide: plain objects first, then the mechanism, then the name.</p><p>When a section can go deeper without changing claim status, open a <strong style='color:var(--champagne)'>Deeper</strong> panel. Full teaching captions under every plate keep the gallery readable.</p>","scan")}
      {fig("home","07-status-materials.png","Fig. 00.06","Status as physical materials: proved, measured, unresolved, hypothesis, and audit are different substances in the exhibition, not interchangeable labels.","seal")}
      <div class="lab" id="lab-status">
        <div class="lab-header">
          <h3 class="lab-title">Status label lab</h3>
          <span class="lab-hint">Tap a label</span>
        </div>
        <div class="status-grid">
          <div class="status-list lab-controls" style="flex-direction:column;margin:0">
            <button type="button" data-status="proved">Proved</button>
            <button type="button" data-status="measured">Measured</button>
            <button type="button" data-status="unresolved">Unresolved</button>
            <button type="button" data-status="hypothesis">Hypothesis</button>
            <button type="button" data-status="audit">Audit</button>
          </div>
          <div class="status-panel" id="lab-status-panel"></div>
        </div>
      </div>
    </section>

    <section class="section wrap" style="padding-top:0">
      <p class="kicker">Interactive map</p>
      <h2>The story in five stations</h2>
      <hr class="gold-rule">
      {fig("home","08-flow-stations.png","Fig. 00.07","Five stations on one path: known prime, chamber, divisor structure, next prime, status labels. The course is a walk, not a random gallery shuffle.","chain", True)}
      <div class="lab" id="lab-home-flow">
        <div class="flow">
          <button type="button" class="flow-node is-active" data-flow="p">Known prime p</button>
          <span class="flow-arrow">→</span>
          <button type="button" class="flow-node" data-flow="chamber">Chamber after p</button>
          <span class="flow-arrow">→</span>
          <button type="button" class="flow-node" data-flow="structure">Divisor structure</button>
          <span class="flow-arrow">→</span>
          <button type="button" class="flow-node" data-flow="q">Next prime q</button>
          <span class="flow-arrow">→</span>
          <button type="button" class="flow-node" data-flow="status">Status labels</button>
        </div>
        <p class="lab-caption" id="lab-home-flow-caption">A known prime is the only required start. Nothing is sampled at random.</p>
      </div>
    </section>

    <section class="section wrap">
      <p class="kicker">Full public atlas</p>
      <h2>Course map</h2>
      <hr class="gold-rule">
      {fig("home","02-course-atlas.png","Fig. 00.08","The atlas as a constellation of nodes. Each chapter is a station with its own plate pack and labs.","chain", True)}
      <div class="grid-3">
        <a class="card course-card" href="gaps.html"><div class="card-index">01</div><h3>What is a prime gap?</h3><p>The open stretch between consecutive primes.</p></a>
        <a class="card course-card" href="mechanism.html"><div class="card-index">02</div><h3>How PGS works</h3><p>Divisor counts and leftmost minimum selection.</p></a>
        <a class="card course-card" href="laws.html"><div class="card-index">03</div><h3>What is proved</h3><p>Three universal pillars, stated carefully.</p></a>
        <a class="card course-card" href="generator.html"><div class="card-index">04</div><h3>The generator</h3><p>Known prime in, next prime out.</p></a>
        <a class="card course-card" href="cryptology.html"><div class="card-index">05</div><h3>Cryptology front</h3><p>Endpoint chains and residual honesty.</p></a>
        <a class="card course-card" href="evidence.html"><div class="card-index">06</div><h3>Evidence surfaces</h3><p>Measured regimes, exact and labeled.</p></a>
        <a class="card course-card" href="glossary.html"><div class="card-index">07</div><h3>Glossary</h3><p>Names after objects.</p></a>
        <a class="card course-card" href="about.html"><div class="card-index">08</div><h3>Program status</h3><p>What is live, measured, and open.</p></a>
      </div>
      {tile_grid("home", [
        ("11-gap-abstract.png","Fig. 00.09","A smaller abstract of the gap object used throughout the atlas.","endpoints"),
        ("14-endpoint-pair.png","Fig. 00.10","Twin endpoint marks: the visual seed of every chamber story.","endpoints"),
        ("10-gold-field.png","Fig. 00.11","Residual gold field: structure that can remain after a path is incomplete.","residual"),
      ], 3)}
    </section>

    <section class="section wrap text-center">
      <p class="kicker">Research source</p>
      <h2>This course is educational</h2>
      <hr class="gold-rule" style="margin-inline:auto">
      {fig("home","09-proof-seals.png","Fig. 00.12","Formal authority stays in the research repository. Plates teach objects; PROOF.md controls theorem status.","seal", True)}
      {fig("home","12-closing-constellation.png","Fig. 00.13","Closing constellation of the home gallery: structure across the void, still quiet, still exact about status.","chain", True)}
      {fig("home","13-museum-wall.png","Fig. 00.14","A museum-wall grid: every chapter ahead will hang plates at this density.","scan", True)}
      <div class="hero-actions">
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure" rel="noopener noreferrer" target="_blank">GitHub repository</a>
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure/blob/main/PROOF.md" rel="noopener noreferrer" target="_blank">PROOF.md</a>
      </div>
    </section>
"""
    write(
        "index.html",
        page(
            "Prime Gap Structure · Educational Course",
            "A public educational course on Prime Gap Structure with a saturated visual plate gallery.",
            body,
            "A deterministic research program on ordered prime-gap structure, taught as a luxury exhibition.",
        ),
    )


def chapter_shell(kicker, h1, lead, chapter_body):
    return f"""
    <div class="page-hero wrap">
      <p class="kicker">{kicker}</p>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div>
    <section class="section wrap">
      {chapter_body}
    </section>
"""


def build_gaps():
    body = chapter_shell(
        "01 · Gaps",
        "What is a prime gap?",
        "Take two primes that sit next to each other in the list of primes. Everything strictly between them is composite. That open stretch is the gap.",
        f"""
      {fig("gaps","01-hero-gap.png","Fig. 01.01","Hero plate for the gap: endpoint walls and a dense interior of composite structure. This is the first object of the course.","endpoints", True)}
      <div class="prose">
        <h2>A picture you can hold</h2>
        <hr class="gold-rule">
        <p>Start at the prime 89. The next prime is 97. Between them live the composites 90 through 96. That list is the interior of the gap.</p>
        <p>The gap is not a void. It is a short hallway of ordinary integers, each with its own divisor pattern.</p>
      </div>
      {tile_grid("gaps", [
        ("02-two-walls.png","Fig. 01.02","Two walls only: the minimal image of consecutive primes as endpoint marks.","endpoints"),
        ("03-interior-composites.png","Fig. 01.03","Interior composites as a bar field. Heights later track divisor load; here they establish presence.","bars"),
        ("04-hallway.png","Fig. 01.04","Hallway reading of the chamber: walkable structure between walls.","scan"),
      ])}
      {split_block("gaps","09-gap-question.png","Fig. 01.05","The gap question is geometric: where does the interval after a known prime close?","<h2>Why this matters</h2><p>Many stories jump to “is this number prime?” That is a candidate question. This course asks a gap question: what structure does the interval carry, and where does it end?</p>","scan")}
      <div class="gallery-band">
        <p class="gallery-band-title">Gap scale gallery</p>
        {process_strip("gaps", [
          ("05-tiny-gap.png","Fig. 01.06","Tiny gap: almost no interior. Still a chamber, even when thin.","endpoints"),
          ("06-medium-gap.png","Fig. 01.07","Medium gap: enough interior for a selected landmark to appear.","witness"),
          ("07-long-gap.png","Fig. 01.08","Longer gap: more composite structure, same endpoint grammar.","scan"),
        ], 3)}
      </div>
      <div class="lab" id="lab-gap-ruler">
        <div class="lab-header"><h3 class="lab-title">Gap ruler lab</h3><span class="lab-hint">Bar height tracks divisor count τ</span></div>
        <div class="lab-controls">
          <button type="button" data-gap="11-13">11 → 13</button>
          <button type="button" data-gap="89-97">89 → 97</button>
          <button type="button" data-gap="113-127">113 → 127</button>
        </div>
        <div class="lab-stage" id="lab-ruler-stage"></div>
        <p class="lab-caption" id="lab-ruler-caption"></p>
      </div>
      {tile_grid("gaps", [
        ("08-ruler-ticks.png","Fig. 01.09","Ruler ticks along an ordered walk: the gap is measured from left to right.","scan"),
        ("10-composite-field.png","Fig. 01.10","Composite field without yet naming the witness. Presence before selection.","bars"),
        ("11-open-interval.png","Fig. 01.11","Open interval emphasis: the interior is the working room.","endpoints"),
        ("12-closing-wall.png","Fig. 01.12","Closing wall: the next prime as the right endpoint of the story.","endpoints"),
        ("13-structure-not-void.png","Fig. 01.13","Structure, not void: nodes of relation inside the chamber idea.","chain"),
        ("14-gap-recap.png","Fig. 01.14","Recap strip: walls, path, and closure as one exhibition sentence.","chain"),
      ], 3)}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="mechanism.html">Next: How PGS works</a>
        <a class="btn btn-ghost" href="index.html">Course home</a>
      </div>
        """,
    )
    write(
        "gaps.html",
        page(
            "What is a prime gap? · Prime Gap Structure",
            "Visual course chapter on prime gaps as chambers of composite structure.",
            body,
            "Educational course · Chapter 01",
            extra_head='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">',
            extra_js="""
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>document.addEventListener("DOMContentLoaded",function(){if(window.renderMathInElement){renderMathInElement(document.body,{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}]});}});</script>
""",
        ),
    )


def build_mechanism():
    body = chapter_shell(
        "02 · Mechanism",
        "How PGS works",
        "Count the positive divisors of each integer after a known prime. The first time that count is exactly two, you have the next prime. Inside the gap, the first integer with the smallest divisor count is a distinguished landmark.",
        f"""
      {fig("mechanism","01-hero-walk.png","Fig. 02.01","The ordered walk after a known prime: left endpoint bright, interior bars, right endpoint waiting to be forced by structure.","scan", True)}
      {tile_grid("mechanism", [
        ("02-divisor-count.png","Fig. 02.02","Divisor count as bar height: load visible before any name is attached.","bars"),
        ("03-tau-two.png","Fig. 02.03","The special height of two-divisor purity: the visual cue for a prime in this exhibition language.","bars"),
        ("04-ordered-scan.png","Fig. 02.04","Ordered scan energy along the baseline: increasing integers, no random jumps.","scan"),
      ])}
      <div class="prose">
        <h2>The walk after a known prime</h2>
        <hr class="gold-rule">
        <p>You are given a prime <code>p</code>. Look at <code>p+1</code>, then <code>p+2</code>, and so on. For each integer, compute how many positive divisors it has. The first later integer with divisor count 2 is the next prime <code>q</code>.</p>
      </div>
      {fig("mechanism","05-chamber-landmark.png","Fig. 02.05","Chamber with a selected landmark glowing inside the interior. The mechanism is not only endpoints; it is the ordered inside.","witness", True)}
      <div class="lab" id="lab-chamber">
        <div class="lab-header"><h3 class="lab-title">Chamber diagram lab</h3><span class="lab-hint">Endpoints and selected witness</span></div>
        <div class="lab-controls">
          <button type="button" data-chamber="89">89 → 97</button>
          <button type="button" data-chamber="113">113 → 127</button>
        </div>
        <div class="lab-stage" id="lab-chamber-stage"></div>
        <p class="lab-caption" id="lab-chamber-caption"></p>
      </div>
      {split_block("mechanism","06-leftmost-min.png","Fig. 02.06","Leftmost minimum-divisor selection: first lightest load wins.","<h2>The landmark inside the gap</h2><p>When the gap has a nonempty interior, find the smallest divisor count that appears, then take the first integer that achieves it. That selected witness is a proved maximizer of a fixed comparison score.</p>","witness", True)}
      {tile_grid("mechanism", [
        ("07-comparison-score.png","Fig. 02.07","Comparison score as a peaking field among bars.","bars"),
        ("08-zero-excess.png","Fig. 02.08","Zero-excess coordinate as a calm central seal: primes sit at zero excess.","seal"),
        ("09-not-lottery.png","Fig. 02.09","Not a lottery: quiet geometry instead of random candidate noise.","scan"),
        ("10-deterministic-path.png","Fig. 02.10","Deterministic path of stations from start to closure.","chain"),
        ("11-interior-scan.png","Fig. 02.11","Interior scan across a longer chamber.","witness"),
        ("12-score-peak.png","Fig. 02.12","Score peak localized on the selected mark.","bars"),
        ("13-objects-strip.png","Fig. 02.13","Object strip: the mechanism’s inventory as linked nodes.","chain"),
        ("14-mechanism-recap.png","Fig. 02.14","Recap: twin marks after the walk has closed.","endpoints"),
      ], 2)}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="laws.html">Next: What is proved</a>
        <a class="btn btn-ghost" href="gaps.html">Back: Gaps</a>
      </div>
        """,
    )
    write(
        "mechanism.html",
        page(
            "How PGS works · Prime Gap Structure",
            "Mechanism chapter: divisor counts, ordered walk, selected witness.",
            body,
            "Educational course · Chapter 02",
            extra_head='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">',
            extra_js="""
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>document.addEventListener("DOMContentLoaded",function(){if(window.renderMathInElement){renderMathInElement(document.body,{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}]});}});</script>
""",
        ),
    )


def build_laws():
    body = chapter_shell(
        "03 · Laws",
        "What is proved",
        "Three universal pillars stand in the formal proof reference. This page states them in public language. None is a heuristic, a benchmark slogan, or a probability claim.",
        f"""
      {fig("laws","01-hero-pillars.png","Fig. 03.01","Three-law constellation: the exhibition’s formal core rendered as linked structural nodes.","chain", True)}
      {process_strip("laws", [
        ("02-pillar-I.png","Fig. 03.02","Pillar I plate: ordered walk to the next prime.","scan"),
        ("03-pillar-II.png","Fig. 03.03","Pillar II plate: interior maximizer landmark.","witness"),
        ("04-pillar-III.png","Fig. 03.04","Pillar III plate: bounded compression interval.","scan"),
      ], 3)}
      <div class="prose">
        <p><span class="status status-proved">Proved · universal</span></p>
        <h2>Pillar I · Next prime from divisor counts</h2>
        <hr class="gold-rule">
        <p>Start with a known prime. Walk integers above it in order. Stop at the first integer with exactly two positive divisors. That integer is the next prime.</p>
      </div>
      {fig("laws","05-next-prime-law.png","Fig. 03.05","Law I as a full-width walk: the first pure endpoint after the chamber is forced by structure.","scan", True)}
      <div class="prose">
        <h2>Pillar II · The interior maximizer</h2>
        <hr class="gold-rule">
        <p>Inside a nonempty gap, the leftmost minimum-divisor interior integer uniquely maximizes the comparison score.</p>
      </div>
      {fig("laws","06-maximizer-law.png","Fig. 03.06","Law II as chamber geometry with a unique interior crown.","witness", True)}
      <div class="prose">
        <h2>Pillar III · Universal bounded compression</h2>
        <hr class="gold-rule">
        <p>The selected witness offset from the left prime is bounded by a dynamic cutoff at logarithmic-square scale.</p>
        <div class="callout callout-boundary">
          <div class="callout-title">Boundary · read carefully</div>
          <p>This bounds the selected-witness offset <code>w − p</code>. It does not by itself prove RH, PNT, or every classical formulation of Cramér’s conjecture for raw gap size <code>q − p</code>.</p>
        </div>
      </div>
      {tile_grid("laws", [
        ("07-compression-law.png","Fig. 03.07","Compression law as a short gold measure from the left wall.","scan"),
        ("08-square-branch.png","Fig. 03.08","Square-branch closure as nested seals at the same scale language.","seal"),
        ("09-boundary-rh.png","Fig. 03.09","Boundary plate: quiet restraint where claims stop.","scan"),
        ("10-dynamic-cutoff.png","Fig. 03.10","Dynamic cutoff as a finite gold interval, not an infinite leash.","scan"),
        ("11-three-seals.png","Fig. 03.11","Three seals: formal completeness of the local pillar set.","seal"),
        ("12-speak-carefully.png","Fig. 03.12","Speak carefully: status materials stay distinct.","seal"),
        ("13-universal-field.png","Fig. 03.13","Universal field atmosphere for theorems that hold under stated hypotheses.","residual"),
        ("14-laws-recap.png","Fig. 03.14","Recap chain of the three pillars.","chain"),
      ], 2)}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="generator.html">Next: Generator</a>
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure/blob/main/PROOF.md" rel="noopener noreferrer" target="_blank">Research source · PROOF.md</a>
      </div>
        """,
    )
    write(
        "laws.html",
        page(
            "What is proved · Prime Gap Structure",
            "Three universal pillars of Prime Gap Structure with visual plates.",
            body,
            "Educational course · Chapter 03",
            extra_head='<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">',
            extra_js="""
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
  <script>document.addEventListener("DOMContentLoaded",function(){if(window.renderMathInElement){renderMathInElement(document.body,{delimiters:[{left:"\\\\[",right:"\\\\]",display:true},{left:"\\\\(",right:"\\\\)",display:false}]});}});</script>
""",
        ),
    )


def build_generator():
    body = chapter_shell(
        "04 · Generator",
        "Known prime in.<br>Next prime out.",
        "The Minimal PGS Generator turns the gap story into a production contract: given a known prime, emit the successor prime as a minimal record.",
        f"""
      {fig("generator","01-hero-pair.png","Fig. 04.01","Hero pair: two monoliths for the minimal record of start and successor.","endpoints", True)}
      {tile_grid("generator", [
        ("02-minimal-record.png","Fig. 04.02","Minimal record as twin marks only. Diagnostics live elsewhere.","endpoints"),
        ("03-clean-stream.png","Fig. 04.03","Clean stream: quiet field without clutter icons.","scan"),
        ("13-json-pair-abstract.png","Fig. 04.04","Abstract of the pair contract without readable code noise.","endpoints"),
      ])}
      <div class="prose">
        <pre>{{"p": 89, "q": 97}}</pre>
        <p>That record says only what matters. No confidence fields. No source labels inside the stream.</p>
        <h2>A different question than “is this prime?”</h2>
        <hr class="gold-rule">
        <p>The generator asks where the interval after a known prime closes.</p>
      </div>
      {fig("generator","04-gap-question.png","Fig. 04.05","Gap-question plate: chamber first, output second.","endpoints", True)}
      {tile_grid("generator", [
        ("05-not-candidate-loop.png","Fig. 04.06","Not a candidate lottery loop: bars without random rejection theater.","bars"),
        ("06-contract.png","Fig. 04.07","Contract seal for p to q under deterministic selection.","seal"),
        ("07-unresolved-gate.png","Fig. 04.08","Unresolved gate: incomplete ring when the rule does not close.","residual"),
        ("08-audit-after.png","Fig. 04.09","Audit after generation: separate material, downstream only.","seal"),
        ("09-evidence-surface.png","Fig. 04.10","Evidence surface grid for implementation regimes.","scan"),
        ("10-high-scale.png","Fig. 04.11","High-scale decade windows as a constellation of tested stations.","chain"),
        ("11-sidecar.png","Fig. 04.12","Sidecar diagnostics as a quieter ornament, not the main stream.","scan"),
        ("12-production-path.png","Fig. 04.13","Production path stations from input prime to emitted pair.","chain"),
        ("14-generator-recap.png","Fig. 04.14","Recap walk of the generator story.","scan"),
      ], 3)}
      <div class="table-wrap">
        <table>
          <thead><tr><th>Surface</th><th>Result</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td><code>11 .. 1,000,000</code></td><td><code>78494 / 78494</code> · 0 unresolved · 0 audit failures</td><td><span class="status status-measured">Measured</span></td></tr>
            <tr><td><code>10^8</code> through <code>10^18</code></td><td><code>2816 / 2816</code> · 0 unresolved · 0 audit failures</td><td><span class="status status-measured">Measured</span></td></tr>
            <tr><td><code>11 .. 100,000</code></td><td><code>9588 / 9588</code> exact outputs · 0 failures</td><td><span class="status status-measured">Measured</span></td></tr>
          </tbody>
        </table>
      </div>
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="cryptology.html">Next: Cryptology</a>
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure/blob/main/docs/PRIME_GAP_GENERATOR.md" rel="noopener noreferrer" target="_blank">Research source · generator doc</a>
      </div>
        """,
    )
    write(
        "generator.html",
        page(
            "The generator · Prime Gap Structure",
            "Minimal PGS Generator chapter with visual plate gallery.",
            body,
            "Educational course · Chapter 04",
        ),
    )


def build_cryptology():
    body = chapter_shell(
        "05 · Cryptology",
        "Factorization-adjacent research, without the classical script",
        "Full public technical brief: endpoint chains, floor transport, reciprocal closure, residual state, and structural certificates. Not ordinary search over candidate factors.",
        f"""
      {fig("cryptology","01-hero-modulus.png","Fig. 05.01","Modulus plane with reciprocal loop energy: the cryptology front’s opening object.","chain", True)}
      <div class="callout callout-boundary">
        <div class="callout-title">Status discipline</div>
        <p>Nothing here claims RSA is broken at scale. Ladder rows are measured inside exact case IDs. Open cases remain unresolved.</p>
      </div>
      {fig("cryptology","02-frame-lock.png","Fig. 05.02","Frame lock: the research begins from locked structure, not a bag of secret guesses.","seal")}
      {process_strip("cryptology", [
        ("03-endpoint-chain.png","Fig. 05.03","Locked endpoint chain as ordered stations.","chain"),
        ("04-floor-transport.png","Fig. 05.04","Floor transport across the modulus plane.","scan"),
        ("05-reciprocal-closure.png","Fig. 05.05","Reciprocal closure as concentric seal geometry.","seal"),
        ("06-residual-state.png","Fig. 05.06","Residual mist when closure is unfinished.","residual"),
        ("07-certificate.png","Fig. 05.07","Structural certificate seal when invariants finish.","seal"),
      ], 5)}
      <div class="lab" id="lab-modulus">
        <div class="lab-header"><h3 class="lab-title">Modulus-link map lab</h3><span class="lab-hint">Click each station</span></div>
        <div class="mod-map">
          <div class="mod-step" data-mod="1"><div class="mod-step-num">1</div><div><h4>Locked endpoint chain</h4><p>Ordered public endpoints as the working object.</p></div></div>
          <div class="mod-step" data-mod="2"><div class="mod-step-num">2</div><div><h4>Floor transport</h4><p>Carry structure through the modulus by floor-scale maps.</p></div></div>
          <div class="mod-step" data-mod="3"><div class="mod-step-num">3</div><div><h4>Reciprocal closure</h4><p>Ask whether reciprocal endpoint structure closes consistently.</p></div></div>
          <div class="mod-step" data-mod="4"><div class="mod-step-num">4</div><div><h4>Residual state</h4><p>What remains when the certificate is not finished.</p></div></div>
          <div class="mod-step" data-mod="5"><div class="mod-step-num">5</div><div><h4>Certificate or unresolved</h4><p>Emit structure, or refuse to fake closure.</p></div></div>
        </div>
        <div class="lab-stage" style="margin-top:1rem" id="lab-mod-detail"></div>
      </div>
      {tile_grid("cryptology", [
        ("08-unresolved.png","Fig. 05.08","Unresolved as an honest incomplete ring.","residual"),
        ("09-public-ladder.png","Fig. 05.09","Public ladder grid for measured case rows.","scan"),
        ("10-no-factor-bag.png","Fig. 05.10","Refusal plate: no candidate-factor bag as the first frame.","scan"),
        ("11-transport-loop.png","Fig. 05.11","Transport loop path across stations.","chain"),
        ("12-endpoint-class.png","Fig. 05.12","Endpoint class as twin resolved marks on a measured case.","endpoints"),
        ("13-honesty-wall.png","Fig. 05.13","Honesty wall: materials for what we will not claim.","seal"),
        ("14-crypto-recap.png","Fig. 05.14","Recap modulus plane for the chapter close.","chain"),
      ], 2)}
      <div class="table-wrap">
        <table>
          <thead><tr><th>Case ID</th><th>Public outcome</th><th>Status</th></tr></thead>
          <tbody>
            <tr><td><code>rsa_v2_40bit_static_001</code></td><td>Endpoint class <code>(1048559, 1048589)</code></td><td><span class="status status-measured">Measured · resolved</span></td></tr>
            <tr><td><code>rsa_v2_50bit_static_001</code></td><td>Reciprocal carrier misalignment</td><td><span class="status status-unresolved">Unresolved</span></td></tr>
            <tr><td><code>rsa_v2_64bit_static_001</code></td><td>Endpoint class <code>(3221225473, 3221275501)</code></td><td><span class="status status-measured">Measured · resolved</span></td></tr>
          </tbody>
        </table>
      </div>
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="evidence.html">Next: Evidence</a>
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure/blob/main/research/06-cryptology-rsa/docs/endpoint_structure_law.md" rel="noopener noreferrer" target="_blank">Research source · endpoint structure law</a>
      </div>
        """,
    )
    write(
        "cryptology.html",
        page(
            "Cryptology front · Prime Gap Structure",
            "Public technical brief on PGS cryptology with saturated visual plates.",
            body,
            "Educational course · Chapter 05",
        ),
    )


def build_evidence():
    body = chapter_shell(
        "06 · Evidence",
        "Measured surfaces, exact regimes",
        "Public map of implementation and experiment evidence. Every row is a tested regime. None of these tables is a substitute for universal theorems in PROOF.md.",
        f"""
      {fig("evidence","01-hero-surfaces.png","Fig. 06.01","Evidence as a lit grid of regimes: exact cells, not vague clouds of success.","scan", True)}
      {fig("evidence","02-measured-not-proved.png","Fig. 06.02","Measured is not proved: different materials in the status exhibition.","seal")}
      {tile_grid("evidence", [
        ("03-generator-surface.png","Fig. 06.03","Generator surface grid for production regimes.","scan"),
        ("04-decade-windows.png","Fig. 06.04","Decade windows as linked high-scale stations.","chain"),
        ("05-recursive-walk.png","Fig. 06.05","Recursive walk surface: step-to-step recovery geometry.","scan"),
        ("06-zero-unresolved.png","Fig. 06.06","Zero-unresolved seal for clean measured surfaces inside stated ranges.","seal"),
        ("07-audit-corroboration.png","Fig. 06.07","Audit corroboration as secondary bar field, not a theorem.","bars"),
        ("08-rsa-ladder.png","Fig. 06.08","RSA ladder table geometry for public cases.","scan"),
        ("09-resolved-row.png","Fig. 06.09","Resolved row seal for a closed public case.","seal"),
        ("10-unresolved-row.png","Fig. 06.10","Unresolved row residual for an open public case.","residual"),
        ("11-regime-map.png","Fig. 06.11","Regime map constellation across surfaces.","chain"),
        ("12-not-inflation.png","Fig. 06.12","Anti-inflation ornament: beauty without claim stretch.","scan"),
        ("13-evidence-grid.png","Fig. 06.13","Dense evidence grid wall.","scan"),
        ("14-evidence-recap.png","Fig. 06.14","Recap chain of evidence discipline.","chain"),
      ], 3)}
      <div class="table-wrap">
        <table>
          <thead><tr><th>Regime</th><th>Record</th><th>Notes</th></tr></thead>
          <tbody>
            <tr><td><code>11 .. 1,000,000</code></td><td><code>78494 / 78494</code> · 0 unresolved · 0 audit failures</td><td>Generator surface</td></tr>
            <tr><td><code>11 .. 100,000</code></td><td><code>9588 / 9588</code> exact outputs</td><td>Production path</td></tr>
            <tr><td><code>10^8</code> … <code>10^18</code></td><td><code>2816 / 2816</code></td><td>Decade windows</td></tr>
          </tbody>
        </table>
      </div>
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="glossary.html">Next: Glossary</a>
        <a class="btn btn-ghost" href="https://github.com/zfifteen/prime-gap-structure/blob/main/docs/RESULTS.md" rel="noopener noreferrer" target="_blank">Research source · RESULTS.md</a>
      </div>
        """,
    )
    write(
        "evidence.html",
        page(
            "Evidence surfaces · Prime Gap Structure",
            "Measured regimes with visual plate gallery.",
            body,
            "Educational course · Chapter 06",
        ),
    )


def build_glossary():
    terms = [
        ("02-prime-gap-term.png", "Fig. 07.02", "Prime gap", "Open stretch between consecutive primes.", "endpoints"),
        ("03-chamber-term.png", "Fig. 07.03", "Chamber", "Interior region after a known prime before the next.", "scan"),
        ("04-tau-term.png", "Fig. 07.04", "Divisor count", "How many positive divisors an integer has.", "bars"),
        ("05-witness-term.png", "Fig. 07.05", "Selected witness", "Leftmost interior minimum-divisor integer.", "witness"),
        ("06-gwr-term.png", "Fig. 07.06", "Leftmost Minimum-Divisor Rule", "Selection rule for the witness; maximizer of F.", "witness"),
        ("07-dni-term.png", "Fig. 07.07", "DNI / zero excess", "Exact coordinate where primes sit at zero excess.", "seal"),
        ("08-compression-term.png", "Fig. 07.08", "Bounded compression", "Proved bound on selected-witness offset.", "scan"),
        ("09-generator-term.png", "Fig. 07.09", "Minimal generator", "Known prime in, next prime out.", "endpoints"),
        ("10-unresolved-term.png", "Fig. 07.10", "Unresolved state", "Explicit non-answer when structure does not close.", "residual"),
        ("11-endpoint-term.png", "Fig. 07.11", "Endpoint chain", "Ordered structural endpoints for traversal.", "chain"),
        ("12-certificate-term.png", "Fig. 07.12", "Structural certificate", "Finished public structural emission.", "seal"),
        ("13-audit-term.png", "Fig. 07.13", "Audit", "Downstream verification; does not choose the answer.", "seal"),
    ]
    tiles = tile_grid(
        "glossary",
        [(f, i, f"<strong style='color:var(--champagne)'>{title}.</strong> {cap}", ov) for f, i, title, cap, ov in terms],
        3,
    )
    body = chapter_shell(
        "07 · Glossary",
        "Names after objects",
        "Project vocabulary is useful once you can picture the thing being named. Each entry hangs under a plate.",
        f"""
      {fig("glossary","01-hero-lexicon.png","Fig. 07.01","Lexicon constellation: every term is a node after an object, not a password before understanding.","chain", True)}
      {tiles}
      {fig("glossary","14-glossary-mosaic.png","Fig. 07.14","Closing mosaic of the glossary wall.","chain", True)}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="about.html">Next: Program status</a>
        <a class="btn btn-ghost" href="index.html">Course home</a>
      </div>
        """,
    )
    write(
        "glossary.html",
        page(
            "Glossary · Prime Gap Structure",
            "Visual glossary of Prime Gap Structure terms.",
            body,
            "Educational course · Chapter 07",
        ),
    )


def build_about():
    body = chapter_shell(
        "08 · About",
        "Program status map",
        "What is proved, what is implemented, what is measured, and what remains open. A public continuity surface, not a biography.",
        f"""
      {fig("about","01-hero-status.png","Fig. 08.01","Status materials for the whole program, hung as an opening wall.","seal", True)}
      {process_strip("about", [
        ("02-proved-band.png","Fig. 08.02","Proved band: local universal pillars under PROOF.md.","seal"),
        ("03-implemented-band.png","Fig. 08.03","Implemented band: Minimal Generator v1.1 as production milestone.","endpoints"),
        ("04-measured-band.png","Fig. 08.04","Measured band: exact regimes and clean surfaces.","scan"),
        ("05-research-band.png","Fig. 08.05","Active research band: modulus-link cryptology front.","chain"),
        ("06-open-band.png","Fig. 08.06","Open band: residual honesty where claims stop.","residual"),
      ], 5)}
      <div class="status-map">
        <div class="status-map-row"><div><span class="status status-proved">Proved</span></div><div><h3 style="margin-top:0">Universal local pillars</h3><p>Direct next-prime rule, interior maximizer, universal bounded compression including Prime-Square Proximity.</p></div></div>
        <div class="status-map-row"><div><span class="status status-measured">Implemented</span></div><div><h3 style="margin-top:0">Minimal PGS Generator v1.1</h3><p>Production milestone, not the whole active project.</p></div></div>
        <div class="status-map-row"><div><span class="status status-measured">Measured</span></div><div><h3 style="margin-top:0">Generator and walk surfaces</h3><p>Including 11..1,000,000 full exact output and decade windows through 10^18.</p></div></div>
        <div class="status-map-row"><div><span class="status status-measured">Active research</span></div><div><h3 style="margin-top:0">Cryptology and modulus-link work</h3><p>Endpoint chains, transport, residual state, certificates on public ladders.</p></div></div>
        <div class="status-map-row"><div><span class="status status-unresolved">Open / careful</span></div><div><h3 style="margin-top:0">What this program does not claim here</h3><p>PROOF.md does not itself prove RH. Cryptology ladders are not a universal RSA-scale theorem.</p></div></div>
      </div>
      {tile_grid("about", [
        ("07-not-claims.png","Fig. 08.07","Quiet plate for claims we refuse to inflate.","scan"),
        ("08-lean-mirror.png","Fig. 08.08","Lean formalization as a mirror seal in progress.","seal"),
        ("09-site-role.png","Fig. 08.09","This website’s role: education and exhibition, not proof authority.","chain"),
        ("10-source-links.png","Fig. 08.10","Research source path as linked stations.","chain"),
        ("11-continuity.png","Fig. 08.11","Continuity walk for future sessions and readers.","scan"),
        ("12-program-map.png","Fig. 08.12","Program map constellation.","chain"),
        ("13-about-recap.png","Fig. 08.13","Recap chamber for the status map.","endpoints"),
        ("14-final-seal.png","Fig. 08.14","Final seal of the public course.","seal"),
      ], 2)}
      <div class="hero-actions" style="justify-content:flex-start;margin-top:2.5rem">
        <a class="btn btn-primary" href="index.html">Return to course home</a>
        <a class="btn btn-ghost" href="gaps.html">Start chapter 01</a>
      </div>
        """,
    )
    write(
        "about.html",
        page(
            "Program status · Prime Gap Structure",
            "Public status map with saturated visual plates.",
            body,
            "Educational course · Chapter 08",
        ),
    )


def main():
    build_home()
    build_gaps()
    build_mechanism()
    build_laws()
    build_generator()
    build_cryptology()
    build_evidence()
    build_glossary()
    build_about()
    print("all pages rebuilt")


if __name__ == "__main__":
    main()
