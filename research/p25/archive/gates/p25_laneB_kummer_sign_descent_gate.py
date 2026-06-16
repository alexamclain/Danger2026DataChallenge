#!/usr/bin/env python3
"""Kummer/sign descent gate for the p25 Lane B single anchor.

The punctured Hasse-Davenport gate shows that replacing the single degenerate
anchor J(1,1)=q-2 by 1 fixes the product-formula identities, but that the
anchor scalar has no c-th root in the small Jacobi value field.

This gate sharpens that statement.  It computes the class of q-2 in
F_l^*/(F_l^*)^c, checks the negative sign, and determines the minimal finite
field extension degree in which a c-th root can exist.

For the p25 prime-axis labs, -1 is already a c-th power in the value field, so
the sign choice does not change the Kummer class.  The anchor class is
primitive, hence the minimal Kummer extension degree is exactly c.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd

from p25_laneB_punctured_hd_anchor_gate import (
    CASES as ANCHOR_CASES,
    AnchorCase,
    make_context,
    primitive_root,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class KummerClass:
    name: str
    value: int
    log_index: int
    class_index: int
    base_has_root: bool
    minimal_extension_degree: int
    root_degrees_up_to_c: tuple[int, ...]


def discrete_log_index(value: int, modulus: int, generator: int) -> int:
    residue = 1
    for exponent in range(modulus - 1):
        if residue == value % modulus:
            return exponent
        residue = residue * generator % modulus
    raise AssertionError("missing discrete log")


def has_c_root_in_degree(value: int, c_axis: int, value_field_l: int, degree: int) -> bool:
    if (pow(value_field_l, degree, c_axis) - 1) % c_axis:
        return False
    exponent = (value_field_l**degree - 1) // c_axis
    return pow(value % value_field_l, exponent, value_field_l) == 1


def minimal_extension_degree(c_axis: int, class_index: int) -> int:
    if class_index % c_axis == 0:
        return 1
    return c_axis // gcd(c_axis, class_index)


def kummer_class(
    name: str, value: int, c_axis: int, value_field_l: int, generator: int
) -> KummerClass:
    log_index = discrete_log_index(value, value_field_l, generator)
    class_index = log_index % c_axis
    root_degrees = tuple(
        degree
        for degree in range(1, c_axis + 1)
        if has_c_root_in_degree(value, c_axis, value_field_l, degree)
    )
    return KummerClass(
        name=name,
        value=value % value_field_l,
        log_index=log_index,
        class_index=class_index,
        base_has_root=class_index == 0,
        minimal_extension_degree=minimal_extension_degree(c_axis, class_index),
        root_degrees_up_to_c=root_degrees,
    )


def audit_case(case: AnchorCase) -> tuple[list[str], bool]:
    c_axis = case.c_axis
    ctx = make_context(RIGHT_DEGREE * c_axis)
    generator = primitive_root(ctx.value_field_l)
    anchor = (ctx.base_field_q - 2) % ctx.value_field_l
    rows = (
        kummer_class("anchor", anchor, c_axis, ctx.value_field_l, generator),
        kummer_class("-anchor", -anchor, c_axis, ctx.value_field_l, generator),
        kummer_class("-1", -1, c_axis, ctx.value_field_l, generator),
    )
    by_name = {row.name: row for row in rows}
    anchor_row = by_name["anchor"]
    neg_anchor_row = by_name["-anchor"]
    sign_row = by_name["-1"]

    sign_does_not_change_class = (
        sign_row.class_index == 0
        and neg_anchor_row.class_index == anchor_row.class_index
    )
    primitive_anchor_class = gcd(anchor_row.class_index, c_axis) == 1
    primitive_neg_anchor_class = gcd(neg_anchor_row.class_index, c_axis) == 1
    full_degree_anchor = (
        not anchor_row.base_has_root
        and anchor_row.minimal_extension_degree == c_axis
        and anchor_row.root_degrees_up_to_c == (c_axis,)
    )
    full_degree_neg_anchor = (
        not neg_anchor_row.base_has_root
        and neg_anchor_row.minimal_extension_degree == c_axis
        and neg_anchor_row.root_degrees_up_to_c == (c_axis,)
    )
    sign_is_base_root = (
        sign_row.base_has_root
        and sign_row.minimal_extension_degree == 1
        and sign_row.root_degrees_up_to_c == tuple(range(1, c_axis + 1))
    )
    row_ok = (
        sign_does_not_change_class
        and primitive_anchor_class
        and primitive_neg_anchor_class
        and full_degree_anchor
        and full_degree_neg_anchor
        and sign_is_base_root
    )

    class_lines = [
        (
            f"{row.name}: value={row.value} log_index={row.log_index} "
            f"class_index={row.class_index} "
            f"base_has_{c_axis}th_root={int(row.base_has_root)} "
            f"minimal_extension_degree={row.minimal_extension_degree} "
            f"root_degrees_up_to_c={list(row.root_degrees_up_to_c)}"
        )
        for row in rows
    ]
    lines = [
        (
            f"case {case.name}: c={c_axis} order={RIGHT_DEGREE * c_axis} "
            f"base_field_q={ctx.base_field_q} value_field_l={ctx.value_field_l} "
            f"primitive_root={generator} "
            f"anchor_class_primitive={int(primitive_anchor_class)} "
            f"neg_anchor_class_primitive={int(primitive_neg_anchor_class)} "
            f"sign_class_zero={int(sign_row.class_index == 0)} "
            f"sign_does_not_change_anchor_class={int(sign_does_not_change_class)} "
            f"anchor_requires_full_degree_c={int(full_degree_anchor)} "
            f"neg_anchor_requires_full_degree_c={int(full_degree_neg_anchor)} "
            f"ok={int(row_ok)}"
        ),
        *[f"  {line}" for line in class_lines],
    ]
    return lines, row_ok


def main() -> int:
    print("p25 Lane B Kummer/sign descent gate")
    print(f"right_degree={RIGHT_DEGREE}")
    ok_rows = 0
    for case in ANCHOR_CASES:
        lines, ok = audit_case(case)
        ok_rows += int(ok)
        for line in lines:
            print(line)
    print(f"kummer_sign_descent_rows={ok_rows}/{len(ANCHOR_CASES)}")
    print("interpretation")
    print("  sign_choice_does_not_change_the_anchor_kummer_class=1")
    print("  anchor_class_is_primitive_in_F_l_star_mod_c_powers=1")
    print("  anchor_and_negative_anchor_need_full_degree_c_kummer_extension=1")
    print("  no_base_field_or_sign_only_descent_can_supply_the_single_anchor_root=1")
    print("conclusion=reported_p25_laneB_kummer_sign_descent_gate")
    return 0 if ok_rows == len(ANCHOR_CASES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
