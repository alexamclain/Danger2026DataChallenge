#!/usr/bin/env python3
"""Cost-shape audit for decomposed CM on the smooth-ish p24 target.

Sutherland's decomposed CM method can obtain a root of H_D mod p using
polynomials of degrees m and n with m*n=h(D), avoiding a full degree-h
root-finding step once the embedded decomposed equations are available.

For the third p24 target, h factors as 2*157*211*3107441, so the best
root-degree split is attractive.  This script records that attraction and the
remaining obstruction: constructing the embedded equations is still a CM
class-orbit/CRT computation at roughly sqrt(|D|) scale in the known methods.
"""

from __future__ import annotations

import itertools
import math

P24 = 10**24 + 7
TRACE = -1178414874616
D_K = -652834595820939249713143
CLASS_FACTORS = [2, 157, 211, 3107441]


def main() -> None:
    h = math.prod(CLASS_FACTORS)
    sqrt_p = math.isqrt(P24)
    sqrt_D = math.isqrt(abs(D_K))
    print("p24 decomposed CM tradeoff audit")
    print(f"p={P24}")
    print(f"trace={TRACE}")
    print(f"fundamental_D_K={D_K}")
    print(f"class_number={h}")
    print(f"class_factors={CLASS_FACTORS}")
    print(f"sqrt_floor_p={sqrt_p}")
    print(f"sqrt_floor_abs_D={sqrt_D}")
    print()
    print("divisor_split degree_a degree_b max_degree sum_degrees max_over_sqrt_p")

    rows: list[tuple[int, int, int, int, tuple[int, ...]]] = []
    seen: set[tuple[int, int]] = set()
    for r in range(len(CLASS_FACTORS) + 1):
        for comb in itertools.combinations(CLASS_FACTORS, r):
            a = math.prod(comb) if comb else 1
            b = h // a
            lo, hi = sorted((a, b))
            if (lo, hi) in seen:
                continue
            seen.add((lo, hi))
            rows.append((hi, lo + hi, lo, hi, comb))

    for _max_degree, _sum_degrees, lo, hi, comb in sorted(rows, key=lambda row: (row[0], row[1])):
        print(
            f"{comb!s:30s} {lo:12d} {hi:12d} {hi:12d} "
            f"{lo + hi:12d} {hi / sqrt_p:.6e}"
        )

    best = min(rows, key=lambda row: (row[0], row[1]))
    best_hi, best_sum, best_lo, _best_hi_again, best_comb = best
    print()
    print(f"best_balanced_factor_subset={best_comb}")
    print(f"best_degrees={best_lo}*{best_hi}")
    print(f"best_largest_degree={best_hi}")
    print(f"best_largest_degree_over_sqrt_p={best_hi / sqrt_p:.6e}")
    print(f"best_sum_degrees={best_sum}")
    print()
    print("known_method_obstruction")
    print("  decomposed_CM_reduces_root_degree_and_memory=1")
    print("  embedded_equations_required=1")
    print("  abstract_class_field_equation_suffices=0")
    print("  seed_CM_root_required_for_isogeny_orbit_enumeration=1")
    print("  known_embedded_construction_cost_scale=about_sqrt_abs_D_or_worse")
    print(
        "conclusion=smooth_class_group_makes_decomposed_CM_the_best_remaining_"
        "lead_but_known_embedded_methods_do_not_beat_sqrt_scale"
    )


if __name__ == "__main__":
    main()
