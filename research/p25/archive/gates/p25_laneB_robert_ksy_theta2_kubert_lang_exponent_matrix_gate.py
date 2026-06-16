#!/usr/bin/env python3
"""Kubert-Lang exponent-matrix precheck for the p25 KSY theta2 target.

Kubert-Lang Siegel-unit products satisfy elementary congruence conditions on
the exponent matrix: the exponent sum is 0 modulo 12, and the three quadratic
sums vanish modulo the level.  This gate applies those necessary tests to the
current p25 finite payloads.

Passing this gate is not an arithmetic producer.  It says the exact packet and
theta2 footprint survive the first Siegel-unit exponent-matrix screen; the
remaining issue is finding a theorem-legal mixed-level lift/product that emits
the payload.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from math import prod

from p25_laneB_robert_ksy_theta2_normalized_y_product_gate import (
    normalized_y_product_footprint,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)


Coord = tuple[int, int]
Ring = dict[Coord, int]

QUOTIENT_RIGHT_ORDER = 3
QUOTIENT_LEVEL = QUOTIENT_RIGHT_ORDER * C_ORDER
RAW_LEVEL = RIGHT_ORDER * C_ORDER


@dataclass(frozen=True)
class KLExponentMatrixProfile:
    name: str
    level: int
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum: int
    exponent_sum_mod_12: int
    quadratic_right: int
    quadratic_c: int
    quadratic_mixed: int
    quadratic_relations_ok: bool
    level_prime_power_away_from_2_3: bool
    preserves_right_data: bool
    preserves_t_edge: bool
    p25_finite_payload_ok: bool
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class KLExponentMatrixScreenProfile:
    source_packet_profile: KLExponentMatrixProfile
    theta2_inverse_profile: KLExponentMatrixProfile
    theta2_profile: KLExponentMatrixProfile
    c_axis_projection_profile: KLExponentMatrixProfile
    truncated_d_rejected: bool
    wrong_d_rejected: bool
    wrong_t_rejected: bool
    positive_only_rejected: bool
    exact_payloads_survive_congruence_screen: bool
    prime_power_projection_is_finite_insufficient: bool
    next_debt: str
    row_ok: bool


def add_quotient(left: Coord, right: Coord) -> Coord:
    return ((left[0] + right[0]) % QUOTIENT_RIGHT_ORDER, (left[1] + right[1]) % C_ORDER)


def scale_quotient(step: Coord, scale: int) -> Coord:
    return ((step[0] * scale) % QUOTIENT_RIGHT_ORDER, (step[1] * scale) % C_ORDER)


def add_packet_entry(packet: Ring, coord: Coord, coefficient: int) -> None:
    packet[coord] = packet.get(coord, 0) + coefficient
    if packet[coord] == 0:
        del packet[coord]


def source_packet(
    base: Coord = (1, 25),
    d_step: Coord = (1, 3),
    t_step: Coord = (2, 113),
    d_length: int = 3,
) -> Ring:
    packet: Ring = {}
    for index in range(d_length):
        positive = add_quotient(base, scale_quotient(d_step, index))
        negative = add_quotient(positive, t_step)
        add_packet_entry(packet, positive, 1)
        add_packet_entry(packet, negative, -1)
    return dict(sorted(packet.items()))


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def is_prime_power_away_from_2_3(level: int) -> bool:
    value = level
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return len(factors) == 1 and factors[0] not in (2, 3) and prod(factors) > 1


def kl_profile(
    name: str,
    ring: Ring,
    level: int,
    right_scale: int,
    c_scale: int,
    preserves_right_data: bool,
    preserves_t_edge: bool,
    p25_finite_payload_ok: bool,
    recommendation: str,
) -> KLExponentMatrixProfile:
    exponent_sum = sum(ring.values())
    quadratic_right = sum(
        coefficient * ((coord[0] * right_scale) % level) ** 2
        for coord, coefficient in ring.items()
    ) % level
    quadratic_c = sum(
        coefficient * ((coord[1] * c_scale) % level) ** 2
        for coord, coefficient in ring.items()
    ) % level
    quadratic_mixed = sum(
        coefficient
        * ((coord[0] * right_scale) % level)
        * ((coord[1] * c_scale) % level)
        for coord, coefficient in ring.items()
    ) % level
    quadratic_ok = (
        exponent_sum % 12 == 0
        and quadratic_right == 0
        and quadratic_c == 0
        and quadratic_mixed == 0
    )
    level_ok = is_prime_power_away_from_2_3(level)
    row_ok = (
        quadratic_ok
        and p25_finite_payload_ok
        and (preserves_right_data or level_ok)
    )
    return KLExponentMatrixProfile(
        name=name,
        level=level,
        support=len(ring),
        coefficient_counts=coefficient_counts(ring),
        exponent_sum=exponent_sum,
        exponent_sum_mod_12=exponent_sum % 12,
        quadratic_right=quadratic_right,
        quadratic_c=quadratic_c,
        quadratic_mixed=quadratic_mixed,
        quadratic_relations_ok=quadratic_ok,
        level_prime_power_away_from_2_3=level_ok,
        preserves_right_data=preserves_right_data,
        preserves_t_edge=preserves_t_edge,
        p25_finite_payload_ok=p25_finite_payload_ok,
        recommendation=recommendation,
        row_ok=row_ok,
    )


def c_axis_projection(packet: Ring) -> Ring:
    out: Ring = {}
    for (_right_class, c_log), coefficient in packet.items():
        add_packet_entry(out, (0, c_log), coefficient)
    return dict(sorted(out.items()))


def profile_kl_exponent_matrix_screen() -> KLExponentMatrixScreenProfile:
    target_packet = source_packet()
    target_packet_profile = kl_profile(
        "source_packet_common_level_507",
        target_packet,
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation=(
            "positive necessary congruence screen; still needs theorem-legal "
            "mixed C3 x C169 Siegel/Kronecker lift"
        ),
    )

    theta2_inverse = normalized_y_product_footprint(
        BASE_POINT,
        KERNEL_SHIFT,
        D_SHIFT,
        BRIDGE_SHIFT,
    )
    theta2_inverse_profile = kl_profile(
        "theta2_inverse_raw_level_12675",
        theta2_inverse,
        RAW_LEVEL,
        C_ORDER,
        RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation=(
            "exact theta2 inverse divisor footprint survives the congruence "
            "screen; level is mixed/composite, so a legal lift remains needed"
        ),
    )
    theta2 = {coord: -coefficient for coord, coefficient in theta2_inverse.items()}
    theta2_profile = kl_profile(
        "theta2_raw_level_12675",
        theta2,
        RAW_LEVEL,
        C_ORDER,
        RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation="same congruence status as theta2 inverse, with orientation reversed",
    )

    c_projection = c_axis_projection(target_packet)
    c_projection_profile = kl_profile(
        "c_axis_projection_level_169",
        c_projection,
        C_ORDER,
        0,
        1,
        preserves_right_data=False,
        preserves_t_edge=False,
        p25_finite_payload_ok=False,
        recommendation=(
            "prime-power Siegel congruence survives only after losing right "
            "classes and the T edge; finite payload is insufficient"
        ),
    )

    truncated_d = kl_profile(
        "truncated_d_control",
        source_packet(d_length=2),
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        True,
        True,
        False,
        "reject: D length two breaks the congruence screen",
    )
    wrong_d = kl_profile(
        "wrong_d_control",
        source_packet(d_step=(1, 4)),
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        True,
        True,
        False,
        "reject: wrong D class breaks the congruence screen",
    )
    wrong_t = kl_profile(
        "wrong_t_control",
        source_packet(t_step=add_quotient((2, 113), (1, 3))),
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        True,
        False,
        False,
        "reject: wrong T edge breaks the congruence screen",
    )
    positive_only = kl_profile(
        "positive_only_control",
        {coord: coefficient for coord, coefficient in target_packet.items() if coefficient > 0},
        QUOTIENT_LEVEL,
        C_ORDER,
        QUOTIENT_RIGHT_ORDER,
        True,
        False,
        False,
        "reject: missing negative layer breaks sum and quadratic conditions",
    )

    exact_survives = (
        target_packet_profile.quadratic_relations_ok
        and theta2_inverse_profile.quadratic_relations_ok
        and theta2_profile.quadratic_relations_ok
        and target_packet_profile.exponent_sum_mod_12 == 0
        and theta2_inverse_profile.exponent_sum_mod_12 == 0
    )
    projection_insufficient = (
        c_projection_profile.quadratic_relations_ok
        and c_projection_profile.level_prime_power_away_from_2_3
        and not c_projection_profile.p25_finite_payload_ok
        and not c_projection_profile.preserves_right_data
        and not c_projection_profile.preserves_t_edge
    )
    row_ok = (
        exact_survives
        and projection_insufficient
        and not truncated_d.quadratic_relations_ok
        and not wrong_d.quadratic_relations_ok
        and not wrong_t.quadratic_relations_ok
        and not positive_only.quadratic_relations_ok
        and target_packet_profile.support == 6
        and theta2_inverse_profile.support == 300
        and theta2_profile.support == 300
        and target_packet_profile.level_prime_power_away_from_2_3 is False
        and theta2_inverse_profile.level_prime_power_away_from_2_3 is False
    )

    return KLExponentMatrixScreenProfile(
        source_packet_profile=target_packet_profile,
        theta2_inverse_profile=theta2_inverse_profile,
        theta2_profile=theta2_profile,
        c_axis_projection_profile=c_projection_profile,
        truncated_d_rejected=not truncated_d.quadratic_relations_ok,
        wrong_d_rejected=not wrong_d.quadratic_relations_ok,
        wrong_t_rejected=not wrong_t.quadratic_relations_ok,
        positive_only_rejected=not positive_only.quadratic_relations_ok,
        exact_payloads_survive_congruence_screen=exact_survives,
        prime_power_projection_is_finite_insufficient=projection_insufficient,
        next_debt=(
            "find a theorem-legal lift/product: exact p25 payloads pass the "
            "Kubert-Lang quadratic congruence screen, but their natural levels "
            "507 and 12675 are mixed/composite and include the row-3 component"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang exponent-matrix precheck")
    profile = profile_kl_exponent_matrix_screen()
    print(f"kl_exponent_matrix_screen_profile={profile}")
    print("accepted_congruence_profiles")
    print(
        "  source_packet_common_level_507="
        f"{int(profile.source_packet_profile.quadratic_relations_ok)}"
    )
    print(
        "  theta2_inverse_raw_level_12675="
        f"{int(profile.theta2_inverse_profile.quadratic_relations_ok)}"
    )
    print(
        "  theta2_raw_level_12675="
        f"{int(profile.theta2_profile.quadratic_relations_ok)}"
    )
    print("controls")
    print(f"  truncated_D_rejected={int(profile.truncated_d_rejected)}")
    print(f"  wrong_D_rejected={int(profile.wrong_d_rejected)}")
    print(f"  wrong_T_rejected={int(profile.wrong_t_rejected)}")
    print(f"  positive_only_rejected={int(profile.positive_only_rejected)}")
    print("interpretation")
    print("  exact_payloads_survive_Kubert_Lang_quadratic_congruence_screen=1")
    print("  C169_prime_power_projection_passes_but_loses_p25_right_T_data=1")
    print("  remaining_debt_is_theorem_legal_mixed_level_lift_or_product=1")
    print(f"robert_ksy_theta2_kubert_lang_exponent_matrix_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
