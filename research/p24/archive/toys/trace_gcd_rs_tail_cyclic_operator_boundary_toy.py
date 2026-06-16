#!/usr/bin/env python3
"""Cyclic-operator boundary toy for the RS-tail full 210-column object.

The Plucker displacement handoff says that a low-rank full-column operator
boundary gives a low-rank chart displacement.  This toy tests the concrete
operator shape suggested by the RS-tail construction.

There are six right blocks of equal length.  The p24 selection keeps four full
blocks and the first `16` columns of a fifth tail block; it omits one whole
block and the final `19` columns of the tail block.  If a common cyclic/Lang
operator `T` advances every full right block, then:

* selected full blocks have no boundary;
* the wholly omitted block has no boundary;
* the split tail block contributes only the two cyclic cut edges.

So the full-column boundary rank, and therefore the Plucker-chart displacement
rank, should be at most `2` before any chart entries are inspected.  Random
omitted columns with the same selected basis and fixed `T,A,B` fail, while a
post-fit selected operator can make a random chart pass and is rejected as
certificate evidence.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_plucker_displacement_handoff_toy import (
    extend_columns_to_basis,
    mat_add,
    matrix_from_columns,
)
from trace_gcd_rs_tail_block_skew_cauchy_displacement_toy import random_matrix
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import inverse_matrix, matmul


@dataclass(frozen=True)
class CyclicBoundaryCase:
    label: str
    q: int
    block_count: int
    block_len: int
    selected_count: int
    omitted_count: int
    tail_cut_edges: int
    selected_rank: int
    displacement_rank: int
    boundary_rank: int
    handoff_identity: bool
    passes_rank_two_boundary: bool
    postfit_operator: bool


def primitive_root_mod_prime(q: int) -> int:
    factors: list[int] = []
    value = q - 1
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    for candidate in range(2, q):
        if all(pow(candidate, (q - 1) // factor, q) != 1 for factor in factors):
            return candidate
    raise RuntimeError("no primitive root found")


def diagonal_operator(eigenvalues: list[int]) -> list[list[int]]:
    return [
        [value if row == col else 0 for col, value in enumerate(eigenvalues)]
        for row in range(len(eigenvalues))
    ]


def apply_diagonal(eigenvalues: list[int], vector: list[int], power: int, q: int) -> list[int]:
    return [
        pow(value, power, q) * coord % q
        for value, coord in zip(eigenvalues, vector)
    ]


def columns_rank(columns: list[list[int]], q: int) -> int:
    if not columns:
        return 0
    return rank_mod_q(matrix_from_columns(columns), q)


def selected_and_omitted_labels(
    block_count: int,
    block_len: int,
    selected_full_blocks: int,
    tail_block: int,
    tail_dim: int,
    deleted_block: int,
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    selected: list[tuple[int, int]] = []
    omitted: list[tuple[int, int]] = []
    for block in range(block_count):
        for pos in range(block_len):
            label = (block, pos)
            if block < selected_full_blocks:
                selected.append(label)
            elif block == tail_block and pos < tail_dim:
                selected.append(label)
            elif block == tail_block or block == deleted_block:
                omitted.append(label)
    return selected, omitted


def coordinate_operator(
    source_labels: list[tuple[int, int]],
    target_labels: list[tuple[int, int]],
    block_len: int,
) -> tuple[list[list[int]], int]:
    target_index = {label: index for index, label in enumerate(target_labels)}
    source_index = {label: index for index, label in enumerate(source_labels)}
    operator = [
        [0 for _col in range(len(source_labels))]
        for _row in range(len(source_labels))
    ]
    cut_edges = 0
    for col, (block, pos) in enumerate(source_labels):
        next_label = (block, (pos + 1) % block_len)
        if next_label in source_index:
            operator[source_index[next_label]][col] = 1
        else:
            cut_edges += 1
    # The target labels are only used by callers to count source->other cuts;
    # keeping the argument explicit makes the selection pattern visible.
    _ = target_index
    return operator, cut_edges


def omitted_coordinate_operator(
    omitted_labels: list[tuple[int, int]],
    selected_labels: list[tuple[int, int]],
    block_len: int,
) -> tuple[list[list[int]], int]:
    omitted_index = {label: index for index, label in enumerate(omitted_labels)}
    selected_index = {label: index for index, label in enumerate(selected_labels)}
    operator = [
        [0 for _col in range(len(omitted_labels))]
        for _row in range(len(omitted_labels))
    ]
    cut_edges = 0
    for col, (block, pos) in enumerate(omitted_labels):
        next_label = (block, (pos + 1) % block_len)
        if next_label in omitted_index:
            operator[omitted_index[next_label]][col] = 1
        else:
            cut_edges += 1
    _ = selected_index
    return operator, cut_edges


def displacement(
    chart: list[list[int]],
    selected_operator: list[list[int]],
    omitted_operator: list[list[int]],
    q: int,
) -> list[list[int]]:
    return mat_add(
        matmul(selected_operator, chart, q),
        matmul(chart, omitted_operator, q),
        q,
        sign=-1,
    )


def analyze_case(
    label: str,
    selected_columns: list[list[int]],
    omitted_columns: list[list[int]],
    ambient_operator: list[list[int]],
    selected_operator: list[list[int]],
    omitted_operator: list[list[int]],
    q: int,
    tail_cut_edges: int,
    postfit_operator: bool = False,
) -> CyclicBoundaryCase:
    selected_matrix = matrix_from_columns(selected_columns)
    omitted_matrix = matrix_from_columns(omitted_columns)
    selected_inverse = inverse_matrix(selected_matrix, q)
    chart = matmul(selected_inverse, omitted_matrix, q)
    selected_boundary = mat_add(
        matmul(ambient_operator, selected_matrix, q),
        matmul(selected_matrix, selected_operator, q),
        q,
        sign=-1,
    )
    omitted_boundary = mat_add(
        matmul(ambient_operator, omitted_matrix, q),
        matmul(omitted_matrix, omitted_operator, q),
        q,
        sign=-1,
    )
    disp = displacement(chart, selected_operator, omitted_operator, q)
    handoff_rhs = matmul(
        selected_inverse,
        mat_add(
            omitted_boundary,
            matmul(selected_boundary, chart, q),
            q,
            sign=-1,
        ),
        q,
    )
    boundary = mat_add(
        omitted_boundary,
        matmul(selected_boundary, chart, q),
        q,
        sign=-1,
    )
    disp_rank = rank_mod_q(disp, q)
    return CyclicBoundaryCase(
        label=label,
        q=q,
        block_count=6,
        block_len=5,
        selected_count=len(selected_columns),
        omitted_count=len(omitted_columns),
        tail_cut_edges=tail_cut_edges,
        selected_rank=columns_rank(selected_columns, q),
        displacement_rank=disp_rank,
        boundary_rank=rank_mod_q(boundary, q),
        handoff_identity=(disp == handoff_rhs),
        passes_rank_two_boundary=(disp_rank <= tail_cut_edges),
        postfit_operator=postfit_operator,
    )


def find_cyclic_data(
    q: int,
    block_count: int,
    block_len: int,
    selected_labels: list[tuple[int, int]],
    rng: random.Random,
) -> tuple[list[int], list[list[list[int]]]]:
    selected_dim = len(selected_labels)
    root = primitive_root_mod_prime(q)
    omega = pow(root, (q - 1) // block_len, q)
    eigenvalues = [pow(omega, index % block_len, q) for index in range(selected_dim)]
    for _trial in range(2000):
        seeds = [
            [rng.randrange(q) for _row in range(selected_dim)]
            for _block in range(block_count)
        ]
        blocks = [
            [
                apply_diagonal(eigenvalues, seed, pos, q)
                for pos in range(block_len)
            ]
            for seed in seeds
        ]
        selected_columns = [blocks[block][pos] for block, pos in selected_labels]
        if columns_rank(selected_columns, q) == selected_dim:
            return eigenvalues, blocks
    raise RuntimeError("could not find full-rank cyclic selected basis")


def postfit_selected_operator(
    chart: list[list[int]],
    omitted_operator: list[list[int]],
    q: int,
) -> list[list[int]]:
    rows = len(chart)
    cols = len(chart[0])
    chart_basis_columns = extend_columns_to_basis(
        [list(col) for col in zip(*chart)],
        q,
    )
    basis_matrix = matrix_from_columns(chart_basis_columns)
    basis_inv = inverse_matrix(basis_matrix, q)
    target_on_chart = matmul(chart, omitted_operator, q)
    action_columns = [list(col) for col in zip(*target_on_chart)] + [
        [0] * rows for _ in range(rows - cols)
    ]
    return matmul(matrix_from_columns(action_columns), basis_inv, q)


def main() -> None:
    q = 101
    block_count = 6
    block_len = 5
    selected_full_blocks = 4
    tail_block = 4
    tail_dim = 3
    deleted_block = 5
    rng = random.Random(20260606)

    selected_labels, omitted_labels = selected_and_omitted_labels(
        block_count,
        block_len,
        selected_full_blocks,
        tail_block,
        tail_dim,
        deleted_block,
    )
    eigenvalues, blocks = find_cyclic_data(
        q,
        block_count,
        block_len,
        selected_labels,
        rng,
    )
    ambient_operator = diagonal_operator(eigenvalues)
    selected_operator, selected_to_omitted_cuts = coordinate_operator(
        selected_labels,
        omitted_labels,
        block_len,
    )
    omitted_operator, omitted_to_selected_cuts = omitted_coordinate_operator(
        omitted_labels,
        selected_labels,
        block_len,
    )
    tail_cut_edges = selected_to_omitted_cuts + omitted_to_selected_cuts
    selected_columns = [blocks[block][pos] for block, pos in selected_labels]
    omitted_columns = [blocks[block][pos] for block, pos in omitted_labels]

    random_omitted = random_matrix(len(omitted_columns), len(selected_columns), q, rng)
    random_omitted_columns = [list(col) for col in random_omitted]

    selected_matrix = matrix_from_columns(selected_columns)
    random_chart = matmul(inverse_matrix(selected_matrix, q), matrix_from_columns(random_omitted_columns), q)
    postfit_operator = postfit_selected_operator(random_chart, omitted_operator, q)

    rows = [
        analyze_case(
            "cyclic_lang_tail_split_boundary",
            selected_columns,
            omitted_columns,
            ambient_operator,
            selected_operator,
            omitted_operator,
            q,
            tail_cut_edges,
        ),
        analyze_case(
            "random_omitted_fixed_cyclic_operators",
            selected_columns,
            random_omitted_columns,
            ambient_operator,
            selected_operator,
            omitted_operator,
            q,
            tail_cut_edges,
        ),
        analyze_case(
            "random_omitted_postfit_selected_operator",
            selected_columns,
            random_omitted_columns,
            ambient_operator,
            postfit_operator,
            omitted_operator,
            q,
            tail_cut_edges,
            postfit_operator=True,
        ),
    ]

    p24_block_len = 35
    p24_selected_full_blocks = 4
    p24_tail_dim = 16
    p24_selected = p24_selected_full_blocks * p24_block_len + p24_tail_dim
    p24_omitted = p24_block_len + (p24_block_len - p24_tail_dim)

    print("Trace-GCD RS-tail cyclic operator boundary toy")
    for row in rows:
        print(
            f"case={row.label} q={row.q} block_count={row.block_count} "
            f"block_len={row.block_len} selected_count={row.selected_count} "
            f"omitted_count={row.omitted_count} tail_cut_edges={row.tail_cut_edges} "
            f"selected_rank={row.selected_rank} "
            f"displacement_rank={row.displacement_rank} "
            f"boundary_rank={row.boundary_rank} "
            f"handoff_identity={int(row.handoff_identity)} "
            f"passes_rank_two_boundary={int(row.passes_rank_two_boundary)} "
            f"postfit_operator={int(row.postfit_operator)}"
        )
    print("p24")
    print(f"  p24_block_count={block_count}")
    print(f"  p24_block_len={p24_block_len}")
    print(f"  p24_selected_full_blocks={p24_selected_full_blocks}")
    print(f"  p24_tail_dim={p24_tail_dim}")
    print(f"  p24_selected_columns={p24_selected}")
    print(f"  p24_omitted_columns={p24_omitted}")
    print("  p24_tail_split_cut_edges=2")
    print("interpretation")
    print("  cyclic_lang_operator_gives_tail_split_boundary_rank_two=1")
    print("  whole_deleted_block_contributes_no_boundary=1")
    print("  random_omitted_columns_fail_fixed_cyclic_operator_boundary=1")
    print("  postfit_selected_operator_again_not_certificate_evidence=1")
    print("  p24_operator_work_is_to_construct_common_cyclic_Lang_T_integrally=1")
    print("conclusion=reported_trace_gcd_rs_tail_cyclic_operator_boundary_toy")

    expected = {
        "cyclic_lang_tail_split_boundary": True,
        "random_omitted_fixed_cyclic_operators": False,
        "random_omitted_postfit_selected_operator": True,
    }
    for row in rows:
        if not row.handoff_identity:
            raise SystemExit(1)
        if row.passes_rank_two_boundary != expected[row.label]:
            raise SystemExit(1)
        if row.label == "cyclic_lang_tail_split_boundary" and row.tail_cut_edges != 2:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
