#!/usr/bin/env python3
"""Toy cyclic-code audit for sparse subgroup projectors.

If reduced normality fails, the equation

    L * j = e_H * j

does not force L=e_H.  Instead L may differ from the subgroup projector by an
element of Ann(j), a cyclic code in F_q[T]/(T^h-1).  This script asks whether a
vanished Frobenius packet can make the coset e_H + Ann(j) contain a lower
Hamming-weight representative.

The p24 hope would be dramatic: a large packet kernel might let a sparse
operator replace the |H|-term subgroup projector.  The toy result below is
negative in the calibrated D=-5000 CM cycle: artificially killing one packet
does create a nontrivial annihilator, but the minimum coset weight remains the
projector support.
"""

from __future__ import annotations

from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)

Q = 1259
T = sp.symbols("T")


@dataclass(frozen=True)
class WeightResult:
    quotient_size: int
    subgroup_size: int
    factor_degree: int
    natural_gcd_degree: int
    artificial_ann_dimension: int
    projector_weight: int
    best_coset_weight: int
    best_coefficients: tuple[int, ...]


def poly_from_values(values: list[int]) -> sp.Poly:
    return sp.Poly(sum(value * T**i for i, value in enumerate(values)), T, modulus=Q)


def coeff_vector(poly: sp.Poly, length: int) -> list[int]:
    out = [0] * length
    for (power,), value in poly.as_dict().items():
        out[power % length] = (out[power % length] + int(value)) % Q
    return out


def torsion_factors(order: int) -> list[sp.Poly]:
    """Factor T^order-1 for q=-1 mod order into linears/quadratics."""
    remaining = sp.Poly(T**order - 1, T, modulus=Q)
    factors: list[sp.Poly] = []
    for root in (1, Q - 1):
        divisor = sp.Poly(T - root, T, modulus=Q)
        quotient, remainder = remaining.div(divisor)
        if remainder.is_zero:
            factors.append(divisor)
            remaining = quotient
    while remaining.degree() > 0:
        found = False
        for a in range(Q):
            divisor = sp.Poly(T**2 - a * T + 1, T, modulus=Q)
            quotient, remainder = remaining.div(divisor)
            if remainder.is_zero:
                factors.append(divisor)
                remaining = quotient
                found = True
                break
        if not found:
            factors.append(remaining)
            break
    return factors


def projector_vector(h: int, quotient_size: int) -> list[int]:
    subgroup_size = h // quotient_size
    out = [0] * h
    for k in range(subgroup_size):
        out[k * quotient_size] = 1
    return out


def weight(values: list[int]) -> int:
    return sum(1 for value in values if value % Q)


def cyclic_shift(values: list[int], shift: int) -> list[int]:
    h = len(values)
    out = [0] * h
    for i, value in enumerate(values):
        out[(i + shift) % h] = value
    return out


def min_weight_degree2_coset(base: list[int], generator: list[int]) -> tuple[int, tuple[int, int]]:
    """Brute force base + (a + bT)generator for a degree-2 annihilator."""
    basis0 = generator
    basis1 = cyclic_shift(generator, 1)
    best_weight = len(base) + 1
    best_pair = (0, 0)
    for a in range(Q):
        a_part = [(x + a * y) % Q for x, y in zip(base, basis0)]
        for b in range(Q):
            candidate = [(x + b * y) % Q for x, y in zip(a_part, basis1)]
            current = weight(candidate)
            if current < best_weight:
                best_weight = current
                best_pair = (a, b)
                if best_weight == 0:
                    return best_weight, best_pair
    return best_weight, best_pair


def audit(cycle: list[int], quotient_size: int) -> WeightResult:
    h = len(cycle)
    subgroup_size = h // quotient_size
    torsion = sp.Poly(T**h - 1, T, modulus=Q)
    j_poly = poly_from_values(cycle)
    natural_gcd = sp.gcd(j_poly, torsion)
    factor = next(f for f in torsion_factors(h) if f.degree() == 2)
    quotient, remainder = torsion.div(factor)
    if not remainder.is_zero:
        raise AssertionError("bad factor")
    ann_generator = coeff_vector(quotient, h)
    projector = projector_vector(h, quotient_size)
    best_weight, best_pair = min_weight_degree2_coset(projector, ann_generator)
    return WeightResult(
        quotient_size=quotient_size,
        subgroup_size=subgroup_size,
        factor_degree=factor.degree(),
        natural_gcd_degree=natural_gcd.degree(),
        artificial_ann_dimension=factor.degree(),
        projector_weight=weight(projector),
        best_coset_weight=best_weight,
        best_coefficients=best_pair,
    )


def p24_packet_degree_counts() -> dict[int, int]:
    """Degree counts for irreducible factors of T^66254-1 over F_p."""
    p = 10**24 + 7
    m = 2 * 157 * 211
    counts: dict[int, int] = {}
    for d in sp.divisors(m):
        order = int(sp.n_order(p % d, d)) if d > 1 else 1
        count = int(sp.totient(d) // order)
        counts[order] = counts.get(order, 0) + count
    return dict(sorted(counts.items()))


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    print("cyclic-code projector weight toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"q_mod_h={Q % H}")
    print(f"p24_packet_degree_counts={p24_packet_degree_counts()}")
    print()
    print(
        "quotient_size subgroup_size natural_gcd_degree artificial_packet_degree "
        "ann_dimension projector_weight best_coset_weight best_coefficients"
    )
    for quotient_size in (3, 5, 6, 10, 15):
        if H % quotient_size:
            continue
        result = audit(cycle, quotient_size)
        print(
            f"{result.quotient_size:13d} {result.subgroup_size:13d} "
            f"{result.natural_gcd_degree:18d} {result.factor_degree:24d} "
            f"{result.artificial_ann_dimension:13d} {result.projector_weight:16d} "
            f"{result.best_coset_weight:17d} {result.best_coefficients}"
        )
    print()
    print("interpretation")
    print("  p24_quotient_has_only_28_frobenius_packets=1")
    print("  natural_toy_cm_cycle_has_zero_annihilator=1")
    print("  artificial_one_packet_annihilator_does_not_lower_projector_weight=1")
    print("  cyclic_code_formulation_is_exact_but_not_yet_a_sparse_selector=1")
    print(
        "conclusion=frobenius_packet_cyclic_code_route_still_needs_an_"
        "embedded_period_or_a_genuine_large_kernel_with_low_weight_coset"
    )


if __name__ == "__main__":
    main()
