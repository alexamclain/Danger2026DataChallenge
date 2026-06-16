#!/usr/bin/env python3
"""CRT decomposition of the first complement augmentation moment.

For h=m*n with gcd(m,n)=1, write the complement fibers

    F_r(X) = sum_k j_{n*r + m*k} X^k,      0 <= r < m.

The first moment

    M1(X) = sum_r r F_r(X)

looks like an order-m weighted sum.  If m is decomposed into coprime factors
`m = prod c_i`, the CRT identity

    r = sum_i e_i (r mod c_i)        in Z/mZ

expresses M1 as a sum of partial first moments

    M1 = sum_i e_i P_i,
    P_i = sum_t t * sum_{r == t mod c_i} F_r.

For p24, m=2*157*211, so the first augmentation derivative is built from
intermediate trace/moment objects of degrees n*2, n*157, n*211 rather than a
dense order-m recovery table.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp

from complement_trace_recovery_toy import find_case
from relative_moment_projection_scan import section_fiber_polynomials

P24_N = 3_107_441
P24_M_FACTORS = (2, 157, 211)


@dataclass(frozen=True)
class CrtComponent:
    component: int
    idempotent: int
    intermediate_degree: int
    partial_nonzero_coeffs: int


def coprime_components(m: int) -> list[int]:
    return [int(p) ** int(e) for p, e in sp.factorint(m).items()]


def crt_idempotent(m: int, component: int) -> int:
    rest = m // component
    return (rest * pow(rest % component, -1, component)) % m


def scale_poly(poly: sp.Poly, coeff: int, q: int) -> sp.Poly:
    return sp.Poly((coeff % q) * poly.as_expr(), poly.gens[0], modulus=q)


def first_moment(fibers: list[sp.Poly], q: int) -> sp.Poly:
    var = fibers[0].gens[0]
    total = sp.Poly(0, var, modulus=q)
    for r, fiber in enumerate(fibers):
        total += scale_poly(fiber, r, q)
    return sp.Poly(total.as_expr(), var, modulus=q)


def partial_moment(fibers: list[sp.Poly], component: int, q: int) -> sp.Poly:
    var = fibers[0].gens[0]
    total = sp.Poly(0, var, modulus=q)
    for t in range(component):
        subtotal = sp.Poly(0, var, modulus=q)
        for r in range(t, len(fibers), component):
            subtotal += fibers[r]
        total += scale_poly(subtotal, t, q)
    return sp.Poly(total.as_expr(), var, modulus=q)


def carry_moment(fibers: list[sp.Poly], components: list[CrtComponent], m: int, q: int) -> sp.Poly:
    """Carry correction from integer representatives to CRT representatives."""
    var = fibers[0].gens[0]
    total = sp.Poly(0, var, modulus=q)
    for r, fiber in enumerate(fibers):
        crt_lift = sum(row.idempotent * (r % row.component) for row in components)
        if crt_lift % m != r:
            raise AssertionError((r, crt_lift, m))
        carry = (crt_lift - r) // m
        if carry:
            total += scale_poly(fiber, carry, q)
    return sp.Poly(total.as_expr(), var, modulus=q)


def nonzero_coeffs(poly: sp.Poly) -> int:
    return sum(1 for coeff in poly.as_dict().values() if int(coeff))


def verify_case(D: int | None, preferred_m: int, q_start: int, q_stop: int) -> tuple[int, int, int, int, int, bool, bool, list[CrtComponent], str, str, str, str]:
    D, q, ell, cycle = find_case(
        D=D,
        q_start=q_start,
        q_stop=q_stop,
        min_h=12,
        max_h=200,
        max_abs_D=80000,
        preferred_m=preferred_m,
    )
    h = len(cycle)
    m = preferred_m
    n = h // m
    fibers = section_fiber_polynomials(cycle, q, m, "complement")
    direct = first_moment(fibers, q)
    components: list[CrtComponent] = []
    crt_linear = sp.Poly(0, direct.gens[0], modulus=q)
    for component in coprime_components(m):
        idem = crt_idempotent(m, component)
        partial = partial_moment(fibers, component, q)
        crt_linear += scale_poly(partial, idem, q)
        components.append(
            CrtComponent(
                component=component,
                idempotent=idem,
                intermediate_degree=n * component,
                partial_nonzero_coeffs=nonzero_coeffs(partial),
            )
        )
    crt_linear = sp.Poly(crt_linear.as_expr(), direct.gens[0], modulus=q)
    carry = carry_moment(fibers, components, m, q)
    corrected = sp.Poly((crt_linear - scale_poly(carry, m, q)).as_expr(), direct.gens[0], modulus=q)
    return (
        D,
        q,
        ell,
        h,
        n,
        crt_linear == direct,
        corrected == direct,
        components,
        str(direct.as_expr()),
        str(crt_linear.as_expr()),
        str(carry.as_expr()),
        str(corrected.as_expr()),
    )


def p24_degree_summary() -> None:
    total = sum(P24_N * component for component in P24_M_FACTORS)
    print("p24_degree_summary")
    print(f"  n={P24_N}")
    print(f"  m_factors={list(P24_M_FACTORS)}")
    for component in P24_M_FACTORS:
        print(f"  component={component:3d} intermediate_degree={P24_N * component}")
    print(f"  sum_intermediate_degrees={total}")
    print(f"  sqrt_p24=1000000000000")
    print(f"  degree_sum_over_sqrt_p24={total / 1_000_000_000_000:.9f}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--D", type=int)
    parser.add_argument("--m", type=int, default=6)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=200000)
    args = parser.parse_args()

    D, q, ell, h, n, crt_ok, corrected_ok, components, direct, crt_linear, carry, corrected = verify_case(
        args.D,
        args.m,
        args.q_start,
        args.q_stop,
    )
    print("augmentation CRT derivative toy")
    print(f"D={D}")
    print(f"q={q}")
    print(f"ell={ell}")
    print(f"h={h}")
    print(f"m={args.m}")
    print(f"n={n}")
    print(f"gcd_m_n={sp.gcd(args.m, n)}")
    print(f"components={[row.component for row in components]}")
    print()
    print("component idempotent intermediate_degree partial_nonzero_coeffs")
    for row in components:
        print(
            f"{row.component:9d} {row.idempotent:10d} "
            f"{row.intermediate_degree:19d} {row.partial_nonzero_coeffs:22d}"
        )
    print()
    print(f"naive_crt_linear_reconstruction_ok={int(crt_ok)}")
    print(f"carry_corrected_reconstruction_ok={int(corrected_ok)}")
    print(f"direct_M1={direct}")
    print(f"crt_linear_M1={crt_linear}")
    print(f"carry_moment={carry}")
    print(f"corrected_M1={corrected}")
    print()
    p24_degree_summary()
    print()
    print("interpretation")
    print("  integer_M1_equals_CRT_linear_moment_minus_m_times_carry_moment=1")
    print("  carry_term_is_the_hidden_cost_of_using_integer_representatives=1")
    print("  CRT_linear_moment_is_tower_native_but_not_identical_to_Hasse_derivative=1")
    print("conclusion=reported_augmentation_crt_derivative_toy")


if __name__ == "__main__":
    main()
