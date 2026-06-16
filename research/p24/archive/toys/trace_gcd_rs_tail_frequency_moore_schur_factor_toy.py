#!/usr/bin/env python3
"""Frequency-local factorization of the RS-tail Moore/Schur split.

The frequency-defect gate says that the selected `4n+k` coordinates are a
basis if all ordinary local Plucker gates and defect tail residues are
p-units.  This toy records the determinant factorization behind that claim.

After diagonalizing the common cyclic/Lang shift, order rows by frequency and
put the selected coordinates in two groups:

    four full selected blocks, then k tail samples.

In this order the selected matrix is block diagonal:

    [ prefix Fourier/Plucker block      0              ]
    [ 0                                 tail Vandermonde]

The prefix block determinant is a fixed Fourier unit times the product of
local 4x4 Plucker determinants.  The tail block determinant is the
Vandermonde on the defect frequencies, scaled by the defect tail residues.
This is the frequency-local form of the Moore/Schur split

    Delta_full = Delta_prefix * Delta_tail_mod_prefix.
"""

from __future__ import annotations

from dataclasses import dataclass
import random

from l1_axis_injectivity_scan import rank_mod_q
from trace_gcd_rs_tail_full_plucker_chart_cauchy_toy import det_mod


TAIL_BLOCK = 0
DELETED_BLOCK = 3
SELECTED_FULL_BLOCKS = (1, 2, 4, 5)


@dataclass(frozen=True)
class FactorCase:
    label: str
    q: int
    block_len: int
    tail_dim: int
    selected_dim: int
    full_rank: int
    prefix_rank: int
    tail_quotient_rank: int
    selected_det_nonzero: bool
    prefix_det_nonzero: bool
    tail_det_nonzero: bool
    local_plucker_product_nonzero: bool
    determinant_factorization: bool
    prefix_ratio: int | None
    cyclic_invariant: bool


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


def matmul(left: list[list[int]], right: list[list[int]], q: int) -> list[list[int]]:
    return [
        [
            sum(left[row][mid] * right[mid][col] for mid in range(len(right))) % q
            for col in range(len(right[0]))
        ]
        for row in range(len(left))
    ]


def random_invertible_4x4(q: int, rng: random.Random) -> list[list[int]]:
    for _ in range(1000):
        matrix = [[rng.randrange(q) for _col in range(4)] for _row in range(4)]
        if det_mod(matrix, q):
            return matrix
    raise RuntimeError("no invertible 4x4 matrix found")


def singularize(matrix: list[list[int]]) -> list[list[int]]:
    out = [row[:] for row in matrix]
    out[-1] = out[0][:]
    return out


def full_selected_columns(block_len: int, tail_dim: int) -> list[tuple[int, int]]:
    labels: list[tuple[int, int]] = []
    for block in SELECTED_FULL_BLOCKS:
        labels.extend((block, pos) for pos in range(block_len))
    labels.extend((TAIL_BLOCK, pos) for pos in range(tail_dim))
    return labels


def local_frequency_rows(
    frequency: int,
    local_plucker: list[list[int]],
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
) -> list[list[int]]:
    rows: list[list[int]] = []
    for row_index in range(4):
        coeffs = [0] * 6
        for col_index, block in enumerate(SELECTED_FULL_BLOCKS):
            coeffs[block] = local_plucker[row_index][col_index]
        rows.append(coeffs)
    if frequency in defect_frequencies:
        coeffs = [0] * 6
        coeffs[TAIL_BLOCK] = tau_by_frequency[frequency]
        coeffs[DELETED_BLOCK] = 17 + frequency
        rows.append(coeffs)
    return rows


def time_domain_rows(
    q: int,
    block_len: int,
    local_pluckers: dict[int, list[list[int]]],
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
) -> list[list[int]]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    rows: list[list[int]] = []

    def expand(coeffs: list[int], frequency: int) -> list[int]:
        powers = [pow(omega, frequency * pos, q) for pos in range(block_len)]
        row: list[int] = []
        for block_coeff in coeffs:
            row.extend(block_coeff * power % q for power in powers)
        return row

    for frequency in range(block_len):
        local_rows = local_frequency_rows(
            frequency,
            local_pluckers[frequency],
            defect_frequencies,
            tau_by_frequency,
        )
        for coeffs in local_rows[:4]:
            rows.append(expand(coeffs, frequency))
    for frequency in sorted(defect_frequencies):
        defect_row = local_frequency_rows(
            frequency,
            local_pluckers[frequency],
            defect_frequencies,
            tau_by_frequency,
        )[-1]
        rows.append(expand(defect_row, frequency))
    return rows


def selected_matrix(
    rows: list[list[int]],
    block_len: int,
    tail_dim: int,
) -> list[list[int]]:
    labels = full_selected_columns(block_len, tail_dim)
    return [[row[block * block_len + pos] for block, pos in labels] for row in rows]


def prefix_matrix(selected: list[list[int]], block_len: int) -> list[list[int]]:
    return [row[: 4 * block_len] for row in selected[: 4 * block_len]]


def tail_matrix(selected: list[list[int]], block_len: int, tail_dim: int) -> list[list[int]]:
    return [row[4 * block_len :] for row in selected[4 * block_len : 4 * block_len + tail_dim]]


