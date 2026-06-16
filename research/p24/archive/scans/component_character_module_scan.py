#!/usr/bin/env python3
"""Component character-module scan inside packet fields.

For a complement component c | m, the c-axis elements are

    Y_t = sum_{r == t mod c} F_r,      0 <= t < c.

If the packet field A=F_q[X]/(f) contains mu_c, i.e.

    ord_c(q) | deg(f),

then the c-axis diagonalizes inside A:

    G_s = sum_t zeta_c^(s*t) Y_t.

This script computes the Frobenius-orbit ranks of the nontrivial character
modules.  It is a small analogue of the p24 situation where the 211-axis
diagonalizes in the degree-388430 H-packet field, while the 157-axis does not.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import coprime_components, sum_polys, zero_poly_like
from l1_axis_injectivity_scan import coeff_vector, rank_mod_q


@dataclass(frozen=True)
class ComponentModuleRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    component: int
    character_degree: int
    orbit_count: int
    zero_orbits: int
    rank_defect_orbits: int
    total_nontrivial_rank: int
    expected_nontrivial_rank: int
    internal_axis_rank: int
    internal_dimension_possible: bool


def poly_one_like(factor: sp.Poly) -> sp.Poly:
    return sp.Poly(1, factor.gens[0], modulus=factor.get_modulus())


def poly_mul(a: sp.Poly, b: sp.Poly, factor: sp.Poly) -> sp.Poly:
    return (a * b).rem(factor)


def poly_pow(base: sp.Poly, exponent: int, factor: sp.Poly) -> sp.Poly:
    result = poly_one_like(factor)
    current = base.rem(factor)
    e = exponent
    while e:
        if e & 1:
            result = poly_mul(result, current, factor)
        current = poly_mul(current, current, factor)
        e >>= 1
    return result


def poly_scale(poly: sp.Poly, coeff: sp.Poly, factor: sp.Poly) -> sp.Poly:
    return poly_mul(coeff, poly, factor)


def element_order_is(element: sp.Poly, order: int, factor: sp.Poly) -> bool:
    if not (poly_pow(element, order, factor) - poly_one_like(factor)).rem(factor).is_zero:
        return False
    for prime in sp.factorint(order):
        if (poly_pow(element, order // int(prime), factor) - poly_one_like(factor)).rem(factor).is_zero:
            return False
    return True


def primitive_root_in_packet(q: int, order: int, factor: sp.Poly) -> sp.Poly | None:
    degree = factor.degree()
    if (q**degree - 1) % order:
        return None
    x = factor.gens[0]
    exponent = (q**degree - 1) // order
    # Deterministic small search.  In tiny fields this usually succeeds fast.
    candidates = [sp.Poly(x, x, modulus=q)]
    candidates.extend(sp.Poly(x + a, x, modulus=q) for a in range(1, min(q, 64)))
    candidates.extend(sp.Poly(a, x, modulus=q) for a in range(2, min(q, 64)))
    for candidate in candidates:
        root = poly_pow(candidate, exponent, factor)
        if element_order_is(root, order, factor):
            return root
    return None


def frobenius_orbits(component: int, q: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for s in range(1, component):
        if s in seen:
            continue
        orbit: list[int] = []
        x = s
        while x not in seen:
            seen.add(x)
            orbit.append(x)
            x = (x * q) % component
        orbits.append(orbit)
    return orbits


def axis_sums(residues: list[sp.Poly], component: int, factor: sp.Poly) -> list[sp.Poly]:
    out: list[sp.Poly] = []
    for t in range(component):
        terms = [residues[r] for r in range(t, len(residues), component)]
        out.append(sum_polys(terms).rem(factor) if terms else zero_poly_like(residues[0]))
    return out


def character_values(axis: list[sp.Poly], zeta: sp.Poly, factor: sp.Poly) -> list[sp.Poly]:
    component = len(axis)
    powers = [poly_one_like(factor)]
    for _ in range(1, component):
        powers.append(poly_mul(powers[-1], zeta, factor))
    values: list[sp.Poly] = []
    for s in range(component):
        total = zero_poly_like(axis[0])
        for t, value in enumerate(axis):
            total += poly_scale(value, powers[(s * t) % component], factor)
        values.append(total.rem(factor))
    return values


def audit_component(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    component: int,
) -> ComponentModuleRow | None:
    h = len(cycle)
    n = h // m
    char_degree = int(sp.n_order(q % component, component)) if component > 1 else 1
    if factor.degree() % char_degree:
        return None
    if component > 80 or factor.degree() > 120:
        return None
    zeta = primitive_root_in_packet(q, component, factor)
    if zeta is None:
        return None
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    axis = axis_sums(residues, component, factor)
    chars = character_values(axis, zeta, factor)
    orbits = frobenius_orbits(component, q)
    zero_orbits = 0
    rank_defects = 0
    total_rank = 0
    for orbit in orbits:
        vectors = [coeff_vector(chars[s], factor.degree(), q) for s in orbit]
        rank = rank_mod_q(vectors, q)
        total_rank += rank
        if all(chars[s].is_zero for s in orbit):
            zero_orbits += 1
        if rank < len(orbit):
            rank_defects += 1
    internal_vectors = [coeff_vector(value, factor.degree(), q) for value in axis]
    return ComponentModuleRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        component=component,
        character_degree=char_degree,
        orbit_count=len(orbits),
        zero_orbits=zero_orbits,
        rank_defect_orbits=rank_defects,
        total_nontrivial_rank=total_rank,
        expected_nontrivial_rank=component - 1,
        internal_axis_rank=rank_mod_q(internal_vectors, q),
        internal_dimension_possible=factor.degree() >= component,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[ComponentModuleRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ComponentModuleRow] = []
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
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
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        if not splits:
            continue
        case_had_row = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    for component in coprime_components(m):
                        if component < args.min_component or component > args.max_component:
                            continue
                        row = audit_component(D, q, ell, cycle, m, factor, component)
                        if row is not None:
                            rows.append(row)
                            case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=40)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=160)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=160)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=4)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--min-component", type=int, default=2)
    parser.add_argument("--max-component", type=int, default=80)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    zero_rows = [row for row in rows if row.zero_orbits]
    rank_defect_rows = [row for row in rows if row.rank_defect_orbits]
    full_rows = [
        row for row in rows
        if row.total_nontrivial_rank == row.expected_nontrivial_rank
        and row.internal_axis_rank == row.component
    ]
    dimension_possible_rows = [
        row for row in rows if row.internal_dimension_possible
    ]
    dimension_bound_rows = [
        row for row in rows if not row.internal_dimension_possible
    ]
    possible_internal_failures = [
        row for row in dimension_possible_rows if row.internal_axis_rank < row.component
    ]
    by_component: dict[int, int] = {}
    for row in rows:
        by_component[row.component] = by_component.get(row.component, 0) + 1

    print("component character-module scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"component_window=[{args.min_component},{args.max_component}]")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg c char_deg orbits "
            "zero_orbits rank_defects nontriv_rank axis_rank dim_possible"
        )
        display = zero_rows + rank_defect_rows
        if not display:
            display = rows[:40]
        for row in display[:80]:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} c={row.component:3d} "
                f"char_deg={row.character_degree:3d} orbits={row.orbit_count:3d} "
                f"zero_orbits={row.zero_orbits:3d} "
                f"rank_defects={row.rank_defect_orbits:3d} "
                f"nontriv_rank={row.total_nontrivial_rank:3d}/{row.expected_nontrivial_rank:3d} "
                f"axis_rank={row.internal_axis_rank:3d}/{row.component:3d} "
                f"dim_possible={int(row.internal_dimension_possible)}"
            )
    print()
    print("summary")
    print(f"  module_rows={len(rows)}")
    print(f"  dimension_possible_rows={len(dimension_possible_rows)}")
    print(f"  dimension_bound_rows={len(dimension_bound_rows)}")
    print(f"  full_module_rows={len(full_rows)}")
    print(f"  dimension_possible_internal_failure_rows={len(possible_internal_failures)}")
    print(f"  zero_orbit_rows={len(zero_rows)}")
    print(f"  rank_defect_rows={len(rank_defect_rows)}")
    print(f"  rows_by_component={dict(sorted(by_component.items()))}")
    print()
    print("interpretation")
    print("  component_roots_live_in_packet_field_for_each_reported_row=1")
    print("  rank_defect_rows_detect_failed_frobenius_module_normality=1")
    print("  p24_211_axis_has_this_packet-field-diagonal shape=1")
    print("conclusion=reported_component_character_module_scan")


if __name__ == "__main__":
    main()
