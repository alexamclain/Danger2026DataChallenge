#!/usr/bin/env python3
"""Bridge check between the B-line and signed-doubling K-line targets.

The B-line and K-line quartic packets look numerically similar in q1607/q1847.
This probe tests the explicit branch relation

    K^2 = (B - 2)^4 / (8*B*(B + 2)^2)

for Bplus and checks whether d3/d4 target signs agree after passing from B to
the signed K class.
"""

from __future__ import annotations

import argparse
from collections import Counter

from p27_b_line_branch_support_probe import legal_b_maps
from p27_k_belyi_involution_probe import collect_rows, parse_ints


def inv(a: int, p: int) -> int:
    return pow(a % p, p - 2, p)


def sqrt_table(p: int) -> list[list[int]]:
    roots: list[list[int]] = [[] for _ in range(p)]
    for x in range(p):
        roots[x * x % p].append(x)
    return roots


def b_to_l(B: int, p: int) -> int | None:
    B %= p
    if B == 0 or (B + 2) % p == 0:
        return None
    num = pow((B - 2) % p, 4, p)
    den = 8 * B % p * ((B + 2) % p) ** 2 % p
    return num * inv(den, p) % p


def compare_family(
    label: str,
    b_targets: dict[int, int],
    k_targets: dict[int, int],
    p: int,
    roots: list[list[int]],
) -> Counter:
    stats: Counter = Counter()
    for B, b_target in sorted(b_targets.items()):
        stats["B_rows"] += 1
        L = b_to_l(B, p)
        if L is None:
            stats["B_degenerate"] += 1
            continue
        ks = roots[L]
        stats[f"K_roots_{len(ks)}"] += 1
        present = [k for k in ks if k in k_targets]
        stats[f"K_present_{len(present)}"] += 1
        if not present:
            continue
        values = {k_targets[k] for k in present}
        if len(values) > 1:
            stats["K_target_mixed_on_signed_class"] += 1
        k_value = next(iter(values))
        if k_value == b_target:
            stats["target_match"] += 1
        else:
            stats["target_opposite"] += 1
    stats["family_" + label + "_rows"] = stats["B_rows"]
    return stats


def print_counter(prefix: str, stats: Counter) -> None:
    print(f"{prefix}:")
    for key in sorted(stats):
        print(f"  {key} = {stats[key]}")


def run_field(q: int) -> None:
    b_d3, b_d4, b_stats = legal_b_maps(q)
    k_d3_rows, k_d4_rows, _s_d3, _s_d4, k_stats = collect_rows(q)
    k_d3 = {row.k: row.target for row in k_d3_rows}
    k_d4 = {row.k: row.target for row in k_d4_rows}
    roots = sqrt_table(q)

    setup = Counter()
    setup.update({f"B_{key}": value for key, value in b_stats.items()})
    setup.update({f"K_{key}": value for key, value in k_stats.items()})
    setup["B_d3_rows"] = len(b_d3)
    setup["B_d3_plus"] = sum(1 for value in b_d3.values() if value == 1)
    setup["B_d3_minus"] = sum(1 for value in b_d3.values() if value == -1)
    setup["K_d3_rows"] = len(k_d3)
    setup["K_d3_plus"] = sum(1 for value in k_d3.values() if value == 1)
    setup["K_d3_minus"] = sum(1 for value in k_d3.values() if value == -1)
    setup["B_d4_rows"] = len(b_d4)
    setup["B_d4_plus"] = sum(1 for value in b_d4.values() if value == 1)
    setup["B_d4_minus"] = sum(1 for value in b_d4.values() if value == -1)
    setup["K_d4_rows"] = len(k_d4)
    setup["K_d4_plus"] = sum(1 for value in k_d4.values() if value == 1)
    setup["K_d4_minus"] = sum(1 for value in k_d4.values() if value == -1)

    print(f"q={q}:")
    print_counter("  setup", setup)
    print_counter("  d3_bridge", compare_family("d3", b_d3, k_d3, q, roots))
    print_counter("  d4_bridge", compare_family("d4", b_d4, k_d4, q, roots))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--small-primes", default="1471,1607,1847,2087")
    args = parser.parse_args()

    print("p27 B-line / K-line bridge probe")
    print("relation = K^2 - (B-2)^4/(8*B*(B+2)^2)")
    for q in parse_ints(args.small_primes):
        run_field(q)
    print("p27_b_kline_bridge_probe_rows=1/1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
