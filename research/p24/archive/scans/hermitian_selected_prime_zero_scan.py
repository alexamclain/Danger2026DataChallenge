#!/usr/bin/env python3
"""Selected-prime zero distribution for packet scalars.

The p24 Hermitian target is a selected-prime p-unit statement, not a global
norm statement.  This bounded toy scan rotates complete small CM cycles through
all embedded roots and records whether Hermitian packet zeros occur for one
selected embedding, for an entire packet norm, or across the full class orbit.

For a cycle ``j_i`` and quotient ``h=m*n`` it computes the carry-adjusted
Hermitian packet polynomial

    H(X) = sum_u X^c(u) J_u(X) J_{-u}(X),

modulo each Frobenius factor of Phi_n over the split base field.  Rotating the
cycle models choosing a different prime above the same split rational prime.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from packetized_relative_content_scan import (
    autocorrelation_energy_poly,
    hermitian_energy_poly,
    packet_factors,
    quotient_sizes_with_prime_subgroup,
)


@dataclass(frozen=True)
class PacketOrbitRow:
    scalar: str
    quotient_m: int
    subgroup_n: int
    factor_degree: int
    selected_zero_origin0: bool
    packet_norm_zero_origin0: bool
    selected_packet_norm_mismatch: bool
    zero_count_across_origins: int
    zero_origins_sample: tuple[int, ...]


@dataclass(frozen=True)
class ScanRow:
    D: int
    q: int
    ell: int
    h: int
    packets: tuple[PacketOrbitRow, ...]


def rotate(cycle: list[int], shift: int) -> list[int]:
    if shift == 0:
        return cycle
    return cycle[shift:] + cycle[:shift]


def scalar_poly(cycle: list[int], q: int, m: int, scalar: str) -> sp.Poly:
    if scalar == "hermitian":
        return hermitian_energy_poly(cycle, q, m)
    if scalar == "ordinary":
        return autocorrelation_energy_poly(cycle, q, m)
    raise ValueError(f"unknown scalar {scalar}")


def scalar_zero_for_factor(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> bool:
    return scalar_poly(cycle, q, m, scalar).rem(factor).is_zero


def packet_norm_zero_for_factor(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> bool:
    X = factor.gens[0]
    packet_poly = scalar_poly(cycle, q, m, scalar)
    resultant = int(sp.resultant(factor.as_expr(), packet_poly.as_expr(), X)) % q
    return resultant == 0


def audit_packet_orbit(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> PacketOrbitRow:
    h = len(cycle)
    origin0_zero = scalar_zero_for_factor(cycle, q, m, factor, scalar)
    origin0_norm_zero = packet_norm_zero_for_factor(cycle, q, m, factor, scalar)
    mismatch = origin0_zero != origin0_norm_zero

    zero_origins: list[int] = []
    for shift in range(h):
        if scalar_zero_for_factor(rotate(cycle, shift), q, m, factor, scalar):
            zero_origins.append(shift)

    return PacketOrbitRow(
        scalar=scalar,
        quotient_m=m,
        subgroup_n=h // m,
        factor_degree=factor.degree(),
        selected_zero_origin0=origin0_zero,
        packet_norm_zero_origin0=origin0_norm_zero,
        selected_packet_norm_mismatch=mismatch,
        zero_count_across_origins=len(zero_origins),
        zero_origins_sample=tuple(zero_origins[:12]),
    )


def scan(
    max_cases: int,
    min_h: int,
    max_h: int,
    max_abs_D: int,
    max_quotients: int,
    min_n: int,
    q_start: int,
    q_stop: int,
    nonlinear_only: bool,
    scalar: str,
) -> list[ScanRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    out: list[ScanRow] = []
    seen: set[int] = set()
    for D in discriminants:
        if D in seen:
            continue
        seen.add(D)
        try:
            hilbert = pari.polclass(D)
            h = int(pari.poldegree(hilbert))
        except Exception:
            continue
        if not (min_h <= h <= max_h):
            continue
        quotient_sizes = quotient_sizes_with_prime_subgroup(h, max_quotients, min_n)
        if not quotient_sizes:
            continue
        split = find_splitting_prime(pari, hilbert, h, q_start, q_stop)
        if split is None:
            continue
        q, roots = split
        full = find_full_cycle_prime(roots, D, q)
        if full is None:
            continue
        ell, cycle = full
        packets: list[PacketOrbitRow] = []
        for m in quotient_sizes:
            n = h // m
            for factor in packet_factors(n, q):
                if nonlinear_only and factor.degree() == 1:
                    continue
                packets.append(audit_packet_orbit(cycle, q, m, factor, scalar))
        if packets:
            out.append(ScanRow(D=D, q=q, ell=ell, h=h, packets=tuple(packets)))
        if len(out) >= max_cases:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=20)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=80)
    ap.add_argument("--max-abs-D", type=int, default=12000)
    ap.add_argument("--max-quotients", type=int, default=3)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=150000)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--scalar", choices=("hermitian", "ordinary"), default="hermitian")
    ap.add_argument("--summary-only", action="store_true")
    args = ap.parse_args()

    rows = scan(
        max_cases=args.max_cases,
        min_h=args.min_h,
        max_h=args.max_h,
        max_abs_D=args.max_abs_D,
        max_quotients=args.max_quotients,
        min_n=args.min_n,
        q_start=args.q_start,
        q_stop=args.q_stop,
        nonlinear_only=not args.include_linear,
        scalar=args.scalar,
    )

    print("selected-prime packet-scalar zero distribution scan")
    print(f"scalar={args.scalar}")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"min_n={args.min_n}")
    print(f"q_stop={args.q_stop}")
    print(f"include_linear={args.include_linear}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h scalar m n factor_degree selected_zero_origin0 "
            "packet_norm_zero_origin0 mismatch zero_count zero_origins_sample"
        )
        for row in rows:
            for packet in row.packets:
                print(
                    f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                    f"scalar={packet.scalar:9s} "
                    f"m={packet.quotient_m:3d} n={packet.subgroup_n:3d} "
                    f"factor_degree={packet.factor_degree:3d} "
                    f"selected_zero_origin0={int(packet.selected_zero_origin0)} "
                    f"packet_norm_zero_origin0={int(packet.packet_norm_zero_origin0)} "
                    f"mismatch={int(packet.selected_packet_norm_mismatch)} "
                    f"zero_count={packet.zero_count_across_origins:3d} "
                    f"zero_origins_sample={list(packet.zero_origins_sample)}"
                )

    packets = [packet for row in rows for packet in row.packets]
    zero_packets = [packet for packet in packets if packet.zero_count_across_origins]
    full_orbit_zero_packets = [
        (row, packet)
        for row in rows
        for packet in row.packets
        if packet.zero_count_across_origins == row.h
    ]
    isolated_zero_packets = [
        (row, packet)
        for row in rows
        for packet in row.packets
        if 0 < packet.zero_count_across_origins < row.h
    ]
    mismatches = sum(1 for packet in packets if packet.selected_packet_norm_mismatch)
    origin0_zeros = sum(1 for packet in packets if packet.selected_zero_origin0)
    total_selected_tests = sum(row.h * len(row.packets) for row in rows)
    total_selected_zeros = sum(packet.zero_count_across_origins for packet in packets)

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  packet_rows={len(packets)}")
    print(f"  selected_embedding_tests={total_selected_tests}")
    print(f"  selected_embedding_zeros={total_selected_zeros}")
    print(f"  origin0_zero_packets={origin0_zeros}")
    print(f"  packet_rows_with_any_selected_zero={len(zero_packets)}")
    print(f"  packet_rows_with_full_orbit_zero={len(full_orbit_zero_packets)}")
    print(f"  packet_rows_with_isolated_or_partial_zeros={len(isolated_zero_packets)}")
    print(f"  selected_vs_packet_norm_mismatches={mismatches}")
    if isolated_zero_packets[:8]:
        print("  isolated_or_partial_zero_samples=")
        for row, packet in isolated_zero_packets[:8]:
            print(
                f"    D={row.D} q={row.q} h={row.h} m={packet.quotient_m} "
                f"n={packet.subgroup_n} deg={packet.factor_degree} "
                f"zero_count={packet.zero_count_across_origins} "
                f"origins={list(packet.zero_origins_sample)}"
            )
    print()
    print("interpretation")
    print("  selected_embedding_zero_tests_the_selected_prime_punit_issue=1")
    print("  zero_count_across_origins_models_full_class_norm_divisibility=1")
    print("  mismatch_zero_should_be_0_for_irreducible_packet_norm_identity=1")
    print("  hermitian_no_zeros_supports_packet_punit_heuristic_not_proof=1")
    print("  ordinary_energy_mode_is_a_control_for_scalar_cancellation_failures=1")
    print("conclusion=reported_hermitian_selected_prime_zero_scan")


if __name__ == "__main__":
    main()
