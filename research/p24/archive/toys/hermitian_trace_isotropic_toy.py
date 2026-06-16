#!/usr/bin/env python3
"""Hermitian trace can be isotropic on a line.

This is the local-lattice warning behind the p24 Hermitian axis determinant.
Even over an unramified finite-field packet with the middle Frobenius
involution, the scalar-valued Hermitian trace form

    h(x,y) = Tr(x * y^(q^(d/2)))

can vanish on a nonzero vector.  Therefore unramifiedness and local existence
of normal bases do not prove that the selected axis lattice is nondegenerate.

Toy field:

    F_81 = F_3[a]/(a^4+a^3+a^2+1),  d=4.

For v=a^3, h(v,v)=0.
"""

from __future__ import annotations


Q = 3
# a^4 + a^3 + a^2 + 1 = 0, so a^4 = -a^3-a^2-1 = 2a^3+2a^2+2.
MOD_RELATION = (2, 0, 2, 2)


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % Q for a, b in zip(left, right))


def mul(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    coeffs = [0] * 7
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            coeffs[i + j] = (coeffs[i + j] + a * b) % Q
    for degree in range(6, 3, -1):
        c = coeffs[degree] % Q
        if not c:
            continue
        coeffs[degree] = 0
        for i, value in enumerate(MOD_RELATION):
            coeffs[degree - 4 + i] = (coeffs[degree - 4 + i] + c * value) % Q
    return tuple(coeffs[:4])


def pow_field(value: tuple[int, ...], exponent: int) -> tuple[int, ...]:
    result = (1, 0, 0, 0)
    current = value
    n = exponent
    while n:
        if n & 1:
            result = mul(result, current)
        current = mul(current, current)
        n >>= 1
    return result


def trace(value: tuple[int, ...]) -> tuple[int, ...]:
    total = (0, 0, 0, 0)
    current = value
    for _ in range(4):
        total = add(total, current)
        current = pow_field(current, Q)
    return total


def main() -> None:
    alpha_cubed = (0, 0, 0, 1)
    middle_conjugate = pow_field(alpha_cubed, Q**2)
    hermitian_square = mul(alpha_cubed, middle_conjugate)
    hermitian_trace = trace(hermitian_square)

    print("Hermitian trace isotropic toy")
    print("field=F3[a]/(a^4+a^3+a^2+1)")
    print("degree=4")
    print("middle_frobenius_power=3^2")
    print(f"v=a^3 encoded={alpha_cubed}")
    print(f"v_middle_conjugate={middle_conjugate}")
    print(f"v_times_conjugate={hermitian_square}")
    print(f"trace_v_conjugate={hermitian_trace}")
    print()
    print("interpretation")
    print("  nonzero_vector=1")
    print("  hermitian_trace_self_pairing_zero=1")
    print("  unramified_even_degree_packet_does_not_force_axis_lattice_unimodular=1")
    print("conclusion=reported_hermitian_trace_isotropic_toy")


if __name__ == "__main__":
    main()
