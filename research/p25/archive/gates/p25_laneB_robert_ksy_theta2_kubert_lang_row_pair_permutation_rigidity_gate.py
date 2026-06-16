#!/usr/bin/env python3
"""Permutation rigidity for the p25 row-labeled KL pair contract.

The row-labeled pair contract killed row-only shortcuts and one wrong pairing.
This gate scans the whole finite family with the same visible C-axis
projection and one signed pair per row:

    assign 25,28,31 to the three rows with coefficient +1,
    assign 138,141,144 to the three rows with coefficient -1.

All 36 such packets pass the elementary Kubert-Lang congruence screen and are
balanced.  The mixed source geometry is much stricter: only the recorded packet
passes the primitive-K source contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

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
from p25_laneB_robert_ksy_theta2_kubert_lang_row_labeled_pair_contract_gate import (
    c_axis_projection_vector,
)
from p25_laneB_robert_ksy_theta2_source_quotient_packet_harness import (
    packet_entries,
    profile_source_quotient_packet,
)


POSITIVE_C_AXIS = (25, 28, 31)
NEGATIVE_C_AXIS = (138, 141, 144)
TARGET_POSITIVE_BY_ROW = (31, 25, 28)
TARGET_NEGATIVE_BY_ROW = (138, 141, 144)


@dataclass(frozen=True)
class RowPairPermutationLaw:
    positive_by_row: tuple[int, int, int]
    negative_by_row: tuple[int, int, int]
    packet_exact: bool
    c_axis_projection_matches_target: bool
    kl_congruence_ok: bool
    balanced: bool
    d_segment_t_edge_shape: bool
    fixed_t_edge_shape: bool
    exact_base_d_t_shape: bool
    source_contract_ok: bool
    trace_correct: bool


@dataclass(frozen=True)
class RowPairPermutationRigidityProfile:
    permutations_scanned: int
    c_axis_projection_hits: int
    kl_congruence_hits: int
    balanced_hits: int
    d_segment_t_edge_hits: int
    fixed_t_edge_hits: int
    exact_base_d_t_hits: int
    source_contract_hits: int
    trace_correct_hits: int
    fixed_t_edge_laws: tuple[RowPairPermutationLaw, ...]
    source_contract_law: RowPairPermutationLaw
    elementary_kl_screen_saturated: bool
    fixed_t_leaves_three_cyclic_row_translates: bool
    source_contract_selects_unique_target: bool
    recommendation: str
    row_ok: bool


def pair_permutation_packet(
    positive_by_row: tuple[int, int, int],
    negative_by_row: tuple[int, int, int],
) -> Ring:
    packet: Ring = {}
    for row, c_log in enumerate(positive_by_row):
        packet[(row, c_log)] = 1
    for row, c_log in enumerate(negative_by_row):
        packet[(row, c_log)] = -1
    return dict(sorted(packet.items()))


def profile_law(
    positive_by_row: tuple[int, int, int],
    negative_by_row: tuple[int, int, int],
) -> RowPairPermutationLaw:
    packet = pair_permutation_packet(positive_by_row, negative_by_row)
    source_profile = profile_source_quotient_packet(
        f"row_pair_perm_pos_{positive_by_row}_neg_{negative_by_row}",
        packet_entries(packet),
        1,
    )
    return RowPairPermutationLaw(
        positive_by_row=positive_by_row,
        negative_by_row=negative_by_row,
        packet_exact=packet == source_packet(),
        c_axis_projection_matches_target=c_axis_projection_vector(packet)
        == (1, 1, 1, -1, -1, -1),
        kl_congruence_ok=kl_congruence_ok(packet),
        balanced=balanced(packet),
        d_segment_t_edge_shape=d_segment_t_edge_shape(packet),
        fixed_t_edge_shape=fixed_t_edge_shape(packet),
        exact_base_d_t_shape=exact_base_d_t_shape(packet),
        source_contract_ok=source_profile.ok,
        trace_correct=source_profile.bridge_profile.trace_correct,
    )


def profile_row_pair_permutation_rigidity() -> RowPairPermutationRigidityProfile:
    laws = tuple(
        profile_law(positive_by_row, negative_by_row)
        for positive_by_row in permutations(POSITIVE_C_AXIS)
        for negative_by_row in permutations(NEGATIVE_C_AXIS)
    )
    fixed_t_laws = tuple(law for law in laws if law.fixed_t_edge_shape)
    source_laws = tuple(law for law in laws if law.source_contract_ok)
    source_law = source_laws[0]
    elementary_screen_saturated = (
        all(law.c_axis_projection_matches_target for law in laws)
        and all(law.kl_congruence_ok for law in laws)
        and all(law.balanced for law in laws)
    )
    fixed_t_cyclic = tuple(
        (law.positive_by_row, law.negative_by_row, law.source_contract_ok)
        for law in fixed_t_laws
    ) == (
        ((25, 28, 31), (141, 144, 138), False),
        ((28, 31, 25), (144, 138, 141), False),
        ((31, 25, 28), (138, 141, 144), True),
    )
    source_selects_target = (
        len(source_laws) == 1
        and source_law.positive_by_row == TARGET_POSITIVE_BY_ROW
        and source_law.negative_by_row == TARGET_NEGATIVE_BY_ROW
        and source_law.packet_exact
        and source_law.exact_base_d_t_shape
        and source_law.trace_correct
    )
    row_ok = (
        C_ORDER == 169
        and QUOTIENT_RIGHT_ORDER == 3
        and len(laws) == 36
        and sum(int(law.c_axis_projection_matches_target) for law in laws) == 36
        and sum(int(law.kl_congruence_ok) for law in laws) == 36
        and sum(int(law.balanced) for law in laws) == 36
        and sum(int(law.d_segment_t_edge_shape) for law in laws) == 9
        and sum(int(law.fixed_t_edge_shape) for law in laws) == 3
        and sum(int(law.exact_base_d_t_shape) for law in laws) == 1
        and sum(int(law.source_contract_ok) for law in laws) == 1
        and sum(int(law.trace_correct) for law in laws) == 1
        and elementary_screen_saturated
        and fixed_t_cyclic
        and source_selects_target
    )
    return RowPairPermutationRigidityProfile(
        permutations_scanned=len(laws),
        c_axis_projection_hits=sum(int(law.c_axis_projection_matches_target) for law in laws),
        kl_congruence_hits=sum(int(law.kl_congruence_ok) for law in laws),
        balanced_hits=sum(int(law.balanced) for law in laws),
        d_segment_t_edge_hits=sum(int(law.d_segment_t_edge_shape) for law in laws),
        fixed_t_edge_hits=sum(int(law.fixed_t_edge_shape) for law in laws),
        exact_base_d_t_hits=sum(int(law.exact_base_d_t_shape) for law in laws),
        source_contract_hits=sum(int(law.source_contract_ok) for law in laws),
        trace_correct_hits=sum(int(law.trace_correct) for law in laws),
        fixed_t_edge_laws=fixed_t_laws,
        source_contract_law=source_law,
        elementary_kl_screen_saturated=elementary_screen_saturated,
        fixed_t_leaves_three_cyclic_row_translates=fixed_t_cyclic,
        source_contract_selects_unique_target=source_selects_target,
        recommendation=(
            "do not accept a theorem that only supplies the C-axis projection, "
            "one pair per row, or KL congruences; it must recover the exact "
            "fixed-T cyclic row translate selected by the source contract"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang row-pair permutation rigidity gate")
    profile = profile_row_pair_permutation_rigidity()
    print(f"row_pair_permutation_rigidity_profile={profile}")
    print("permutation_scan")
    print(f"  permutations_scanned={profile.permutations_scanned}")
    print(f"  c_axis_projection_hits={profile.c_axis_projection_hits}")
    print(f"  kl_congruence_hits={profile.kl_congruence_hits}")
    print(f"  balanced_hits={profile.balanced_hits}")
    print(f"  d_segment_t_edge_hits={profile.d_segment_t_edge_hits}")
    print(f"  fixed_t_edge_hits={profile.fixed_t_edge_hits}")
    print(f"  exact_base_d_t_hits={profile.exact_base_d_t_hits}")
    print(f"  source_contract_hits={profile.source_contract_hits}")
    print(f"  trace_correct_hits={profile.trace_correct_hits}")
    print("fixed_T_row_translates")
    for law in profile.fixed_t_edge_laws:
        print(
            "  "
            f"positive_by_row={law.positive_by_row} "
            f"negative_by_row={law.negative_by_row} "
            f"source_ok={int(law.source_contract_ok)}"
        )
    print("unique_source_contract_law")
    print(f"  positive_by_row={profile.source_contract_law.positive_by_row}")
    print(f"  negative_by_row={profile.source_contract_law.negative_by_row}")
    print("interpretation")
    print("  elementary_KL_screen_is_saturated_on_pair_permutations=1")
    print("  fixed_T_edge_leaves_three_cyclic_row_translates=1")
    print("  source_contract_selects_unique_target_translate=1")
    print(
        "robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
