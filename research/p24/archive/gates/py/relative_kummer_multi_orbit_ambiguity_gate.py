#!/usr/bin/env python3
"""Finite gate for multi-orbit relative Kummer ambiguity and glue.

For a cyclic prime-degree child layer of degree r, write

    T_s = sum_u zeta_r^(s*u) y_u,        K_s = T_s^r.

When Frobenius has one orbit on the primitive characters s=1,...,r-1,
the r root choices for one K_s are exactly cyclic relabelings of the child
fiber, so the unordered child polynomial is selected.

When Frobenius has several primitive-character orbits, however, each orbit has
its own r-th-root phase.  Frobenius compatibility alone still gives base-field
children after inverse DFT, but the independent phases need not be one global
cyclic shift.  This is the p24 211-layer shape: ord_211(p)=35, so there are
six primitive-character orbits.

The natural repair is to add cross-orbit invariants such as T_a / T_1^a.
These are unchanged by a global cyclic relabeling, but they reject independent
orbit phases.
"""

from __future__ import annotations

import argparse
from itertools import product
import random

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
    primitive_root_of_order,
)


FpE = tuple[int, ...]


def monic_poly_from_roots(roots: list[int], q: int) -> tuple[int, ...]:
    poly = [1]
    for root in roots:
        new = [0] * (len(poly) + 1)
        for i, coeff in enumerate(poly):
            new[i] = (new[i] - coeff * root) % q
            new[i + 1] = (new[i + 1] + coeff) % q
        poly = new
    return tuple(poly)


def base_value(field: ExtensionField, value: FpE) -> int | None:
    if any(coord % field.q for coord in value[1:]):
        return None
    return value[0] % field.q


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


def dft_traces(
    field: ExtensionField,
    zeta: FpE,
    children: list[int],
    r: int,
) -> list[FpE]:
    traces: list[FpE] = []
    for s in range(r):
        value = field.zero
        for u, child in enumerate(children):
            value = field.add(
                value,
                field.scalar_mul(child, field.pow(zeta, (s * u) % r)),
            )
        traces.append(value)
    return traces


def inverse_dft_children(
    field: ExtensionField,
    zeta: FpE,
    traces: list[FpE],
    r: int,
) -> list[FpE]:
    inv_r = pow(r, -1, field.q)
    children: list[FpE] = []
    for u in range(r):
        value = field.zero
        for s, trace in enumerate(traces):
            value = field.add(value, field.mul(trace, field.pow(zeta, (-s * u) % r)))
        children.append(field.scalar_mul(inv_r, value))
    return children


def shifted_trace_packet(
    field: ExtensionField,
    zeta: FpE,
    traces: list[FpE],
    r: int,
    q: int,
    orbits: list[list[int]],
    orbit_phase_exponents: tuple[int, ...],
) -> list[FpE]:
    shifted = [field.zero for _ in range(r)]
    shifted[0] = traces[0]
    for orbit, exponent_at_rep in zip(orbits, orbit_phase_exponents):
        rep = orbit[0]
        q_power = 1
        current = rep
        while True:
            shifted[current] = field.mul(
                field.pow(zeta, (exponent_at_rep * q_power) % r),
                traces[current],
            )
            q_power = (q_power * q) % r
            current = (current * q) % r
            if current == rep:
                break
    return shifted


def is_global_cyclic_shift(
    r: int,
    orbits: list[list[int]],
    orbit_phase_exponents: tuple[int, ...],
) -> bool:
    shift: int | None = None
    for orbit, exponent_at_rep in zip(orbits, orbit_phase_exponents):
        rep = orbit[0]
        candidate = exponent_at_rep * pow(rep, -1, r) % r
        if shift is None:
            shift = candidate
        elif shift != candidate:
            return False
    return True


def cross_orbit_glues(
    field: ExtensionField,
    traces: list[FpE],
    orbits: list[list[int]],
) -> tuple[FpE, ...]:
    base = traces[1]
    return tuple(
        field.div(traces[orbit[0]], field.pow(base, orbit[0]))
        for orbit in orbits[1:]
    )


