#!/usr/bin/env python3
"""Structure diagnostics for CM Hermitian packet vectors.

The selected-prime Hermitian theorem needs more than generic finite-field
linear algebra: nonzero vectors can be isotropic.  This scan records extra
features of the actual CM packet vectors

    (J_0 mod f, ..., J_{m-1} mod f)

and compares their Hermitian scalar against two cheap controls:

* random packet vectors with the same `(q, m, deg f)` shape;
* random permutations of the same CM roots, breaking the class-cycle order.

The goal is not to prove anything by randomness.  It is to identify candidate
rigidity worth turning into a theorem, or to show that a proposed statistic is
just generic packet behavior.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from packetized_relative_content_scan import (
    X,
    fiber_polynomials,
    hermitian_energy_poly,
    packet_factors,
    quotient_sizes_with_prime_subgroup,
)


@dataclass(frozen=True)
class PacketStructureRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    coord_zero_count: int
    term_zero_count: int
    span_rank: int
    max_possible_span: int
    span_maximal: bool
    cm_hermitian_zero: bool
    random_vector_trials: int
    random_vector_zeros: int
    random_vector_span_defects: int
    shuffled_cycle_trials: int
    shuffled_cycle_zeros: int
    shuffled_cycle_span_defects: int


def rank_mod_q(rows: list[list[int]], q: int) -> int:
    mat = [row[:] for row in rows if any(value % q for value in row)]
    if not mat:
        return 0
    nrows = len(mat)
    ncols = len(mat[0])
    rank = 0
    for col in range(ncols):
        pivot = None
        for row in range(rank, nrows):
            if mat[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % q, -1, q)
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(nrows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if scale:
                mat[row] = [
                    (left - scale * right) % q
                    for left, right in zip(mat[row], mat[rank])
                ]
        rank += 1
        if rank == nrows:
            break
    return rank


def coeff_vector(poly: sp.Poly, degree: int, q: int) -> list[int]:
    return [int(poly.nth(i)) % q for i in range(degree)]


def random_poly(rng: random.Random, degree: int, q: int) -> sp.Poly:
    return sp.Poly(
        sum(rng.randrange(q) * X**i for i in range(degree)),
        X,
        modulus=q,
    )


def hermitian_from_residues(
    residues: list[sp.Poly],
    factor: sp.Poly,
    q: int,
) -> sp.Poly:
    m = len(residues)
    total = sp.Poly(0, X, modulus=q)
    for u, left in enumerate(residues):
        inv_u = (-u) % m
        carry = (u + inv_u) // m
        total += sp.Poly(X**carry, X, modulus=q) * left * residues[inv_u]
    return total.rem(factor)


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    rng: random.Random,
    random_trials: int,
    shuffle_trials: int,
) -> PacketStructureRow:
    h = len(cycle)
    n = h // m
    degree = factor.degree()
    residues = [fiber.rem(factor) for fiber in fiber_polynomials(cycle, q, m)]

    cm_from_residues = hermitian_from_residues(residues, factor, q)
    cm_from_cycle = hermitian_energy_poly(cycle, q, m).rem(factor)
    if cm_from_residues != cm_from_cycle:
        raise AssertionError("residue and cycle Hermitian packets differ")

    term_zero_count = 0
    for u, left in enumerate(residues):
        inv_u = (-u) % m
        carry = (u + inv_u) // m
        term = (sp.Poly(X**carry, X, modulus=q) * left * residues[inv_u]).rem(factor)
        if term.is_zero:
            term_zero_count += 1

    vectors = [coeff_vector(residue, degree, q) for residue in residues]
    span_rank = rank_mod_q(vectors, q)
    max_possible_span = min(m, degree)

    random_vector_zeros = 0
    random_vector_span_defects = 0
    for _ in range(random_trials):
        random_residues = [random_poly(rng, degree, q).rem(factor) for _ in range(m)]
        if hermitian_from_residues(random_residues, factor, q).is_zero:
            random_vector_zeros += 1
        random_vectors = [coeff_vector(residue, degree, q) for residue in random_residues]
        if rank_mod_q(random_vectors, q) < max_possible_span:
            random_vector_span_defects += 1

    shuffled_cycle_zeros = 0
    shuffled_cycle_span_defects = 0
    for _ in range(shuffle_trials):
        shuffled = cycle[:]
        rng.shuffle(shuffled)
        if hermitian_energy_poly(shuffled, q, m).rem(factor).is_zero:
            shuffled_cycle_zeros += 1
        shuffled_residues = [fiber.rem(factor) for fiber in fiber_polynomials(shuffled, q, m)]
        shuffled_vectors = [coeff_vector(residue, degree, q) for residue in shuffled_residues]
        if rank_mod_q(shuffled_vectors, q) < max_possible_span:
            shuffled_cycle_span_defects += 1

    return PacketStructureRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=degree,
        coord_zero_count=sum(1 for residue in residues if residue.is_zero),
        term_zero_count=term_zero_count,
        span_rank=span_rank,
        max_possible_span=max_possible_span,
        span_maximal=(span_rank == max_possible_span),
        cm_hermitian_zero=cm_from_cycle.is_zero,
        random_vector_trials=random_trials,
        random_vector_zeros=random_vector_zeros,
        random_vector_span_defects=random_vector_span_defects,
        shuffled_cycle_trials=shuffle_trials,
        shuffled_cycle_zeros=shuffled_cycle_zeros,
        shuffled_cycle_span_defects=shuffled_cycle_span_defects,
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
    random_trials: int,
    shuffle_trials: int,
    seed: int,
) -> list[PacketStructureRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rng = random.Random(seed)
    discriminants = [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]
    rows: list[PacketStructureRow] = []
    seen: set[int] = set()
    cases = 0
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
        for m in quotient_sizes:
            n = h // m
            for factor in packet_factors(n, q):
                if factor.degree() == 1:
                    continue
                rows.append(
                    audit_packet(
                        D=D,
                        q=q,
                        ell=ell,
                        cycle=cycle,
                        m=m,
                        factor=factor,
                        rng=rng,
                        random_trials=random_trials,
                        shuffle_trials=shuffle_trials,
                    )
                )
        cases += 1
        if cases >= max_cases:
            break
    return rows


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-cases", type=int, default=20)
    ap.add_argument("--min-h", type=int, default=12)
    ap.add_argument("--max-h", type=int, default=90)
    ap.add_argument("--max-abs-D", type=int, default=15000)
    ap.add_argument("--max-quotients", type=int, default=3)
    ap.add_argument("--min-n", type=int, default=5)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=150000)
    ap.add_argument("--random-trials", type=int, default=200)
    ap.add_argument("--shuffle-trials", type=int, default=200)
    ap.add_argument("--seed", type=int, default=20260604)
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
        random_trials=args.random_trials,
        shuffle_trials=args.shuffle_trials,
        seed=args.seed,
    )

    print("Hermitian packet structure scan")
    print(f"max_cases={args.max_cases}")
    print(f"min_h={args.min_h}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"random_trials={args.random_trials}")
    print(f"shuffle_trials={args.shuffle_trials}")
    print(f"seed={args.seed}")
    print()

    if not args.summary_only:
        print(
            "columns: D q ell h m n deg coord_zero term_zero span_rank "
            "cm_zero random_zeros/trials random_span_defects "
            "shuffled_zeros/trials shuffled_span_defects"
        )
        for row in rows:
            print(
                f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
                f"m={row.m:3d} n={row.n:3d} deg={row.factor_degree:3d} "
                f"coord_zero={row.coord_zero_count:3d} "
                f"term_zero={row.term_zero_count:3d} "
                f"span_rank={row.span_rank:3d}/{row.max_possible_span:<3d} "
                f"cm_zero={int(row.cm_hermitian_zero)} "
                f"random_zeros={row.random_vector_zeros}/{row.random_vector_trials} "
                f"random_span_defects={row.random_vector_span_defects} "
                f"shuffled_zeros={row.shuffled_cycle_zeros}/{row.shuffled_cycle_trials} "
                f"shuffled_span_defects={row.shuffled_cycle_span_defects}"
            )

    packet_rows = len(rows)
    print()
    print("summary")
    print(f"  packet_rows={packet_rows}")
    print(f"  cm_hermitian_zero_packets={sum(row.cm_hermitian_zero for row in rows)}")
    print(f"  cm_any_zero_coordinate_packets={sum(row.coord_zero_count > 0 for row in rows)}")
    print(f"  cm_any_zero_term_packets={sum(row.term_zero_count > 0 for row in rows)}")
    print(f"  cm_maximal_span_packets={sum(row.span_maximal for row in rows)}")
    print(f"  cm_span_defect_packets={sum(not row.span_maximal for row in rows)}")
    print(f"  factor_degree_gt_m_packets={sum(row.factor_degree > row.m for row in rows)}")
    print(f"  random_vector_zeros={sum(row.random_vector_zeros for row in rows)}")
    print(f"  random_vector_trials={sum(row.random_vector_trials for row in rows)}")
    print(f"  random_vector_span_defects={sum(row.random_vector_span_defects for row in rows)}")
    print(f"  shuffled_cycle_zeros={sum(row.shuffled_cycle_zeros for row in rows)}")
    print(f"  shuffled_cycle_trials={sum(row.shuffled_cycle_trials for row in rows)}")
    print(f"  shuffled_cycle_span_defects={sum(row.shuffled_cycle_span_defects for row in rows)}")
    if rows:
        worst_span = min(row.span_rank / row.max_possible_span for row in rows)
        max_coord_zeros = max(row.coord_zero_count for row in rows)
        max_term_zeros = max(row.term_zero_count for row in rows)
        print(f"  worst_span_rank_ratio={worst_span:.6f}")
        print(f"  max_coord_zero_count={max_coord_zeros}")
        print(f"  max_term_zero_count={max_term_zeros}")
    print()
    print("interpretation")
    print("  coordinate_nonvanishing_is_the_product_certificate_signal=1")
    print("  maximal_span_uses_min_m_degree_not_factor_degree=1")
    print("  maximal_span_does_not_rule_out_hermitian_isotropy=1")
    print("  random_controls_are_diagnostics_not_certificates=1")
    print("  useful_theorem_candidate_must_explain_cm_packet_structure_not_generic_isotropy=1")
    print("conclusion=reported_hermitian_packet_structure_scan")


if __name__ == "__main__":
    main()
