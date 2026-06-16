#!/usr/bin/env python3
"""Formal raw-Y control from the p25 Gross-Koblitz Frobenius projector.

The Frobenius-projector gate repairs the six-term Lucas/binomial seed at the
quotient level.  This gate checks the next finite obligation: if an arithmetic
HD/GK/Barnes unit phase realizes that projector, then no further finite
correction is needed to satisfy the square-axis theta_{3,1} raw-Y harness.

It builds the C_3 x C_169 quotient packet as

    507 * (C13 fiber background + S*(binom(h,t) - projector(h,t))).

The second term is exactly the 18-point boundary residual.  The resulting
quotient packet equals the canonical theta_{3,1} carry packet, and the
kernel-trivial raw lift passes the existing ray-local producer harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

from p25_laneB_literal_jacobi_packet_model import carry_packet
from p25_laneB_ray_local_theta31_pullback_falsifier_gate import (
    audit_candidate,
    case_by_name,
    local_coordinates,
)
from p25_laneB_square_axis_boundary_residual_gate import (
    BASE_C,
    SQUARE_C,
    component_vector,
)
from p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate import (
    frobenius_projector_profile,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import (
    S_STEP,
    X_STEP,
    Y_STEP,
    residual_q_values,
)
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


CASE_NAME = "square_axis_C3xC169"


@dataclass(frozen=True)
class ProjectorRawYProfile:
    modulus: int
    scale_value: int
    base_support: int
    residual_support: int
    quotient_support: int
    corrected_seed_payload: tuple[tuple[int, int, int], ...]
    residual_terms: tuple[int, ...]
    quotient_packet_exact: bool
    raw_y_length: int
    raw_y_nonzero: int
    ray_local_harness_ok: bool


def quotient_index(right: int, c_index: int) -> int:
    return right * SQUARE_C + c_index


def quotient_coord_from_q(q_value: int) -> tuple[int, int]:
    for right in range(RIGHT_DEGREE):
        c_index = ((q_value - SQUARE_C * right) * pow(RIGHT_DEGREE, -1, SQUARE_C)) % SQUARE_C
        if (SQUARE_C * right + RIGHT_DEGREE * c_index) % QUOTIENT_ORDER == q_value:
            return right, c_index
    raise AssertionError(f"failed to convert q={q_value} to quotient coordinates")


def projector_by_cell() -> dict[tuple[int, int], int]:
    profile = frobenius_projector_profile()
    return {
        (cell.h_value, cell.t_value): cell.quotient_projector
        for cell in profile.cells
        if cell.selected
    }


def corrected_residual_vector() -> tuple[list[int], tuple[tuple[int, int, int], ...]]:
    projector = projector_by_cell()
    residual = [0] * (RIGHT_DEGREE * SQUARE_C)
    payload: list[tuple[int, int, int]] = []
    for h_value in range(RIGHT_DEGREE):
        for t_value in range(h_value + 1):
            corrected_value = comb(h_value, t_value) - projector[(h_value, t_value)]
            payload.append((h_value, t_value, corrected_value))
            for s_value in range(RIGHT_DEGREE):
                q_value = (
                    X_STEP * (h_value + 1) + S_STEP * s_value + Y_STEP * t_value
                ) % QUOTIENT_ORDER
                right, c_index = quotient_coord_from_q(q_value)
                residual[quotient_index(right, c_index)] = corrected_value
    return residual, tuple(payload)


def raw_y_from_quotient(quotient: list[int], modulus: int) -> list[int]:
    case = case_by_name(CASE_NAME)
    coordinates = local_coordinates(case)
    inv_b = pow(case.b_trace % modulus, -1, modulus)
    return [
        quotient[quotient_index(right, c_index)] * inv_b % modulus
        for right, c_index in coordinates
    ]


def projector_raw_y_profile() -> ProjectorRawYProfile:
    case = case_by_name(CASE_NAME)
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    scale_value = RIGHT_DEGREE * SQUARE_C
    base = component_vector("base")
    residual, corrected_payload = corrected_residual_vector()
    quotient_bits = [base_value + residual_value for base_value, residual_value in zip(base, residual)]
    quotient = [scale_value * bit % modulus for bit in quotient_bits]
    canonical = carry_packet(SQUARE_C, RIGHT_DEGREE, 1, modulus)
    raw_y = raw_y_from_quotient(quotient, modulus)
    _audit_lines, ray_ok = audit_candidate(
        "formal_gk_projector_raw_y",
        raw_y,
        case,
        local_coordinates(case),
        modulus,
    )
    return ProjectorRawYProfile(
        modulus=modulus,
        scale_value=scale_value,
        base_support=sum(1 for value in base if value),
        residual_support=sum(1 for value in residual if value),
        quotient_support=sum(1 for value in quotient_bits if value),
        corrected_seed_payload=corrected_payload,
        residual_terms=tuple(sorted(residual_q_values())),
        quotient_packet_exact=quotient == canonical,
        raw_y_length=len(raw_y),
        raw_y_nonzero=sum(1 for value in raw_y if value % modulus),
        ray_local_harness_ok=ray_ok,
    )


def main() -> int:
    print("p25 Lane B square-axis Gross-Koblitz projector raw-Y gate")
    profile = projector_raw_y_profile()
    row_ok = (
        profile.modulus == 2029
        and profile.scale_value == 507
        and profile.base_support == 234
        and profile.residual_support == 18
        and profile.quotient_support == 252
        and profile.corrected_seed_payload
        == (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 0, 1),
            (2, 1, 1),
            (2, 2, 1),
        )
        and profile.residual_terms
        == (
            43,
            86,
            95,
            129,
            138,
            147,
            215,
            258,
            267,
            301,
            310,
            319,
            387,
            430,
            439,
            473,
            482,
            491,
        )
        and profile.quotient_packet_exact
        and profile.raw_y_length == 12675
        and profile.raw_y_nonzero == 6300
        and profile.ray_local_harness_ok
    )

    print(f"projector_raw_y_profile={profile}")
    print("projector_raw_y_laws")
    print("  quotient = 507*(C13_background + S*(binom-projector))")
    print("  quotient equals the canonical square-axis theta_3_1 carry packet")
    print("  kernel-trivial raw-Y lift passes the existing ray-local harness")
    print("interpretation")
    print("  formal_gk_projector_closes_the_finite_theta31_payload_gap=1")
    print("  remaining_gap_is_arithmetic_realization_of_the_projector_unit_phase=1")
    print(f"square_axis_gross_koblitz_projector_raw_y_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