def audit_case(q: int, r: int, trials: int, seed: int) -> dict[str, int]:
    degree = int(sp.n_order(q % r, r))
    modulus = find_irreducible_modulus(q, degree, seed + 31 * r)
    field = ExtensionField(q, degree, modulus)
    zeta = primitive_root_of_order(field, r, seed + 97 * r)
    orbits = q_orbits_mod_prime(r, q)
    rng = random.Random(seed + 1009 * q + 9176 * r)

    total_assignments = r ** len(orbits)
    descending_assignments = 0
    noncyclic_descending_assignments = 0
    glue_preserving_assignments = 0
    noncyclic_glue_preserving_assignments = 0
    unique_poly_counts: list[int] = []
    global_shift_poly_counts: list[int] = []
    noncyclic_poly_counts: list[int] = []
    glue_unique_poly_counts: list[int] = []
    nonzero_trace_trials = 0

    for _ in range(trials):
        for _attempt in range(200):
            children = [rng.randrange(q) for _ in range(r)]
            traces = dft_traces(field, zeta, children, r)
            if all(trace != field.zero for trace in traces[1:]):
                break
        else:
            raise RuntimeError(f"could not find nondegenerate children for q={q}, r={r}")

        nonzero_trace_trials += 1
        true_glues = cross_orbit_glues(field, traces, orbits)
        unique_polys: set[tuple[int, ...]] = set()
        global_shift_polys: set[tuple[int, ...]] = set()
        noncyclic_polys: set[tuple[int, ...]] = set()
        glue_polys: set[tuple[int, ...]] = set()
        for phases in product(range(r), repeat=len(orbits)):
            shifted = shifted_trace_packet(field, zeta, traces, r, q, orbits, phases)
            child_values = inverse_dft_children(field, zeta, shifted, r)
            base_children = [base_value(field, value) for value in child_values]
            if any(value is None for value in base_children):
                continue
            preserves_glue = cross_orbit_glues(field, shifted, orbits) == true_glues
            descending_assignments += 1
            poly = monic_poly_from_roots([int(value) for value in base_children], q)
            unique_polys.add(poly)
            if is_global_cyclic_shift(r, orbits, phases):
                global_shift_polys.add(poly)
            else:
                noncyclic_descending_assignments += 1
                noncyclic_polys.add(poly)
            if preserves_glue:
                glue_preserving_assignments += 1
                glue_polys.add(poly)
                if not is_global_cyclic_shift(r, orbits, phases):
                    noncyclic_glue_preserving_assignments += 1
        unique_poly_counts.append(len(unique_polys))
        global_shift_poly_counts.append(len(global_shift_polys))
        noncyclic_poly_counts.append(len(noncyclic_polys))
        glue_unique_poly_counts.append(len(glue_polys))

    return {
        "q": q,
        "r": r,
        "zeta_degree": degree,
        "orbit_count": len(orbits),
        "orbit_lengths_equal_degree": int(all(len(orbit) == degree for orbit in orbits)),
        "total_assignments_per_trial": total_assignments,
        "trials": trials,
        "nonzero_trace_trials": nonzero_trace_trials,
        "descending_assignments": descending_assignments,
        "noncyclic_descending_assignments": noncyclic_descending_assignments,
        "glue_preserving_assignments": glue_preserving_assignments,
        "noncyclic_glue_preserving_assignments": noncyclic_glue_preserving_assignments,
        "min_unique_polynomials": min(unique_poly_counts),
        "max_unique_polynomials": max(unique_poly_counts),
        "min_global_shift_polynomials": min(global_shift_poly_counts),
        "max_global_shift_polynomials": max(global_shift_poly_counts),
        "min_noncyclic_polynomials": min(noncyclic_poly_counts),
        "max_noncyclic_polynomials": max(noncyclic_poly_counts),
        "min_glue_unique_polynomials": min(glue_unique_poly_counts),
        "max_glue_unique_polynomials": max(glue_unique_poly_counts),
    }


def print_result(result: dict[str, int]) -> None:
    print(
        f"case q={result['q']} r={result['r']} "
        f"zeta_degree={result['zeta_degree']} orbit_count={result['orbit_count']}"
    )
    for key in (
        "orbit_lengths_equal_degree",
        "total_assignments_per_trial",
        "trials",
        "nonzero_trace_trials",
        "descending_assignments",
        "noncyclic_descending_assignments",
        "glue_preserving_assignments",
        "noncyclic_glue_preserving_assignments",
        "min_unique_polynomials",
        "max_unique_polynomials",
        "min_global_shift_polynomials",
        "max_global_shift_polynomials",
        "min_noncyclic_polynomials",
        "max_noncyclic_polynomials",
        "min_glue_unique_polynomials",
        "max_glue_unique_polynomials",
    ):
        print(f"  {key}={result[key]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    one_orbit = audit_case(q=3, r=5, trials=args.trials, seed=args.seed)
    two_orbit = audit_case(q=11, r=7, trials=args.trials, seed=args.seed + 1)
    three_orbit = audit_case(q=5, r=13, trials=args.trials, seed=args.seed + 2)

    print("relative Kummer multi-orbit ambiguity gate")
    print_result(one_orbit)
    print_result(two_orbit)
    print_result(three_orbit)
    print()
    print("p24_211_layer")
    print("  r=211")
    print("  ord_211(p)=35")
    print("  primitive_character_orbits=6")
    print(f"  independent_phase_ambiguity_after_global_shift={211**5}")
    print("  cross_orbit_glue_invariants_needed=5")
    print()
    print("interpretation")
    print(
        "  one_orbit_kummer_powers_select_child_polynomial="
        f"{int(one_orbit['max_unique_polynomials'] == 1)}"
    )
    print(
        "  multi_orbit_kummer_powers_have_noncyclic_descents="
        f"{int(two_orbit['noncyclic_descending_assignments'] > 0 and three_orbit['noncyclic_descending_assignments'] > 0)}"
    )
    print(
        "  multi_orbit_kummer_powers_do_not_select_child_polynomial="
        f"{int(two_orbit['min_unique_polynomials'] > 1 and three_orbit['min_unique_polynomials'] > 1)}"
    )
    print(
        "  cross_orbit_glue_restores_child_selection="
        f"{int(two_orbit['max_glue_unique_polynomials'] == 1 and three_orbit['max_glue_unique_polynomials'] == 1)}"
    )
    print(
        "  cross_orbit_glue_rejects_noncyclic_phases="
        f"{int(two_orbit['noncyclic_glue_preserving_assignments'] == 0 and three_orbit['noncyclic_glue_preserving_assignments'] == 0)}"
    )
    print("  p24_211_layer_needs_cross_orbit_phase_glue=1")
    print("conclusion=relative_Kummer_minpolys_need_cross_orbit_glue_for_multi_orbit_child_selection")


if __name__ == "__main__":
    main()
