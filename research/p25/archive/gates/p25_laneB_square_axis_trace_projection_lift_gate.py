#!/usr/bin/env python3
"""Trace projection versus kernel-trivial lift for the p25 square-axis residual.

The kernel-character trace gate shows that nontrivial C_25 modes vanish under
trace.  This gate makes the corresponding producer-contract distinction
explicit.

There are raw lifts with only 18 nonzero representatives that trace to the same
18-class quotient residual.  They are not block-constant: their hidden C_25
kernel Fourier support is full.  The Lane B raw producer harness deliberately
requires the stronger kernel-trivial/block-constant lift, whose 450 raw
positions have only kernel mode 0.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import CASES as PULLBACK_CASES, PullbackCase
from p25_laneB_square_axis_quotient_shift_normal_form_gate import (
    q_from_coord,
    selected_terms,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class LiftProfile:
    name: str
    raw_support: int
    normalized_trace_hits: int
    quotient_support: int
    block_constancy_hits: int
    kernel_mode_support: tuple[int, ...]
    nontrivial_kernel_modes: int
    selected_block_mode_counts: tuple[int, ...]
    ok: bool


def square_axis_case() -> PullbackCase:
    for case in PULLBACK_CASES:
        if case.name == "square_axis_C3xC169":
            return case
    raise AssertionError("square-axis case missing")


def selected_qs() -> tuple[int, ...]:
    return tuple(
        sorted(
            q_from_coord(right, c_coord)
            for _s_value, _h_value, _t_value, right, c_coord in selected_terms()
        )
    )


def make_lift(
    case: PullbackCase,
    selected: tuple[int, ...],
    modulus: int,
    kind: str,
    zeta25: int,
) -> list[int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    raw = [0] * case.raw_order
    selected_set = set(selected)
    for q_value in range(quotient_order):
        if q_value not in selected_set:
            continue
        for layer in range(case.b_trace):
            index = q_value + quotient_order * layer
            if kind == "block":
                raw[index] = 1
            elif kind == "sparse_section":
                raw[index] = case.b_trace if layer == 0 else 0
            elif kind == "block_plus_hidden_mode":
                raw[index] = (1 + pow(zeta25, layer, modulus)) % modulus
            elif kind == "hidden_mode_only":
                raw[index] = pow(zeta25, layer, modulus)
            else:
                raise AssertionError(f"unknown lift kind: {kind}")
    return raw


def normalized_trace(
    raw: list[int],
    case: PullbackCase,
    modulus: int,
) -> list[int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    inv_b = pow(case.b_trace, -1, modulus)
    out = []
    for q_value in range(quotient_order):
        total = sum(raw[q_value + quotient_order * layer] for layer in range(case.b_trace))
        out.append(total * inv_b % modulus)
    return out


def block_constant_count(raw: list[int], case: PullbackCase) -> int:
    quotient_order = RIGHT_DEGREE * case.c_axis
    hits = 0
    for q_value in range(quotient_order):
        values = {
            raw[q_value + quotient_order * layer]
            for layer in range(case.b_trace)
        }
        hits += int(len(values) == 1)
    return hits


def kernel_mode_support(
    raw: list[int],
    case: PullbackCase,
    modulus: int,
    zeta25: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    supported_modes: set[int] = set()
    selected_mode_counts = [0 for _ in range(case.b_trace)]
    for mode in range(case.b_trace):
        for q_value in range(quotient_order):
            total = 0
            for layer in range(case.b_trace):
                # Negative exponent convention for the per-block Fourier coefficient.
                total += raw[q_value + quotient_order * layer] * pow(
                    zeta25,
                    (-mode * layer) % case.b_trace,
                    modulus,
                )
            if total % modulus:
                supported_modes.add(mode)
                selected_mode_counts[mode] += 1
    return tuple(sorted(supported_modes)), tuple(selected_mode_counts)


def profile_lift(
    name: str,
    raw: list[int],
    case: PullbackCase,
    selected: tuple[int, ...],
    modulus: int,
    zeta25: int,
    expected_modes: tuple[int, ...],
    expected_trace_hits: int,
    expected_block_hits: int,
    expected_raw_support: int,
) -> LiftProfile:
    quotient_order = RIGHT_DEGREE * case.c_axis
    selected_set = set(selected)
    expected_trace = [int(q_value in selected_set) for q_value in range(quotient_order)]
    trace = normalized_trace(raw, case, modulus)
    normalized_trace_hits = sum(
        int(value == target % modulus) for value, target in zip(trace, expected_trace)
    )
    quotient_support = sum(int(value % modulus != 0) for value in trace)
    raw_support = sum(int(value % modulus != 0) for value in raw)
    block_constancy_hits = block_constant_count(raw, case)
    modes, mode_counts = kernel_mode_support(raw, case, modulus, zeta25)
    row_ok = (
        raw_support == expected_raw_support
        and normalized_trace_hits == expected_trace_hits
        and block_constancy_hits == expected_block_hits
        and quotient_support == (len(selected) if expected_trace_hits == quotient_order else 0)
        and modes == expected_modes
    )
    return LiftProfile(
        name=name,
        raw_support=raw_support,
        normalized_trace_hits=normalized_trace_hits,
        quotient_support=quotient_support,
        block_constancy_hits=block_constancy_hits,
        kernel_mode_support=modes,
        nontrivial_kernel_modes=sum(1 for mode in modes if mode != 0),
        selected_block_mode_counts=mode_counts,
        ok=row_ok,
    )


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    selected = selected_qs()
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta25 = pow(root, (modulus - 1) // case.b_trace, modulus)

    print("p25 Lane B square-axis trace-projection lift gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={quotient_order} "
        f"B={case.b_trace} selected_qs={len(selected)} modulus={modulus}"
    )

    full_modes = tuple(range(case.b_trace))
    lifts = [
        profile_lift(
            "block_constant_kernel_trivial",
            make_lift(case, selected, modulus, "block", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_modes=(0,),
            expected_trace_hits=quotient_order,
            expected_block_hits=quotient_order,
            expected_raw_support=len(selected) * case.b_trace,
        ),
        profile_lift(
            "sparse_section_trace_correct",
            make_lift(case, selected, modulus, "sparse_section", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_modes=full_modes,
            expected_trace_hits=quotient_order,
            expected_block_hits=quotient_order - len(selected),
            expected_raw_support=len(selected),
        ),
        profile_lift(
            "block_plus_hidden_kernel_mode",
            make_lift(case, selected, modulus, "block_plus_hidden_mode", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_modes=(0, 1),
            expected_trace_hits=quotient_order,
            expected_block_hits=quotient_order - len(selected),
            expected_raw_support=len(selected) * case.b_trace,
        ),
        profile_lift(
            "hidden_kernel_mode_only",
            make_lift(case, selected, modulus, "hidden_mode_only", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_modes=(1,),
            expected_trace_hits=quotient_order - len(selected),
            expected_block_hits=quotient_order - len(selected),
            expected_raw_support=len(selected) * case.b_trace,
        ),
    ]

    ok_rows = 0
    for lift in lifts:
        ok_rows += int(lift.ok)
        print(
            f"lift {lift.name}: "
            f"raw_support={lift.raw_support} "
            f"normalized_trace_hits={lift.normalized_trace_hits}/{quotient_order} "
            f"quotient_support={lift.quotient_support}/{len(selected)} "
            f"block_constancy_hits={lift.block_constancy_hits}/{quotient_order} "
            f"kernel_mode_support={list(lift.kernel_mode_support)} "
            f"nontrivial_kernel_modes={lift.nontrivial_kernel_modes} "
            f"mode_counts_first={list(lift.selected_block_mode_counts[:6])} "
            f"mode_counts_last={list(lift.selected_block_mode_counts[-3:])} "
            f"ok={int(lift.ok)}"
        )

    block = lifts[0]
    sparse = lifts[1]
    hidden = lifts[2]
    hidden_only = lifts[3]
    distinction_ok = (
        block.normalized_trace_hits == sparse.normalized_trace_hits == hidden.normalized_trace_hits == quotient_order
        and hidden_only.normalized_trace_hits == quotient_order - len(selected)
        and block.block_constancy_hits == quotient_order
        and sparse.block_constancy_hits == hidden.block_constancy_hits == hidden_only.block_constancy_hits == quotient_order - len(selected)
        and block.kernel_mode_support == (0,)
        and sparse.kernel_mode_support == full_modes
        and hidden.kernel_mode_support == (0, 1)
        and hidden_only.kernel_mode_support == (1,)
    )
    row_ok = ok_rows == len(lifts) and distinction_ok
    print(
        "projection_summary: "
        f"trace_correct_lifts=3/4 "
        f"kernel_trivial_trace_correct_lifts=1/3 "
        f"sparse_trace_correct_but_not_block_constant=1 "
        f"hidden_modes_do_not_change_trace=1 "
        f"distinction_ok={int(distinction_ok)}"
    )
    print(f"square_axis_trace_projection_lift_rows={int(row_ok)}/1")
    print("interpretation")
    print("  quotient_trace_correctness_does_not_force_block_constancy=1")
    print("  sparse_18_point_raw_lift_has_full_C25_kernel_support=1")
    print("  block_constant_450_point_lift_is_exactly_kernel_trivial=1")
    print("  producer_harness_intentionally_requires_kernel_trivial_block_lift=1")
    print("conclusion=reported_p25_laneB_square_axis_trace_projection_lift_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
