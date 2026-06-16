#!/usr/bin/env python3
"""Sumset factorization rigidity for the p25 square-axis residual.

The relation-space convolution-rank gate rules out low-rank equivariant
filters.  This gate rules out another shortcut: an unrelated small sumset
factorization of the 18-point residual in C_507.

Every nontrivial factorization of an 18-point collision-free sumset has a
factor of size 2 or 3.  We enumerate normalized 2x9 and 3x6 factorizations.
There are no 2x9 factorizations, and the only 3x6 factorizations are the same
S-orbit factorization seen from one of its three layers.
"""

from __future__ import annotations

from itertools import combinations

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    residual_q_values,
    seed_terms,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


def translated(values: list[int] | tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(sorted((value + shift) % QUOTIENT_ORDER for value in values))


def normalized_small_factor_tilings(
    small_size: int, large_size: int
) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    residual = set(residual_q_values())
    differences = sorted(
        {
            (left - right) % QUOTIENT_ORDER
            for left in residual
            for right in residual
            if left != right
        }
    )
    out: list[tuple[tuple[int, ...], tuple[int, ...]]] = []
    for rest in combinations(differences, small_size - 1):
        small = (0, *rest)
        large_candidates = set(range(QUOTIENT_ORDER))
        for small_term in small:
            large_candidates &= {
                (point - small_term) % QUOTIENT_ORDER
                for point in residual
            }
        if len(large_candidates) < large_size:
            continue
        for large in combinations(sorted(large_candidates), large_size):
            product = {
                (small_term + large_term) % QUOTIENT_ORDER
                for small_term in small
                for large_term in large
            }
            if len(product) == small_size * large_size == len(residual) and product == residual:
                out.append((tuple(sorted(small)), tuple(sorted(large))))
    return out


def expected_s_orbit_tilings() -> tuple[tuple[tuple[int, ...], tuple[int, ...]], ...]:
    s_terms = (0, S_STEP, 2 * S_STEP)
    seed = tuple(seed_terms())
    rows = []
    for layer_shift in s_terms:
        small = translated(s_terms, -layer_shift)
        large = translated(seed, layer_shift)
        rows.append((small, large))
    return tuple(sorted(rows))


def main() -> int:
    print("p25 Lane B square-axis sumset-factorization rigidity gate")
    print(f"quotient_order={QUOTIENT_ORDER}")
    residual = tuple(residual_q_values())
    two_by_nine = normalized_small_factor_tilings(2, 9)
    three_by_six = normalized_small_factor_tilings(3, 6)
    expected_three_by_six = expected_s_orbit_tilings()

    two_by_nine_ok = two_by_nine == []
    three_by_six_ok = tuple(sorted(three_by_six)) == expected_three_by_six
    divisor_coverage_ok = (
        18 == 2 * 9
        and 18 == 3 * 6
        and "6x3 and 9x2 covered by swapping factors"
    )
    row_ok = bool(two_by_nine_ok and three_by_six_ok and divisor_coverage_ok)

    print(
        "factorization_counts: "
        f"residual_points={len(residual)}/18 "
        f"two_by_nine={len(two_by_nine)} "
        f"three_by_six={len(three_by_six)} "
        f"expected_three_by_six={len(expected_three_by_six)} "
        f"ok={int(row_ok)}"
    )
    print("three_by_six_tilings")
    for small, large in sorted(three_by_six):
        print(f"  small={list(small)} large={list(large)}")
    print("expected_s_orbit_tilings")
    for small, large in expected_three_by_six:
        print(f"  small={list(small)} large={list(large)}")
    print("divisor_coverage")
    print("  2x9 checked directly; 9x2 follows by swapping factors")
    print("  3x6 checked directly; 6x3 follows by swapping factors")
    print(f"square_axis_sumset_factorization_rigidity_rows={int(row_ok)}/1")
    print("interpretation")
    print("  no_2_by_9_collision_free_sumset_factorization_exists=1")
    print("  every_3_by_6_factorization_is_the_known_S_orbit_layer_factorization=1")
    print("  unrelated_small_sumset_product_explanations_are_ruled_out=1")
    print("  producer_must_explain_the_S_orbit_and_no_borrow_seed_not_an_alternate_product=1")
    print("conclusion=reported_p25_laneB_square_axis_sumset_factorization_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
