#!/usr/bin/env python3
"""Axis-support injectivity scan for the L1 tower scalar.

The L1 scalar uses the coefficient function

    w(r) = 1 + sum_c (r mod c)

where the coprime components c multiply to the complement size m.  More
generally, the tower-native axis coefficient space is

    W_axis = {a0 + sum_c g_c(r mod c)}.

After fixing a Frobenius packet factor f | Phi_n and complement fibers
J_r mod f, evaluation at a selected K-origin gives an F_q-linear map

    T_f : W_axis -> F_q[X]/(f),
    w   -> sum_r w(r) J_r.

If T_f is injective, then every nonzero axis scalar is nonzero in that packet,
including L1.  This is stronger than the previous "translate rank" diagnostic:
it rules out selected-origin cancellation for all axis-supported weights.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
    rotate,
    section_fiber_polynomials,
)
from crt_partial_moment_projection_scan import (
    coprime_components,
    scale_poly,
    sum_polys,
    zero_poly_like,
)


@dataclass(frozen=True)
class AxisRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    components: tuple[int, ...]
    origin_shift: int
    content_zero: bool
    axis_dim: int
    axis_rank: int
    pivot_max: int | None
    y0_zero: bool
    block_internal_failures: int
    pair_directness_failures: int
    cross_directness_failure: bool
    full_k_rank: int
    full_k_pivot_max: int | None
    full_k_injective_possible: bool
    full_k_injective_failure: bool
    injective_possible: bool
    injective_failure: bool
    m0_zero: bool
    l1_zero: bool
    random_trials: int
    random_nonzero_trials: int
    random_zero_hits: int


def rank_mod_q(matrix: list[list[int]], q: int) -> int:
    return len(pivot_columns_mod_q(matrix, q))


def pivot_columns_mod_q(matrix: list[list[int]], q: int) -> list[int]:
    mat = [row[:] for row in matrix if any(value % q for value in row)]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    pivots: list[int] = []
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
        mat[rank] = [(value * inv) % q for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            scale = mat[row][col] % q
            if scale:
                mat[row] = [
                    (left - scale * right) % q
                    for left, right in zip(mat[row], mat[rank])
                ]
        rank += 1
        pivots.append(col)
        if rank == rows:
            break
    return pivots


def coeff_vector(poly: sp.Poly, degree: int, q: int) -> list[int]:
    x = poly.gens[0]
    reduced = poly
    return [int(reduced.coeff_monomial(x**i)) % q for i in range(degree)]


def axis_basis_images(
    residues: list[sp.Poly],
    components: tuple[int, ...],
    factor: sp.Poly,
) -> list[tuple[str, sp.Poly]]:
    """Images of a basis for a0 + sum_c g_c(r mod c).

    The basis is the constant function plus indicators 1_{r == t mod c} for
    t=1..c-1.  Omitting t=0 removes the redundant component constants.
    """
    images: list[tuple[str, sp.Poly]] = [("1", sum_polys(residues).rem(factor))]
    for component in components:
        for t in range(1, component):
            subtotal = zero_poly_like(residues[0])
            for r in range(t, len(residues), component):
                subtotal += residues[r]
            images.append((f"I{component}_{t}", subtotal.rem(factor)))
    return images


def block_internal_failure_count(
    images: list[tuple[str, sp.Poly]],
    components: tuple[int, ...],
    factor_degree: int,
    q: int,
) -> int:
    image_by_name = dict(images)
    failures = 0
    for component in components:
        block = [image_by_name["1"]]
        block.extend(image_by_name[f"I{component}_{t}"] for t in range(1, component))
        vectors = [coeff_vector(poly, factor_degree, q) for poly in block]
        expected_rank = len(block)
        if factor_degree >= expected_rank and rank_mod_q(vectors, q) < expected_rank:
            failures += 1
    return failures


def rank_for_names(
    images: list[tuple[str, sp.Poly]],
    names: list[str],
    factor_degree: int,
    q: int,
) -> int:
    image_by_name = dict(images)
    vectors = [coeff_vector(image_by_name[name], factor_degree, q) for name in names]
    return rank_mod_q(vectors, q)


def pair_directness_failure_count(
    images: list[tuple[str, sp.Poly]],
    components: tuple[int, ...],
    factor_degree: int,
    q: int,
) -> int:
    failures = 0
    for i, left in enumerate(components):
        for right in components[i + 1 :]:
            names = ["1"]
            names.extend(f"I{left}_{t}" for t in range(1, left))
            names.extend(f"I{right}_{t}" for t in range(1, right))
            expected_rank = 1 + (left - 1) + (right - 1)
            if factor_degree >= expected_rank:
                if rank_for_names(images, names, factor_degree, q) < expected_rank:
                    failures += 1
    return failures


def linear_combo_from_vectors(
    vectors: list[list[int]],
    coeffs: list[int],
    q: int,
) -> list[int]:
    if not vectors:
        return []
    total = [0] * len(vectors[0])
    for coeff, vector in zip(coeffs, vectors):
        c = coeff % q
        if not c:
            continue
        total = [(left + c * right) % q for left, right in zip(total, vector)]
    return total


def l1_from_axis_images(
    images: list[tuple[str, sp.Poly]],
    components: tuple[int, ...],
    factor: sp.Poly,
) -> sp.Poly:
    image_by_name = dict(images)
    total = image_by_name["1"]
    for component in components:
        for t in range(1, component):
            total += scale_poly(image_by_name[f"I{component}_{t}"], t)
    return total.rem(factor)


def random_zero_count(
    vectors: list[list[int]],
    q: int,
    trials: int,
    rng: random.Random,
) -> tuple[int, int]:
    nonzero_trials = 0
    zero_hits = 0
    for _ in range(trials):
        coeffs = [rng.randrange(q) for _ in vectors]
        if not any(coeffs):
            continue
        nonzero_trials += 1
        value = linear_combo_from_vectors(vectors, coeffs, q)
        if not any(value):
            zero_hits += 1
    return nonzero_trials, zero_hits


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    origin_shift: int,
    random_trials: int,
    rng: random.Random,
) -> AxisRow:
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]
    full_k_pivots = pivot_columns_mod_q(residue_vectors, q)
    full_k_rank = len(full_k_pivots)
    full_k_possible = factor.degree() >= m
    components = coprime_components(m)
    images = axis_basis_images(residues, components, factor)
    vectors = [coeff_vector(poly, factor.degree(), q) for _, poly in images]
    axis_dim = len(images)
    pivots = pivot_columns_mod_q(vectors, q)
    axis_rank = len(pivots)
    block_failures = block_internal_failure_count(
        images, components, factor.degree(), q
    )
    pair_failures = pair_directness_failure_count(
        images, components, factor.degree(), q
    )
    m0 = images[0][1]
    l1 = l1_from_axis_images(images, components, factor)
    nonzero_trials, zero_hits = random_zero_count(vectors, q, random_trials, rng)
    injective_possible = factor.degree() >= axis_dim
    content_zero = all(residue.is_zero for residue in residues)
    return AxisRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        components=components,
        origin_shift=origin_shift,
        content_zero=content_zero,
        axis_dim=axis_dim,
        axis_rank=axis_rank,
        pivot_max=(pivots[-1] if pivots else None),
        y0_zero=m0.is_zero,
        block_internal_failures=block_failures,
        pair_directness_failures=pair_failures,
        cross_directness_failure=(
            factor.degree() >= axis_dim
            and axis_rank < axis_dim
            and block_failures == 0
            and not content_zero
        ),
        full_k_rank=full_k_rank,
        full_k_pivot_max=(full_k_pivots[-1] if full_k_pivots else None),
        full_k_injective_possible=full_k_possible,
        full_k_injective_failure=full_k_possible and full_k_rank < m and not content_zero,
        injective_possible=injective_possible,
        injective_failure=injective_possible and axis_rank < axis_dim and not content_zero,
        m0_zero=m0.is_zero,
        l1_zero=l1.is_zero,
        random_trials=random_trials,
        random_nonzero_trials=nonzero_trials,
        random_zero_hits=zero_hits,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[AxisRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rng = random.Random(args.seed)
    rows: list[AxisRow] = []
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
            quotient_sizes = [m for m in quotient_sizes if len(coprime_components(m)) >= 2]
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
            shifts = range(h) if args.scan_origins else range(1)
            for shift in shifts:
                shifted = rotate(cycle, shift)
                for m in quotient_sizes:
                    n = h // m
                    for factor in packet_factors(n, q):
                        if factor.degree() == 1 and not args.include_linear:
                            continue
                        axis_dim = 1 + sum(c - 1 for c in coprime_components(m))
                        if args.require_deg_ge_axis_dim and factor.degree() < axis_dim:
                            continue
                        rows.append(
                            audit_packet(
                                D=D,
                                q=q,
                                ell=ell,
                                cycle=shifted,
                                m=m,
                                factor=factor,
                                origin_shift=shift,
                                random_trials=args.random_trials,
                                rng=rng,
                            )
                        )
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=60)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=180)
    parser.add_argument("--max-abs-D", type=int, default=80000)
    parser.add_argument("--max-prime-quotients", type=int, default=8)
    parser.add_argument("--max-composite-quotients", type=int, default=8)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=180)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=800000)
    parser.add_argument("--max-splitting-primes", type=int, default=2)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--scan-origins", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--require-deg-ge-axis-dim", action="store_true")
    parser.add_argument("--random-trials", type=int, default=0)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    nonzero_rows = [row for row in rows if not row.content_zero]
    possible_rows = [row for row in nonzero_rows if row.injective_possible]
    injective_rows = [row for row in possible_rows if row.axis_rank == row.axis_dim]
    injective_failures = [row for row in possible_rows if row.injective_failure]
    l1_zeros = [row for row in nonzero_rows if row.l1_zero]
    m0_zeros = [row for row in nonzero_rows if row.m0_zero]
    dimension_bound_rows = [row for row in nonzero_rows if not row.injective_possible]
    rank_defect_hist: dict[int, int] = {}
    for row in nonzero_rows:
        defect = row.axis_dim - row.axis_rank
        rank_defect_hist[defect] = rank_defect_hist.get(defect, 0) + 1
    block_internal_failure_rows = [
        row for row in nonzero_rows if row.block_internal_failures
    ]
    pair_directness_failure_rows = [
        row for row in nonzero_rows if row.pair_directness_failures
    ]
    cross_directness_failure_rows = [
        row for row in nonzero_rows if row.cross_directness_failure
    ]
    full_k_possible_rows = [
        row for row in nonzero_rows if row.full_k_injective_possible
    ]
    full_k_injective_rows = [
        row for row in full_k_possible_rows if row.full_k_rank == row.m
    ]
    full_k_failure_rows = [
        row for row in nonzero_rows if row.full_k_injective_failure
    ]

    print("L1 axis-injectivity scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"max_splitting_primes={args.max_splitting_primes}")
    print(f"include_linear={args.include_linear}")
    print(f"scan_origins={args.scan_origins}")
    print(f"require_composite_m={args.require_composite_m}")
    print(f"require_deg_ge_axis_dim={args.require_deg_ge_axis_dim}")
    print(f"random_trials={args.random_trials}")
    print()
    if not args.summary_only:
        print(
            "columns: D q ell h m n n_prime deg axis_dim axis_rank "
            "pivot_max y0_zero block_fail pair_fail components origin "
            "content_zero fullK M0_zero L1_zero rand_zero"
        )
        display_rows = injective_failures + l1_zeros + m0_zeros[:20]
        if not display_rows:
            display_rows = rows[:40]
        for row in display_rows:
            print(
                f"D={row.D:7d} q={row.q:7d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"n_prime={int(row.n_is_prime)} deg={row.factor_degree:3d} "
                f"axis_dim={row.axis_dim:3d} axis_rank={row.axis_rank:3d} "
                f"pivot_max={-1 if row.pivot_max is None else row.pivot_max:3d} "
                f"y0_zero={int(row.y0_zero)} "
                f"block_fail={row.block_internal_failures:2d} "
                f"pair_fail={row.pair_directness_failures:2d} "
                f"components={list(row.components)} origin={row.origin_shift:3d} "
                f"content_zero={int(row.content_zero)} "
                f"fullK={row.full_k_rank:3d}/{row.m:3d} "
                f"fullK_pivot={-1 if row.full_k_pivot_max is None else row.full_k_pivot_max:3d} "
                f"M0_zero={int(row.m0_zero)} L1_zero={int(row.l1_zero)} "
                f"rand_zero={row.random_zero_hits}/{row.random_nonzero_trials}"
            )

    print()
    print("summary")
    print(f"  packet_rows={len(rows)}")
    print(f"  nonzero_rows={len(nonzero_rows)}")
    print(f"  dimension_bound_rows={len(dimension_bound_rows)}")
    print(f"  injective_possible_rows={len(possible_rows)}")
    print(f"  injective_rows={len(injective_rows)}")
    print(f"  injective_failures={len(injective_failures)}")
    print(f"  block_internal_failure_rows={len(block_internal_failure_rows)}")
    print(f"  pair_directness_failure_rows={len(pair_directness_failure_rows)}")
    print(f"  cross_directness_failure_rows={len(cross_directness_failure_rows)}")
    print(f"  full_k_injective_possible_rows={len(full_k_possible_rows)}")
    print(f"  full_k_injective_rows={len(full_k_injective_rows)}")
    print(f"  full_k_injective_failure_rows={len(full_k_failure_rows)}")
    print(f"  m0_zero_rows={len(m0_zeros)}")
    print(f"  l1_zero_rows={len(l1_zeros)}")
    print(f"  rank_defect_histogram={dict(sorted(rank_defect_hist.items()))}")
    injective_prefixes = [
        row.pivot_max + 1
        for row in injective_rows
        if row.pivot_max is not None
    ]
    if injective_prefixes:
        print(f"  injective_pivot_prefix_min={min(injective_prefixes)}")
        print(f"  injective_pivot_prefix_max={max(injective_prefixes)}")
    full_k_prefixes = [
        row.full_k_pivot_max + 1
        for row in full_k_injective_rows
        if row.full_k_pivot_max is not None
    ]
    if full_k_prefixes:
        print(f"  full_k_pivot_prefix_min={min(full_k_prefixes)}")
        print(f"  full_k_pivot_prefix_max={max(full_k_prefixes)}")
    print(f"  random_zero_hits={sum(row.random_zero_hits for row in nonzero_rows)}")
    print(f"  random_nonzero_trials={sum(row.random_nonzero_trials for row in nonzero_rows)}")
    print()
    print("interpretation")
    print("  axis_injectivity_implies_L1_nonzero_for_every_nonzero_axis_weight=1")
    print("  dimension_bound_rows_have_factor_degree_below_axis_dimension=1")
    print("  p24_factor_degree_388430_is_much_larger_than_axis_dimension_368=1")
    print("conclusion=reported_l1_axis_injectivity_scan")


if __name__ == "__main__":
    main()
