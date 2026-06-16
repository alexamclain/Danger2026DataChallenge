#!/usr/bin/env python3
"""Toy gate for the Gaussian-period normal basis used by the p24 prefix.

If ell = t*n + 1 is prime, gcd(t,n)=1, and q has order n modulo ell, then
Gaussian periods

    eta_i = sum_{c in C0} zeta_ell^(q^i c)

for C0 the order-t subgroup of (Z/ellZ)^* form a normal basis of the
degree-n cyclotomic field.  The p24 right field has exactly this shape:

    211 = 6*35 + 1,    ord_211(10^24+7) = 35.

This toy verifies the construction in a small type-2 example and checks that
the Gaussian basis can be used in the same trace-dual coefficient identity as
the prefix Fitting theorem.
"""

from __future__ import annotations

import argparse
from math import gcd
import random

from hermitian_mixed_lang_normality_audit import (
    lang_inverse_for_orbit,
    subfield_power_basis,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)
from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_prefix_normal_basis_toy import (
    audit_tuple,
    find_good_seeds,
    trace_dual_basis,
)
from trace_gcd_prefix_adjoint_trace_toy import random_element


P24_P = 10**24 + 7
P24_RIGHT = 211
P24_RIGHT_DEGREE = 35
P24_GAUSSIAN_TYPE = 6


def multiplicative_order(value: int, modulus: int) -> int:
    x = 1
    for order in range(1, modulus):
        x = (x * value) % modulus
        if x == 1:
            return order
    raise ValueError("order not found")


def prime_factors(value: int) -> list[int]:
    factors: list[int] = []
    n = value
    p = 2
    while p * p <= n:
        if n % p == 0:
            factors.append(p)
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        factors.append(n)
    return factors


