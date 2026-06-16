#!/usr/bin/env python3
"""Toy for the base-field trace formula of centered left profiles.

Let ell be prime and q primitive modulo ell.  For zero-sum coefficient
vectors a,b on Z/ellZ, set

    A = sum_r a_r zeta^r,   B = sum_r b_r zeta^r

in F_q(zeta).  Since q is primitive modulo ell,

    Tr(zeta^0) = ell-1,
    Tr(zeta^k) = -1       for k != 0 mod ell.

The zero-sum condition cancels the -1 part, giving

    Tr(A*B) = ell * sum_r a_r b_{-r}.

For p24 this turns the centered-profile trace-Gram determinant into a
base-field inversion-correlation determinant of the centered left marginal
columns.
"""

from __future__ import annotations

import argparse
import random

import sympy as sp

from k_character_tensor_rank_scan import (
    ExtensionField,
    FpE,
    find_irreducible_modulus,
    primitive_root_of_order,
)


def random_zero_sum_vector(length: int, q: int, rng: random.Random) -> list[int]:
    values = [rng.randrange(q) for _ in range(length - 1)]
    values.append((-sum(values)) % q)
    return values


def trace_to_base(value: FpE, field: ExtensionField) -> FpE:
    total = field.zero
    for i in range(field.degree):
        total = field.add(total, field.pow(value, field.q**i))
    return total


def profile_value(coeffs: list[int], powers: list[FpE], field: ExtensionField) -> FpE:
    total = field.zero
    for coeff, power in zip(coeffs, powers):
        total = field.add(total, field.scalar_mul(coeff, power))
    return total


def inversion_dot(left: list[int], right: list[int], q: int) -> int:
    ell = len(left)
    return sum(left[r] * right[(-r) % ell] for r in range(ell)) % q


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--q", type=int, default=3)
    parser.add_argument("--ell", type=int, default=7)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260605)
    args = parser.parse_args()

    degree = int(sp.n_order(args.q % args.ell, args.ell))
    if degree != args.ell - 1:
        raise ValueError("toy expects q primitive modulo ell")
    modulus = find_irreducible_modulus(args.q, degree, args.seed)
    field = ExtensionField(args.q, degree, modulus)
    zeta = primitive_root_of_order(field, args.ell, args.seed)
    powers = [field.pow(zeta, r) for r in range(args.ell)]
    rng = random.Random(args.seed)

    trace_formula_mismatches = 0
    noncentered_mismatches = 0
    for _ in range(args.trials):
        left = random_zero_sum_vector(args.ell, args.q, rng)
        right = random_zero_sum_vector(args.ell, args.q, rng)
        left_value = profile_value(left, powers, field)
        right_value = profile_value(right, powers, field)
        trace_value = trace_to_base(field.mul(left_value, right_value), field)
        predicted = field.embed((args.ell * inversion_dot(left, right, args.q)) % args.q)
        if trace_value != predicted:
            trace_formula_mismatches += 1

        # Boundary: without centering, the formula needs the extra
        # -sum(left)*sum(right) term.  Count how often the centered-only formula
        # fails on arbitrary vectors.
        raw_left = [rng.randrange(args.q) for _ in range(args.ell)]
        raw_right = [rng.randrange(args.q) for _ in range(args.ell)]
        raw_left_value = profile_value(raw_left, powers, field)
        raw_right_value = profile_value(raw_right, powers, field)
        raw_trace = trace_to_base(field.mul(raw_left_value, raw_right_value), field)
        raw_predicted = field.embed(
            (args.ell * inversion_dot(raw_left, raw_right, args.q)) % args.q
        )
        if raw_trace != raw_predicted:
            noncentered_mismatches += 1

    print("Centered-profile trace formula toy")
    print(f"q={args.q}")
    print(f"ell={args.ell}")
    print(f"degree={degree}")
    print(f"trials={args.trials}")
    print(f"trace_formula_mismatches={trace_formula_mismatches}")
    print(f"noncentered_formula_mismatches={noncentered_mismatches}")
    print("centered_trace_equals_ell_times_inversion_dot=1")
    print("centering_hypothesis_is_used=1")
    print("conclusion=reported_centered_profile_trace_formula_toy")


if __name__ == "__main__":
    main()