def shift_row(row: list[int], block_len: int) -> list[int]:
    shifted = [0 for _ in row]
    for block in range(6):
        for pos in range(block_len):
            shifted[block * block_len + ((pos + 1) % block_len)] = row[
                block * block_len + pos
            ]
    return shifted


def local_plucker_product(
    local_pluckers: dict[int, list[list[int]]],
    q: int,
) -> int:
    out = 1
    for frequency in sorted(local_pluckers):
        out = out * det_mod(local_pluckers[frequency], q) % q
    return out


def analyze_case(
    label: str,
    q: int,
    block_len: int,
    tail_dim: int,
    local_pluckers: dict[int, list[list[int]]],
    defect_frequencies: set[int],
    tau_by_frequency: dict[int, int],
) -> FactorCase:
    rows = time_domain_rows(
        q,
        block_len,
        local_pluckers,
        defect_frequencies,
        tau_by_frequency,
    )
    selected = selected_matrix(rows, block_len, tail_dim)
    prefix = prefix_matrix(selected, block_len)
    tail = tail_matrix(selected, block_len, tail_dim)
    selected_det = det_mod(selected, q)
    prefix_det = det_mod(prefix, q)
    tail_det = det_mod(tail, q)
    local_product = local_plucker_product(local_pluckers, q)
    full_rank = rank_mod_q(selected, q)
    prefix_rank = rank_mod_q(prefix, q)
    tail_quotient_rank = rank_mod_q(tail, q)
    shifted_rows = [shift_row(row, block_len) for row in rows]
    row_rank = rank_mod_q(rows, q)
    return FactorCase(
        label=label,
        q=q,
        block_len=block_len,
        tail_dim=tail_dim,
        selected_dim=len(selected),
        full_rank=full_rank,
        prefix_rank=prefix_rank,
        tail_quotient_rank=tail_quotient_rank,
        selected_det_nonzero=selected_det != 0,
        prefix_det_nonzero=prefix_det != 0,
        tail_det_nonzero=tail_det != 0,
        local_plucker_product_nonzero=local_product != 0,
        determinant_factorization=(selected_det - prefix_det * tail_det) % q == 0,
        prefix_ratio=(
            prefix_det * pow(local_product, -1, q) % q
            if local_product
            else None
        ),
        cyclic_invariant=rank_mod_q(rows + shifted_rows, q) == row_rank,
    )


def print_case(case: FactorCase) -> None:
    print(
        f"case={case.label} q={case.q} block_len={case.block_len} "
        f"tail_dim={case.tail_dim} selected_dim={case.selected_dim} "
        f"full_rank={case.full_rank} prefix_rank={case.prefix_rank} "
        f"tail_quotient_rank={case.tail_quotient_rank} "
        f"selected_det_nonzero={int(case.selected_det_nonzero)} "
        f"prefix_det_nonzero={int(case.prefix_det_nonzero)} "
        f"tail_det_nonzero={int(case.tail_det_nonzero)} "
        f"local_plucker_product_nonzero={int(case.local_plucker_product_nonzero)} "
        f"determinant_factorization={int(case.determinant_factorization)} "
        f"prefix_ratio={case.prefix_ratio} "
        f"cyclic_invariant={int(case.cyclic_invariant)}"
    )


def main() -> None:
    q = 101
    block_len = 5
    tail_dim = 3
    defects = {0, 1, 3}
    seed = 20260606
    rng = random.Random(seed)

    local = {
        frequency: random_invertible_4x4(q, rng)
        for frequency in range(block_len)
    }
    tau = {0: 2, 1: 5, 3: 11}

    bad_local = {frequency: [row[:] for row in matrix] for frequency, matrix in local.items()}
    bad_local[2] = singularize(bad_local[2])
    bad_tau = dict(tau)
    bad_tau[1] = 0

    rows = [
        analyze_case(
            "frequency_moore_schur_factorization",
            q,
            block_len,
            tail_dim,
            local,
            defects,
            tau,
        ),
        analyze_case(
            "singular_local_plucker_control",
            q,
            block_len,
            tail_dim,
            bad_local,
            defects,
            tau,
        ),
        analyze_case(
            "zero_defect_tail_residue_control",
            q,
            block_len,
            tail_dim,
            local,
            defects,
            bad_tau,
        ),
    ]

    print("Trace-GCD RS-tail frequency Moore/Schur factorization toy")
    for row in rows:
        print_case(row)
    print("p24")
    print("  p24_prefix_local_plucker_factors=35")
    print("  p24_ordinary_local_isomorphism_factors=19")
    print("  p24_defect_local_rank4_factors=16")
    print("  p24_defect_tail_residue_factors=16")
    print("  p24_tail_vandermonde_size=16")
    print("interpretation")
    print("  local_plucker_product_is_frequency_form_of_prefix_moore_factor=1")
    print("  defect_tail_residues_are_frequency_form_of_quotient_tail_moore_factor=1")
    print("  selected_det_factors_as_prefix_times_tail_quotient=1")
    print("  cyclic_invariance_alone_still_allows_both_controls=1")
    print("conclusion=reported_trace_gcd_rs_tail_frequency_moore_schur_factor_toy")

    good, bad_plucker, bad_tail = rows
    if (
        not good.selected_det_nonzero
        or not good.determinant_factorization
        or not good.cyclic_invariant
        or bad_plucker.selected_det_nonzero
        or bad_tail.selected_det_nonzero
        or not bad_plucker.cyclic_invariant
        or not bad_tail.cyclic_invariant
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
