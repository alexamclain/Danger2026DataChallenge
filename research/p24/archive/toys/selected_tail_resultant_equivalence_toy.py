#!/usr/bin/env python3
"""Toy verifier for the selected-tail linearized-resultant reduction.

The p24 proof target is:

    U cap T = {0}

where T is the normal-basis tail in C/E and U is the residual image
b_28(K_2).  This script checks the finite-field equivalences in small
GF(2^m) models with an actual normal basis:

* U cap T = {0};
* the normal-head coordinate matrix of U has full rank;
* the Moore determinant of the head projection P_H(U) is nonzero;
* the Moore determinant of the tail-annihilator image A_T(U) is nonzero;
* the common-kernel zero test for A_U and A_T is trivial.

It does not model the CM construction of U.  Its purpose is to keep the
linearized-resultant handoff honest before attacking the arithmetic p-unit.
"""

from __future__ import annotations

import argparse
import random
from dataclasses import dataclass


PRIMITIVE_POLYS = {
    2: 0b111,
    3: 0b1011,
    4: 0b10011,
    5: 0b100101,
    6: 0b1000011,
    7: 0b10000011,
    8: 0b100011101,
}


@dataclass(frozen=True)
class GF2m:
    m: int
    modulus: int

    @property
    def mask(self) -> int:
        return (1 << self.m) - 1

    def reduce(self, value: int) -> int:
        while value.bit_length() > self.m:
            shift = value.bit_length() - self.m - 1
            value ^= self.modulus << shift
        return value & self.mask

    def mul(self, left: int, right: int) -> int:
        out = 0
        a = left
        b = right
        while b:
            if b & 1:
                out ^= a
            a <<= 1
            b >>= 1
        return self.reduce(out)

    def pow(self, value: int, exponent: int) -> int:
        out = 1
        base = value
        e = exponent
        while e:
            if e & 1:
                out = self.mul(out, base)
            base = self.mul(base, base)
            e >>= 1
        return out

    def inv(self, value: int) -> int:
        if value == 0:
            raise ZeroDivisionError("0 has no inverse")
        return self.pow(value, (1 << self.m) - 2)


def rank_binary(columns: list[int], width: int) -> int:
    pivots = [0] * width
    rank = 0
    for column in columns:
        x = column
        while x:
            bit = x.bit_length() - 1
            if pivots[bit]:
                x ^= pivots[bit]
            else:
                pivots[bit] = x
                rank += 1
                break
    return rank


def rank_field(field: GF2m, matrix: list[list[int]]) -> int:
    rows = [row[:] for row in matrix]
    if not rows:
        return 0
    height = len(rows)
    width = len(rows[0])
    rank = 0
    for col in range(width):
        pivot = None
        for row in range(rank, height):
            if rows[row][col] != 0:
                pivot = row
                break
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = field.inv(rows[rank][col])
        rows[rank] = [field.mul(inv, value) for value in rows[rank]]
        for row in range(height):
            if row == rank or rows[row][col] == 0:
                continue
            factor = rows[row][col]
            rows[row] = [
                value ^ field.mul(factor, pivot_value)
                for value, pivot_value in zip(rows[row], rows[rank])
            ]
        rank += 1
        if rank == height:
            break
    return rank


def normal_basis(field: GF2m) -> list[int]:
    for value in range(1, 1 << field.m):
        conjugates = [field.pow(value, 1 << i) for i in range(field.m)]
        if rank_binary(conjugates, field.m) == field.m:
            return conjugates
    raise RuntimeError("no normal element found")


def coordinate_maps(basis: list[int]) -> tuple[dict[int, int], dict[int, int]]:
    coords_to_value: dict[int, int] = {}
    value_to_coords: dict[int, int] = {}
    for mask in range(1 << len(basis)):
        value = 0
        for index, basis_value in enumerate(basis):
            if mask & (1 << index):
                value ^= basis_value
        coords_to_value[mask] = value
        value_to_coords[value] = mask
    return coords_to_value, value_to_coords


def span_values(basis: list[int]) -> set[int]:
    values = {0}
    for basis_value in basis:
        values |= {value ^ basis_value for value in list(values)}
    return values


def linearized_eval(field: GF2m, coeffs: list[int], value: int) -> int:
    out = 0
    frob = value
    for coeff in coeffs:
        out ^= field.mul(coeff, frob)
        frob = field.mul(frob, frob)
    return out


def subspace_polynomial(field: GF2m, basis: list[int]) -> list[int]:
    coeffs = [1]
    for basis_value in basis:
        image = linearized_eval(field, coeffs, basis_value)
        if image == 0:
            continue
        factor = image
        new_coeffs = [0] * (len(coeffs) + 1)
        for index, coeff in enumerate(coeffs):
            new_coeffs[index + 1] ^= field.mul(coeff, coeff)
            new_coeffs[index] ^= field.mul(factor, coeff)
        coeffs = new_coeffs
    return coeffs


