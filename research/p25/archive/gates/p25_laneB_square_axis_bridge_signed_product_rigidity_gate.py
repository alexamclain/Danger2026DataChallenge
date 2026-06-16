#!/usr/bin/env python3
"""Signed product rigidity for the p25 square-axis bridge.

The bridge has the known product

    S * X * Y^-2 * (1 - X^2Y^3).

The bridge factorization gate checked this inside the oriented family
S*x^base*(1-x^step).  This gate broadens the search to every normalized signed
collision-free 2 x 3 product in Z[C_507].  If a six-point bridge producer is a
small signed product, this enumeration should find it.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product

from p25_laneB_square_axis_bridge_factorization_gate import (
    BRIDGE_STEP,
    bridge_coefficients,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP
from p25_laneB_square_axis_inversion_partner_uniqueness_gate import (
    ANOMALY_BASE,
    PARTNER_BASE,
    s_layer,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


Factor = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class SignedProduct:
    two_factor: Factor
    three_factor: Factor
    two_direction: int
    two_sign: int
    three_support: tuple[int, int, int]
    three_coefficients: tuple[int, int, int]
    is_forward_bridge: bool
    is_reverse_bridge: bool


def convolution(left: Factor, right: Factor) -> dict[int, int]:
    out: dict[int, int] = {}
    for left_q, left_coeff in left:
        for right_q, right_coeff in right:
            q_value = (left_q + right_q) % QUOTIENT_ORDER
            out[q_value] = out.get(q_value, 0) + left_coeff * right_coeff
    return {q_value: value for q_value, value in sorted(out.items()) if value}


def normalized_signed_products() -> tuple[SignedProduct, ...]:
    target = bridge_coefficients()
    target_support = tuple(target)
    matches: list[SignedProduct] = []
    for direction in range(1, QUOTIENT_ORDER):
        for two_sign in (1, -1):
            two_factor = ((0, 1), (direction, two_sign))
            for support in combinations(target_support, 3):
                for coefficients in product((1, -1), repeat=3):
                    three_factor = tuple(zip(support, coefficients))
                    if convolution(two_factor, three_factor) != target:
                        continue
                    matches.append(
                        SignedProduct(
                            two_factor=two_factor,
                            three_factor=three_factor,
                            two_direction=direction,
                            two_sign=two_sign,
                            three_support=support,  # type: ignore[arg-type]
                            three_coefficients=coefficients,  # type: ignore[arg-type]
                            is_forward_bridge=(
                                direction == BRIDGE_STEP
                                and two_sign == -1
                                and support == tuple(sorted(s_layer(PARTNER_BASE)))
                                and coefficients == (1, 1, 1)
                            ),
                            is_reverse_bridge=(
                                direction == (-BRIDGE_STEP) % QUOTIENT_ORDER
                                and two_sign == -1
                                and support == tuple(sorted(s_layer(ANOMALY_BASE)))
                                and coefficients == (-1, -1, -1)
                            ),
                        )
                    )
    return tuple(matches)


def factor_support_is_collision_free(product_row: SignedProduct) -> bool:
    sums = [
        (left_q + right_q) % QUOTIENT_ORDER
        for left_q, _left_coeff in product_row.two_factor
        for right_q, _right_coeff in product_row.three_factor
    ]
    return len(sums) == len(set(sums)) == 6


def main() -> int:
    print("p25 Lane B square-axis bridge signed-product rigidity gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} S_step={S_STEP} "
        f"bridge_step={BRIDGE_STEP} reverse_step={(-BRIDGE_STEP) % QUOTIENT_ORDER}"
    )
    matches = normalized_signed_products()
    direction_counts = Counter(
        (row.two_direction, row.two_sign) for row in matches
    )
    support_counts = Counter(row.three_support for row in matches)
    all_collision_free = all(factor_support_is_collision_free(row) for row in matches)
    expected_matches = (
        SignedProduct(
            two_factor=((0, 1), (BRIDGE_STEP, -1)),
            three_factor=tuple((q_value, 1) for q_value in sorted(s_layer(PARTNER_BASE))),
            two_direction=BRIDGE_STEP,
            two_sign=-1,
            three_support=tuple(sorted(s_layer(PARTNER_BASE))),
            three_coefficients=(1, 1, 1),
            is_forward_bridge=True,
            is_reverse_bridge=False,
        ),
        SignedProduct(
            two_factor=((0, 1), ((-BRIDGE_STEP) % QUOTIENT_ORDER, -1)),
            three_factor=tuple((q_value, -1) for q_value in sorted(s_layer(ANOMALY_BASE))),
            two_direction=(-BRIDGE_STEP) % QUOTIENT_ORDER,
            two_sign=-1,
            three_support=tuple(sorted(s_layer(ANOMALY_BASE))),
            three_coefficients=(-1, -1, -1),
            is_forward_bridge=False,
            is_reverse_bridge=True,
        ),
    )
    row_ok = (
        matches == expected_matches
        and all_collision_free
        and direction_counts == Counter({(BRIDGE_STEP, -1): 1, ((-BRIDGE_STEP) % QUOTIENT_ORDER, -1): 1})
        and support_counts == Counter(
            {
                tuple(sorted(s_layer(PARTNER_BASE))): 1,
                tuple(sorted(s_layer(ANOMALY_BASE))): 1,
            }
        )
    )

    print(
        "signed_product_scan: "
        f"target_support={sorted(bridge_coefficients().items())} "
        f"normalized_2x3_matches={len(matches)} "
        f"collision_free_matches={sum(factor_support_is_collision_free(row) for row in matches)} "
        f"all_collision_free={int(all_collision_free)} "
        f"ok={int(row_ok)}"
    )
    print(f"direction_counts={dict(sorted(direction_counts.items()))}")
    print(f"three_support_counts={dict(sorted(support_counts.items()))}")
    print("matches")
    for row in matches:
        print(f"  {row}")
    print("factor_laws")
    print("  forward = (1 - x^113) * (+S*X*Y^-2)")
    print("  reverse = (1 - x^394) * (-S*X^3Y)")
    print("interpretation")
    print("  bridge_has_no_unrelated_signed_2x3_product_factorization=1")
    print("  every_signed_product_explanation_is_the_known_S_layer_times_bridge_edge=1")
    print("  reverse_orientation_adds_no_new_producer_geometry=1")
    print("  producer_must_explain_the_same_S_parallel_top_to_bottom_edge=1")
    print(f"square_axis_bridge_signed_product_rigidity_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_signed_product_rigidity_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
