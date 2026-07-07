"""Correlation analysis engine for remainder vectors vs gap/prime placement.

Implements the functions specified in the Remainder-Gap-Prime Placement
Correlation Analysis Plan (Phase 2).

Design constraints (mandatory):
- Minimal dependencies. Prefer stdlib (collections, math, statistics, json).
- numpy allowed only for convenience in later tables if already present in env;
  core algorithms must have pure-Python reference paths.
- No scikit-learn, no heavy ML, no external solvers for the predictive delta.
- For logistic: either pure Python gradient descent on log-loss or
  closed-form / simple linear probability model where appropriate.
- All functions are deterministic given inputs + explicit seeds/bins.
- Outputs are human tables (list of dicts or printed MD/CSV strings).
- Every function and the report must carry the PGS framing reminder.

This file is developed under the 4-phase procedure.
Phase 1 = this skeleton (signatures + exhaustive descriptive comments).
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Any, Sequence

# ---------------------------------------------------------------------------
# PGS Framing Reminder (present in every public function docstring)
# These computations operate on already-generated records that describe
# ordered prime-gap interior points.  The underlying selection of q and of
# the GWR winner is performed exclusively by the divisor-count / GWR rules.
# Remainder features are observed coordinates only.
# ---------------------------------------------------------------------------


def compute_residue_histograms(
    records: list[dict[str, Any]],
    group_by: Sequence[str] = ("norm_position_bin", "gap_size_bin"),
    moduli_version: str = "M_v1",
) -> dict[str, Any]:
    """Compute marginal frequency tables of each residue class.

    Grouped by the supplied keys (normally normalized position bin and/or
    gap-size bin).

    Phase-1 scaffold comments (logic to be implemented later):
    - For every record compute or read "norm_position_bin" = floor( (k/g)*B )
      where B is a resolution (e.g. 10).
    - Determine gap_size_bin similarly.
    - For each modulus slot i, for each possible residue value, count
      occurrences inside each group.
    - Also produce a "gwr_only" conditioned table and "non_gwr" table.
    - Return nested dicts or a structure easily turned into Markdown/CSV.
    - Must be pure given the records (no global state).
    """
    # Implementation (incremental after scaffold review)
    B = 10  # resolution for normalized position 0.0-1.0 -> 0..9
    counts: dict[tuple, dict[tuple, int]] = defaultdict(lambda: defaultdict(int))
    group_totals: dict[tuple, int] = defaultdict(int)

    for rec in records:
        g = rec.get("g", 0)
        k = rec.get("k", 0)
        vec = rec.get("remainder_vector", ())
        if g <= 0 or not vec:
            continue

        norm = k / g
        pos_bin = min(int(norm * B), B - 1)
        g_bin = min(g // 4, 6)  # coarse gap size bins

        group_key = (pos_bin, g_bin)
        group_totals[group_key] += 1

        for slot, r in enumerate(vec):
            key = (slot, int(r))
            counts[group_key][key] += 1

    # Build human-friendly result
    result: dict[str, Any] = {
        "bins": {"position_resolution": B, "gap_bin_max": 6},
        "groups": {},
    }
    for gk, slot_counts in counts.items():
        posb, gb = gk
        total = group_totals[gk]
        group_data: dict[str, Any] = {"total": total, "slots": {}}
        for (slot, res), c in sorted(slot_counts.items()):
            if slot not in group_data["slots"]:
                group_data["slots"][slot] = {}
            group_data["slots"][slot][res] = {"count": c, "freq": c / total if total else 0.0}
        result["groups"][f"pos{posb}_g{gb}"] = group_data

    return result


def mutual_information(
    residue_feature: Sequence[Any],
    placement_label: Sequence[Any],
    bins: int | None = None,
) -> dict[str, float]:
    """Estimate mutual information between a (binned) remainder-derived feature
    and a placement outcome (e.g. binned termination distance or is_termination_soon).

    Uses histogram counts only (no external MI libraries).

    Phase-1 scaffold:
    - Discretize both sides if continuous (equal-width or quantile bins).
    - Build joint count table + marginals.
    - MI = sum p(x,y) log( p(x,y) / (p(x)p(y)) )
    - Return dict with 'mi', 'n', 'effective_bins', plus optional normalized version.
    """
    if len(residue_feature) != len(placement_label):
        raise ValueError("Inputs must have same length")
    if not residue_feature:
        return {"mi": 0.0, "n": 0, "effective_bins_x": 0, "effective_bins_y": 0, "normalized_mi": 0.0}
    
    counts = defaultdict(int)
    count_x = defaultdict(int)
    count_y = defaultdict(int)
    n = len(residue_feature)
    
    for x, y in zip(residue_feature, placement_label):
        counts[(x, y)] += 1
        count_x[x] += 1
        count_y[y] += 1
        
    mi = 0.0
    for (x, y), c in counts.items():
        pxy = c / n
        px = count_x[x] / n
        py = count_y[y] / n
        mi += pxy * math.log(pxy / (px * py))
        
    hx = -sum((cx / n) * math.log(cx / n) for cx in count_x.values())
    hy = -sum((cy / n) * math.log(cy / n) for cy in count_y.values())
    
    norm_mi = 0.0
    if hx + hy > 0:
        norm_mi = 2 * mi / (hx + hy)
        
    return {
        "mi": mi,
        "n": n,
        "effective_bins_x": len(count_x),
        "effective_bins_y": len(count_y),
        "normalized_mi": norm_mi
    }


def transition_matrix(
    remainder_state_sequence: Sequence[tuple[int, ...] | int | Sequence[int]],
    lag: int = 1,
    state_key: str = "discretized",
) -> dict[str, Any]:
    """Build empirical transition matrix of remainder states (or discretized
    version) with given lag.

    Especially interesting for the final 5-10 positions before termination.

    Supports:
    - A single sequence of states (vectors as tuples or discretized ints).
    - For convenience when passed a list of per-gap near-end sequences, the
      function will aggregate transitions across all provided sequences.
    Returns dict with 'counts' (from_state -> to_state -> int), 'probabilities'
    (row-normalized), 'lag', 'n_transitions'.
    Keys for vector states are tuples (hashable); ints for discretized.
    """
    if lag < 1:
        raise ValueError("lag must be >=1")
    if not remainder_state_sequence:
        return {"counts": {}, "probabilities": {}, "lag": lag, "n_transitions": 0}

    def _is_vector_state(x):
        return isinstance(x, (list, tuple)) and len(x) == 7 and all(isinstance(v, int) for v in x)

    # Robust detection:
    # - If top-level elements are vector-states (len-7 int tuples), treat input as one sequence-of-vectors.
    # - Else if top-level[0] 's elements are vector-states, treat as list-of-sequences.
    sequences: list = []
    first = remainder_state_sequence[0] if remainder_state_sequence else None
    if first is not None and _is_vector_state(first):
        sequences = [remainder_state_sequence]
    elif first is not None and isinstance(first, (list, tuple)) and len(first) > 0 and _is_vector_state(first[0]):
        sequences = list(remainder_state_sequence)
    else:
        sequences = [remainder_state_sequence]

    counts: dict = defaultdict(lambda: defaultdict(int))
    n_trans = 0
    for seq in sequences:
        seq_list = [tuple(int(v) for v in s) if isinstance(s, (list, tuple)) else s for s in seq]
        if len(seq_list) <= lag:
            continue
        for i in range(len(seq_list) - lag):
            prev = seq_list[i]
            curr = seq_list[i + lag]
            pkey = prev if isinstance(prev, tuple) else prev
            ckey = curr if isinstance(curr, tuple) else curr
            counts[pkey][ckey] += 1
            n_trans += 1

    probs: dict = {}
    for pkey, tos in counts.items():
        tot = sum(tos.values())
        if tot > 0:
            probs[pkey] = {ckey: cnt / tot for ckey, cnt in tos.items()}

    return {
        "counts": {k: dict(v) for k, v in counts.items()},
        "probabilities": {k: dict(v) for k, v in probs.items()},
        "lag": lag,
        "n_transitions": n_trans,
    }


def _get_repeat_state(rec: dict[str, Any]) -> tuple[int, ...]:
    """Project to residue signature excluding the large-modulus slot that encodes n itself
    (fixes 'by construction' uniqueness for n < 2310 in remainder_vector built with full M_v1).
    Uses first 6 components (mod up to 210) so that pattern repeats are possible in analysis.
    """
    vec = rec.get("remainder_vector", [])
    return tuple(int(v) for v in vec[:6])

def _count_prior_repeats(vec_seq: list[tuple[int, ...]]) -> list[int]:
    """Pure helper: for a sequence of states (vectors), return list of prior exact-match counts.
    Separated for independent unit testing as required by plan.
    """
    seen: list = []
    counts: list[int] = []
    for v in vec_seq:
        prior = sum(1 for s in seen if s == v)
        counts.append(prior)
        seen.append(v)
    return counts

def compute_intra_gap_repeat_stats(
    records: list[dict[str, Any]],
) -> dict[str, Any]:
    """Pure function: group records into per-gap remainder-vector sequences,
    for each position count exact prior repeats of that vector in the same gap,
    report aggregate frequencies and counts split by relative position (near-end
    vs middle) and classify gaps by presence of repeats in final positions.

    Uses 'p' for gap id, 'k'/'g' for relative position, 'remainder_vector' (projected for state),
    'is_gwr_winner' and 'distance_to_next_prime' (or termination_distance) to determine
    whether prime arrives right after GWR min-d position.

    Late positions defined uniformly as the final min(3, gap_length) records (absolute, works for small g).

    Returns counts, rates, and per-class GWR-immediate-after rates.
    """
    if not records:
        return {"num_gaps": 0, "error": "no records"}

    # Group by gap using 'p', keep order by 'k'
    from collections import defaultdict
    gaps: dict = defaultdict(list)
    for r in records:
        gaps[r["p"]].append(r)

    pos_repeat_counts = {"near_end": [], "middle": [], "all": []}
    gaps_with_late_repeats = 0
    gaps_without = 0
    late_gwr_right_after = 0
    no_late_gwr_right_after = 0
    total_gaps = 0

    for p, grecs in gaps.items():
        total_gaps += 1
        grecs = sorted(grecs, key=lambda x: x.get("k", 0))
        g = grecs[0].get("g", 0) if grecs else 0
        states = [_get_repeat_state(r) for r in grecs]
        prior_counts = _count_prior_repeats(states)
        last_n = min(3, len(grecs))
        has_late_repeat = False
        for i, prior in enumerate(prior_counts):
            pos_repeat_counts["all"].append(prior)
            is_late = i >= len(grecs) - last_n
            if is_late:
                pos_repeat_counts["near_end"].append(prior)
                if prior > 0:
                    has_late_repeat = True
            else:
                pos_repeat_counts["middle"].append(prior)

        if has_late_repeat:
            gaps_with_late_repeats += 1
        else:
            gaps_without += 1

        # Does prime arrive right after GWR min-d position?
        # i.e. the record(s) with is_gwr_winner (or is_current_min_d) has distance==1
        gwr_right_after = False
        for r in grecs:
            is_gwr = r.get("is_gwr_winner") or r.get("is_current_min_d")
            dist = r.get("distance_to_next_prime") or r.get("termination_distance") or 99
            if is_gwr and dist == 1:
                gwr_right_after = True
                break
        if has_late_repeat:
            if gwr_right_after:
                late_gwr_right_after += 1
        else:
            if gwr_right_after:
                no_late_gwr_right_after += 1

    def safe_avg(lst):
        return sum(lst) / len(lst) if lst else 0.0

    def safe_rate(num, den):
        return num / den if den > 0 else 0.0

    return {
        "num_gaps": total_gaps,
        "gaps_with_late_repeats": gaps_with_late_repeats,
        "gaps_without_late_repeats": gaps_without,
        "repeat_freq_near_end": safe_avg([1 if c > 0 else 0 for c in pos_repeat_counts["near_end"]]),
        "repeat_freq_middle": safe_avg([1 if c > 0 else 0 for c in pos_repeat_counts["middle"]]),
        "avg_prior_repeats_near_end": safe_avg(pos_repeat_counts["near_end"]),
        "avg_prior_repeats_middle": safe_avg(pos_repeat_counts["middle"]),
        "gwr_right_after_rate_with_late_repeats": safe_rate(late_gwr_right_after, gaps_with_late_repeats),
        "gwr_right_after_rate_without": safe_rate(no_late_gwr_right_after, gaps_without),
        "late_gwr_right_after_count": late_gwr_right_after,
        "no_late_gwr_right_after_count": no_late_gwr_right_after,
        "note": "late positions = last min(3, gap_len) records (absolute); repeat state = vec[:6] (mod<=210 proj to allow pattern repeats); GWR right after = GWR winner record has dist_to_next==1",
    }


def compute_per_gap_late_repeat_feature(
    records: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Return per-gap summaries with 'late_repeat_count' feature (count of exact repeats of
    the repeat_state in the last min(3,len) positions).
    Uses _get_repeat_state and _count_prior_repeats for consistency and testability.
    """
    from collections import defaultdict
    gaps: dict = defaultdict(list)
    for r in records:
        gaps[r["p"]].append(r)

    results = []
    for p, grecs in gaps.items():
        grecs = sorted(grecs, key=lambda x: x.get("k", 0))
        g = grecs[0].get("g", 0) if grecs else 0
        states = [_get_repeat_state(r) for r in grecs]
        prior_counts = _count_prior_repeats(states)
        last_n = min(3, len(grecs))
        late_count = sum(1 for i in range(len(grecs) - last_n, len(grecs)) if prior_counts[i] > 0)
        # attach to records or summary
        is_gwr_right_after = False
        for r in grecs:
            is_gwr = r.get("is_gwr_winner") or r.get("is_current_min_d")
            dist = r.get("distance_to_next_prime") or r.get("termination_distance") or 99
            if is_gwr and dist == 1:
                is_gwr_right_after = True
                break
        results.append({
            "p": p,
            "g": g,
            "late_repeat_count": late_count,
            "has_late_repeats": late_count > 0,
            "gwr_right_after": is_gwr_right_after,
            "num_records": len(grecs),
        })
    return results


