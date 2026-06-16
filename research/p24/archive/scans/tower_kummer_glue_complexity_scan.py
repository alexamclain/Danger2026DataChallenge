#!/usr/bin/env python3
"""Complexity scan for cross-orbit Kummer glue invariants.

For a prime relative child layer of degree r, with relative traces

    T_s(u) = sum_v zeta_r^(s*v) y_{u+a*v},

the multi-orbit Kummer repair uses glue invariants

    G_a(u) = T_a(u) / T_1(u)^a

for one representative a of each primitive-character Frobenius orbit other
than the orbit of 1.  These are invariant under a global cyclic relabeling of
the child fiber and, together with the Kummer powers, select the unordered
child polynomial in the finite glue gate.

This scan asks whether the glue invariants are low-complexity functions of the
parent period in small actual-CM towers.  A low-degree pattern would suggest a
producer theorem; full interpolation degree means the glue is the right finite
payload but not a cheap parent-period formula.
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
    FpE,
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
class GlueRow:
    D: int
    q: int
    ell: int
    h: int
    parent_count: int
    child_factor: int
    recovery_size: int
    zeta_degree: int
    primitive_orbits: int
    glue_representatives: tuple[int, ...]
    parent_distinct: bool
    fine_distinct: bool
    zero_denominators: int
    coordinate_slots: int
    full_degree_coordinates: int
    low_degree_coordinates: int
    max_interp_degree: int
    avg_interp_degree: float
    low_bm_coordinates: int
    max_bm: int
    avg_bm: float
    glue_values: int
    zero_glue_values: int
    full_frobenius_degree_glue_values: int
    proper_frobenius_descent_glue_values: int
    max_glue_frobenius_degree: int


def q_orbits_mod_prime(r: int, q: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(1, r):
        if start in seen:
            continue
        orbit: list[int] = []
        current = start
        while current not in seen:
            seen.add(current)
            orbit.append(current)
            current = (current * q) % r
        orbits.append(orbit)
    return orbits


def relative_traces(
    field: ExtensionField,
    zeta: FpE,
    children: list[int],
    r: int,
) -> list[FpE]:
    traces: list[FpE] = [field.zero for _ in range(r)]
    for s in range(1, r):
        value = field.zero
        for v, child in enumerate(children):
            value = field.add(
                value,
                field.scalar_mul(child, field.pow(zeta, (s * v) % r)),
            )
        traces[s] = value
    return traces


def minimal_frobenius_degree(field: ExtensionField, value: FpE) -> int:
    """Return least d | [field:F_q] with value^(q^d)=value."""
    for divisor in sp.divisors(field.degree):
        d = int(divisor)
        if field.pow(value, field.q**d) == value:
            return d
    return field.degree


def audit_glue_chain(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    parent_count: int,
    child_factor: int,
    seed: int,
) -> GlueRow:
    h = len(cycle)
    quotient_size = parent_count * child_factor
    recovery_size = h // quotient_size
    parents = parent_periods(cycle, q, parent_count)
    fine = fine_periods(cycle, q, quotient_size, recovery_size)

    zeta_degree = int(sp.n_order(q % child_factor, child_factor))
    orbits = q_orbits_mod_prime(child_factor, q)
    representatives = tuple(orbit[0] for orbit in orbits[1:])
    modulus = find_irreducible_modulus(q, zeta_degree, seed + 31 * child_factor)
    field = ExtensionField(q, zeta_degree, modulus)
    zeta = primitive_root_of_order(field, child_factor, seed + 97 * child_factor)

    values_by_key: dict[tuple[int, int], list[int]] = {
        (rep, coord): []
        for rep in representatives
        for coord in range(zeta_degree)
    }
    glue_frobenius_degrees: list[int] = []
    zero_glue_values = 0
    zero_denominators = 0
    for u in range(parent_count):
        children = [fine[u + parent_count * v] for v in range(child_factor)]
        traces = relative_traces(field, zeta, children, child_factor)
        base = traces[1]
        if base == field.zero:
            zero_denominators += 1
            continue
        for rep in representatives:
            glue = field.div(traces[rep], field.pow(base, rep))
            if glue == field.zero:
                zero_glue_values += 1
            glue_frobenius_degrees.append(minimal_frobenius_degree(field, glue))
            for coord, value in enumerate(glue):
                values_by_key[(rep, coord)].append(value)

    degrees: list[int] = []
    bms: list[int] = []
    usable = (
        len(set(parents)) == parent_count
        and zero_denominators == 0
        and bool(representatives)
    )
    if usable:
        for values in values_by_key.values():
            degrees.append(interpolate_degree(parents, values, q))
            bms.append(bm_linear_complexity(values * 2, q))

    full_degree = parent_count - 1
    low_degree_limit = max(0, parent_count // 2)
    low_bm_limit = max(1, parent_count // 2)
    return GlueRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        parent_count=parent_count,
        child_factor=child_factor,
        recovery_size=recovery_size,
        zeta_degree=zeta_degree,
        primitive_orbits=len(orbits),
        glue_representatives=representatives,
        parent_distinct=len(set(parents)) == parent_count,
        fine_distinct=len(set(fine)) == quotient_size,
        zero_denominators=zero_denominators,
        coordinate_slots=len(degrees),
        full_degree_coordinates=sum(degree == full_degree for degree in degrees),
        low_degree_coordinates=sum(degree <= low_degree_limit for degree in degrees),
        max_interp_degree=max(degrees, default=-1),
        avg_interp_degree=sum(degrees) / len(degrees) if degrees else -1,
        low_bm_coordinates=sum(bm <= low_bm_limit for bm in bms),
        max_bm=max(bms, default=-1),
        avg_bm=sum(bms) / len(bms) if bms else -1,
        glue_values=len(glue_frobenius_degrees),
        zero_glue_values=zero_glue_values,
        full_frobenius_degree_glue_values=sum(
            degree == zeta_degree for degree in glue_frobenius_degrees
        ),
        proper_frobenius_descent_glue_values=sum(
            degree < zeta_degree for degree in glue_frobenius_degrees
        ),
        max_glue_frobenius_degree=max(glue_frobenius_degrees, default=-1),
    )


def scan(args: argparse.Namespace) -> list[GlueRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -args.max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[GlueRow] = []
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
                primitive_orbits = (child_factor - 1) // zeta_degree
                if primitive_orbits <= 1:
                    continue
                if zeta_degree > args.max_zeta_degree:
                    continue
                rows.append(
                    audit_glue_chain(
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


def print_row(row: GlueRow) -> None:
    reps = ",".join(str(rep) for rep in row.glue_representatives)
    print(
        f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
        f"a={row.parent_count:3d} r={row.child_factor:3d} n={row.recovery_size:3d} "
        f"zeta_deg={row.zeta_degree:2d} orbit_count={row.primitive_orbits:2d} "
        f"glue_reps=[{reps}] "
        f"parent_distinct={int(row.parent_distinct)} fine_distinct={int(row.fine_distinct)} "
        f"zero_denoms={row.zero_denominators:2d} "
        f"full_deg_coords={row.full_degree_coordinates:4d}/{row.coordinate_slots:4d} "
        f"low_deg_coords={row.low_degree_coordinates:4d} "
        f"max_deg={row.max_interp_degree:3d} avg_deg={row.avg_interp_degree:6.2f} "
        f"low_bm_coords={row.low_bm_coordinates:4d} "
        f"max_bm={row.max_bm:3d} avg_bm={row.avg_bm:6.2f} "
        f"glue_frob_full={row.full_frobenius_degree_glue_values:3d}/{row.glue_values:3d} "
        f"glue_frob_proper={row.proper_frobenius_descent_glue_values:3d}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=30000)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--min-quotient", type=int, default=10)
    parser.add_argument("--max-quotient", type=int, default=120)
    parser.add_argument("--min-parent", type=int, default=3)
    parser.add_argument("--max-parent", type=int, default=50)
    parser.add_argument("--min-child", type=int, default=5)
    parser.add_argument("--max-child", type=int, default=17)
    parser.add_argument("--max-zeta-degree", type=int, default=8)
    parser.add_argument("--min-recovery", type=int, default=2)
    parser.add_argument("--max-rows-per-case", type=int, default=8)
    parser.add_argument("--summary-only", action="store_true")
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    rows = scan(args)
    print("tower Kummer cross-orbit glue complexity scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_zeta_degree={args.max_zeta_degree}")
    print()

    if not args.summary_only:
        print("columns: D q ell h a(parent) r(child) n(recovery) glue coordinate degrees/BM")
        for row in rows:
            print_row(row)
        print()

    good = [
        row
        for row in rows
        if row.parent_distinct and row.fine_distinct and row.zero_denominators == 0
    ]
    coordinate_slots = sum(row.coordinate_slots for row in good)
    full_coords = sum(row.full_degree_coordinates for row in good)
    low_coords = sum(row.low_degree_coordinates for row in good)
    low_bm = sum(row.low_bm_coordinates for row in good)
    glue_values = sum(row.glue_values for row in good)
    zero_glue_values = sum(row.zero_glue_values for row in good)
    full_frob_glue_values = sum(
        row.full_frobenius_degree_glue_values for row in good
    )
    proper_frob_glue_values = sum(
        row.proper_frobenius_descent_glue_values for row in good
    )
    nonsplit_good = [row for row in good if row.zeta_degree > 1]
    nonsplit_glue_values = sum(row.glue_values for row in nonsplit_good)
    nonsplit_full_frob_glue_values = sum(
        row.full_frobenius_degree_glue_values for row in nonsplit_good
    )
    nonsplit_proper_frob_glue_values = sum(
        row.proper_frobenius_descent_glue_values for row in nonsplit_good
    )
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  good_distinct_nonzero_rows={len(good)}")
    print(f"  glue_coordinate_slots={coordinate_slots}")
    print(f"  full_degree_coordinates={full_coords}")
    print(f"  low_degree_coordinates={low_coords}")
    print(f"  low_bm_coordinates={low_bm}")
    print(f"  glue_values={glue_values}")
    print(f"  zero_glue_values={zero_glue_values}")
    print(f"  full_frobenius_degree_glue_values={full_frob_glue_values}")
    print(f"  proper_frobenius_descent_glue_values={proper_frob_glue_values}")
    print(f"  nonsplit_glue_values={nonsplit_glue_values}")
    print(
        "  nonsplit_full_frobenius_degree_glue_values="
        f"{nonsplit_full_frob_glue_values}"
    )
    print(
        "  nonsplit_proper_frobenius_descent_glue_values="
        f"{nonsplit_proper_frob_glue_values}"
    )
    print(
        "  zero_denominator_rows="
        f"{sum(1 for row in rows if row.zero_denominators > 0)}"
    )
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
    print("  glue_invariants_are_needed_for_multi_orbit_Kummer_child_selection=1")
    print("  low_degree_glue_coordinates_would_suggest_a_formulaic_phase_glue=1")
    print("  full_degree_glue_coordinates_mean_glue_is_payload_not_parent_formula=1")
    print("  proper_frobenius_descent_would_reduce_base_field_glue_slots=1")
    print("conclusion=reported_tower_kummer_glue_complexity_scan")


if __name__ == "__main__":
    main()
