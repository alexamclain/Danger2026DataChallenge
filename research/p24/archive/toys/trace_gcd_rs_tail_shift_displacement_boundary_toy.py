#!/usr/bin/env python3
"""Canonical cyclic-shift displacement boundary for the RS-tail chart.

The block/skew Cauchy candidate should not fit arbitrary operators after
seeing the Plucker chart.  A natural source for the operators is the full
coordinate cyclic shift on the 210 Lang coordinates.  After the p24
selected/omitted split, this shift is block diagonal except for the two cut
edges in the truncated tail block.

For a full code row space `W` that is invariant under this coordinate shift
and whose selected coordinates are a basis, the graph chart `C` satisfies

    M_SS C - C M_OO

with rank bounded by the two boundary maps.  More exactly,

    M_SS C + C M_OS C - C M_OO - M_SO = 0,

the usual graph/Riccati form of invariance.  Thus the fixed operators in the
candidate theorem should be the selected and omitted blocks of the transported
coordinate shift, while the small residue comes from the tail cut.

This toy builds a small six-block cyclic-shift analogue, constructs a
shift-invariant row space by frequency subspaces, checks the low displacement
rank, and rejects a random graph chart with the same selected/omitted split.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import inverse_matrix, matmul


@dataclass(frozen=True)
class ShiftDisplacementReport:
    label: str
    q: int
    block_count: int
    block_len: int
    selected_dim: int
    omitted_dim: int
    selected_rank: int
    m_so_rank: int
    m_os_rank: int
    pure_displacement_rank: int
    boundary_corrected_rank: int
    riccati_residual_rank: int
    low_rank_gate: bool


def mat_add(
    left: list[list[int]],
    right: list[list[int]],
    q: int,
    sign: int = 1,
) -> list[list[int]]:
    return [
        [(a + sign * b) % q for a, b in zip(left_row, right_row)]
        for left_row, right_row in zip(left, right)
    ]


def primitive_root(q: int) -> int:
    factors: set[int] = set()
    n = q - 1
    d = 2
    while d * d <= n:
        if n % d == 0:
            factors.add(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        factors.add(n)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root found")


def independent_vectors(
    q: int,
    width: int,
    count: int,
    rng: random.Random,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for _trial in range(5000):
        candidate = [rng.randrange(q) for _ in range(width)]
        if not any(candidate):
            continue
        if rank_mod_q(rows + [candidate], q) > len(rows):
            rows.append(candidate)
            if len(rows) == count:
                return rows
    raise RuntimeError("could not find independent coefficient vectors")


def frequency_rows(
    q: int,
    block_count: int,
    block_len: int,
    dims_by_frequency: list[int],
    rng: random.Random,
) -> list[list[int]]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    rows: list[list[int]] = []
    for frequency, dim in enumerate(dims_by_frequency):
        coeffs = independent_vectors(q, block_count, dim, rng)
        powers = [pow(omega, frequency * time, q) for time in range(block_len)]
        for coeff in coeffs:
            row: list[int] = []
            for block_coeff in coeff:
                row.extend((block_coeff * power) % q for power in powers)
            rows.append(row)
    return rows


def p24_shaped_indices(
    block_count: int,
    block_len: int,
    tail_selected: int,
) -> tuple[list[int], list[int]]:
    if block_count != 6:
        raise ValueError("this toy uses the six p24 fixed-source blocks")
    selected: list[int] = []
    omitted: list[int] = []

    def block_coord(block: int, time: int) -> int:
        return block * block_len + time

    selected.extend(block_coord(0, time) for time in range(tail_selected))
    omitted.extend(block_coord(0, time) for time in range(tail_selected, block_len))
    for block in (1, 2, 4, 5):
        selected.extend(block_coord(block, time) for time in range(block_len))
    omitted.extend(block_coord(3, time) for time in range(block_len))
    return selected, omitted


def cyclic_shift_matrix(block_count: int, block_len: int) -> list[list[int]]:
    size = block_count * block_len
    matrix = [[0 for _col in range(size)] for _row in range(size)]
    for block in range(block_count):
        base = block * block_len
        for time in range(block_len):
            src = base + time
            dst = base + ((time + 1) % block_len)
            matrix[src][dst] = 1
    return matrix


def reorder_matrix(matrix: list[list[int]], order: list[int]) -> list[list[int]]:
    return [[matrix[row][col] for col in order] for row in order]


def columns(matrix: list[list[int]], indices: list[int]) -> list[list[int]]:
    return [[row[index] for index in indices] for row in matrix]


def rank_matrix(matrix: list[list[int]], q: int) -> int:
    return rank_mod_q(matrix, q) if matrix and matrix[0] else 0


def chart_from_rows(
    rows: list[list[int]],
    selected: list[int],
    omitted: list[int],
    q: int,
) -> tuple[list[list[int]], int]:
    selected_part = columns(rows, selected)
    omitted_part = columns(rows, omitted)
    selected_rank = rank_mod_q(selected_part, q)
    if selected_rank != len(selected):
        raise ValueError("selected coordinates are not a basis")
    return matmul(inverse_matrix(selected_part, q), omitted_part, q), selected_rank


def split_operator(
    block_count: int,
    block_len: int,
    selected_dim: int,
    selected: list[int],
    omitted: list[int],
) -> tuple[list[list[int]], list[list[int]], list[list[int]], list[list[int]]]:
    order = selected + omitted
    matrix = reorder_matrix(cyclic_shift_matrix(block_count, block_len), order)
    d = selected_dim
    m_ss = [row[:d] for row in matrix[:d]]
    m_so = [row[d:] for row in matrix[:d]]
    m_os = [row[:d] for row in matrix[d:]]
    m_oo = [row[d:] for row in matrix[d:]]
    return m_ss, m_so, m_os, m_oo


def displacement_report(
    label: str,
    chart: list[list[int]],
    selected_rank: int,
    q: int,
    block_count: int,
    block_len: int,
    selected: list[int],
    omitted: list[int],
) -> ShiftDisplacementReport:
    m_ss, m_so, m_os, m_oo = split_operator(
        block_count, block_len, len(selected), selected, omitted
    )
    mss_c = matmul(m_ss, chart, q)
    c_moo = matmul(chart, m_oo, q)
    c_mos_c = matmul(matmul(chart, m_os, q), chart, q)
    pure = mat_add(mss_c, c_moo, q, sign=-1)
    boundary_corrected = mat_add(pure, m_so, q, sign=-1)
    riccati = mat_add(boundary_corrected, c_mos_c, q, sign=1)
    boundary_rank = rank_matrix(m_so, q) + rank_matrix(m_os, q)
    pure_rank = rank_matrix(pure, q)
    return ShiftDisplacementReport(
        label=label,
        q=q,
        block_count=block_count,
        block_len=block_len,
        selected_dim=len(selected),
        omitted_dim=len(omitted),
        selected_rank=selected_rank,
        m_so_rank=rank_matrix(m_so, q),
        m_os_rank=rank_matrix(m_os, q),
        pure_displacement_rank=pure_rank,
        boundary_corrected_rank=rank_matrix(boundary_corrected, q),
        riccati_residual_rank=rank_matrix(riccati, q),
        low_rank_gate=(pure_rank <= boundary_rank),
    )


def find_invariant_chart(
    q: int,
    block_count: int,
    block_len: int,
    tail_selected: int,
    dims_by_frequency: list[int],
    seed: int,
) -> tuple[list[list[int]], int, list[int], list[int]]:
    selected, omitted = p24_shaped_indices(block_count, block_len, tail_selected)
    for attempt in range(200):
        rng = random.Random(seed + attempt)
        rows = frequency_rows(q, block_count, block_len, dims_by_frequency, rng)
        try:
            chart, selected_rank = chart_from_rows(rows, selected, omitted, q)
            return chart, selected_rank, selected, omitted
        except ValueError:
            continue
    raise RuntimeError("did not find an invariant row space with selected basis")


def random_chart(
    q: int,
    selected_dim: int,
    omitted_dim: int,
    seed: int,
) -> list[list[int]]:
    rng = random.Random(seed)
    return [
        [rng.randrange(q) for _col in range(omitted_dim)]
        for _row in range(selected_dim)
    ]


def print_report(report: ShiftDisplacementReport) -> None:
    print(
        f"case={report.label} q={report.q} blocks={report.block_count} "
        f"block_len={report.block_len} selected_dim={report.selected_dim} "
        f"omitted_dim={report.omitted_dim} selected_rank={report.selected_rank} "
        f"M_SO_rank={report.m_so_rank} M_OS_rank={report.m_os_rank} "
        f"pure_displacement_rank={report.pure_displacement_rank} "
        f"boundary_corrected_rank={report.boundary_corrected_rank} "
        f"riccati_residual_rank={report.riccati_residual_rank} "
        f"low_rank_gate={int(report.low_rank_gate)}"
    )


def main() -> None:
    q = 31
    block_count = 6
    block_len = 5
    tail_selected = 3
    seed = 20260606
    dims_by_frequency = [5, 5, 5, 4, 4]

    chart, selected_rank, selected, omitted = find_invariant_chart(
        q, block_count, block_len, tail_selected, dims_by_frequency, seed
    )
    invariant = displacement_report(
        "shift_invariant_frequency_code",
        chart,
        selected_rank,
        q,
        block_count,
        block_len,
        selected,
        omitted,
    )
    random = displacement_report(
        "random_graph_same_split",
        random_chart(q, len(selected), len(omitted), seed + 1000),
        len(selected),
        q,
        block_count,
        block_len,
        selected,
        omitted,
    )

    p24_block_len = 35
    p24_tail_selected = 16
    p24_selected_dim = 4 * p24_block_len + p24_tail_selected
    p24_omitted_dim = p24_block_len + (p24_block_len - p24_tail_selected)

    print("Trace-GCD RS-tail cyclic-shift displacement boundary toy")
    print_report(invariant)
    print_report(random)
    print("p24")
    print(f"  p24_cyclic_shift_blocks=6")
    print(f"  p24_block_len={p24_block_len}")
    print(f"  p24_selected_dim={p24_selected_dim}")
    print(f"  p24_omitted_dim={p24_omitted_dim}")
    print("  p24_tail_cut_cross_edges=2")
    print("  p24_expected_M_SO_rank=1")
    print("  p24_expected_M_OS_rank=1")
    print("interpretation")
    print("  invariant_full_code_gives_low_shift_displacement=1")
    print("  random_graph_same_split_rejected_by_shift_displacement=1")
    print("  riccati_identity_is_exact_for_shift_invariant_graph=1")
    print("  p24_candidate_A_B_are_selected_and_omitted_shift_blocks=1")
    print("  p24_small_residue_should_come_from_two_tail_cut_edges=1")
    print("conclusion=reported_trace_gcd_rs_tail_shift_displacement_boundary_toy")

    if (
        not invariant.low_rank_gate
        or invariant.riccati_residual_rank != 0
        or random.low_rank_gate
        or invariant.m_so_rank != 1
        or invariant.m_os_rank != 1
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