def feature_correlation_matrix(
    feature_list: list[dict[str, float]],
    method: str = "spearman",
) -> list[list[float]]:
    """Compute rank or Pearson correlation matrix among a list of per-gap
    summary features (e.g. entropy_of_remainders, realized_g, avg_d, ...).

    Pure Python implementation of Spearman (rank) or Pearson.

    Phase-1 comments describe:
    - Handling of ties for Spearman.
    - Return as square matrix + feature name order.
    - Also a human 'pairs ranked by |corr|' table.
    """
    if not feature_list:
        return []
    
    features = sorted(list(feature_list[0].keys()))
    
    def rank(vals):
        indexed = sorted(enumerate(vals), key=lambda x: x[1])
        ranks = [0.0] * len(vals)
        i = 0
        while i < len(vals):
            j = i
            while j < len(vals) and indexed[j][1] == indexed[i][1]:
                j += 1
            avg_rank = sum(range(i + 1, j + 1)) / (j - i)
            for k in range(i, j):
                ranks[indexed[k][0]] = avg_rank
            i = j
        return ranks
        
    def pearson(x, y):
        n = len(x)
        if n < 2: return 0.0
        mx, my = sum(x)/n, sum(y)/n
        num = sum((xi - mx)*(yi - my) for xi, yi in zip(x, y))
        den_x = sum((xi - mx)**2 for xi in x)
        den_y = sum((yi - my)**2 for yi in y)
        if den_x == 0 or den_y == 0: return 0.0
        return num / math.sqrt(den_x * den_y)
        
    matrix = []
    
    data = {f: [row[f] for row in feature_list] for f in features}
    
    if method == "spearman":
        data = {f: rank(data[f]) for f in features}
        
    for i, f1 in enumerate(features):
        row = []
        for j, f2 in enumerate(features):
            corr = pearson(data[f1], data[f2])
            row.append(corr)
        matrix.append(row)
        
    # Optionally one could return dict with features and matrix, but signature expects list[list[float]]
    return matrix


