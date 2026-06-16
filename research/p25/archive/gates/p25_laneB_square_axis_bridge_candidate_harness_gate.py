#!/usr/bin/env python3
"""Producer-facing bridge candidate harness for the p25 square-axis lane.

The recent bridge gates identify the finite object a successful local
producer must realize:

    S * X * Y^-2 * (1 - X^2 * Y^3)

on the C_3 x C_169 quotient, with the kernel-trivial raw lift on C_12675.
This gate packages that as a small candidate audit.  It compares the real
block bridge against three tempting shortcuts:

* a trace-correct sparse C_25 section,
* the positive D segment without the inversion partner,
* a separated right-trace-times-C axis hull.

Only the kernel-trivial bridge passes the full producer contract.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_square_axis_bridge_axis_hull_character_gap_gate import (
    support_profile,
)
from p25_laneB_square_axis_bridge_factorization_gate import bridge_coefficients
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    C_ORDER,
    MODULUS,
    RIGHT_ORDER,
    raw_source_mask,
)
from p25_laneB_square_axis_bridge_raw_source_gate import (
    kernel_mode_support,
    normalized_trace,
    raw_bridge_lift,
    square_axis_case,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER, RAW_ORDER
from p25_laneB_square_axis_quotient_shift_normal_form_gate import coord_from_q


@dataclass(frozen=True)
class CandidateProfile:
    name: str
    raw_support: int
    quotient_support: int
    trace_correct: bool
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    target_raw_exact: bool
    source_mask_exact: bool
    quotient_scalar_nonzero: int
    quotient_pure_c_nonzero: int
    quotient_mixed_nonzero: int
    ok: bool


def mod_value(value: int) -> int:
    return value % MODULUS


def signed_mod(value: int) -> int:
    value %= MODULUS
    if value > MODULUS // 2:
        return value - MODULUS
    return value


def crt_source_to_raw(right_log: int, c_log: int) -> int:
    """Return e with e = right_log mod 75 and e = c_log mod 169."""

    inverse_75 = pow(RIGHT_ORDER, -1, C_ORDER)
    lift = ((c_log - right_log) * inverse_75) % C_ORDER
    return (right_log + RIGHT_ORDER * lift) % RAW_ORDER


def target_raw_bridge() -> list[int]:
    case = square_axis_case()
    return [signed_mod(value) for value in raw_bridge_lift(case, MODULUS)]


def sparse_trace_section() -> list[int]:
    case = square_axis_case()
    raw = [0] * case.raw_order
    for q_value, coefficient in bridge_coefficients().items():
        raw[q_value] = signed_mod(coefficient * case.b_trace)
    return raw


def positive_only_bridge() -> list[int]:
    target = target_raw_bridge()
    return [value if value > 0 else 0 for value in target]


def axis_hull_bridge() -> list[int]:
    mask = raw_source_mask()
    positive_c_values = sorted({c_log for (_right, c_log), value in mask.items() if value > 0})
    negative_c_values = sorted({c_log for (_right, c_log), value in mask.items() if value < 0})
    raw = [0] * RAW_ORDER
    for right_log in range(RIGHT_ORDER):
        for c_log in positive_c_values:
            raw[crt_source_to_raw(right_log, c_log)] = 1
        for c_log in negative_c_values:
            raw[crt_source_to_raw(right_log, c_log)] = -1
    return raw


def parse_raw_candidate(path: Path) -> list[int]:
    values = [int(token) for token in re.findall(r"-?\d+", path.read_text())]
    if len(values) != RAW_ORDER:
        raise ValueError(f"{path} contains {len(values)} integers, expected {RAW_ORDER}")
    return values


def block_constancy_hits(raw: list[int]) -> int:
    hits = 0
    for q_value in range(QUOTIENT_ORDER):
        values = {
            mod_value(raw[q_value + QUOTIENT_ORDER * layer])
            for layer in range(25)
        }
        hits += int(len(values) == 1)
    return hits


def raw_relation_mismatches(raw: list[int]) -> int:
    mismatches = 0
    for e_value in range(RAW_ORDER):
        if mod_value(raw[(e_value + 3 * S_STEP) % RAW_ORDER]) != mod_value(
            raw[(e_value + Y_STEP) % RAW_ORDER]
        ):
            mismatches += 1
    return mismatches


def quotient_trace(raw: list[int]) -> list[int]:
    case = square_axis_case()
    return [signed_mod(value) for value in normalized_trace([mod_value(v) for v in raw], case, MODULUS)]


def trace_correct(trace: list[int]) -> bool:
    expected = [bridge_coefficients().get(q_value, 0) for q_value in range(QUOTIENT_ORDER)]
    return all(mod_value(value) == mod_value(target) for value, target in zip(trace, expected))


def quotient_mask(trace: list[int]) -> dict[tuple[int, int], int]:
    out: dict[tuple[int, int], int] = {}
    for q_value, value in enumerate(trace):
        if mod_value(value):
            out[coord_from_q(q_value)] = signed_mod(value)
    return out


def source_mask(raw: list[int]) -> dict[tuple[int, int], int]:
    out: dict[tuple[int, int], int] = {}
    for e_value, value in enumerate(raw):
        if mod_value(value):
            out[(e_value % RIGHT_ORDER, e_value % C_ORDER)] = signed_mod(value)
    return dict(sorted(out.items()))


def profile_candidate(name: str, raw: list[int], target: list[int]) -> CandidateProfile:
    case = square_axis_case()
    root = primitive_root(MODULUS)
    zeta25 = pow(root, (MODULUS - 1) // case.b_trace, MODULUS)
    raw_mod = [mod_value(value) for value in raw]
    target_mod = [mod_value(value) for value in target]
    trace = quotient_trace(raw)
    q_mask = quotient_mask(trace)
    q_profile = support_profile(f"{name}_quotient_trace", q_mask)
    kernel_modes, _mode_counts = kernel_mode_support(raw_mod, case, MODULUS, zeta25)
    exact_raw = raw_mod == target_mod
    exact_source = source_mask(raw) == raw_source_mask()
    block_hits = block_constancy_hits(raw)
    relation_mismatches = raw_relation_mismatches(raw)
    trace_ok = trace_correct(trace)
    raw_support = sum(1 for value in raw_mod if value)
    quotient_support = len(q_mask)
    ok = (
        raw_support == 150
        and quotient_support == 6
        and trace_ok
        and block_hits == QUOTIENT_ORDER
        and kernel_modes == (0,)
        and relation_mismatches == 0
        and exact_raw
        and exact_source
        and q_profile.scalar_nonzero == 0
        and q_profile.pure_c_nonzero == C_ORDER - 1
        and q_profile.mixed_nonzero == 2 * (C_ORDER - 1)
    )
    return CandidateProfile(
        name=name,
        raw_support=raw_support,
        quotient_support=quotient_support,
        trace_correct=trace_ok,
        block_constancy_hits=block_hits,
        kernel_modes=kernel_modes,
        raw_relation_mismatches=relation_mismatches,
        target_raw_exact=exact_raw,
        source_mask_exact=exact_source,
        quotient_scalar_nonzero=q_profile.scalar_nonzero,
        quotient_pure_c_nonzero=q_profile.pure_c_nonzero,
        quotient_mixed_nonzero=q_profile.mixed_nonzero,
        ok=ok,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit a p25 square-axis bridge raw candidate."
    )
    parser.add_argument(
        "--raw-candidate",
        type=Path,
        help="optional raw vector with length 12675 to check against the bridge contract",
    )
    args = parser.parse_args()

    print("p25 Lane B square-axis bridge candidate-harness gate")
    print(
        f"raw_order={RAW_ORDER} quotient_order={QUOTIENT_ORDER} "
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} modulus={MODULUS}"
    )
    target = target_raw_bridge()
    if args.raw_candidate is not None:
        profile = profile_candidate(str(args.raw_candidate), parse_raw_candidate(args.raw_candidate), target)
        print("mode=raw_candidate")
        print(f"candidate_profile={profile}")
        print("candidate_contract")
        print("  pass requires: exact signed quotient trace, kernel-trivial block lift, raw D^3=Y relation")
        print("  pass requires: exact C_75 x C_169 source graph and full mixed quotient character payload")
        print(f"square_axis_bridge_candidate_harness_raw_candidate_rows={int(profile.ok)}/1")
        print("conclusion=reported_p25_laneB_square_axis_bridge_candidate_harness_raw_candidate")
        return 0 if profile.ok else 1

    profiles = (
        profile_candidate("kernel_trivial_block_bridge", target, target),
        profile_candidate("trace_correct_sparse_section", sparse_trace_section(), target),
        profile_candidate("positive_D_segment_only", positive_only_bridge(), target),
        profile_candidate("separated_axis_hull_bridge", axis_hull_bridge(), target),
    )

    by_name = {profile.name: profile for profile in profiles}
    row_ok = (
        by_name["kernel_trivial_block_bridge"].ok
        and by_name["trace_correct_sparse_section"].trace_correct
        and by_name["trace_correct_sparse_section"].block_constancy_hits < QUOTIENT_ORDER
        and by_name["trace_correct_sparse_section"].kernel_modes == tuple(range(25))
        and by_name["trace_correct_sparse_section"].raw_relation_mismatches > 0
        and not by_name["trace_correct_sparse_section"].ok
        and not by_name["positive_D_segment_only"].trace_correct
        and by_name["positive_D_segment_only"].quotient_support == 3
        and by_name["positive_D_segment_only"].kernel_modes == (0,)
        and not by_name["positive_D_segment_only"].ok
        and not by_name["separated_axis_hull_bridge"].trace_correct
        and by_name["separated_axis_hull_bridge"].raw_support == 450
        and by_name["separated_axis_hull_bridge"].kernel_modes == (0,)
        and by_name["separated_axis_hull_bridge"].quotient_mixed_nonzero == 0
        and not by_name["separated_axis_hull_bridge"].ok
    )

    print("candidate_profiles")
    for profile in profiles:
        print(f"  {profile}")
    print("candidate_contract")
    print("  pass requires: exact signed quotient trace, kernel-trivial block lift, raw D^3=Y relation")
    print("  pass requires: exact C_75 x C_169 source graph and full mixed quotient character payload")
    print("shortcut_falsifiers")
    print("  sparse section: trace-correct, but exposes all 25 kernel modes and breaks raw D^3=Y")
    print("  positive segment: kernel-trivial, but omits the inversion partner and fails the signed bridge trace")
    print("  axis hull: kernel-trivial, but overproduces support and has no mixed right/C quotient characters")
    print("interpretation")
    print("  bridge_candidate_harness_accepts_only_the_kernel_trivial_anti_invariant_bridge=1")
    print("  trace_correctness_alone_is_not_a_producer_certificate=1")
    print("  separated_axis_hulls_are_valid_kernel_traces_but_not_valid_bridge_producers=1")
    print("  future_modular_unit_or_CM_candidates_can_be_audited_against_this_finite_contract=1")
    print(f"square_axis_bridge_candidate_harness_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_candidate_harness_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
