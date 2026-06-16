#!/usr/bin/env python3
"""Scalar-balance escape hatch for the p25 Lane B anomaly orbit.

The anomaly-orbit balance gate rules out repairing the q-binomial coefficient
error with one more small S-orbit.  There is, however, one quotient-level way
to make the correction degree zero: add a scalar background.

For the anomaly orbit O = S*X^3Y, the scalar-balanced representative is

    -1_O + (3/507) * 1_{C_507}.

This gate records that this escape hatch is unique modulo scalars and is
highly nonlocal: it has support on every quotient class and every raw block.
Thus a producer may use the scalar component, but then it must account for a
dense kernel-trivial background rather than a small local orbit patch.
"""

from __future__ import annotations

from collections import Counter

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_anomaly_orbit_balance_gate import anomaly_orbit
from p25_laneB_square_axis_relation_kernel_equivalence_gate import relation_holds
from p25_laneB_square_axis_trace_projection_lift_gate import (
    block_constant_count,
    kernel_mode_support,
    normalized_trace,
    square_axis_case,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_selected_defect_value_gate import split_prime_for


def scalar_balanced_vector(modulus: int) -> list[int]:
    orbit = set(anomaly_orbit())
    alpha = 3 * pow(QUOTIENT_ORDER, -1, modulus) % modulus
    return [
        (alpha - int(q_value in orbit)) % modulus
        for q_value in range(QUOTIENT_ORDER)
    ]


def vector_degree(vector: list[int], modulus: int) -> int:
    return sum(vector) % modulus


def weighted_dft_zeros(vector: list[int], modulus: int) -> tuple[int, ...]:
    root = primitive_root(modulus)
    zeta = pow(root, (modulus - 1) // len(vector), modulus)
    zeros: list[int] = []
    for frequency in range(len(vector)):
        total = sum(
            value * pow(zeta, frequency * index, modulus)
            for index, value in enumerate(vector)
        ) % modulus
        if total == 0:
            zeros.append(frequency)
    return tuple(zeros)


def block_lift(quotient: list[int], case) -> list[int]:
    raw = [0] * case.raw_order
    quotient_order = len(quotient)
    for q_value, value in enumerate(quotient):
        for layer in range(case.b_trace):
            raw[q_value + quotient_order * layer] = value
    return raw


def remove_scalar(vector: list[int], modulus: int) -> list[int]:
    alpha = 3 * pow(QUOTIENT_ORDER, -1, modulus) % modulus
    return [(value - alpha) % modulus for value in vector]


def main() -> int:
    case = square_axis_case()
    modulus = split_prime_for(case.raw_order)
    quotient = scalar_balanced_vector(modulus)
    orbit = anomaly_orbit()
    alpha = 3 * pow(QUOTIENT_ORDER, -1, modulus) % modulus
    inside_value = (alpha - 1) % modulus
    outside_value = alpha
    value_counts = Counter(quotient)
    support = sum(int(value != 0) for value in quotient)
    zeros = weighted_dft_zeros(quotient, modulus)
    scalar_removed = remove_scalar(quotient, modulus)
    scalar_removed_support = [index for index, value in enumerate(scalar_removed) if value]
    scalar_removed_values = sorted(set(scalar_removed))

    raw = block_lift(quotient, case)
    trace = normalized_trace(raw, case, modulus)
    trace_hits = sum(int(left == right) for left, right in zip(trace, quotient))
    raw_support = sum(int(value != 0) for value in raw)
    raw_degree = vector_degree(raw, modulus)
    block_hits = block_constant_count(raw, case)
    root = primitive_root(modulus)
    zeta25 = pow(root, (modulus - 1) // case.b_trace, modulus)
    modes, mode_counts = kernel_mode_support(raw, case, modulus, zeta25)
    relation_offset = QUOTIENT_ORDER

    row_ok = (
        modulus == 126751
        and alpha == 126001
        and inside_value == 126000
        and outside_value == 126001
        and dict(value_counts) == {inside_value: 3, outside_value: 504}
        and support == QUOTIENT_ORDER
        and vector_degree(quotient, modulus) == 0
        and zeros == (0, 169, 338)
        and scalar_removed_support == orbit
        and scalar_removed_values == [0, modulus - 1]
        and raw_support == case.raw_order
        and raw_degree == 0
        and trace_hits == QUOTIENT_ORDER
        and block_hits == QUOTIENT_ORDER
        and modes == (0,)
        and mode_counts[0] == QUOTIENT_ORDER
        and relation_holds(raw, relation_offset)
    )
    print("p25 Lane B square-axis scalar-balance escape gate")
    print(
        f"quotient_order={QUOTIENT_ORDER} modulus={modulus} "
        f"case={case.name} raw_order={case.raw_order} B={case.b_trace}"
    )
    print(
        "scalar_balance: "
        f"alpha=3/507={alpha} "
        f"inside_value={inside_value} "
        f"outside_value={outside_value} "
        f"value_counts={dict(sorted(value_counts.items()))} "
        f"quotient_support={support}/{QUOTIENT_ORDER} "
        f"quotient_degree={vector_degree(quotient, modulus)} "
        f"weighted_fourier_zeros={list(zeros)} "
        f"scalar_removed_support={scalar_removed_support} "
        f"ok={int(row_ok)}"
    )
    print(
        "raw_block_lift: "
        f"raw_support={raw_support}/{case.raw_order} "
        f"raw_degree={raw_degree} "
        f"trace_hits={trace_hits}/{QUOTIENT_ORDER} "
        f"block_constancy_hits={block_hits}/{QUOTIENT_ORDER} "
        f"kernel_modes={list(modes)} "
        f"mode0_count={mode_counts[0]} "
        f"relation_holds={int(relation_holds(raw, relation_offset))}"
    )
    print("interpretation")
    print("  scalar_balance_repairs_degree_but_is_dense_on_C507=1")
    print("  removing_the_scalar_recovers_exactly_the_anomaly_orbit=1")
    print("  raw_lift_is_kernel_trivial_but_dense_on_all_12675_positions=1")
    print("  producer_using_q_binomial_support_must_account_for_dense_scalar_background=1")
    print("conclusion=reported_p25_laneB_square_axis_scalar_balance_escape_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
