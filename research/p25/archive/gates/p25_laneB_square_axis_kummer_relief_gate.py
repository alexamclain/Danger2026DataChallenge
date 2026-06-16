#!/usr/bin/env python3
"""Square-axis Kummer-relief gate for p25 Lane B.

The prime-axis Kummer/sign gate shows that the C_13 and C_53 anchors require a
full degree-c Kummer extension.  The square-axis C_169 target behaves
differently: the same single-anchor scalar has class index 13 modulo 169, so
its Kummer class has order 13 rather than 169.

This does not construct the missing producer, and it does not make the larger
C_3 x C_169 mask cheap.  It records a real p25-specific opportunity: if a
producer can tolerate the 507-point quotient, the anchor descent is only
degree 13.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_kummer_sign_descent_gate import KummerClass, kummer_class
from p25_laneB_punctured_hd_anchor_gate import make_context, primitive_root
from p25_selected_defect_value_gate import RIGHT_DEGREE


SQUARE_C_AXIS = 169


@dataclass(frozen=True)
class SquareKummerProfile:
    c_axis: int
    order: int
    base_field_q: int
    value_field_l: int
    primitive_root: int
    anchor: KummerClass
    neg_anchor: KummerClass
    sign: KummerClass


def class_order(c_axis: int, class_index: int) -> int:
    if class_index % c_axis == 0:
        return 1
    return c_axis // gcd(c_axis, class_index)


def square_profile() -> SquareKummerProfile:
    order = RIGHT_DEGREE * SQUARE_C_AXIS
    ctx = make_context(order)
    generator = primitive_root(ctx.value_field_l)
    anchor = (ctx.base_field_q - 2) % ctx.value_field_l
    return SquareKummerProfile(
        c_axis=SQUARE_C_AXIS,
        order=order,
        base_field_q=ctx.base_field_q,
        value_field_l=ctx.value_field_l,
        primitive_root=generator,
        anchor=kummer_class("anchor", anchor, SQUARE_C_AXIS, ctx.value_field_l, generator),
        neg_anchor=kummer_class(
            "-anchor", -anchor, SQUARE_C_AXIS, ctx.value_field_l, generator
        ),
        sign=kummer_class("-1", -1, SQUARE_C_AXIS, ctx.value_field_l, generator),
    )


def audit_profile(profile: SquareKummerProfile) -> tuple[list[str], bool]:
    anchor_order = class_order(profile.c_axis, profile.anchor.class_index)
    neg_anchor_order = class_order(profile.c_axis, profile.neg_anchor.class_index)
    root_degrees_are_multiples_of_13 = profile.anchor.root_degrees_up_to_c == tuple(
        range(13, profile.c_axis + 1, 13)
    )
    sign_does_not_change_class = (
        profile.sign.class_index == 0
        and profile.neg_anchor.class_index == profile.anchor.class_index
    )
    row_ok = (
        profile.anchor.class_index == 13
        and profile.neg_anchor.class_index == 13
        and anchor_order == 13
        and neg_anchor_order == 13
        and not profile.anchor.base_has_root
        and profile.anchor.minimal_extension_degree == 13
        and not profile.neg_anchor.base_has_root
        and profile.neg_anchor.minimal_extension_degree == 13
        and root_degrees_are_multiples_of_13
        and sign_does_not_change_class
    )
    lines = [
        (
            f"case square_axis_C3xC169: c={profile.c_axis} order={profile.order} "
            f"base_field_q={profile.base_field_q} value_field_l={profile.value_field_l} "
            f"primitive_root={profile.primitive_root} "
            f"anchor_class_index={profile.anchor.class_index} "
            f"anchor_class_order={anchor_order} "
            f"anchor_minimal_extension_degree={profile.anchor.minimal_extension_degree} "
            f"neg_anchor_class_index={profile.neg_anchor.class_index} "
            f"neg_anchor_class_order={neg_anchor_order} "
            f"neg_anchor_minimal_extension_degree={profile.neg_anchor.minimal_extension_degree} "
            f"sign_class_zero={int(profile.sign.class_index == 0)} "
            f"sign_does_not_change_anchor_class={int(sign_does_not_change_class)} "
            f"root_degrees_up_to_169={list(profile.anchor.root_degrees_up_to_c)} "
            f"ok={int(row_ok)}"
        )
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B square-axis Kummer-relief gate")
    print(f"right_degree={RIGHT_DEGREE}")
    profile = square_profile()
    lines, ok = audit_profile(profile)
    for line in lines:
        print(line)
    print(f"square_axis_kummer_relief_rows={int(ok)}/1")
    print("interpretation")
    print("  C169_anchor_class_has_order_13_not_169=1")
    print("  C169_anchor_and_negative_anchor_need_degree_13_kummer_extension=1")
    print("  sign_choice_still_does_not_change_the_anchor_kummer_class=1")
    print("  square_axis_anchor_descent_is_no_worse_than_the_C13_prime_axis=1")
    print("conclusion=reported_p25_laneB_square_axis_kummer_relief_gate")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
