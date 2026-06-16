#!/usr/bin/env python3
"""Structure audit for the relative coefficient block code.

The trace-frame sum-rank route views the axis image as an E-linear code in
C^r, where r=[B:C].  This script builds the small tensor analogue of that
generator matrix and compares simple LRS/MSRD signatures against random
controls:

* individual and pair block ranks;
* flattened Toeplitz/Hankel/cyclic displacement ranks;
* random matrices with the same shape over E.

The goal is to filter hypotheses, not to certify p24.
"""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from itertools import combinations
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from k_character_tensor_factor_block_scan import frequency_blocks
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    axis_frequency_set,
    character_rows,
    find_irreducible_modulus,
    primitive_root_of_order,
    rank_over_extension,
)
from l1_axis_injectivity_scan import coeff_vector
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)
from tensor_factor_dual_basis_window_audit import (
    discriminants,
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
)
from tensor_factor_marginal_cs_structure_audit import displacement_ranks
from tensor_factor_moore_audit import b_is_zero
from tensor_factor_relative_block_erasure_audit import coefficient_blocks
from tensor_factor_subfield_trace_audit import divisors


Matrix = list[list[FpE]]


@dataclass(frozen=True)
class PreparedBlockCode:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    subdegree: int
    relative_degree: int
    target: str
    matrix: Matrix
    field: ExtensionField


def frequencies_for_target(m: int, target: str) -> list[int]:
    if target == "axis":
        return axis_frequency_set(m)
    for name, frequencies in frequency_blocks(m):
        if target == name:
            return frequencies
        if target == f"constant_plus_{name}":
            return sorted(set([0] + frequencies))
    raise ValueError(f"unknown target {target!r} for m={m}")


def flatten_blocks(blocks: list[list[FpE]]) -> list[FpE]:
    out: list[FpE] = []
    for block in blocks:
        out.extend(block)
    return out


def block_projection(matrix: Matrix, block: int, subdegree: int) -> Matrix:
    cols = range(block * subdegree, (block + 1) * subdegree)
    return [[row[col] for col in cols] for row in matrix]


def block_subset_projection(matrix: Matrix, blocks: tuple[int, ...], subdegree: int) -> Matrix:
    cols: list[int] = []
    for block in blocks:
        cols.extend(range(block * subdegree, (block + 1) * subdegree))
    return [[row[col] for col in cols] for row in matrix]


def random_element(field: ExtensionField, rng: random.Random) -> FpE:
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_matrix(rows: int, cols: int, field: ExtensionField, rng: random.Random) -> Matrix:
    return [[random_element(field, rng) for _ in range(cols)] for _ in range(rows)]


def rank_hist(values: list[int]) -> dict[int, int]:
    return dict(sorted(Counter(values).items()))


def matrix_summary(matrix: Matrix, relative_degree: int, subdegree: int, field: ExtensionField) -> dict[str, object]:
    full_rank = rank_over_extension(matrix, field)
    block_ranks = [
        rank_over_extension(block_projection(matrix, block, subdegree), field)
        for block in range(relative_degree)
    ]
    pair_ranks = [
        rank_over_extension(block_subset_projection(matrix, pair, subdegree), field)
        for pair in combinations(range(relative_degree), 2)
    ]
    return {
        "rank": full_rank,
        "block_rank_hist": rank_hist(block_ranks),
        "pair_rank_hist": rank_hist(pair_ranks),
        "displacement": displacement_ranks(matrix, field),
    }


