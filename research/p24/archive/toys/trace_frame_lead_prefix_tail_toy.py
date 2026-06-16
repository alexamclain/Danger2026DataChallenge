#!/usr/bin/env python3
"""Tiny linear-algebra model for the leading trace-frame determinant.

p24 shape:

  prefix rows = 358
  tail rows   = 10
  source dim  = 368

If the full leading 368x368 determinant is nonzero, then the first 358 prefix
rows must have rank 358; otherwise adding only 10 tail rows cannot reach rank
368.  The selected tail rows also separate the 10-dimensional prefix kernel.

This toy uses the smaller shape prefix=3, tail=1, source=4 over F_101.
"""

from __future__ import annotations

P = 101


def mod(x: int) -> int:
    return x % P


def inv(x: int) -> int:
    if x % P == 0:
        raise ZeroDivisionError("zero has no inverse")
    return pow(x % P, P - 2, P)


def rank(matrix: list[list[int]]) -> int:
    rows = [[mod(x) for x in row] for row in matrix]
    if not rows:
        return 0
    m = len(rows)
    n = len(rows[0])
    r = 0
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = inv(rows[r][c])
        rows[r] = [mod(scale * x) for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [mod(a - factor * b) for a, b in zip(rows[i], rows[r])]
        r += 1
        if r == m:
            break
    return r


def kernel_basis(matrix: list[list[int]]) -> list[list[int]]:
    rows = [[mod(x) for x in row] for row in matrix]
    m = len(rows)
    n = len(rows[0])
    r = 0
    pivots: list[int] = []
    for c in range(n):
        pivot = None
        for i in range(r, m):
            if rows[i][c] != 0:
                pivot = i
                break
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        scale = inv(rows[r][c])
        rows[r] = [mod(scale * x) for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] != 0:
                factor = rows[i][c]
                rows[i] = [mod(a - factor * b) for a, b in zip(rows[i], rows[r])]
        pivots.append(c)
        r += 1

    free_cols = [c for c in range(n) if c not in pivots]
    basis = []
    for free in free_cols:
        vec = [0] * n
        vec[free] = 1
        for row_idx, pivot_col in enumerate(pivots):
            vec[pivot_col] = mod(-rows[row_idx][free])
        basis.append(vec)
    return basis


def mat_vec(row: list[int], vec: list[int]) -> int:
    return mod(sum(a * b for a, b in zip(row, vec)))


def main() -> None:
    prefix = [
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
    ]
    tail = [[1, 1, 1, 2]]
    lead = prefix + tail

    bad_prefix = [
        [1, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 1, 0, 2],
    ]
    bad_lead = bad_prefix + tail

    ker = kernel_basis(prefix)
    tail_on_kernel = [[mat_vec(row, vec) for vec in ker] for row in tail]

    print("trace-frame lead/prefix/tail toy")
    print(f"p={P}")
    print()
    print("good_leading_section")
    print(f"  prefix_rank={rank(prefix)}")
    print(f"  prefix_kernel_dim={len(ker)}")
    print(f"  tail_on_prefix_kernel={tail_on_kernel}")
    print(f"  tail_separates_kernel={int(rank(tail_on_kernel) == len(ker))}")
    print(f"  full_lead_rank={rank(lead)}")
    print(f"  full_lead_nonzero={int(rank(lead) == 4)}")
    print()
    print("dimension_guardrail")
    print(f"  bad_prefix_rank={rank(bad_prefix)}")
    print(f"  bad_full_lead_rank={rank(bad_lead)}")
    print("  bad_prefix_rank_plus_tail_rows=3")
    print("  full_rank_impossible_when_prefix_rank_below_3=1")
    print("conclusion=full_lead_nonzero_forces_prefix_rank_and_tail_injectivity")


if __name__ == "__main__":
    main()
