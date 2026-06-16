#!/usr/bin/env python3
"""Selected-origin interpolation diagnostic for L1 packet norms.

For each small split CM torsor, rotate the embedded cycle.  The selected root
is then `j_origin`, and the packet scalar is

    M0 or L1 in F_q[X]/(f),       f | Phi_n.

We reduce that scalar to a base-field value by taking its packet norm

    Res(f, scalar) mod q.

The diagnostic asks whether the function

    j_origin -> Norm_f(L1(origin))

has unexpectedly low polynomial or rational degree.  A low rational degree
well below the generic interpolation threshold would be evidence for an
embedded finite-field identity.  Generic degree supports the selected-origin
obstruction: the scalar may be nonzero, but it is not being selected by a
simple rational function of the CM root.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import random

import sympy as sp
from cypari2 import Pari

from abstract_embedded_pairing_non_genus_toy import null_vector_mod_q
from cycle_period_complexity_scan import find_full_cycle_prime
from l1_selected_origin_zero_scan import scalar_value
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import find_splitting_primes, quotient_sizes_any, rotate
from crt_partial_moment_projection_scan import coprime_components

X = sp.symbols("X")


@dataclass(frozen=True)
class InterpolationRow:
    scalar: str
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    n_is_prime: bool
    factor_degree: int
    components: tuple[int, ...]
    h_period_ok: bool
    zero_norms: int
    distinct_norms: int
    polynomial_degree: int
    random_poly_min: int
    random_poly_max: int
    rational_threshold: int
    rational_search_limit: int
    first_low_rational_degree: int | None
    random_low_rational_hits: int


def solve_square_mod_q(matrix: list[list[int]], rhs: list[int], q: int) -> list[int]:
    rows = [[v % q for v in row] + [rhs[i] % q] for i, row in enumerate(matrix)]
    n = len(matrix)
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, n):
            if rows[i][c] % q:
                pivot = i
                break
        if pivot is None:
            raise ValueError("singular interpolation matrix")
        rows[r], rows[pivot] = rows[pivot], rows[r]
        inv = pow(rows[r][c] % q, -1, q)
        rows[r] = [(v * inv) % q for v in rows[r]]
        for i in range(n):
            if i == r or rows[i][c] % q == 0:
                continue
            factor = rows[i][c] % q
            rows[i] = [(rows[i][j] - factor * rows[r][j]) % q for j in range(n + 1)]
        r += 1
    return [rows[i][-1] % q for i in range(n)]


def polynomial_degree(xs: list[int], ys: list[int], q: int) -> int:
    matrix: list[list[int]] = []
    for x in xs:
        row: list[int] = []
        power = 1
        for _ in xs:
            row.append(power)
            power = power * x % q
        matrix.append(row)
    coeffs = solve_square_mod_q(matrix, ys, q)
    for degree in range(len(coeffs) - 1, -1, -1):
        if coeffs[degree] % q:
            return degree
    return 0


def eval_poly(coeffs: list[int], x: int, q: int) -> int:
    total = 0
    power = 1
    for coeff in coeffs:
        total = (total + coeff * power) % q
        power = power * x % q
    return total


def rational_vector_valid(vec: list[int], xs: list[int], ys: list[int], q: int, degree: int) -> bool:
    num = [v % q for v in vec[: degree + 1]]
    den = [v % q for v in vec[degree + 1 :]]
    if all(v == 0 for v in den):
        return False
    for x, y in zip(xs, ys):
        den_value = eval_poly(den, x, q)
        if den_value == 0:
            return False
        if eval_poly(num, x, q) != y * den_value % q:
            return False
    return True


def rational_relation_matrix(xs: list[int], ys: list[int], q: int, degree: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for x, y in zip(xs, ys):
        row: list[int] = []
        power = 1
        for _ in range(degree + 1):
            row.append(power)
            power = power * x % q
        power = 1
        for _ in range(degree + 1):
            row.append((-y * power) % q)
            power = power * x % q
        matrix.append(row)
    return matrix


def has_rational_degree(
    xs: list[int],
    ys: list[int],
    q: int,
    degree: int,
    rng: random.Random,
    random_combos: int,
) -> bool:
    matrix = rational_relation_matrix(xs, ys, q, degree)
    vec = null_vector_mod_q(matrix, q)
    if vec is None:
        return False
    if rational_vector_valid(vec, xs, ys, q, degree):
        return True

    # The imported helper returns one null vector.  If it has a pole at a test
    # point, perturb the value vector deterministically by recomputing with
    # random row scalings.  This is not a proof of nonexistence, but it avoids
    # a common false negative in the diagnostic.
    for _ in range(random_combos):
        scaled: list[list[int]] = []
        for row in matrix:
            scale = rng.randrange(1, q)
            scaled.append([(scale * value) % q for value in row])
        candidate = null_vector_mod_q(scaled, q)
        if candidate is not None and rational_vector_valid(candidate, xs, ys, q, degree):
            return True
    return False


def first_low_rational_degree(
    xs: list[int],
    ys: list[int],
    q: int,
    limit: int,
    rng: random.Random,
    random_combos: int,
) -> int | None:
    for degree in range(limit + 1):
        if has_rational_degree(xs, ys, q, degree, rng, random_combos):
            return degree
    return None


def packet_norm(poly: sp.Poly, factor: sp.Poly, q: int) -> int:
    if poly.is_zero:
        return 0
    return int(sp.resultant(factor.as_expr(), poly.as_expr(), X)) % q


def scalar_norms_for_origins(
    cycle: list[int],
    q: int,
    m: int,
    factor: sp.Poly,
    scalar: str,
) -> list[int]:
    values: list[int] = []
    for shift in range(len(cycle)):
        shifted = rotate(cycle, shift)
        value = scalar_value(shifted, q, m, factor, scalar).rem(factor)
        values.append(packet_norm(value, factor, q))
    return values


def h_period_invariant(values: list[int], m: int) -> bool:
    h = len(values)
    n = h // m
    return all(values[r + m * k] == values[r] for r in range(m) for k in range(n))


def random_values_like(
    q: int,
    h: int,
    m: int,
    preserve_h_repetition: bool,
    rng: random.Random,
) -> list[int]:
    if not preserve_h_repetition:
        return [rng.randrange(q) for _ in range(h)]
    base = [rng.randrange(q) for _ in range(m)]
    return [base[i % m] for i in range(h)]


def audit_scalar(
    D: int,
    q: int,
    ell: int,
    cycle: list[int],
    m: int,
    factor: sp.Poly,
    scalar: str,
    max_rational_degree: int,
    random_trials: int,
    random_combos: int,
    rng: random.Random,
) -> InterpolationRow:
    h = len(cycle)
    n = h // m
    xs = [value % q for value in cycle]
    ys = scalar_norms_for_origins(cycle, q, m, factor, scalar)
    h_period_ok = h_period_invariant(ys, m)
    poly_degree = polynomial_degree(xs, ys, q)
    threshold = h // 2
    search_limit = min(max_rational_degree, max(0, threshold - 1))
    low_degree = first_low_rational_degree(xs, ys, q, search_limit, rng, random_combos)

    random_poly_degrees: list[int] = []
    random_low_hits = 0
    for _ in range(random_trials):
        random_ys = random_values_like(q, h, m, h_period_ok, rng)
        random_poly_degrees.append(polynomial_degree(xs, random_ys, q))
        if first_low_rational_degree(xs, random_ys, q, search_limit, rng, random_combos) is not None:
            random_low_hits += 1

    return InterpolationRow(
        scalar=scalar,
        D=D,
        q=q,
        ell=ell,
        h=h,
        m=m,
        n=n,
        n_is_prime=bool(sp.isprime(n)),
        factor_degree=factor.degree(),
        components=coprime_components(m),
        h_period_ok=h_period_ok,
        zero_norms=sum(value == 0 for value in ys),
        distinct_norms=len(set(ys)),
        polynomial_degree=poly_degree,
        random_poly_min=min(random_poly_degrees) if random_poly_degrees else -1,
        random_poly_max=max(random_poly_degrees) if random_poly_degrees else -1,
        rational_threshold=threshold,
        rational_search_limit=search_limit,
        first_low_rational_degree=low_degree,
        random_low_rational_hits=random_low_hits,
    )


def discriminants(max_abs_D: int, only_D: int | None) -> list[int]:
    if only_D is not None:
        return [only_D]
    return [-5000] + [
        D for D in range(-200, -max_abs_D - 1, -1)
        if D % 4 in (0, 1)
    ]


def scan(args: argparse.Namespace) -> list[InterpolationRow]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    rng = random.Random(args.seed)
    rows: list[InterpolationRow] = []
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
            for m in quotient_sizes:
                n = h // m
                for factor in packet_factors(n, q):
                    if factor.degree() == 1 and not args.include_linear:
                        continue
                    for scalar in ("M0", "L1"):
                        rows.append(
                            audit_scalar(
                                D,
                                q,
                                ell,
                                cycle,
                                m,
                                factor,
                                scalar,
                                args.max_rational_degree,
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-cases", type=int, default=12)
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
    parser.add_argument("--max-rational-degree", type=int, default=5)
    parser.add_argument("--random-trials", type=int, default=8)
    parser.add_argument("--random-combos", type=int, default=8)
    parser.add_argument("--max-rows", type=int, default=40)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    rows = scan(args)
    low_rows = [row for row in rows if row.first_low_rational_degree is not None]
    l1_rows = [row for row in rows if row.scalar == "L1"]
    m0_rows = [row for row in rows if row.scalar == "M0"]

    print("L1 selected-origin interpolation shape scan")
    print(f"max_cases={args.max_cases}")
    print(f"max_h={args.max_h}")
    print(f"max_abs_D={args.max_abs_D}")
    print(f"q_stop={args.q_stop}")
    print(f"include_linear={args.include_linear}")
    print(f"require_composite_m={args.require_composite_m}")
    print(f"max_rational_degree={args.max_rational_degree}")
    print(f"random_trials={args.random_trials}")
    print()
    if not args.summary_only:
        print(
            "columns: scalar D q ell h m n n_prime deg components zero_norms "
            "H_period_ok distinct_norms poly_degree random_poly_range rational_threshold "
            "search_limit first_low_rational random_low_hits"
        )
        for row in rows:
            print(
                f"scalar={row.scalar:2s} D={row.D:7d} q={row.q:6d} ell={row.ell:3d} "
                f"h={row.h:3d} m={row.m:3d} n={row.n:3d} "
                f"n_prime={int(row.n_is_prime)} deg={row.factor_degree:3d} "
                f"components={list(row.components)} zero_norms={row.zero_norms:3d} "
                f"H_period_ok={int(row.h_period_ok)} "
                f"distinct_norms={row.distinct_norms:3d} "
                f"poly_degree={row.polynomial_degree:3d} "
                f"random_poly_range=[{row.random_poly_min},{row.random_poly_max}] "
                f"rational_threshold={row.rational_threshold:3d} "
                f"search_limit={row.rational_search_limit:3d} "
                f"first_low_rational={row.first_low_rational_degree} "
                f"random_low_hits={row.random_low_rational_hits}/{args.random_trials}"
            )

    print()
    print("summary")
    print(f"  rows={len(rows)}")
    print(f"  m0_rows={len(m0_rows)}")
    print(f"  l1_rows={len(l1_rows)}")
    print(f"  rows_with_low_rational_degree={len(low_rows)}")
    print(f"  l1_rows_with_low_rational_degree={sum(row.first_low_rational_degree is not None for row in l1_rows)}")
    print(f"  l1_rows_with_H_period_ok={sum(row.h_period_ok for row in l1_rows)}")
    print(f"  l1_zero_norms={sum(row.zero_norms for row in l1_rows)}")
    print(f"  max_l1_poly_degree={max((row.polynomial_degree for row in l1_rows), default=-1)}")
    print()
    print("interpretation")
    print("  rational_threshold_is_generic_interpolation_degree_floor_h_over_2=1")
    print("  random_controls_preserve_H_repetition_when_present=1")
    print("  low_rational_degree_below_threshold_would_support_embedded_identity=1")
    print("  no_low_l1_relation_supports_selected_origin_obstruction=1")
    print("conclusion=reported_l1_interpolation_shape_scan")


if __name__ == "__main__":
    main()
