#!/usr/bin/env python3
"""Small actual-CM audit for right-unit orbit-norm overcompression.

The p24 unit-2 route should only claim propagation of p-unit nonvanishing
under a determinant-line comparison.  It should not claim literal equality of
the printed orbit norms after a right-unit permutation.

This script checks that boundary on the pinned actual trace-GCD CM row used by
the orbit-norm miner.  In the row

    D=-13319, q=13463, right=7, q mod right=2,

Frobenius has two nonzero right orbits, and the unit 3 mod 7 swaps them.
The actual Fitting orbit norms on both omitted rows are p-units, but the
swapped norms are not literally equal.
"""

from __future__ import annotations

from collections import defaultdict
from types import SimpleNamespace

from trace_gcd_actual_cm_orbit_norm_miner import (
    OrbitSummary,
    frobenius_orbits,
    iter_matrix_rows,
    summarize_row,
)


UNIT = 3


def pinned_args() -> SimpleNamespace:
    return SimpleNamespace(
        profile="pinned",
        max_rows=1,
        max_cases=24,
        min_h=12,
        max_h=500,
        max_abs_D=80000,
        max_prime_quotients=12,
        max_composite_quotients=24,
        min_n=3,
        max_n=220,
        q_start=13463,
        q_stop=13464,
        max_splitting_primes=2,
        max_m=120,
        min_factor_degree=1,
        max_factor_degree=8,
        max_extension_degree=8,
        min_left_orbit_len=2,
        min_right_orbits=2,
        min_block_size=1,
        include_linear=True,
        require_square_tail=True,
        require_prime_right=False,
        origin_shift=0,
        max_origin_shifts=None,
        only_D=-13319,
        only_q=13463,
        only_m=28,
        only_left=4,
        only_right=7,
        only_omitted=None,
        pari_stack_mb=256,
        seed=20260605,
    )


def orbit_label_map(orbits: list[list[int]]) -> dict[int, int]:
    return {value: orbit[0] for orbit in orbits for value in orbit}


def summaries_by_omitted(summaries: list[OrbitSummary]) -> dict[int, list[OrbitSummary]]:
    out: dict[int, list[OrbitSummary]] = defaultdict(list)
    for summary in summaries:
        out[summary.omitted].append(summary)
    return dict(sorted(out.items()))


def main() -> None:
    args = pinned_args()
    rows = list(iter_matrix_rows(args))
    summaries: list[OrbitSummary] = []
    for row_index, row in enumerate(rows):
        summaries.extend(summarize_row(row_index, row, args.min_block_size))

    print("trace-GCD actual-CM unit-action falsifier")
    print(f"matrix_rows={len(rows)}")
    print(f"orbit_rows={len(summaries)}")
    if not rows:
        raise SystemExit("no pinned actual-CM row found")

    row = rows[0]
    orbits = frobenius_orbits(row.right, row.q % row.right)
    labels = orbit_label_map(orbits)
    unit_mapping = {
        orbit[0]: labels[(UNIT * orbit[0]) % row.right]
        for orbit in orbits
    }
    nonzero_cycle = [orbit[0] for orbit in orbits if orbit[0] != 0]

    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"right={row.right}")
    print(f"q_mod_right={row.q % row.right}")
    print(f"unit={UNIT}")
    print(f"frobenius_orbits={orbits}")
    print(f"unit_action_mapping={unit_mapping}")
    print(f"nonzero_orbit_reps={nonzero_cycle}")

    literal_equal_edges = 0
    punit_ratio_edges = 0
    total_edges = 0
    for omitted, group in summaries_by_omitted(summaries).items():
        norms = {summary.orbit_rep: summary.orbit_norm for summary in group}
        print(f"omitted={omitted}")
        print(f"  norm_by_orbit_rep={norms}")
        for source in nonzero_cycle:
            target = unit_mapping[source]
            source_norm = norms[source] % row.q
            target_norm = norms[target] % row.q
            literal_equal = source_norm == target_norm
            punit_ratio = source_norm != 0 and target_norm != 0
            ratio = target_norm * pow(source_norm, -1, row.q) % row.q
            literal_equal_edges += int(literal_equal)
            punit_ratio_edges += int(punit_ratio)
            total_edges += 1
            print(
                f"  unit_edge={source}->{target} "
                f"source_norm={source_norm} target_norm={target_norm} "
                f"literal_equal={int(literal_equal)} "
                f"punit_ratio={int(punit_ratio)} ratio={ratio}"
            )

    print("totals")
    print(f"  literal_equal_edges={literal_equal_edges}/{total_edges}")
    print(f"  punit_ratio_edges={punit_ratio_edges}/{total_edges}")
    print("interpretation")
    print("  actual CM data falsifies literal unit-invariance of printed norms.")
    print("  it remains compatible with determinant-line equivariance up to p-unit scale.")
    print("  the p24 theorem must prove p-unit transition factors, not equal scalars.")
    print("conclusion=reported_trace_gcd_actual_cm_unit_action_falsifier")
    if literal_equal_edges:
        raise SystemExit(1)
    if punit_ratio_edges != total_edges:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
