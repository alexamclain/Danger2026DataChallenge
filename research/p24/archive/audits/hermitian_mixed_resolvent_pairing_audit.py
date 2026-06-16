#!/usr/bin/env python3
"""Audit the mixed DFT entries as pairings of K-character resolvents.

For the Hermitian kernel

    K(r,s)=Tr_packet(F_r(X)F_s(X^-1)),

the mixed Fourier entry is

    H_{c,d}(u,v)=sum_{r,s} zeta_c^(u*r) zeta_d^(v*s) K(r,s).

This is the bilinear pairing of the two K-character resolvents

    A_u = sum_r zeta_c^(u*r) F_r,
    B_v = sum_s zeta_d^(v*s) F_s.

The script verifies the direct resolvent-pairing formula against the
double-marginal DFT matrix on small CM rows and reports the seed periods
used by the p24 trace-intersection theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import double_marginal, kernel_matrix
from hermitian_double_marginal_fourier_audit import (
    dft_double_marginal,
    zeta_powers,
)
from hermitian_mixed_frobenius_orbit_audit import q_orbits
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
class ResolventPairTest:
    left: int
    right: int
    left_orbit_count: int
    right_orbit_count: int
    left_orbit_len_histogram: tuple[tuple[int, int], ...]
    right_orbit_len_histogram: tuple[tuple[int, int], ...]
    dft_rank: int
    direct_pairing_rank: int
    entry_mismatches: int
    seed_period_count: int
    nonzero_seed_periods: int
    seed_fq_rank: int


@dataclass(frozen=True)
class ResolventPairRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    components: tuple[int, ...]
    tests: tuple[ResolventPairTest, ...]


def orbit_len_histogram(orbits: list[list[int]]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for orbit in orbits:
        counts[len(orbit)] = counts.get(len(orbit), 0) + 1
    return tuple(sorted(counts.items()))


def fq_rank(values: list[FpE], q: int) -> int:
    if not values:
        return 0
    rows = [[coord % q for coord in value] for value in values]
    return rank_mod_q_local(rows, q)


def rank_mod_q_local(matrix: list[list[int]], q: int) -> int:
    mat = [[value % q for value in row] for row in matrix if any(value % q for value in row)]
    if not mat:
        return 0
    rows = len(mat)
    cols = len(mat[0])
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(inv * value) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if not scale:
                continue
            mat[row] = [
                (left - scale * right) % q
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def direct_resolvent_pairing_matrix(
    kernel: list[list[int]],
    left: int,
    right: int,
    powers: list[FpE],
    m: int,
    field: ExtensionField,
) -> list[list[FpE]]:
    step_left = m // left
    step_right = m // right
    out: list[list[FpE]] = []
    for u in range(1, left):
        row: list[FpE] = []
        left_weights = [powers[(u * step_left * r) % m] for r in range(m)]
        for v in range(1, right):
            total = field.zero
            for r, kernel_row in enumerate(kernel):
                left_weight = left_weights[r]
                if left_weight == field.zero:
                    continue
                for s, value in enumerate(kernel_row):
                    if value % field.q == 0:
                        continue
                    coeff = field.mul(left_weight, powers[(v * step_right * s) % m])
                    total = field.add(total, field.mul(coeff, field.embed(value)))
            row.append(total)
        out.append(row)
    return out


def matrix_mismatches(left, right) -> int:
    return sum(
        1
        for left_row, right_row in zip(left, right)
        for left_value, right_value in zip(left_row, right_row)
        if left_value != right_value
    )


def audit_pair(
    kernel: list[list[int]],
    left: int,
    right: int,
    powers: list[FpE],
    m: int,
    q: int,
    field: ExtensionField,
) -> ResolventPairTest:
    marginal = double_marginal(kernel, left, right, q)
    dft_matrix = dft_double_marginal(marginal, left, right, powers, m, field)
    direct_matrix = direct_resolvent_pairing_matrix(
        kernel, left, right, powers, m, field
    )
    left_orbits = q_orbits(left, q)
    right_orbits = q_orbits(right, q)
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    seed_periods = [
        dft_matrix[row_index[left_orbits[0][0]]][col_index[right_orbit[0]]]
        for right_orbit in right_orbits
    ]
    return ResolventPairTest(
        left=left,
        right=right,
        left_orbit_count=len(left_orbits),
        right_orbit_count=len(right_orbits),
        left_orbit_len_histogram=orbit_len_histogram(left_orbits),
        right_orbit_len_histogram=orbit_len_histogram(right_orbits),
        dft_rank=rank_over_extension(dft_matrix, field),
        direct_pairing_rank=rank_over_extension(direct_matrix, field),
        entry_mismatches=matrix_mismatches(dft_matrix, direct_matrix),
        seed_period_count=len(seed_periods),
        nonzero_seed_periods=sum(1 for value in seed_periods if value != field.zero),
        seed_fq_rank=fq_rank(seed_periods, q),
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> ResolventPairRow | None:
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
    tests: list[ResolventPairTest] = []
    for left in components:
        for right in components:
            if left == 2 or right == 2:
                continue
            tests.append(audit_pair(kernel, left, right, powers, m, q, field))

    if not tests:
        return None
    return ResolventPairRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        components=components,
        tests=tuple(tests),
    )


def scan(args: argparse.Namespace) -> list[ResolventPairRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[ResolventPairRow] = []
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


def format_hist(histogram: tuple[tuple[int, int], ...]) -> str:
    return "{" + ",".join(f"{length}:{count}" for length, count in histogram) + "}"


def format_test(test: ResolventPairTest) -> str:
    return (
        f"({test.left},{test.right})"
        f":Lorbits{test.left_orbit_count}{format_hist(test.left_orbit_len_histogram)}"
        f":Rorbits{test.right_orbit_count}{format_hist(test.right_orbit_len_histogram)}"
        f":dftrank{test.dft_rank}"
        f":pairrank{test.direct_pairing_rank}"
        f":mismatch{test.entry_mismatches}"
        f":seeds{test.nonzero_seed_periods}/{test.seed_period_count}"
        f":seedfqrank{test.seed_fq_rank}"
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
    tests = [test for row in rows for test in row.tests]
    mismatches = sum(test.entry_mismatches for test in tests)
    rank_mismatches = [
        test for test in tests if test.dft_rank != test.direct_pairing_rank
    ]
    all_seeds_nonzero = [
        test for test in tests if test.nonzero_seed_periods == test.seed_period_count
    ]

    print("Hermitian mixed resolvent-pairing audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext comps "
            "tests=(c,d):orbits:ranks:mismatch:seeds:seedfqrank"
        )
        for row in rows[:80]:
            formatted = ",".join(format_test(test) for test in row.tests)
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} ext={row.extension_degree:2d} "
                f"comps={list(row.components)} tests={formatted}"
            )
    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  tests={len(tests)}")
    print(f"  entry_mismatches={mismatches}")
    print(f"  rank_mismatch_tests={len(rank_mismatches)}")
    print(f"  all_seed_periods_nonzero_tests={len(all_seeds_nonzero)}")
    if tests:
        print(f"  max_dft_rank={max(test.dft_rank for test in tests)}")
        print(f"  max_seed_fq_rank={max(test.seed_fq_rank for test in tests)}")
    print()
    print("interpretation")
    print("  zero_entry_mismatches_confirms_mixed_DFT_is_resolvent_pairing=1")
    print("  seed_periods_are_the_S_j_for_trace_intersection_theorem=1")
    print("conclusion=reported_hermitian_mixed_resolvent_pairing_audit")


if __name__ == "__main__":
    main()