def prepare_case(args: argparse.Namespace) -> PreparedBlockCode:
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
        quotient_sizes = [m for m in quotient_sizes if sp.gcd(m, h // m) == 1]
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
        case_had_cycle = False
        for q, roots in splits:
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
                    if factor.degree() > args.max_factor_degree:
                        continue
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if args.subdegree not in divisors(tensor_factor_degree):
                        continue
                    relative_degree = tensor_factor_degree // args.subdegree
                    if relative_degree <= 1:
                        continue

                    residues = [
                        fiber.rem(factor)
                        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
                    ]
                    residue_vectors = [
                        coeff_vector(residue, factor.degree(), q)
                        for residue in residues
                    ]
                    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
                    field = ExtensionField(q, extension_degree, modulus)
                    zeta = primitive_root_of_order(field, m, args.seed)
                    rows = character_rows(
                        residue_vectors,
                        frequencies_for_target(m, args.target),
                        zeta,
                        field,
                    )
                    factors = equal_degree_factors(
                        sympy_factor_to_poly_e(factor, field),
                        tensor_factor_degree,
                        field,
                        args.seed,
                    )
                    selected_factor = factors[0]
                    subfield_basis = normal_subfield_basis(
                        args.subdegree,
                        tensor_factor_degree,
                        selected_factor,
                        field,
                    )
                    basis_columns = relative_basis_columns(
                        subfield_basis,
                        relative_degree,
                        selected_factor,
                        field,
                    )
                    gprime_theta = relative_gprime_theta(
                        args.subdegree,
                        tensor_factor_degree,
                        selected_factor,
                        field,
                    )
                    matrix: Matrix = []
                    for row in rows:
                        value = poly_mod(row_to_poly(row, field), selected_factor, field)
                        if b_is_zero(value, field):
                            continue
                        matrix.append(
                            flatten_blocks(
                                coefficient_blocks(
                                    value,
                                    args.subdegree,
                                    relative_degree,
                                    gprime_theta,
                                    basis_columns,
                                    selected_factor,
                                    field,
                                )
                            )
                        )
                    if matrix:
                        return PreparedBlockCode(
                            D=D,
                            q=q,
                            ell=ell,
                            h=h,
                            m=m,
                            n=n,
                            factor_degree=factor.degree(),
                            extension_degree=extension_degree,
                            tensor_factor_degree=tensor_factor_degree,
                            subdegree=args.subdegree,
                            relative_degree=relative_degree,
                            target=args.target,
                            matrix=matrix,
                            field=field,
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    raise RuntimeError("no matching tensor block-code case found")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-trials", type=int, default=100)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=220)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=220)
    parser.add_argument("--max-m", type=int, default=48)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=2)
    parser.add_argument("--target", default="axis")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    prepared = prepare_case(args)
    cm_summary = matrix_summary(
        prepared.matrix,
        prepared.relative_degree,
        prepared.subdegree,
        prepared.field,
    )
    rng = random.Random(args.seed + 12345)
    random_summaries = [
        matrix_summary(
            random_matrix(
                len(prepared.matrix),
                prepared.relative_degree * prepared.subdegree,
                prepared.field,
                rng,
            ),
            prepared.relative_degree,
            prepared.subdegree,
            prepared.field,
        )
        for _ in range(args.random_trials)
    ]

    print("tensor factor relative block-structure audit")
    print(f"D={prepared.D}")
    print(f"q={prepared.q}")
    print(f"ell={prepared.ell}")
    print(f"h={prepared.h}")
    print(f"m={prepared.m}")
    print(f"n={prepared.n}")
    print(f"factor_degree={prepared.factor_degree}")
    print(f"extension_degree={prepared.extension_degree}")
    print(f"tensor_factor_degree={prepared.tensor_factor_degree}")
    print(f"subdegree={prepared.subdegree}")
    print(f"relative_degree={prepared.relative_degree}")
    print(f"target={prepared.target}")
    print(f"rows={len(prepared.matrix)}")
    print(f"cols={len(prepared.matrix[0]) if prepared.matrix else 0}")
    print()
    print("cm_matrix")
    print(f"  rank={cm_summary['rank']}")
    print(f"  block_rank_hist={cm_summary['block_rank_hist']}")
    print(f"  pair_rank_hist={cm_summary['pair_rank_hist']}")
    print(f"  displacement={cm_summary['displacement']}")
    print()
    print("random_controls")
    print(f"  trials={args.random_trials}")
    print(f"  rank_hist={rank_hist([int(s['rank']) for s in random_summaries])}")
    print(
        "  block_rank_hists="
        + str(rank_hist([tuple(sorted(s["block_rank_hist"].items())) for s in random_summaries]))
    )
    print(
        "  pair_rank_hists="
        + str(rank_hist([tuple(sorted(s["pair_rank_hist"].items())) for s in random_summaries]))
    )
    for name in ("toeplitz", "hankel", "cyclic_toeplitz", "cyclic_hankel"):
        print(
            f"  {name}_disp_hist="
            + str(rank_hist([int(s["displacement"][name]) for s in random_summaries]))
        )
    print()
    print("interpretation")
    print("  matching_random_profiles_demotes_visible_lrs_structure=1")
    print("  p24_still_needs_explicit_block_equivalence_or_selected_punit=1")
    print("conclusion=reported_tensor_factor_relative_block_structure_audit")


if __name__ == "__main__":
    main()
