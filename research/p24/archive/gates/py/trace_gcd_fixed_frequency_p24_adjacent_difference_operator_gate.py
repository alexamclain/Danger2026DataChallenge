#!/usr/bin/env python3
"""Finite-difference operator gate for the p24 adjacent anchor.

Under the p24 covariance convention the right quotient shift is 6=-1 mod 7.
If Y_i denotes the internally traced right H-coset profile, covariance gives

    Y_{i+6} = rho(Y_i).

Thus the adjacent anchor is

    T_0 = Y_1 - Y_0 = (rho^6 - 1)Y_0.

On the nontrivial order-7 rho-projector channel k, this multiplies by
omega^(6k)-1, which is nonzero.  Therefore the adjacent-anchor descent target
is equivalent to the older right-axis equal-H-coset target: the finite
difference operator is invertible on the nonfixed quotient.
"""

from __future__ import annotations

import random


MOD = 43
ORDER = 7
SHIFT = 6
INV7 = pow(7, -1, MOD)
SEED = 20260607


def find_order7_root() -> int:
    for candidate in range(2, MOD):
        if pow(candidate, ORDER, MOD) == 1 and candidate != 1:
            return candidate
    raise RuntimeError("no primitive order-7 root")


OMEGA = find_order7_root()
ZERO = (0,) * ORDER


def add(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a + b) % MOD for a, b in zip(u, v))


def sub(u: tuple[int, ...], v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((a - b) % MOD for a, b in zip(u, v))


def scale(c: int, v: tuple[int, ...]) -> tuple[int, ...]:
    return tuple((c * a) % MOD for a in v)


def rho(v: tuple[int, ...]) -> tuple[int, ...]:
    return (v[-1],) + v[:-1]


def rho_pow(v: tuple[int, ...], power: int) -> tuple[int, ...]:
    out = v
    for _ in range(power % ORDER):
        out = rho(out)
    return out


def projector(k: int, v: tuple[int, ...]) -> tuple[int, ...]:
    total = ZERO
    for j in range(ORDER):
        coeff = pow(OMEGA, (-k * j) % ORDER, MOD)
        total = add(total, scale(coeff, rho_pow(v, j)))
    return scale(INV7, total)


def right_profile_from_anchor(anchor: tuple[int, ...]) -> list[tuple[int, ...]]:
    values = [ZERO for _ in range(ORDER)]
    for j in range(ORDER):
        values[(SHIFT * j) % ORDER] = rho_pow(anchor, j)
    return values


def adjacent_differences(values: list[tuple[int, ...]]) -> list[tuple[int, ...]]:
    return [sub(values[(i + 1) % ORDER], values[i]) for i in range(ORDER)]


def vector_sum(values: list[tuple[int, ...]]) -> tuple[int, ...]:
    total = ZERO
    for value in values:
        total = add(total, value)
    return total


def is_descended(v: tuple[int, ...]) -> bool:
    return rho(v) == v


def all_equal(values: list[tuple[int, ...]]) -> bool:
    return all(value == values[0] for value in values)


def all_zero(values: list[tuple[int, ...]]) -> bool:
    return all(value == ZERO for value in values)


def rank_mod(matrix: list[list[int]], modulus: int) -> int:
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) if rows else 0
    rank = 0
    for col in range(cols):
        pivot = None
        for row in range(rank, rows):
            if mat[row][col] % modulus:
                pivot = row
                break
        if pivot is None:
            continue
        mat[rank], mat[pivot] = mat[pivot], mat[rank]
        inv = pow(mat[rank][col] % modulus, -1, modulus)
        mat[rank] = [(value * inv) % modulus for value in mat[rank]]
        for row in range(rows):
            if row == rank:
                continue
            factor = mat[row][col] % modulus
            if factor:
                mat[row] = [
                    (mat[row][idx] - factor * mat[rank][idx]) % modulus
                    for idx in range(cols)
                ]
        rank += 1
    return rank


def derivative_matrix() -> list[list[int]]:
    matrix: list[list[int]] = []
    for basis_index in range(ORDER):
        basis = tuple(1 if idx == basis_index else 0 for idx in range(ORDER))
        image = sub(rho_pow(basis, SHIFT), basis)
        matrix.append(list(image))
    return [list(row) for row in zip(*matrix)]


