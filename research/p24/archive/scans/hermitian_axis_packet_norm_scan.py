#!/usr/bin/env python3
"""Packet norm scan for Hermitian axis Gram determinants.

Origin invariance reduces the Hermitian axis determinant to one value per
H-character packet.  This script groups those packet determinant values and
computes their product over packet factors, the finite-field analogue of the
decomposition-field norm.

The p24 theorem should be phrased as a p-unit statement for this packet norm:

    product_a det(H_a) != 0 mod p.

This is equivalent to every packet determinant being nonzero over a field, but
it packages the eight p24 packet checks into one scalar.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

from hermitian_gram_determinant_distribution import DetRow, scan


@dataclass(frozen=True)
class NormRow:
    D: int
    q: int
    ell: int
    m: int
    n: int
    packet_count: int
    factor_degrees: tuple[int, ...]
    axis_dim: int
    packet_values: tuple[int, ...]
    packet_norm: int
    origin_invariant: bool
    zero_packets: int


def group_key(row: DetRow) -> tuple[int, int, int, int, int]:
    return (row.D, row.q, row.ell, row.m, row.n)


def collapse_packet_values(rows: list[DetRow]) -> tuple[bool, dict[int, DetRow]]:
    by_factor: dict[int, list[DetRow]] = {}
    for row in rows:
        by_factor.setdefault(row.factor_index, []).append(row)
    invariant = True
    collapsed: dict[int, DetRow] = {}
    for factor_index, group in by_factor.items():
        values = {row.determinant for row in group}
        if len(values) != 1:
            invariant = False
        collapsed[factor_index] = group[0]
    return invariant, collapsed


def norm_rows(rows: list[DetRow]) -> list[NormRow]:
    groups: dict[tuple[int, int, int, int, int], list[DetRow]] = {}
    for row in rows:
        if row.determinant is None:
            continue
        groups.setdefault(group_key(row), []).append(row)

    out: list[NormRow] = []
    for key, group in sorted(groups.items()):
        D, q, ell, m, n = key
        invariant, collapsed = collapse_packet_values(group)
        ordered = [collapsed[index] for index in sorted(collapsed)]
        values = tuple(int(row.determinant or 0) % q for row in ordered)
        packet_norm = 1
        for value in values:
            packet_norm = (packet_norm * value) % q
        out.append(
            NormRow(
                D=D,
                q=q,
                ell=ell,
                m=m,
                n=n,
                packet_count=len(values),
                factor_degrees=tuple(row.factor_degree for row in ordered),
                axis_dim=ordered[0].axis_dim if ordered else 0,
                packet_values=values,
                packet_norm=packet_norm,
                origin_invariant=invariant,
                zero_packets=sum(1 for value in values if value == 0),
            )
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=120)
    parser.add_argument("--max-abs-D", type=int, default=25000)
    parser.add_argument("--max-prime-quotients", type=int, default=6)
    parser.add_argument("--max-composite-quotients", type=int, default=6)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=120)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=250000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=45)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = norm_rows([row for row in scan(args) if row.determinant is not None])
    zero_norm_rows = [row for row in rows if row.packet_norm == 0]
    noninvariant_rows = [row for row in rows if not row.origin_invariant]
    multi_packet_rows = [row for row in rows if row.packet_count > 1]

    print("Hermitian axis packet-norm scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell m n packet_count degrees axis_dim "
            "zero_packets packet_norm origin_invariant packet_values"
        )
        display = zero_norm_rows + noninvariant_rows
        if not display:
            display = rows[:80]
        for row in display[:120]:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"m={row.m:3d} n={row.n:3d} packets={row.packet_count:2d} "
                f"degrees={list(row.factor_degrees)} axis_dim={row.axis_dim:3d} "
                f"zero_packets={row.zero_packets:2d} "
                f"packet_norm={row.packet_norm:7d} "
                f"origin_invariant={int(row.origin_invariant)} "
                f"packet_values={list(row.packet_values)}"
            )

    print()
    print("summary")
    print(f"  norm_rows={len(rows)}")
    print(f"  multi_packet_rows={len(multi_packet_rows)}")
    print(f"  zero_packet_norm_rows={len(zero_norm_rows)}")
    print(f"  non_origin_invariant_rows={len(noninvariant_rows)}")
    if rows:
        max_packets = max(row.packet_count for row in rows)
        print(f"  max_packet_count={max_packets}")
    print()
    print("interpretation")
    print("  packet_norm_nonzero_iff_every_packet_determinant_nonzero=1")
    print("  origin_invariance_allows_one_value_per_packet_factor=1")
    print("  p24_target_is_degree8_packet_norm_punit=1")
    print("conclusion=reported_hermitian_axis_packet_norm_scan")


if __name__ == "__main__":
    main()
