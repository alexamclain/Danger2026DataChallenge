#!/usr/bin/env python3
"""Resultant packaging for the RS-tail frequency-defect gate.

The frequency-defect theorem reduces the selected-basis determinant to local
frequency gates: a 4x4 Plucker unit at every length-n frequency, plus nonzero
tail residues on the k defect frequencies.  This toy records the next useful
compression step.

If those local Plucker and tail-residue values are evaluations of cyclic
polynomial sections P(x) and T(x), then all local checks can be certified by
resultants:

    Res(P, x^n - 1) != 0,
    product_{a in A} T(omega^a) != 0,

together with a selector polynomial whose roots inside mu_n are exactly the
defect frequencies A, |A|=k.  The hard p24 arithmetic remains identifying the
actual CM/Lang sections P,T,A; this file only checks the finite reduction and
its failure controls.
"""

from __future__ import annotations

from dataclasses import dataclass

from l1_axis_injectivity_scan import rank_mod_q


TAIL_BLOCK = 0
DELETED_BLOCK = 3
SELECTED_FULL_BLOCKS = (1, 2, 4, 5)


@dataclass(frozen=True)
class ResultantGateCase:
    label: str
    q: int
    block_len: int
    tail_dim: int
    defect_count: int
    full_rank: int
    selected_rank: int
    selected_dim: int
    plucker_resultant_nonzero: bool
    tail_support_resultant_nonzero: bool
    selector_has_exact_tail_size: bool
    resultant_gate_predicts_basis: bool
    selected_basis: bool
    omitted_support_kernel_dim: int


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


def poly_eval(poly: list[int], x: int, q: int) -> int:
    value = 0
    power = 1
    for coeff in poly:
        value = (value + coeff * power) % q
        power = power * x % q
    return value


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


def expand_frequency_row(
    q: int,
    block_len: int,
    omega: int,
    frequency: int,
    coeffs: list[int],
) -> list[int]:
    powers = [pow(omega, frequency * pos, q) for pos in range(block_len)]
    row: list[int] = []
    for coeff in coeffs:
        row.extend(coeff * power % q for power in powers)
    return row


def time_domain_rows(
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
    plucker_poly: list[int],
    tail_poly: list[int],
) -> list[list[int]]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    rows: list[list[int]] = []
    for frequency in range(block_len):
        x = pow(omega, frequency, q)
        plucker_value = poly_eval(plucker_poly, x, q)
        local_rows: list[list[int]] = []
        for index, block in enumerate(SELECTED_FULL_BLOCKS):
            coeffs = [0] * 6
            coeffs[block] = plucker_value if index == 0 else 1
            if index == 0:
                coeffs[DELETED_BLOCK] = 1
            local_rows.append(coeffs)
        if frequency in defect_frequencies:
            coeffs = [0] * 6
            coeffs[TAIL_BLOCK] = poly_eval(tail_poly, x, q)
            coeffs[DELETED_BLOCK] = 17 + frequency
            local_rows.append(coeffs)
        for coeffs in local_rows:
            rows.append(expand_frequency_row(q, block_len, omega, frequency, coeffs))
    return rows


