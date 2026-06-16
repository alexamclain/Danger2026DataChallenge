#!/usr/bin/env python3
"""Complexity scan for relative Kummer powers in embedded CM towers.

For a tower slice with

    h = a * r * n

where `r` is a prime child degree, form fine periods `y_{u+a*v}` over a
parent period `Z_u`.  With a primitive `r`th root of unity, define

    T_s(u) = sum_v zeta_r^(s*v) y_{u+a*v},
    K_s(u) = T_s(u)^r.

The Kummer powers are invariant under cyclic relabeling of the children.  In a
one-Frobenius-orbit relative layer they are equivalent to the unordered child
polynomial once the parent trace is known.  In multi-orbit layers they also
need cross-orbit phase glue.  This scan asks whether these Kummer powers are
low-complexity functions of the parent period in small CM towers.

It is theorem-lab only: a low-degree pattern would suggest a producer theorem;
full interpolation degree means Kummer is a cleaner normal form for the same
hard relative phase.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import (
    bm_linear_complexity,
    find_full_cycle_prime,
    find_splitting_prime,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from tower_phase_coefficient_complexity_scan import (
    divisors_between,
    fine_periods,
    interpolate_degree,
    parent_periods,
)


@dataclass(frozen=True)
class KummerRow:
    D: int
    q: int
    ell: int
    h: int
    parent_count: int
    child_factor: int
    recovery_size: int
    zeta_degree: int
    parent_distinct: bool
    fine_distinct: bool
    coordinate_slots: int
    full_degree_coordinates: int
    low_degree_coordinates: int
    max_interp_degree: int
    avg_interp_degree: float
    low_bm_coordinates: int
    max_bm: int
    avg_bm: float


def audit_kummer_chain(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    parent_count: int,
    child_factor: int,
    seed: int,
) -> KummerRow:
    h = len(cycle)
    quotient_size = parent_count * child_factor
    recovery_size = h // quotient_size
    parents = parent_periods(cycle, q, parent_count)
    fine = fine_periods(cycle, q, quotient_size, recovery_size)

    zeta_degree = int(sp.n_order(q % child_factor, child_factor))
    modulus = find_irreducible_modulus(q, zeta_degree, seed + 17 * child_factor)
    field = ExtensionField(q, zeta_degree, modulus)
    zeta = primitive_root_of_order(field, child_factor, seed)

    # values_by_key[(s, coord)] = [coordinate over parents]
    values_by_key: dict[tuple[int, int], list[int]] = {
        (s, coord): []
        for s in range(1, child_factor)
        for coord in range(zeta_degree)
    }
    for u in range(parent_count):
        children = [fine[u + parent_count * v] for v in range(child_factor)]
        for s in range(1, child_factor):
            trace = field.zero
            for v, child in enumerate(children):
                term = field.scalar_mul(
                    child,
                    field.pow(zeta, (s * v) % child_factor),
                )
                trace = field.add(trace, term)
            kummer = field.pow(trace, child_factor)
            for coord, value in enumerate(kummer):
                values_by_key[(s, coord)].append(value)

    degrees: list[int] = []
    bms: list[int] = []
    if len(set(parents)) == parent_count:
        for values in values_by_key.values():
            degrees.append(interpolate_degree(parents, values, q))
            bms.append(bm_linear_complexity(values * 2, q))

    full_degree = parent_count - 1
    low_degree_limit = max(0, parent_count // 2)
    low_bm_limit = max(1, parent_count // 2)
    return KummerRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        parent_count=parent_count,
        child_factor=child_factor,
        recovery_size=recovery_size,
        zeta_degree=zeta_degree,
        parent_distinct=len(set(parents)) == parent_count,
        fine_distinct=len(set(fine)) == quotient_size,
        coordinate_slots=len(degrees),
        full_degree_coordinates=sum(degree == full_degree for degree in degrees),
        low_degree_coordinates=sum(degree <= low_degree_limit for degree in degrees),
        max_interp_degree=max(degrees, default=-1),
        avg_interp_degree=sum(degrees) / len(degrees) if degrees else -1,
        low_bm_coordinates=sum(bm <= low_bm_limit for bm in bms),
        max_bm=max(bms, default=-1),
        avg_bm=sum(bms) / len(bms) if bms else -1,
    )


def scan(args: argparse.Namespace) -> list[KummerRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -args.max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[KummerRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        split = find_splitting_prime(pari, hilbert, h, args.q_start, args.q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        case_rows = 0
        for quotient_size in divisors_between(h, args.min_quotient, args.max_quotient):
            if quotient_size == h:
                continue
            recovery_size = h // quotient_size
            if recovery_size < args.min_recovery:
                continue
            for child_factor in divisors_between(quotient_size, args.min_child, args.max_child):
                if child_factor == quotient_size or not sp.isprime(child_factor):
                    continue
                parent_count = quotient_size // child_factor
                if not (args.min_parent <= parent_count <= args.max_parent):
                    continue
                zeta_degree = int(sp.n_order(q % child_factor, child_factor))
                if zeta_degree > args.max_zeta_degree:
                    continue
                rows.append(
                    audit_kummer_chain(
                        D,
                        q,
                        ell,
                        cycle,
                        parent_count,
                        child_factor,
                        args.seed,
                    )
                )
                case_rows += 1
                if case_rows >= args.max_rows_per_case:
                    break
            if case_rows >= args.max_rows_per_case:
                break
        if case_rows:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def print_row(row: KummerRow) -> None:
    print(
        f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
        f"a={row.parent_count:3d} r={row.child_factor:3d} n={row.recovery_size:3d} "
        f"zeta_deg={row.zeta_degree:2d} "
        f"parent_distinct={int(row.parent_distinct)} fine_distinct={int(row.fine_distinct)} "
        f"full_deg_coords={row.full_degree_coordinates:4d}/{row.coordinate_slots:4d} "
        f"low_deg_coords={row.low_degree_coordinates:4d} "
        f"max_deg={row.max_interp_degree:3d} avg_deg={row.avg_interp_degree:6.2f} "
        f"low_bm_coords={row.low_bm_coordinates:4d} "
        f"max_bm={row.max_bm:3d} avg_bm={row.avg_bm:6.2f}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=12)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--min-quotient", type=int, default=6)
    parser.add_argument("--max-quotient", type=int, default=90)
    parser.add_argument("--min-parent", type=int, default=3)
    parser.add_argument("--max-parent", type=int, default=40)
    parser.add_argument("--min-child", type=int, default=2)
    parser.add_argument("--max-child", type=int, default=13)
    parser.add_argument("--max-zeta-degree", type=int, default=12)
    parser.add_argument("--min-recovery", type=int, default=2)
    parser.add_argument("--max-rows-per-case", type=int, default=10)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("tower Kummer phase complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_zeta_degree={args.max_zeta_degree}")
    print()

    if not args.summary_only:
        print("columns: D q ell h a(parent) r(child) n(recovery) Kummer coordinate degrees/BM")
        for row in rows:
            print_row(row)
        print()

    good = [row for row in rows if row.parent_distinct and row.fine_distinct]
    coordinate_slots = sum(row.coordinate_slots for row in good)
    full_coords = sum(row.full_degree_coordinates for row in good)
    low_coords = sum(row.low_degree_coordinates for row in good)
    low_bm = sum(row.low_bm_coordinates for row in good)
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  good_distinct_rows={len(good)}")
    print(f"  kummer_coordinate_slots={coordinate_slots}")
    print(f"  full_degree_coordinates={full_coords}")
    print(f"  low_degree_coordinates={low_coords}")
    print(f"  low_bm_coordinates={low_bm}")
    print(
        "  max_interp_degree_seen="
        f"{max((row.max_interp_degree for row in good), default=-1)}"
    )
    print(
        "  avg_interp_degree_over_rows="
        f"{sum(row.avg_interp_degree for row in good) / len(good) if good else -1:.6f}"
    )
    print()
    print("interpretation")
    print("  Kummer_coordinates_are_coordinates_of_T_s_to_child_degree=1")
    print("  low_degree_coordinates_would_suggest_a_formulaic_Kummer_phase=1")
    print("  full_degree_coordinates_mean_Kummer_is_a_normal_form_not_a_collapse=1")
    print("conclusion=reported_tower_kummer_phase_complexity_scan")


if __name__ == "__main__":
    main()
