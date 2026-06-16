#!/usr/bin/env python3
"""Cyclic-resultant audit for trace-frame beta products.

For a fixed alpha, the beta shifts give a sequence

    D_beta = D(theta^(-beta)),       beta mod n,

where `D` is either the full leading trace-frame determinant or the
residual-tail determinant.  A product over beta can always be written as a
cyclic resultant after interpolation:

    prod_beta D_beta
      = det(mul_by_f on B[Y]/(Y^n - 1)),

where `f(theta^(-beta)) = D_beta`.

This script checks that identity in small CM tensor rows and measures whether
the interpolating polynomial has any exploitable sparsity or subfield descent.
It is a theorem-shaping audit: the p24 goal would be to construct `f` from the
class-field/tower data and prove the cyclic resultant is a p-unit without
enumerating all beta values.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass

import sympy as sp
from cypari2 import Pari

from crt_partial_moment_projection_scan import coprime_components
from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_mixed_subspace_polynomial_toy import (
    base_value_or_none,
    relative_norm_to_base,
)
from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    sympy_factor_to_poly_e,
    trim,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import discriminants
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    quotient_sizes_any,
)
from tensor_factor_dual_basis_window_audit import theta_element
from tensor_factor_moore_audit import (
    b_add,
    b_inv,
    b_is_zero,
    b_mul,
    b_one,
    b_pow,
    b_sub,
)
from tensor_factor_subfield_trace_audit import divisors, element_rank
from trace_frame_residual_tail_origin_action_audit import (
    OriginTailRow,
    rows_for_case,
)


PolyB = list[FpE]


@dataclass(frozen=True)
class ResultantRow:
    D: int
    q: int
    ell: int
    h: int
    m: int
    n: int
    factor_degree: int
    extension_degree: int
    tensor_factor_degree: int
    target: str
    subdegree: int
    determinant_kind: str
    raw_rank: int
    top_count: int
    residual_dim: int
    beta_values: int
    beta_distinct: int
    beta_zero_count: int
    product_base_norm: int | None
    interp_support: int
    interp_e_coefficients: int
    interp_subfield_histogram: tuple[tuple[int, int], ...]
    coefficient_orbit_count: int
    coefficient_orbit_support: int
    coefficient_orbit_length_histogram: tuple[tuple[int, int], ...]
    coefficient_semilinear_failures: int
    trace_reconstruction_failures: int
    seed_rank_histogram: tuple[tuple[int, int], ...]
    nonzero_seed_normal_count: int
    value_orbit_constant_count: int
    beta_orbit_count: int
    beta_orbit_length_histogram: tuple[tuple[int, int], ...]
    beta_orbit_zero_products: int
    beta_orbit_product_norm_distinct: int
    cyclic_resultant_matches_product: bool
    resultant_lands_in_E: bool
    resultant_zero: bool


def b_embed(value: FpE) -> PolyB:
    return [value]


def b_equal(left: PolyB, right: PolyB, field: ExtensionField) -> bool:
    return trim(left, field) == trim(right, field)


def b_det(matrix: list[list[PolyB]], modulus: PolyB, field: ExtensionField) -> PolyB:
    size = len(matrix)
    if any(len(row) != size for row in matrix):
        raise ValueError("square B-matrix expected")
    mat = [
        [trim(entry, field) for entry in row]
        for row in matrix
    ]
    det = b_one(field)
    for col in range(size):
        pivot = None
        for row in range(col, size):
            if not b_is_zero(mat[row][col], field):
                pivot = row
                break
        if pivot is None:
            return [field.zero]
        if pivot != col:
            mat[col], mat[pivot] = mat[pivot], mat[col]
            det = b_sub([field.zero], det, modulus, field)
        pivot_value = mat[col][col]
        det = b_mul(det, pivot_value, modulus, field)
        inv = b_inv(pivot_value, modulus, field)
        for row in range(col + 1, size):
            scale = mat[row][col]
            if b_is_zero(scale, field):
                continue
            factor = b_mul(scale, inv, modulus, field)
            mat[row] = [
                b_sub(left, b_mul(factor, right, modulus, field), modulus, field)
                for left, right in zip(mat[row], mat[col])
            ]
    return trim(det, field)


def b_product(values: list[PolyB], modulus: PolyB, field: ExtensionField) -> PolyB:
    out = b_one(field)
    for value in values:
        out = b_mul(out, value, modulus, field)
    return out


def e_product(values: list[FpE], field: ExtensionField) -> FpE:
    out = field.one
    for value in values:
        out = field.mul(out, value)
    return out


def norm_base(value: FpE, field: ExtensionField) -> int | None:
    return base_value_or_none(relative_norm_to_base(value, field.degree, field), field)


def beta_orbits(n: int, multiplier: int) -> list[list[int]]:
    seen: set[int] = set()
    orbits: list[list[int]] = []
    for start in range(n):
        if start in seen:
            continue
        orbit: list[int] = []
        value = start
        while value not in seen:
            seen.add(value)
            orbit.append(value)
            value = (value * multiplier) % n
        orbits.append(orbit)
    return orbits


def coefficient_semilinear_failures(
    coeffs: list[PolyB],
    multiplier: int,
    modulus: PolyB,
    field: ExtensionField,
) -> int:
    """Check f(Y) = sigma(f)(Y^multiplier).

    If f(root^beta) lies in E for every beta, with root^multiplier equal to
    the E-Frobenius of root, uniqueness of interpolation forces

        c_l = c_{l / multiplier}^{Q}

    where Q=|E|.
    """

    n = len(coeffs)
    inv_multiplier = pow(multiplier, -1, n)
    Q = field.q ** field.degree
    failures = 0
    for index, coeff in enumerate(coeffs):
        previous = (index * inv_multiplier) % n
        expected = b_pow(coeffs[previous], Q, modulus, field)
        if not b_equal(coeff, expected, field):
            failures += 1
    return failures


def orbit_trace(value: PolyB, orbit_length: int, modulus: PolyB, field: ExtensionField) -> PolyB:
    Q = field.q ** field.degree
    total = [field.zero]
    current = value
    for _ in range(orbit_length):
        total = b_add(total, current, modulus, field)
        current = b_pow(current, Q, modulus, field)
    return trim(total, field)


def seed_rank(seed: PolyB, factor_degree: int, modulus: PolyB, field: ExtensionField) -> int:
    if b_is_zero(seed, field):
        return 0
    Q = field.q ** field.degree
    conjugates = [
        b_pow(seed, Q**i, modulus, field)
        for i in range(factor_degree)
    ]
    return element_rank(conjugates, modulus, field)


def trace_reconstruction_failures(
    values: list[FpE],
    coeffs: list[PolyB],
    coefficient_orbits: list[list[int]],
    theta_inv: PolyB,
    factor_degree: int,
    modulus: PolyB,
    field: ExtensionField,
) -> int:
    failures = 0
    n = len(values)
    theta_inv_powers = [b_one(field)]
    for _ in range(1, n):
        theta_inv_powers.append(
            b_mul(theta_inv_powers[-1], theta_inv, modulus, field)
        )
    for beta, expected in enumerate(values):
        total = [field.zero]
        for orbit in coefficient_orbits:
            rep = orbit[0]
            seed = coeffs[rep]
            if b_is_zero(seed, field):
                continue
            argument = b_mul(
                seed,
                b_pow(theta_inv_powers[beta], rep, modulus, field),
                modulus,
                field,
            )
            total = b_add(
                total,
                orbit_trace(argument, len(orbit), modulus, field),
                modulus,
                field,
            )
        if not b_equal(total, b_embed(expected), field):
            failures += 1
    return failures


def cyclic_interpolation_coeffs(
    values: list[FpE],
    root: PolyB,
    root_inv: PolyB,
    modulus: PolyB,
    field: ExtensionField,
) -> list[PolyB]:
    """Return f coefficients with f(root^beta)=values[beta]."""

    n = len(values)
    inv_n = field.inv(field.embed(n % field.q))
    coeffs: list[PolyB] = []
    root_inv_powers = [b_one(field)]
    for _ in range(1, n):
        root_inv_powers.append(
            b_mul(root_inv_powers[-1], root_inv, modulus, field)
        )
    for j in range(n):
        total = [field.zero]
        step = root_inv_powers[j]
        power = b_one(field)
        for value in values:
            total = b_add(
                total,
                b_mul(b_embed(value), power, modulus, field),
                modulus,
                field,
            )
            power = b_mul(power, step, modulus, field)
        coeffs.append(b_mul(b_embed(inv_n), total, modulus, field))

    # Sanity check at the same points.
    root_powers = [b_one(field)]
    for _ in range(1, n):
        root_powers.append(b_mul(root_powers[-1], root, modulus, field))
    for beta, point in enumerate(root_powers):
        total = [field.zero]
        power = b_one(field)
        for coeff in coeffs:
            total = b_add(total, b_mul(coeff, power, modulus, field), modulus, field)
            power = b_mul(power, point, modulus, field)
        if not b_equal(total, b_embed(values[beta]), field):
            raise AssertionError("cyclic interpolation failed")
    return coeffs


def cyclic_resultant(coeffs: list[PolyB], modulus: PolyB, field: ExtensionField) -> PolyB:
    n = len(coeffs)
    matrix: list[list[PolyB]] = []
    for row in range(n):
        matrix_row: list[PolyB] = []
        for col in range(n):
            matrix_row.append(coeffs[(row - col) % n])
        matrix.append(matrix_row)
    return b_det(matrix, modulus, field)


def b_lands_in_E(value: PolyB, field: ExtensionField) -> bool:
    value = trim(value, field)
    return len(value) == 1


def b_subfield_degree(value: PolyB, factor_degree: int, modulus: PolyB, field: ExtensionField) -> int:
    if b_is_zero(value, field):
        return 0
    Q = field.q ** field.degree
    for degree in divisors(factor_degree):
        if b_equal(b_pow(value, Q**degree, modulus, field), value, field):
            return degree
    return factor_degree


def summarize_sequence(
    group_rows: list[OriginTailRow],
    selected_factor: PolyB,
    factor_degree: int,
    field: ExtensionField,
    determinant_kind: str,
) -> ResultantRow:
    n = group_rows[0].n
    by_beta: dict[int, FpE] = {}
    for row in group_rows:
        if row.alpha != 0:
            continue
        value = row.full_det if determinant_kind == "full" else row.tail_det
        if value is None:
            continue
        by_beta[row.beta] = value
    if len(by_beta) != n:
        raise RuntimeError(
            f"expected {n} beta values for {determinant_kind}, got {len(by_beta)}"
        )
    values = [by_beta[beta] for beta in range(n)]
    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    coeffs = cyclic_interpolation_coeffs(
        values,
        theta_inv,
        theta,
        selected_factor,
        field,
    )
    direct_product_e = e_product(values, field)
    direct_product_b = b_embed(direct_product_e)
    resultant = cyclic_resultant(coeffs, selected_factor, field)

    support = sum(1 for coeff in coeffs if not b_is_zero(coeff, field))
    e_coeffs = sum(1 for coeff in coeffs if b_lands_in_E(coeff, field))
    subfield_hist = Counter(
        b_subfield_degree(coeff, factor_degree, selected_factor, field)
        for coeff in coeffs
        if not b_is_zero(coeff, field)
    )
    Q_mod_n = pow(field.q, field.degree, n)
    orbits = beta_orbits(n, Q_mod_n)
    coefficient_orbits = beta_orbits(n, Q_mod_n)
    orbit_products = [
        e_product([values[beta] for beta in orbit], field)
        for orbit in orbits
    ]
    orbit_norms = [norm_base(value, field) for value in orbit_products]
    orbit_length_hist = Counter(len(orbit) for orbit in orbits)
    coefficient_orbit_length_hist = Counter(len(orbit) for orbit in coefficient_orbits)
    coefficient_orbit_support = sum(
        1 for orbit in coefficient_orbits
        if not b_is_zero(coeffs[orbit[0]], field)
    )
    seed_ranks = [
        seed_rank(coeffs[orbit[0]], factor_degree, selected_factor, field)
        for orbit in coefficient_orbits
        if not b_is_zero(coeffs[orbit[0]], field)
    ]
    seed_rank_hist = Counter(seed_ranks)
    value_orbit_constant_count = sum(
        1 for orbit in orbits
        if len({values[beta] for beta in orbit}) == 1
    )

    first = group_rows[0]
    return ResultantRow(
        D=first.D,
        q=first.q,
        ell=first.ell,
        h=first.h,
        m=first.m,
        n=first.n,
        factor_degree=first.factor_degree,
        extension_degree=first.extension_degree,
        tensor_factor_degree=first.tensor_factor_degree,
        target=first.target,
        subdegree=first.subdegree,
        determinant_kind=determinant_kind,
        raw_rank=first.raw_rank,
        top_count=first.top_count,
        residual_dim=first.residual_dim,
        beta_values=len(values),
        beta_distinct=len(set(values)),
        beta_zero_count=sum(1 for value in values if value == field.zero),
        product_base_norm=norm_base(direct_product_e, field),
        interp_support=support,
        interp_e_coefficients=e_coeffs,
        interp_subfield_histogram=tuple(sorted(subfield_hist.items())),
        coefficient_orbit_count=len(coefficient_orbits),
        coefficient_orbit_support=coefficient_orbit_support,
        coefficient_orbit_length_histogram=tuple(sorted(coefficient_orbit_length_hist.items())),
        coefficient_semilinear_failures=coefficient_semilinear_failures(
            coeffs,
            Q_mod_n,
            selected_factor,
            field,
        ),
        trace_reconstruction_failures=trace_reconstruction_failures(
            values,
            coeffs,
            coefficient_orbits,
            theta_inv,
            factor_degree,
            selected_factor,
            field,
        ),
        seed_rank_histogram=tuple(sorted(seed_rank_hist.items())),
        nonzero_seed_normal_count=sum(1 for rank in seed_ranks if rank == factor_degree),
        value_orbit_constant_count=value_orbit_constant_count,
        beta_orbit_count=len(orbits),
        beta_orbit_length_histogram=tuple(sorted(orbit_length_hist.items())),
        beta_orbit_zero_products=sum(1 for value in orbit_products if value == field.zero),
        beta_orbit_product_norm_distinct=len(set(value for value in orbit_norms if value is not None)),
        cyclic_resultant_matches_product=b_equal(resultant, direct_product_b, field),
        resultant_lands_in_E=b_lands_in_E(resultant, field),
        resultant_zero=b_is_zero(resultant, field),
    )


def find_case(args: argparse.Namespace):
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
        if args.require_composite_m:
            quotient_sizes = [
                m for m in quotient_sizes
                if len(coprime_components(m)) >= 2
            ]
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
                    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
                    if gcd_degree < args.min_tensor_factor_count:
                        continue
                    tensor_factor_degree = factor.degree() // gcd_degree
                    if tensor_factor_degree > args.max_tensor_factor_degree:
                        continue
                    if len(divisors(tensor_factor_degree)) <= 2:
                        continue
                    return D, q, ell, cycle, m, factor
        cases += 1
        if cases >= args.max_cases:
            break
    return None


def audit(args: argparse.Namespace) -> list[ResultantRow]:
    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    tensor_factor_degree = factor.degree() // int(sp.igcd(factor.degree(), extension_degree))
    selected_factor = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        args.seed,
    )[0]

    rows = rows_for_case(
        D,
        q,
        ell,
        cycle,
        m,
        factor,
        args.target or ["axis"],
        args.seed,
        args.max_top_count,
    )
    groups: dict[tuple[str, int], list[OriginTailRow]] = defaultdict(list)
    for row in rows:
        groups[(row.target, row.subdegree)].append(row)

    out: list[ResultantRow] = []
    for group in groups.values():
        out.append(
            summarize_sequence(
                group,
                selected_factor,
                tensor_factor_degree,
                field,
                "full",
            )
        )
        if all(row.tail_det is not None for row in group):
            out.append(
                summarize_sequence(
                    group,
                    selected_factor,
                    tensor_factor_degree,
                    field,
                    "tail",
                )
            )
    return out


def fmt_hist(hist: tuple[tuple[int, int], ...]) -> str:
    return "[" + ",".join(f"{degree}:{count}" for degree, count in hist) + "]"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-abs-D", type=int, default=20000)
    ap.add_argument("--only-D", type=int, default=None)
    ap.add_argument("--min-h", type=int, default=1)
    ap.add_argument("--max-h", type=int, default=240)
    ap.add_argument("--min-n", type=int, default=2)
    ap.add_argument("--max-n", type=int, default=240)
    ap.add_argument("--max-m", type=int, default=48)
    ap.add_argument("--only-m", type=int, default=None)
    ap.add_argument("--q-start", type=int, default=101)
    ap.add_argument("--q-stop", type=int, default=20000)
    ap.add_argument("--max-splitting-primes", type=int, default=1)
    ap.add_argument("--max-prime-quotients", type=int, default=48)
    ap.add_argument("--max-composite-quotients", type=int, default=48)
    ap.add_argument("--max-factor-degree", type=int, default=24)
    ap.add_argument("--max-extension-degree", type=int, default=8)
    ap.add_argument("--max-tensor-factor-degree", type=int, default=14)
    ap.add_argument("--min-tensor-factor-count", type=int, default=1)
    ap.add_argument("--max-top-count", type=int, default=4)
    ap.add_argument("--max-cases", type=int, default=4)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--include-linear", action="store_true")
    ap.add_argument("--require-composite-m", action="store_true")
    ap.add_argument(
        "--target",
        action="append",
        help="Target such as axis, constant_plus_4, constant_plus_3.",
    )
    args = ap.parse_args()

    rows = audit(args)
    print("trace-frame beta-product cyclic-resultant audit")
    print(f"rows={len(rows)}")
    print("cyclic_resultant_is_det_mul_by_interpolant_in_B_Y_mod_Yn_minus_1=1")
    print()
    print(
        "columns: D q ell h m n target subdeg kind raw top residual_dim "
        "beta distinct zeros product_norm support E_coeffs subfield_hist "
        "coeff_orbits coeff_orbit_support coeff_orbit_lengths "
        "coeff_semilin_fail trace_recon_fail seed_rank_hist normal_seeds "
        "value_orbit_constants "
        "orbit_count orbit_lengths orbit_zero_products orbit_norm_distinct "
        "resultant_match resultant_in_E resultant_zero"
    )
    for row in rows:
        print(
            f"D={row.D} q={row.q} ell={row.ell} h={row.h} m={row.m} n={row.n} "
            f"target={row.target} subdeg={row.subdegree} kind={row.determinant_kind} "
            f"raw={row.raw_rank} top={row.top_count} residual_dim={row.residual_dim} "
            f"beta={row.beta_values} distinct={row.beta_distinct} "
            f"zeros={row.beta_zero_count} "
            f"product_norm={row.product_base_norm if row.product_base_norm is not None else 'NA'} "
            f"support={row.interp_support} E_coeffs={row.interp_e_coefficients} "
            f"subfield_hist={fmt_hist(row.interp_subfield_histogram)} "
            f"coeff_orbits={row.coefficient_orbit_count} "
            f"coeff_orbit_support={row.coefficient_orbit_support} "
            f"coeff_orbit_lengths={fmt_hist(row.coefficient_orbit_length_histogram)} "
            f"coeff_semilin_fail={row.coefficient_semilinear_failures} "
            f"trace_recon_fail={row.trace_reconstruction_failures} "
            f"seed_rank_hist={fmt_hist(row.seed_rank_histogram)} "
            f"normal_seeds={row.nonzero_seed_normal_count} "
            f"value_orbit_constants={row.value_orbit_constant_count} "
            f"orbit_count={row.beta_orbit_count} "
            f"orbit_lengths={fmt_hist(row.beta_orbit_length_histogram)} "
            f"orbit_zero_products={row.beta_orbit_zero_products} "
            f"orbit_norm_distinct={row.beta_orbit_product_norm_distinct} "
            f"resultant_match={int(row.cyclic_resultant_matches_product)} "
            f"resultant_in_E={int(row.resultant_lands_in_E)} "
            f"resultant_zero={int(row.resultant_zero)}"
        )
    print()
    print("interpretation")
    print("  support_equal_n_means_no_sparse_beta_interpolant_in_this_frame=1")
    print("  E_coeffs_less_than_n_means_interpolant_does_not_descend_to_E[Y]=1")
    print("  zero_coeff_semilin_failures_means_interpolant_is_Frobenius_twisted=1")
    print("  zero_trace_recon_failures_means_beta_values_are_trace_sums_from_orbit_seeds=1")
    print("  normal_seed_count_shows_whether_orbit_seeds_escape_proper_subfields=1")
    print("  value_orbit_constants_less_than_orbits_rules_out_ordinary_E_norm=1")
    print("  orbit_factors_are_the_degree_ord_n_Q_resultant_pieces=1")
    print("  cyclic_resultant_match_is_the_exact_product_packaging_gate=1")
    print("conclusion=reported_trace_frame_beta_product_resultant_audit")


if __name__ == "__main__":
    main()
