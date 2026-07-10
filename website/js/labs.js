/**
 * Visual explainer suite for the public PGS course.
 * Fixed didactic examples only. No primality-search engine.
 */
(function () {
  "use strict";

  /* --- Gap ruler: consecutive primes and interior composites --- */
  var GAP_EXAMPLES = {
    "11-13": {
      p: 11,
      q: 13,
      interior: [12],
      tau: { 11: 2, 12: 6, 13: 2 },
      w: null,
      note: "A tiny gap. Between 11 and 13 sits only 12. The next prime is the first later integer whose divisor count is exactly 2."
    },
    "89-97": {
      p: 89,
      q: 97,
      interior: [90, 91, 92, 93, 94, 95, 96],
      tau: { 89: 2, 90: 12, 91: 4, 92: 6, 93: 4, 94: 4, 95: 4, 96: 12, 97: 2 },
      w: 91,
      note: "From 89 to 97. Every interior integer is composite. The leftmost interior integer with the smallest divisor count is 91 (four divisors). That selected witness is a proved structural object inside the gap, not a random pick."
    },
    "113-127": {
      p: 113,
      q: 127,
      interior: [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126],
      tau: {
        113: 2, 114: 8, 115: 4, 116: 6, 117: 6, 118: 4, 119: 4,
        120: 16, 121: 3, 122: 4, 123: 4, 124: 6, 125: 4, 126: 12, 127: 2
      },
      w: 121,
      note: "A longer chamber. 121 is a square (11×11) with three divisors. In this gap it is the leftmost minimum-divisor interior integer."
    }
  };

  function barHeight(tau) {
    if (tau === 2) return 96;
    if (tau === 3) return 72;
    if (tau === 4) return 58;
    if (tau <= 6) return 42;
    if (tau <= 12) return 28;
    return 18;
  }

  function renderRuler(key) {
    var stage = document.getElementById("lab-ruler-stage");
    var caption = document.getElementById("lab-ruler-caption");
    if (!stage) return;
    var ex = GAP_EXAMPLES[key];
    if (!ex) return;

    var nums = [ex.p].concat(ex.interior).concat([ex.q]);
    var html = '<div class="ruler" role="img" aria-label="Gap ruler for primes ' + ex.p + " and " + ex.q + '">';
    nums.forEach(function (n) {
      var tau = ex.tau[n];
      var isPrime = tau === 2;
      var isW = ex.w === n;
      var cls = "tick " + (isPrime ? "is-prime" : "is-composite");
      if (isW) cls += " is-selected";
      var h = barHeight(tau);
      var title = n + " · τ=" + tau + (isW ? " · selected witness" : isPrime ? " · prime" : " · composite");
      html +=
        '<div class="' + cls + '" title="' + title + '">' +
        '<div class="tick-bar" style="height:' + h + 'px"></div>' +
        '<div class="tick-label">' + n + "</div>" +
        "</div>";
    });
    html += "</div>";
    stage.innerHTML = html;
    if (caption) {
      caption.innerHTML =
        "<strong style=\"color:var(--champagne)\">" +
        ex.p +
        " → " +
        ex.q +
        "</strong>. " +
        ex.note +
        (ex.w
          ? " Highlighted bar: selected witness <code>w = " + ex.w + "</code>."
          : " Twin-adjacent gap: no interior witness.");
    }
  }

  function initRuler() {
    var root = document.getElementById("lab-gap-ruler");
    if (!root) return;
    root.querySelectorAll("[data-gap]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelectorAll("[data-gap]").forEach(function (b) {
          b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
        renderRuler(btn.getAttribute("data-gap"));
      });
    });
    var first = root.querySelector("[data-gap]");
    if (first) {
      first.classList.add("is-active");
      renderRuler(first.getAttribute("data-gap"));
    }
  }

  /* --- Status label explorer --- */
  var STATUS_COPY = {
    proved: {
      title: "Proved",
      body: "A mathematical theorem established in the formal proof reference PROOF.md. State it directly. Do not hedge with “likely,” “suggests,” or “validated so far.” Scope is exactly the hypotheses written in the proof."
    },
    measured: {
      title: "Measured",
      body: "An implementation or experiment surface with an exact tested regime (for example a prime range or a fixed RSA toy ladder). Measured results certify code and regimes. They do not bound universal theorems unless the proof itself says so."
    },
    unresolved: {
      title: "Unresolved",
      body: "The PGS rule or invariant did not close the case. The honest output is an explicit unresolved state. Unresolved does not mean “try a classical search instead.” It means the structural path has not finished."
    },
    hypothesis: {
      title: "Hypothesis",
      body: "A candidate law, residual map, or research direction that is not proved and not yet settled by measurement. Useful for planning the next probe. Not a claim of fact."
    },
    audit: {
      title: "Audit",
      body: "A downstream check that verifies an already produced answer. Audit may use classical tools for confirmation. Audit does not choose the PGS answer and is not itself a proof."
    }
  };

  function renderStatus(key) {
    var panel = document.getElementById("lab-status-panel");
    if (!panel) return;
    var item = STATUS_COPY[key];
    if (!item) return;
    var chipClass =
      key === "proved"
        ? "status-proved"
        : key === "measured"
          ? "status-measured"
          : key === "unresolved"
            ? "status-unresolved"
            : "status-hypothesis";
    panel.innerHTML =
      '<span class="status ' +
      chipClass +
      '">' +
      item.title +
      "</span>" +
      "<h4 style=\"margin:1rem 0 0.5rem;font-family:var(--font-display);font-size:1.4rem;color:var(--text)\">" +
      item.title +
      " means</h4>" +
      "<p style=\"margin:0\">" +
      item.body +
      "</p>";
  }

  function initStatusExplorer() {
    var root = document.getElementById("lab-status");
    if (!root) return;
    root.querySelectorAll("[data-status]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelectorAll("[data-status]").forEach(function (b) {
          b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
        renderStatus(btn.getAttribute("data-status"));
      });
    });
    var first = root.querySelector("[data-status]");
    if (first) {
      first.classList.add("is-active");
      renderStatus(first.getAttribute("data-status"));
    }
  }

  /* --- Chamber / endpoint story --- */
  var CHAMBERS = {
    "89": {
      p: 89,
      q: 97,
      cells: [
        { n: 90, tag: "τ12" },
        { n: 91, tag: "τ4 · w", w: true },
        { n: 92, tag: "τ6" },
        { n: 93, tag: "τ4" },
        { n: 94, tag: "τ4" },
        { n: 95, tag: "τ4" },
        { n: 96, tag: "τ12" }
      ],
      story:
        "Start at the known prime 89. The chamber is the open interval of composites until the next prime 97. The structure inside the chamber is read before the endpoint is named. The leftmost minimum-divisor interior integer is 91."
    },
    "113": {
      p: 113,
      q: 127,
      cells: [
        { n: 115, tag: "τ4" },
        { n: 119, tag: "τ4" },
        { n: 121, tag: "τ3 · w", w: true },
        { n: 125, tag: "τ4" }
      ],
      story:
        "A wider chamber from 113 to 127. Not every composite is shown. The selected witness 121 is a square with three divisors: the leftmost minimum load in this interior."
    }
  };

  function renderChamber(key) {
    var stage = document.getElementById("lab-chamber-stage");
    var caption = document.getElementById("lab-chamber-caption");
    if (!stage) return;
    var c = CHAMBERS[key];
    if (!c) return;
    var cells = c.cells
      .map(function (cell) {
        return (
          '<div class="chamber-cell' +
          (cell.w ? " is-w" : "") +
          '">' +
          cell.n +
          "<br><span style=\"opacity:0.7\">" +
          cell.tag +
          "</span></div>"
        );
      })
      .join("");
    stage.innerHTML =
      '<div class="chamber">' +
      '<div class="chamber-end">p = ' +
      c.p +
      "</div>" +
      '<div class="chamber-interior">' +
      cells +
      "</div>" +
      '<div class="chamber-end">q = ' +
      c.q +
      "</div>" +
      "</div>";
    if (caption) caption.textContent = c.story;
  }

  function initChamber() {
    var root = document.getElementById("lab-chamber");
    if (!root) return;
    root.querySelectorAll("[data-chamber]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        root.querySelectorAll("[data-chamber]").forEach(function (b) {
          b.classList.remove("is-active");
        });
        btn.classList.add("is-active");
        renderChamber(btn.getAttribute("data-chamber"));
      });
    });
    var first = root.querySelector("[data-chamber]");
    if (first) {
      first.classList.add("is-active");
      renderChamber(first.getAttribute("data-chamber"));
    }
  }

  /* --- Modulus-link conceptual map --- */
  var MOD_STEPS = {
    "1": {
      title: "Locked endpoint chain",
      body: "Begin from a public structural path: an ordered chain of endpoints that the program treats as the working object. The frame is not “guess a factor and test it.”"
    },
    "2": {
      title: "Floor transport through the modulus",
      body: "Carry information through the public modulus using floor-scale transport maps. The modulus is a structural medium, not a bag of candidates."
    },
    "3": {
      title: "Reciprocal endpoint closure",
      body: "Ask whether reciprocal structure closes consistently. Closure is a deterministic check on the transported chain, not a product-identity hunt."
    },
    "4": {
      title: "Modulus-link residual",
      body: "What remains after transport and closure is residual state: structure that is still informative but not yet a finished certificate."
    },
    "5": {
      title: "Certificate or unresolved",
      body: "If the invariants finish, emit a structural certificate (for example a public endpoint class on a measured toy ladder). If not, return unresolved. Do not silently switch to classical factorization."
    }
  };

  function renderMod(key) {
    var panel = document.getElementById("lab-mod-detail");
    if (!panel) return;
    var s = MOD_STEPS[key];
    if (!s) return;
    panel.innerHTML =
      "<h4 style=\"margin:0 0 0.5rem;font-family:var(--font-display);font-size:1.45rem;color:var(--champagne)\">" +
      s.title +
      "</h4><p style=\"margin:0\">" +
      s.body +
      "</p>";
  }

  function initModMap() {
    var root = document.getElementById("lab-modulus");
    if (!root) return;
    root.querySelectorAll("[data-mod]").forEach(function (el) {
      el.addEventListener("click", function () {
        root.querySelectorAll("[data-mod]").forEach(function (b) {
          b.classList.remove("is-active");
        });
        el.classList.add("is-active");
        renderMod(el.getAttribute("data-mod"));
      });
    });
    var first = root.querySelector("[data-mod]");
    if (first) {
      first.classList.add("is-active");
      renderMod(first.getAttribute("data-mod"));
    }
  }

  /* --- Home flow (optional) --- */
  function initHomeFlow() {
    var root = document.getElementById("lab-home-flow");
    if (!root) return;
    var caption = document.getElementById("lab-home-flow-caption");
    var copy = {
      p: "A known prime is the only required start. Nothing is sampled at random.",
      chamber: "The integers after p form a chamber of composites until the next prime appears.",
      structure: "Divisor counts on those integers carry the gap’s internal order.",
      q: "The first later integer with exactly two positive divisors is the next prime q.",
      status: "Every claim is labeled: proved, measured, unresolved, or still a hypothesis."
    };
    root.querySelectorAll(".flow-node").forEach(function (node) {
      node.addEventListener("click", function () {
        root.querySelectorAll(".flow-node").forEach(function (n) {
          n.classList.remove("is-active");
        });
        node.classList.add("is-active");
        var key = node.getAttribute("data-flow");
        if (caption && copy[key]) caption.textContent = copy[key];
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initRuler();
    initStatusExplorer();
    initChamber();
    initModMap();
    initHomeFlow();
  });
})();
