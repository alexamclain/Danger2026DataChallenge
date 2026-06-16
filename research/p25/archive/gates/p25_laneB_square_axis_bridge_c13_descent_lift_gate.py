#!/usr/bin/env python3
"""C13 descent/lift obstruction for the p25 square-axis bridge shadow.

The formal-unit bridge shadow has a cheap C_13 projection: reducing the
C_169 source coordinate modulo 13 preserves the 150-cell signed product.
This is a tempting arithmetic descent because the D and T C-axis Kummer
classes drop from degree 169 to degree 13 on the shadow.

This gate records why that shadow is not enough.  Pulling the C_13 shadow
back to C_169 overproduces by a factor of 13, loses all non-lifted C_169
characters, and fails the bridge candidate harness.  The full bridge is a
specific fiber lift of the C_13 shadow, not the pullback of that shadow.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_square_axis_bridge_axis_hull_character_gap_gate import support_profile
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    CandidateProfile,
    crt_source_to_raw,
    profile_candidate,
    quotient_mask,
    quotient_trace,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_factor_kummer_gate import factor_profile
from p25_laneB_square_axis_bridge_formal_unit_shadow_gate import (
    Ring,
    formal_factors,
    multiply_factors,
    source_mask_to_raw,
)
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    BASE_POINT,
    BRIDGE_SHIFT,
    C_ORDER,
    D_SHIFT,
    KERNEL_SHIFT,
    RIGHT_ORDER,
)
from p25_laneB_square_axis_local_graph_residue_gate import RAW_ORDER


Coord13 = tuple[int, int]


@dataclass(frozen=True)
class C13DescentProfile:
    full_support: int
    projected_support: int
    projected_degree: int
    projected_coefficient_counts: tuple[tuple[int, int], ...]
    projected_factor_word_matches: bool
    true_raw_support: int
    pullback_raw_support: int
    pullback_quotient_support: int
    pullback_trace_correct: bool
    pullback_kernel_modes: tuple[int, ...]
    pullback_raw_relation_mismatches: int
    pullback_pure_c_characters: int
    pullback_mixed_characters: int
    missing_pure_c_characters: int
    missing_mixed_characters: int
    fiber_set_size_counts: tuple[tuple[int, int], ...]
    selected_fiber_counts: tuple[tuple[int, int], ...]
    c_kummer_degree_gap: tuple[tuple[str, int, int], ...]


def add_coord_mod(left: Coord13, right: Coord13, c_modulus: int) -> Coord13:
    return (
        (left[0] + right[0]) % RIGHT_ORDER,
        (left[1] + right[1]) % c_modulus,
    )


def scale_coord_mod(step: Coord13, scale: int, c_modulus: int) -> Coord13:
    return ((step[0] * scale) % RIGHT_ORDER, (step[1] * scale) % c_modulus)


def multiply_ring_mod(left: dict[Coord13, int], right: dict[Coord13, int], c_modulus: int) -> dict[Coord13, int]:
    out: dict[Coord13, int] = {}
    for left_coord, left_value in left.items():
        for right_coord, right_value in right.items():
            coord = add_coord_mod(left_coord, right_coord, c_modulus)
            out[coord] = out.get(coord, 0) + left_value * right_value
            if out[coord] == 0:
                del out[coord]
    return dict(sorted(out.items()))


def geometric_factor_mod(step: Coord13, length: int, c_modulus: int) -> dict[Coord13, int]:
    return {scale_coord_mod(step, index, c_modulus): 1 for index in range(length)}


def projected_factor_word() -> dict[Coord13, int]:
    c_modulus = 13
    factors = (
        {(BASE_POINT[0], BASE_POINT[1] % c_modulus): 1},
        geometric_factor_mod((KERNEL_SHIFT[0], KERNEL_SHIFT[1] % c_modulus), 25, c_modulus),
        geometric_factor_mod((D_SHIFT[0], D_SHIFT[1] % c_modulus), 3, c_modulus),
        {
            (0, 0): 1,
            (BRIDGE_SHIFT[0], BRIDGE_SHIFT[1] % c_modulus): -1,
        },
    )
    product: dict[Coord13, int] = {(0, 0): 1}
    for factor in factors:
        product = multiply_ring_mod(product, factor, c_modulus)
    return product


def project_to_c13(ring: Ring) -> dict[Coord13, int]:
    out: dict[Coord13, int] = {}
    for (right_log, c_log), value in ring.items():
        coord = (right_log, c_log % 13)
        out[coord] = out.get(coord, 0) + value
        if out[coord] == 0:
            del out[coord]
    return dict(sorted(out.items()))


def pullback_from_c13(shadow: dict[Coord13, int]) -> Ring:
    out: Ring = {}
    for (right_log, c13), value in shadow.items():
        for fiber in range(13):
            out[(right_log, c13 + 13 * fiber)] = value
    return dict(sorted(out.items()))


def source_ring_to_raw(ring: Ring) -> list[int]:
    raw = [0] * RAW_ORDER
    for (right_log, c_log), value in ring.items():
        raw[crt_source_to_raw(right_log, c_log)] = value
    return raw


def fiber_profile(full: Ring) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, int], ...]]:
    fibers_by_shadow: dict[tuple[int, int, int], set[int]] = {}
    for (right_log, c_log), value in full.items():
        fibers_by_shadow.setdefault((right_log, c_log % 13, value), set()).add(c_log // 13)
    set_size_counts = tuple(sorted(Counter(len(values) for values in fibers_by_shadow.values()).items()))
    selected_fiber_counts = tuple(
        sorted(Counter(next(iter(values)) for values in fibers_by_shadow.values()).items())
    )
    return set_size_counts, selected_fiber_counts


def profile_c13_descent() -> tuple[C13DescentProfile, CandidateProfile, CandidateProfile]:
    full = multiply_factors(formal_factors())
    projected = project_to_c13(full)
    pullback = pullback_from_c13(projected)
    target = target_raw_bridge()
    true_candidate = profile_candidate("formal_unit_shadow", source_mask_to_raw(full), target)
    pullback_candidate = profile_candidate("c13_naive_pullback", source_ring_to_raw(pullback), target)
    pullback_q_profile = support_profile(
        "c13_naive_pullback_quotient",
        quotient_mask(quotient_trace(source_ring_to_raw(pullback))),
    )
    true_q_profile = support_profile(
        "true_bridge_quotient",
        quotient_mask(quotient_trace(source_mask_to_raw(full))),
    )
    set_size_counts, selected_fiber_counts = fiber_profile(full)
    d_profile = factor_profile("D_segment", D_SHIFT)
    t_profile = factor_profile("bridge_edge", BRIDGE_SHIFT)

    profile = C13DescentProfile(
        full_support=len(full),
        projected_support=len(projected),
        projected_degree=sum(projected.values()),
        projected_coefficient_counts=tuple(sorted(Counter(projected.values()).items())),
        projected_factor_word_matches=projected == projected_factor_word(),
        true_raw_support=true_candidate.raw_support,
        pullback_raw_support=pullback_candidate.raw_support,
        pullback_quotient_support=pullback_candidate.quotient_support,
        pullback_trace_correct=pullback_candidate.trace_correct,
        pullback_kernel_modes=pullback_candidate.kernel_modes,
        pullback_raw_relation_mismatches=pullback_candidate.raw_relation_mismatches,
        pullback_pure_c_characters=pullback_q_profile.pure_c_nonzero,
        pullback_mixed_characters=pullback_q_profile.mixed_nonzero,
        missing_pure_c_characters=true_q_profile.pure_c_nonzero - pullback_q_profile.pure_c_nonzero,
        missing_mixed_characters=true_q_profile.mixed_nonzero - pullback_q_profile.mixed_nonzero,
        fiber_set_size_counts=set_size_counts,
        selected_fiber_counts=selected_fiber_counts,
        c_kummer_degree_gap=(
            ("D_segment", d_profile.c_c13_min_degree, d_profile.c_c169_min_degree),
            ("bridge_edge", t_profile.c_c13_min_degree, t_profile.c_c169_min_degree),
        ),
    )
    return profile, true_candidate, pullback_candidate


def main() -> int:
    print("p25 Lane B square-axis bridge C13 descent/lift gate")
    print(
        f"source_group=C_{RIGHT_ORDER}xC_{C_ORDER} "
        f"C13_shadow_group=C_{RIGHT_ORDER}xC_13 "
        f"base={BASE_POINT} K={KERNEL_SHIFT} D={D_SHIFT} T={BRIDGE_SHIFT}"
    )
    profile, true_candidate, pullback_candidate = profile_c13_descent()
    row_ok = (
        profile.full_support == 150
        and profile.projected_support == 150
        and profile.projected_degree == 0
        and profile.projected_coefficient_counts == ((-1, 75), (1, 75))
        and profile.projected_factor_word_matches
        and true_candidate.ok
        and profile.true_raw_support == 150
        and profile.pullback_raw_support == 1950
        and profile.pullback_quotient_support == 78
        and not profile.pullback_trace_correct
        and profile.pullback_kernel_modes == (0,)
        and profile.pullback_raw_relation_mismatches == 0
        and not pullback_candidate.ok
        and profile.pullback_pure_c_characters == 12
        and profile.pullback_mixed_characters == 24
        and profile.missing_pure_c_characters == 156
        and profile.missing_mixed_characters == 312
        and profile.fiber_set_size_counts == ((1, 150),)
        and profile.selected_fiber_counts == ((1, 25), (2, 50), (10, 50), (11, 25))
        and profile.c_kummer_degree_gap == (("D_segment", 13, 169), ("bridge_edge", 13, 169))
    )

    print(f"c13_descent_profile={profile}")
    print(f"true_candidate={true_candidate}")
    print(f"naive_pullback_candidate={pullback_candidate}")
    print("descent_laws")
    print("  reducing C_169 logs modulo 13 preserves the 150-cell signed formal product")
    print("  naive pullback of that C13 shadow has 1950 raw cells and 78 quotient cells")
    print("  naive pullback is kernel-trivial and satisfies raw D^3=Y, but fails the signed bridge trace")
    print("  naive pullback has only lifted C13 characters: 12 pure C and 24 mixed")
    print("  true C169 bridge adds 156 pure C and 312 mixed non-lifted characters")
    print("interpretation")
    print("  c13_shadow_is_a_valid_low_degree_shadow_but_not_the_c169_bridge=1")
    print("  bridge_arithmetic_realization_must_select_one_c169_fiber_over_each_c13_shadow_point=1")
    print("  cheap_c13_kummer_descent_does_not_replace_the_c169_fiber_lift=1")
    print("  naive_pullback_is_a_kernel_trivial_raw_relation_solution_but_not_a_producer=1")
    print(f"square_axis_bridge_c13_descent_lift_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_c13_descent_lift_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
