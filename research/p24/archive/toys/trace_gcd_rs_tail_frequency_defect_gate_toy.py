#!/usr/bin/env python3
"""Frequency-defect gate for the RS-tail selected basis theorem.

The cyclic-shift/Riccati toys explain why the full Plucker chart should have
low displacement once the selected columns are already known to be a basis.
This toy isolates the non-circular determinant step that would make that chart
available.

After diagonalizing the common length-n cyclic/Lang shift, a six-block
shift-invariant row space splits into local frequency spaces W_a <= F^6.  The
p24 selection keeps four full blocks and k tail samples of a fifth block.  A
clean selected-basis theorem follows from:

* ordinary frequencies: W_a projects isomorphically to the four full selected
  blocks;
* defect frequencies: W_a has one extra dimension, the kernel of projection
  to the four full selected blocks is a line, and its tail coordinate is
  nonzero;
* the k tail samples give a k by k Fourier/Vandermonde matrix on those defect
  lines.

This turns the cyclic-shift evidence into a concrete p-unit proof obligation:
prove the local frequency Plucker minors and the defect tail residues are
p-units.  The tail Vandermonde factor is automatically a p-unit when p does
not divide n.
"""

from __future__ import annotations

from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q


TAIL_BLOCK = 0
DELETED_BLOCK = 3
SELECTED_FULL_BLOCKS = (1, 2, 4, 5)


@dataclass(frozen=True)
class FrequencyGateCase:
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


def selected_indices(block_len: int, tail_dim: int) -> list[int]:
    out: list[int] = []

    def coord(block: int, pos: int) -> int:
        return block * block_len + pos

    out.extend(coord(TAIL_BLOCK, pos) for pos in range(tail_dim))
    for block in SELECTED_FULL_BLOCKS:
        out.extend(coord(block, pos) for pos in range(block_len))
    return out


def columns(matrix: list[list[int]], indices: list[int]) -> list[list[int]]:
    return [[row[index] for index in indices] for row in matrix]


def local_basis(
    frequency: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
    bad_ordinary_frequency: int | None,
) -> list[list[int]]:
    rows: list[list[int]] = []
    for block in SELECTED_FULL_BLOCKS:
        row = [0] * 6
        row[block] = 1
        rows.append(row)

    if frequency in defect_frequencies:
        row = [0] * 6
        row[TAIL_BLOCK] = tau_by_frequency.get(frequency, 0)
        row[DELETED_BLOCK] = 17 + frequency
        rows.append(row)
    elif frequency == bad_ordinary_frequency:
        row = [0] * 6
        row[DELETED_BLOCK] = 1
        rows[-1] = row
    return rows


def time_domain_rows(
    q: int,
    block_len: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
    bad_ordinary_frequency: int | None = None,
) -> list[list[int]]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    rows: list[list[int]] = []
    for frequency in range(block_len):
        powers = [pow(omega, frequency * pos, q) for pos in range(block_len)]
        for coeffs in local_basis(
            frequency,
            defect_frequencies,
            tau_by_frequency,
            bad_ordinary_frequency,
        ):
            row: list[int] = []
            for block_coeff in coeffs:
                row.extend(block_coeff * power % q for power in powers)
            rows.append(row)
    return rows


def shift_row(row: list[int], block_len: int) -> list[int]:
    shifted = [0 for _ in row]
    for block in range(6):
        for pos in range(block_len):
            shifted[block * block_len + ((pos + 1) % block_len)] = row[
                block * block_len + pos
            ]
    return shifted


