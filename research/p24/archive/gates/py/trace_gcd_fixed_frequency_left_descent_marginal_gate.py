#!/usr/bin/env python3
"""Left-descent form of the fixed-frequency H-kernel theorem.

For an uncentered Hermitian double marginal M(a,b), the centered mixed block is

    C(a,b) = M(a,b) - M(a,0) - M(0,b) + M(0,0),
    a,b nonzero.

For a right H-coset Q, the row-wise H-kernel equation

    sum_{b in Q} C(a,b) = 0      for every nonzero a

is equivalent to left descent of the uncentered H-period leakage

    D_Q(a) = sum_{b in Q} M(a,b) - |Q| M(a,0):

    D_Q(a) = D_Q(0)              for every a.

So the p24 target `C P_H = 0` can be phrased geometrically: after subtracting
the right-zero baseline, each right H-period leakage must descend to the
left-constant component.  The pinned actual-CM marginal shows this is not a
generic Hermitian packet property.
"""

from __future__ import annotations

import random

from cypari2 import Pari

from cycle_period_complexity_scan import find_full_cycle_prime
from hermitian_double_marginal_audit import (
    centered_double_marginal,
    double_marginal,
    kernel_matrix,
)
from packetized_relative_content_scan import packet_factors
from relative_moment_projection_scan import (
    find_splitting_primes,
    rotate,
    section_fiber_polynomials,
)


PINNED_D = -13319
PINNED_Q = 13463
PINNED_M = 28
LEFT = 4
RIGHT = 7
RIGHT_PRIMITIVE = 3
QUOTIENT_ORDER = 2
FIELD_Q = 101
TRIALS = 24
SEED = 20260606


def log_table(modulus: int, generator: int) -> dict[int, int]:
    value = 1
    logs: dict[int, int] = {}
    for exponent in range(modulus - 1):
        logs[value] = exponent
        value = value * generator % modulus
    if len(logs) != modulus - 1:
        raise RuntimeError("bad primitive root")
    return logs


def h_cosets() -> list[list[int]]:
    logs = log_table(RIGHT, RIGHT_PRIMITIVE)
    return [
        sorted(
            [value for value in range(1, RIGHT) if logs[value] % QUOTIENT_ORDER == residue],
            key=logs.__getitem__,
        )
        for residue in range(QUOTIENT_ORDER)
    ]


def random_marginal(rng: random.Random, q: int = FIELD_Q) -> list[list[int]]:
    return [[rng.randrange(q) for _b in range(RIGHT)] for _a in range(LEFT)]


def centered_h_sums(
    marginal: list[list[int]],
    cosets: list[list[int]],
    q: int,
) -> list[list[int]]:
    centered = centered_double_marginal(marginal, q)
    return [
        [sum(row[b - 1] for b in coset) % q for coset in cosets]
        for row in centered
    ]


def left_descent_values(
    marginal: list[list[int]],
    cosets: list[list[int]],
    q: int,
) -> list[list[int]]:
    values: list[list[int]] = []
    for coset in cosets:
        row: list[int] = []
        for a in range(LEFT):
            row.append(
                (
                    sum(marginal[a][b] for b in coset)
                    - len(coset) * marginal[a][0]
                )
                % q
            )
        values.append(row)
    return values


def left_descent_failures(values: list[list[int]]) -> int:
    return sum(
        1
        for row in values
        for value in row[1:]
        if value != row[0]
    )


def equivalence_failures(
    marginal: list[list[int]],
    cosets: list[list[int]],
    q: int,
) -> int:
    sums = centered_h_sums(marginal, cosets, q)
    values = left_descent_values(marginal, cosets, q)
    failures = 0
    for coset_index in range(len(cosets)):
        for a in range(1, LEFT):
            centered_zero = sums[a - 1][coset_index] == 0
            descended = values[coset_index][a] == values[coset_index][0]
            failures += int(centered_zero != descended)
    return failures


def force_left_descent(
    marginal: list[list[int]],
    cosets: list[list[int]],
    q: int,
) -> list[list[int]]:
    adjusted = [row[:] for row in marginal]
    values = left_descent_values(adjusted, cosets, q)
    for coset_index, coset in enumerate(cosets):
        pivot = coset[0]
        for a in range(1, LEFT):
            diff = (values[coset_index][a] - values[coset_index][0]) % q
            adjusted[a][pivot] = (adjusted[a][pivot] - diff) % q
    return adjusted


