#!/usr/bin/env python3
"""Exact Belyi-involution quartic screen for the p27 B-line selector.

The B-line branch set is {0, -2, infinity}.  Its three visible order-2
Möbius symmetries give small monic quartic families:

    B -> -B-2:
        B^4 + 4B^3 + bB^2 + (2b-8)B + d

    B -> 4/B:
        B^4 + aB^3 + bB^2 + 4aB + 16
        B^4 + aB^3 - 4aB - 16

    B+2 -> 4/(B+2):
        (B+2)^4 + a(B+2)^3 + b(B+2)^2 + 4a(B+2) + 16
        (B+2)^4 + a(B+2)^3 - 4a(B+2) - 16

This q^2/q screen tests whether the remaining B-line quartic GPU target is
already explained by a visible branch-set involution.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable

from p27_b_line_quartic_verify import DEFAULT_PACKET, load_packet, target_entry
from p27_kline_reverse_z_relation_probe import parse_ints


@dataclass(frozen=True)
class Shape:
    name: str
    parameters: int
    coeffs: tuple[int, int, int, int]


@dataclass(frozen=True)
class Hit:
    shape: str
    polarity: int
    coeffs: tuple[int, int, int, int]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for value in range(1, p):
        table[value] = 1 if pow(value, (p - 1) // 2, p) == 1 else -1
    return table


def involution_shapes(q: int) -> Iterable[Shape]:
    for b in range(q):
        c = (2 * b - 8) % q
        for d in range(q):
            yield Shape("B_to_-B-2", 2, (4 % q, b, c, d))

    for a in range(q):
        for b in range(q):
            yield Shape("B_to_4_over_B_plus", 2, (a, b, 4 * a % q, 16 % q))
    for a in range(q):
        yield Shape("B_to_4_over_B_minus", 1, (a, 0, -4 * a % q, -16 % q))

    for a in range(q):
        for b in range(q):
            yield Shape(
                "Bplus2_to_4_over_Bplus2_plus",
                2,
                (
                    (8 + a) % q,
                    (24 + 6 * a + b) % q,
                    (32 + 16 * a + 4 * b) % q,
                    (32 + 16 * a + 4 * b) % q,
                ),
            )
    for a in range(q):
        yield Shape(
            "Bplus2_to_4_over_Bplus2_minus",
            1,
            (
                (8 + a) % q,
                (24 + 6 * a) % q,
                (32 + 8 * a) % q,
                0,
            ),
        )


def shape_counts(q: int) -> dict[str, int]:
    return {
        "B_to_-B-2": q * q,
        "B_to_4_over_B_plus": q * q,
        "B_to_4_over_B_minus": q,
        "Bplus2_to_4_over_Bplus2_plus": q * q,
        "Bplus2_to_4_over_Bplus2_minus": q,
    }


def scan_involution_quartics(target: dict, sample_limit: int) -> tuple[dict[str, int], list[Hit]]:
    q = int(target["field"])
    rows = [(int(row["B"]) % q, int(row["sign"])) for row in target["rows"]]
    powers = [(B, B * B % q, B * B % q * B % q, pow(B, 4, q)) for B, _ in rows]
    chi = legendre_table(q)
    counts = shape_counts(q)
    stats = {
        "field": q,
        "rows": len(rows),
        "total_polynomial_shapes": sum(counts.values()),
        "polarity_1_hits": 0,
        "polarity_-1_hits": 0,
        "exact_involution_quartics": 0,
    }
    for name, count in counts.items():
        stats[f"{name}_tested"] = count
        stats[f"{name}_hits"] = 0

    hits: list[Hit] = []
    for shape in involution_shapes(q):
        a, b, c, d = shape.coeffs
        for polarity in (1, -1):
            ok = True
            for (_B, target_sign), (B, B2, B3, B4) in zip(rows, powers):
                value_sign = chi[(B4 + a * B3 + b * B2 + c * B + d) % q]
                if value_sign == 0 or value_sign != polarity * target_sign:
                    ok = False
                    break
            if ok:
                stats[f"{shape.name}_hits"] += 1
                stats[f"polarity_{polarity}_hits"] += 1
                stats["exact_involution_quartics"] += 1
                if len(hits) < sample_limit:
                    hits.append(Hit(shape=shape.name, polarity=polarity, coeffs=shape.coeffs))
    return stats, hits


def print_stats(stats: dict[str, int]) -> None:
    print("involution_quartic_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=DEFAULT_PACKET)
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--families", default="d3_on_legalB,gate4_prefix_on_legalB")
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    fields = parse_ints(args.small_primes)
    families = [part.strip() for part in args.families.split(",") if part.strip()]

    print("p27 B-line Belyi-involution quartic probe")
    print(f"packet = {args.packet}")
    print("families:")
    print("  B_to_-B-2: B^4 + 4B^3 + bB^2 + (2b-8)B + d")
    print("  B_to_4_over_B_plus: B^4 + aB^3 + bB^2 + 4aB + 16")
    print("  B_to_4_over_B_minus: B^4 + aB^3 - 4aB - 16")
    print("  Bplus2_to_4_over_Bplus2_plus: shifted plus reciprocal")
    print("  Bplus2_to_4_over_Bplus2_minus: shifted minus reciprocal")
    print("global polarity allowed")
    for q in fields:
        for family in families:
            target = target_entry(packet, q, family)
            print(f"target: field={q} family={family}")
            stats, hits = scan_involution_quartics(target, args.sample_limit)
            print_stats(stats)
            print("hit_samples:")
            for hit in hits:
                a, b, c, d = hit.coeffs
                print(f"  shape={hit.shape} polarity={hit.polarity} coeffs={a},{b},{c},{d}")
    print("p27_b_line_involution_quartic_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
