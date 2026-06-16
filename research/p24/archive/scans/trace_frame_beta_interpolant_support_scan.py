#!/usr/bin/env python3
"""Scan beta-interpolant support for trace-frame determinant sequences.

For a fixed alpha, the beta-shifted determinant sequence

    D_beta = Delta_lead(theta^(-beta))

has a unique cyclic interpolant `f(Y)` modulo `Y^n-1`.  The p24 norm route
does not want to carry this interpolant literally, but its support pattern is
useful theorem evidence: a sparse or orbit-sparse full-leading interpolant
would point to a determinant-line identity, while dense residual-tail support
warns that a basis-dependent tail determinant is the wrong scalar payload.

This scan is intentionally cheaper than `trace_frame_beta_product_resultant`:
it interpolates compact rows and records support/orbit support, but it does
not build the full cyclic resultant determinant.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import equal_degree_factors, sympy_factor_to_poly_e
from k_character_tensor_rank_scan import ExtensionField, FpE, find_irreducible_modulus
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any
from tensor_factor_dual_basis_window_audit import theta_element
from tensor_factor_moore_audit import b_is_zero, b_pow
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_beta_product_resultant_audit import (
    PolyB,
    b_lands_in_E,
    b_subfield_degree,
    beta_orbits,
    cyclic_interpolation_coeffs,
    seed_rank,
)
from trace_frame_residual_tail_origin_action_audit import OriginTailRow, rows_for_case


@dataclass(frozen=True)
class CaseData:
    D: int
    q: int
    ell: int
    cycle: list[int]
    m: int
    factor: sp.Poly


@dataclass(frozen=True)
class SupportRow:
    D: int
    q: int
    h: int
    m: int
    n: int
    target: str
    subdegree: int
    determinant_kind: str
    raw_rank: int
    top_count: int
    residual_dim: int
    beta_values: int
    beta_distinct: int
    beta_zero_count: int
    support: int
    e_coefficients: int
    subfield_histogram: tuple[tuple[int, int], ...]
    coefficient_orbit_count: int
    coefficient_orbit_support: int
    coefficient_orbit_length_histogram: tuple[tuple[int, int], ...]
    seed_rank_histogram: tuple[tuple[int, int], ...]
    normal_seed_count: int
    value_orbit_constant_count: int


def find_cases(args: argparse.Namespace) -> list[CaseData]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[CaseData] = []
    seen: set[int] = set()
    discriminants_seen = 0
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
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
        if args.only_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m == args.only_m]
        if args.max_m is not None:
            quotient_sizes = [m for m in quotient_sizes if m <= args.max_m]
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
        if not splits:
            continue
        discriminants_seen += 1
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    out.append(CaseData(D, q, ell, cycle, m, factor))
                    if len(out) >= args.max_cases:
                        return out
        if discriminants_seen >= args.max_discriminants:
            break
    return out


def summarize_group(
    group_rows: list[OriginTailRow],
    selected_factor: PolyB,
    factor_degree: int,
    field: ExtensionField,
    determinant_kind: str,
) -> SupportRow | None:
    n = group_rows[0].n
    by_beta: dict[int, FpE] = {}
    for row in group_rows:
        if row.alpha != 0:
            continue
        value = row.full_det if determinant_kind == "full" else row.tail_det
        if value is None:
            continue
        by_beta[row.beta] = value
    if len(by_beta) != n:
        return None

    values = [by_beta[beta] for beta in range(n)]
    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    coeffs = cyclic_interpolation_coeffs(
        values,
        theta_inv,
        theta,
        selected_factor,
        field,
    )
    Q_mod_n = pow(field.q, field.degree, n)
    coefficient_orbits = beta_orbits(n, Q_mod_n)
    nonzero_coeffs = [coeff for coeff in coeffs if not b_is_zero(coeff, field)]
    subfield_hist = Counter(
        b_subfield_degree(coeff, factor_degree, selected_factor, field)
        for coeff in nonzero_coeffs
    )
    seed_ranks = [
        seed_rank(coeffs[orbit[0]], factor_degree, selected_factor, field)
        for orbit in coefficient_orbits
        if not b_is_zero(coeffs[orbit[0]], field)
    ]
    first = group_rows[0]
    return SupportRow(
        D=first.D,
        q=first.q,
        h=first.h,
        m=first.m,
        n=first.n,
        target=first.target,
        subdegree=first.subdegree,
        determinant_kind=determinant_kind,
        raw_rank=first.raw_rank,
        top_count=first.top_count,
        residual_dim=first.residual_dim,
        beta_values=len(values),
        beta_distinct=len(set(values)),
        beta_zero_count=sum(1 for value in values if value == field.zero),
        support=len(nonzero_coeffs),
        e_coefficients=sum(1 for coeff in coeffs if b_lands_in_E(coeff, field)),
        subfield_histogram=tuple(sorted(subfield_hist.items())),
        coefficient_orbit_count=len(coefficient_orbits),
        coefficient_orbit_support=sum(
            1 for orbit in coefficient_orbits
            if not b_is_zero(coeffs[orbit[0]], field)
        ),
        coefficient_orbit_length_histogram=tuple(sorted(
            Counter(len(orbit) for orbit in coefficient_orbits).items()
        )),
        seed_rank_histogram=tuple(sorted(Counter(seed_ranks).items())),
        normal_seed_count=sum(1 for rank in seed_ranks if rank == factor_degree),
        value_orbit_constant_count=sum(
            1 for orbit in coefficient_orbits
            if len({values[beta] for beta in orbit}) == 1
        ),
    )


def scan_case(case: CaseData, args: argparse.Namespace) -> list[SupportRow]:
    extension_degree = int(sp.n_order(case.q % case.m, case.m))
    modulus = find_irreducible_modulus(case.q, extension_degree, args.seed)
    field = ExtensionField(case.q, extension_degree, modulus)
    factor_degree = case.factor.degree() // int(sp.igcd(case.factor.degree(), extension_degree))
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(case.factor, field),
        factor_degree,
        field,
        args.seed,
    )[0]
    try:
        rows = rows_for_case(
            case.D,
            case.q,
            case.ell,
            case.cycle,
            case.m,
            case.factor,
            args.target or ["axis"],
            args.seed,
            args.max_top_count,
        )
    except ValueError:
        return []
    groups: dict[tuple[str, int], list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        groups[(row.target, row.subdegree)].append(row)

    out: list[SupportRow] = []
    for group in groups.values():
        full = summarize_group(group, selected_factor, factor_degree, field, "full")
        if full is not None:
            out.append(full)
        if all(row.tail_det is not None for row in group):
            tail = summarize_group(group, selected_factor, factor_degree, field, "tail")
            if tail is not None:
                out.append(tail)
    return out


def fmt_hist(hist: tuple[tuple[int, int], ...]) -> str:
    return "[" + ",".join(f"{degree}:{count}" for degree, count in hist) + "]"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=30000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--max-discriminants", type=int, default=2000)
    ap.add_argument("--min-h", type=int, default=24)
    ap.add_argument("--max-h", type=int, default=220)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=120)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=30000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=48)
    ap.add_argument("--max-composite-quotients", type=int, default=48)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=1)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument(
        "--target",
        action="append",
        help="Target such as axis, constant_plus_4, constant_plus_3.",
    )
    args = ap.parse_args()

    cases = find_cases(args)
    rows: list[SupportRow] = []
    for case in cases:
        rows.extend(scan_case(case, args))

    print("trace-frame beta-interpolant support scan")
    print(f"cases={len(cases)}")
    print(f"rows={len(rows)}")
    print(
        "columns: D q h m n target subdeg kind raw top residual_dim "
        "beta distinct zeros support E_coeffs subfield_hist "
        "coeff_orbits coeff_orbit_support coeff_orbit_lengths "
        "seed_rank_hist normal_seeds value_orbit_constants"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} h={row.h} m={row.m} n={row.n} "
            f"target={row.target} subdeg={row.subdegree} "
            f"kind={row.determinant_kind} raw={row.raw_rank} "
            f"top={row.top_count} residual_dim={row.residual_dim} "
            f"beta={row.beta_values} distinct={row.beta_distinct} "
            f"zeros={row.beta_zero_count} support={row.support} "
            f"E_coeffs={row.e_coefficients} "
            f"subfield_hist={fmt_hist(row.subfield_histogram)} "
            f"coeff_orbits={row.coefficient_orbit_count} "
            f"coeff_orbit_support={row.coefficient_orbit_support} "
            f"coeff_orbit_lengths={fmt_hist(row.coefficient_orbit_length_histogram)} "
            f"seed_rank_hist={fmt_hist(row.seed_rank_histogram)} "
            f"normal_seeds={row.normal_seed_count} "
            f"value_orbit_constants={row.value_orbit_constant_count}"
        )
    print()
    print("interpretation")
    print("  support<n means the beta determinant sequence has a sparse cyclic interpolant.")
    print("  coeff_orbit_support<coeff_orbits means Frobenius-orbit sparsity survives semilinear descent.")
    print("  full rows are the determinant-line object; tail rows are basis-dependent diagnostics.")
    print("conclusion=reported_trace_frame_beta_interpolant_support_scan")


if __name__ == "__main__":
    main()
