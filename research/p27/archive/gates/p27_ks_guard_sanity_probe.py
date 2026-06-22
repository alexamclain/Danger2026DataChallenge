#!/usr/bin/env python3
"""Guard-field sanity checks for the p27 K/S branch-extraction route.

This is the local analogue of the older q1471 online Magma sanity fixture,
but run over p27-signature fields q = 7 mod 16.  It validates the K/S map and
the H90/order-4 identities before the heavier post-quartic normalization work.
"""

from __future__ import annotations

import argparse
from collections import Counter


def parse_ints(raw: str) -> list[int]:
    return [int(part) for part in raw.split(",") if part.strip()]


def inv(a: int, p: int) -> int | None:
    a %= p
    if a == 0:
        return None
    return pow(a, p - 2, p)


def legendre(a: int, p: int) -> int:
    a %= p
    if a == 0:
        return 0
    return 1 if pow(a, (p - 1) // 2, p) == 1 else -1


def sqrt_roots(a: int, p: int) -> list[int]:
    a %= p
    if a == 0:
        return [0]
    if legendre(a, p) != 1:
        return []
    # All current guard fields are 3 mod 4.
    root = pow(a, (p + 1) // 4, p)
    return sorted({root, (-root) % p})


def run_field(q: int) -> Counter:
    stats: Counter = Counter()
    stats["q_mod_16"] = q % 16
    stats["chi_minus_one"] = legendre(-1, q)
    stats["chi_two"] = legendre(2, q)

    for x in range(q):
        x2 = x * x % q
        x3 = x2 * x % q
        for w in sqrt_roots(x3 - x, q):
            snum = (x2 - 2 * x - 1) * (x2 + 2 * x - 1) % q
            sden = 2 * w * (x2 + 1) % q
            kden = 4 * x * (x - 1) * (x + 1) * pow(x2 + 1, 2, q) % q
            if sden == 0 or kden == 0:
                stats["skipped_denominator"] += 1
                continue

            sroot = snum * inv(sden, q) % q  # type: ignore[arg-type]
            k = snum * snum * inv(kden, q) % q  # type: ignore[arg-type]
            stats["checked_points"] += 1

            if sroot * sroot % q != k:
                stats["sroot_square_mismatch"] += 1
            if 2 * sroot * w * (x2 + 1) % q != snum:
                stats["sroot_linear_mismatch"] += 1
            if k * kden % q != snum * snum % q:
                stats["k_relation_mismatch"] += 1

            t2 = x * (x2 + 1) * (x2 + 2 * x - 1) % q
            mt = (x + 1) * (2 * w * x + x3 + x2 - x - 1) % q
            m0 = (x2 + 1) * (x2 + 2 * x - 1) * (w * x + w + 2 * x2) % q
            x4 = x2 * x2 % q
            l_value = (4 * w * x2 + 4 * w * x + x4 + 6 * x3 - 2 * x - 1) % q
            salpha = (w * (x + 1) + 2 * x2) % q

            if salpha * salpha % q != x * l_value % q:
                stats["h90_salpha_mismatch"] += 1
            if (m0 * m0 - mt * mt * t2 - 4 * t2 * salpha * salpha) % q != 0:
                stats["h90_norm_mismatch"] += 1

    stats["total_mismatches"] = (
        stats["sroot_square_mismatch"]
        + stats["sroot_linear_mismatch"]
        + stats["k_relation_mismatch"]
        + stats["h90_salpha_mismatch"]
        + stats["h90_norm_mismatch"]
    )
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1607,1847,2087")
    args = parser.parse_args()

    print("p27 K/S guard-field sanity probe")
    print("checks = Sroot^2=K, K relation, Sroot linear relation, H90 Salpha, H90 norm")
    for q in parse_ints(args.small_primes):
        stats = run_field(q)
        print_counter(f"q{q}", stats)
    print("p27_ks_guard_sanity_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