def predictive_delta(
    baseline_features: list[dict[str, float]],
    augmented_features: list[dict[str, float]],
    target: list[int | float],
    *,
    model: str = "logistic",
    n_folds: int = 5,
    seed: int = 42,
) -> dict[str, float]:
    """Fit two simple models (baseline vs baseline+remainder features) and
    report the delta in performance (accuracy, log-loss, etc.) on held-out data.

    Pure-Python or minimal closed-form / GD logistic as specified in plan.
    Uses gap-stratified or simple CV.

    Phase-1 scaffold:
    - Split logic described.
    - For logistic: implement gradient descent on binary cross-entropy with
      tiny learning rate / fixed steps (or linear probability model for speed).
    - Return {'baseline_score': , 'augmented_score': , 'delta': , 'metric': }
    - Never use the remainder features to choose which gaps are "test".
    """
    n = len(target)
    if n == 0:
        return {}
        
    def train_predict(X_train, y_train, X_test):
        X_train = [[1.0] + list(row) for row in X_train]
        X_test = [[1.0] + list(row) for row in X_test]
        weights = [0.0] * len(X_train[0])
        lr = 0.01
        epochs = 100
        
        def sigmoid(z):
            if z < -250: return 0.0
            if z > 250: return 1.0
            return 1.0 / (1.0 + math.exp(-z))
            
        for _ in range(epochs):
            for x, y in zip(X_train, y_train):
                pred = sigmoid(sum(w*xi for w, xi in zip(weights, x)))
                err = pred - y
                for i in range(len(weights)):
                    weights[i] -= lr * err * x[i]
                    
        preds = []
        for x in X_test:
            pred = sigmoid(sum(w*xi for w, xi in zip(weights, x)))
            preds.append(pred)
        return preds
        
    def evaluate(features_list):
        if not features_list: return 0.0
        keys = sorted(list(features_list[0].keys()))
        X = [[row[k] for k in keys] for row in features_list]
        
        for j in range(len(keys)):
            col = [X[i][j] for i in range(n)]
            mean = sum(col)/n
            std = math.sqrt(sum((c - mean)**2 for c in col)/n) if n > 0 else 1.0
            if std == 0: std = 1.0
            for i in range(n):
                X[i][j] = (X[i][j] - mean) / std
        
        random.seed(seed)
        indices = list(range(n))
        random.shuffle(indices)
        
        fold_size = n // n_folds if n_folds > 0 else 1
        log_loss_sum = 0.0
        
        for i in range(n_folds):
            start = i * fold_size
            end = (i + 1) * fold_size if i != n_folds - 1 else n
            test_idx = set(indices[start:end])
            train_idx = [idx for idx in indices if idx not in test_idx]
            
            X_train = [X[idx] for idx in train_idx]
            y_train = [target[idx] for idx in train_idx]
            X_test = [X[idx] for idx in test_idx]
            y_test = [target[idx] for idx in test_idx]
            
            preds = train_predict(X_train, y_train, X_test)
            
            for p, y in zip(preds, y_test):
                p = max(min(p, 1 - 1e-15), 1e-15)
                if y == 1:
                    log_loss_sum -= math.log(p)
                else:
                    log_loss_sum -= math.log(1 - p)
                    
        return log_loss_sum / n
        
    base_loss = evaluate(baseline_features)
    aug_loss = evaluate(augmented_features)
    
    return {
        "baseline_log_loss": base_loss,
        "augmented_log_loss": aug_loss,
        "delta": base_loss - aug_loss,
        "metric": "log_loss"
    }


