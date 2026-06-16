#!/usr/bin/env python3
"""Raw quotient-relation lift gate for the p25 square-axis residual.

The quotient normal form has the relation D^3 = Y.  On the raw C_12675 source
cycle, D^3 and Y differ by one C_25 kernel layer.  Therefore this relation is
true on raw values exactly for kernel-trivial/block-constant lifts.

This gate compares trace-correct lifts from the trace-projection checkpoint.
The sparse 18-point section and the block lift plus a hidden kernel mode both
trace to the same quotient residual as the canonical block lift, but they fail
the raw D^3 = Y relation.  This turns the quotient relation into a concrete
producer falsifier.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_trace_projection_lift_gate import (
    block_constant_count,
    kernel_mode_support,
    make_lift,
    normalized_trace,
    selected_qs,
    square_axis_case,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class RelationProfile:
    name: str
    trace_correct: bool
    block_constant: bool
    kernel_modes: tuple[int, ...]
    relation_hits: int
    relation_mismatches: int
    mismatch_q_count: int
    mismatch_per_q_values: tuple[int, ...]
    ok: bool


def relation_profile(
    name: str,
    raw: list[int],
    case,
    selected: tuple[int, ...],
    modulus: int,
    zeta25: int,
    expected_relation_hits: int,
    expected_mismatch_q_count: int,
    expected_mismatch_per_q_values: tuple[int, ...],
    expected_trace_correct: bool,
    expected_block_constant: bool,
    expected_kernel_modes: tuple[int, ...],
) -> RelationProfile:
    quotient_order = RIGHT_DEGREE * case.c_axis
    selected_set = set(selected)
    expected_trace = [int(q_value in selected_set) for q_value in range(quotient_order)]
    trace = normalized_trace(raw, case, modulus)
    trace_correct = all(value == target % modulus for value, target in zip(trace, expected_trace))
    block_constant = block_constant_count(raw, case) == quotient_order
    kernel_modes, _mode_counts = kernel_mode_support(raw, case, modulus, zeta25)

    relation_hits = 0
    mismatch_by_q: dict[int, int] = {}
    for e_value in range(case.raw_order):
        d3_value = raw[(e_value + 3 * S_STEP) % case.raw_order]
        y_value = raw[(e_value + Y_STEP) % case.raw_order]
        if d3_value == y_value:
            relation_hits += 1
        else:
            q_value = e_value % quotient_order
            mismatch_by_q[q_value] = mismatch_by_q.get(q_value, 0) + 1
    relation_mismatches = case.raw_order - relation_hits
    mismatch_per_q_values = tuple(sorted(set(mismatch_by_q.values())))
    row_ok = (
        trace_correct == expected_trace_correct
        and block_constant == expected_block_constant
        and kernel_modes == expected_kernel_modes
        and relation_hits == expected_relation_hits
        and len(mismatch_by_q) == expected_mismatch_q_count
        and mismatch_per_q_values == expected_mismatch_per_q_values
    )
    return RelationProfile(
        name=name,
        trace_correct=trace_correct,
        block_constant=block_constant,
        kernel_modes=kernel_modes,
        relation_hits=relation_hits,
        relation_mismatches=relation_mismatches,
        mismatch_q_count=len(mismatch_by_q),
        mismatch_per_q_values=mismatch_per_q_values,
        ok=row_ok,
    )


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    selected = selected_qs()
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta25 = pow(root, (modulus - 1) // case.b_trace, modulus)
    full_modes = tuple(range(case.b_trace))

    print("p25 Lane B square-axis raw quotient-relation gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={quotient_order} "
        f"B={case.b_trace} selected_qs={len(selected)} modulus={modulus}"
    )

    profiles = [
        relation_profile(
            "block_constant_kernel_trivial",
            make_lift(case, selected, modulus, "block", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_relation_hits=case.raw_order,
            expected_mismatch_q_count=0,
            expected_mismatch_per_q_values=(),
            expected_trace_correct=True,
            expected_block_constant=True,
            expected_kernel_modes=(0,),
        ),
        relation_profile(
            "sparse_section_trace_correct",
            make_lift(case, selected, modulus, "sparse_section", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_relation_hits=case.raw_order - 2 * len(selected),
            expected_mismatch_q_count=len(selected),
            expected_mismatch_per_q_values=(2,),
            expected_trace_correct=True,
            expected_block_constant=False,
            expected_kernel_modes=full_modes,
        ),
        relation_profile(
            "block_plus_hidden_kernel_mode",
            make_lift(case, selected, modulus, "block_plus_hidden_mode", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_relation_hits=case.raw_order - case.b_trace * len(selected),
            expected_mismatch_q_count=len(selected),
            expected_mismatch_per_q_values=(case.b_trace,),
            expected_trace_correct=True,
            expected_block_constant=False,
            expected_kernel_modes=(0, 1),
        ),
        relation_profile(
            "hidden_kernel_mode_only",
            make_lift(case, selected, modulus, "hidden_mode_only", zeta25),
            case,
            selected,
            modulus,
            zeta25,
            expected_relation_hits=case.raw_order - case.b_trace * len(selected),
            expected_mismatch_q_count=len(selected),
            expected_mismatch_per_q_values=(case.b_trace,),
            expected_trace_correct=False,
            expected_block_constant=False,
            expected_kernel_modes=(1,),
        ),
    ]

    ok_rows = 0
    for profile in profiles:
        ok_rows += int(profile.ok)
        print(
            f"lift {profile.name}: "
            f"trace_correct={int(profile.trace_correct)} "
            f"block_constant={int(profile.block_constant)} "
            f"kernel_modes={list(profile.kernel_modes)} "
            f"D3_equals_Y_hits={profile.relation_hits}/{case.raw_order} "
            f"mismatches={profile.relation_mismatches} "
            f"mismatch_q_count={profile.mismatch_q_count} "
            f"mismatch_per_q_values={list(profile.mismatch_per_q_values)} "
            f"ok={int(profile.ok)}"
        )

    trace_correct_profiles = [profile for profile in profiles if profile.trace_correct]
    trace_correct_relation_profiles = [
        profile
        for profile in trace_correct_profiles
        if profile.relation_hits == case.raw_order
    ]
    row_ok = (
        ok_rows == len(profiles)
        and len(trace_correct_profiles) == 3
        and len(trace_correct_relation_profiles) == 1
        and trace_correct_relation_profiles[0].name == "block_constant_kernel_trivial"
    )
    print(
        "relation_summary: "
        f"trace_correct_lifts={len(trace_correct_profiles)}/4 "
        f"trace_correct_and_raw_D3_equals_Y={len(trace_correct_relation_profiles)}/3 "
        f"only_block_constant_lift_satisfies_raw_relation={int(row_ok)}"
    )
    print(f"square_axis_raw_quotient_relation_rows={int(row_ok)}/1")
    print("interpretation")
    print("  quotient_trace_correctness_does_not_force_raw_D_cubed_equals_Y=1")
    print("  raw_D_cubed_equals_Y_selects_the_kernel_trivial_block_lift=1")
    print("  sparse_trace_correct_sections_break_the_raw_quotient_relation=1")
    print("  hidden_trace_zero_kernel_modes_break_the_raw_quotient_relation=1")
    print("conclusion=reported_p25_laneB_square_axis_raw_quotient_relation_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
