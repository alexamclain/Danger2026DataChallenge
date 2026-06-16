#!/usr/bin/env python3
"""Toy check for the linearized subspace-polynomial certificate.

After the Lang/trace-dual reductions, the p24 mixed Schur target is:

    210 elements w_i in L = F_p(mu_157) span L over F_p.

For any finite-field tuple, this is equivalent to saying that the monic
q-linearized annihilator polynomial of the F_q-span of the tuple has q-degree
equal to [L:F_q].  In the full-span case the annihilator is X^(q^L)-X.

This script verifies the finite-field identity on the same coprime-degree
mixed-DFT toy data used by the trace-dual scripts, and also includes a forced
low-rank control.  It is deliberately small: the value is the exact algebraic
certificate shape, not a large random-rank search.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass
from math import gcd

import sympy as sp

from hermitian_double_marginal_fourier_audit import dft_double_marginal, zeta_powers
from hermitian_mixed_dual_trace_injectivity_toy import transformed_coordinates
from hermitian_mixed_frobenius_orbit_audit import q_orbits
from hermitian_mixed_lang_normality_audit import fq_rank
from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


@dataclass(frozen=True)
class SubspaceTrial:
    trial: int
    left_orbit_rep: int
    left_orbit_len: int
    right_orbit_count: int
    right_orbit_len: int
    coordinate_count: int
    coordinate_rank: int
    annihilator_q_degree: int
    annihilator_vanish_failures: int
    degree_matches_rank: bool
    full_span: bool
    full_field_annihilator: bool
    forced_low_rank_degree: int
    forced_low_rank_expected: int


def random_base_table(left: int, right: int, q: int, rng: random.Random) -> list[list[int]]:
    return [[rng.randrange(q) for _ in range(right)] for _ in range(left)]


def qpoly_eval(coeffs: list[FpE], x: FpE, field: ExtensionField) -> FpE:
    total = field.zero
    q_power = 1
    for coeff in coeffs:
        total = field.add(total, field.mul(coeff, field.pow(x, q_power)))
        q_power *= field.q
    return total


def qpoly_extend_profile(
    coeffs: list[FpE],
    elements: list[FpE],
    field: ExtensionField,
) -> tuple[list[FpE], list[int], list[FpE]]:
    """Extend an annihilator by adjoining elements.

    The coefficient list represents sum_i coeffs[i] * X^(q^i).
    If the current polynomial annihilates U, adjoin a new independent value
    x by

        P_new(X) = P(X)^q - P(x)^(q-1) P(X).

    This is the standard subspace-polynomial update.
    """

    coeffs = coeffs[:]
    pivot_indices: list[int] = []
    residuals: list[FpE] = []
    for index, x in enumerate(elements):
        y = qpoly_eval(coeffs, x, field)
        if y == field.zero:
            continue
        pivot_indices.append(index)
        residuals.append(y)
        scale = field.pow(y, field.q - 1)
        new_coeffs = [field.zero for _ in range(len(coeffs) + 1)]
        for i, coeff in enumerate(coeffs):
            new_coeffs[i] = field.sub(new_coeffs[i], field.mul(scale, coeff))
            new_coeffs[i + 1] = field.add(new_coeffs[i + 1], field.pow(coeff, field.q))
        coeffs = new_coeffs
    return coeffs, pivot_indices, residuals


def qpoly_annihilator_profile(
    elements: list[FpE],
    field: ExtensionField,
) -> tuple[list[FpE], list[int], list[FpE]]:
    """Return annihilator plus pivot residuals for the F_q-span."""

    return qpoly_extend_profile([field.one], elements, field)


def qpoly_annihilator(elements: list[FpE], field: ExtensionField) -> list[FpE]:
    """Return the monic q-linearized annihilator of the F_q-span."""

    coeffs, _, _ = qpoly_annihilator_profile(elements, field)
    return coeffs


def relative_norm_to_base(value: FpE, degree: int, field: ExtensionField) -> FpE:
    total = field.one
    for i in range(degree):
        total = field.mul(total, field.pow(value, field.q**i))
    return total


def base_value_or_none(value: FpE, field: ExtensionField) -> int | None:
    if any(coord % field.q for coord in value[1:]):
        return None
    return value[0] % field.q


def q_degree(coeffs: list[FpE], field: ExtensionField) -> int:
    for i in range(len(coeffs) - 1, -1, -1):
        if coeffs[i] != field.zero:
            return i
    return -1


def full_field_annihilator(left_degree: int, coeffs: list[FpE], field: ExtensionField) -> bool:
    expected = [field.zero for _ in range(left_degree + 1)]
    expected[0] = field.scalar_mul(-1, field.one)
    expected[left_degree] = field.one
    return coeffs == expected


def audit_trial(
    trial: int,
    left: int,
    right: int,
    q: int,
    field: ExtensionField,
    zeta_pows,
    seed: int,
    rng: random.Random,
    force_dim: int,
) -> list[SubspaceTrial]:
    table = random_base_table(left, right, q, rng)
    dft_matrix = dft_double_marginal(table, left, right, zeta_pows, left * right, field)
    left_degree = int(sp.n_order(q % left, left))
    right_degree = int(sp.n_order(q % right, right))
    right_orbits = q_orbits(right, q)
    out: list[SubspaceTrial] = []
    for left_orbit in q_orbits(left, q):
        transformed = transformed_coordinates(
            dft_matrix,
            left,
            right,
            left_orbit,
            right_orbits,
            q,
            field,
            seed,
        )
        rank = fq_rank(transformed, q)
        ann = qpoly_annihilator(transformed, field)
        degree = q_degree(ann, field)
        vanish_failures = sum(1 for x in transformed if qpoly_eval(ann, x, field) != field.zero)

        forced_basis = transformed[: min(force_dim, len(transformed))]
        forced_elements: list[FpE] = []
        if forced_basis:
            for index, value in enumerate(transformed):
                coeff = (index + trial + 1) % q
                forced_elements.append(field.scalar_mul(coeff, forced_basis[index % len(forced_basis)]))
        else:
            forced_elements = transformed
        forced_rank = fq_rank(forced_elements, q)
        forced_ann = qpoly_annihilator(forced_elements, field)
        forced_degree = q_degree(forced_ann, field)

        out.append(
            SubspaceTrial(
                trial=trial,
                left_orbit_rep=left_orbit[0],
                left_orbit_len=len(left_orbit),
                right_orbit_count=len(right_orbits),
                right_orbit_len=right_degree,
                coordinate_count=len(transformed),
                coordinate_rank=rank,
                annihilator_q_degree=degree,
                annihilator_vanish_failures=vanish_failures,
                degree_matches_rank=(degree == rank),
                full_span=(rank >= len(left_orbit)),
                full_field_annihilator=full_field_annihilator(len(left_orbit), ann, field),
                forced_low_rank_degree=forced_degree,
                forced_low_rank_expected=forced_rank,
            )
        )
    return out


def format_trial(row: SubspaceTrial) -> str:
    return (
        f"trial={row.trial} left_rep={row.left_orbit_rep} "
        f"L={row.left_orbit_len} right_orbits={row.right_orbit_count} "
        f"R={row.right_orbit_len} coords={row.coordinate_count} "
        f"rank={row.coordinate_rank} ann_deg={row.annihilator_q_degree} "
        f"vanish_fail={row.annihilator_vanish_failures} "
        f"match={int(row.degree_matches_rank)} full={int(row.full_span)} "
        f"full_poly={int(row.full_field_annihilator)} "
        f"forced_deg={row.forced_low_rank_degree}/{row.forced_low_rank_expected}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=2)
    parser.add_argument("--left", type=int, default=7)
    parser.add_argument("--right", type=int, default=31)
    parser.add_argument("--trials", type=int, default=20)
    parser.add_argument("--seed", type=int, default=20260605)
    parser.add_argument("--force-dim", type=int, default=2)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()

    left_degree = int(sp.n_order(args.q % args.left, args.left))
    right_degree = int(sp.n_order(args.q % args.right, args.right))
    if gcd(left_degree, right_degree) != 1:
        raise ValueError("toy expects coprime left/right orbit degrees")
    extension_degree = int(sp.ilcm(left_degree, right_degree))
    modulus = find_irreducible_modulus(args.q, extension_degree, args.seed)
    field = ExtensionField(args.q, extension_degree, modulus)
    zeta = primitive_root_of_order(field, args.left * args.right, args.seed)
    powers = zeta_powers(zeta, args.left * args.right, field)
    rng = random.Random(args.seed)

    rows: list[SubspaceTrial] = []
    for trial in range(args.trials):
        rows.extend(
            audit_trial(
                trial,
                args.left,
                args.right,
                args.q,
                field,
                powers,
                args.seed,
                rng,
                args.force_dim,
            )
        )

    mismatches = [row for row in rows if not row.degree_matches_rank]
    vanish_failures = sum(row.annihilator_vanish_failures for row in rows)
    full_span = [row for row in rows if row.full_span]
    full_poly = [row for row in rows if row.full_field_annihilator]
    forced_mismatches = [
        row for row in rows if row.forced_low_rank_degree != row.forced_low_rank_expected
    ]

    print("Hermitian mixed subspace-polynomial toy")
    print(f"q={args.q}")
    print(f"left={args.left} ord_left={left_degree}")
    print(f"right={args.right} ord_right={right_degree}")
    print(f"right_orbits={(args.right - 1) // right_degree}")
    print(f"gcd_degrees={gcd(left_degree, right_degree)}")
    print(f"extension_degree={extension_degree}")
    print(f"trials={args.trials}")
    print(f"force_dim={args.force_dim}")
    print()
    if not args.summary_only:
        for row in rows[:80]:
            print(format_trial(row))
    print()
    print("summary")
    print(f"  subspace_tests={len(rows)}")
    print(f"  degree_rank_mismatches={len(mismatches)}")
    print(f"  vanish_failures={vanish_failures}")
    print(f"  full_span_tests={len(full_span)}")
    print(f"  full_field_annihilator_tests={len(full_poly)}")
    print(f"  forced_low_rank_degree_mismatches={len(forced_mismatches)}")
    if rows:
        print(f"  max_coordinate_rank={max(row.coordinate_rank for row in rows)}")
        print(f"  max_annihilator_q_degree={max(row.annihilator_q_degree for row in rows)}")
    print()
    print("interpretation")
    print("  annihilator_q_degree_equals_Fq_span_rank=1")
    print("  full_span_iff_annihilator_is_X_qL_minus_X=1")
    print("  p24_target_can_be_stated_as_no_q_annihilator_degree_lt_156=1")
    print("conclusion=reported_hermitian_mixed_subspace_polynomial_toy")


if __name__ == "__main__":
    main()
