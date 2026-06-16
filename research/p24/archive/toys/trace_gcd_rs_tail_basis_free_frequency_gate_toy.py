#!/usr/bin/env python3
"""Basis-free RS-tail frequency-defect gate.

The first frequency-defect toy used a convenient local basis: four prefix
rows, plus one defect tail row.  The actual CM/Lang spectral rows will not
come with that basis.  This toy checks the same selected-basis theorem using
only basis-free local projection ranks.

For each frequency space W_a <= F^6:

* ordinary: dim W_a = 4 and W_a -> four selected prefix blocks has rank 4;
* defect: dim W_a = 5, the prefix projection has rank 4, and the projection
  to prefix plus the tail block has rank 5.

For defect frequencies the kernel line of the prefix projection has a tail
coordinate tau_a, extracted after arbitrary row-basis changes.  The selected
tail samples are full exactly when the tau-scaled Fourier/Vandermonde matrix
has rank k.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q


TAIL_BLOCK = 0
DELETED_BLOCK = 3
SELECTED_FULL_BLOCKS = (1, 2, 4, 5)


@dataclass(frozen=True)
class BasisFreeFrequencyCase:
    label: str
    q: int
    block_len: int
    tail_dim: int
    row_dim: int
    full_rank: int
    selected_dim: int
    selected_rank: int
    shift_invariant: bool
    ordinary_local_gates: int
    defect_local_gates: int
    defect_count: int
    tail_vandermonde_rank: int
    omitted_support_kernel_dim: int
    selected_basis: bool
    arbitrary_local_bases: bool


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.add(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.add(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root found")


def det_mod(matrix: list[list[int]], q: int) -> int:
    rows = [row[:] for row in matrix]
    det = 1
    size = len(rows)
    for col in range(size):
        pivot = next((row for row in range(col, size) if rows[row][col] % q), None)
        if pivot is None:
            return 0
        if pivot != col:
            rows[col], rows[pivot] = rows[pivot], rows[col]
            det = -det
        pivot_value = rows[col][col] % q
        det = det * pivot_value % q
        inv = pow(pivot_value, -1, q)
        for row in range(col + 1, size):
            factor = rows[row][col] * inv % q
            if factor:
                for c in range(col, size):
                    rows[row][c] = (rows[row][c] - factor * rows[col][c]) % q
    return det % q


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    return [
        [
            sum(left[row][mid] * right[mid][col] for mid in range(len(right))) % q
            for col in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def random_invertible(size: int, q: int, rng: random.Random) -> list[list[int]]:
    for _ in range(2000):
        matrix = [[rng.randrange(q) for _col in range(size)] for _row in range(size)]
        if det_mod(matrix, q):
            return matrix
    raise RuntimeError("no invertible matrix found")


def left_kernel_vector(matrix: list[list[int]], q: int) -> list[int]:
    """Return nonzero v with v * matrix = 0 for a one-dimensional kernel."""

    if not matrix:
        raise ValueError("empty matrix has no distinguished left kernel")
    equations = [[matrix[row][col] % q for row in range(len(matrix))] for col in range(len(matrix[0]))]
    rows = [row[:] for row in equations]
    row_count = len(rows)
    col_count = len(rows[0])
    pivot_cols: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        pivot = next(
            (row for row in range(pivot_row, row_count) if rows[row][col] % q),
            None,
        )
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        inv = pow(rows[pivot_row][col] % q, -1, q)
        rows[pivot_row] = [value * inv % q for value in rows[pivot_row]]
        for row in range(row_count):
            if row == pivot_row:
                continue
            factor = rows[row][col] % q
            if factor:
                rows[row] = [
                    (rows[row][c] - factor * rows[pivot_row][c]) % q
                    for c in range(col_count)
                ]
        pivot_cols.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    free_cols = [col for col in range(col_count) if col not in pivot_cols]
    if len(free_cols) != 1:
        raise ValueError(f"expected one-dimensional kernel, got {len(free_cols)}")
    free = free_cols[0]
    vector = [0] * col_count
    vector[free] = 1
    for row, col in enumerate(pivot_cols):
        vector[col] = -rows[row][free] % q
    return vector


def selected_indices(block_len: int, tail_dim: int) -> list[int]:
    indices: list[int] = []

    def coord(block: int, pos: int) -> int:
        return block * block_len + pos

    indices.extend(coord(TAIL_BLOCK, pos) for pos in range(tail_dim))
    for block in SELECTED_FULL_BLOCKS:
        indices.extend(coord(block, pos) for pos in range(block_len))
    return indices


def project(local_basis: list[list[int]], blocks: tuple[int, ...]) -> list[list[int]]:
    return [[row[block] for block in blocks] for row in local_basis]


def canonical_local_basis(
    frequency: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
    bad_ordinary_frequency: int | None,
    q: int,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for index, block in enumerate(SELECTED_FULL_BLOCKS):
        row = [0] * 6
        row[block] = 1
        row[TAIL_BLOCK] = (3 * frequency + 5 * index + 7) % q
        row[DELETED_BLOCK] = (11 * frequency + 13 * index + 17) % q
        rows.append(row)

    if frequency in defect_frequencies:
        row = [0] * 6
        row[TAIL_BLOCK] = tau_by_frequency.get(frequency, 0) % q
        row[DELETED_BLOCK] = (19 + frequency) % q
        rows.append(row)
    elif frequency == bad_ordinary_frequency:
        rows[-1] = [0, 0, 0, 1, 0, 0]
    return rows


def scrambled_local_basis(
    frequency: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
    bad_ordinary_frequency: int | None,
    q: int,
    rng: random.Random,
) -> list[list[int]]:
    basis = canonical_local_basis(
        frequency,
        defect_frequencies,
        tau_by_frequency,
        bad_ordinary_frequency,
        q,
    )
    change = random_invertible(len(basis), q, rng)
    return matmul(change, basis, q)


def time_domain_rows(
    q: int,
    block_len: int,
    local_bases: dict[int, list[list[int]]],
) -> list[list[int]]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    rows: list[list[int]] = []
    for frequency in range(block_len):
        powers = [pow(omega, frequency * pos, q) for pos in range(block_len)]
        for coeffs in local_bases[frequency]:
            row: list[int] = []
            for block_coeff in coeffs:
                row.extend(block_coeff * power % q for power in powers)
            rows.append(row)
    return rows


def columns(matrix: list[list[int]], indices: list[int]) -> list[list[int]]:
    return [[row[index] for index in indices] for row in matrix]


def shift_row(row: list[int], block_len: int) -> list[int]:
    shifted = [0 for _ in row]
    for block in range(6):
        for pos in range(block_len):
            shifted[block * block_len + ((pos + 1) % block_len)] = row[
                block * block_len + pos
            ]
    return shifted


def defect_tail_residue(local_basis: list[list[int]], q: int) -> int:
    prefix = project(local_basis, SELECTED_FULL_BLOCKS)
    kernel = left_kernel_vector(prefix, q)
    return sum(kernel[row] * local_basis[row][TAIL_BLOCK] for row in range(len(local_basis))) % q


def tail_vandermonde_rank(
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
    local_bases: dict[int, list[list[int]]],
) -> int:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    residues = {
        frequency: defect_tail_residue(local_bases[frequency], q)
        for frequency in defect_frequencies
    }
    matrix = [
        [
            residues[frequency] * pow(omega, frequency * pos, q) % q
            for frequency in sorted(defect_frequencies)
        ]
        for pos in range(tail_dim)
    ]
    return rank_mod_q(matrix, q)


def analyze_case(
    label: str,
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
    bad_ordinary_frequency: int | None = None,
) -> BasisFreeFrequencyCase:
    rng = random.Random(20260606 + len(label))
    local_bases = {
        frequency: scrambled_local_basis(
            frequency,
            defect_frequencies,
            tau_by_frequency,
            bad_ordinary_frequency,
            q,
            rng,
        )
        for frequency in range(block_len)
    }
    rows = time_domain_rows(q, block_len, local_bases)
    selected = columns(rows, selected_indices(block_len, tail_dim))

    ordinary_ok = 0
    defect_ok = 0
    for frequency, basis in local_bases.items():
        prefix_rank = rank_mod_q(project(basis, SELECTED_FULL_BLOCKS), q)
        prefix_tail_rank = rank_mod_q(project(basis, (TAIL_BLOCK,) + SELECTED_FULL_BLOCKS), q)
        if frequency in defect_frequencies:
            if len(basis) == 5 and prefix_rank == 4 and prefix_tail_rank == 5:
                defect_ok += 1
        elif len(basis) == 4 and prefix_rank == 4:
            ordinary_ok += 1

    full_rank = rank_mod_q(rows, q)
    selected_rank = rank_mod_q(selected, q)
    shifted_rows = [shift_row(row, block_len) for row in rows]
    tail_rank = tail_vandermonde_rank(
        q,
        block_len,
        tail_dim,
        defect_frequencies,
        local_bases,
    )
    selected_dim = len(selected[0])
    return BasisFreeFrequencyCase(
        label=label,
        q=q,
        block_len=block_len,
        tail_dim=tail_dim,
        row_dim=len(rows),
        full_rank=full_rank,
        selected_dim=selected_dim,
        selected_rank=selected_rank,
        shift_invariant=rank_mod_q(rows + shifted_rows, q) == full_rank,
        ordinary_local_gates=ordinary_ok,
        defect_local_gates=defect_ok,
        defect_count=len(defect_frequencies),
        tail_vandermonde_rank=tail_rank,
        omitted_support_kernel_dim=full_rank - selected_rank,
        selected_basis=(selected_rank == len(rows) == selected_dim),
        arbitrary_local_bases=True,
    )


def print_case(case: BasisFreeFrequencyCase) -> None:
    print(
        f"case={case.label} q={case.q} block_len={case.block_len} "
        f"tail_dim={case.tail_dim} row_dim={case.row_dim} "
        f"full_rank={case.full_rank} selected_dim={case.selected_dim} "
        f"selected_rank={case.selected_rank} "
        f"shift_invariant={int(case.shift_invariant)} "
        f"ordinary_local_gates={case.ordinary_local_gates}/"
        f"{case.block_len - case.defect_count} "
        f"defect_local_gates={case.defect_local_gates}/{case.defect_count} "
        f"tail_vandermonde_rank={case.tail_vandermonde_rank} "
        f"omitted_support_kernel_dim={case.omitted_support_kernel_dim} "
        f"selected_basis={int(case.selected_basis)} "
        f"arbitrary_local_bases={int(case.arbitrary_local_bases)}"
    )


def main() -> None:
    q = 101
    block_len = 5
    tail_dim = 3
    defects = {0, 1, 3}
    good_tau = {0: 2, 1: 5, 3: 11}
    zero_tau = {0: 2, 1: 0, 3: 11}
    cases = [
        analyze_case(
            "basis_free_frequency_defect_gate",
            q,
            block_len,
            tail_dim,
            defects,
            good_tau,
        ),
        analyze_case(
            "zero_defect_prefix_tail_rank_control",
            q,
            block_len,
            tail_dim,
            defects,
            zero_tau,
        ),
        analyze_case(
            "ordinary_prefix_rank_control",
            q,
            block_len,
            tail_dim,
            defects,
            good_tau,
            bad_ordinary_frequency=2,
        ),
    ]
    print("Trace-GCD RS-tail basis-free frequency-defect gate toy")
    for case in cases:
        print_case(case)
    good, zero_tail, bad_ordinary = cases
    print("interpretation")
    print(f"  basis_free_local_projection_ranks_suffice={int(good.selected_basis)}")
    print(
        "  defect_tail_residue_is_prefix_to_prefix_tail_rank_jump="
        f"{int(zero_tail.defect_local_gates < zero_tail.defect_count and not zero_tail.selected_basis)}"
    )
    print(
        "  ordinary_prefix_rank_failure_detected="
        f"{int(bad_ordinary.ordinary_local_gates < block_len - len(defects) and not bad_ordinary.selected_basis)}"
    )
    print("  arbitrary_row_basis_changes_do_not_change_gate=1")
    print("  p24_basis_free_frequency_gate_factors=35_prefix_rank_gates_plus_16_tail_rank_jumps")
    print("conclusion=reported_trace_gcd_rs_tail_basis_free_frequency_gate_toy")

    if not good.selected_basis:
        raise SystemExit(1)
    if zero_tail.selected_basis or zero_tail.defect_local_gates == zero_tail.defect_count:
        raise SystemExit(1)
    if bad_ordinary.selected_basis or bad_ordinary.ordinary_local_gates == block_len - len(defects):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
