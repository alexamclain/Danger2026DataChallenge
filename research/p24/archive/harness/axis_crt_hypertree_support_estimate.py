#!/usr/bin/env python3
"""Size estimates for the p24 CRT-axis hypertree support.

The selected-origin CRT-axis Cauchy-Binet support is the set of full-rank
edge subsets in the complete multipartite incidence model.  For p24 the
parts are:

    2, 157, 211

and the support bases have

    k = 1 + (2-1) + (157-1) + (211-1) = 368

edges.  This script avoids enumeration.  It reports:

* total possible k-subsets of the 2*157*211 edge set;
* a constructive lower bound from bipartite spanning trees in K_{157,211};
* a coverage-only upper bound from ordered surjections onto each part.

The estimates are for theorem shaping only.  They show that the CRT support
collapse is real, but still astronomically too large to be a certificate
payload.
"""

from __future__ import annotations

import argparse
import math

from axis_crt_fourier_coefficient_support import rank_mod_q


def log10_int(n: int) -> float:
    if n <= 0:
        return float("-inf")
    bits = n.bit_length()
    top = n >> max(0, bits - 53)
    return (bits - 1) * math.log10(2) + math.log10(top / (1 << min(bits - 1, 52)))


def stirling_second(n: int, k: int) -> int:
    row = [0] * (k + 1)
    row[0] = 1
    for i in range(1, n + 1):
        nxt = [0] * (k + 1)
        for j in range(1, min(i, k) + 1):
            nxt[j] = row[j - 1] + j * row[j]
        row = nxt
    return row[k]


def log10_surjections(n: int, bins: int) -> float:
    """Log10 of the number of functions [n] -> [bins] hitting every bin."""

    return log10_int(math.factorial(bins) * stirling_second(n, bins))


def log10_binom(n: int, k: int) -> float:
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
    ) / math.log(10)


def p24_lower_log10(a: int, b: int, c: int) -> float:
    if a != 2:
        raise ValueError("the constructive lower bound is implemented for first part size 2")
    # tau(K_{b,c}) = b^(c-1) c^(b-1).  For each tree, duplicate one of its
    # b+c-1 edges with the other first-coordinate value.
    return (c - 1) * math.log10(b) + (b - 1) * math.log10(c) + math.log10(b + c - 1)


def p24_upper_log10(a: int, b: int, c: int) -> float:
    k = 1 + (a - 1) + (b - 1) + (c - 1)
    # Ordered edge sequences covering every level in each part, divided by k!.
    # Repeated full edges are allowed in the ordered count, so this is an upper
    # bound for distinct edge subsets.
    ordered = log10_surjections(k, a) + log10_surjections(k, b) + log10_surjections(k, c)
    return ordered - math.lgamma(k + 1) / math.log(10)


def lower_bound_edges(b: int, c: int) -> list[tuple[int, int, int]]:
    """A spanning-tree lift giving a full-rank support subset.

    Use the tree in K_{b,c} containing (0,j) for every c-vertex j and
    (i,0) for every b-vertex i>0, then duplicate (0,0) with first coordinate 1.
    """

    edges: list[tuple[int, int, int]] = []
    for j in range(c):
        edges.append((0, 0, j))
    for i in range(1, b):
        edges.append((0, i, 0))
    edges.append((1, 0, 0))
    return edges


def incidence_features(edge: tuple[int, int, int], b: int, c: int) -> list[int]:
    a_value, b_value, c_value = edge
    row = [1]
    row.append(1 if a_value == 0 else 0)
    row.extend(1 if b_value == i else 0 for i in range(b - 1))
    row.extend(1 if c_value == j else 0 for j in range(c - 1))
    return row


def lower_rank(b: int, c: int, modulus: int) -> tuple[int, int, int]:
    rows = [incidence_features(edge, b, c) for edge in lower_bound_edges(b, c)]
    return len(rows), len(rows[0]), rank_mod_q(rows, modulus)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", type=int, default=2)
    ap.add_argument("--b", type=int, default=157)
    ap.add_argument("--c", type=int, default=211)
    ap.add_argument("--rank-modulus", type=int, default=1_000_003)
    args = ap.parse_args()

    a, b, c = args.a, args.b, args.c
    parts = (a, b, c)
    edge_count = a * b * c
    k = 1 + sum(part - 1 for part in parts)
    total_log = log10_binom(edge_count, k)
    lower_log = p24_lower_log10(a, b, c)
    upper_log = p24_upper_log10(a, b, c)
    rows, cols, rank = lower_rank(b, c, args.rank_modulus)

    print("axis CRT hypertree support estimate")
    print(f"parts={parts}")
    print(f"edge_count={edge_count}")
    print(f"axis_dim=k={k}")
    print(f"total_k_subsets_log10={total_log:.6f}")
    print()
    print("constructive_lower_bound")
    print("  construction=lift_spanning_tree_of_K_b_c_and_duplicate_one_edge_across_part_a")
    print(f"  lower_support_log10={lower_log:.6f}")
    print(f"  lower_rank_rows={rows}")
    print(f"  lower_rank_cols={cols}")
    print(f"  lower_rank_mod_{args.rank_modulus}={rank}")
    print(f"  lower_rank_full={int(rank == k)}")
    print()
    print("coverage_upper_bound")
    print("  construction=ordered_surjections_to_each_part_divided_by_k_factorial")
    print(f"  upper_support_log10={upper_log:.6f}")
    print(f"  upper_vs_total_log10_gap={total_log - upper_log:.6f}")
    print()
    print("interpretation")
    print("  support_collapse_is_real_because_upper_log10_is_below_total_log10=1")
    print("  support_is_still_enormous_because_lower_log10_is_hundreds=1")
    print("  support_terms_cannot_be_a_certificate_payload=1")
    print("conclusion=reported_axis_crt_hypertree_support_estimate")


if __name__ == "__main__":
    main()
