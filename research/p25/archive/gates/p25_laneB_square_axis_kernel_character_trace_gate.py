#!/usr/bin/env python3
"""Kernel-character trace obstruction for the p25 square-axis raw lift.

The raw-shift lift gate shows that D^3 and Y differ by one generator of the
B=25 trace kernel on the raw C_12675 source cycle.  This gate checks the
obvious attempted explanation: put the producer on a nontrivial C_25 kernel
character so that the one-layer monodromy is visible as a phase.

That works raw, but it dies under trace.  Over a split field for C_12675, every
nontrivial kernel character has zero trace to C_3 x C_169.  Therefore a
producer cannot explain the quotient residual using only a nontrivial kernel
mode; the surviving quotient payload must have a kernel-trivial component, and
any monodromy must cancel or trace out.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import CASES as PULLBACK_CASES, PullbackCase
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    q_from_coord,
    selected_terms,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class KernelModeAudit:
    mode: int
    trace_sum: int
    expected_trace_sum: int
    phase: int
    expected_phase: int
    selected_trace_nonzero: int
    selected_normalized_ones: int
    ok: bool


def square_axis_case() -> PullbackCase:
    for case in PULLBACK_CASES:
        if case.name == "square_axis_C3xC169":
            return case
    raise AssertionError("square-axis case missing")


def kernel_layer(e_value: int, quotient_order: int, raw_order: int) -> int:
    return (e_value % raw_order) // quotient_order


def mode_value(
    e_value: int,
    mode: int,
    zeta25: int,
    quotient_order: int,
    raw_order: int,
    modulus: int,
) -> int:
    return pow(zeta25, mode * kernel_layer(e_value, quotient_order, raw_order), modulus)


def trace_sum_for_q(
    q_value: int,
    mode: int,
    zeta25: int,
    quotient_order: int,
    raw_order: int,
    b_trace: int,
    modulus: int,
) -> int:
    return sum(
        mode_value(
            q_value + quotient_order * layer,
            mode,
            zeta25,
            quotient_order,
            raw_order,
            modulus,
        )
        for layer in range(b_trace)
    ) % modulus


def audit_mode(
    mode: int,
    zeta25: int,
    case: PullbackCase,
    modulus: int,
    selected_qs: list[int],
) -> KernelModeAudit:
    quotient_order = RIGHT_DEGREE * case.c_axis
    expected_trace_sum = case.b_trace % modulus if mode == 0 else 0
    trace_sums = {
        trace_sum_for_q(
            q_value,
            mode,
            zeta25,
            quotient_order,
            case.raw_order,
            case.b_trace,
            modulus,
        )
        for q_value in range(quotient_order)
    }
    if len(trace_sums) != 1:
        raise AssertionError(f"mode {mode} trace depends on q: {trace_sums}")
    trace_sum = next(iter(trace_sums))

    expected_phase = pow(zeta25, mode, modulus)
    phase_hits = 0
    for e_value in range(case.raw_order):
        lhs = mode_value(
            e_value + 3 * S_STEP,
            mode,
            zeta25,
            quotient_order,
            case.raw_order,
            modulus,
        )
        rhs = mode_value(
            e_value + Y_STEP,
            mode,
            zeta25,
            quotient_order,
            case.raw_order,
            modulus,
        )
        phase = lhs * pow(rhs, -1, modulus) % modulus
        phase_hits += int(phase == expected_phase)

    inv_b = pow(case.b_trace, -1, modulus)
    selected_traces = [
        trace_sum_for_q(
            q_value,
            mode,
            zeta25,
            quotient_order,
            case.raw_order,
            case.b_trace,
            modulus,
        )
        for q_value in selected_qs
    ]
    selected_trace_nonzero = sum(int(value % modulus != 0) for value in selected_traces)
    selected_normalized_ones = sum(int(value * inv_b % modulus == 1) for value in selected_traces)

    row_ok = (
        trace_sum == expected_trace_sum
        and phase_hits == case.raw_order
        and selected_trace_nonzero == (len(selected_qs) if mode == 0 else 0)
        and selected_normalized_ones == (len(selected_qs) if mode == 0 else 0)
    )
    return KernelModeAudit(
        mode=mode,
        trace_sum=trace_sum,
        expected_trace_sum=expected_trace_sum,
        phase=expected_phase,
        expected_phase=expected_phase,
        selected_trace_nonzero=selected_trace_nonzero,
        selected_normalized_ones=selected_normalized_ones,
        ok=row_ok,
    )


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta25 = pow(root, (modulus - 1) // case.b_trace, modulus)
    zeta_raw = pow(root, (modulus - 1) // case.raw_order, modulus)
    selected_qs = sorted(
        q_from_coord(right, c_coord)
        for _s_value, _h_value, _t_value, right, c_coord in selected_terms()
    )

    zeta25_ok = (
        pow(zeta25, case.b_trace, modulus) == 1
        and all(pow(zeta25, divisor, modulus) != 1 for divisor in (1, 5))
    )
    zeta_raw_ok = (
        pow(zeta_raw, case.raw_order, modulus) == 1
        and pow(zeta_raw, case.raw_order // 3, modulus) != 1
        and pow(zeta_raw, case.raw_order // 5, modulus) != 1
        and pow(zeta_raw, case.raw_order // 13, modulus) != 1
    )

    print("p25 Lane B square-axis kernel-character trace gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={quotient_order} "
        f"B={case.b_trace} modulus={modulus}"
    )
    print(
        f"roots: zeta25_order_ok={int(zeta25_ok)} "
        f"zeta_raw_order_ok={int(zeta_raw_ok)}"
    )

    audits = [
        audit_mode(mode, zeta25, case, modulus, selected_qs)
        for mode in range(case.b_trace)
    ]
    ok_rows = sum(int(audit.ok) for audit in audits)
    nontrivial_zero_trace = sum(
        int(audit.mode != 0 and audit.trace_sum == 0 and audit.selected_trace_nonzero == 0)
        for audit in audits
    )
    nontrivial_phase_visible = sum(
        int(audit.mode != 0 and audit.phase != 1)
        for audit in audits
    )
    for audit in audits[:6]:
        print(
            f"mode {audit.mode}: trace_sum={audit.trace_sum} "
            f"expected_trace_sum={audit.expected_trace_sum} "
            f"D3_over_Y_phase={audit.phase} "
            f"selected_trace_nonzero={audit.selected_trace_nonzero}/{len(selected_qs)} "
            f"selected_normalized_ones={audit.selected_normalized_ones}/{len(selected_qs)} "
            f"ok={int(audit.ok)}"
        )
    print(
        f"mode_summary: rows_ok={ok_rows}/{case.b_trace} "
        f"nontrivial_zero_trace={nontrivial_zero_trace}/{case.b_trace - 1} "
        f"nontrivial_phase_visible={nontrivial_phase_visible}/{case.b_trace - 1}"
    )
    print(
        "trace_dimensions: "
        f"raw_dimension={case.raw_order} "
        f"quotient_image_dimension={quotient_order} "
        f"nontrivial_kernel_dimension={(case.b_trace - 1) * quotient_order}"
    )
    row_ok = (
        zeta25_ok
        and zeta_raw_ok
        and ok_rows == case.b_trace
        and nontrivial_zero_trace == case.b_trace - 1
        and nontrivial_phase_visible == case.b_trace - 1
    )
    print(f"square_axis_kernel_character_trace_rows={int(row_ok)}/1")
    print("interpretation")
    print("  nontrivial_C25_kernel_characters_detect_the_raw_D_cubed_over_Y_monodromy=1")
    print("  nontrivial_C25_kernel_characters_trace_to_zero_on_C3xC169=1")
    print("  quotient_residual_requires_a_kernel_trivial_trace_surviving_component=1")
    print("  monodromy_must_cancel_or_trace_out_in_any_valid_raw_producer=1")
    print("conclusion=reported_p25_laneB_square_axis_kernel_character_trace_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
