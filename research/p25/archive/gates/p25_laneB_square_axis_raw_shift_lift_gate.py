#!/usr/bin/env python3
"""Raw source-cycle lift of the p25 square-axis quotient shifts.

The quotient-shift normal form lives on C_3 x C_169, equivalently the
507-cycle q = 169*right + 3*c.  The actual ray-local source for this lab is a
12675-cycle with B = 25 raw representatives above each quotient point.

This gate checks how the quotient shifts

    D = x^172, X = x^43, Y = x^9

lift to the raw source exponent e.  Each is visible as raw addition by the same
integer step, but the quotient relation D^3 = Y hides a kernel translate:

    3*172 = 516 = 9 + 507.

Thus D^3 and Y agree on C_3 x C_169 while differing by one B-kernel layer on
the raw source cycle.  A producer using the quotient-shift law must account for
this trace-kernel monodromy instead of imposing D^3 = Y before trace-down.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    PullbackCase,
    precompute_source_logs,
    quotient_coordinates,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    coord_from_q,
    q_from_coord,
    selected_terms,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE


@dataclass(frozen=True)
class ShiftAudit:
    name: str
    step: int
    vector: tuple[int, int]
    coordinate_hits: int
    kernel_delta_counts: dict[int, int]
    expected_kernel_delta_counts: dict[int, int]
    ok: bool


def square_axis_case() -> PullbackCase:
    for case in PULLBACK_CASES:
        if case.name == "square_axis_C3xC169":
            return case
    raise AssertionError("square-axis case missing")


def add_coord(
    left: tuple[int, int], right: tuple[int, int], c_axis: int
) -> tuple[int, int]:
    return (
        (left[0] + right[0]) % RIGHT_DEGREE,
        (left[1] + right[1]) % c_axis,
    )


def kernel_index(e_value: int, raw_order: int, quotient_order: int) -> int:
    e_mod = e_value % raw_order
    return e_mod // quotient_order


def expected_kernel_counts(step: int, quotient_order: int, b_trace: int) -> dict[int, int]:
    counts: Counter[int] = Counter()
    quotient_step = step % quotient_order
    base_delta = step // quotient_order
    for q_value in range(quotient_order):
        counts[base_delta + int(q_value + quotient_step >= quotient_order)] += b_trace
    return dict(sorted(counts.items()))


def audit_shift(
    name: str,
    step: int,
    case: PullbackCase,
    coordinates: list[tuple[int, int]],
) -> ShiftAudit:
    quotient_order = RIGHT_DEGREE * case.c_axis
    vector = coord_from_q(step % quotient_order)
    coordinate_hits = 0
    kernel_deltas: Counter[int] = Counter()
    for e_value, coord in enumerate(coordinates):
        shifted_e = (e_value + step) % case.raw_order
        expected_coord = add_coord(coord, vector, case.c_axis)
        coordinate_hits += int(coordinates[shifted_e] == expected_coord)
        delta = (
            kernel_index(shifted_e, case.raw_order, quotient_order)
            - kernel_index(e_value, case.raw_order, quotient_order)
        ) % case.b_trace
        kernel_deltas[delta] += 1
    expected = expected_kernel_counts(step, quotient_order, case.b_trace)
    row_ok = coordinate_hits == case.raw_order and dict(sorted(kernel_deltas.items())) == expected
    return ShiftAudit(
        name=name,
        step=step,
        vector=vector,
        coordinate_hits=coordinate_hits,
        kernel_delta_counts=dict(sorted(kernel_deltas.items())),
        expected_kernel_delta_counts=expected,
        ok=row_ok,
    )


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    source_logs = precompute_source_logs(case)
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]

    print("p25 Lane B square-axis raw-shift lift gate")
    print(
        f"case={case.name} raw_order={case.raw_order} "
        f"quotient_order={quotient_order} B={case.b_trace}"
    )
    audits = [
        audit_shift("D", S_STEP, case, coordinates),
        audit_shift("X", X_STEP, case, coordinates),
        audit_shift("Y", Y_STEP, case, coordinates),
        audit_shift("D_cubed", 3 * S_STEP, case, coordinates),
    ]
    ok_rows = 0
    for audit in audits:
        ok_rows += int(audit.ok)
        print(
            f"shift {audit.name}: step={audit.step} "
            f"quotient_step={audit.step % quotient_order} "
            f"vector={audit.vector} "
            f"coordinate_hits={audit.coordinate_hits}/{case.raw_order} "
            f"kernel_delta_counts={audit.kernel_delta_counts} "
            f"expected_kernel_delta_counts={audit.expected_kernel_delta_counts} "
            f"ok={int(audit.ok)}"
        )

    d3_y_quotient_hits = 0
    d3_y_raw_same_hits = 0
    d3_y_kernel_offsets: Counter[int] = Counter()
    for e_value in range(case.raw_order):
        d3_e = (e_value + 3 * S_STEP) % case.raw_order
        y_e = (e_value + Y_STEP) % case.raw_order
        d3_y_quotient_hits += int(coordinates[d3_e] == coordinates[y_e])
        d3_y_raw_same_hits += int(d3_e == y_e)
        offset = (
            kernel_index(d3_e, case.raw_order, quotient_order)
            - kernel_index(y_e, case.raw_order, quotient_order)
        ) % case.b_trace
        d3_y_kernel_offsets[offset] += 1

    selected_steps = sorted(
        S_STEP * s_value + X_STEP * (h_value + 1) + Y_STEP * t_value
        for s_value, h_value, t_value, _right, _c_coord in selected_terms()
    )
    selected_qs_from_raw_steps = sorted(step % quotient_order for step in selected_steps)
    selected_qs = sorted(
        q_from_coord(right, c_coord)
        for _s_value, _h_value, _t_value, right, c_coord in selected_terms()
    )
    selected_word_ok = (
        selected_steps == selected_qs
        and selected_qs_from_raw_steps == selected_qs
        and max(selected_steps) < quotient_order
    )
    relation_ok = (
        d3_y_quotient_hits == case.raw_order
        and d3_y_raw_same_hits == 0
        and dict(sorted(d3_y_kernel_offsets.items())) == {1: case.raw_order}
        and selected_word_ok
    )
    print(
        "relation D_cubed_vs_Y: "
        f"quotient_hits={d3_y_quotient_hits}/{case.raw_order} "
        f"raw_same_hits={d3_y_raw_same_hits}/{case.raw_order} "
        f"kernel_offsets={dict(sorted(d3_y_kernel_offsets.items()))} "
        f"ok={int(relation_ok)}"
    )
    print(
        "selected_word_raw_steps: "
        f"max_step={max(selected_steps)} "
        f"all_below_quotient_order={int(max(selected_steps) < quotient_order)} "
        f"raw_steps_match_selected_qs={int(selected_steps == selected_qs)} "
        f"ok={int(selected_word_ok)}"
    )
    row_ok = ok_rows == len(audits) and relation_ok
    print(f"square_axis_raw_shift_lift_rows={int(row_ok)}/1")
    print("interpretation")
    print("  quotient_shifts_are_visible_as_raw_source_cycle_additions=1")
    print("  D_cubed_equals_Y_only_after_quotienting_by_the_B_kernel=1")
    print("  raw_producers_must_account_for_the_one_layer_trace_kernel_monodromy=1")
    print("  selected_residual_word_uses_raw_steps_below_the_507_quotient_order=1")
    print("conclusion=reported_p25_laneB_square_axis_raw_shift_lift_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
