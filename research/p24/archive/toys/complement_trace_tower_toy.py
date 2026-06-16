#!/usr/bin/env python3
"""Tower decomposition of complement-trace recovery in a small CM cycle."""

from __future__ import annotations

import argparse
import math

import sympy as sp

from complement_trace_recovery_toy import (
    J,
    Y,
    find_case,
    inv_mod,
    lagrange_interpolate,
)


def trace_values_at_subgroup(cycle: list[int], q: int, m: int, subgroup_size: int) -> dict[tuple[int, int], int]:
    """Trace over subgroup of K=<g^n> of order subgroup_size.

    Keys are (a,k), where a indexes cosets in K/K_s and k indexes H.
    """
    h = len(cycle)
    n = h // m
    if m % subgroup_size:
        raise ValueError("subgroup_size must divide m")
    cosets = m // subgroup_size
    out: dict[tuple[int, int], int] = {}
    for a in range(cosets):
        for k in range(n):
            total = 0
            for r in range(subgroup_size):
                total += cycle[(n * (a + cosets * r) + m * k) % h]
            out[(a, k)] = total % q
    return out


def monic_poly_from_roots(roots: list[int], q: int) -> sp.Poly:
    poly = sp.Poly(1, J, modulus=q)
    for root in roots:
        poly *= sp.Poly(J - root, J, modulus=q)
    return poly.monic()


def interpolate_child_relation(
    parent_values: dict[tuple[int, int], int],
    child_values: dict[tuple[int, int], int],
    q: int,
    m: int,
    parent_size: int,
    child_size: int,
) -> tuple[int, int, int, bool]:
    """Interpolate degree parent_size/child_size child polynomial over parent values."""
    factor = parent_size // child_size
    parent_cosets = m // parent_size
    child_cosets = m // child_size
    parent_points: list[tuple[int, sp.Poly]] = []
    for parent_a in range(parent_cosets):
        for k in sorted(k for a, k in parent_values if a == parent_a):
            base = parent_values[(parent_a, k)]
            roots: list[int] = []
            for b in range(factor):
                child_a = parent_a + parent_cosets * b
                if child_a >= child_cosets:
                    raise AssertionError((parent_a, child_a, child_cosets))
                roots.append(child_values[(child_a, k)])
            parent_points.append((base, monic_poly_from_roots(roots, q)))

    if len({value for value, _poly in parent_points}) != len(parent_points):
        raise ValueError("parent values collide; cannot use one-variable interpolation")

    coeff_tables: list[list[tuple[int, int]]] = [[] for _ in range(factor)]
    for y_value, poly in parent_points:
        coeffs = [0] * (factor + 1)
        for (degree,), coeff in poly.as_dict().items():
            coeffs[degree] = int(coeff) % q
        if coeffs[factor] != 1:
            raise AssertionError("child polynomial is not monic")
        for degree in range(factor):
            coeff_tables[degree].append((y_value, coeffs[degree]))

    coeff_polys = [lagrange_interpolate(table, q) for table in coeff_tables]
    ok = True
    for y_value, expected in parent_points:
        reconstructed = sp.Poly(J**factor, J, modulus=q)
        for degree, coeff_poly in enumerate(coeff_polys):
            reconstructed += sp.Poly((int(coeff_poly.eval(y_value)) % q) * J**degree, J, modulus=q)
        if reconstructed.monic() != expected:
            ok = False
            break

    nonzero_terms = sum(len(poly.as_dict()) for poly in coeff_polys)
    dense_slots = factor * len(parent_points)
    degree_y_max = max(poly.degree() for poly in coeff_polys)
    return degree_y_max, nonzero_terms, dense_slots, ok


def factor_chain(m: int) -> list[int]:
    factors: list[int] = []
    for prime, exp in sp.factorint(m).items():
        factors.extend([int(prime)] * int(exp))
    return factors


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--D", type=int, default=-5000)
    ap.add_argument("--m", type=int, default=6)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=200000)
    args = ap.parse_args()

    D, q, ell, cycle = find_case(
        D=args.D,
        q_start=args.q_start,
        q_stop=args.q_stop,
        min_h=12,
        max_h=120,
        max_abs_D=20000,
        preferred_m=args.m,
    )
    h = len(cycle)
    m = args.m
    n = h // m
    chain = factor_chain(m)

    print("complement trace tower toy")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"factor_chain={chain}")
    print()
    print("level parent_size child_size factor parents deg_y_max nonzero_terms dense_slots density ok")

    total_terms = 0
    total_slots = 0
    parent_size = m
    parent_values = trace_values_at_subgroup(cycle, q, m, parent_size)
    for level, factor in enumerate(chain, start=1):
        child_size = parent_size // factor
        child_values = trace_values_at_subgroup(cycle, q, m, child_size)
        degree_y_max, nonzero_terms, dense_slots, ok = interpolate_child_relation(
            parent_values,
            child_values,
            q,
            m,
            parent_size,
            child_size,
        )
        parents = len(parent_values)
        total_terms += nonzero_terms
        total_slots += dense_slots
        density = nonzero_terms / dense_slots
        print(
            f"{level:5d} {parent_size:11d} {child_size:10d} {factor:6d} "
            f"{parents:7d} {degree_y_max:9d} {nonzero_terms:13d} "
            f"{dense_slots:11d} {density:7.3f} {int(ok):2d}"
        )
        parent_size = child_size
        parent_values = child_values

    print()
    print("summary")
    print(f"  total_nonzero_terms={total_terms}")
    print(f"  total_dense_slots={total_slots}")
    print(f"  tower_density={total_terms / total_slots:.6f}")
    print(f"  direct_dense_slots=m*n={m*n}")
    print(f"  tower_slots_over_direct={total_slots / (m*n):.6f}")
    print()
    print("interpretation")
    print("  tower_replaces_one_degree_m_recovery_by_prime_factor_steps=1")
    print("  naive_tower_interpolation_still_has_size_comparable_to_mn=1")
    print("  useful_p24_tower_needs_formulaic_coefficients_not_dense_tables=1")
    print("conclusion=reported_complement_trace_tower_toy")


if __name__ == "__main__":
    main()
