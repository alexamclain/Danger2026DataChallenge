#!/usr/bin/env python3
"""Audit origin action on centered marginal leading minors.

For `h=m*n`, an origin shift decomposes as

    shift == n*alpha + m*beta mod h.

For Hermitian packet pairings, the packet monomial shift indexed by `beta`
should cancel between the two arguments.  Thus the centered marginal leading
minor should vary only with the CRT-axis translation `alpha`.  The product
over alpha is then the natural origin-stable package for the visible
`Delta_C_leading` minor.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from centered_marginal_leading_minor_audit import det_mod


@dataclass(frozen=True)
class OriginProductAudit:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    left: int
    right: int
    cycle: tuple[int, ...]
    alpha_values: tuple[int, ...]
    alpha_product: int
    alpha_zero_count: int
    alpha_distinct_count: int
    beta_distinct_histogram: tuple[tuple[int, int], ...]
    beta_mismatch_count: int
    left_sign_normalized_right_mismatches: int
    left_sign_normalized_right_classes: int


def product_mod(values: list[int], q: int) -> int:
    out = 1
    for value in values:
        out = out * (value % q) % q
    return out


def histogram(values: list[int]) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for value in values:
        out[value] = out.get(value, 0) + 1
    return tuple(sorted(out.items()))


def translation_det_on_zero_sum(component: int, shift: int) -> int:
    """Determinant of translation by shift on sum-zero coordinates."""

    shift %= component
    if shift == 0:
        return 1
    return -1 if (component - gcd(component, shift)) % 2 else 1


def leading_det_for_shift(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    shift: int,
) -> int:
    shifted = rotate(cycle, shift)
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(shifted, q, m, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    marginal = double_marginal(kernel, left, right, q)
    centered = centered_double_marginal(marginal, q)
    width = left - 1
    if right - 1 < width:
        raise ValueError("right component too small for leading square window")
    return det_mod([row[:width] for row in centered], q)


def audit_case(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
) -> OriginProductAudit | None:
    h = len(cycle)
    n = h // m
    if factor.degree() % 2:
        return None
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None
    if right - 1 < left - 1:
        return None

    alpha_values: list[int] = []
    beta_distinct_counts: list[int] = []
    beta_mismatches = 0
    for alpha in range(m):
        beta_values: list[int] = []
        for beta in range(n):
            shift = (n * alpha + m * beta) % h
            beta_values.append(
                leading_det_for_shift(cycle, q, m, factor, left, right, shift)
            )
        distinct = len(set(beta_values))
        beta_distinct_counts.append(distinct)
        if distinct != 1:
            beta_mismatches += 1
        alpha_values.append(beta_values[0])

    by_right: dict[int, set[int]] = {}
    for alpha, value in enumerate(alpha_values):
        sign = translation_det_on_zero_sum(left, alpha)
        normalized = value if sign == 1 else (-value) % q
        by_right.setdefault(alpha % right, set()).add(normalized)
    right_mismatches = sum(1 for values in by_right.values() if len(values) != 1)

    return OriginProductAudit(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        left=left,
        right=right,
        cycle=tuple(cycle),
        alpha_values=tuple(alpha_values),
        alpha_product=product_mod(alpha_values, q),
        alpha_zero_count=sum(1 for value in alpha_values if value == 0),
        alpha_distinct_count=len(set(alpha_values)),
        beta_distinct_histogram=histogram(beta_distinct_counts),
        beta_mismatch_count=beta_mismatches,
        left_sign_normalized_right_mismatches=right_mismatches,
        left_sign_normalized_right_classes=len(by_right),
    )


def scan(args: argparse.Namespace) -> OriginProductAudit | None:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    seen: set[int] = set()
    cases = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (args.min_h <= h <= args.max_h):
            continue
        quotient_sizes = quotient_sizes_any(
            h,
            max_prime=args.max_prime_quotients,
            max_composite=args.max_composite_quotients,
            min_n=args.min_n,
            max_n=args.max_n,
        )
        quotient_sizes = [
            m
            for m in quotient_sizes
            if gcd(m, h // m) == 1
            and m <= args.max_m
            and (args.only_m is None or m == args.only_m)
            and len([c for c in coprime_components(m) if c > 2]) >= 2
        ]
        if not quotient_sizes:
            continue
        splits = find_splitting_primes(
            pari,
            hilbert,
            h,
            args.q_start,
            args.q_stop,
            args.max_splitting_primes,
        )
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                components = tuple(c for c in coprime_components(m) if c > 2)
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in components:
                        if args.only_left and left != args.only_left:
                            continue
                        for right in components:
                            if args.only_right and right != args.only_right:
                                continue
                            row = audit_case(
                                D, q, ell, cycle, m, factor, left, right
                            )
                            if row is not None:
                                return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    args = parser.parse_args()

    row = scan(args)
    if row is None:
        raise SystemExit("no eligible case found")
    print("Centered marginal origin-product audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"pair=({row.left},{row.right})")
    print()
    print("alpha_values_prefix")
    for alpha, value in list(enumerate(row.alpha_values))[:40]:
        print(f"  alpha={alpha:3d} det={value}")
    print()
    print("summary")
    print(f"  alpha_count={len(row.alpha_values)}")
    print(f"  alpha_zero_count={row.alpha_zero_count}")
    print(f"  alpha_distinct_count={row.alpha_distinct_count}")
    print(f"  alpha_product={row.alpha_product}")
    print(f"  beta_distinct_histogram={dict(row.beta_distinct_histogram)}")
    print(f"  beta_mismatch_count={row.beta_mismatch_count}")
    print(
        "  left_sign_normalized_right_mismatches="
        f"{row.left_sign_normalized_right_mismatches}"
    )
    print(
        "  left_sign_normalized_right_classes="
        f"{row.left_sign_normalized_right_classes}"
    )
    print()
    print("interpretation")
    print("  beta_shift_invariance_tests_hermitian_origin_cancellation=1")
    print("  alpha_dependence_factors_through_right_translation_up_to_left_sign=1")
    print("  alpha_product_packages_origin_translated_leading_minors=1")
    print("conclusion=reported_centered_marginal_origin_product_audit")


if __name__ == "__main__":
    main()
