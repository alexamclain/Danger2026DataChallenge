#!/usr/bin/env python3
"""K-character tensor-rank scan without assuming K roots are in F_q.

This is the nonsplit analogue of `k_character_rank_split_scan.py`.

For a packet algebra

    A = F_q[X]/(f)

and complement size `m`, adjoin `mu_m` in an independent finite extension

    E = F_q(mu_m).

The correct K-character rank lives in the tensor algebra

    A_E = A tensor_{F_q} E ~= E[X]/(f),

not in a single embedding of `A` into a larger field.  This script computes
K-character resolvents as coefficient vectors in the E-basis
`1, X, ..., X^(deg f - 1)` and takes rank over E.

Small rows use this to test whether dimension-possible rank failures are
visible after tensor-separating the K-character roots from the H-packet root.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from l1_axis_injectivity_scan import (
    axis_basis_images,
    coeff_vector,
    rank_mod_q,
)
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    section_fiber_polynomials,
)


FpE = tuple[int, ...]


class ExtensionField:
    def __init__(self, q: int, degree: int, modulus: list[int]):
        self.q = q
        self.degree = degree
        self.modulus = [c % q for c in modulus]
        if len(self.modulus) != degree + 1 or self.modulus[-1] != 1:
            raise ValueError("modulus must be monic of requested degree")
        self.zero = tuple(0 for _ in range(degree))
        self.one = (1,) + tuple(0 for _ in range(degree - 1))

    def embed(self, value: int) -> FpE:
        return (value % self.q,) + tuple(0 for _ in range(self.degree - 1))

    def add(self, left: FpE, right: FpE) -> FpE:
        return tuple((a + b) % self.q for a, b in zip(left, right))

    def neg(self, value: FpE) -> FpE:
        return tuple((-a) % self.q for a in value)

    def sub(self, left: FpE, right: FpE) -> FpE:
        return tuple((a - b) % self.q for a, b in zip(left, right))

    def scalar_mul(self, scalar: int, value: FpE) -> FpE:
        s = scalar % self.q
        if not s:
            return self.zero
        return tuple((s * a) % self.q for a in value)

    def mul(self, left: FpE, right: FpE) -> FpE:
        q = self.q
        e = self.degree
        tmp = [0] * (2 * e - 1)
        for i, a in enumerate(left):
            if not a:
                continue
            for j, b in enumerate(right):
                if b:
                    tmp[i + j] = (tmp[i + j] + a * b) % q
        for k in range(2 * e - 2, e - 1, -1):
            coeff = tmp[k] % q
            if not coeff:
                continue
            tmp[k] = 0
            shift = k - e
            for i in range(e):
                tmp[shift + i] = (
                    tmp[shift + i] - coeff * self.modulus[i]
                ) % q
        return tuple(c % q for c in tmp[:e])

    def pow(self, base: FpE, exponent: int) -> FpE:
        result = self.one
        current = base
        e = exponent
        while e:
            if e & 1:
                result = self.mul(result, current)
            current = self.mul(current, current)
            e >>= 1
        return result

    def inv(self, value: FpE) -> FpE:
        if value == self.zero:
            raise ZeroDivisionError("inverse of zero")
        return self.pow(value, self.q**self.degree - 2)

    def div(self, left: FpE, right: FpE) -> FpE:
        return self.mul(left, self.inv(right))


def find_irreducible_modulus(q: int, degree: int, seed: int) -> list[int]:
    if degree == 1:
        return [0, 1]
    x = sp.symbols("x")
    rng = random.Random(seed + 1009 * q + 9176 * degree)
    # Try sparse small-looking polynomials first for reproducibility/readability.
    limit = min(q, 32)
    for a in range(limit):
        for b in range(1, limit):
            coeffs = [b, a] + [0] * (degree - 2) + [1]
            poly = sp.Poly.from_list(list(reversed(coeffs)), x, modulus=q)
            if poly.is_irreducible:
                return coeffs
    for _ in range(2000):
        coeffs = [rng.randrange(q) for _ in range(degree)] + [1]
        if coeffs[0] == 0:
            coeffs[0] = rng.randrange(1, q)
        poly = sp.Poly.from_list(list(reversed(coeffs)), x, modulus=q)
        if poly.is_irreducible:
            return coeffs
    raise RuntimeError(f"could not find irreducible polynomial over F_{q} degree {degree}")


def element_order_is(field: ExtensionField, value: FpE, order: int) -> bool:
    if field.pow(value, order) != field.one:
        return False
    for prime in sp.factorint(order):
        if field.pow(value, order // int(prime)) == field.one:
            return False
    return True


def primitive_root_of_order(field: ExtensionField, order: int, seed: int) -> FpE:
    group_order = field.q**field.degree - 1
    if group_order % order:
        raise ValueError("order does not divide extension multiplicative group")
    rng = random.Random(seed + 424242 * order + field.q)
    exponent = group_order // order
    candidates: list[FpE] = []
    if field.degree > 1:
        candidates.append(tuple([0, 1] + [0] * (field.degree - 2)))
    candidates.extend(field.embed(a) for a in range(2, min(field.q, 32)))
    for _ in range(512):
        candidates.append(tuple(rng.randrange(field.q) for _ in range(field.degree)))
    for candidate in candidates:
        if candidate == field.zero:
            continue
        root = field.pow(candidate, exponent)
        if element_order_is(field, root, order):
            return root
    raise RuntimeError(f"could not find primitive root of order {order}")


def rank_over_extension(matrix: list[list[FpE]], field: ExtensionField) -> int:
    mat = [row[:] for row in matrix if any(value != field.zero for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = field.inv(mat[rank][col])
        mat[rank] = [field.mul(value, inv) for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col]
            if scale == field.zero:
                continue
            mat[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(mat[row], mat[rank])
            ]
        rank += 1
        if rank == rows:
            break
    return rank


def axis_frequency_set(m: int) -> list[int]:
    frequencies = {0}
    for component in coprime_components(m):
        step = m // component
        for j in range(1, component):
            frequencies.add((j * step) % m)
    return sorted(frequencies)


def character_rows(
    residue_vectors: list[list[int]],
    frequencies: list[int],
    zeta: FpE,
    field: ExtensionField,
) -> list[list[FpE]]:
    m = len(residue_vectors)
    degree = len(residue_vectors[0]) if residue_vectors else 0
    powers = [field.one]
    for _ in range(1, m):
        powers.append(field.mul(powers[-1], zeta))
    rows: list[list[FpE]] = []
    for s in frequencies:
        out = [field.zero for _ in range(degree)]
        for r, vector in enumerate(residue_vectors):
            coeff = powers[(s * r) % m]
            if coeff == field.zero:
                continue
            for k, value in enumerate(vector):
                if value:
                    out[k] = field.add(out[k], field.scalar_mul(value, coeff))
        rows.append(out)
    return rows


@dataclass(frozen=True)
class TensorRankRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    axis_dim: int
    axis_base_rank: int
    axis_character_rank: int
    axis_zero_characters: int
    full_k_base_rank: int
    full_k_character_rank: int
    full_k_zero_characters: int
    axis_dimension_possible: bool
    full_k_dimension_possible: bool


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> TensorRankRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    full_k_base_rank = rank_mod_q(residue_vectors, q)

    components = coprime_components(m)
    axis_images = axis_basis_images(residues, components, factor)
    axis_base_rank = rank_mod_q(
        [coeff_vector(poly, factor.degree(), q) for _, poly in axis_images],
        q,
    )

    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, seed)
    field = ExtensionField(q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, m, seed)

    axis_frequencies = axis_frequency_set(m)
    axis_rows = character_rows(residue_vectors, axis_frequencies, zeta, field)
    full_frequencies = list(range(m))
    full_rows = character_rows(residue_vectors, full_frequencies, zeta, field)

    return TensorRankRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        axis_dim=len(axis_frequencies),
        axis_base_rank=axis_base_rank,
        axis_character_rank=rank_over_extension(axis_rows, field),
        axis_zero_characters=sum(
            all(value == field.zero for value in row) for row in axis_rows
        ),
        full_k_base_rank=full_k_base_rank,
        full_k_character_rank=rank_over_extension(full_rows, field),
        full_k_zero_characters=sum(
            all(value == field.zero for value in row) for row in full_rows
        ),
        axis_dimension_possible=factor.degree() >= len(axis_frequencies),
        full_k_dimension_possible=factor.degree() >= m,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[TensorRankRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[TensorRankRow] = []
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
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
        case_had_row = False
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
                    rows.append(audit_packet(D, q, ell, cycle, m, factor, args.seed))
                    case_had_row = True
        if case_had_row:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=12)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=50000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=12)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--max-m", type=int, default=40)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-factor-degree", type=int, default=40)
    parser.add_argument("--max-extension-degree", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20260604)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    axis_rank_mismatches = [
        row for row in rows if row.axis_character_rank != row.axis_base_rank
    ]
    full_rank_mismatches = [
        row for row in rows if row.full_k_character_rank != row.full_k_base_rank
    ]
    axis_possible = [row for row in rows if row.axis_dimension_possible]
    axis_possible_failures = [
        row for row in axis_possible if row.axis_character_rank < row.axis_dim
    ]
    axis_support_not_rank = [
        row for row in rows
        if row.axis_zero_characters == 0
        and row.axis_character_rank < row.axis_dim
    ]
    axis_possible_support_not_rank = [
        row for row in axis_support_not_rank if row.axis_dimension_possible
    ]
    full_possible = [row for row in rows if row.full_k_dimension_possible]
    full_possible_failures = [
        row for row in full_possible if row.full_k_character_rank < row.m
    ]
    extension_hist: dict[int, int] = {}
    for row in rows:
        extension_hist[row.extension_degree] = (
            extension_hist.get(row.extension_degree, 0) + 1
        )

    print("K-character tensor-rank scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_m={args.max_m}")
    print(f"max_factor_degree={args.max_factor_degree}")
    print(f"max_extension_degree={args.max_extension_degree}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext axis_rank axis_char "
            "axis_zero full_rank full_char full_zero"
        )
        display = (
            axis_rank_mismatches
            + full_rank_mismatches
            + axis_possible_failures
            + rows[:40]
        )
        seen_keys: set[tuple[int, int, int, int, int, int]] = set()
        for row in display[:80]:
            key = (row.D, row.q, row.m, row.n, row.factor_degree, row.extension_degree)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"deg={row.factor_degree:3d} ext={row.extension_degree:2d} "
                f"axis_rank={row.axis_base_rank:3d}/{row.axis_dim:3d} "
                f"axis_char={row.axis_character_rank:3d}/{row.axis_dim:3d} "
                f"axis_zero={row.axis_zero_characters:3d} "
                f"full_rank={row.full_k_base_rank:3d}/{row.m:3d} "
                f"full_char={row.full_k_character_rank:3d}/{row.m:3d} "
                f"full_zero={row.full_k_zero_characters:3d}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  extension_degree_histogram={dict(sorted(extension_hist.items()))}")
    print(f"  axis_rank_mismatch_rows={len(axis_rank_mismatches)}")
    print(f"  full_k_rank_mismatch_rows={len(full_rank_mismatches)}")
    print(f"  axis_dimension_possible_rows={len(axis_possible)}")
    print(f"  axis_dimension_possible_failure_rows={len(axis_possible_failures)}")
    print(f"  axis_support_not_rank_rows={len(axis_support_not_rank)}")
    print(f"  axis_dimension_possible_support_not_rank_rows={len(axis_possible_support_not_rank)}")
    print(f"  full_k_dimension_possible_rows={len(full_possible)}")
    print(f"  full_k_dimension_possible_failure_rows={len(full_possible_failures)}")
    print()
    print("interpretation")
    print("  tensor_character_rank_matches_base_rank_if_DFT_extension_is_correct=1")
    print("  support_not_rank_rows_show_nonzero_characters_are_not_formally_enough=1")
    print("  dimension_possible_failures_are_candidate_counterexamples_to_rank_theorem=1")
    print("conclusion=reported_k_character_tensor_rank_scan")


if __name__ == "__main__":
    main()
