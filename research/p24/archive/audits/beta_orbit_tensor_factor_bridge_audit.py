#!/usr/bin/env python3
"""Multi-case audit for the beta-orbit / tensor-factor bridge.

The p24 bridge says that after adjoining E=F_p(mu_m), the nonzero beta
Frobenius orbits are exactly the scalar-extension tensor factors inside the
eight H-packets:

    560 = 8 * 70.

This script checks the same finite-field bookkeeping and crossed-product
orbit determinant identities in several small CM rows.  It deliberately keeps
the window small; the point is to test theorem shape, not to spend CPU on
large class sets.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
)
from tensor_factor_subfield_trace_audit import divisors
from trace_frame_residual_tail_origin_action_audit import OriginTailRow, rows_for_case
from trace_frame_trace_sum_crossed_product_audit import summarize_group


@dataclass(frozen=True)
class Case:
    D: int
    q: int
    ell: int
    cycle: list[int]
    m: int
    factor: sp.Poly


@dataclass(frozen=True)
class BridgeSummary:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    target: str
    subdegree: int
    determinant_kind: str
    packet_degree: int
    extension_degree: int
    tensor_factor_count: int
    tensor_factor_degree: int
    h_packet_count: int
    e_orbit_size: int
    e_orbit_count: int
    bridge_count_match: bool
    orbit_rows: int
    nonzero_orbits: int
    nonzero_orbit_rows: int
    block_match_rows: int
    block_in_e_rows: int
    zero_block_rows: int
    ordinary_power_fail_nonconstant: int


def eligible_cases(args: argparse.Namespace) -> list[Case]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    out: list[Case] = []
    seen: set[int] = set()
    scanned_discriminants = 0
    for D in discriminants(args.max_abs_D, args.only_D):
        if D in seen:
            continue
        seen.add(D)
        scanned_discriminants += 1
        if scanned_discriminants > args.max_discriminants:
            break
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
        if args.require_prime_n:
            quotient_sizes = [m for m in quotient_sizes if sp.isprime(h // m)]
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
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            ell, cycle = full
            for m in quotient_sizes:
                n = h // m
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    tensor_factor_count = int(sp.igcd(factor.degree(), extension_degree))
                    if tensor_factor_count < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // tensor_factor_count
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    out.append(Case(D, q, ell, cycle, m, factor))
                    if len(out) >= args.max_cases:
                        return out
    return out


def summarize_case(case: Case, args: argparse.Namespace) -> list[BridgeSummary]:
    D, q, ell, cycle, m, factor = (
        case.D,
        case.q,
        case.ell,
        case.cycle,
        case.m,
        case.factor,
    )
    h = len(cycle)
    n = h // m
    packet_degree = factor.degree()
    extension_degree = int(sp.n_order(q % m, m))
    tensor_factor_count = int(sp.igcd(packet_degree, extension_degree))
    tensor_factor_degree = packet_degree // tensor_factor_count
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        args.seed,
    )[0]

    rows = rows_for_case(
        D,
        q,
        ell,
        cycle,
        m,
        factor,
        args.target or ["axis"],
        args.seed,
        args.max_top_count,
    )
    groups: dict[tuple[str, int], list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        groups[(row.target, row.subdegree)].append(row)

    h_packet_count = int(sp.totient(n)) // packet_degree
    e_multiplier = pow(q, extension_degree, n)
    e_orbit_size = int(sp.n_order(e_multiplier, n))
    e_orbit_count = int(sp.totient(n)) // e_orbit_size
    bridge_count_match = e_orbit_count == h_packet_count * tensor_factor_count

    out: list[BridgeSummary] = []
    for (target, subdegree), group in sorted(groups.items()):
        for kind in ("full", "tail"):
            if kind == "tail" and not all(row.tail_det is not None for row in group):
                continue
            orbit_rows = summarize_group(
                group,
                selected_factor,
                tensor_factor_degree,
                field,
                kind,
            )
            if not orbit_rows:
                continue
            out.append(
                BridgeSummary(
                    D=D,
                    q=q,
                    ell=ell,
                    h=h,
                    m=m,
                    n=n,
                    target=target,
                    subdegree=subdegree,
                    determinant_kind=kind,
                    packet_degree=packet_degree,
                    extension_degree=extension_degree,
                    tensor_factor_count=tensor_factor_count,
                    tensor_factor_degree=tensor_factor_degree,
                    h_packet_count=h_packet_count,
                    e_orbit_size=e_orbit_size,
                    e_orbit_count=e_orbit_count,
                    bridge_count_match=bridge_count_match,
                    orbit_rows=len(orbit_rows),
                    nonzero_orbits=sum(1 for row in orbit_rows if row["orbit_rep"] != 0),
                    nonzero_orbit_rows=sum(
                        1 for row in orbit_rows
                        if row["orbit_rep"] != 0 and not row["block_det_zero"]
                    ),
                    block_match_rows=sum(int(row["block_det_match"]) for row in orbit_rows),
                    block_in_e_rows=sum(int(row["block_det_in_E"]) for row in orbit_rows),
                    zero_block_rows=sum(int(row["block_det_zero"]) for row in orbit_rows),
                    ordinary_power_fail_nonconstant=sum(
                        1 for row in orbit_rows
                        if not row["value_constant"] and not row["ordinary_power_match"]
                    ),
                )
            )
    return out


def audit(args: argparse.Namespace) -> list[BridgeSummary]:
    summaries: list[BridgeSummary] = []
    for case in eligible_cases(args):
        summaries.extend(summarize_case(case, args))
    return summaries


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=40000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--max-discriminants", type=int, default=120)
    ap.add_argument("--min-h", type=int, default=24)
    ap.add_argument("--max-h", type=int, default=220)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--max-n", type=int, default=80)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=30000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=32)
    ap.add_argument("--max-composite-quotients", type=int, default=16)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=2)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-prime-n", action=argparse.BooleanOptionalAction, default=True)
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument("--target", action="append")
    args = ap.parse_args()

    rows = audit(args)
    print("beta-orbit tensor-factor bridge multi-case audit")
    print(f"rows={len(rows)}")
    print(
        "columns: D q ell h m n target subdeg kind packet_deg E_deg "
        "tensor_count tensor_deg H_packets E_orbit_size E_orbits "
        "bridge_match orbit_rows nonzero_orbits nonzero_orbit_rows "
        "block_match_rows block_in_E_rows zero_block_rows "
        "ordinary_power_fail_nonconstant"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"target={row.target} subdeg={row.subdegree} kind={row.determinant_kind} "
            f"packet_deg={row.packet_degree} E_deg={row.extension_degree} "
            f"tensor_count={row.tensor_factor_count} tensor_deg={row.tensor_factor_degree} "
            f"H_packets={row.h_packet_count} E_orbit_size={row.e_orbit_size} "
            f"E_orbits={row.e_orbit_count} bridge_match={int(row.bridge_count_match)} "
            f"orbit_rows={row.orbit_rows} nonzero_orbits={row.nonzero_orbits} "
            f"nonzero_orbit_rows={row.nonzero_orbit_rows} "
            f"block_match_rows={row.block_match_rows} "
            f"block_in_E_rows={row.block_in_e_rows} "
            f"zero_block_rows={row.zero_block_rows} "
            f"ordinary_power_fail_nonconstant={row.ordinary_power_fail_nonconstant}"
        )
    print()
    print("interpretation")
    print("  bridge_match=1 verifies E-orbits refine H-packets by tensor factor count.")
    print("  block_match_rows=orbit_rows verifies the crossed-product block identity.")
    print("  block_in_E_rows=orbit_rows verifies each orbit block descends to E.")
    print("  zero_block_rows=0 is small-data support for the p-unit theorem.")
    print("  ordinary_power_fail_nonconstant>0 rules out ordinary norm collapse.")
    print("conclusion=reported_beta_orbit_tensor_factor_bridge_multicase_audit")


if __name__ == "__main__":
    main()
