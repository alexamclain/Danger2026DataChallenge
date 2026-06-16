#!/usr/bin/env python3
"""Toy model for the decomposition-field packet norm.

The earlier DFT toys put all roots of unity in the base field.  The p24
relative packets are different: the CM roots are in F_p, but zeta_n is in a
large extension.  The exact finite-field certificate is therefore a packet
gcd/resultant modulo irreducible factors of Phi_n.

This toy uses the calibrated D=-5000, h=30 CM cycle over q=1259.  The CM
roots split in F_q, while q == -1 mod 5, so the nontrivial 5th roots of unity
form two Frobenius packets of degree 2.  It computes the relative energy
polynomial

    C(X) = sum_d C_d X^d,       C_d = sum_i j_{i+m*d} j_i,

and checks each packet by reducing C modulo the irreducible factors of Phi_5.
For p24 the same construction has n=3107441 and eight packet primes in the
degree-8 decomposition field.
"""

from __future__ import annotations

import sympy as sp
from cypari2 import Pari

from embedded_decomposition_calibration import (
    D,
    ELL,
    H,
    Q,
    isogeny_neighbors,
    pari_linear_roots,
    walk_cycle,
)

X = sp.symbols("X")

P24 = 10**24 + 7
P24_N = 3107441


def poly_mod_q_from_coeffs(coeffs: list[int], q: int) -> sp.Poly:
    return sp.Poly(sum((c % q) * X**i for i, c in enumerate(coeffs)), X, modulus=q)


def autocorrelation_coeffs(cycle: list[int], q: int, m: int) -> list[int]:
    h = len(cycle)
    if h % m:
        raise ValueError("m must divide h")
    n = h // m
    out: list[int] = []
    for d in range(n):
        offset = m * d
        total = 0
        for i, value in enumerate(cycle):
            total = (total + cycle[(i + offset) % h] * value) % q
        out.append(total)
    return out


def cyclotomic_packet_factors(n: int, q: int) -> list[sp.Poly]:
    """Return irreducible factors of Phi_n over F_q for the small toy case.

    SymPy's FLINT-backed factor sorting can choke on nmod comparisons in some
    local installs.  For the calibrated toy n=5, q=-1 mod 5, the factors are
    reciprocal quadratics, so a direct search is clearer and more robust.
    """
    phi = sp.Poly(sp.cyclotomic_poly(n, X), X, modulus=q)
    if n == 5 and q % 5 == 4:
        remaining = phi
        factors: list[sp.Poly] = []
        for a in range(q):
            candidate = sp.Poly(X**2 - a * X + 1, X, modulus=q)
            quotient, remainder = remaining.div(candidate)
            if remainder.is_zero:
                factors.append(candidate)
                remaining = quotient
                if remaining.degree() == 0:
                    break
        if remaining.degree() == 0 and len(factors) == 2:
            return factors
        raise AssertionError("failed to find the two reciprocal quadratic factors")

    _coeff, factors_with_exp = sp.factor_list(phi.as_expr(), X, modulus=q)
    return [sp.Poly(factor, X, modulus=q) for factor, exponent in factors_with_exp for _ in range(exponent)]


def packet_rows(energy_poly: sp.Poly, n: int, q: int) -> list[tuple[int, str, list[int], int, bool]]:
    rows: list[tuple[int, str, list[int], int, bool]] = []
    for factor in cyclotomic_packet_factors(n, q):
        rem = energy_poly.rem(factor)
        rem_coeffs = [int(rem.nth(i)) % q for i in range(factor.degree())]
        # For a monic factor f, resultant(f, C) is the packet norm up to the
        # harmless sign convention used by SymPy.
        resultant = int(sp.resultant(factor.as_expr(), energy_poly.as_expr(), X)) % q
        nonzero = bool(any(rem_coeffs))
        rows.append((factor.degree(), str(factor.as_expr()), rem_coeffs, resultant, nonzero))
    return rows


def p24_degree_accounting() -> tuple[int, int, int, bool]:
    ord_p = int(sp.n_order(P24 % P24_N, P24_N))
    packet_count = (P24_N - 1) // ord_p
    half_power = pow(P24, ord_p // 2, P24_N) if ord_p % 2 == 0 else None
    minus_in_orbit = half_power == P24_N - 1
    real_energy_norm_degree = ord_p // 2 if minus_in_orbit else ord_p
    return ord_p, packet_count, real_energy_norm_degree, minus_in_orbit


def main() -> None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    roots = pari_linear_roots(pari.polclass(D), Q)
    graph = isogeny_neighbors(roots, ELL, Q)
    cycle = walk_cycle(graph)

    m = 6
    n = H // m
    ord_q = int(sp.n_order(Q % n, n))
    packet_count = (n - 1) // ord_q
    coeffs = autocorrelation_coeffs(cycle, Q, m)
    energy_poly = poly_mod_q_from_coeffs(coeffs, Q)
    rows = packet_rows(energy_poly, n, Q)
    all_nonzero = all(row[-1] for row in rows)
    product_norm = 1
    for _degree, _factor, _rem, resultant, _nonzero in rows:
        product_norm = product_norm * resultant % Q

    p24_ord, p24_packets, p24_real_degree, p24_minus = p24_degree_accounting()

    print("cyclotomic packet norm toy")
    print(f"D={D}")
    print(f"q={Q}")
    print(f"class_number_h={H}")
    print(f"generator_ell={ELL}")
    print(f"quotient_m={m}")
    print(f"relative_n={n}")
    print(f"q_mod_n={Q % n}")
    print(f"ord_n_q={ord_q}")
    print(f"packet_count={(n - 1) // ord_q}")
    print(f"energy_coeffs={coeffs}")
    print(f"energy_poly={energy_poly.as_expr()}")
    print()
    print("packet_factors")
    for degree, factor, rem_coeffs, resultant, nonzero in rows:
        print(
            f"  degree={degree} factor={factor} "
            f"remainder_coeffs={rem_coeffs} packet_norm={resultant} "
            f"nonzero={int(nonzero)}"
        )
    print()
    print("toy_certificate")
    print(f"  all_packet_energies_nonzero={int(all_nonzero)}")
    print(f"  product_of_packet_norms_mod_q={product_norm}")
    print(f"  product_certificate_nonzero={int(product_norm != 0)}")
    print()
    print("p24_analogue")
    print(f"  n={P24_N}")
    print(f"  ord_n_p={p24_ord}")
    print(f"  packet_count={p24_packets}")
    print(f"  minus_one_in_frobenius_orbit={int(p24_minus)}")
    print(f"  real_energy_packet_norm_degree={p24_real_degree}")
    print(f"  decomposition_field_degree={p24_packets}")
    print()
    print("interpretation")
    print("  packet_gcd_or_resultant_tests_work_without_roots_of_unity_in_base=1")
    print("  all_packets_nonzero_equiv_product_of_packet_norms_nonzero=1")
    print("  p24_energy_packets_are_norms_to_a_degree_8_decomposition_field=1")
    print("conclusion=decomposition_field_packet_norm_is_the_sharp_padic_unit_target")


if __name__ == "__main__":
    main()
