#!/usr/bin/env python3
"""Raw relation/kernel-trivial equivalence for the p25 square-axis lift.

The raw quotient-relation gate tests several concrete lifts.  This gate proves
the underlying finite linear algebra:

    D^3 = Y on raw values

is exactly invariance under the 507-step trace kernel, because

    3*172 - 9 = 507.

Thus the raw relation cuts the C_12675 function space down to the
kernel-trivial/block-constant subspace of dimension 507.  On that subspace the
normalized B-trace to C_3 x C_169 is an isomorphism, so any quotient payload has
a unique raw lift satisfying the raw relation.  For the square-axis residual,
that unique lift is the 450-point block lift.
"""

from __future__ import annotations

from collections import Counter

from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_trace_projection_lift_gate import (
    make_lift,
    normalized_trace,
    selected_qs,
    square_axis_case,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


def relation_holds(raw: list[int], step: int) -> bool:
    size = len(raw)
    return all(raw[(index + step) % size] == raw[index] for index in range(size))


def cycle_lengths(size: int, step: int) -> list[int]:
    seen = [False] * size
    lengths: list[int] = []
    for start in range(size):
        if seen[start]:
            continue
        current = start
        length = 0
        while not seen[current]:
            seen[current] = True
            length += 1
            current = (current + step) % size
        lengths.append(length)
    return sorted(lengths)


def quotient_block_lift(case, quotient: list[int]) -> list[int]:
    quotient_order = RIGHT_DEGREE * case.c_axis
    raw = [0] * case.raw_order
    for q_value, value in enumerate(quotient):
        for layer in range(case.b_trace):
            raw[q_value + quotient_order * layer] = value
    return raw


def main() -> int:
    case = square_axis_case()
    quotient_order = RIGHT_DEGREE * case.c_axis
    relation_offset = (3 * S_STEP - Y_STEP) % case.raw_order
    modulus = split_prime_for(case.raw_order)
    selected = selected_qs()
    selected_set = set(selected)
    quotient_residual = [
        int(q_value in selected_set) for q_value in range(quotient_order)
    ]
    unique_block = quotient_block_lift(case, quotient_residual)
    trace = normalized_trace(unique_block, case, modulus)
    trace_matches = sum(
        int(value == target % modulus)
        for value, target in zip(trace, quotient_residual)
    )

    lengths = cycle_lengths(case.raw_order, relation_offset)
    length_counts = Counter(lengths)
    relation_rank = case.raw_order - len(lengths)
    relation_nullity = len(lengths)
    trace_rank = quotient_order
    trace_kernel_dimension = case.raw_order - quotient_order

    raw_relation_equals_kernel_step = relation_offset == quotient_order
    cycle_structure_ok = (
        len(lengths) == quotient_order
        and set(lengths) == {case.b_trace}
        and length_counts[case.b_trace] == quotient_order
    )
    dimension_ok = (
        relation_nullity == quotient_order
        and relation_rank == trace_kernel_dimension
        and trace_rank == relation_nullity
    )
    unique_block_ok = (
        relation_holds(unique_block, relation_offset)
        and trace_matches == quotient_order
        and sum(1 for value in unique_block if value) == len(selected) * case.b_trace
    )

    # A period-507 lift is determined by its normalized trace: averaging over
    # each 25-cycle returns the same value.  Check this on a deterministic,
    # non-binary quotient payload so the assertion is not special to masks.
    sample_quotient = [
        (17 * q_value * q_value + 5 * q_value + 3) % modulus
        for q_value in range(quotient_order)
    ]
    sample_block = quotient_block_lift(case, sample_quotient)
    sample_trace = normalized_trace(sample_block, case, modulus)
    sample_isomorphism_hits = sum(
        int(value == target)
        for value, target in zip(sample_trace, sample_quotient)
    )

    row_ok = (
        raw_relation_equals_kernel_step
        and cycle_structure_ok
        and dimension_ok
        and unique_block_ok
        and sample_isomorphism_hits == quotient_order
    )

    print("p25 Lane B square-axis relation/kernel equivalence gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={quotient_order} "
        f"B={case.b_trace} modulus={modulus}"
    )
    print(
        "relation_offset: "
        f"3*S_STEP-Y_STEP={relation_offset} "
        f"equals_quotient_order={int(raw_relation_equals_kernel_step)}"
    )
    print(
        "cycle_structure: "
        f"cycle_count={len(lengths)} "
        f"length_counts={dict(sorted(length_counts.items()))} "
        f"ok={int(cycle_structure_ok)}"
    )
    print(
        "linear_dimensions: "
        f"relation_rank={relation_rank} "
        f"relation_nullity={relation_nullity} "
        f"trace_rank={trace_rank} "
        f"trace_kernel_dimension={trace_kernel_dimension} "
        f"ok={int(dimension_ok)}"
    )
    print(
        "residual_unique_block_lift: "
        f"trace_matches={trace_matches}/{quotient_order} "
        f"raw_support={sum(1 for value in unique_block if value)}/{len(selected) * case.b_trace} "
        f"relation_holds={int(relation_holds(unique_block, relation_offset))} "
        f"ok={int(unique_block_ok)}"
    )
    print(
        "trace_restricted_to_relation_space: "
        f"sample_isomorphism_hits={sample_isomorphism_hits}/{quotient_order} "
        f"ok={int(sample_isomorphism_hits == quotient_order)}"
    )
    print(f"square_axis_relation_kernel_equivalence_rows={int(row_ok)}/1")
    print("interpretation")
    print("  raw_D_cubed_equals_Y_is_exactly_507_step_kernel_invariance=1")
    print("  relation_space_is_the_kernel_trivial_block_constant_subspace=1")
    print("  normalized_trace_is_an_isomorphism_on_the_relation_space=1")
    print("  quotient_residual_has_a_unique_raw_relation_satisfying_lift=1")
    print("conclusion=reported_p25_laneB_square_axis_relation_kernel_equivalence_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
