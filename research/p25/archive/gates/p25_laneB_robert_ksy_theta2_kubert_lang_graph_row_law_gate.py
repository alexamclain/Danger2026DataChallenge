#!/usr/bin/env python3
"""Graph row-law gate for the p25 Kubert-Lang exact matrix route.

The C_169 projection of the six-cell KL packet is prime-power-compatible, but
it loses the C_3 row selector.  This gate asks how much of that row selector is
recovered by the most natural sign-affine lift:

    positive rows: row = pos_base + slope*j
    negative rows: row = neg_base + slope*j

for the three C-axis cells in each sign.  The answer is sharp: every one of
the 27 sign-affine row laws passes the elementary KL congruence screen.  The
fixed T edge narrows them to three row translations, and the base row anchor
selects exactly one.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_crt_coupling_gate import (
    balanced,
    d_segment_t_edge_shape,
    exact_base_d_t_shape,
    fixed_t_edge_shape,
    kl_congruence_ok,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    C_ORDER,
    QUOTIENT_RIGHT_ORDER,
    Ring,
    source_packet,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    SourceQuotientPacketProfile,
    packet_entries,
    profile_source_quotient_packet,
)


POSITIVE_C_AXIS = (25, 28, 31)
NEGATIVE_C_AXIS = (138, 141, 144)


@dataclass(frozen=True)
class SignAffineRowLaw:
    slope: int
    positive_base_row: int
    negative_base_row: int
    packet_exact: bool
    kl_congruence_ok: bool
    balanced: bool
    d_segment_t_edge_shape: bool
    fixed_t_edge_shape: bool
    exact_base_d_t_shape: bool


@dataclass(frozen=True)
class FixedTEdgeRowLaw:
    slope: int
    positive_base_row: int
    negative_base_row: int
    source_packet_profile: SourceQuotientPacketProfile


@dataclass(frozen=True)
class KLGraphRowLawProfile:
    c_axis_positive_cells: tuple[int, int, int]
    c_axis_negative_cells: tuple[int, int, int]
    sign_affine_laws_scanned: int
    kl_congruence_laws: int
    balanced_laws: int
    d_segment_t_edge_laws: int
    fixed_t_edge_laws: int
    exact_base_d_t_laws: int
    exact_law: SignAffineRowLaw
    fixed_t_edge_profiles: tuple[FixedTEdgeRowLaw, ...]
    all_sign_affine_laws_pass_kl: bool
    fixed_t_edge_leaves_three_row_translates: bool
    base_row_anchor_selects_unique_target: bool
    wrong_fixed_t_row_translates_rejected_by_source_packet_contract: bool
    next_debt: str
    row_ok: bool


def sign_affine_packet(slope: int, positive_base_row: int, negative_base_row: int) -> Ring:
    packet: Ring = {}
    for index, c_log in enumerate(POSITIVE_C_AXIS):
        packet[((positive_base_row + slope * index) % QUOTIENT_RIGHT_ORDER, c_log)] = 1
    for index, c_log in enumerate(NEGATIVE_C_AXIS):
        packet[((negative_base_row + slope * index) % QUOTIENT_RIGHT_ORDER, c_log)] = -1
    return dict(sorted(packet.items()))


def row_law(slope: int, positive_base_row: int, negative_base_row: int) -> SignAffineRowLaw:
    packet = sign_affine_packet(slope, positive_base_row, negative_base_row)
    return SignAffineRowLaw(
        slope=slope,
        positive_base_row=positive_base_row,
        negative_base_row=negative_base_row,
        packet_exact=packet == source_packet(),
        kl_congruence_ok=kl_congruence_ok(packet),
        balanced=balanced(packet),
        d_segment_t_edge_shape=d_segment_t_edge_shape(packet),
        fixed_t_edge_shape=fixed_t_edge_shape(packet),
        exact_base_d_t_shape=exact_base_d_t_shape(packet),
    )


def profile_graph_row_law() -> KLGraphRowLawProfile:
    laws = tuple(
        row_law(slope, positive_base_row, negative_base_row)
        for slope in range(QUOTIENT_RIGHT_ORDER)
        for positive_base_row in range(QUOTIENT_RIGHT_ORDER)
        for negative_base_row in range(QUOTIENT_RIGHT_ORDER)
    )
    fixed_t_laws = tuple(law for law in laws if law.fixed_t_edge_shape)
    fixed_t_profiles = tuple(
        FixedTEdgeRowLaw(
            slope=law.slope,
            positive_base_row=law.positive_base_row,
            negative_base_row=law.negative_base_row,
            source_packet_profile=profile_source_quotient_packet(
                f"sign_affine_fixed_T_{law.slope}_{law.positive_base_row}_{law.negative_base_row}",
                packet_entries(
                    sign_affine_packet(
                        law.slope,
                        law.positive_base_row,
                        law.negative_base_row,
                    )
                ),
                1,
            ),
        )
        for law in fixed_t_laws
    )
    exact_laws = tuple(law for law in laws if law.exact_base_d_t_shape)
    exact_law = exact_laws[0]
    wrong_fixed_t_rejected = all(
        profile.source_packet_profile.ok == profile.source_packet_profile.packet_exact
        for profile in fixed_t_profiles
    ) and sum(int(profile.source_packet_profile.ok) for profile in fixed_t_profiles) == 1

    row_ok = (
        C_ORDER == 169
        and QUOTIENT_RIGHT_ORDER == 3
        and POSITIVE_C_AXIS == (25, 28, 31)
        and NEGATIVE_C_AXIS == (138, 141, 144)
        and len(laws) == 27
        and sum(int(law.kl_congruence_ok) for law in laws) == 27
        and sum(int(law.balanced) for law in laws) == 21
        and sum(int(law.d_segment_t_edge_shape) for law in laws) == 9
        and sum(int(law.fixed_t_edge_shape) for law in laws) == 3
        and len(exact_laws) == 1
        and exact_law
        == SignAffineRowLaw(
            slope=1,
            positive_base_row=1,
            negative_base_row=0,
            packet_exact=True,
            kl_congruence_ok=True,
            balanced=True,
            d_segment_t_edge_shape=True,
            fixed_t_edge_shape=True,
            exact_base_d_t_shape=True,
        )
        and tuple(
            (
                profile.slope,
                profile.positive_base_row,
                profile.negative_base_row,
                profile.source_packet_profile.ok,
            )
            for profile in fixed_t_profiles
        )
        == (
            (1, 0, 2, False),
            (1, 1, 0, True),
            (1, 2, 1, False),
        )
        and wrong_fixed_t_rejected
    )
    return KLGraphRowLawProfile(
        c_axis_positive_cells=POSITIVE_C_AXIS,
        c_axis_negative_cells=NEGATIVE_C_AXIS,
        sign_affine_laws_scanned=len(laws),
        kl_congruence_laws=sum(int(law.kl_congruence_ok) for law in laws),
        balanced_laws=sum(int(law.balanced) for law in laws),
        d_segment_t_edge_laws=sum(int(law.d_segment_t_edge_shape) for law in laws),
        fixed_t_edge_laws=sum(int(law.fixed_t_edge_shape) for law in laws),
        exact_base_d_t_laws=len(exact_laws),
        exact_law=exact_law,
        fixed_t_edge_profiles=fixed_t_profiles,
        all_sign_affine_laws_pass_kl=all(law.kl_congruence_ok for law in laws),
        fixed_t_edge_leaves_three_row_translates=len(fixed_t_laws) == 3,
        base_row_anchor_selects_unique_target=len(exact_laws) == 1,
        wrong_fixed_t_row_translates_rejected_by_source_packet_contract=wrong_fixed_t_rejected,
        next_debt=(
            "an exact Kubert-Lang/Siegel theorem must supply the sign-affine "
            "row graph and base row anchor; C169 projection plus KL congruences "
            "do not select the p25 packet"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang graph row-law gate")
    profile = profile_graph_row_law()
    print(f"kl_graph_row_law_profile={profile}")
    print("sign_affine_scan")
    print(f"  laws_scanned={profile.sign_affine_laws_scanned}")
    print(f"  kl_congruence_laws={profile.kl_congruence_laws}")
    print(f"  balanced_laws={profile.balanced_laws}")
    print(f"  d_segment_t_edge_laws={profile.d_segment_t_edge_laws}")
    print(f"  fixed_t_edge_laws={profile.fixed_t_edge_laws}")
    print(f"  exact_base_d_t_laws={profile.exact_base_d_t_laws}")
    print(f"  exact_law={profile.exact_law}")
    print("fixed_T_row_translates")
    for row in profile.fixed_t_edge_profiles:
        print(
            "  "
            f"slope={row.slope} pos_base={row.positive_base_row} "
            f"neg_base={row.negative_base_row} "
            f"source_packet_ok={int(row.source_packet_profile.ok)}"
        )
    print("interpretation")
    print("  C169_projection_plus_KL_congruences_do_not_select_the_row_graph=1")
    print("  fixed_T_edge_leaves_three_row_translates=1")
    print("  base_row_anchor_selects_the_unique_target=1")
    print("  wrong_fixed_T_row_translates_fail_source_packet_contract=1")
    print(
        "robert_ksy_theta2_kubert_lang_graph_row_law_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_graph_row_law_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