# ---------------------------------------------------------------------------
# Convenience / driver functions for the report workflow
# ---------------------------------------------------------------------------


def load_records(path: Path | str) -> list[dict[str, Any]]:
    """Streaming loader for JSONL (used by all analysis)."""
    p = Path(path)
    out: list[dict[str, Any]] = []
    with p.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                out.append(json.loads(line))
    return out


def run_descriptive_analysis(
    records: list[dict[str, Any]],
    out_dir: Path,
) -> dict[str, Any]:
    """High-level driver that calls the above primitives for the common
    descriptive surfaces and writes human-readable tables.

    Phase-1 comments outline the exact sequence that will be executed:
    histograms → basic MI for key features → per-gap entropy vs g → GWR vs avg
    comparison → write CSVs and append to CORRELATION_REPORT.md.
    """
    # Minimal working driver for validation (will be expanded)
    out_dir.mkdir(parents=True, exist_ok=True)
    h = compute_residue_histograms(records)
    # Write a tiny example table for mod-2 (slot 0)
    lines = ["| pos_bin | gap_bin | res | count | freq |", "|---------|---------|-----|-------|------|"]
    for gname, gdata in sorted(h["groups"].items())[:8]:
        pb, gb = gname.split("_")
        for res, info in sorted(gdata.get("slots", {}).get(0, {}).items()):
            lines.append(f"| {pb} | {gb} | {res} | {info['count']} | {info['freq']:.3f} |")
    (out_dir / "mod2_marginal_sample.md").write_text("\n".join(lines) + "\n")
    return {"histograms_groups": len(h["groups"]), "sample_table_written": True}


