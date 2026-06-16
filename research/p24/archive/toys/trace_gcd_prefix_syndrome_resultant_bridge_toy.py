#!/usr/bin/env python3
"""Finite bridge from prefix syndrome rank to tail resultant rank.

Rows are trace-pairing coordinate elements in an ambient F_q^d.  Prefix
syndrome surjectivity is row rank k.  Once that holds, the tail resultant is
the test that the tail rows restrict injectively to the prefix kernel.
"""

from __future__ import annotations

from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q


def rref(matrix: list[list[int]], q: int) -> tuple[list[list[int]], list[int]]:
    rows = [row[:] for row in matrix if any(value % q for value in row)]
    if not rows:
        return [], []
    width = len(rows[0])
    pivot_columns: list[int] = []
    pivot_row = 0
    for col in range(width):
        pivot = None
        for row in range(pivot_row, len(rows)):
            if rows[row][col] % q:
                pivot = row
                break
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % q, -1, q)
        rows[pivot_row] = [(value * inv) % q for value in rows[pivot_row]]
        for row in range(len(rows)):
            if row == pivot_row:
                continue
            factor = rows[row][col] % q
            if factor:
                rows[row] = [
                    (value - factor * pivot_value) % q
                    for value, pivot_value in zip(rows[row], rows[pivot_row])
                ]
        pivot_columns.append(col)
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return rows, pivot_columns


def nullspace_basis(matrix: list[list[int]], q: int, width: int) -> list[list[int]]:
    reduced, pivots = rref(matrix, q)
    pivot_set = set(pivots)
    free_columns = [col for col in range(width) if col not in pivot_set]
    basis: list[list[int]] = []
    for free in free_columns:
        vector = [0] * width
        vector[free] = 1
        for row, pivot_col in enumerate(pivots):
            vector[pivot_col] = (-reduced[row][free]) % q
        basis.append(vector)
    return basis


def dot(row: list[int], vector: list[int], q: int) -> int:
    return sum(a * b for a, b in zip(row, vector)) % q


def tail_rank_on_kernel(
    tail_rows: list[list[int]],
    kernel_basis: list[list[int]],
    q: int,
) -> int:
    if not kernel_basis:
        return 0
    restricted = [
        [dot(row, vector, q) for vector in kernel_basis]
        for row in tail_rows
    ]
    return rank_mod_q(restricted, q)


@dataclass(frozen=True)
class Case:
    label: str
    prefix_rows: list[list[int]]
    tail_rows: list[list[int]]


def e(index: int, dim: int) -> list[int]:
    row = [0] * dim
    row[index] = 1
    return row


def add_rows(*rows: list[int], q: int) -> list[int]:
    return [sum(values) % q for values in zip(*rows)]


def report_case(case: Case, q: int, ambient_dim: int, prefix_dim: int, tail_dim: int) -> None:
    prefix_rank = rank_mod_q(case.prefix_rows, q)
    kernel = nullspace_basis(case.prefix_rows, q, ambient_dim)
    tail_kernel_rank = tail_rank_on_kernel(case.tail_rows, kernel, q)
    full_rank = rank_mod_q(case.prefix_rows + case.tail_rows, q)
    prefix_surjective = prefix_rank == prefix_dim
    tail_injective = tail_kernel_rank == len(kernel) == tail_dim
    full_nonzero = full_rank == ambient_dim
    event_match = full_nonzero == (prefix_surjective and tail_injective)
    print(
        f"case={case.label} "
        f"prefix_rank={prefix_rank} "
        f"prefix_surjective={int(prefix_surjective)} "
        f"kernel_dim={len(kernel)} "
        f"tail_rank_on_kernel={tail_kernel_rank} "
        f"tail_injective_on_kernel={int(tail_injective)} "
        f"full_rank={full_rank} "
        f"full_residual_nonzero={int(full_nonzero)} "
        f"event_match={int(event_match)}"
    )


def main() -> None:
    q = 5
    ambient_dim = 6
    prefix_dim = 4
    tail_dim = 2
    basis = [e(i, ambient_dim) for i in range(ambient_dim)]

    cases = [
        Case(
            label="good_prefix_good_tail",
            prefix_rows=[basis[0], basis[1], basis[2], basis[3]],
            tail_rows=[basis[4], basis[5]],
        ),
        Case(
            label="dependent_prefix",
            prefix_rows=[basis[0], basis[1], basis[2], basis[2]],
            tail_rows=[basis[4], basis[5]],
        ),
        Case(
            label="good_prefix_bad_tail",
            prefix_rows=[basis[0], basis[1], basis[2], basis[3]],
            tail_rows=[
                add_rows(basis[0], basis[1], q=q),
                add_rows(basis[2], basis[3], q=q),
            ],
        ),
        Case(
            label="good_prefix_one_tail_direction",
            prefix_rows=[basis[0], basis[1], basis[2], basis[3]],
            tail_rows=[basis[4], add_rows(basis[4], basis[0], q=q)],
        ),
    ]

    print("Trace-GCD prefix syndrome/resultant bridge toy")
    print(f"q={q}")
    print(f"ambient_dim={ambient_dim}")
    print(f"prefix_dim={prefix_dim}")
    print(f"tail_dim={tail_dim}")
    for case in cases:
        report_case(case, q, ambient_dim, prefix_dim, tail_dim)
    print("p24")
    print("  p24_ambient_dim=156")
    print("  p24_prefix_syndrome_target_dim=140")
    print("  p24_residual_kernel_dim=16")
    print("  p24_tail_window_dim=16")
    print("interpretation")
    print("  prefix_syndrome_surjective_gives_kernel_dim_16=1")
    print("  tail_resultant_nonzero_iff_tail_injective_on_kernel=1")
    print("  full_140_plus_16_residual_nonzero_iff_prefix_and_tail=1")
    print("  dependent_prefix_and_bad_tail_controls_detected=1")
    print("conclusion=reported_trace_gcd_prefix_syndrome_resultant_bridge_toy")


if __name__ == "__main__":
    main()
