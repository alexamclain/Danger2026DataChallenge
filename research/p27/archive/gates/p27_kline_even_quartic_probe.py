#!/usr/bin/env python3
"""Exact even-quartic screen for the p27 K-line selector.

This tests the descended subfamily

    chi(K^4 + a*K^2 + b)

inside the GPU-sized K-line quartic packet.  A positive would mean the
selector descends through K^2 and should be a much cheaper B/K bridge target.
A negative means any K-line quartic must use odd K terms, i.e. the signed K
sheet rather than only the bridge coordinate K^2.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from p27_kline_quartic_verify import DEFAULT_PACKET, load_packet, target_entry


@dataclass(frozen=True)
class Hit:
    polarity: int
    coeffs: tuple[int, int]


def legendre_table(p: int) -> list[int]:
    table = [0] * p
    for value in range(1, p):
        table[value] = 1 if pow(value, (p - 1) // 2, p) == 1 else -1
    return table


def scan_even_quartics(target: dict, sample_limit: int) -> tuple[dict[str, int], list[Hit]]:
    q = int(target["field"])
    rows = [(int(row["K"]) % q, int(row["sign"])) for row in target["rows"]]
    powers = [(K * K % q, pow(K, 4, q)) for K, _ in rows]
    chi = legendre_table(q)
    stats = {
        "field": q,
        "rows": len(rows),
        "pairs_tested": q * q,
        "polarity_1_hits": 0,
        "polarity_-1_hits": 0,
        "exact_even_quartics": 0,
    }
    hits: list[Hit] = []
    for a in range(q):
        a_terms = [(K4 + a * K2) % q for K2, K4 in powers]
        for b in range(q):
            for polarity in (1, -1):
                ok = True
                for (base, (_K, target_sign)) in zip(a_terms, rows):
                    value_sign = chi[(base + b) % q]
                    if value_sign == 0 or value_sign != polarity * target_sign:
                        ok = False
                        break
                if ok:
                    stats[f"polarity_{polarity}_hits"] += 1
                    stats["exact_even_quartics"] += 1
                    if len(hits) < sample_limit:
                        hits.append(Hit(polarity=polarity, coeffs=(a, b)))
    return stats, hits


def print_stats(stats: dict[str, int]) -> None:
    print("even_quartic_stats:")
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

    print("p27 K-line even-quartic probe")
    print(f"packet = {args.packet}")
    print("family = chi(K^4 + a*K^2 + b), global polarity allowed")
    for q in fields:
        for family in families:
            target = target_entry(packet, q, family)
            print(f"target: field={q} family={family}")
            stats, hits = scan_even_quartics(target, args.sample_limit)
            print_stats(stats)
            print("hit_samples:")
            for hit in hits:
                a, b = hit.coeffs
                print(f"  polarity={hit.polarity} coeffs={a},{b}")
    print("p27_kline_even_quartic_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
