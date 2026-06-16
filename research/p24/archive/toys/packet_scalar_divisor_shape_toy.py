#!/usr/bin/env python3
"""Divisor-shape diagnostics for packet scalar functions on CM torsors.

The phase-aware Borcherds route would be much more credible if a packet scalar
looked like a special modular-function value on the CM torsor.  This toy does
not try to prove that.  It asks a cheaper falsification question:

  As a function of the selected CM root j_i, does a packet scalar interpolate
  at lower degree than random data on the same root set?

For each small CM cycle and packet factor f | Phi_n, we rotate the cycle
through all CM roots and compute the selected packet scalar norm:

    value(j_i) = Res(f, scalar_poly(rotate_i(cycle))).

Then we compare the minimal polynomial/rational interpolation degree of this
function with random controls preserving the number of zero values.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime, find_splitting_prime
from embedded_decomposition_calibration import isogeny_neighbors, pari_linear_roots, walk_cycle
from embedded_selector_identity_toy import (
    candidate_from_basis,
    matrix_for_degree,
    nullspace_mod,
)
from packetized_relative_content_scan import (
    autocorrelation_energy_poly,
    hermitian_energy_poly,
    packet_factors,
    quotient_sizes_with_prime_subgroup,
)
from relative_moment_projection_scan import rotate

X = sp.symbols("X")


@dataclass(frozen=True)
class PacketShapeRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    scalar: str
    zero_values: int
    polynomial_degree: int
    rational_degree: int
    random_polynomial_degree_mean: float
    random_rational_degree_mean: float
    random_polynomial_degree_min: int
    random_rational_degree_min: int
    numerator_roots: int
    numerator_roots_in_cm: int


def scalar_poly(cycle: list[int], q: int, m: int, scalar: str) -> sp.Poly:
    if scalar == "hermitian":
        return hermitian_energy_poly(cycle, q, m)
    if scalar == "ordinary":
        return autocorrelation_energy_poly(cycle, q, m)
    raise ValueError(f"unknown scalar {scalar}")


def packet_norm_value(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> int:
    poly = scalar_poly(cycle, q, m, scalar)
    return int(sp.resultant(factor.as_expr(), poly.as_expr(), X)) % q


def packet_values(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for shift in range(len(cycle)):
        shifted = rotate(cycle, shift)
        out.append((cycle[shift] % q, packet_norm_value(shifted, q, m, factor, scalar)))
    return out


def rank_mod(matrix: list[list[int]], q: int) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    m = len(rows)
    n = len(rows[0])
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(m):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % q for j in range(n)]
        r += 1
        if r == m:
            break
    return r


def polynomial_degree(pairs: list[tuple[int, int]], q: int) -> int:
    for degree in range(len(pairs)):
        matrix: list[list[int]] = []
        rhs: list[list[int]] = []
        for x, y in pairs:
            powers = [1]
            for _ in range(degree):
                powers.append(powers[-1] * x % q)
            matrix.append(powers)
            rhs.append(powers + [y % q])
        if rank_mod(matrix, q) == rank_mod(rhs, q):
            return degree
    raise RuntimeError("polynomial interpolation failed")


def rational_degree(pairs: list[tuple[int, int]], q: int) -> int:
    for degree in range(len(pairs)):
        matrix = matrix_for_degree(pairs, degree, q)
        basis, _ = nullspace_mod(matrix, q)
        if candidate_from_basis(basis, degree, pairs, q) is not None:
            return degree
    raise RuntimeError("rational interpolation failed")


def random_values_like(
    xs: list[int],
    q: int,
    zero_count: int,
    rng: random.Random,
) -> list[tuple[int, int]]:
    zero_positions = set(rng.sample(range(len(xs)), zero_count))
    pairs: list[tuple[int, int]] = []
    for i, x in enumerate(xs):
        if i in zero_positions:
            pairs.append((x, 0))
        else:
            pairs.append((x, rng.randrange(1, q)))
    return pairs


def numerator_root_stats(
    pairs: list[tuple[int, int]],
    q: int,
    degree: int,
) -> tuple[int, int]:
    matrix: list[list[int]] = []
    for x, y in pairs:
        powers = [1]
        for _ in range(degree):
            powers.append(powers[-1] * x % q)
        matrix.append(powers + [(-y * xp) % q for xp in powers])
    basis, _ = nullspace_mod(matrix, q)
    candidate = candidate_from_basis(basis, degree, pairs, q)
    if candidate is None:
        return 0, 0
    numerator, denominator = candidate
    cm_roots = {x for x, _ in pairs}
    roots = []
    for x in range(q):
        num = 0
        den = 0
        for coeff in reversed(numerator):
            num = (num * x + coeff) % q
        for coeff in reversed(denominator):
            den = (den * x + coeff) % q
        if num == 0 and den != 0:
            roots.append(x)
    return len(roots), sum(root in cm_roots for root in roots)


def audit_packet(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    scalar: str,
    random_controls: int,
    rng: random.Random,
) -> PacketShapeRow:
    pairs = packet_values(cycle, q, m, factor, scalar)
    zero_count = sum(y == 0 for _, y in pairs)
    poly_degree = polynomial_degree(pairs, q)
    rat_degree = rational_degree(pairs, q)
    xs = [x for x, _ in pairs]

    random_poly_degrees: list[int] = []
    random_rat_degrees: list[int] = []
    for _ in range(random_controls):
        random_pairs = random_values_like(xs, q, zero_count, rng)
        random_poly_degrees.append(polynomial_degree(random_pairs, q))
        random_rat_degrees.append(rational_degree(random_pairs, q))

    numerator_roots, numerator_roots_in_cm = numerator_root_stats(pairs, q, rat_degree)
    h = len(cycle)
    n = h // m
    return PacketShapeRow(
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        factor_degree=factor.degree(),
        scalar=scalar,
        zero_values=zero_count,
        polynomial_degree=poly_degree,
        rational_degree=rat_degree,
        random_polynomial_degree_mean=sum(random_poly_degrees) / len(random_poly_degrees),
        random_rational_degree_mean=sum(random_rat_degrees) / len(random_rat_degrees),
        random_polynomial_degree_min=min(random_poly_degrees),
        random_rational_degree_min=min(random_rat_degrees),
        numerator_roots=numerator_roots,
        numerator_roots_in_cm=numerator_roots_in_cm,
    )


def fixed_cycle(D: int, q: int, ell: int | None) -> tuple[int, list[int]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(D)
    roots = pari_linear_roots(hilbert, q)
    if ell is not None:
        graph = isogeny_neighbors(roots, ell, q)
        return ell, walk_cycle(graph)
    full = find_full_cycle_prime(roots, D, q)
    if full is None:
        raise RuntimeError(f"no full cycle found for D={D}, q={q}")
    return full


def scan(args: argparse.Namespace) -> list[PacketShapeRow]:
    rng = random.Random(args.seed)
    cases: list[tuple[int, int, int | None]]
    if args.toy == "fixed":
        if args.D is None or args.q is None:
            raise ValueError("--toy fixed requires --D and --q")
        cases = [(args.D, args.q, args.ell)]
    else:
        cases = [(-5000, 1259, 3), (-2239, 2243, None)]

    out: list[PacketShapeRow] = []
    for D, q, ell_hint in cases:
        ell, cycle = fixed_cycle(D, q, ell_hint)
        h = len(cycle)
        quotient_sizes = quotient_sizes_with_prime_subgroup(
            h,
            max_quotients=args.max_quotients,
            min_n=args.min_n,
        )
        for m in quotient_sizes:
            for factor in packet_factors(h // m, q):
                if factor.degree() == 1 and not args.include_linear:
                    continue
                out.append(
                    audit_packet(
                        D,
                        q,
                        ell,
                        cycle,
                        m,
                        factor,
                        args.scalar,
                        args.random_controls,
                        rng,
                    )
                )
                if len(out) >= args.max_packets:
                    return out
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--toy", choices=("default", "fixed"), default="default")
    parser.add_argument("--D", type=int)
    parser.add_argument("--q", type=int)
    parser.add_argument("--ell", type=int)
    parser.add_argument("--scalar", choices=("hermitian", "ordinary"), default="hermitian")
    parser.add_argument("--max-quotients", type=int, default=3)
    parser.add_argument("--min-n", type=int, default=5)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--random-controls", type=int, default=20)
    parser.add_argument("--max-packets", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    rows = scan(args)
    print("packet scalar divisor-shape toy")
    print(f"toy={args.toy}")
    print(f"scalar={args.scalar}")
    print(f"random_controls={args.random_controls}")
    print(f"include_linear={args.include_linear}")
    print()
    print(
        "columns: D q ell h m n deg scalar zero_values poly_degree "
        "rand_poly_mean rand_poly_min rat_degree rand_rat_mean rand_rat_min "
        "num_roots num_roots_in_cm"
    )
    for row in rows:
        print(
            f"D={row.D:7d} q={row.q:6d} ell={row.ell:3d} h={row.h:3d} "
            f"m={row.m:3d} n={row.n:3d} deg={row.factor_degree:2d} "
            f"scalar={row.scalar:9s} zero_values={row.zero_values:2d} "
            f"poly_degree={row.polynomial_degree:2d} "
            f"rand_poly_mean={row.random_polynomial_degree_mean:5.2f} "
            f"rand_poly_min={row.random_polynomial_degree_min:2d} "
            f"rat_degree={row.rational_degree:2d} "
            f"rand_rat_mean={row.random_rational_degree_mean:5.2f} "
            f"rand_rat_min={row.random_rational_degree_min:2d} "
            f"num_roots={row.numerator_roots:2d} "
            f"num_roots_in_cm={row.numerator_roots_in_cm:2d}"
        )
    print()
    print("interpretation")
    print("  degree_near_random_means_no_simple_plain_j_divisor_shape=1")
    print("  low_degree_vs_random_would_support_a_structured_product_formula=1")
    print("  numerator_roots_outside_cm_are_a_generic-divisor_warning=1")
    print("conclusion=reported_packet_scalar_divisor_shape_toy")


if __name__ == "__main__":
    main()
