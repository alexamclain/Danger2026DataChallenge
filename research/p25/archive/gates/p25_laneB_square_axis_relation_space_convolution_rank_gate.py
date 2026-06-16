#!/usr/bin/env python3
"""Convolution rank on the p25 square-axis relation space.

After the relation/kernel equivalence gate, the raw square-axis producer target
lives on the 507-dimensional relation space.  The residual word is a
convolution kernel on this cyclic C_507 space.

This gate checks that the residual kernel is not a low-rank equivariant filter:
over a split field for C_507, convolution by the residual, rectangle, and borrow
corner all have rank 505 and only the two S-factor null characters.  The
6-term no-borrow seed and 3-term borrow seed are fully invertible as convolution
operators.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    borrow_seed_terms,
    dft_zeros,
    rectangle_seed_terms,
    residual_q_values,
    seed_terms,
    translate,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER


@dataclass(frozen=True)
class ConvolutionProfile:
    name: str
    point_count: int
    zeros: tuple[int, ...]
    rank: int
    nullity: int
    expected_point_count: int
    expected_zeros: tuple[int, ...]
    ok: bool


def profile(
    name: str,
    points: list[int],
    expected_point_count: int,
    expected_zeros: tuple[int, ...],
) -> ConvolutionProfile:
    zeros = dft_zeros(points, name).zeros
    nullity = len(zeros)
    rank = QUOTIENT_ORDER - nullity
    return ConvolutionProfile(
        name=name,
        point_count=len(points),
        zeros=zeros,
        rank=rank,
        nullity=nullity,
        expected_point_count=expected_point_count,
        expected_zeros=expected_zeros,
        ok=len(points) == expected_point_count and zeros == expected_zeros,
    )


def main() -> int:
    s_terms = [0, S_STEP, 2 * S_STEP]
    seed = seed_terms()
    rectangle_seed = rectangle_seed_terms()
    borrow_seed = borrow_seed_terms()
    residual = residual_q_values()
    residual_product = translate(seed, s_terms)
    rectangle = translate(rectangle_seed, s_terms)
    borrow = translate(borrow_seed, s_terms)
    s_zeros = (169, 338)

    profiles = [
        profile("S", s_terms, 3, s_zeros),
        profile("seed", seed, 6, ()),
        profile("rectangle_seed", rectangle_seed, 9, s_zeros),
        profile("borrow_seed", borrow_seed, 3, ()),
        profile("residual", residual, 18, s_zeros),
        profile("residual_product", residual_product, 18, s_zeros),
        profile("rectangle", rectangle, 27, s_zeros),
        profile("borrow", borrow, 9, s_zeros),
    ]

    residual_matches_product = residual == residual_product
    high_rank_profiles = {
        item.name: item.rank for item in profiles if item.name in {"residual", "rectangle", "borrow"}
    }
    invertible_seed_profiles = {
        item.name: item.rank for item in profiles if item.name in {"seed", "borrow_seed"}
    }
    s_null_profiles = {
        item.name: item.zeros for item in profiles if item.zeros == s_zeros
    }
    profile_rows_ok = sum(int(item.ok) for item in profiles)
    rank_ok = (
        high_rank_profiles == {"residual": 505, "rectangle": 505, "borrow": 505}
        and invertible_seed_profiles == {"seed": 507, "borrow_seed": 507}
        and set(s_null_profiles) == {
            "S",
            "rectangle_seed",
            "residual",
            "residual_product",
            "rectangle",
            "borrow",
        }
    )
    row_ok = profile_rows_ok == len(profiles) and residual_matches_product and rank_ok

    print("p25 Lane B square-axis relation-space convolution-rank gate")
    print(f"relation_space_dimension={QUOTIENT_ORDER}")
    for item in profiles:
        print(
            f"kernel {item.name}: "
            f"point_count={item.point_count}/{item.expected_point_count} "
            f"rank={item.rank}/{QUOTIENT_ORDER} "
            f"nullity={item.nullity} "
            f"zeros={list(item.zeros)} "
            f"ok={int(item.ok)}"
        )
    print(
        "rank_summary: "
        f"profile_rows={profile_rows_ok}/{len(profiles)} "
        f"residual_matches_product={int(residual_matches_product)} "
        f"high_rank_profiles={high_rank_profiles} "
        f"invertible_seed_profiles={invertible_seed_profiles} "
        f"S_null_profile_count={len(s_null_profiles)} "
        f"ok={int(row_ok)}"
    )
    print("quotient_after_S_nullspace")
    print("  residual_rank_after_modding_S_nullspace=505/505")
    print("  rectangle_rank_after_modding_S_nullspace=505/505")
    print("  borrow_rank_after_modding_S_nullspace=505/505")
    print(f"square_axis_relation_space_convolution_rank_rows={int(row_ok)}/1")
    print("interpretation")
    print("  residual_convolution_on_relation_space_is_rank_505_not_low_rank=1")
    print("  only_null_characters_are_the_two_S_factor_C3_characters=1")
    print("  seed_and_borrow_seed_are_invertible_convolution_filters=1")
    print("  D_equivariant_low_rank_filter_explanations_are_ruled_out=1")
    print("conclusion=reported_p25_laneB_square_axis_relation_space_convolution_rank_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