def moore_full_rank(field: GF2m, values: list[int]) -> bool:
    dim = len(values)
    matrix = [
        [field.pow(value, 1 << row) for value in values]
        for row in range(dim)
    ]
    return rank_field(field, matrix) == dim


def random_subspace_basis(field: GF2m, dim: int, rng: random.Random) -> list[int]:
    basis: list[int] = []
    while len(basis) < dim:
        candidate = rng.randrange(1, 1 << field.m)
        if rank_binary(basis + [candidate], field.m) == len(basis) + 1:
            basis.append(candidate)
    return basis


def check_case(
    field: GF2m,
    normal: list[int],
    coords_to_value: dict[int, int],
    value_to_coords: dict[int, int],
    head_dim: int,
    basis_u: list[int],
    tail_annihilator: list[int],
) -> tuple[bool, dict[str, int]]:
    tail_basis = normal[head_dim:]
    tail = span_values(tail_basis)
    subspace_u = span_values(basis_u)
    inter_zero = int(subspace_u & tail == {0})

    head_mask = (1 << head_dim) - 1
    head_columns = [value_to_coords[value] & head_mask for value in basis_u]
    head_rank_full = int(rank_binary(head_columns, head_dim) == head_dim)
    projected_values = [coords_to_value[column] for column in head_columns]
    projection_moore = int(moore_full_rank(field, projected_values))

    tail_annihilator_images = [
        linearized_eval(field, tail_annihilator, value)
        for value in basis_u
    ]
    annihilator_moore = int(moore_full_rank(field, tail_annihilator_images))

    ann_u = subspace_polynomial(field, basis_u)
    common_kernel_trivial = True
    for value in range(1, 1 << field.m):
        if (
            linearized_eval(field, ann_u, value) == 0
            and linearized_eval(field, tail_annihilator, value) == 0
        ):
            common_kernel_trivial = False
            break

    flags = {
        "intersection_zero": inter_zero,
        "head_rank_full": head_rank_full,
        "projection_moore_nonzero": projection_moore,
        "annihilator_moore_nonzero": annihilator_moore,
        "common_kernel_trivial": int(common_kernel_trivial),
    }
    return len(set(flags.values())) == 1, flags


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--m", type=int, default=6)
    parser.add_argument("--head-dim", type=int, default=3)
    parser.add_argument("--trials", type=int, default=200)
    parser.add_argument("--seed", type=int, default=20260606)
    args = parser.parse_args()

    if args.m not in PRIMITIVE_POLYS:
        raise SystemExit(f"no built-in GF(2^m) modulus for m={args.m}")
    if not 0 < args.head_dim < args.m:
        raise SystemExit("--head-dim must be between 1 and m-1")

    field = GF2m(args.m, PRIMITIVE_POLYS[args.m])
    normal = normal_basis(field)
    coords_to_value, value_to_coords = coordinate_maps(normal)
    tail_annihilator = subspace_polynomial(field, normal[args.head_dim:])
    tail_kernel = {
        value
        for value in range(1 << args.m)
        if linearized_eval(field, tail_annihilator, value) == 0
    }
    tail = span_values(normal[args.head_dim:])
    rng = random.Random(args.seed)

    mismatches = 0
    forced_intersection = 0
    examples: list[dict[str, int]] = []

    for _ in range(args.trials):
        basis_u = random_subspace_basis(field, args.head_dim, rng)
        ok, flags = check_case(
            field,
            normal,
            coords_to_value,
            value_to_coords,
            args.head_dim,
            basis_u,
            tail_annihilator,
        )
        mismatches += int(not ok)
        if not ok and len(examples) < 3:
            examples.append(flags)

    for tail_value in normal[args.head_dim : min(args.m, args.head_dim + 3)]:
        basis_u = [tail_value]
        while len(basis_u) < args.head_dim:
            candidate = rng.randrange(1, 1 << args.m)
            if rank_binary(basis_u + [candidate], args.m) == len(basis_u) + 1:
                basis_u.append(candidate)
        ok, flags = check_case(
            field,
            normal,
            coords_to_value,
            value_to_coords,
            args.head_dim,
            basis_u,
            tail_annihilator,
        )
        forced_intersection += 1
        mismatches += int(not ok)
        if not ok and len(examples) < 3:
            examples.append(flags)

    print("Selected-tail resultant equivalence toy")
    print(f"field=GF(2^{args.m})")
    print(f"modulus=0b{field.modulus:b}")
    print(f"normal_element={normal[0]}")
    print(f"head_dim={args.head_dim}")
    print(f"tail_dim={args.m - args.head_dim}")
    print(f"tail_annihilator_qdegree={len(tail_annihilator) - 1}")
    print(f"tail_kernel_matches_tail={int(tail_kernel == tail)}")
    print(f"random_trials={args.trials}")
    print(f"forced_intersection_trials={forced_intersection}")
    print(f"equivalence_mismatches={mismatches}")
    for index, flags in enumerate(examples, start=1):
        print(f"mismatch_{index}={flags}")


if __name__ == "__main__":
    main()