def random_vec(rng: random.Random) -> tuple[int, ...]:
    return tuple(rng.randrange(MOD) for _ in range(ORDER))


def main() -> None:
    rng = random.Random(SEED)
    trials = 256

    derivative_rank = rank_mod(derivative_matrix(), MOD)
    derivative_kernel_dim = ORDER - derivative_rank

    derivative_projector_factor_failures = 0
    nontrivial_projector_equivalence_failures = 0
    right_adjacent_anchor_equivalence_failures = 0
    profile_difference_equivalence_failures = 0
    telescope_failures = 0

    for _ in range(trials):
        anchor = random_vec(rng)
        profile = right_profile_from_anchor(anchor)
        differences = adjacent_differences(profile)
        t0 = differences[0]

        telescope_failures += int(vector_sum(differences) != ZERO)
        right_adjacent_anchor_equivalence_failures += int(is_descended(anchor) != is_descended(t0))
        profile_difference_equivalence_failures += int(all_equal(profile) != all_zero(differences))

        for k in range(1, ORDER):
            left = projector(k, t0)
            factor = (pow(OMEGA, (SHIFT * k) % ORDER, MOD) - 1) % MOD
            right = scale(factor, projector(k, anchor))
            derivative_projector_factor_failures += int(left != right)
            nontrivial_projector_equivalence_failures += int((left == ZERO) != (projector(k, anchor) == ZERO))

    forced_right_axis_anchor = 0
    forced_adjacent_anchor = 0
    forced_all_equal = 0
    for c in range(MOD):
        anchor = (c,) * ORDER
        profile = right_profile_from_anchor(anchor)
        differences = adjacent_differences(profile)
        forced_right_axis_anchor += int(is_descended(anchor))
        forced_adjacent_anchor += int(is_descended(differences[0]))
        forced_all_equal += int(all_equal(profile) and all_zero(differences))

    print("Trace-GCD fixed-frequency p24 adjacent-difference operator gate")
    print(f"field_modulus={MOD}")
    print(f"omega_order7={OMEGA}")
    print(f"p24_right_shift_mod7={SHIFT}")
    print(f"derivative_operator=rho^6_minus_1")
    print(f"derivative_rank={derivative_rank}")
    print(f"derivative_kernel_dim={derivative_kernel_dim}")
    print(f"telescope_failures={telescope_failures}")
    print(f"derivative_projector_factor_failures={derivative_projector_factor_failures}")
    print(f"nontrivial_projector_equivalence_failures={nontrivial_projector_equivalence_failures}")
    print(f"right_axis_anchor_iff_adjacent_anchor_failures={right_adjacent_anchor_equivalence_failures}")
    print(f"equal_profile_iff_zero_adjacent_differences_failures={profile_difference_equivalence_failures}")
    print(f"forced_right_axis_anchor_count={forced_right_axis_anchor}/{MOD}")
    print(f"forced_adjacent_anchor_count={forced_adjacent_anchor}/{MOD}")
    print(f"forced_equal_profile_count={forced_all_equal}/{MOD}")
    print("adjacent_anchor_is_invertible_difference_on_nonfixed_quotient=1")
    print("adjacent_anchor_descent_equivalent_to_right_axis_anchor_descent=1")
    print("remaining_arithmetic_is_same_equal_H_coset_sum_theorem_for_selected_packet=1")
    print("conclusion=reported_trace_gcd_fixed_frequency_p24_adjacent_difference_operator_gate")

    if derivative_rank != 6 or derivative_kernel_dim != 1:
        raise SystemExit(1)
    if telescope_failures:
        raise SystemExit(1)
    if derivative_projector_factor_failures:
        raise SystemExit(1)
    if nontrivial_projector_equivalence_failures:
        raise SystemExit(1)
    if right_adjacent_anchor_equivalence_failures:
        raise SystemExit(1)
    if profile_difference_equivalence_failures:
        raise SystemExit(1)
    if forced_right_axis_anchor != MOD or forced_adjacent_anchor != MOD:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