def load_actual_marginal() -> tuple[int, int, int, int, int, int, list[list[int]]]:
    pari = Pari()
    pari.allocatemem(256 * 1024 * 1024)
    hilbert = pari.polclass(PINNED_D)
    h = int(pari.poldegree(hilbert))
    splits = find_splitting_primes(
        pari,
        hilbert,
        h,
        PINNED_Q,
        PINNED_Q + 1,
        1,
    )
    if not splits:
        raise RuntimeError("pinned split prime not found")
    q, roots = splits[0]
    full = find_full_cycle_prime(roots, PINNED_D, q)
    if full is None:
        raise RuntimeError("pinned full cycle not found")
    ell, cycle = full
    shifted = rotate(cycle, 0)
    n = h // PINNED_M
    factors = [factor for factor in packet_factors(n, q) if factor.degree() == 4]
    if not factors:
        raise RuntimeError("pinned degree-4 packet factor not found")
    factor = factors[0]
    residues = [
        fiber.rem(factor)
        for fiber in section_fiber_polynomials(shifted, q, PINNED_M, "complement")
    ]
    kernel = kernel_matrix(residues, factor, q)
    marginal = double_marginal(kernel, LEFT, RIGHT, q)
    return q, ell, h, PINNED_M, n, factor.degree(), marginal


def all_zero(matrix: list[list[int]]) -> bool:
    return all(value == 0 for row in matrix for value in row)


def main() -> None:
    cosets = h_cosets()
    rng = random.Random(SEED)
    random_equivalence_failures = 0
    random_left_descent_passes = 0
    forced_left_descent_passes = 0
    forced_centered_h_zeroes = 0

    for _trial in range(TRIALS):
        marginal = random_marginal(rng)
        random_equivalence_failures += equivalence_failures(marginal, cosets, FIELD_Q)
        random_left_descent_passes += int(
            left_descent_failures(left_descent_values(marginal, cosets, FIELD_Q)) == 0
        )
        forced = force_left_descent(marginal, cosets, FIELD_Q)
        forced_left_descent_passes += int(
            left_descent_failures(left_descent_values(forced, cosets, FIELD_Q)) == 0
        )
        forced_centered_h_zeroes += int(all_zero(centered_h_sums(forced, cosets, FIELD_Q)))

    actual_q, ell, h, m, n, factor_degree, actual_marginal = load_actual_marginal()
    actual_sums = centered_h_sums(actual_marginal, cosets, actual_q)
    actual_values = left_descent_values(actual_marginal, cosets, actual_q)
    actual_equivalence_failures = equivalence_failures(actual_marginal, cosets, actual_q)
    actual_centered_zeroes = sum(value == 0 for row in actual_sums for value in row)
    actual_left_descent_failures = left_descent_failures(actual_values)

    print("Trace-GCD fixed-frequency left-descent marginal gate")
    print("finite_formula")
    print(f"  field_q={FIELD_Q}")
    print(f"  left={LEFT}")
    print(f"  right={RIGHT}")
    print(f"  quotient_order={QUOTIENT_ORDER}")
    print(f"  right_H_cosets={cosets}")
    print(f"  random_equivalence_failures={random_equivalence_failures}")
    print(f"  random_left_descent_passes={random_left_descent_passes}/{TRIALS}")
    print(f"  forced_left_descent_passes={forced_left_descent_passes}/{TRIALS}")
    print(f"  forced_centered_H_kernel_passes={forced_centered_h_zeroes}/{TRIALS}")
    print("pinned_actual_cm_row")
    print(f"  D={PINNED_D}")
    print(f"  q={actual_q}")
    print(f"  ell={ell}")
    print(f"  h={h}")
    print(f"  m={m}")
    print(f"  n={n}")
    print(f"  factor_degree={factor_degree}")
    print(f"  actual_centered_H_sum_zeroes={actual_centered_zeroes}/{(LEFT - 1) * len(cosets)}")
    print(f"  actual_left_descent_failures={actual_left_descent_failures}/{(LEFT - 1) * len(cosets)}")
    print(f"  actual_equivalence_failures={actual_equivalence_failures}")
    print(f"  actual_centered_H_sums={actual_sums}")
    print(f"  actual_left_descent_values={actual_values}")
    print("interpretation")
    print("  centered_H_kernel_equiv_left_descent_of_period_leakage=1")
    print("  left_descent_is_geometric_form_of_CPH_zero=1")
    print("  actual_cm_marginal_refutes_generic_left_descent=1")
    print("  p24_must_prove_left_descent_for_trace_gcd_weighted_packet=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_left_descent_marginal_gate")

    if random_equivalence_failures:
        raise SystemExit(1)
    if forced_left_descent_passes != TRIALS or forced_centered_h_zeroes != TRIALS:
        raise SystemExit(1)
    if (actual_q, h, m, n, factor_degree) != (PINNED_Q, 140, PINNED_M, 5, 4):
        raise SystemExit(1)
    if actual_equivalence_failures:
        raise SystemExit(1)
    if actual_centered_zeroes != 0 or actual_left_descent_failures != (LEFT - 1) * len(cosets):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
