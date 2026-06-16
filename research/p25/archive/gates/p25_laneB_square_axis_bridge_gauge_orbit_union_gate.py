#!/usr/bin/env python3
"""Half-Frobenius gauge-orbit union gate for the p25 primitive bridge.

The half-Frobenius raw-gauge gate shows how p^39 permutes the 150 raw bridge
points.  This gate asks whether a smaller p^39-stable raw fragment could
replace the full C_25 kernel trace in a sign-twist producer.

It cannot, if the fragment is supposed to pass the bridge harness.  The p^39
action splits the 150 bridge points into 15 small orbits, and every nonempty
union of those orbits is scanned.  Proper unions either expose nontrivial
kernel modes/raw relation failures, or are kernel-trivial whole quotient-pair
subbridges with support 50 or 100 and therefore fail the six-point bridge
trace.  The full 150-point bridge is the unique trace-correct, exact,
harness-acceptable p^39-gauge-stable union.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

from p25_laneB_divisor_footprint_gate import primitive_root
from p25_laneB_local_pullback_gate import P25
from p25_laneB_square_axis_bridge_candidate_harness_gate import (
    crt_source_to_raw,
    target_raw_bridge,
)
from p25_laneB_square_axis_bridge_half_frobenius_gauge_gate import multiply_coord
from p25_laneB_square_axis_bridge_raw_source_character_gate import (
    MODULUS,
    raw_source_mask,
)
from p25_laneB_square_axis_local_graph_residue_gate import (
    QUOTIENT_ORDER,
    RAW_ORDER,
)


@dataclass(frozen=True)
class GaugeOrbitProfile:
    index: int
    size: int
    q_counts: tuple[tuple[int, int], ...]
    sign_counts: tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class UnionProfile:
    raw_support: int
    quotient_support: int
    trace_correct: bool
    trace_hits: int
    block_constancy_hits: int
    kernel_modes: tuple[int, ...]
    raw_relation_mismatches: int
    target_exact: bool
    harness_ok: bool


@dataclass(frozen=True)
class GaugeOrbitUnionProfile:
    p39_raw: int
    bridge_q_values: tuple[int, ...]
    orbit_count: int
    orbit_size_histogram: tuple[tuple[int, int], ...]
    orbit_profiles: tuple[GaugeOrbitProfile, ...]
    unions_scanned: int
    exact_union_count: int
    harness_ok_union_count: int
    trace_correct_union_count: int
    kernel_trivial_union_count: int
    block_constant_union_count: int
    raw_relation_union_count: int
    proper_kernel_trivial_supports: tuple[int, ...]
    proper_kernel_trivial_quotient_supports: tuple[int, ...]
    kernel_mode_count_histogram: tuple[tuple[int, int], ...]
    quotient_support_histogram: tuple[tuple[int, int], ...]
    trace_hit_histogram_tail: tuple[tuple[int, int], ...]
    block_constancy_histogram_tail: tuple[tuple[int, int], ...]
    full_union: UnionProfile


def p39_orbits() -> tuple[tuple[tuple[int, int], ...], ...]:
    mask = raw_source_mask()
    p39 = pow(P25 % RAW_ORDER, 39, RAW_ORDER)
    unseen = set(mask)
    rows: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        start = next(iter(unseen))
        orbit: list[tuple[int, int]] = []
        point = start
        while point not in orbit:
            orbit.append(point)
            unseen.discard(point)
            point = multiply_coord(point, p39)
        rows.append(tuple(orbit))
    return tuple(sorted(rows, key=lambda orbit: (len(orbit), sorted(orbit))))


def orbit_profile(index: int, orbit: tuple[tuple[int, int], ...]) -> GaugeOrbitProfile:
    mask = raw_source_mask()
    q_counter: Counter[int] = Counter()
    sign_counter: Counter[int] = Counter()
    for coord in orbit:
        raw_index = crt_source_to_raw(*coord)
        q_counter[raw_index % QUOTIENT_ORDER] += 1
        sign_counter[mask[coord]] += 1
    return GaugeOrbitProfile(
        index=index,
        size=len(orbit),
        q_counts=tuple(sorted(q_counter.items())),
        sign_counts=tuple(sorted(sign_counter.items())),
    )


def bridge_q_values(target: list[int]) -> tuple[int, ...]:
    return tuple(
        q_value
        for q_value in range(QUOTIENT_ORDER)
        if any(target[q_value + QUOTIENT_ORDER * layer] % MODULUS for layer in range(25))
    )


def union_profile(
    union_mask: int,
    orbits: tuple[tuple[tuple[int, int], ...], ...],
    orbit_entries: tuple[tuple[tuple[int, int, int], ...], ...],
    bridge_qs: tuple[int, ...],
    target: list[int],
    zeta25: int,
) -> UnionProfile:
    q_layers = {q_value: [0] * 25 for q_value in bridge_qs}
    raw_support = 0
    for index, entries in enumerate(orbit_entries):
        if union_mask >> index & 1:
            raw_support += len(orbits[index])
            for q_value, layer, value in entries:
                q_layers[q_value][layer] = value

    quotient_support = sum(1 for values in q_layers.values() if any(values))
    bridge_block_hits = sum(1 for values in q_layers.values() if len(set(values)) == 1)
    block_constancy_hits = QUOTIENT_ORDER - len(bridge_qs) + bridge_block_hits

    trace_hits = QUOTIENT_ORDER - len(bridge_qs)
    for q_value, values in q_layers.items():
        total = sum(values) % MODULUS
        expected = sum(
            target[q_value + QUOTIENT_ORDER * layer]
            for layer in range(25)
        ) % MODULUS
        trace_hits += int(total == expected)
    trace_correct = trace_hits == QUOTIENT_ORDER

    kernel_modes: set[int] = set()
    for mode in range(25):
        for values in q_layers.values():
            total = 0
            for layer, value in enumerate(values):
                total = (
                    total
                    + value * pow(zeta25, (-mode * layer) % 25, MODULUS)
                ) % MODULUS
            if total:
                kernel_modes.add(mode)
                break

    relation_mismatches = 0
    for values in q_layers.values():
        for layer, value in enumerate(values):
            relation_mismatches += int(values[(layer + 1) % 25] != value)

    target_exact = raw_support == 150 and trace_correct
    harness_ok = (
        target_exact
        and quotient_support == 6
        and block_constancy_hits == QUOTIENT_ORDER
        and tuple(sorted(kernel_modes)) == (0,)
        and relation_mismatches == 0
    )
    return UnionProfile(
        raw_support=raw_support,
        quotient_support=quotient_support,
        trace_correct=trace_correct,
        trace_hits=trace_hits,
        block_constancy_hits=block_constancy_hits,
        kernel_modes=tuple(sorted(kernel_modes)),
        raw_relation_mismatches=relation_mismatches,
        target_exact=target_exact,
        harness_ok=harness_ok,
    )


def profile_gauge_orbit_unions() -> GaugeOrbitUnionProfile:
    target = target_raw_bridge()
    bridge_qs = bridge_q_values(target)
    mask = raw_source_mask()
    orbits = p39_orbits()
    orbit_profiles = tuple(
        orbit_profile(index, orbit)
        for index, orbit in enumerate(orbits)
    )
    orbit_entries: list[tuple[tuple[int, int, int], ...]] = []
    for orbit in orbits:
        entries: list[tuple[int, int, int]] = []
        for coord in orbit:
            raw_index = crt_source_to_raw(*coord)
            entries.append((raw_index % QUOTIENT_ORDER, raw_index // QUOTIENT_ORDER, mask[coord]))
        orbit_entries.append(tuple(entries))

    root = primitive_root(MODULUS)
    zeta25 = pow(root, (MODULUS - 1) // 25, MODULUS)

    exact_count = 0
    ok_count = 0
    trace_count = 0
    kernel_trivial_count = 0
    block_count = 0
    relation_count = 0
    proper_kernel_supports: set[int] = set()
    proper_kernel_q_supports: set[int] = set()
    mode_hist: Counter[int] = Counter()
    q_hist: Counter[int] = Counter()
    trace_hist: Counter[int] = Counter()
    block_hist: Counter[int] = Counter()
    full_mask = (1 << len(orbits)) - 1
    full_profile: UnionProfile | None = None
    for union_mask in range(1, 1 << len(orbits)):
        row = union_profile(
            union_mask,
            orbits,
            tuple(orbit_entries),
            bridge_qs,
            target,
            zeta25,
        )
        exact_count += int(row.target_exact)
        ok_count += int(row.harness_ok)
        trace_count += int(row.trace_correct)
        kernel_trivial = row.kernel_modes == (0,)
        kernel_trivial_count += int(kernel_trivial)
        block_count += int(row.block_constancy_hits == QUOTIENT_ORDER)
        relation_count += int(row.raw_relation_mismatches == 0)
        if kernel_trivial and union_mask != full_mask:
            proper_kernel_supports.add(row.raw_support)
            proper_kernel_q_supports.add(row.quotient_support)
        mode_hist[len(row.kernel_modes)] += 1
        q_hist[row.quotient_support] += 1
        trace_hist[row.trace_hits] += 1
        block_hist[row.block_constancy_hits] += 1
        if union_mask == full_mask:
            full_profile = row

    if full_profile is None:
        raise AssertionError("full bridge union was not scanned")
    return GaugeOrbitUnionProfile(
        p39_raw=pow(P25 % RAW_ORDER, 39, RAW_ORDER),
        bridge_q_values=bridge_qs,
        orbit_count=len(orbits),
        orbit_size_histogram=tuple(sorted(Counter(len(orbit) for orbit in orbits).items())),
        orbit_profiles=orbit_profiles,
        unions_scanned=(1 << len(orbits)) - 1,
        exact_union_count=exact_count,
        harness_ok_union_count=ok_count,
        trace_correct_union_count=trace_count,
        kernel_trivial_union_count=kernel_trivial_count,
        block_constant_union_count=block_count,
        raw_relation_union_count=relation_count,
        proper_kernel_trivial_supports=tuple(sorted(proper_kernel_supports)),
        proper_kernel_trivial_quotient_supports=tuple(sorted(proper_kernel_q_supports)),
        kernel_mode_count_histogram=tuple(sorted(mode_hist.items())),
        quotient_support_histogram=tuple(sorted(q_hist.items())),
        trace_hit_histogram_tail=tuple(sorted(trace_hist.items())[-4:]),
        block_constancy_histogram_tail=tuple(sorted(block_hist.items())[-4:]),
        full_union=full_profile,
    )


def main() -> int:
    print("p25 Lane B square-axis bridge gauge-orbit union gate")
    profile = profile_gauge_orbit_unions()
    expected_orbit_sizes = ((2, 3), (4, 6), (20, 6))
    expected_mode_hist = ((1, 7), (5, 504), (25, 32256))
    expected_q_hist = ((2, 93), (4, 2883), (6, 29791))
    expected_trace_tail = ((501, 29790), (503, 2883), (505, 93), (507, 1))
    expected_block_tail = ((501, 27000), (503, 5400), (505, 360), (507, 7))
    row_ok = (
        profile.p39_raw == 2027
        and profile.bridge_q_values == (25, 138, 197, 310, 369, 482)
        and profile.orbit_count == 15
        and profile.orbit_size_histogram == expected_orbit_sizes
        and profile.unions_scanned == 32767
        and profile.exact_union_count == 1
        and profile.harness_ok_union_count == 1
        and profile.trace_correct_union_count == 1
        and profile.kernel_trivial_union_count == 7
        and profile.block_constant_union_count == 7
        and profile.raw_relation_union_count == 7
        and profile.proper_kernel_trivial_supports == (50, 100)
        and profile.proper_kernel_trivial_quotient_supports == (2, 4)
        and profile.kernel_mode_count_histogram == expected_mode_hist
        and profile.quotient_support_histogram == expected_q_hist
        and profile.trace_hit_histogram_tail == expected_trace_tail
        and profile.block_constancy_histogram_tail == expected_block_tail
        and profile.full_union == UnionProfile(
            raw_support=150,
            quotient_support=6,
            trace_correct=True,
            trace_hits=507,
            block_constancy_hits=507,
            kernel_modes=(0,),
            raw_relation_mismatches=0,
            target_exact=True,
            harness_ok=True,
        )
    )

    print(f"gauge_orbit_union_profile={profile}")
    print("orbit_laws")
    print("  p^39 splits the 150 raw bridge points into 15 orbits: 3 of size 2, 6 of size 4, 6 of size 20")
    print("  every orbit touches exactly one positive/negative quotient pair")
    print("  all 32767 nonempty p^39-gauge-stable orbit unions were scanned")
    print("union_scan_laws")
    print("  only the full 150-point union is trace-correct and target-exact")
    print("  only seven unions are kernel-trivial/block-constant/raw-relation compatible")
    print("  the six proper kernel-trivial unions are support-50 or support-100 quotient-pair subbridges")
    print("  all other proper unions expose nontrivial C25 kernel modes or raw relation failures")
    print("interpretation")
    print("  half_frobenius_gauge_stability_alone_has_small_fragments=1")
    print("  bridge_harness_acceptance_forces_the_full_C25_trace_over_all_three_pairs=1")
    print("  proper_kernel_trivial_fragments_fail_the_six_point_bridge_trace=1")
    print("  sign_local_system_candidates_must_not_replace_the_bridge_by_a_gauge_orbit_fragment=1")
    print(f"square_axis_bridge_gauge_orbit_union_rows={int(row_ok)}/1")
    print("conclusion=reported_p25_laneB_square_axis_bridge_gauge_orbit_union_gate")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
