#!/usr/bin/env python3
"""Square-axis quotient-shift normal form for p25 Lane B.

The group-ring normal form is written on the exponent cycle C_507.  This gate
translates its factors back to the quotient coordinates C_3 x C_169.

For q = 169*r + 3*c, the group-ring steps act as:

    D = x^172 : (r,c) -> (r+1, c+1)
    X = x^43  : (r,c) -> (r+1, c-42)
    Y = x^9   : (r,c) -> (r,   c+3)

and D^3 = Y.  Thus the residual is

    D^s X^(h+1) Y^t,  s=0,1,2; h=0,1,2; t=0..h.

This is the quotient-coordinate version of the triangular/no-borrow comb.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_canonical_half_arc_gate import template_bits
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
    borrow_seed_terms,
    rectangle_seed_terms,
    seed_terms,
    translate,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    SQUARE_C,
    triangular_parameters,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


BASE_C = 13


@dataclass(frozen=True)
class ShiftVector:
    name: str
    exponent_step: int
    right_step: int
    c_step: int


def coord_from_q(q_value: int) -> tuple[int, int]:
    right = q_value % RIGHT_DEGREE
    c_coord = ((q_value - SQUARE_C * right) // RIGHT_DEGREE) % SQUARE_C
    return right, c_coord


def q_from_coord(right: int, c_coord: int) -> int:
    return (SQUARE_C * right + RIGHT_DEGREE * c_coord) % QUOTIENT_ORDER


def shift_vector(name: str, step: int) -> ShiftVector:
    right, c_coord = coord_from_q(step % QUOTIENT_ORDER)
    return ShiftVector(name, step % QUOTIENT_ORDER, right, c_coord)


def add_coord(
    left: tuple[int, int], right: tuple[int, int]
) -> tuple[int, int]:
    return (
        (left[0] + right[0]) % RIGHT_DEGREE,
        (left[1] + right[1]) % SQUARE_C,
    )


def mul_coord(vector: tuple[int, int], scalar: int) -> tuple[int, int]:
    return (
        scalar * vector[0] % RIGHT_DEGREE,
        scalar * vector[1] % SQUARE_C,
    )


def selected_terms() -> list[tuple[int, int, int, int, int]]:
    rows: list[tuple[int, int, int, int, int]] = []
    for s_value in range(3):
        for h_value in range(3):
            for t_value in range(h_value + 1):
                q_value = (
                    S_STEP * s_value
                    + X_STEP * (h_value + 1)
                    + Y_STEP * t_value
                ) % QUOTIENT_ORDER
                right, c_coord = coord_from_q(q_value)
                rows.append((s_value, h_value, t_value, right, c_coord))
    return rows


def term_to_local_shape(
    h_value: int, right: int, c_coord: int
) -> tuple[int, int, int, int]:
    residue = c_coord % BASE_C
    fiber = c_coord // BASE_C
    local_h = (right - residue) % RIGHT_DEGREE
    bit = template_bits(BASE_C, residue)[right]
    return residue, fiber, local_h, bit


def main() -> int:
    print("p25 Lane B square-axis quotient-shift normal-form gate")
    print(f"right_degree={RIGHT_DEGREE} square_c={SQUARE_C} quotient_order={QUOTIENT_ORDER}")
    d_shift = shift_vector("D", S_STEP)
    x_shift = shift_vector("X", X_STEP)
    y_shift = shift_vector("Y", Y_STEP)
    shifts = (d_shift, x_shift, y_shift)
    d_cubed = mul_coord((d_shift.right_step, d_shift.c_step), 3)
    step_rows_ok = (
        d_shift == ShiftVector("D", 172, 1, 1)
        and x_shift == ShiftVector("X", 43, 1, 127)
        and y_shift == ShiftVector("Y", 9, 0, 3)
        and d_cubed == (y_shift.right_step, y_shift.c_step)
    )

    selected = selected_terms()
    expected_qs = sorted(q_value for *_prefix, q_value in triangular_parameters())
    selected_qs = sorted(q_from_coord(right, c_coord) for _s, _h, _t, right, c_coord in selected)
    layer_counts = [0, 0, 0]
    h_counts = [0, 0, 0]
    t_counts = [0, 0, 0]
    local_shape_hits = 0
    graph_hits = 0
    shift_formula_hits = 0
    for s_value, h_value, t_value, right, c_coord in selected:
        layer_counts[s_value] += 1
        h_counts[h_value] += 1
        t_counts[t_value] += 1
        direct = add_coord(
            mul_coord((d_shift.right_step, d_shift.c_step), s_value),
            add_coord(
                mul_coord((x_shift.right_step, x_shift.c_step), h_value + 1),
                mul_coord((y_shift.right_step, y_shift.c_step), t_value),
            ),
        )
        shift_formula_hits += int(direct == (right, c_coord))
        residue, fiber, local_h, bit = term_to_local_shape(h_value, right, c_coord)
        local_shape_hits += int(
            local_h == h_value
            and fiber == 9 - 3 * h_value
            and bit == 1
        )
        graph_hits += int(
            c_coord == (residue + BASE_C * (9 - 3 * h_value)) % SQUARE_C
        )

    s_terms = [0, S_STEP, 2 * S_STEP]
    rectangle = translate(rectangle_seed_terms(), s_terms)
    borrow = translate(borrow_seed_terms(), s_terms)
    residual = translate(seed_terms(), s_terms)
    rectangle_coords = {coord_from_q(q_value) for q_value in rectangle}
    borrow_coords = {coord_from_q(q_value) for q_value in borrow}
    residual_coords = {coord_from_q(q_value) for q_value in residual}
    selected_coords = {(right, c_coord) for _s, _h, _t, right, c_coord in selected}
    coordinate_subtraction_ok = (
        residual_coords == selected_coords
        and residual_coords.isdisjoint(borrow_coords)
        and residual_coords | borrow_coords == rectangle_coords
    )

    row_ok = (
        step_rows_ok
        and selected_qs == expected_qs
        and len(selected_coords) == len(selected) == 18
        and layer_counts == [6, 6, 6]
        and h_counts == [3, 6, 9]
        and t_counts == [9, 6, 3]
        and shift_formula_hits == 18
        and local_shape_hits == 18
        and graph_hits == 18
        and len(rectangle_coords) == 27
        and len(borrow_coords) == 9
        and coordinate_subtraction_ok
    )
    print(
        f"shift_vectors: "
        f"D=({d_shift.right_step},{d_shift.c_step}) "
        f"X=({x_shift.right_step},{x_shift.c_step}) "
        f"Y=({y_shift.right_step},{y_shift.c_step}) "
        f"D_cubed={d_cubed} "
        f"step_rows_ok={int(step_rows_ok)}"
    )
    print(
        f"quotient_shift_word: "
        f"selected_count={len(selected)}/18 "
        f"selected_qs_match={int(selected_qs == expected_qs)} "
        f"layer_counts={layer_counts} "
        f"h_counts={h_counts} "
        f"t_counts={t_counts} "
        f"shift_formula_hits={shift_formula_hits}/18 "
        f"local_shape_hits={local_shape_hits}/18 "
        f"graph_hits={graph_hits}/18 "
        f"rectangle_coord_count={len(rectangle_coords)}/27 "
        f"borrow_coord_count={len(borrow_coords)}/9 "
        f"coordinate_subtraction_ok={int(coordinate_subtraction_ok)} "
        f"ok={int(row_ok)}"
    )
    print("selected_terms")
    for s_value, h_value, t_value, right, c_coord in sorted(selected, key=lambda row: q_from_coord(row[3], row[4])):
        residue, fiber, local_h, bit = term_to_local_shape(h_value, right, c_coord)
        print(
            f"  q={q_from_coord(right, c_coord)}: "
            f"s={s_value} h={h_value} t={t_value} "
            f"right={right} c={c_coord} a={residue} b={fiber} "
            f"local_h={local_h} trace_bit={bit}"
        )
    print("quotient_shift_law")
    print("  D = (right+1, c+1), X = (right+1, c-42), Y = (right, c+3)")
    print("  D^3 = Y")
    print("  residual = {D^s X^(h+1) Y^t : s=0,1,2; h=0,1,2; t=0..h}")
    print(f"square_axis_quotient_shift_normal_form_rows={int(row_ok)}/1")
    print("interpretation")
    print("  group_ring_factors_are_concrete_quotient_coordinate_shifts=1")
    print("  S_factor_is_three_diagonal_translates_with_D_cubed_equal_Y=1")
    print("  no_borrow_seed_lands_exactly_on_the_boundary_graph_fibers=1")
    print("  rectangle_minus_borrow_corner_holds_in_quotient_coordinates=1")
    print("conclusion=reported_p25_laneB_square_axis_quotient_shift_normal_form_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
