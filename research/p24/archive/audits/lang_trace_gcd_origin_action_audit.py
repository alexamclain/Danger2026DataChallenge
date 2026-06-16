#!/usr/bin/env python3
"""Origin-action audit for the Lang trace-gcd tail determinant.

The p24 representative trace-gcd determinant is attached to a selected CM
origin/embedding.  This script tests, in small actual-CM rows, how the
tail-on-kernel determinant changes when the CM cycle origin is shifted.

For h=m*n, write an origin shift as

    shift == n*alpha + m*beta mod h.

The script reports determinant variation over all shifts and separately along
pure alpha and pure beta directions.  Stable nonvanishing would support a
norm/product p-unit package; many unrelated values suggest the determinant is
selected-origin data rather than an easy invariant.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from lang_arc_strength_audit import transformed_blocks_for_row
from lang_trace_gcd_kernel_audit import trace_gcd_profile
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
)


@dataclass(frozen=True)
class OriginDet:
    shift: int
    alpha: int
    beta: int
    omitted: int
    prefix_len: int
    tail_len: int
    kernel_dim: int
    tail_rank: int
    gcd_degree: int
    determinant: int | None


@dataclass(frozen=True)
class OriginActionRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_lengths: tuple[int, ...]
    records: tuple[OriginDet, ...]


def crt_alpha_beta(shift: int, m: int, n: int) -> tuple[int, int]:
    # shift = n*alpha + m*beta mod m*n
    alpha = (shift * pow(n % m, -1, m)) % m
    beta = (shift * pow(m % n, -1, n)) % n
    return alpha, beta


def audit_origin_row(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    left: int,
    right: int,
    left_orbit: list[int],
    args: argparse.Namespace,
) -> OriginActionRow | None:
    h = len(cycle)
    n = h // m
    records: list[OriginDet] = []
    right_lengths: tuple[int, ...] | None = None
    extension_degree: int | None = None
    max_shift = h if args.max_origin_shifts is None else min(h, args.max_origin_shifts)
    for shift in range(max_shift):
        shifted = rotate(cycle, shift)
        try:
            ext_degree, field, blocks = transformed_blocks_for_row(
                D, q, ell, shifted, m, factor, left, right, left_orbit, args.seed
            )
        except ValueError:
            continue
        extension_degree = ext_degree
        right_lengths = tuple(len(block) for block in blocks)
        basis = None
        # `trace_gcd_profile` needs a left-subfield basis; construct lazily via
        # the imported function's helper path by using its own internal basis is
        # not available, so import here to avoid a circular top-level dependency.
        from hermitian_mixed_left_subfield_normality_audit import subfield_power_basis

        basis = subfield_power_basis(q, len(left_orbit), field, args.seed)
        for omitted in range(len(blocks)):
            if args.only_omitted is not None and omitted != args.only_omitted:
                continue
            profile = trace_gcd_profile(
                blocks, omitted, len(left_orbit), q, field, basis
            )
            if profile is None:
                continue
            if args.require_square_tail and (
                profile.tail_len != profile.dual_kernel_dim
            ):
                continue
            alpha, beta = crt_alpha_beta(shift, m, n)
            records.append(
                OriginDet(
                    shift=shift,
                    alpha=alpha,
                    beta=beta,
                    omitted=omitted,
                    prefix_len=profile.prefix_len,
                    tail_len=profile.tail_len,
                    kernel_dim=profile.dual_kernel_dim,
                    tail_rank=profile.tail_rank_on_kernel,
                    gcd_degree=profile.trace_gcd_degree,
                    determinant=profile.tail_kernel_det,
                )
            )
    if not records or right_lengths is None or extension_degree is None:
        return None
    return OriginActionRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=len(left_orbit),
        right_orbit_lengths=right_lengths,
        records=tuple(records),
    )


def first_row(args: argparse.Namespace) -> OriginActionRow | None:
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
            and len([component for component in coprime_components(m) if component > 2])
            >= 2
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
            if args.only_q is not None and q != args.only_q:
                continue
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < args.min_factor_degree:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    for left in coprime_components(m):
                        if left <= 2 or (args.only_left and left != args.only_left):
                            continue
                        for right in coprime_components(m):
                            if right <= 2 or (args.only_right and right != args.only_right):
                                continue
                            right_orbits = q_orbits(right, q)
                            if len(right_orbits) < args.min_right_orbits:
                                continue
                            for left_orbit in q_orbits(left, q):
                                if len(left_orbit) < args.min_left_orbit_len:
                                    continue
                                row = audit_origin_row(
                                    D,
                                    q,
                                    ell,
                                    cycle,
                                    m,
                                    factor,
                                    left,
                                    right,
                                    left_orbit,
                                    args,
                                )
                                if row is not None:
                                    return row
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return None


def value_summary(values: list[int | None]) -> tuple[int, int, int]:
    zeros = sum(1 for value in values if value == 0)
    nonnull = [value for value in values if value is not None]
    distinct = len(set(nonnull))
    missing = sum(1 for value in values if value is None)
    return zeros, distinct, missing


def product_mod(values: list[int | None], modulus: int) -> int | None:
    product = 1
    for value in values:
        if value is None:
            return None
        product = (product * (value % modulus)) % modulus
    return product


def fixed_group_products(
    records: list[OriginDet], key: str, modulus: int
) -> list[tuple[int, int | None]]:
    groups: dict[int, list[int | None]] = {}
    for record in records:
        groups.setdefault(getattr(record, key), []).append(record.determinant)
    return [
        (group_key, product_mod(values, modulus))
        for group_key, values in sorted(groups.items())
    ]


def cyclic_period(values: list[object]) -> int | None:
    if not values:
        return None
    n = len(values)
    for period in range(1, n + 1):
        if n % period != 0:
            continue
        if all(values[index] == values[index % period] for index in range(n)):
            return period
    return None


def fixed_value_period(records: list[OriginDet], key: str) -> int | None:
    groups: dict[int, set[int | None]] = {}
    for record in records:
        groups.setdefault(getattr(record, key), set()).add(record.determinant)
    if sorted(groups) != list(range(len(groups))):
        return None
    values = [tuple(sorted(groups[index], key=lambda value: (-1 if value is None else value))) for index in range(len(groups))]
    return cyclic_period(values)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=24)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=12)
    parser.add_argument("--max-composite-quotients", type=int, default=24)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=600000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--max-m", type=int, default=120)
    parser.add_argument("--min-factor-degree", type=int, default=1)
    parser.add_argument("--max-factor-degree", type=int, default=12)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-left-orbit-len", type=int, default=2)
    parser.add_argument("--min-right-orbits", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--require-square-tail", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--max-origin-shifts", type=int)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-q", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--only-left", type=int)
    parser.add_argument("--only-right", type=int)
    parser.add_argument("--only-omitted", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    row = first_row(args)
    if row is None:
        raise SystemExit("no eligible origin-action row found")

    values = [record.determinant for record in row.records]
    zeros, distinct, missing = value_summary(values)
    bad_gcd = [record for record in row.records if record.gcd_degree != 0]
    print("Lang trace-gcd origin-action audit")
    print(f"D={row.D}")
    print(f"q={row.q}")
    print(f"ell={row.ell}")
    print(f"h={row.h}")
    print(f"m={row.m}")
    print(f"n={row.n}")
    print(f"factor_degree={row.factor_degree}")
    print(f"extension_degree={row.extension_degree}")
    print(f"pair=({row.left},{row.right})")
    print(f"left_orbit={row.left_orbit_rep}:L{row.left_orbit_len}")
    print(f"right_lengths={list(row.right_orbit_lengths)}")
    print(f"records={len(row.records)}")
    print(f"det_zero_count={zeros}")
    print(f"det_distinct_count={distinct}")
    print(f"det_missing_count={missing}")
    print(f"gcd_failure_count={len(bad_gcd)}")

    by_omitted: dict[int, list[OriginDet]] = {}
    for record in row.records:
        by_omitted.setdefault(record.omitted, []).append(record)
    for omitted, records in sorted(by_omitted.items()):
        vals = [record.determinant for record in records]
        o_zeros, o_distinct, o_missing = value_summary(vals)
        product_all = product_mod(vals, row.q)
        alpha_products = fixed_group_products(records, "alpha", row.q)
        beta_products = fixed_group_products(records, "beta", row.q)
        alpha_product_values = [value for _, value in alpha_products]
        beta_product_values = [value for _, value in beta_products]
        alpha_product_period = cyclic_period(alpha_product_values)
        beta_product_period = cyclic_period(beta_product_values)
        alpha_value_period = fixed_value_period(records, "alpha")
        beta_value_period = fixed_value_period(records, "beta")
        print(
            f"omitted={omitted} count={len(records)} zeros={o_zeros} "
            f"distinct={o_distinct} missing={o_missing} "
            f"sample={vals[:12]}"
        )
        print(f"  product_all_mod_q={product_all}")
        print(
            "  alpha_fixed_product_distinct="
            f"{len(set(alpha_product_values))} "
            f"period={alpha_product_period} "
            f"sample={alpha_products[:8]}"
        )
        print(
            "  beta_fixed_product_distinct="
            f"{len(set(beta_product_values))} "
            f"period={beta_product_period} "
            f"sample={beta_products[:8]}"
        )
        print(
            f"  alpha_value_period={alpha_value_period} "
            f"beta_value_period={beta_value_period}"
        )

    alpha_hist: dict[int, int] = {}
    beta_hist: dict[int, int] = {}
    for alpha in sorted({record.alpha for record in row.records}):
        vals = [record.determinant for record in row.records if record.alpha == alpha]
        alpha_hist[len(set(vals))] = alpha_hist.get(len(set(vals)), 0) + 1
    for beta in sorted({record.beta for record in row.records}):
        vals = [record.determinant for record in row.records if record.beta == beta]
        beta_hist[len(set(vals))] = beta_hist.get(len(set(vals)), 0) + 1
    print(f"alpha_fixed_distinct_hist={dict(sorted(alpha_hist.items()))}")
    print(f"beta_fixed_distinct_hist={dict(sorted(beta_hist.items()))}")

    print("interpretation")
    print("  zero_count_zero_supports_origin_product_punit_candidate=1")
    print("  many_distinct_values_means_not_a_literal_origin_invariant=1")
    print("  alpha_beta_hist_separates_CRT_origin_directions=1")
    print("conclusion=reported_lang_trace_gcd_origin_action_audit")


if __name__ == "__main__":
    main()
