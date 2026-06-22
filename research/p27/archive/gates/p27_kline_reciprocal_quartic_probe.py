#!/usr/bin/env python3
"""Exact Belyi-reciprocal quartic screen for the p27 K-line selector.

The K-line has the visible Belyi involution K -> 4/K.  A monic quartic whose
branch divisor is preserved by this involution must satisfy

    K^4 f(4/K) = s*16*f(K),  s in {+1, -1},

so it has one of the two forms

    K^4 + a*K^3 + b*K^2 + 4*a*K + 16
    K^4 + a*K^3 + b*K^2 - 4*a*K - 16.

This is a small q^2 screen for the nearest Belyi-symmetric subfamily inside
the GPU-sized full K-line quartic family.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p27_kline_quartic_verify import DEFAULT_PACKET, load_packet, target_entry


@dataclass(frozen=True)
class Hit:
    reciprocal_sign: int
    polarity: int
    coeffs: tuple[int, int, int, int]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for value in range(1, p):
        table[value] = 1 if pow(value, (p - 1) // 2, p) == 1 else -1
    return table


def scan_reciprocal_quartics(target: dict, sample_limit: int) -> tuple[dict[str, int], list[Hit]]:
    q = int(target["field"])
    rows = [(int(row["K"]) % q, int(row["sign"])) for row in target["rows"]]
    powers = [(K, K * K % q, K * K % q * K % q, pow(K, 4, q)) for K, _ in rows]
    chi = legendre_table(q)
    stats = {
        "field": q,
        "rows": len(rows),
        "pairs_tested_per_reciprocal_sign": q * q,
        "total_polynomial_shapes": 2 * q * q,
        "reciprocal_sign_1_hits": 0,
        "reciprocal_sign_-1_hits": 0,
        "polarity_1_hits": 0,
        "polarity_-1_hits": 0,
        "exact_reciprocal_quartics": 0,
    }
    hits: list[Hit] = []
    for reciprocal_sign in (1, -1):
        c_factor = 4 * reciprocal_sign
        d = 16 * reciprocal_sign
        for a in range(q):
            c = c_factor * a
            a_terms = [
                (K4 + a * K3 + c * K + d) % q
                for K, _K2, K3, K4 in powers
            ]
            for b in range(q):
                for polarity in (1, -1):
                    ok = True
                    for (base, (_K, K2, _K3, _K4), (_row_k, target_sign)) in zip(
                        a_terms, powers, rows
                    ):
                        value_sign = chi[(base + b * K2) % q]
                        if value_sign == 0 or value_sign != polarity * target_sign:
                            ok = False
                            break
                    if ok:
                        stats[f"reciprocal_sign_{reciprocal_sign}_hits"] += 1
                        stats[f"polarity_{polarity}_hits"] += 1
                        stats["exact_reciprocal_quartics"] += 1
                        if len(hits) < sample_limit:
                            hits.append(
                                Hit(
                                    reciprocal_sign=reciprocal_sign,
                                    polarity=polarity,
                                    coeffs=(a % q, b % q, c % q, d % q),
                                )
                            )
    return stats, hits


def print_stats(stats: dict[str, int]) -> None:
    print("reciprocal_quartic_stats:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--packet", default=DEFAULT_PACKET)
    parser.add_argument("--small-primes", default="1471,1607,1847")
    parser.add_argument("--families", default="d3_on_K,d4_on_K_after_d3")
    parser.add_argument("--sample-limit", type=int, default=8)
    args = parser.parse_args()

    packet = load_packet(args.packet)
    fields = [int(part) for part in args.small_primes.split(",") if part.strip()]
    families = [part.strip() for part in args.families.split(",") if part.strip()]

    print("p27 K-line Belyi-reciprocal quartic probe")
    print(f"packet = {args.packet}")
    print("families:")
    print("  sign=+1: K^4 + a*K^3 + b*K^2 + 4*a*K + 16")
    print("  sign=-1: K^4 + a*K^3 + b*K^2 - 4*a*K - 16")
    print("global polarity allowed")
    for q in fields:
        for family in families:
            target = target_entry(packet, q, family)
            print(f"target: field={q} family={family}")
            stats, hits = scan_reciprocal_quartics(target, args.sample_limit)
            print_stats(stats)
            print("hit_samples:")
            for hit in hits:
                a, b, c, d = hit.coeffs
                print(
                    "  "
                    f"reciprocal_sign={hit.reciprocal_sign} "
                    f"polarity={hit.polarity} coeffs={a},{b},{c},{d}"
                )
    print("p27_kline_reciprocal_quartic_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
