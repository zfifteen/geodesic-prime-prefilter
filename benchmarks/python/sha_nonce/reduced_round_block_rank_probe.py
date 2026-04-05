#!/usr/bin/env python3
"""Probe whether reduced-round SHA-256 block scores enrich final low-hash blocks."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path


DEFAULT_OUTPUT_DIR = Path(
    "benchmarks/output/python/sha_nonce/reduced_round_block_rank_probe"
)
DEFAULT_ROUNDS = [4, 8, 12, 16]
DEFAULT_HEADER_COUNT = 8
DEFAULT_BLOCKS_PER_HEADER = 256
DEFAULT_BLOCK_SIZE = 128
DEFAULT_KEEP_FRACTION = 0.25
DEFAULT_THRESHOLD_BYTE = 1

K16 = [
    0x428A2F98,
    0x71374491,
    0xB5C0FBCF,
    0xE9B5DBA5,
    0x3956C25B,
    0x59F111F1,
    0x923F82A4,
    0xAB1C5ED5,
    0xD807AA98,
    0x12835B01,
    0x243185BE,
    0x550C7DC3,
    0x72BE5D74,
    0x80DEB1FE,
    0x9BDC06A7,
    0xC19BF174,
]
K64 = K16 + [
    0xE49B69C1,
    0xEFBE4786,
    0x0FC19DC6,
    0x240CA1CC,
    0x2DE92C6F,
    0x4A7484AA,
    0x5CB0A9DC,
    0x76F988DA,
    0x983E5152,
    0xA831C66D,
    0xB00327C8,
    0xBF597FC7,
    0xC6E00BF3,
    0xD5A79147,
    0x06CA6351,
    0x14292967,
    0x27B70A85,
    0x2E1B2138,
    0x4D2C6DFC,
    0x53380D13,
    0x650A7354,
    0x766A0ABB,
    0x81C2C92E,
    0x92722C85,
    0xA2BFE8A1,
    0xA81A664B,
    0xC24B8B70,
    0xC76C51A3,
    0xD192E819,
    0xD6990624,
    0xF40E3585,
    0x106AA070,
    0x19A4C116,
    0x1E376C08,
    0x2748774C,
    0x34B0BCB5,
    0x391C0CB3,
    0x4ED8AA4A,
    0x5B9CCA4F,
    0x682E6FF3,
    0x748F82EE,
    0x78A5636F,
    0x84C87814,
    0x8CC70208,
    0x90BEFFFA,
    0xA4506CEB,
    0xBEF9A3F7,
    0xC67178F2,
]
IV = [
    0x6A09E667,
    0xBB67AE85,
    0x3C6EF372,
    0xA54FF53A,
    0x510E527F,
    0x9B05688C,
    0x1F83D9AB,
    0x5BE0CD19,
]


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Rank nonce blocks by reduced-round second-block SHA-256 state and "
            "measure final low-hash enrichment."
        )
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for JSON and SVG artifacts.",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        nargs="+",
        default=list(DEFAULT_ROUNDS),
        help="Reduced-round checkpoints to evaluate. Must stay within 1..16.",
    )
    parser.add_argument(
        "--headers",
        type=int,
        default=DEFAULT_HEADER_COUNT,
        help="Number of deterministic 76-byte header prefixes to scan.",
    )
    parser.add_argument(
        "--blocks-per-header",
        type=int,
        default=DEFAULT_BLOCKS_PER_HEADER,
        help="Number of contiguous nonce blocks scanned for each header.",
    )
    parser.add_argument(
        "--block-size",
        type=int,
        default=DEFAULT_BLOCK_SIZE,
        help="Nonce count inside each block.",
    )
    parser.add_argument(
        "--keep-fraction",
        type=float,
        default=DEFAULT_KEEP_FRACTION,
        help="Fraction of lowest-scored blocks kept by the reduced-round ranker.",
    )
    parser.add_argument(
        "--threshold-byte",
        type=int,
        default=DEFAULT_THRESHOLD_BYTE,
        help="Treat a final digest as a hit when digest[0] < threshold-byte.",
    )
    return parser


def ror(value: int, shift: int) -> int:
    """Return a 32-bit rotate-right."""
    return ((value >> shift) | ((value << (32 - shift)) & 0xFFFFFFFF)) & 0xFFFFFFFF


def ch(x: int, y: int, z: int) -> int:
    """Return the SHA-256 choose function."""
    return (x & y) ^ (~x & z)


def maj(x: int, y: int, z: int) -> int:
    """Return the SHA-256 majority function."""
    return (x & y) ^ (x & z) ^ (y & z)


def big_sigma0(value: int) -> int:
    """Return the SHA-256 big sigma 0 transform."""
    return ror(value, 2) ^ ror(value, 13) ^ ror(value, 22)


def big_sigma1(value: int) -> int:
    """Return the SHA-256 big sigma 1 transform."""
    return ror(value, 6) ^ ror(value, 11) ^ ror(value, 25)


def small_sigma0(value: int) -> int:
    """Return the SHA-256 small sigma 0 transform."""
    return ror(value, 7) ^ ror(value, 18) ^ (value >> 3)


def small_sigma1(value: int) -> int:
    """Return the SHA-256 small sigma 1 transform."""
    return ror(value, 17) ^ ror(value, 19) ^ (value >> 10)


def deterministic_header_prefix(index: int) -> bytes:
    """Return one deterministic 76-byte prefix for nonce-line probing."""
    seed = f"prime-gap-structure/sha-reduced-round-block-rank/{index}".encode(
        "utf-8"
    )
    chunks: list[bytes] = []
    counter = 0
    total = 0
    while total < 76:
        chunk = hashlib.sha256(seed + counter.to_bytes(4, "little")).digest()
        chunks.append(chunk)
        total += len(chunk)
        counter += 1
    return b"".join(chunks)[:76]


def words_from_block(block: bytes) -> list[int]:
    """Return the big-endian 32-bit words of one 64-byte block."""
    return [int.from_bytes(block[index : index + 4], "big") for index in range(0, 64, 4)]


def full_compress(state: list[int], words16: list[int]) -> list[int]:
    """Return the SHA-256 compression result for one 64-byte block."""
    words = words16[:] + [0] * 48
    for index in range(16, 64):
        words[index] = (
            small_sigma1(words[index - 2])
            + words[index - 7]
            + small_sigma0(words[index - 15])
            + words[index - 16]
        ) & 0xFFFFFFFF

    a, b, c, d, e, f, g, h = state
    for index in range(64):
        t1 = (
            h + big_sigma1(e) + ch(e, f, g) + K64[index] + words[index]
        ) & 0xFFFFFFFF
        t2 = (big_sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
        h = g
        g = f
        f = e
        e = (d + t1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (t1 + t2) & 0xFFFFFFFF

    return [
        (state[0] + a) & 0xFFFFFFFF,
        (state[1] + b) & 0xFFFFFFFF,
        (state[2] + c) & 0xFFFFFFFF,
        (state[3] + d) & 0xFFFFFFFF,
        (state[4] + e) & 0xFFFFFFFF,
        (state[5] + f) & 0xFFFFFFFF,
        (state[6] + g) & 0xFFFFFFFF,
        (state[7] + h) & 0xFFFFFFFF,
    ]


def first_block_midstate(prefix: bytes) -> list[int]:
    """Return the SHA-256 midstate after the first 64-byte block."""
    return full_compress(IV, words_from_block(prefix[:64]))


def second_block_words(tail12: bytes, nonce: int) -> list[int]:
    """Return the sixteen second-block words for one nonce."""
    return [
        int.from_bytes(tail12[0:4], "big"),
        int.from_bytes(tail12[4:8], "big"),
        int.from_bytes(tail12[8:12], "big"),
        int.from_bytes(nonce.to_bytes(4, "little"), "big"),
        0x80000000,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        640,
    ]


def reduced_round_scores(
    state: list[int],
    words16: list[int],
    checkpoints: list[int],
) -> dict[int, int]:
    """Return reduced-round leading-64-bit scores at the requested checkpoints."""
    target_set = set(checkpoints)
    result: dict[int, int] = {}
    a, b, c, d, e, f, g, h = state
    for index in range(max(checkpoints)):
        t1 = (
            h + big_sigma1(e) + ch(e, f, g) + K16[index] + words16[index]
        ) & 0xFFFFFFFF
        t2 = (big_sigma0(a) + maj(a, b, c)) & 0xFFFFFFFF
        h = g
        g = f
        f = e
        e = (d + t1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (t1 + t2) & 0xFFFFFFFF
        round_count = index + 1
        if round_count in target_set:
            result[round_count] = (a << 32) | b
    return result


def evaluate_round_probe(
    rounds: list[int],
    header_count: int,
    blocks_per_header: int,
    block_size: int,
    keep_fraction: float,
    threshold_byte: int,
) -> list[dict[str, object]]:
    """Evaluate reduced-round block ranking across deterministic headers."""
    block_rows: list[dict[str, object]] = []
    for header_index in range(header_count):
        prefix = deterministic_header_prefix(header_index)
        midstate = first_block_midstate(prefix)
        tail12 = prefix[64:76]

        for block_index in range(blocks_per_header):
            base_nonce = (header_index * blocks_per_header + block_index) * block_size
            best_scores = {round_count: None for round_count in rounds}
            hit_count = 0

            for offset in range(block_size):
                nonce = base_nonce + offset
                words16 = second_block_words(tail12, nonce)
                scores = reduced_round_scores(midstate, words16, rounds)
                for round_count, score in scores.items():
                    if best_scores[round_count] is None or score < best_scores[round_count]:
                        best_scores[round_count] = score

                digest = hashlib.sha256(prefix + nonce.to_bytes(4, "little")).digest()
                if digest[0] < threshold_byte:
                    hit_count += 1

            block_rows.append(
                {
                    "header_index": header_index,
                    "block_index": block_index,
                    "hit_count": hit_count,
                    "best_scores": best_scores,
                }
            )

    total_blocks = len(block_rows)
    selected_blocks = max(1, int(total_blocks * keep_fraction))
    total_hits = sum(row["hit_count"] for row in block_rows)
    expected_retention = selected_blocks / total_blocks

    rows: list[dict[str, object]] = []
    for round_count in rounds:
        ranked = sorted(
            block_rows,
            key=lambda row: row["best_scores"][round_count],
        )
        selected = ranked[:selected_blocks]
        selected_hits = sum(row["hit_count"] for row in selected)
        baseline_density = total_hits / total_blocks if total_blocks else 0.0
        selected_density = selected_hits / selected_blocks if selected_blocks else 0.0
        hit_density_ratio = (
            selected_density / baseline_density if baseline_density > 0.0 else 0.0
        )
        hit_retention_share = selected_hits / total_hits if total_hits > 0 else 0.0
        variance = (
            total_hits * expected_retention * (1.0 - expected_retention)
            if total_hits > 0
            else 0.0
        )
        z_score = (
            (selected_hits - total_hits * expected_retention) / math.sqrt(variance)
            if variance > 0.0
            else 0.0
        )
        rows.append(
            {
                "rounds": round_count,
                "total_blocks": total_blocks,
                "selected_blocks": selected_blocks,
                "total_hits": total_hits,
                "selected_hits": selected_hits,
                "selected_fraction": expected_retention,
                "expected_hit_retention_share": expected_retention,
                "hit_retention_share": hit_retention_share,
                "baseline_hits_per_block": baseline_density,
                "selected_hits_per_block": selected_density,
                "hit_density_ratio": hit_density_ratio,
                "hit_retention_z_score": z_score,
            }
        )
    return rows


def render_retention_svg(rows: list[dict[str, object]], output_path: Path) -> None:
    """Render one SVG showing retained hit share by reduced-round depth."""
    width = 900
    height = 420
    margin_left = 80
    margin_right = 40
    margin_top = 50
    margin_bottom = 70
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom
    expected = rows[0]["expected_hit_retention_share"] if rows else 0.0
    y_max = max(
        0.5,
        max([expected] + [row["hit_retention_share"] for row in rows]) * 1.15,
    )

    def x_at(index: int) -> float:
        if len(rows) == 1:
            return margin_left + plot_width / 2
        return margin_left + index * (plot_width / (len(rows) - 1))

    def y_at(value: float) -> float:
        return margin_top + plot_height * (1.0 - value / y_max)

    polyline = " ".join(
        f"{x_at(index):.1f},{y_at(row['hit_retention_share']):.1f}"
        for index, row in enumerate(rows)
    )
    x_labels = "\n".join(
        f'<text x="{x_at(index):.1f}" y="{height - 30}" text-anchor="middle" '
        f'font-size="12" fill="#1f2937">{row["rounds"]}</text>'
        for index, row in enumerate(rows)
    )
    y_labels = "\n".join(
        f'<text x="{margin_left - 12}" y="{y_at(tick):.1f}" text-anchor="end" '
        f'dominant-baseline="middle" font-size="12" fill="#1f2937">{tick:.3f}</text>'
        for tick in (0.0, y_max / 4, y_max / 2, 3 * y_max / 4, y_max)
    )
    points = "\n".join(
        f'<circle cx="{x_at(index):.1f}" cy="{y_at(row["hit_retention_share"]):.1f}" '
        f'r="4" fill="#2563eb" />'
        for index, row in enumerate(rows)
    )

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="{width}" height="{height}" fill="white" />
<text x="{width / 2:.1f}" y="28" text-anchor="middle" font-size="18" fill="#111827">Retained final-hit share after reduced-round block ranking</text>
<line x1="{margin_left}" y1="{y_at(expected):.1f}" x2="{width - margin_right}" y2="{y_at(expected):.1f}" stroke="#dc2626" stroke-width="2" stroke-dasharray="6 6" />
<text x="{width - margin_right}" y="{y_at(expected) - 8:.1f}" text-anchor="end" font-size="12" fill="#dc2626">baseline retained share</text>
<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{height - margin_bottom}" stroke="#111827" stroke-width="1.5" />
<line x1="{margin_left}" y1="{height - margin_bottom}" x2="{width - margin_right}" y2="{height - margin_bottom}" stroke="#111827" stroke-width="1.5" />
<polyline fill="none" stroke="#2563eb" stroke-width="3" points="{polyline}" />
{points}
{x_labels}
{y_labels}
<text x="{width / 2:.1f}" y="{height - 8}" text-anchor="middle" font-size="12" fill="#1f2937">reduced-round depth</text>
<text x="20" y="{height / 2:.1f}" text-anchor="middle" font-size="12" fill="#1f2937" transform="rotate(-90 20 {height / 2:.1f})">share of final hits retained in selected blocks</text>
</svg>
"""
    output_path.write_text(svg + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """Run the reduced-round block-rank probe."""
    args = build_parser().parse_args(argv)
    if not args.rounds:
        raise SystemExit("At least one reduced-round checkpoint is required.")
    if min(args.rounds) < 1 or max(args.rounds) > 16:
        raise SystemExit("Rounds must stay within the 1..16 range.")
    if args.keep_fraction <= 0.0 or args.keep_fraction >= 1.0:
        raise SystemExit("Keep fraction must stay strictly between 0 and 1.")

    rounds = sorted(set(args.rounds))
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = evaluate_round_probe(
        rounds=rounds,
        header_count=args.headers,
        blocks_per_header=args.blocks_per_header,
        block_size=args.block_size,
        keep_fraction=args.keep_fraction,
        threshold_byte=args.threshold_byte,
    )
    payload = {
        "headers": args.headers,
        "blocks_per_header": args.blocks_per_header,
        "block_size": args.block_size,
        "keep_fraction": args.keep_fraction,
        "threshold_byte": args.threshold_byte,
        "rounds": rounds,
        "rows": rows,
    }

    json_path = args.output_dir / "reduced_round_block_rank_probe.json"
    svg_path = args.output_dir / "reduced_round_block_rank_probe_retention.svg"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    render_retention_svg(rows, svg_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
