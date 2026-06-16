#!/usr/bin/env python3
"""Two-resultant holdout audit for the trace-GCD certificate surface.

The p24 theorem target has narrowed to:

    fixed orbit p-linearized resultant is a p-unit
    + one nonzero Frobenius-orbit crossed norm is a p-unit
    + diamond/unit transport preserves p-unitness.

This script tests exactly that shape on two bounded actual-CM rows already
known to produce trace-GCD tail-on-kernel records.  It is deliberately not a
row search; it is a cheap theorem microscope and false-shortcut guard.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from types import SimpleNamespace

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from lang_trace_gcd_factor_bezout_audit import dft_interpolate, is_base
from trace_gcd_actual_cm_norm_triangle_audit import base_value, field_product
from trace_gcd_actual_cm_orbit_norm_miner import (
    OrbitSummary,
    iter_matrix_rows,
    summarize_row,
)
from lang_trace_gcd_block_cycle_norm_audit import (
    class_representatives,
    frobenius_orbits,
    product_mod,
    records_by_omitted,
)


@dataclass(frozen=True)
class Case:
    label: str
    D: int
    q: int
    m: int
    left: int
    right: int
    max_h: int
    max_abs_D: int
    max_m: int
    max_n: int
    max_factor_degree: int
    max_extension_degree: int
    max_origin_shifts: int


CASES = (
    Case(
        label="pinned_D13319",
        D=-13319,
        q=13463,
        m=28,
        left=4,
        right=7,
        max_h=500,
        max_abs_D=80000,
        max_m=120,
        max_n=220,
        max_factor_degree=8,
        max_extension_degree=8,
        max_origin_shifts=140,
    ),
    Case(
        label="holdout_D26759",
        D=-26759,
        q=26903,
        m=21,
        left=3,
        right=7,
        max_h=300,
        max_abs_D=30000,
        max_m=40,
        max_n=40,
        max_factor_degree=12,
        max_extension_degree=12,
        max_origin_shifts=231,
    ),
)


def case_args(case: Case) -> SimpleNamespace:
    return SimpleNamespace(
        profile="scan",
        max_rows=1,
        max_cases=1,
        min_h=12,
        max_h=case.max_h,
        max_abs_D=case.max_abs_D,
        max_prime_quotients=20,
        max_composite_quotients=40,
        min_n=3,
        max_n=case.max_n,
        q_start=case.q,
        q_stop=case.q + 1,
        max_splitting_primes=2,
        max_m=case.max_m,
        min_factor_degree=1,
        max_factor_degree=case.max_factor_degree,
        max_extension_degree=case.max_extension_degree,
        min_left_orbit_len=2,
        min_right_orbits=2,
        min_block_size=1,
        include_linear=True,
        require_square_tail=True,
        require_prime_right=True,
        origin_shift=0,
        max_origin_shifts=case.max_origin_shifts,
        only_D=case.D,
        only_q=case.q,
        only_m=case.m,
        only_left=case.left,
        only_right=case.right,
        only_omitted=None,
        pari_stack_mb=256,
        seed=20260605,
    )


def orbit_rep_map(orbits: list[list[int]]) -> dict[int, int]:
    return {value: orbit[0] for orbit in orbits for value in orbit}


def unit_mapping(unit: int, right: int, orbits: list[list[int]]) -> dict[int, int]:
    reps = orbit_rep_map(orbits)
    return {orbit[0]: reps[(unit * orbit[0]) % right] for orbit in orbits}


def cycle_covers_nonzero(mapping: dict[int, int], nonzero_reps: list[int]) -> bool:
    if not nonzero_reps:
        return False
    start = nonzero_reps[0]
    seen: set[int] = set()
    value = start
    while value not in seen:
        seen.add(value)
        value = mapping[value]
    return value == start and sorted(seen) == sorted(nonzero_reps)


def quotient_cycle_unit(right: int, q_mod_right: int, orbits: list[list[int]]) -> int | None:
    nonzero_reps = [orbit[0] for orbit in orbits if orbit[0] != 0]
    for unit in range(2, right):
        if gcd(unit, right) != 1:
            continue
        mapping = unit_mapping(unit, right, orbits)
        if cycle_covers_nonzero(mapping, nonzero_reps):
            return unit
    return None


def summaries_by_omitted(summaries: list[OrbitSummary]) -> dict[int, list[OrbitSummary]]:
    out: dict[int, list[OrbitSummary]] = {}
    for summary in summaries:
        out.setdefault(summary.omitted, []).append(summary)
    return dict(sorted(out.items()))


def split_norm_diagnostics(row, seed: int) -> tuple[int, int, int]:
    right_order = int(sp.n_order(row.q % row.right, row.right))
    modulus = find_irreducible_modulus(row.q, right_order, seed)
    field = ExtensionField(row.q, right_order, modulus)
    root = primitive_root_of_order(field, row.right, seed)
    orbits = frobenius_orbits(row.right, row.q % row.right)

    split_norm_matches = 0
    split_norm_tests = 0
    naive_base_possible = 0
    for _omitted, records in records_by_omitted(row.records).items():
        reps, det_mismatches = class_representatives(records, row.right)
        if det_mismatches:
            continue
        seq = [int(record.determinant) for record in reps]
        coeffs = dft_interpolate(seq, root, field)
        if all(is_base(coeff) for coeff in coeffs):
            naive_base_possible += 1
        evals = []
        for index in range(row.right):
            value = field.zero
            power = field.one
            point = field.pow(root, index)
            for coeff in coeffs:
                value = field.add(value, field.mul(coeff, power))
                power = field.mul(power, point)
            evals.append(value)
        for orbit in orbits:
            scalar_product = product_mod([seq[index] for index in orbit], row.q)
            split_norm = base_value(field_product([evals[index] for index in orbit], field))
            split_norm_tests += 1
            split_norm_matches += int(split_norm == scalar_product)
    return split_norm_matches, split_norm_tests, naive_base_possible


def main() -> None:
    total_groups = 0
    selected_groups = 0
    all_nonzero_groups = 0
    transport_edges = 0
    punit_transport_edges = 0
    literal_equal_nonzero_edges = 0
    split_matches = 0
    split_tests = 0
    naive_base_possible_groups = 0
    failures = 0

    print("trace-GCD two-resultant holdout audit")
    print("p24_target=fixed_resultant_plus_one_nonzero_crossed_norm_plus_unit_transport")

    for case in CASES:
        args = case_args(case)
        rows = list(iter_matrix_rows(args))
        print(f"case={case.label}")
        print(f"  matrix_rows={len(rows)}")
        if len(rows) != 1:
            failures += 1
            continue

        row = rows[0]
        summaries: list[OrbitSummary] = summarize_row(0, row, args.min_block_size)
        orbits = frobenius_orbits(row.right, row.q % row.right)
        nonzero_reps = [orbit[0] for orbit in orbits if orbit[0] != 0]
        unit = quotient_cycle_unit(row.right, row.q % row.right, orbits)
        mapping = {} if unit is None else unit_mapping(unit, row.right, orbits)
        covers = bool(unit is not None and cycle_covers_nonzero(mapping, nonzero_reps))
        case_split_matches, case_split_tests, case_naive_base = split_norm_diagnostics(
            row,
            args.seed,
        )
        split_matches += case_split_matches
        split_tests += case_split_tests
        naive_base_possible_groups += case_naive_base

        print(f"  D={row.D}")
        print(f"  q={row.q}")
        print(f"  h={row.h}")
        print(f"  m={row.m}")
        print(f"  n={row.n}")
        print(f"  factor_degree={row.factor_degree}")
        print(f"  pair=({row.left},{row.right})")
        print(f"  right={row.right}")
        print(f"  q_mod_right={row.q % row.right}")
        print(f"  frobenius_orbits={orbits}")
        print(f"  quotient_cycle_unit={unit}")
        print(f"  quotient_cycle_covers_nonzero={int(covers)}")
        print(
            "  split_norm_matches="
            f"{case_split_matches}/{case_split_tests}"
        )
        print(f"  naive_base_polynomial_groups={case_naive_base}")

        if not covers:
            failures += 1

        for omitted, group in summaries_by_omitted(summaries).items():
            norms = {summary.orbit_rep: summary.orbit_norm for summary in group}
            selected_rep = nonzero_reps[0]
            fixed_nonzero = norms.get(0, 0) != 0
            selected_nonzero = norms.get(selected_rep, 0) != 0
            all_nonzero = all(summary.orbit_nonzero for summary in group)
            total_groups += 1
            selected_groups += int(fixed_nonzero and selected_nonzero)
            all_nonzero_groups += int(all_nonzero)
            failures += int(not (fixed_nonzero and selected_nonzero and all_nonzero))

            print(f"  omitted={omitted}")
            print(f"    orbit_norms={norms}")
            print(f"    fixed_orbit_nonzero={int(fixed_nonzero)}")
            print(f"    selected_nonzero_rep={selected_rep}")
            print(f"    selected_nonzero_norm={norms.get(selected_rep)}")
            print(f"    selected_nonzero_crossed_norm_punit={int(selected_nonzero)}")
            print(f"    all_orbit_norms_nonzero={int(all_nonzero)}")

            if unit is None:
                continue
            for source in nonzero_reps:
                target = mapping[source]
                source_norm = norms[source] % row.q
                target_norm = norms[target] % row.q
                ratio_defined = source_norm != 0 and target_norm != 0
                transport_edges += 1
                punit_transport_edges += int(ratio_defined)
                literal_equal_nonzero_edges += int(source_norm == target_norm)
                ratio = None
                if ratio_defined:
                    ratio = target_norm * pow(source_norm, -1, row.q) % row.q
                print(
                    f"    unit_edge={source}->{target} "
                    f"source_norm={source_norm} target_norm={target_norm} "
                    f"punit_ratio={int(ratio_defined)} literal_equal={int(source_norm == target_norm)} "
                    f"ratio={ratio}"
                )

    print("totals")
    print(f"  omitted_groups={total_groups}")
    print(f"  selected_two_punit_groups={selected_groups}/{total_groups}")
    print(f"  all_nonzero_groups={all_nonzero_groups}/{total_groups}")
    print(f"  punit_transport_edges={punit_transport_edges}/{transport_edges}")
    print(f"  literal_equal_nonzero_edges={literal_equal_nonzero_edges}/{transport_edges}")
    print(f"  split_norm_matches={split_matches}/{split_tests}")
    print(f"  naive_base_polynomial_groups={naive_base_possible_groups}/{total_groups}")
    print("interpretation")
    print("  positive result supports the two-resultant theorem shape on actual-CM holdouts")
    print("  literal equality remains false, so transport must be by p-unit determinant-line factors")
    print("  naive_base_polynomial_groups=0 keeps the crossed-product norm distinction alive")
    print(f"failures={failures}")
    print("conclusion=reported_trace_gcd_two_resultant_holdout_audit")
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