def run_full_descriptive(
    records: list[dict[str, Any]],
    out_dir: Path,
) -> dict[str, Any]:
    """Run MI, Spearman, marginals, and repeat stats; write numeric tables."""
    import math
    from collections import defaultdict

    out_dir.mkdir(parents=True, exist_ok=True)

    gaps: dict[Any, list[dict[str, Any]]] = defaultdict(list)
    for rec in records:
        gaps[rec["p"]].append(rec)

    gap_features: list[dict[str, float]] = []
    for grecs in gaps.values():
        grecs.sort(key=lambda r: int(r.get("k", 0)))
        g = float(grecs[0]["g"])
        counts: dict[tuple[int, ...], int] = defaultdict(int)
        for r in grecs:
            vec = tuple(int(v) for v in r["remainder_vector"][:6])
            counts[vec] += 1
        n = len(grecs)
        entropy = 0.0
        for c in counts.values():
            p_val = c / n
            entropy -= p_val * math.log(p_val)
        gap_features.append({"g": g, "entropy": entropy})

    feat_list = [{"g": f["g"], "entropy": f["entropy"]} for f in gap_features]
    corr_matrix = feature_correlation_matrix(feat_list, method="spearman")
    spearman_entropy_g = corr_matrix[0][1] if corr_matrix else 0.0

    residues = []
    dists = []
    for r in records:
        zeros = sum(1 for v in r["remainder_vector"] if v == 0)
        dist = int(r.get("distance_to_next_prime", r.get("termination_distance", 99)))
        residues.append(zeros)
        dists.append(min(dist, 5))
    mi_res = mutual_information(residues, dists)

    repeat_stats = compute_intra_gap_repeat_stats(records)
    histograms = compute_residue_histograms(records)

    gwr_last = sum(
        1
        for grecs in gaps.values()
        for r in grecs
        if (r.get("is_gwr_winner") or r.get("is_current_min_d"))
        and int(r.get("distance_to_next_prime", r.get("termination_distance", 99))) == 1
    )

    result = {
        "records": len(records),
        "gaps": len(gaps),
        "mi_num_zeros_vs_dist_bin": mi_res,
        "spearman_entropy_vs_g": spearman_entropy_g,
        "gwr_last_rate": gwr_last / len(gaps) if gaps else 0.0,
        "repeat_stats": repeat_stats,
        "histogram_groups": len(histograms["groups"]),
    }

    (out_dir / "descriptive_stats.json").write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "| metric | value |",
        "| --- | --- |",
        f"| records | {result['records']} |",
        f"| gaps | {result['gaps']} |",
        f"| MI(num_zeros, dist_bin) | {mi_res['mi']:.4f} |",
        f"| normalized_MI | {mi_res['normalized_mi']:.4f} |",
        f"| Spearman(entropy, g) | {spearman_entropy_g:.4f} |",
        f"| GWR_last_rate | {result['gwr_last_rate']:.4f} |",
        f"| histogram_groups | {result['histogram_groups']} |",
    ]
    (out_dir / "descriptive_stats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    run_descriptive_analysis(records, out_dir)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--records",
        type=Path,
        required=True,
        help="Input JSONL from collect_remainder_stats.py",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Output directory for tables and JSON stats",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """CLI entry for correlation engine."""
    args = build_parser().parse_args(argv)
    records = load_records(args.records)
    result = run_full_descriptive(records, args.out)
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