def tail_vandermonde_rank(
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
) -> int:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    matrix = [
        [
            tau_by_frequency.get(frequency, 0) * pow(omega, frequency * pos, q) % q
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
) -> FrequencyGateCase:
    rows = time_domain_rows(
        q,
        block_len,
        defect_frequencies,
        tau_by_frequency,
        bad_ordinary_frequency,
    )
    selected = columns(rows, selected_indices(block_len, tail_dim))
    ordinary_ok = 0
    defect_ok = 0
    for frequency in range(block_len):
        basis = local_basis(
            frequency,
            defect_frequencies,
            tau_by_frequency,
            bad_ordinary_frequency,
        )
        projection_rank = rank_mod_q(
            [[row[block] for block in SELECTED_FULL_BLOCKS] for row in basis],
            q,
        )
        if frequency in defect_frequencies:
            tail_nonzero = tau_by_frequency.get(frequency, 0) % q != 0
            if projection_rank == 4 and len(basis) == 5 and tail_nonzero:
                defect_ok += 1
        elif projection_rank == 4 and len(basis) == 4:
            ordinary_ok += 1
    selected_dim = len(selected[0])
    full_rank = rank_mod_q(rows, q)
    selected_rank = rank_mod_q(selected, q)
    shifted_rows = [shift_row(row, block_len) for row in rows]
    shift_invariant = rank_mod_q(rows + shifted_rows, q) == full_rank
    return FrequencyGateCase(
        label=label,
        q=q,
        block_len=block_len,
        tail_dim=tail_dim,
        row_dim=len(rows),
        full_rank=full_rank,
        selected_dim=selected_dim,
        selected_rank=selected_rank,
        shift_invariant=shift_invariant,
        ordinary_local_gates=ordinary_ok,
        defect_local_gates=defect_ok,
        defect_count=len(defect_frequencies),
        tail_vandermonde_rank=tail_vandermonde_rank(
            q,
            block_len,
            tail_dim,
            defect_frequencies,
            tau_by_frequency,
        ),
        omitted_support_kernel_dim=full_rank - selected_rank,
        selected_basis=(selected_rank == len(rows) == selected_dim),
    )


def print_case(case: FrequencyGateCase) -> None:
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
        f"selected_basis={int(case.selected_basis)}"
    )


def main() -> None:
    q = 101
    block_len = 5
    tail_dim = 3
    defects = {0, 1, 3}
    good_tau = {0: 2, 1: 5, 3: 11}
    zero_tau = {0: 2, 1: 0, 3: 11}

    good = analyze_case(
        "frequency_defect_vandermonde_gate",
        q,
        block_len,
        tail_dim,
        defects,
        good_tau,
    )
    bad_tail = analyze_case(
        "zero_tail_residue_control",
        q,
        block_len,
        tail_dim,
        defects,
        zero_tau,
    )
    bad_local = analyze_case(
        "ordinary_local_plucker_failure_control",
        q,
        block_len,
        tail_dim,
        defects,
        good_tau,
        bad_ordinary_frequency=2,
    )

    print("Trace-GCD RS-tail frequency-defect selected-basis gate toy")
    for case in (good, bad_tail, bad_local):
        print_case(case)
    print("p24")
    print("  p24_cyclic_shift_frequency_count=35")
    print("  p24_frequency_profile=16 defect lines of dimension 5 plus 19 ordinary dimensions 4")
    print("  p24_selected_full_blocks=4")
    print("  p24_tail_samples=16")
    print("  p24_selected_dim=156")
    print("  p24_omitted_dim=54")
    print("  p24_tail_vandermonde_is_punit=1")
    print("interpretation")
    print("  frequency_defect_gate_proves_selected_basis_without_chart_assumption=1")
    print("  local_frequency_plucker_punits_are_the_missing_arithmetic=1")
    print("  defect_tail_residue_punits_are_the_missing_arithmetic=1")
    print("  cyclic_invariance_alone_does_not_imply_selected_punit=1")
    print("  tail_invisible_eigenline_gives_omitted_support_kernel=1")
    print("  cyclic_shift_displacement_becomes_non_circular_after_this_gate=1")
    print("conclusion=reported_trace_gcd_rs_tail_frequency_defect_gate_toy")

    if (
        not good.selected_basis
        or good.tail_vandermonde_rank != tail_dim
        or not good.shift_invariant
        or bad_tail.selected_basis
        or bad_local.selected_basis
        or bad_tail.omitted_support_kernel_dim == 0
        or bad_local.omitted_support_kernel_dim == 0
        or not bad_tail.shift_invariant
        or not bad_local.shift_invariant
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
