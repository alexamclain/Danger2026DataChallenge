#!/usr/bin/env python3
"""Edge-coordinate shape diagnostic for packet scalar norms.

The plain-j divisor diagnostics ask whether a packet scalar norm is a low
degree function of the selected CM root `j_i`.  A phase-aware correspondence
route could instead live on an oriented edge or short path.  This script tests
the first such coordinate:

    (x_i, z_i) = (j_i, j_{i+step}).

For each rotated origin it computes a packet norm value and asks whether

    value_i = F(x_i, z_i)

or `value_i = P(x_i,z_i)/Q(x_i,z_i)` has unexpectedly low bidegree, compared
with random controls preserving any observed H-periodicity.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp
from cypari2 import Pari

from abstract_embedded_pairing_non_genus_toy import null_vector_mod_q
from cycle_period_complexity_scan import find_full_cycle_prime
from embedded_selector_identity_toy import nullspace_mod
from l1_interpolation_shape_scan import h_period_invariant, random_values_like
from l1_selected_origin_zero_scan import scalar_value as l1_scalar_value
from packet_scalar_divisor_shape_toy import packet_norm_value as energy_packet_norm_value
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any, rotate
from crt_partial_moment_projection_scan import coprime_components

X = sp.symbols("X")


@dataclass(frozen=True)
class EdgeShapeRow:
    scalar: str
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    step: int
    components: tuple[int, ...]
    zero_values: int
    distinct_values: int
    h_period_ok: bool
    first_poly_bidegree: tuple[int, int] | None
    first_poly_variables: int | None
    random_poly_hits: int
    first_rat_bidegree: tuple[int, int] | None
    first_rat_variables: int | None
    random_rat_hits: int
    variable_threshold: int


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    row_count = len(rows)
    col_count = len(rows[0])
    rank = 0
    for col in range(col_count):
        pivot = None
        for row in range(rank, row_count):
            if rows[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col] % q, -1, q)
        rows[rank] = [(value * inv) % q for value in rows[rank]]
        for row in range(row_count):
            if row == rank or rows[row][col] % q == 0:
                continue
            factor = rows[row][col] % q
            rows[row] = [
                (rows[row][j] - factor * rows[rank][j]) % q
                for j in range(col_count)
            ]
        rank += 1
        if rank == row_count:
            break
    return rank


def monomial_row(x: int, z: int, deg_x: int, deg_z: int, q: int) -> list[int]:
    xpows = [1]
    zpows = [1]
    for _ in range(deg_x):
        xpows.append(xpows[-1] * x % q)
    for _ in range(deg_z):
        zpows.append(zpows[-1] * z % q)
    return [xpows[i] * zpows[j] % q for i in range(deg_x + 1) for j in range(deg_z + 1)]


def degree_pairs(max_degree: int) -> list[tuple[int, int]]:
    pairs = [(i, j) for i in range(max_degree + 1) for j in range(max_degree + 1)]
    return sorted(pairs, key=lambda pair: ((pair[0] + 1) * (pair[1] + 1), pair[0] + pair[1], pair))


def has_polynomial_bidegree(
    xs: list[int],
    zs: list[int],
    ys: list[int],
    q: int,
    deg_x: int,
    deg_z: int,
) -> bool:
    matrix = [monomial_row(x, z, deg_x, deg_z, q) for x, z in zip(xs, zs)]
    augmented = [row + [y % q] for row, y in zip(matrix, ys)]
    return rank_mod(matrix, q) == rank_mod(augmented, q)


def first_polynomial_bidegree(
    xs: list[int],
    zs: list[int],
    ys: list[int],
    q: int,
    max_degree: int,
) -> tuple[int, int] | None:
    for deg_x, deg_z in degree_pairs(max_degree):
        if has_polynomial_bidegree(xs, zs, ys, q, deg_x, deg_z):
            return deg_x, deg_z
    return None


def eval_poly2(coeffs: list[int], x: int, z: int, q: int, deg_x: int, deg_z: int) -> int:
    row = monomial_row(x, z, deg_x, deg_z, q)
    return sum(c * v for c, v in zip(coeffs, row)) % q


def rational_candidate_valid(
    vec: list[int],
    xs: list[int],
    zs: list[int],
    ys: list[int],
    q: int,
    deg_x: int,
    deg_z: int,
) -> bool:
    variables = (deg_x + 1) * (deg_z + 1)
    num = [v % q for v in vec[:variables]]
    den = [v % q for v in vec[variables:]]
    if all(v == 0 for v in den):
        return False
    for x, z, y in zip(xs, zs, ys):
        den_value = eval_poly2(den, x, z, q, deg_x, deg_z)
        if den_value == 0:
            return False
        if eval_poly2(num, x, z, q, deg_x, deg_z) != y * den_value % q:
            return False
    return True


def has_rational_bidegree(
    xs: list[int],
    zs: list[int],
    ys: list[int],
    q: int,
    deg_x: int,
    deg_z: int,
    rng: random.Random,
    random_combos: int,
) -> bool:
    rows: list[list[int]] = []
    for x, z, y in zip(xs, zs, ys):
        row = monomial_row(x, z, deg_x, deg_z, q)
        rows.append(row + [(-y * value) % q for value in row])
    vec = null_vector_mod_q(rows, q)
    if vec is not None and rational_candidate_valid(vec, xs, zs, ys, q, deg_x, deg_z):
        return True

    # Try a few random nullspace combinations if the first basis vector has a
    # pole at a sample point.
    basis, _ = nullspace_mod(rows, q)
    if not basis:
        return False
    candidates = basis[:]
    for _ in range(random_combos):
        coeffs = [rng.randrange(q) for _ in basis]
        if not any(coeffs):
            coeffs[0] = 1
        candidate = [0] * len(basis[0])
        for coeff, base in zip(coeffs, basis):
            if coeff:
                candidate = [(v + coeff * b) % q for v, b in zip(candidate, base)]
        candidates.append(candidate)
    return any(
        rational_candidate_valid(candidate, xs, zs, ys, q, deg_x, deg_z)
        for candidate in candidates
    )


def first_rational_bidegree(
    xs: list[int],
    zs: list[int],
    ys: list[int],
    q: int,
    max_degree: int,
    rng: random.Random,
    random_combos: int,
) -> tuple[int, int] | None:
    for deg_x, deg_z in degree_pairs(max_degree):
        if has_rational_bidegree(xs, zs, ys, q, deg_x, deg_z, rng, random_combos):
            return deg_x, deg_z
    return None


def packet_norm_for_scalar(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> int:
    if scalar in ("hermitian", "ordinary"):
        return energy_packet_norm_value(cycle, q, m, factor, scalar)
    if scalar in ("M0", "L1"):
        poly = l1_scalar_value(cycle, q, m, factor, scalar).rem(factor)
        if poly.is_zero:
            return 0
        return int(sp.resultant(factor.as_expr(), poly.as_expr(), X)) % q
    raise ValueError(f"unknown scalar {scalar}")


def packet_values(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> list[int]:
    out: list[int] = []
    for shift in range(len(cycle)):
        out.append(packet_norm_for_scalar(rotate(cycle, shift), q, m, factor, scalar))
    return out


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    scalar: str,
    step: int,
    max_bidegree: int,
    random_trials: int,
    random_combos: int,
    rng: random.Random,
) -> EdgeShapeRow:
    h = len(cycle)
    xs = [cycle[i] % q for i in range(h)]
    zs = [cycle[(i + step) % h] % q for i in range(h)]
    ys = packet_values(cycle, q, m, factor, scalar)
    h_period_ok = h_period_invariant(ys, m)
    poly = first_polynomial_bidegree(xs, zs, ys, q, max_bidegree)
    rat = first_rational_bidegree(xs, zs, ys, q, max_bidegree, rng, random_combos)
    poly_variables = None if poly is None else (poly[0] + 1) * (poly[1] + 1)
    rat_variables = None if rat is None else (rat[0] + 1) * (rat[1] + 1)

    random_poly_hits = 0
    random_rat_hits = 0
    for _ in range(random_trials):
        random_ys = random_values_like(q, h, m, h_period_ok, rng)
        if first_polynomial_bidegree(xs, zs, random_ys, q, max_bidegree) is not None:
            random_poly_hits += 1
        if first_rational_bidegree(xs, zs, random_ys, q, max_bidegree, rng, random_combos) is not None:
            random_rat_hits += 1

    n = h // m
    return EdgeShapeRow(
        scalar=scalar,
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        step=step,
        components=coprime_components(m),
        zero_values=sum(value == 0 for value in ys),
        distinct_values=len(set(ys)),
        h_period_ok=h_period_ok,
        first_poly_bidegree=poly,
        first_poly_variables=poly_variables,
        random_poly_hits=random_poly_hits,
        first_rat_bidegree=rat,
        first_rat_variables=rat_variables,
        random_rat_hits=random_rat_hits,
        variable_threshold=(h + 1) // 2,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[EdgeShapeRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rng = random.Random(args.seed)
    rows: list[EdgeShapeRow] = []
    cases = 0
    seen: set[int] = set()
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
            steps = args.steps or [1]
            for m in quotient_sizes:
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    for step in steps:
                        for scalar in args.scalars:
                            rows.append(
                                audit_packet(
                                    D,
                                    q,
                                    ell,
                                    cycle,
                                    m,
                                    factor,
                                    scalar,
                                    step % h,
                                    args.max_bidegree,
                                    args.random_trials,
                                    args.random_combos,
                                    rng,
                                )
                            )
                            if len(rows) >= args.max_rows:
                                return rows
        if case_had_cycle:
            cases += 1
            if cases >= args.max_cases:
                break
    return rows


def theorem_relevant_poly(row: EdgeShapeRow, random_trials: int) -> bool:
    return (
        row.first_poly_variables is not None
        and row.first_poly_variables < row.h
        and row.random_poly_hits == 0
    )


def theorem_relevant_rat(row: EdgeShapeRow, random_trials: int) -> bool:
    return (
        row.first_rat_variables is not None
        and 2 * row.first_rat_variables <= row.h
        and row.random_rat_hits == 0
    )


def theorem_relevant(row: EdgeShapeRow, random_trials: int) -> bool:
    return theorem_relevant_poly(row, random_trials) or theorem_relevant_rat(row, random_trials)


def fmt_pair(pair: tuple[int, int] | None) -> str:
    return "none" if pair is None else f"{pair[0]},{pair[1]}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scalars", nargs="+", choices=("hermitian", "ordinary", "M0", "L1"), default=["hermitian", "L1"])
    parser.add_argument("--steps", nargs="*", type=int)
    parser.add_argument("--max-cases", type=int, default=8)
    parser.add_argument("--min-h", type=int, default=12)
    parser.add_argument("--max-h", type=int, default=80)
    parser.add_argument("--max-abs-D", type=int, default=20000)
    parser.add_argument("--max-prime-quotients", type=int, default=3)
    parser.add_argument("--max-composite-quotients", type=int, default=3)
    parser.add_argument("--min-n", type=int, default=3)
    parser.add_argument("--max-n", type=int, default=80)
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=160000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--require-composite-m", action="store_true")
    parser.add_argument("--max-bidegree", type=int, default=4)
    parser.add_argument("--random-trials", type=int, default=6)
    parser.add_argument("--random-combos", type=int, default=8)
    parser.add_argument("--max-rows", type=int, default=40)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    fitted = [
        row for row in rows
        if row.first_poly_bidegree is not None or row.first_rat_bidegree is not None
    ]
    relevant = [row for row in rows if theorem_relevant(row, args.random_trials)]
    l1_rows = [row for row in rows if row.scalar == "L1"]
    hermitian_rows = [row for row in rows if row.scalar == "hermitian"]

    print("packet scalar edge-coordinate shape scan")
    print(f"scalars={args.scalars}")
    print(f"steps={args.steps or [1]}")
    print(f"max_bidegree={args.max_bidegree}")
    print(f"random_trials={args.random_trials}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print()
    if not args.summary_only:
        print(
            "columns: scalar D q ell h m n deg step components zero_values "
            "distinct_values H_period_ok poly_bideg poly_vars poly_rand_hits "
            "rat_bideg rat_vars rat_rand_hits variable_threshold theorem_relevant"
        )
        for row in rows:
            print(
                f"scalar={row.scalar:9s} D={row.D:7d} q={row.q:6d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} deg={row.factor_degree:3d} "
                f"step={row.step:3d} components={list(row.components)} "
                f"zero_values={row.zero_values:3d} distinct_values={row.distinct_values:3d} "
                f"H_period_ok={int(row.h_period_ok)} "
                f"poly_bideg={fmt_pair(row.first_poly_bidegree)} "
                f"poly_vars={row.first_poly_variables} "
                f"poly_rand_hits={row.random_poly_hits}/{args.random_trials} "
                f"rat_bideg={fmt_pair(row.first_rat_bidegree)} "
                f"rat_vars={row.first_rat_variables} "
                f"rat_rand_hits={row.random_rat_hits}/{args.random_trials} "
                f"variable_threshold={row.variable_threshold} "
                f"theorem_relevant={int(theorem_relevant(row, args.random_trials))}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  rows_with_any_edge_fit_in_search_window={len(fitted)}")
    print(f"  rows_with_theorem_relevant_edge_fit={len(relevant)}")
    print(f"  l1_rows={len(l1_rows)}")
    print(f"  l1_rows_with_theorem_relevant_edge_fit={sum(theorem_relevant(row, args.random_trials) for row in l1_rows)}")
    print(f"  hermitian_rows={len(hermitian_rows)}")
    print(f"  hermitian_rows_with_theorem_relevant_edge_fit={sum(theorem_relevant(row, args.random_trials) for row in hermitian_rows)}")
    print()
    print("interpretation")
    print("  variables_below_h_are_needed_to_beat_interpolation_noise=1")
    print("  random_controls_preserve_H_repetition_when_present=1")
    print("  low_edge_relation_matching_random_controls_is_not_theorem_evidence=1")
    print("  no_low_relation_supports_correspondence_edge_obstruction=1")
    print("conclusion=reported_packet_scalar_edge_shape_scan")


if __name__ == "__main__":
    main()
