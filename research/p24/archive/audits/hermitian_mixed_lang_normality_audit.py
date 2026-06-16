#!/usr/bin/env python3
"""Audit Lang-trivialized normality for mixed Hermitian Moore blocks.

For one mixed DFT orbit block with right-orbit length R, rows have the form

    B(a,b) = sigma^a(seed[b-a]).

Let T(seed)_b = sigma(seed[b-1]).  The fixed vectors of T are

    u_alpha(b) = sigma^b(alpha),       alpha in F_{q^R}.

Choosing an F_q-basis of F_{q^R} gives an invertible Moore matrix U with
T U = U sigma.  If seed = U*w, then the row-orbit matrix is column-equivalent
to the ordinary Moore matrix

    (sigma^a(w_i)).

Thus its E-rank is min(left_orbit_len, F_q-rank of the transformed seed
coordinates).  This script verifies that criterion on small CM rows.
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
from l1_axis_injectivity_scan import discriminants, rank_mod_q
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)


@dataclass(frozen=True)
class LangOrbitRank:
    left: int
    right: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len_histogram: tuple[tuple[int, int], ...]
    row_orbit_rank: int
    transformed_fq_rank: int
    predicted_rank: int
    criterion_match: bool


@dataclass(frozen=True)
class LangRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    components: tuple[int, ...]
    orbit_ranks: tuple[LangOrbitRank, ...]


def fq_rank(values: list[FpE], q: int) -> int:
    if not values:
        return 0
    return rank_mod_q([[coord % q for coord in value] for value in values], q)


def submatrix(matrix, rows: list[int], cols: list[int]):
    return [[matrix[row][col] for col in cols] for row in rows]


def matrix_inverse(matrix: list[list[FpE]], field: ExtensionField) -> list[list[FpE]]:
    n = len(matrix)
    augmented = [
        row[:]
        + [field.one if i == j else field.zero for j in range(n)]
        for i, row in enumerate(matrix)
    ]
    rank = 0
    for col in range(n):
        pivot = None
        for row in range(rank, n):
            if augmented[row][col] != field.zero:
                pivot = row
                break
        if pivot is None:
            raise ValueError("singular matrix in Lang trivialization")
        augmented[rank], augmented[pivot] = augmented[pivot], augmented[rank]
        inv = field.inv(augmented[rank][col])
        augmented[rank] = [field.mul(value, inv) for value in augmented[rank]]
        for row in range(n):
            if row == rank:
                continue
            scale = augmented[row][col]
            if scale == field.zero:
                continue
            augmented[row] = [
                field.sub(left, field.mul(scale, right))
                for left, right in zip(augmented[row], augmented[rank])
            ]
        rank += 1
    return [row[n:] for row in augmented]


def matrix_vector_mul(
    matrix: list[list[FpE]],
    vector: list[FpE],
    field: ExtensionField,
) -> list[FpE]:
    out: list[FpE] = []
    for row in matrix:
        total = field.zero
        for coeff, value in zip(row, vector):
            total = field.add(total, field.mul(coeff, value))
        out.append(total)
    return out


def subfield_power_basis(
    q: int,
    subdegree: int,
    field: ExtensionField,
    seed: int,
) -> list[FpE]:
    if subdegree == 1:
        return [field.one]
    if field.degree % subdegree:
        raise ValueError("requested subfield degree does not divide field degree")

    exponent = (q**field.degree - 1) // (q**subdegree - 1)
    candidates: list[FpE] = []
    if field.degree > 1:
        candidates.append(tuple([0, 1] + [0] * (field.degree - 2)))
    candidates.extend(field.embed(a) for a in range(2, min(q, 64)))
    # Deterministic sparse fallbacks, enough for the small audit fields.
    for pos in range(field.degree):
        candidates.append(
            tuple(1 if i in (0, pos) else 0 for i in range(field.degree))
        )

    for candidate in candidates:
        if candidate == field.zero:
            continue
        beta = field.pow(candidate, exponent)
        if beta == field.zero:
            continue
        if field.pow(beta, q**subdegree) != beta:
            continue
        basis = [field.one]
        for _ in range(1, subdegree):
            basis.append(field.mul(basis[-1], beta))
        if fq_rank(basis, q) == subdegree:
            return basis
    raise RuntimeError(f"could not find F_q-basis for subfield degree {subdegree}")


def lang_inverse_for_orbit(
    q: int,
    orbit_len: int,
    field: ExtensionField,
    seed: int,
) -> list[list[FpE]]:
    basis = subfield_power_basis(q, orbit_len, field, seed)
    matrix: list[list[FpE]] = []
    for row in range(orbit_len):
        matrix.append([field.pow(alpha, q**row) for alpha in basis])
    return matrix_inverse(matrix, field)


def orbit_len_histogram(orbits: list[list[int]]) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for orbit in orbits:
        counts[len(orbit)] = counts.get(len(orbit), 0) + 1
    return tuple(sorted(counts.items()))


def audit_left_orbit(
    dft_matrix: list[list[FpE]],
    left: int,
    right: int,
    left_orbit: list[int],
    right_orbits: list[list[int]],
    q: int,
    field: ExtensionField,
    seed: int,
) -> LangOrbitRank:
    row_index = {u: u - 1 for u in range(1, left)}
    col_index = {v: v - 1 for v in range(1, right)}
    row_indices = [row_index[u] for u in left_orbit]
    col_indices = [col_index[v] for orbit in right_orbits for v in orbit]
    row_orbit_matrix = submatrix(dft_matrix, row_indices, col_indices)
    row_orbit_rank = rank_over_extension(row_orbit_matrix, field)

    transformed: list[FpE] = []
    inverses: dict[int, list[list[FpE]]] = {}
    for right_orbit in right_orbits:
        orbit_len = len(right_orbit)
        if orbit_len not in inverses:
            inverses[orbit_len] = lang_inverse_for_orbit(
                q, orbit_len, field, seed
            )
        seed_vector = [
            dft_matrix[row_index[left_orbit[0]]][col_index[v]]
            for v in right_orbit
        ]
        transformed.extend(
            matrix_vector_mul(inverses[orbit_len], seed_vector, field)
        )

    transformed_rank = fq_rank(transformed, q)
    predicted_rank = min(len(left_orbit), transformed_rank)
    return LangOrbitRank(
        left=left,
        right=right,
        left_orbit_rep=left_orbit[0],
        left_orbit_len=len(left_orbit),
        right_orbit_count=len(right_orbits),
        right_orbit_len_histogram=orbit_len_histogram(right_orbits),
        row_orbit_rank=row_orbit_rank,
        transformed_fq_rank=transformed_rank,
        predicted_rank=predicted_rank,
        criterion_match=(row_orbit_rank == predicted_rank),
    )


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    seed: int,
) -> LangRow | None:
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
    orbit_ranks: list[LangOrbitRank] = []
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
            right_orbits = q_orbits(right, q)
            for left_orbit in q_orbits(left, q):
                orbit_ranks.append(
                    audit_left_orbit(
                        dft_matrix,
                        left,
                        right,
                        left_orbit,
                        right_orbits,
                        q,
                        field,
                        seed,
                    )
                )

    if not orbit_ranks:
        return None
    return LangRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        extension_degree=extension_degree,
        components=components,
        orbit_ranks=tuple(orbit_ranks),
    )


def scan(args: argparse.Namespace) -> list[LangRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rows: list[LangRow] = []
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
    left = 157
    right = 211
    left_len = int(sp.n_order(p % left, left))
    right_len = int(sp.n_order(p % right, right))
    right_orbits = (right - 1) // right_len
    return (
        "p24_lang_normality_target: "
        f"left_orbit_len={left_len} transformed_coordinates="
        f"{right_orbits * right_len} required_Fp_rank_at_least={left_len}"
    )


def format_hist(histogram: tuple[tuple[int, int], ...]) -> str:
    return "{" + ",".join(f"{length}:{count}" for length, count in histogram) + "}"


def format_orbit_rank(rank: LangOrbitRank) -> str:
    return (
        f"({rank.left},{rank.right})[{rank.left_orbit_rep}]"
        f":L{rank.left_orbit_len}:right{rank.right_orbit_count}"
        f":Rhist{format_hist(rank.right_orbit_len_histogram)}"
        f":rowrank{rank.row_orbit_rank}"
        f":fqrank{rank.transformed_fq_rank}"
        f":pred{rank.predicted_rank}"
        f":match{int(rank.criterion_match)}"
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
    orbit_ranks = [rank for row in rows for rank in row.orbit_ranks]
    mismatches = [rank for rank in orbit_ranks if not rank.criterion_match]
    full_left = [
        rank
        for rank in orbit_ranks
        if rank.row_orbit_rank == rank.left_orbit_len
    ]

    print("Hermitian mixed Lang-normality audit")
    print(f"max_rows={args.max_rows}")
    print(f"max_h={args.max_h}")
    print(f"q_stop={args.q_stop}")
    print(f"max_axis_dim={args.max_axis_dim}")
    print(p24_forecast())
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n deg ext comps "
            "orbit=(c,d)[u0]:L:right:Rhist:rowrank:fqrank:pred:match"
        )
        for row in rows[:80]:
            formatted = ",".join(format_orbit_rank(rank) for rank in row.orbit_ranks)
            print(
                f"D={row.D:8d} q={row.q:8d} ell={row.ell:3d} "
                f"h={row.h:4d} m={row.m:4d} n={row.n:4d} "
                f"deg={row.factor_degree:4d} ext={row.extension_degree:2d} "
                f"comps={list(row.components)} orbit_ranks={formatted}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  left_orbit_tests={len(orbit_ranks)}")
    print(f"  criterion_mismatches={len(mismatches)}")
    print(f"  full_left_orbit_rank_tests={len(full_left)}")
    if orbit_ranks:
        print(
            "  max_transformed_fq_rank="
            f"{max(rank.transformed_fq_rank for rank in orbit_ranks)}"
        )
        print(
            "  max_left_orbit_len="
            f"{max(rank.left_orbit_len for rank in orbit_ranks)}"
        )
    print()
    print("interpretation")
    print("  zero_mismatches_confirms_lang_normality_rank_criterion=1")
    print("  p24_target_is_Fp_rank_at_least_156_after_lang_trivialization=1")
    print("conclusion=reported_hermitian_mixed_lang_normality_audit")


if __name__ == "__main__":
    main()