def primitive_generator_mod_prime(ell: int) -> int:
    factors = prime_factors(ell - 1)
    for candidate in range(2, ell):
        if all(pow(candidate, (ell - 1) // factor, ell) != 1 for factor in factors):
            return candidate
    raise ValueError("primitive generator not found")


def gaussian_coset(g: int, n: int, t: int, ell: int) -> list[int]:
    return [pow(g, n * i, ell) for i in range(t)]


def gaussian_periods(
    q: int,
    n: int,
    t: int,
    ell: int,
    field: ExtensionField,
    zeta: FpE,
) -> list[FpE]:
    g = primitive_generator_mod_prime(ell)
    c0 = gaussian_coset(g, n, t, ell)
    periods: list[FpE] = []
    for i in range(n):
        multiplier = pow(q, i, ell)
        total = field.zero
        for c in c0:
            total = field.add(total, field.pow(zeta, (multiplier * c) % ell))
        periods.append(total)
    return periods


def p24_coset_audit() -> tuple[int, int, int, list[int], int, int]:
    q = P24_P % P24_RIGHT
    order = multiplicative_order(q, P24_RIGHT)
    g = primitive_generator_mod_prime(P24_RIGHT)
    c0 = gaussian_coset(g, P24_RIGHT_DEGREE, P24_GAUSSIAN_TYPE, P24_RIGHT)
    cosets = {
        tuple(sorted((pow(q, i, P24_RIGHT) * c) % P24_RIGHT for c in c0))
        for i in range(P24_RIGHT_DEGREE)
    }
    cover = len({value for coset in cosets for value in coset})
    intersection = len(set(c0) & {pow(q, i, P24_RIGHT) for i in range(order)})
    return q, order, g, c0, cover, intersection


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--right-degree", type=int, default=3)
    parser.add_argument("--gaussian-type", type=int, default=2)
    parser.add_argument("--left-degree", type=int, default=5)
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--trials", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    ell = args.gaussian_type * args.right_degree + 1
    if gcd(args.gaussian_type, args.right_degree) != 1:
        raise ValueError("Gaussian type and degree must be coprime")
    if multiplicative_order(args.q % ell, ell) != args.right_degree:
        raise ValueError("q must have the requested order modulo ell")
    if gcd(args.left_degree, args.right_degree) != 1:
        raise ValueError("left and right degrees must be coprime")
    if args.k * args.right_degree > args.left_degree:
        raise ValueError("toy expects positive residual dimension in L")

    extension_degree = args.left_degree * args.right_degree
    field = ExtensionField(
        args.q,
        extension_degree,
        find_irreducible_modulus(args.q, extension_degree, args.seed),
    )
    zeta = primitive_root_of_order(field, ell, args.seed)
    periods = gaussian_periods(
        args.q,
        args.right_degree,
        args.gaussian_type,
        ell,
        field,
        zeta,
    )
    period_rank = rank_mod_q([list(value) for value in periods], args.q)
    frobenius_cycle_failures = sum(
        field.pow(periods[i], args.q) != periods[(i + 1) % args.right_degree]
        for i in range(args.right_degree)
    )
    dual_basis, dual_pairing_failures = trace_dual_basis(
        periods,
        args.right_degree,
        field,
    )
    right_power_basis = subfield_power_basis(
        args.q,
        args.right_degree,
        field,
        args.seed + 29,
    )
    left_inverse = lang_inverse_for_orbit(
        args.q,
        args.left_degree,
        field,
        args.seed + 17,
    )

    rng = random.Random(args.seed)
    rows = [
        audit_tuple(
            "forced_zero",
            [field.zero for _ in range(args.k)],
            right_power_basis,
            periods,
            dual_basis,
            args.left_degree,
            args.right_degree,
            left_inverse,
            field,
        )
    ]
    good = find_good_seeds(
        args.k,
        right_power_basis,
        periods,
        dual_basis,
        args.left_degree,
        args.right_degree,
        left_inverse,
        field,
        rng,
        attempts=1000,
    )
    if good is not None:
        rows.append(
            audit_tuple(
                "found_gaussian_coefficient_independent",
                good,
                right_power_basis,
                periods,
                dual_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
            )
        )
    for trial in range(args.trials):
        rows.append(
            audit_tuple(
                f"random_{trial}",
                [random_element(field, rng) for _ in range(args.k)],
                right_power_basis,
                periods,
                dual_basis,
                args.left_degree,
                args.right_degree,
                left_inverse,
                field,
            )
        )

    p24_q, p24_order, p24_g, p24_c0, p24_cover, p24_intersection = p24_coset_audit()

    print("Trace-GCD prefix Gaussian normal-basis toy")
    print(f"q={args.q}")
    print(f"right_degree={args.right_degree}")
    print(f"gaussian_type={args.gaussian_type}")
    print(f"ell={ell}")
    print(f"left_degree={args.left_degree}")
    print(f"extension_degree={extension_degree}")
    print(f"k={args.k}")
    print(f"gaussian_period_rank={period_rank}")
    print(f"frobenius_cycle_failures={frobenius_cycle_failures}")
    print(f"dual_pairing_failures={dual_pairing_failures}")
    print(f"dual_reconstruction_failures={sum(row.reconstruction_failures for row in rows)}")
    print(f"basis_rank_mismatches={sum(not row.rank_match for row in rows)}")
    print(
        "found_gaussian_coefficient_independent="
        f"{int(any(row.label == 'found_gaussian_coefficient_independent' and row.injective for row in rows))}"
    )
    print("p24")
    print(f"  p24_p_mod_211={p24_q}")
    print(f"  p24_ord_211_p={p24_order}")
    print(f"  p24_gaussian_type={P24_GAUSSIAN_TYPE}")
    print(f"  p24_generator_mod_211={p24_g}")
    print(f"  p24_C0={p24_c0}")
    print(f"  p24_coset_cover_size={p24_cover}")
    print(f"  p24_C0_frobenius_subgroup_intersection_size={p24_intersection}")
    print("interpretation")
    print("  gaussian_periods_form_normal_basis_in_toy=1")
    print("  gaussian_trace_dual_coefficients_reconstruct_periods=1")
    print("  p24_right_field_has_type6_gaussian_normal_basis=1")
    print("conclusion=reported_trace_gcd_prefix_gaussian_normal_basis_toy")


if __name__ == "__main__":
    main()