def root_values(q: int, block_len: int) -> list[int]:
    root = primitive_root(q)
    omega = pow(root, (q - 1) // block_len, q)
    return [pow(omega, frequency, q) for frequency in range(block_len)]


def root_product(poly: list[int], roots: list[int], q: int) -> int:
    out = 1
    for root in roots:
        out = out * poly_eval(poly, root, q) % q
    return out


def selector_exact_tail_size(
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
) -> bool:
    # In the p24 proof this would be a divisor/support certificate for the
    # defect idempotent.  Here the finite support is explicit.
    return len(defect_frequencies) == tail_dim and all(
        0 <= frequency < block_len for frequency in defect_frequencies
    )


def analyze_case(
    label: str,
    q: int,
    block_len: int,
    tail_dim: int,
    defect_frequencies: set[int],
    plucker_poly: list[int],
    tail_poly: list[int],
) -> ResultantGateCase:
    rows = time_domain_rows(
        q,
        block_len,
        tail_dim,
        defect_frequencies,
        plucker_poly,
        tail_poly,
    )
    selected = columns(rows, selected_indices(block_len, tail_dim))
    roots = root_values(q, block_len)
    defect_roots = [roots[frequency] for frequency in sorted(defect_frequencies)]
    plucker_resultant = root_product(plucker_poly, roots, q)
    tail_support_resultant = root_product(tail_poly, defect_roots, q)
    selector_ok = selector_exact_tail_size(q, block_len, tail_dim, defect_frequencies)
    full_rank = rank_mod_q(rows, q)
    selected_rank = rank_mod_q(selected, q)
    selected_dim = len(selected[0])
    predicted = plucker_resultant != 0 and tail_support_resultant != 0 and selector_ok
    selected_basis = full_rank == selected_rank == selected_dim == len(rows)
    return ResultantGateCase(
        label=label,
        q=q,
        block_len=block_len,
        tail_dim=tail_dim,
        defect_count=len(defect_frequencies),
        full_rank=full_rank,
        selected_rank=selected_rank,
        selected_dim=selected_dim,
        plucker_resultant_nonzero=plucker_resultant != 0,
        tail_support_resultant_nonzero=tail_support_resultant != 0,
        selector_has_exact_tail_size=selector_ok,
        resultant_gate_predicts_basis=predicted,
        selected_basis=selected_basis,
        omitted_support_kernel_dim=full_rank - selected_rank,
    )


def print_case(case: ResultantGateCase) -> None:
    print(
        f"case={case.label} q={case.q} block_len={case.block_len} "
        f"tail_dim={case.tail_dim} defect_count={case.defect_count} "
        f"full_rank={case.full_rank} selected_rank={case.selected_rank} "
        f"selected_dim={case.selected_dim} "
        f"plucker_resultant_nonzero={int(case.plucker_resultant_nonzero)} "
        f"tail_support_resultant_nonzero={int(case.tail_support_resultant_nonzero)} "
        f"selector_has_exact_tail_size={int(case.selector_has_exact_tail_size)} "
        f"resultant_gate_predicts_basis={int(case.resultant_gate_predicts_basis)} "
        f"selected_basis={int(case.selected_basis)} "
        f"omitted_support_kernel_dim={case.omitted_support_kernel_dim}"
    )


def main() -> None:
    q = 101
    block_len = 5
    tail_dim = 3
    defects = {0, 1, 3}
    roots = root_values(q, block_len)

    good_plucker = [1, 2, 1]  # (x+1)^2, nonzero on the 5th roots in F_101.
    good_tail = [2, 5]
    bad_plucker = [(-roots[2]) % q, 1]
    bad_tail = [(-roots[1]) % q, 1]

    rows = [
        analyze_case(
            "resultant_packaged_frequency_gate",
            q,
            block_len,
            tail_dim,
            defects,
            good_plucker,
            good_tail,
        ),
        analyze_case(
            "plucker_resultant_zero_control",
            q,
            block_len,
            tail_dim,
            defects,
            bad_plucker,
            good_tail,
        ),
        analyze_case(
            "tail_support_resultant_zero_control",
            q,
            block_len,
            tail_dim,
            defects,
            good_plucker,
            bad_tail,
        ),
        analyze_case(
            "defect_selector_size_mismatch_control",
            q,
            block_len,
            tail_dim,
            {0, 1, 2, 3},
            good_plucker,
            good_tail,
        ),
    ]

    print("Trace-GCD RS-tail frequency resultant gate toy")
    for row in rows:
        print_case(row)
    print("p24")
    print("  p24_frequency_count=35")
    print("  p24_tail_defect_count=16")
    print("  p24_local_plucker_checks_to_package=35")
    print("  p24_tail_residue_checks_to_package=16")
    print("interpretation")
    print("  frequency_resultants_package_all_local_gates=1")
    print("  plucker_resultant_zero_gives_ordinary_frequency_failure=1")
    print("  tail_support_resultant_zero_gives_defect_residue_failure=1")
    print("  defect_selector_size_mismatch_rejected=1")
    print("  resultant_gate_reduces_35_local_checks_to_global_cyclic_units=1")
    print("  p24_needs_cm_identification_of_plucker_tail_selector_sections=1")
    print("conclusion=reported_trace_gcd_rs_tail_frequency_resultant_gate_toy")

    good, bad_plucker_row, bad_tail_row, bad_selector = rows
    if (
        not good.selected_basis
        or not good.resultant_gate_predicts_basis
        or bad_plucker_row.selected_basis
        or bad_plucker_row.resultant_gate_predicts_basis
        or bad_tail_row.selected_basis
        or bad_tail_row.resultant_gate_predicts_basis
        or bad_selector.selected_basis
        or bad_selector.resultant_gate_predicts_basis
        or bad_plucker_row.omitted_support_kernel_dim == 0
        or bad_tail_row.omitted_support_kernel_dim == 0
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
