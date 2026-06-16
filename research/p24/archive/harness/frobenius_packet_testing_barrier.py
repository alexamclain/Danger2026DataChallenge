#!/usr/bin/env python3
"""Toy barrier for Frobenius-packet testing of class-character periods.

The p24 third quotient has large Frobenius orbits on quotient characters
(`ord_66254(p)=5460`).  This suggests testing reduced normality packet by
packet over F_p instead of character by character over a root-of-unity
extension.

The packet compression is real, but it does not make the period projector
cheap.  For a quotient-period vector

    Y(T) = sum_r y_r T^r in F_q[T]/(T^m-1),

a Frobenius packet is the remainder of Y modulo an irreducible factor of
T^m-1.  That is still a full-support linear functional in the y_r.  In a
black-box model, if even deg(f) coordinates are left unknown, they can be
altered to force the packet to vanish while agreeing on every queried
coordinate.
"""

from __future__ import annotations

from itertools import combinations

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
QUOTIENT_SIZE = 10
SUBGROUP_SIZE = H // QUOTIENT_SIZE
T = sp.symbols("T")


def period_sums(cycle: list[int]) -> list[int]:
    return [
        sum(cycle[(r + k * QUOTIENT_SIZE) % H] for k in range(SUBGROUP_SIZE)) % Q
        for r in range(QUOTIENT_SIZE)
    ]


def poly_from_values(values: list[int]) -> sp.Poly:
    return sp.Poly(sum(value * T**i for i, value in enumerate(values)), T, modulus=Q)


def small_torsion_factors(poly: sp.Poly) -> list[sp.Poly]:
    """Factor T^10-1 over F_Q without relying on SymPy's factor sorting.

    Here Q == -1 mod 10, so the non-linear Frobenius packets are reciprocal
    quadratics with roots {zeta, zeta^Q} = {zeta, zeta^-1}.
    """
    remaining = poly
    factors: list[sp.Poly] = []
    for root in (1, Q - 1):
        divisor = sp.Poly(T - root, T, modulus=Q)
        quotient, remainder = remaining.div(divisor)
        if not remainder.is_zero:
            raise AssertionError((root, remaining))
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


def coeff_vector(poly: sp.Poly, degree: int) -> list[int]:
    coeffs = [0] * degree
    for (power,), value in poly.as_dict().items():
        if power < degree:
            coeffs[power] = int(value) % Q
    return coeffs


def powers_mod_factor(factor: sp.Poly, count: int) -> list[list[int]]:
    degree = factor.degree()
    out: list[list[int]] = []
    for exponent in range(count):
        rem = sp.Poly(T**exponent, T, modulus=Q).rem(factor)
        out.append(coeff_vector(rem, degree))
    return out


def solve_mod(matrix: list[list[int]], rhs: list[int], q: int) -> list[int] | None:
    """Solve square linear system matrix * x = rhs over F_q."""
    n = len(rhs)
    aug = [row[:] + [rhs[i] % q] for i, row in enumerate(matrix)]
    rank = 0
    pivots: list[int] = []
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if aug[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        aug[rank], aug[pivot] = aug[pivot], aug[rank]
        inv = pow(aug[rank][col] % q, -1, q)
        aug[rank] = [(value * inv) % q for value in aug[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = aug[row][col] % q
            if scale:
                aug[row] = [(x - scale * y) % q for x, y in zip(aug[row], aug[rank])]
        pivots.append(col)
        rank += 1
    if rank != n:
        return None
    solution = [0] * n
    for row, col in enumerate(pivots):
        solution[col] = aug[row][-1] % q
    return solution


def adversarial_packet_kill(values: list[int], factor: sp.Poly) -> tuple[list[int], list[int], list[int]]:
    """Alter deg(f) coordinates so Y mod f becomes zero."""
    degree = factor.degree()
    powers = powers_mod_factor(factor, len(values))
    current = poly_from_values(values).rem(factor)
    target = [(-x) % Q for x in coeff_vector(current, degree)]
    for positions in combinations(range(len(values)), degree):
        # Columns are T^position modulo factor; solve for coordinate deltas.
        matrix = [[powers[position][row] for position in positions] for row in range(degree)]
        deltas = solve_mod(matrix, target, Q)
        if deltas is None:
            continue
        modified = values[:]
        for position, delta in zip(positions, deltas):
            modified[position] = (modified[position] + delta) % Q
        if poly_from_values(modified).rem(factor).degree() == -sp.oo:
            return list(positions), deltas, modified
    raise RuntimeError("no packet-killing coordinate patch found")


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)
    periods = period_sums(cycle)
    period_poly = poly_from_values(periods)
    torsion_poly = sp.Poly(T**QUOTIENT_SIZE - 1, T, modulus=Q)
    factors = small_torsion_factors(torsion_poly)

    print("frobenius packet testing barrier toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number={H}")
    print(f"generator_ell={ELL}")
    print(f"quotient_size={QUOTIENT_SIZE}")
    print(f"subgroup_size={SUBGROUP_SIZE}")
    print(f"q_mod_quotient={Q % QUOTIENT_SIZE}")
    print(f"periods={periods}")
    print()
    print("packet_factors")
    chosen = None
    for factor in factors:
        remainder = period_poly.rem(factor)
        rem_vec = coeff_vector(remainder, factor.degree())
        nonzero = any(rem_vec)
        print(
            f"  degree={factor.degree()} "
            f"factor={factor.as_expr()} remainder_coeffs={rem_vec} nonzero={int(nonzero)}"
        )
        if chosen is None and factor.degree() > 1:
            chosen = factor
    if chosen is None:
        raise RuntimeError("need a non-linear Frobenius packet")

    positions, deltas, modified = adversarial_packet_kill(periods, chosen)
    agrees = sum(1 for a, b in zip(periods, modified) if a == b)
    killed = not any(coeff_vector(poly_from_values(modified).rem(chosen), chosen.degree()))
    print()
    print("black_box_ambiguity_demo")
    print(f"  chosen_factor_degree={chosen.degree()}")
    print(f"  chosen_factor={chosen.as_expr()}")
    print(f"  modified_positions={positions}")
    print(f"  deltas={deltas}")
    print(f"  agrees_on_period_coordinates={agrees}/{len(periods)}")
    print(f"  modified_periods={modified}")
    print(f"  packet_killed={int(killed)}")
    print(f"  modified_values_distinct={int(len(set(modified)) == len(modified))}")
    print()
    print("interpretation")
    print("  frobenius_packet_compression_is_real=1")
    print("  packet_remainder_is_still_a_full_support_linear_function=1")
    print("  leaving_deg_factor_coordinates_unknown_can_force_packet_vanishing=1")
    print("  statistical_or_black_box_sampling_cannot_certify_nonvanishing=1")
    print(
        "conclusion=frobenius_orbit_packets_sharpen_the_normality_gap_but_do_"
        "not_compute_the_missing_embedded_periods"
    )


if __name__ == "__main__":
    main()
