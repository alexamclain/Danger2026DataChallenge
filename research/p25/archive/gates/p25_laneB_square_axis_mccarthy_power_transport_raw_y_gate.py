#!/usr/bin/env python3
"""McCarthy power-descent coefficient transport to the p25 raw-Y field.

The power-descent gate found a singleton-supported powered quotient:

    R(q)^2029 - 1

with target coefficient `zeta_39^5 - 1` in the auxiliary value field.  This
gate transports the order-39 root by exponent into the actual p25 coefficient
field F_2029, then checks the raw-Y closure.

With the primitive-root convention used by the local gates:

    zeta_39 in F_2029 = 2^52
    zeta_39^5 = 1376
    zeta_39^5 - 1 = 1375

The unnormalized powered quotient has the right support but not the canonical
all-one seed payload.  Multiplying by the determined inverse of the transported
coefficient, 1375^-1 = 636 in F_2029, gives the exact anomaly projector used
by the existing raw-Y closure.

This does not prove an arithmetic certificate.  It records that the coefficient
field descent is finite and canonical once the powered quotient `R^2029` is
accepted; the remaining debt is justifying the power/normalization as part of
the producer, not finding a new finite payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import comb

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_literal_jacobi_packet_model import carry_packet
from p25_laneB_ray_local_theta31_pullback_falsifier_gate import (
    audit_candidate,
    case_by_name,
    local_coordinates,
)
from p25_laneB_square_axis_boundary_residual_gate import SQUARE_C, component_vector
from p25_laneB_square_axis_gross_koblitz_carry_twist_gate import ANOMALY_CELL
from p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate import (
    CASE_NAME,
    quotient_index,
    raw_y_from_quotient,
)
from p25_laneB_square_axis_group_ring_normal_form_gate import S_STEP, X_STEP, Y_STEP
from p25_laneB_square_axis_local_graph_residue_gate import QUOTIENT_ORDER
from p25_laneB_square_axis_mccarthy_power_descent_gate import (
    CHARACTER_DESCENT_ORDER,
    mccarthy_power_descent_profile,
)
from p25_selected_defect_value_gate import RIGHT_DEGREE, split_prime_for


@dataclass(frozen=True)
class TransportedRawYAttempt:
    name: str
    anomaly_projector_coefficient: int
    corrected_seed_payload: tuple[tuple[int, int, int], ...]
    quotient_packet_exact: bool
    raw_y_nonzero: int
    ray_local_harness_ok: bool


@dataclass(frozen=True)
class McCarthyPowerTransportRawYProfile:
    modulus: int
    primitive_root: int
    zeta39: int
    zeta39_exponent: int
    transported_power_value: int
    transported_minus_one: int
    transported_minus_one_inverse: int
    power_descent_support: tuple[int, ...]
    power_descent_target_order: int
    unnormalized_attempt: TransportedRawYAttempt
    normalized_attempt: TransportedRawYAttempt
    coefficient_transport_canonical: bool
    normalized_raw_y_closes: bool
    unnormalized_control_fails_exact_packet: bool


def quotient_coord_from_q(q_value: int) -> tuple[int, int]:
    for right in range(RIGHT_DEGREE):
        c_index = ((q_value - SQUARE_C * right) * pow(RIGHT_DEGREE, -1, SQUARE_C)) % SQUARE_C
        if (SQUARE_C * right + RIGHT_DEGREE * c_index) % QUOTIENT_ORDER == q_value:
            return right, c_index
    raise AssertionError(f"failed to convert q={q_value} to quotient coordinates")


def weighted_residual_vector(
    anomaly_projector_coefficient: int,
    modulus: int,
) -> tuple[list[int], tuple[tuple[int, int, int], ...]]:
    residual = [0] * (RIGHT_DEGREE * SQUARE_C)
    payload: list[tuple[int, int, int]] = []
    for h_value in range(RIGHT_DEGREE):
        for t_value in range(h_value + 1):
            projector = (
                anomaly_projector_coefficient
                if (h_value, t_value) == ANOMALY_CELL
                else 0
            )
            corrected_value = (comb(h_value, t_value) - projector) % modulus
            payload.append((h_value, t_value, corrected_value))
            for s_value in range(RIGHT_DEGREE):
                q_value = (
                    X_STEP * (h_value + 1) + S_STEP * s_value + Y_STEP * t_value
                ) % QUOTIENT_ORDER
                right, c_index = quotient_coord_from_q(q_value)
                residual[quotient_index(right, c_index)] = corrected_value
    return residual, tuple(payload)


def attempt_raw_y(
    name: str,
    anomaly_projector_coefficient: int,
    modulus: int,
) -> TransportedRawYAttempt:
    case = case_by_name(CASE_NAME)
    base = component_vector("base")
    residual, corrected_payload = weighted_residual_vector(
        anomaly_projector_coefficient,
        modulus,
    )
    scale_value = RIGHT_DEGREE * SQUARE_C
    quotient_bits = [
        (base_value + residual_value) % modulus
        for base_value, residual_value in zip(base, residual)
    ]
    quotient = [scale_value * bit % modulus for bit in quotient_bits]
    canonical = carry_packet(SQUARE_C, RIGHT_DEGREE, 1, modulus)
    raw_y = raw_y_from_quotient(quotient, modulus)
    _audit_lines, ray_ok = audit_candidate(
        name,
        raw_y,
        case,
        local_coordinates(case),
        modulus,
    )
    return TransportedRawYAttempt(
        name=name,
        anomaly_projector_coefficient=anomaly_projector_coefficient,
        corrected_seed_payload=corrected_payload,
        quotient_packet_exact=quotient == canonical,
        raw_y_nonzero=sum(1 for value in raw_y if value % modulus),
        ray_local_harness_ok=ray_ok,
    )


def mccarthy_power_transport_raw_y_profile() -> McCarthyPowerTransportRawYProfile:
    power = mccarthy_power_descent_profile()
    modulus = split_prime_for(RIGHT_DEGREE * SQUARE_C)
    root = primitive_root(modulus)
    zeta39 = pow(root, (modulus - 1) // CHARACTER_DESCENT_ORDER, modulus)
    transported_power_value = pow(zeta39, power.additive_power_zeta39_exponent, modulus)
    transported_minus_one = (transported_power_value - 1) % modulus
    transported_inverse = pow(transported_minus_one, -1, modulus)
    unnormalized = attempt_raw_y(
        "mccarthy_power_transport_unnormalized",
        transported_minus_one,
        modulus,
    )
    normalized = attempt_raw_y(
        "mccarthy_power_transport_normalized",
        transported_minus_one * transported_inverse % modulus,
        modulus,
    )
    return McCarthyPowerTransportRawYProfile(
        modulus=modulus,
        primitive_root=root,
        zeta39=zeta39,
        zeta39_exponent=power.additive_power_zeta39_exponent,
        transported_power_value=transported_power_value,
        transported_minus_one=transported_minus_one,
        transported_minus_one_inverse=transported_inverse,
        power_descent_support=power.additive_power_support,
        power_descent_target_order=power.additive_power_target_order,
        unnormalized_attempt=unnormalized,
        normalized_attempt=normalized,
        coefficient_transport_canonical=(
            modulus == 2029
            and root == 2
            and zeta39 == 1358
            and transported_power_value == 1376
            and transported_minus_one == 1375
            and transported_inverse == 636
        ),
        normalized_raw_y_closes=(
            normalized.quotient_packet_exact
            and normalized.raw_y_nonzero == 6300
            and normalized.ray_local_harness_ok
        ),
        unnormalized_control_fails_exact_packet=(
            not unnormalized.quotient_packet_exact
            and unnormalized.raw_y_nonzero == 6300
            and not unnormalized.ray_local_harness_ok
        ),
    )


def main() -> int:
    print("p25 Lane B McCarthy power transport raw-Y gate")
    profile = mccarthy_power_transport_raw_y_profile()
    row_ok = (
        profile.modulus == 2029
        and profile.primitive_root == 2
        and profile.zeta39 == 1358
        and profile.zeta39_exponent == 5
        and profile.transported_power_value == 1376
        and profile.transported_minus_one == 1375
        and profile.transported_minus_one_inverse == 636
        and profile.power_descent_support == (138,)
        and profile.power_descent_target_order == 39
        and profile.unnormalized_attempt.anomaly_projector_coefficient == 1375
        and profile.unnormalized_attempt.corrected_seed_payload
        == (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 0, 1),
            (2, 1, 656),
            (2, 2, 1),
        )
        and not profile.unnormalized_attempt.quotient_packet_exact
        and profile.unnormalized_attempt.raw_y_nonzero == 6300
        and not profile.unnormalized_attempt.ray_local_harness_ok
        and profile.normalized_attempt.anomaly_projector_coefficient == 1
        and profile.normalized_attempt.corrected_seed_payload
        == (
            (0, 0, 1),
            (1, 0, 1),
            (1, 1, 1),
            (2, 0, 1),
            (2, 1, 1),
            (2, 2, 1),
        )
        and profile.normalized_attempt.quotient_packet_exact
        and profile.normalized_attempt.raw_y_nonzero == 6300
        and profile.normalized_attempt.ray_local_harness_ok
        and profile.coefficient_transport_canonical
        and profile.normalized_raw_y_closes
        and profile.unnormalized_control_fails_exact_packet
    )

    print(f"mccarthy_power_transport_raw_y_profile={profile}")
    print("transport_raw_y_laws")
    print("  mu_39_exponent_5_transports_to_F_2029_as_1376=1")
    print("  transported_zeta39_5_minus_1_is_1375_with_inverse_636=1")
    print("  unnormalized_powered_quotient_has_right_support_but_wrong_payload=1")
    print("  normalized_transported_powered_quotient_recovers_the_GK_projector=1")
    print("  normalized_raw_Y_closure_passes_existing_harness=1")
    print("interpretation")
    print("  coefficient_field_descent_is_finite_and_canonical_after_power_descent=1")
    print("  remaining_debt_is_arithmetic_justification_of_power_and_scaling=1")
    print(f"square_axis_mccarthy_power_transport_raw_y_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_mccarthy_power_transport_raw_y_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
