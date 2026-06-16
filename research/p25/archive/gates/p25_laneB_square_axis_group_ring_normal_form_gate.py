#!/usr/bin/env python3
"""Square-axis group-ring normal form for p25 Lane B.

The no-borrow digit gate rewrites the square-axis residual classes as a small
digit carry.  This gate packages the same selector as a short group-ring word
in Z[C_507].

Let X = x^43, Y = x^9, and S = 1 + x^172 + x^344.  The residual comb is

    S * (X + X^2 + X^2 Y + X^3 + X^3 Y + X^3 Y^2).

Equivalently it is the 27-term rectangle

    S * (X + X^2 + X^3) * (1 + Y + Y^2)

with the 9-term borrow corner

    S * (X Y + X Y^2 + X^2 Y^2)

removed.  This is the group-ring shadow of the base-3 no-borrow selector.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    triangular_parameters,
)


MODULUS = 2029
X_STEP = 43
Y_STEP = 9
S_STEP = 172


@dataclass(frozen=True)
class FourierZeros:
    name: str
    point_count: int
    zero_count: int
    zeros: tuple[int, ...]


def residual_q_values() -> list[int]:
    return sorted(q_value for *_prefix, q_value in triangular_parameters())


def translate(points: list[int], shifts: list[int]) -> list[int]:
    return sorted((point + shift) % QUOTIENT_ORDER for shift in shifts for point in points)


def seed_terms() -> list[int]:
    return sorted(
        X_STEP * (h_value + 1) + Y_STEP * t_value
        for h_value in range(3)
        for t_value in range(h_value + 1)
    )


def rectangle_seed_terms() -> list[int]:
    return sorted(
        X_STEP * (h_value + 1) + Y_STEP * t_value
        for h_value in range(3)
        for t_value in range(3)
    )


def borrow_seed_terms() -> list[int]:
    return sorted(
        X_STEP * (h_value + 1) + Y_STEP * t_value
        for h_value in range(3)
        for t_value in range(h_value + 1, 3)
    )


def dft_zeros(points: list[int], name: str) -> FourierZeros:
    root = primitive_root(MODULUS)
    zeta = pow(root, (MODULUS - 1) // QUOTIENT_ORDER, MODULUS)
    zeros: list[int] = []
    for frequency in range(QUOTIENT_ORDER):
        total = sum(pow(zeta, frequency * point, MODULUS) for point in points) % MODULUS
        if total == 0:
            zeros.append(frequency)
    return FourierZeros(
        name=name,
        point_count=len(points),
        zero_count=len(zeros),
        zeros=tuple(zeros),
    )


def main() -> int:
    print("p25 Lane B square-axis group-ring normal-form gate")
    print(f"quotient_order={QUOTIENT_ORDER} modulus={MODULUS}")
    s_terms = [0, S_STEP, 2 * S_STEP]
    seed = seed_terms()
    rectangle_seed = rectangle_seed_terms()
    borrow_seed = borrow_seed_terms()
    residual = residual_q_values()
    product = translate(seed, s_terms)
    rectangle = translate(rectangle_seed, s_terms)
    borrow = translate(borrow_seed, s_terms)
    residual_from_subtraction = sorted(set(rectangle) - set(borrow))
    collision_free = (
        len(product) == len(set(product)) == 18
        and len(rectangle) == len(set(rectangle)) == 27
        and len(borrow) == len(set(borrow)) == 9
    )
    subtraction_ok = (
        set(product).isdisjoint(set(borrow))
        and set(product) | set(borrow) == set(rectangle)
        and residual_from_subtraction == residual
    )
    zero_profiles = [
        dft_zeros(s_terms, "S"),
        dft_zeros(seed, "seed"),
        dft_zeros(rectangle_seed, "rectangle_seed"),
        dft_zeros(borrow_seed, "borrow_seed"),
        dft_zeros(product, "residual_product"),
        dft_zeros(rectangle, "rectangle"),
        dft_zeros(borrow, "borrow"),
    ]
    expected_zero_profiles = {
        "S": (2, (169, 338)),
        "seed": (0, ()),
        "rectangle_seed": (2, (169, 338)),
        "borrow_seed": (0, ()),
        "residual_product": (2, (169, 338)),
        "rectangle": (2, (169, 338)),
        "borrow": (2, (169, 338)),
    }

    zero_rows_ok = sum(
        int(
            profile.zero_count == expected_zero_profiles[profile.name][0]
            and profile.zeros == expected_zero_profiles[profile.name][1]
        )
        for profile in zero_profiles
    )
    row_ok = (
        s_terms == [0, 172, 344]
        and seed == [43, 86, 95, 129, 138, 147]
        and rectangle_seed == [43, 52, 61, 86, 95, 104, 129, 138, 147]
        and borrow_seed == [52, 61, 104]
        and product == residual
        and collision_free
        and subtraction_ok
        and zero_rows_ok == len(zero_profiles)
        and zero_profiles[4].zero_count == 2
    )
    print(
        f"group_ring_normal_form: "
        f"S_terms={s_terms} "
        f"seed_terms={seed} "
        f"rectangle_seed_terms={rectangle_seed} "
        f"borrow_seed_terms={borrow_seed} "
        f"product_count={len(product)}/18 "
        f"rectangle_count={len(rectangle)}/27 "
        f"borrow_count={len(borrow)}/9 "
        f"collision_free={int(collision_free)} "
        f"subtraction_ok={int(subtraction_ok)} "
        f"zero_profile_rows={zero_rows_ok}/{len(zero_profiles)} "
        f"ok={int(row_ok)}"
    )
    print(f"residual_product={product}")
    print(f"rectangle={rectangle}")
    print(f"borrow_corner={borrow}")
    print("fourier_zero_profiles")
    for profile in zero_profiles:
        print(
            f"  {profile.name}: point_count={profile.point_count} "
            f"zero_count={profile.zero_count} zeros={list(profile.zeros)}"
        )
    print("group_ring_law")
    print("  S = 1 + x^172 + x^344")
    print("  X = x^43, Y = x^9")
    print("  residual = S * (X + X^2 + X^2Y + X^3 + X^3Y + X^3Y^2)")
    print("  residual = S*(X+X^2+X^3)*(1+Y+Y^2) - S*(XY + XY^2 + X^2Y^2)")
    print(f"square_axis_group_ring_normal_form_rows={int(row_ok)}/1")
    print("interpretation")
    print("  triangular_comb_has_short_group_ring_normal_form=1")
    print("  no_borrow_selector_is_rectangle_minus_borrow_corner=1")
    print("  residual_product_has_only_the_two_S_factor_fourier_zeros=1")
    print("  producer_can_target_a_short_group_ring_word_not_an_opaque_18_set=1")
    print("conclusion=reported_p25_laneB_square_axis_group_ring_normal_form_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
