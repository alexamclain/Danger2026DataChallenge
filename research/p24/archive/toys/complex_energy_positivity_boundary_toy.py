#!/usr/bin/env python3
"""Toy model showing p24 relative energy is not complex-positive.

For CM singular moduli, complex conjugation acts on the class group by
inversion.  In the relative notation h=m*n,

    conjugate(P_u(a)) = zeta_n^(a*c(u)) P_{-u}(a)

where `c(u)` is the carry defined by `(-u mod m) = -u + m*c(u)`.

up to the harmless choice of origin.  The scalar used in the finite-field
energy certificate is

    E_a = sum_u P_u(a) P_u(-a),

which pairs the same quotient coordinate `u`, not the inverted coordinate.
The positive Hermitian norm would be

    H_a = sum_u zeta_n^(a*c(u)) P_u(a) P_{-u}(a).

This toy builds a small conjugation-symmetric cyclic vector and shows these
two quantities differ.  Thus characteristic-zero positivity cannot prove the
p24 energy p-unit theorem.
"""

from __future__ import annotations

import cmath


def make_conjugation_symmetric_values(h: int) -> list[complex]:
    values = [0j] * h
    values[0] = 7.0
    if h % 2 == 0:
        values[h // 2] = -3.0
    for i in range(1, (h + 1) // 2):
        if i == h - i:
            continue
        z = complex((i * i + 3) / 5, (2 * i + 1) / 7)
        values[i] = z
        values[-i % h] = z.conjugate()
    return values


def relative_fiber(values: list[complex], m: int, a: int) -> list[complex]:
    h = len(values)
    n = h // m
    zeta = cmath.exp(2j * cmath.pi / n)
    out: list[complex] = []
    for u in range(m):
        total = 0j
        for k in range(n):
            total += (zeta ** (a * k)) * values[(u + m * k) % h]
        out.append(total)
    return out


def main() -> None:
    h = 12
    m = 4
    n = h // m
    a = 1
    values = make_conjugation_symmetric_values(h)
    p_plus = relative_fiber(values, m, a)
    p_minus = relative_fiber(values, m, -a)
    zeta = cmath.exp(2j * cmath.pi / n)

    energy = sum(p_plus[u] * p_minus[u] for u in range(m))
    positive = 0j
    conjugation_errors = []
    for u in range(m):
        inv_u = (-u) % m
        carry = (u + inv_u) // m
        positive += (zeta ** (a * carry)) * p_plus[u] * p_plus[inv_u]
        conjugation_errors.append(
            abs((zeta ** (a * carry)) * p_plus[inv_u] - p_plus[u].conjugate())
        )
    abs_square = sum(abs(x) ** 2 for x in p_plus)

    print("complex energy positivity boundary toy")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"a={a}")
    print(f"max_conjugation_error={max(conjugation_errors):.3e}")
    print(f"finite_field_energy_pairing={energy.real:.12g}+{energy.imag:.12g}i")
    print(f"hermitian_positive_pairing={positive.real:.12g}+{positive.imag:.12g}i")
    print(f"sum_abs_square={abs_square:.12g}")
    print(f"energy_equals_positive={int(abs(energy - positive) < 1e-9)}")
    print(f"positive_equals_abs_square={int(abs(positive.real - abs_square) < 1e-9 and abs(positive.imag) < 1e-9)}")
    print()
    print("interpretation")
    print("  complex_conjugation_pairs_u_with_minus_u=1")
    print("  relative_energy_pairs_u_with_same_u=1")
    print("  relative_energy_is_not_a_positive_archimedean_norm=1")
    print("  characteristic_zero_positivity_cannot_prove_padic_unit_status=1")
    print("conclusion=energy_punit_theorem_still_needs_selected_prime_arithmetic")


if __name__ == "__main__":
    main()
