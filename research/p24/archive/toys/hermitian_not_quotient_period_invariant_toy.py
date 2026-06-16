#!/usr/bin/env python3
"""Toy showing Hermitian packets do not factor through quotient periods.

The quotient period vector records only

    y_u = J_u(1) = sum_k j_{u+m*k}.

The Hermitian packet scalar uses

    J_u(zeta_n^a)

for a nontrivial relative character.  This toy constructs two cyclic datasets
with identical quotient periods y_u but different Hermitian packet values.
Therefore the Hermitian certificate cannot be computed from the quotient
period polynomial alone; it still needs internal H-character data.
"""

from __future__ import annotations

import sympy as sp


def primitive_root_of_order(q: int, order: int) -> int:
    if (q - 1) % order:
        raise ValueError("order must divide q-1")
    zeta = pow(sp.primitive_root(q), (q - 1) // order, q)
    for prime in sp.factorint(order):
        if pow(zeta, order // prime, q) == 1:
            raise AssertionError("not primitive")
    return int(zeta)


def quotient_periods(values: list[int], q: int, m: int) -> list[int]:
    h = len(values)
    n = h // m
    return [
        sum(values[u + m * k] for k in range(n)) % q
        for u in range(m)
    ]


def relative_fibers(values: list[int], q: int, m: int, a: int) -> list[int]:
    h = len(values)
    n = h // m
    zeta = primitive_root_of_order(q, n)
    return [
        sum(pow(zeta, a * k, q) * values[u + m * k] for k in range(n)) % q
        for u in range(m)
    ]


def hermitian_packet(values: list[int], q: int, m: int, a: int) -> int:
    h = len(values)
    n = h // m
    zeta = primitive_root_of_order(q, n)
    fibers = relative_fibers(values, q, m, a)
    total = 0
    for u, left in enumerate(fibers):
        inv_u = (-u) % m
        carry = (u + inv_u) // m
        total = (total + pow(zeta, a * carry, q) * left * fibers[inv_u]) % q
    return total


def main() -> None:
    q = 101
    m = 2
    n = 5
    h = m * n
    a = 1
    zeta = primitive_root_of_order(q, n)

    # Both datasets have quotient periods [1, 1].  They differ only by moving
    # the nonzero entry inside the second H-fiber.
    values_a = [0] * h
    values_b = [0] * h
    values_a[0] = 1
    values_a[1] = 1
    values_b[0] = 1
    values_b[1 + m] = 1

    periods_a = quotient_periods(values_a, q, m)
    periods_b = quotient_periods(values_b, q, m)
    fibers_a = relative_fibers(values_a, q, m, a)
    fibers_b = relative_fibers(values_b, q, m, a)
    hermitian_a = hermitian_packet(values_a, q, m, a)
    hermitian_b = hermitian_packet(values_b, q, m, a)

    print("Hermitian not quotient-period invariant toy")
    print(f"q={q}")
    print(f"h={h}")
    print(f"m={m}")
    print(f"n={n}")
    print(f"a={a}")
    print(f"zeta_n={zeta}")
    print(f"quotient_periods_a={periods_a}")
    print(f"quotient_periods_b={periods_b}")
    print(f"same_quotient_periods={int(periods_a == periods_b)}")
    print(f"relative_fibers_a={fibers_a}")
    print(f"relative_fibers_b={fibers_b}")
    print(f"hermitian_packet_a={hermitian_a}")
    print(f"hermitian_packet_b={hermitian_b}")
    print(f"same_hermitian_packet={int(hermitian_a == hermitian_b)}")
    print()
    print("interpretation")
    print("  quotient_periods_only_see_Ju_at_X_equals_1=1")
    print("  Hermitian_packets_need_Ju_at_nontrivial_relative_characters=1")
    print("  quotient_period_polynomial_cannot_determine_Hermitian_certificate=1")
    print("conclusion=Hermitian_scalar_still_requires_internal_H_character_data")


if __name__ == "__main__":
    main()
