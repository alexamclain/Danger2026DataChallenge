#!/usr/bin/env python3
"""CM-vs-random support audit for marginal beta Plucker sequences.

This tests whether the low recurrence order of a small CM marginal beta
sequence is special or generic for the same top-coefficient/marginal
determinant.  The random controls replace the quotient-fiber elements
J_r(theta) by random elements of the same tensor factor B/E, then reuse the
same beta-shifted Top_k and CRT marginal determinant.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass

import sympy as sp

from k_character_tensor_factor_rank_scan import (
    equal_degree_factors,
    poly_mod,
    row_to_poly,
    sympy_factor_to_poly_e,
)
from k_character_tensor_rank_scan import (
    ExtensionField,
    find_irreducible_modulus,
)
from l1_axis_injectivity_scan import coeff_vector
from relative_moment_projection_scan import section_fiber_polynomials
from tensor_factor_beta_recurrence_audit import bm_connection, poly_divmod
from tensor_factor_crt_marginal_rank_audit import (
    component_marginals,
    vector_sub,
    vector_sum,
)
from tensor_factor_dual_basis_window_audit import (
    normal_subfield_basis,
    relative_basis_columns,
    relative_gprime_theta,
    theta_element,
    top_window_coords,
)
from tensor_factor_marginal_origin_action_audit import (
    determinant,
    find_case,
    target_components,
)
from tensor_factor_moore_audit import b_mul, b_one, b_pow
from tensor_factor_subfield_trace_audit import divisors
from tensor_factor_top_coefficient_fourier_audit import embedded_residue_vector


@dataclass(frozen=True)
class PreparedCase:
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
    windows: int
    field: ExtensionField
    selected_factor: list[tuple[int, ...]]
    relative_degree: int
    gprime_theta: list[tuple[int, ...]]
    basis_columns: list[list[tuple[int, ...]]]
    theta_inv_powers: list[list[tuple[int, ...]]]
    components: tuple[int, ...]
    include_constant: bool
    cm_values: list[list[tuple[int, ...]]]


def combined_rows(sequence, components: tuple[int, ...], include_constant: bool, field: ExtensionField):
    rows = []
    if include_constant:
        rows.append(vector_sum(sequence, field))
    for component in components:
        marginals = component_marginals(sequence, component, field)
        rows.extend(vector_sub(value, marginals[0], field) for value in marginals[1:])
    return rows


def period_polynomial(n: int, field: ExtensionField):
    poly = [field.zero for _ in range(n + 1)]
    poly[0] = field.neg(field.one)
    poly[n] = field.one
    return poly


def characteristic_polynomial_low_to_high(connection):
    return list(reversed(connection))


def characteristic_divides_period(connection, period: int, field: ExtensionField) -> bool:
    _, remainder = poly_divmod(
        period_polynomial(period, field),
        characteristic_polynomial_low_to_high(connection),
        field,
    )
    return remainder == [field.zero]


def prepare_case(args: argparse.Namespace) -> PreparedCase:
    case = find_case(args)
    if case is None:
        raise SystemExit("no eligible case found")
    D, q, ell, cycle, m, factor = case
    h = len(cycle)
    n = h // m
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(cycle, q, m, "complement")
    ]
    residue_vectors = [coeff_vector(residue, factor.degree(), q) for residue in residues]

    extension_degree = int(sp.n_order(q % m, m))
    modulus = find_irreducible_modulus(q, extension_degree, args.seed)
    field = ExtensionField(q, extension_degree, modulus)
    gcd_degree = int(sp.igcd(factor.degree(), extension_degree))
    tensor_factor_degree = factor.degree() // gcd_degree
    factors = equal_degree_factors(
        sympy_factor_to_poly_e(factor, field),
        tensor_factor_degree,
        field,
        args.seed,
    )
    selected_factor = factors[0]
    if args.subdegree not in divisors(tensor_factor_degree):
        raise ValueError("requested subdegree does not divide tensor factor degree")
    relative_degree = tensor_factor_degree // args.subdegree
    if args.windows > relative_degree:
        raise ValueError("requested windows exceed relative degree")

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
    cm_values = [
        poly_mod(row_to_poly(embedded_residue_vector(vector, field), field), selected_factor, field)
        for vector in residue_vectors
    ]

    theta = theta_element(field)
    theta_inv = b_pow(theta, n - 1, selected_factor, field)
    theta_inv_powers = [b_one(field)]
    for _ in range(1, n):
        theta_inv_powers.append(b_mul(theta_inv_powers[-1], theta_inv, selected_factor, field))

    return PreparedCase(
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
        windows=args.windows,
        field=field,
        selected_factor=selected_factor,
        relative_degree=relative_degree,
        gprime_theta=gprime_theta,
        basis_columns=basis_columns,
        theta_inv_powers=theta_inv_powers,
        components=target_components(m, args.target),
        include_constant=not args.without_constant,
        cm_values=cm_values,
    )


def beta_sequence(values, prepared: PreparedCase):
    out = []
    for beta in range(prepared.n):
        multiplier = prepared.theta_inv_powers[beta]
        sequence = []
        for value in values:
            shifted_value = b_mul(multiplier, value, prepared.selected_factor, prepared.field)
            sequence.append(
                top_window_coords(
                    shifted_value,
                    prepared.windows,
                    prepared.subdegree,
                    prepared.relative_degree,
                    prepared.gprime_theta,
                    prepared.basis_columns,
                    prepared.selected_factor,
                    prepared.field,
                )
            )
        rows = combined_rows(sequence, prepared.components, prepared.include_constant, prepared.field)
        if not rows or len(rows) != len(rows[0]):
            raise ValueError(
                f"target is not square: rows={len(rows)} coords={len(rows[0]) if rows else 0}"
            )
        out.append(determinant(rows, prepared.field))
    return out


def random_field_element(rng: random.Random, field: ExtensionField):
    return tuple(rng.randrange(field.q) for _ in range(field.degree))


def random_b_element(rng: random.Random, prepared: PreparedCase):
    return [
        random_field_element(rng, prepared.field)
        for _ in range(prepared.tensor_factor_degree)
    ]


def sequence_summary(sequence, prepared: PreparedCase):
    doubled = sequence * 2
    connection = bm_connection(doubled, prepared.field)
    order = len(connection) - 1
    return {
        "distinct": len(set(sequence)),
        "zeros": sum(1 for value in sequence if value == prepared.field.zero),
        "order": order,
        "divides": int(characteristic_divides_period(connection, prepared.n, prepared.field)),
    }


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
    parser.add_argument("--q-start", type=int, default=101)
    parser.add_argument("--q-stop", type=int, default=500000)
    parser.add_argument("--max-splitting-primes", type=int, default=1)
    parser.add_argument("--include-linear", action="store_true")
    parser.add_argument("--only-D", type=int)
    parser.add_argument("--only-m", type=int)
    parser.add_argument("--max-factor-degree", type=int, default=60)
    parser.add_argument("--max-extension-degree", type=int, default=12)
    parser.add_argument("--min-tensor-factor-count", type=int, default=2)
    parser.add_argument("--max-tensor-factor-degree", type=int, default=24)
    parser.add_argument("--subdegree", type=int, default=3)
    parser.add_argument("--windows", type=int, default=2)
    parser.add_argument("--target", default="full")
    parser.add_argument("--without-constant", action="store_true")
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    prepared = prepare_case(args)
    cm_sequence = beta_sequence(prepared.cm_values, prepared)
    cm_summary = sequence_summary(cm_sequence, prepared)

    rng = random.Random(args.seed + 99_991)
    random_orders = []
    random_distinct = []
    random_zero_trials = 0
    random_divides = 0
    for _ in range(args.random_trials):
        values = [random_b_element(rng, prepared) for _ in range(prepared.m)]
        seq = beta_sequence(values, prepared)
        summary = sequence_summary(seq, prepared)
        random_orders.append(summary["order"])
        random_distinct.append(summary["distinct"])
        random_zero_trials += int(summary["zeros"] > 0)
        random_divides += int(summary["divides"])

    print("tensor factor marginal CM-vs-random support audit")
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
    print(f"windows={prepared.windows}")
    print(f"components={prepared.components}")
    print(f"include_constant={int(prepared.include_constant)}")
    print(f"random_trials={args.random_trials}")
    print()
    print("cm_sequence")
    print(f"  distinct={cm_summary['distinct']}")
    print(f"  zero_count={cm_summary['zeros']}")
    print(f"  recurrence_order={cm_summary['order']}")
    print(f"  characteristic_divides_T^n_minus_1={cm_summary['divides']}")
    print()
    print("random_baseline")
    print(f"  order_min={min(random_orders) if random_orders else 'NA'}")
    print(f"  order_max={max(random_orders) if random_orders else 'NA'}")
    print(f"  order_avg={sum(random_orders)/len(random_orders) if random_orders else 0:.6f}")
    print(f"  order_hist={dict(sorted((value, random_orders.count(value)) for value in set(random_orders)))}")
    print(f"  distinct_min={min(random_distinct) if random_distinct else 'NA'}")
    print(f"  distinct_max={max(random_distinct) if random_distinct else 'NA'}")
    print(f"  trials_with_any_zero={random_zero_trials}")
    print(f"  characteristic_divides_count={random_divides}")
    print()
    print("interpretation")
    print("  cm_order_below_random_would_signal_cm_specific_support_collapse=1")
    print("  cm_order_matching_random_suggests_no_visible_support_collapse=1")
    print("conclusion=reported_tensor_factor_marginal_random_support_audit")


if __name__ == "__main__":
    main()
