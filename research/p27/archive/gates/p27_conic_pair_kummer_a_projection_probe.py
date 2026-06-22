#!/usr/bin/env python3
"""A-projection counts for the p27 conic-pair Kummer d4-plus layer."""

from __future__ import annotations

import argparse
import math
import time

from p27_conic_pair_d5_tower_probe import deep_bits_for_ax
from p27_conic_pair_sampler_legal_incidence_probe import legal_sets


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    d = 3
    while d * d <= n:
        if n % d == 0:
            return False
        d += 2
    return True


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def auto_primes(start: int, count: int) -> list[int]:
    out: list[int] = []
    n = start
    while len(out) < count:
        if n % 8 == 7 and is_prime(n):
            out.append(n)
        n += 1
    return out


def screen_field(q: int) -> None:
    t0 = time.time()
    _, legal, d3_plus, _ = legal_sets(q)
    d4_plus: list[tuple[int, int]] = []
    d4_minus: list[tuple[int, int]] = []
    bad = 0
    for A, x in d3_plus:
        bits = deep_bits_for_ax(A, x, q)
        if bits.d4 == 1:
            d4_plus.append((A, x))
        elif bits.d4 == -1:
            d4_minus.append((A, x))
        else:
            bad += 1
    d3_A = {A for A, _ in d3_plus}
    d4_A = {A for A, _ in d4_plus}
    elapsed = time.time() - t0
    print(
        f"q{q}: "
        f"legal_Ax={len(legal)} "
        f"d3_Ax={len(d3_plus)} "
        f"d3_A={len(d3_A)} "
        f"d4_Ax={len(d4_plus)} "
        f"d4_A={len(d4_A)} "
        f"d4_minus_Ax={len(d4_minus)} "
        f"bad={bad} "
        f"sqrt={math.sqrt(q):.1f} "
        f"d4_A_over_q={(len(d4_A) / q):.6f} "
        f"time={elapsed:.2f}s"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    parser.add_argument("--auto-start", type=int, default=2200)
    parser.add_argument("--auto-count", type=int, default=8)
    args = parser.parse_args()

    primes = parse_ints(args.small_primes) + auto_primes(args.auto_start, args.auto_count)
    seen: set[int] = set()
    print("p27 conic-pair Kummer A-projection probe")
    for q in primes:
        if q in seen:
            continue
        seen.add(q)
        screen_field(q)
    print("p27_conic_pair_kummer_a_projection_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
