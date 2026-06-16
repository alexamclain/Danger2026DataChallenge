#!/usr/bin/env python3
"""Sparse endpoint intake for McCarthy/Barnes p25 candidates.

The current live target is not a broad hypergeometric value table.  After
q-power projection and coefficient transport it is the pointwise unit

    U(q) = 1 + (zeta_39^5 - 1) * e_138(q)

on `C_507` over `F_2029`, or equivalently the normalized projector `e_138`.
This harness lets a theorem, hand calculation, or literature scout emit sparse
`q coeff` pairs for either endpoint shape:

* `--sparse-projector`: coefficients of the normalized projector.
* `--sparse-unit-minus-one`: coefficients of `U - 1`.

It is an intake/falsifier artifact.  Passing it only means the endpoint object
has the exact finite shape that the existing raw-Y transport gate already
verified; it does not prove the theorem that produced the endpoint.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_boundary_residual_gate import SQUARE_C
from p25_laneB_square_axis_mccarthy_idempotent_unit_gate import (
    dft_support_count,
    pointwise_mul,
    pointwise_order,
    support_count,
)
from p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate import (
    mccarthy_power_transport_raw_y_profile,
)
from p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate import TARGET_Q_EXP
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


SparseEndpointEntry = tuple[int, int]


@dataclass(frozen=True)
class McCarthyEndpointCandidateProfile:
    name: str
    mode: str
    input_terms: int
    active_terms: int
    duplicate_terms: int
    modulus: int
    quotient_order: int
    target_q_exp: int
    zeta39_5_minus_one: int
    zeta39_5_minus_one_inverse: int
    projector_support: int
    projector_target_coefficient: int
    projector_is_idempotent: bool
    projector_exact: bool
    unit_minus_one_support: int
    unit_minus_one_target_coefficient: int
    unit_minus_one_exact: bool
    unit_order: int
    projector_fourier_support: int
    unit_minus_one_fourier_support: int
    raw_y_transport_closes: bool
    ok: bool


def parse_sparse_endpoint(path: Path) -> tuple[SparseEndpointEntry, ...]:
    entries: list[SparseEndpointEntry] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        clean = line.split("#", 1)[0]
        for char in ",()[]":
            clean = clean.replace(char, " ")
        if not clean.strip():
            continue
        parts = clean.split()
        if len(parts) != 2:
            raise ValueError(f"{path}:{line_number} expected two integers: q coeff")
        entries.append((int(parts[0]), int(parts[1])))
    return tuple(entries)


def sparse_endpoint_to_vector(
    entries: tuple[SparseEndpointEntry, ...],
    modulus: int,
) -> tuple[list[int], int, int]:
    coefficients: dict[int, int] = {}
    duplicate_terms = 0
    for q_exp, coefficient in entries:
        q_key = q_exp % QUOTIENT_ORDER
        duplicate_terms += int(q_key in coefficients)
        coefficients[q_key] = (coefficients.get(q_key, 0) + coefficient) % modulus

    vector = [0] * QUOTIENT_ORDER
    active_terms = 0
    for q_exp, coefficient in coefficients.items():
        if coefficient == 0:
            continue
        active_terms += 1
        vector[q_exp] = coefficient
    return vector, active_terms, duplicate_terms


def target_projector_entries() -> tuple[SparseEndpointEntry, ...]:
    return ((TARGET_Q_EXP, 1),)


def target_unit_minus_one_entries() -> tuple[SparseEndpointEntry, ...]:
    transport = mccarthy_power_transport_raw_y_profile()
    return ((TARGET_Q_EXP, transport.transported_minus_one),)


def safe_pointwise_order(vector: list[int], modulus: int, limit: int) -> int:
    try:
        return pointwise_order(vector, modulus, limit)
    except AssertionError:
        return 0


def profile_endpoint_candidate(
    name: str,
    mode: str,
    entries: tuple[SparseEndpointEntry, ...],
) -> McCarthyEndpointCandidateProfile:
    transport = mccarthy_power_transport_raw_y_profile()
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    vector, active_terms, duplicate_terms = sparse_endpoint_to_vector(entries, modulus)

    if mode == "projector":
        projector = vector
        unit_minus_one = [
            value * transport.transported_minus_one % modulus for value in projector
        ]
    elif mode == "unit_minus_one":
        unit_minus_one = vector
        projector = [
            value * transport.transported_minus_one_inverse % modulus
            for value in unit_minus_one
        ]
    else:
        raise ValueError(f"unknown endpoint candidate mode: {mode}")

    point = [0] * QUOTIENT_ORDER
    point[TARGET_Q_EXP] = 1
    target_unit_minus_one = [0] * QUOTIENT_ORDER
    target_unit_minus_one[TARGET_Q_EXP] = transport.transported_minus_one
    unit = [(1 + value) % modulus for value in unit_minus_one]

    projector_exact = projector == point
    unit_minus_one_exact = unit_minus_one == target_unit_minus_one
    raw_y_transport_closes = (
        projector_exact
        and unit_minus_one_exact
        and transport.normalized_attempt.quotient_packet_exact
        and transport.normalized_attempt.raw_y_nonzero == 6300
        and transport.normalized_attempt.ray_local_harness_ok
    )
    unit_order = safe_pointwise_order(unit, modulus, 39)
    ok = (
        active_terms == 1
        and duplicate_terms == 0
        and projector_exact
        and unit_minus_one_exact
        and pointwise_mul(projector, projector, modulus) == projector
        and unit_order == 39
        and raw_y_transport_closes
    )

    return McCarthyEndpointCandidateProfile(
        name=name,
        mode=mode,
        input_terms=len(entries),
        active_terms=active_terms,
        duplicate_terms=duplicate_terms,
        modulus=modulus,
        quotient_order=QUOTIENT_ORDER,
        target_q_exp=TARGET_Q_EXP,
        zeta39_5_minus_one=transport.transported_minus_one,
        zeta39_5_minus_one_inverse=transport.transported_minus_one_inverse,
        projector_support=support_count(projector),
        projector_target_coefficient=projector[TARGET_Q_EXP],
        projector_is_idempotent=pointwise_mul(projector, projector, modulus)
        == projector,
        projector_exact=projector_exact,
        unit_minus_one_support=support_count(unit_minus_one),
        unit_minus_one_target_coefficient=unit_minus_one[TARGET_Q_EXP],
        unit_minus_one_exact=unit_minus_one_exact,
        unit_order=unit_order,
        projector_fourier_support=dft_support_count(projector, modulus),
        unit_minus_one_fourier_support=dft_support_count(unit_minus_one, modulus),
        raw_y_transport_closes=raw_y_transport_closes,
        ok=ok,
    )


def print_candidate(profile: McCarthyEndpointCandidateProfile, candidate_mode: bool) -> None:
    print(f"endpoint_candidate_profile={profile}")
    print("endpoint_contract")
    print("  sparse input is coalesced on C_507")
    print("  normalized endpoint must be exactly e_138")
    print("  unit endpoint must be exactly 1_plus_zeta39_5_minus_1_times_e_138")
    print("  accepted endpoint inherits the existing normalized raw-Y transport closure")
    if candidate_mode:
        print(f"square_axis_mccarthy_endpoint_candidate_harness_candidate_rows={int(profile.ok)}/1")


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Audit sparse q-coefficient endpoints against the p25 McCarthy "
            "projector/unit target on C_507."
        )
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--sparse-projector",
        type=Path,
        help="optional text file of q coeff pairs for the normalized projector",
    )
    group.add_argument(
        "--sparse-unit-minus-one",
        type=Path,
        help="optional text file of q coeff pairs for U - 1",
    )
    args = parser.parse_args()

    print("p25 Lane B McCarthy endpoint candidate intake harness")
    print("endpoint_group=C_507 coefficient_field=F_2029 format='q coeff'")

    if args.sparse_projector is not None:
        profile = profile_endpoint_candidate(
            str(args.sparse_projector),
            "projector",
            parse_sparse_endpoint(args.sparse_projector),
        )
        print("mode=sparse_projector_candidate")
        print_candidate(profile, candidate_mode=True)
        print("conclusion=reported_p25_laneB_square_axis_mccarthy_endpoint_candidate")
        return 0 if profile.ok else 1

    if args.sparse_unit_minus_one is not None:
        profile = profile_endpoint_candidate(
            str(args.sparse_unit_minus_one),
            "unit_minus_one",
            parse_sparse_endpoint(args.sparse_unit_minus_one),
        )
        print("mode=sparse_unit_minus_one_candidate")
        print_candidate(profile, candidate_mode=True)
        print("conclusion=reported_p25_laneB_square_axis_mccarthy_endpoint_candidate")
        return 0 if profile.ok else 1

    projector_profile = profile_endpoint_candidate(
        "target_projector_roundtrip",
        "projector",
        target_projector_entries(),
    )
    unit_profile = profile_endpoint_candidate(
        "target_unit_minus_one_roundtrip",
        "unit_minus_one",
        target_unit_minus_one_entries(),
    )
    row_ok = projector_profile.ok and unit_profile.ok
    print(f"target_projector_profile={projector_profile}")
    print(f"target_unit_minus_one_profile={unit_profile}")
    print("intake_law")
    print("  theorem_hits_can_emit_only_sparse_q_coefficients")
    print("  projector_and_unit_minus_one_forms_are_equivalent_after_canonical_scaling")
    print("  accepted_endpoint_roundtrips_to_the_existing_raw-Y_passing_payload")
    print(f"square_axis_mccarthy_endpoint_candidate_harness_rows={int(row_ok)}/1")
    print("interpretation")
    print("  next_lit_search_hit_can_be_tested_at_the_C_507_endpoint_layer=1")
    print("  passing_this_harness_is_not_an_arithmetic_producer_proof=1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_endpoint_candidate_harness")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
