#!/usr/bin/env python3
"""Raw/source lift gate for the square-axis bridge.

The bridge-factorization gate identifies the quotient correction

    S * X * Y^-2 * (1 - X^2 * Y^3).

This gate lifts that signed bridge to the actual square-axis local source
cycle.  The producer-facing facts are:

* the bridge has the unique kernel-trivial raw lift with 150 nonzero positions,
  six quotient classes times B=25 raw representatives;
* each quotient class is one mod677 C-source singleton times one 25-element
  mod151 right-source coset;
* the bridge step X^2Y^3=113 is a fixed local source multiplier on every
  kernel layer: 45 in mod151 and 667 in mod677.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import (
    CASES as PULLBACK_CASES,
    P25,
    PullbackCase,
    precompute_source_logs,
    quotient_coordinates,
    quotient_exponent,
)
from p25_laneB_square_axis_bridge_factorization_gate import (
    BRIDGE_STEP,
    bridge_coefficients,
    partner_anomaly_pairs,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    RAW_ORDER,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class RawClassProfile:
    q_value: int
    coefficient: int
    right: int
    c_coord: int
    raw_support: int
    right_residue_count: int
    c_residue_count: int
    right_log_mod3_values: tuple[int, ...]
    c_log_values: tuple[int, ...]


@dataclass(frozen=True)
class BridgeMultiplierProfile:
    partner_q: int
    anomaly_q: int
    same_layer_hits: int
    right_multiplier_values: tuple[int, ...]
    c_multiplier_values: tuple[int, ...]


def square_axis_case() -> PullbackCase:
    for case in PULLBACK_CASES:
        if case.name == "square_axis_C3xC169":
            return case
    raise AssertionError("missing square-axis case")


def raw_bridge_lift(case: PullbackCase, modulus: int) -> list[int]:
    raw = [0] * case.raw_order
    for q_value, coefficient in bridge_coefficients().items():
        for layer in range(case.b_trace):
            raw[q_value + QUOTIENT_ORDER * layer] = coefficient % modulus
    return raw


def normalized_trace(raw: list[int], case: PullbackCase, modulus: int) -> list[int]:
    inv_b = pow(case.b_trace, -1, modulus)
    out: list[int] = []
    for q_value in range(QUOTIENT_ORDER):
        total = sum(raw[q_value + QUOTIENT_ORDER * layer] for layer in range(case.b_trace))
        out.append(total * inv_b % modulus)
    return out


def block_constancy_hits(raw: list[int], case: PullbackCase) -> int:
    hits = 0
    for q_value in range(QUOTIENT_ORDER):
        values = {
            raw[q_value + QUOTIENT_ORDER * layer]
            for layer in range(case.b_trace)
        }
        hits += int(len(values) == 1)
    return hits


def kernel_mode_support(
    raw: list[int],
    case: PullbackCase,
    modulus: int,
    zeta_b: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    supported_modes: set[int] = set()
    mode_counts = [0 for _ in range(case.b_trace)]
    for mode in range(case.b_trace):
        for q_value in range(QUOTIENT_ORDER):
            total = 0
            for layer in range(case.b_trace):
                total += raw[q_value + QUOTIENT_ORDER * layer] * pow(
                    zeta_b,
                    (-mode * layer) % case.b_trace,
                    modulus,
                )
            if total % modulus:
                supported_modes.add(mode)
                mode_counts[mode] += 1
    return tuple(sorted(supported_modes)), tuple(mode_counts)


def source_generators(case: PullbackCase) -> tuple[int, int]:
    right_source = case.right_sources[0]
    c_source = case.c_source
    return (
        pow(P25, case.rho_exp, right_source.modulus),
        pow(P25, case.rho_exp, c_source.modulus),
    )


def raw_class_profiles(case: PullbackCase) -> tuple[RawClassProfile, ...]:
    source_logs = precompute_source_logs(case)
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    rows: list[RawClassProfile] = []
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]
    for q_value, coefficient in bridge_coefficients().items():
        exponents = [q_value + QUOTIENT_ORDER * layer for layer in range(case.b_trace)]
        right_residues = {
            pow(right_generator, exponent, right_source.modulus)
            for exponent in exponents
        }
        c_residues = {
            pow(c_generator, exponent, c_source.modulus)
            for exponent in exponents
        }
        right_logs = tuple(
            sorted({(exponent % right_source.expected_order) % RIGHT_DEGREE for exponent in exponents})
        )
        c_logs = tuple(
            sorted({exponent % c_source.expected_order for exponent in exponents})
        )
        right, c_coord = coordinates[q_value]
        rows.append(
            RawClassProfile(
                q_value=q_value,
                coefficient=coefficient,
                right=right,
                c_coord=c_coord,
                raw_support=len(exponents),
                right_residue_count=len(right_residues),
                c_residue_count=len(c_residues),
                right_log_mod3_values=right_logs,
                c_log_values=c_logs,
            )
        )
    return tuple(rows)


def bridge_multiplier_profiles(case: PullbackCase) -> tuple[BridgeMultiplierProfile, ...]:
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_generator, c_generator = source_generators(case)
    rows: list[BridgeMultiplierProfile] = []
    for pair in partner_anomaly_pairs():
        right_multipliers: set[int] = set()
        c_multipliers: set[int] = set()
        same_layer_hits = 0
        for layer in range(case.b_trace):
            partner_e = pair.partner_q + QUOTIENT_ORDER * layer
            anomaly_e = pair.anomaly_q + QUOTIENT_ORDER * layer
            same_layer_hits += int(anomaly_e - partner_e == BRIDGE_STEP)
            partner_right = pow(right_generator, partner_e, right_source.modulus)
            anomaly_right = pow(right_generator, anomaly_e, right_source.modulus)
            partner_c = pow(c_generator, partner_e, c_source.modulus)
            anomaly_c = pow(c_generator, anomaly_e, c_source.modulus)
            right_multipliers.add(
                anomaly_right * pow(partner_right, -1, right_source.modulus)
                % right_source.modulus
            )
            c_multipliers.add(
                anomaly_c * pow(partner_c, -1, c_source.modulus)
                % c_source.modulus
            )
        rows.append(
            BridgeMultiplierProfile(
                partner_q=pair.partner_q,
                anomaly_q=pair.anomaly_q,
                same_layer_hits=same_layer_hits,
                right_multiplier_values=tuple(sorted(right_multipliers)),
                c_multiplier_values=tuple(sorted(c_multipliers)),
            )
        )
    return tuple(rows)


def main() -> int:
    case = square_axis_case()
    modulus = split_prime_for(case.raw_order)
    root = primitive_root(modulus)
    zeta_b = pow(root, (modulus - 1) // case.b_trace, modulus)
    raw = raw_bridge_lift(case, modulus)
    trace = normalized_trace(raw, case, modulus)
    coefficients = bridge_coefficients()
    expected_trace = [
        coefficients.get(q_value, 0) % modulus
        for q_value in range(QUOTIENT_ORDER)
    ]
    trace_hits = sum(int(value == target) for value, target in zip(trace, expected_trace))
    raw_support = sum(1 for value in raw if value % modulus)
    block_hits = block_constancy_hits(raw, case)
    modes, mode_counts = kernel_mode_support(raw, case, modulus, zeta_b)
    source_logs = precompute_source_logs(case)
    coordinates = [
        quotient_coordinates(case, source_logs, e_value)
        for e_value in range(case.raw_order)
    ]
    coordinate_hits = sum(
        int(quotient_exponent(case, *coord) == e_value % QUOTIENT_ORDER)
        for e_value, coord in enumerate(coordinates)
    )
    class_profiles = raw_class_profiles(case)
    multiplier_profiles = bridge_multiplier_profiles(case)
    right_generator, c_generator = source_generators(case)
    right_source = case.right_sources[0]
    c_source = case.c_source
    right_step_multiplier = pow(right_generator, BRIDGE_STEP, right_source.modulus)
    c_step_multiplier = pow(c_generator, BRIDGE_STEP, c_source.modulus)

    expected_c_logs = {
        25: (25,),
        138: (138,),
        197: (28,),
        310: (141,),
        369: (31,),
        482: (144,),
    }
    class_rows_ok = sum(
        int(
            row.raw_support == case.b_trace
            and row.right_residue_count == case.b_trace
            and row.c_residue_count == 1
            and row.right_log_mod3_values == (row.right,)
            and row.c_log_values == expected_c_logs[row.q_value]
        )
        for row in class_profiles
    )
    multiplier_rows_ok = sum(
        int(
            row.same_layer_hits == case.b_trace
            and row.right_multiplier_values == (right_step_multiplier,)
            and row.c_multiplier_values == (c_step_multiplier,)
        )
        for row in multiplier_profiles
    )

    row_ok = (
        case.raw_order == RAW_ORDER
        and case.b_trace == 25
        and coordinate_hits == case.raw_order
        and raw_support == len(coefficients) * case.b_trace == 150
        and trace_hits == QUOTIENT_ORDER
        and block_hits == QUOTIENT_ORDER
        and modes == (0,)
        and mode_counts[0] == len(coefficients)
        and sum(mode_counts[1:]) == 0
        and right_step_multiplier == 45
        and c_step_multiplier == 667
        and BRIDGE_STEP % right_source.expected_order == 38
        and BRIDGE_STEP % c_source.expected_order == 113
        and class_rows_ok == len(coefficients)
        and multiplier_rows_ok == len(multiplier_profiles) == 3
    )

    print("p25 Lane B square-axis bridge raw-source gate")
    print(
        f"case={case.name} raw_order={case.raw_order} quotient_order={QUOTIENT_ORDER} "
        f"B={case.b_trace} modulus={modulus}"
    )
    print(
        "raw_bridge_lift: "
        f"raw_support={raw_support}/150 "
        f"trace_hits={trace_hits}/{QUOTIENT_ORDER} "
        f"block_constancy_hits={block_hits}/{QUOTIENT_ORDER} "
        f"kernel_mode_support={list(modes)} "
        f"mode_counts_first={list(mode_counts[:6])} "
        f"coordinate_hits={coordinate_hits}/{case.raw_order}"
    )
    print(
        "source_step: "
        f"bridge_step={BRIDGE_STEP} "
        f"right_step_mod_order={BRIDGE_STEP % right_source.expected_order} "
        f"c_step_mod_order={BRIDGE_STEP % c_source.expected_order} "
        f"right_multiplier={right_step_multiplier} "
        f"c_multiplier={c_step_multiplier}"
    )
    print("raw_classes")
    for row in class_profiles:
        print(f"  {row}")
    print("bridge_multipliers")
    for row in multiplier_profiles:
        print(f"  {row}")
    print("interpretation")
    print("  bridge_has_unique_kernel_trivial_150_point_raw_lift=1")
    print("  each_bridge_class_is_one_mod677_singleton_times_one_mod151_coset=1")
    print("  X2Y3_bridge_step_is_a_fixed_source_multiplier_on_every_kernel_layer=1")
    print("  producer_must_realize_this_raw_source_edge_not_a_sparse_trace_section=1")
    print(f"square_axis_bridge_raw_source_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_raw_source_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
