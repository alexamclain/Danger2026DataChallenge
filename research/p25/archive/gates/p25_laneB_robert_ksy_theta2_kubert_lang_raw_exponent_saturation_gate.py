#!/usr/bin/env python3
"""Raw KL exponent-screen saturation for the p25 anti-invariant product.

The anti-invariant normalized-y intake is now the smallest finite KL/KSY
interface.  This gate checks whether the elementary Kubert-Lang exponent
congruences at raw level 12675 select that interface.

They do not.  The target raw source packet passes, but so do missing-K,
collapsed-K, truncated-D, wrong-D, and shifted-center anti-invariant controls.
This is expected: a signed pair z^a - z^-a cancels the exponent sum and all
quadratic sums.  Therefore raw KL congruences are necessary hygiene, not a
producer selector.  The finite anti-invariant product intake remains the
selector.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_product_gate import (
    centered_source_trace,
    profile_anti_invariant_product_intake,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import kl_profile
from p25_laneB_robert_ksy_theta2_kubert_lang_raw_ktrace_reflection_gate import (
    source_packet_from_denominator,
)
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import add_coord
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
RAW_LEVEL = RIGHT_ORDER * C_ORDER


@dataclass(frozen=True)
class RawExponentScreenRow:
    name: str
    center: Coord
    k_step: Coord
    d_step: Coord
    k_length: int
    d_offsets: tuple[int, ...]
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    exponent_sum_mod_12: int
    quadratic_right: int
    quadratic_c: int
    quadratic_mixed: int
    kl_congruence_ok: bool
    finite_intake_accepts: bool


@dataclass(frozen=True)
class RawExponentSaturationProfile:
    raw_level: int
    target_row: RawExponentScreenRow
    t_edge_row: RawExponentScreenRow
    control_rows: tuple[RawExponentScreenRow, ...]
    all_rows_pass_kl_screen: bool
    controls_rejected_by_finite_intake: bool
    anti_invariant_pair_identity_explains_pass: bool
    kl_screen_is_not_selector: bool
    first_selector: str
    row_ok: bool


def inverse_coord(coord: Coord) -> Coord:
    return ((-coord[0]) % RIGHT_ORDER, (-coord[1]) % C_ORDER)


def coefficient_counts(ring: Ring) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(Counter(ring.values()).items()))


def anti_invariant_source_packet(
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
) -> Ring:
    centers = centered_source_trace(center, k_step, d_step, k_length, d_offsets)
    return source_packet_from_denominator(centers, inverse_coord)


def t_edge_source_packet(
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    t_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
) -> Ring:
    centers = centered_source_trace(center, k_step, d_step, k_length, d_offsets)
    return source_packet_from_denominator(centers, lambda point: add_coord(point, t_step))


def profile_raw_packet(
    name: str,
    center: Coord,
    k_step: Coord,
    d_step: Coord,
    k_length: int = 25,
    d_offsets: tuple[int, ...] = (-1, 0, 1),
    finite_intake_accepts: bool = False,
    use_t_edge: bool = False,
) -> RawExponentScreenRow:
    ring = (
        t_edge_source_packet(center, k_step, d_step, BRIDGE_SHIFT, k_length, d_offsets)
        if use_t_edge
        else anti_invariant_source_packet(center, k_step, d_step, k_length, d_offsets)
    )
    profile = kl_profile(
        name,
        ring,
        RAW_LEVEL,
        C_ORDER,
        RIGHT_ORDER,
        preserves_right_data=True,
        preserves_t_edge=True,
        p25_finite_payload_ok=True,
        recommendation="raw anti-invariant source-packet exponent screen",
    )
    return RawExponentScreenRow(
        name=name,
        center=center,
        k_step=k_step,
        d_step=d_step,
        k_length=k_length,
        d_offsets=d_offsets,
        support=len(ring),
        coefficient_counts=coefficient_counts(ring),
        exponent_sum_mod_12=profile.exponent_sum_mod_12,
        quadratic_right=profile.quadratic_right,
        quadratic_c=profile.quadratic_c,
        quadratic_mixed=profile.quadratic_mixed,
        kl_congruence_ok=profile.quadratic_relations_ok,
        finite_intake_accepts=finite_intake_accepts,
    )


def profile_raw_exponent_saturation() -> RawExponentSaturationProfile:
    center = add_coord(BASE_POINT, D_SHIFT)
    finite_intake = profile_anti_invariant_product_intake()
    target = profile_raw_packet(
        "target_raw_anti_invariant_packet",
        center,
        KERNEL_SHIFT,
        D_SHIFT,
        finite_intake_accepts=finite_intake.row_ok,
    )
    t_edge = profile_raw_packet(
        "target_raw_T_edge_packet",
        center,
        KERNEL_SHIFT,
        D_SHIFT,
        finite_intake_accepts=finite_intake.row_ok,
        use_t_edge=True,
    )
    controls = (
        profile_raw_packet(
            "missing_K_control",
            center,
            KERNEL_SHIFT,
            D_SHIFT,
            k_length=1,
        ),
        profile_raw_packet(
            "collapsed_K_control",
            center,
            (0, 0),
            D_SHIFT,
        ),
        profile_raw_packet(
            "truncated_D_control",
            center,
            KERNEL_SHIFT,
            D_SHIFT,
            d_offsets=(-1, 0),
        ),
        profile_raw_packet(
            "wrong_D_control",
            center,
            KERNEL_SHIFT,
            (D_SHIFT[0], (D_SHIFT[1] + 1) % C_ORDER),
        ),
        profile_raw_packet(
            "shifted_center_control",
            add_coord(center, D_SHIFT),
            KERNEL_SHIFT,
            D_SHIFT,
        ),
    )
    all_rows = (target, t_edge) + controls
    controls_rejected = (
        finite_intake.missing_k_rejected
        and finite_intake.collapsed_k_rejected
        and finite_intake.truncated_d_rejected
        and finite_intake.wrong_d_rejected
        and finite_intake.shifted_center_rejected
    )
    all_pass = all(row.kl_congruence_ok for row in all_rows)
    anti_invariant_identity = all(
        row.exponent_sum_mod_12 == 0
        and row.quadratic_right == 0
        and row.quadratic_c == 0
        and row.quadratic_mixed == 0
        for row in all_rows
    )
    row_ok = (
        RAW_LEVEL == 12675
        and target.support == 150
        and t_edge.support == 150
        and target.coefficient_counts == ((-1, 75), (1, 75))
        and t_edge.coefficient_counts == ((-1, 75), (1, 75))
        and tuple(row.support for row in controls) == (6, 6, 100, 150, 150)
        and tuple(row.coefficient_counts for row in controls)
        == (
            ((-1, 3), (1, 3)),
            ((-25, 3), (25, 3)),
            ((-1, 50), (1, 50)),
            ((-1, 75), (1, 75)),
            ((-1, 75), (1, 75)),
        )
        and all_pass
        and controls_rejected
        and finite_intake.row_ok
        and anti_invariant_identity
    )
    return RawExponentSaturationProfile(
        raw_level=RAW_LEVEL,
        target_row=target,
        t_edge_row=t_edge,
        control_rows=controls,
        all_rows_pass_kl_screen=all_pass,
        controls_rejected_by_finite_intake=controls_rejected,
        anti_invariant_pair_identity_explains_pass=anti_invariant_identity,
        kl_screen_is_not_selector=all_pass and controls_rejected,
        first_selector=(
            "anti-invariant product intake: full K trace, symmetric length-three "
            "D segment, exact center C=(47,28), and orientation"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang raw exponent-saturation gate")
    profile = profile_raw_exponent_saturation()
    print(f"raw_exponent_saturation_profile={profile}")
    print("accepted_rows")
    print(f"  target={profile.target_row}")
    print(f"  t_edge={profile.t_edge_row}")
    print("controls")
    for row in profile.control_rows:
        print(f"  {row}")
    print("saturation_laws")
    print("  target_raw_source_packet_passes_KL_exponent_screen=1")
    print("  raw_T_edge_packet_passes_same_screen=1")
    print("  missing_K_collapsed_K_truncated_D_wrong_D_and_shifted_center_controls_also_pass_KL_screen=1")
    print("  finite_anti_invariant_product_intake_rejects_those_controls=1")
    print("interpretation")
    print("  raw_anti_invariant_KL_exponent_congruences_are_necessary_but_not_selective=1")
    print("  theorem_claims_need_the_finite_intake_geometry_not_only_exponent_sums=1")
    print(f"robert_ksy_theta2_kubert_lang_raw_exponent_saturation_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_raw_exponent_saturation_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
