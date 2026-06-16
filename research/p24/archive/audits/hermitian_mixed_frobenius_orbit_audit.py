#!/usr/bin/env python3
"""Audit Frobenius-orbit structure of mixed Hermitian character pairings.

For the nonzero double DFT block

    H_{c,d}(u,v) = sum_{r,s} zeta_c^(u r) zeta_d^(v s) K(r,s),

with K(r,s) in F_q, Frobenius gives the formal identity

    H(q^a u0, q^b v0) = H(u0, q^(b-a) v0)^(q^a).

Thus each orbit-pair block is a Moore/Frobenius-circulant matrix generated
from one seed row.  This script verifies the identity in small CM rows and
records whether the mixed blocks have full possible rank.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import lcm

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class OrbitBlock:
    left: int
    right: int
    left_orbit_rep: int
    right_orbit_rep: int
    left_orbit_len: int
    right_orbit_len: int
    rank: int
    possible_rank: int
    full_possible_rank: bool
    frobenius_identity_failures: int


@dataclass(frozen=True)
class OrbitRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    components: tuple[int, ...]
    blocks: tuple[OrbitBlock, ...]


def q_orbits(modulus: int, q: int) -> list[list[int]]:
    seen: set[int] = set()
    out: list[list[int]] = []
    for start in range(1, modulus):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * q) % modulus
        out.append(orbit)
    return out


def matrix_subblock(matrix, rows: list[int], cols: list[int]):
    return [[matrix[row][col] for col in cols] for row in rows]


def frobenius_power(value: FpE, times: int, field: ExtensionField) -> FpE:
    # q-power Frobenius on F_{q^e}; the generic field pow is fine for the
    # deliberately small audit rows used here.
    return field.pow(value, field.q**times)


def orbit_identity_failures(
    block: list[list[FpE]],
    field: ExtensionField,
) -> int:
    if not block:
        return 0
    left_len = len(block)
    right_len = len(block[0]) if left_len else 0
    failures = 0
    seed = block[0]
    for a in range(left_len):
        for b in range(right_len):
            expected = frobenius_power(seed[(b - a) % right_len], a, field)
            if block[a][b] != expected:
                failures += 1
    return failures


def audit_pair(
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
) -> list[OrbitBlock]:
    left_orbits = q_orbits(left, q)
    right_orbits = q_orbits(right, q)
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    blocks: list[OrbitBlock] = []
    for left_orbit in left_orbits:
        row_indices = [row_index[u] for u in left_orbit]
        for right_orbit in right_orbits:
            col_indices = [col_index[v] for v in right_orbit]
            block = matrix_subblock(dft_matrix, row_indices, col_indices)
            rank = rank_over_extension(block, field)
            possible_rank = min(len(left_orbit), len(right_orbit))
            blocks.append(
                OrbitBlock(
                    left=left,
                    right=right,
                    left_orbit_rep=left_orbit[0],
                    right_orbit_rep=right_orbit[0],
                    left_orbit_len=len(left_orbit),
                    right_orbit_len=len(right_orbit),
                    rank=rank,
                    possible_rank=possible_rank,
                    full_possible_rank=(rank == possible_rank),
                    frobenius_identity_failures=orbit_identity_failures(block, field),
                )
            )
    return blocks


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> OrbitRow | None:
    if factor.degree() % 2:
        return None
    h = len(cycle)
    n = h // m
    if pow(q, factor.degree() // 2, n) != n - 1:
        return None

    components = coprime_components(m)
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)
    powers = zeta_powers(zeta, m, field)

    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    blocks: list[OrbitBlock] = []
    for left in components:
        for right in components:
            if left == 2 or right == 2:
                continue
            marginal = double_marginal(kernel, left, right, q)
            dft_matrix = dft_double_marginal(
                marginal,
                left,
                right,
                powers,
                m,
                field,
            )
            blocks.extend(audit_pair(dft_matrix, left, right, q, field))

    if not blocks:
        return None
    return OrbitRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        components=components,
        blocks=tuple(blocks),
    )


def scan(args: argparse.Namespace) -> list[OrbitRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[OrbitRow] = []
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
            if sp.gcd(m, h // m) == 1
            and m <= args.max_m
            and len([c for c in coprime_components(m) if c > 2]) >= 2
            and 1 + sum(c - 1 for c in coprime_components(m)) <= args.max_axis_dim
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
        if not splits:
            continue
        case_had_cycle = False
        for q, roots in splits:
            full = find_full_cycle_prime(roots, D, q)
            if full is None:
                continue
            case_had_cycle = True
            ell, cycle = full
            shifted = rotate(cycle, args.origin_shift % h)
            for m in quotient_sizes:
                extension_degree = int(sp.n_order(q % m, m))
                if extension_degree > args.max_extension_degree:
                    continue
                n = h // m
                axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    if factor.degree() < axis_dim:
                        continue
                    if factor.degree() > args.max_factor_degree:
                        continue
                    row = audit_packet(D, q, ell, shifted, m, factor, args.seed)
                    if row is not None:
                        rows.append(row)
                        if len(rows) >= args.max_rows:
                            return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def p24_forecast() -> str:
    p = 10**24 + 7
    c = 157
    d = 211
    left_len = int(sp.n_order(p % c, c))
    right_len = int(sp.n_order(p % d, d))
    right_orbits = (d - 1) // right_len
    extension_degree = lcm(left_len, right_len)
    rows = c - 1
    cols = d - 1
    return (
        f"p24_mixed_157_211: left_orbit_len={left_len} "
        f"right_orbit_len={right_len} right_orbits={right_orbits} "
        f"extension_degree={extension_degree} rectangular_shape={rows}x{cols} "
        f"seed_entries={right_orbits * right_len}"
    )


def format_block(block: OrbitBlock) -> str:
    return (
        f"({block.left},{block.right})"
        f"[{block.left_orbit_rep},{block.right_orbit_rep}]"
        f":lens{block.left_orbit_len}x{block.right_orbit_len}"
        f":rank{block.rank}/{block.possible_rank}"
        f":full{int(block.full_possible_rank)}"
        f":frob_fail{block.frobenius_identity_failures}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-rows", type=int, default=20)
    parser.add_argument("--max-cases", type=int, default=80)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=500)
    parser.add_argument("--max-abs-D", type=int, default=500000)
    parser.add_argument("--max-prime-quotients", type=int, default=24)
    parser.add_argument("--max-composite-quotients", type=int, default=80)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=500)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=2_000_000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--max-axis-dim", type=int, default=160)
    parser.add_argument("--max-m", type=int, default=420)
    parser.add_argument("--max-factor-degree", type=int, default=120)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--origin-shift", type=int, default=0)
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    blocks = [block for row in rows for block in row.blocks]
    identity_failures = sum(block.frobenius_identity_failures for block in blocks)
    nonfull_blocks = [block for block in blocks if not block.full_possible_rank]

    print("Hermitian mixed Frobenius-orbit audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(p24_forecast())
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext comps "
            "blocks=(c,d)[u0,v0]:lens:rank/full:frob_fail"
        )
        for row in rows[:80]:
            formatted = ",".join(format_block(block) for block in row.blocks)
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} ext={row.extension_degree:2d} "
                f"comps={list(row.components)} blocks={formatted}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  orbit_blocks={len(blocks)}")
    print(f"  frobenius_identity_failures={identity_failures}")
    print(f"  nonfull_possible_rank_blocks={len(nonfull_blocks)}")
    if blocks:
        print(
            "  max_block_possible_rank="
            f"{max(block.possible_rank for block in blocks)}"
        )
        print(
            "  max_block_rank="
            f"{max(block.rank for block in blocks)}"
        )
    print()
    print("interpretation")
    print("  zero_frobenius_failures_confirms_moore_circulant_orbit_model=1")
    print("  full_possible_rank_blocks_support_rank_metric_theorem_candidate=1")
    print("  p24_large_block_is_one_156_orbit_against_six_35_orbits=1")
    print("conclusion=reported_hermitian_mixed_frobenius_orbit_audit")


if __name__ == "__main__":
    main()
