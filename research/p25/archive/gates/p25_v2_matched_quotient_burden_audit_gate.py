#!/usr/bin/env python3
"""Audit the source-theorem burden of matched-quotient aggregate packets."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_matched_quotient_burden_audit_rows=1/1"
ROW_NAMES = ("m1", "m2", "m4", "m8")


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


@dataclass(frozen=True)
class BurdenRow:
    name: str
    vector: tuple[int, int, int, int]
    target_index: int
    matched_quotient: tuple[int, int, int, int]
    decision: str
    source_burden: str
    first_missing_or_falsifier: str

    @property
    def coefficient_sum(self) -> int:
        return sum(self.vector)

    @property
    def target_name(self) -> str:
        return ROW_NAMES[self.target_index]


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "matched_quotient_closure_packet",
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_source_feasibility",
        "evidence/p25_v2_matched_quotient_source_feasibility_20260617.md",
        "p25_v2_matched_quotient_source_feasibility_rows=1/1",
    ),
    EvidenceMarker(
        "affine_row_normal_form",
        "evidence/p25_v2_affine_row_normal_form_20260617.md",
        "p25_v2_affine_row_normal_form_rows=1/1",
    ),
    EvidenceMarker(
        "source_theorem_acceptance_automaton",
        "evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
        "p25_v2_source_theorem_acceptance_automaton_rows=1/1",
    ),
    EvidenceMarker(
        "drew_kernel_review_packet",
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
)


def unit(index: int) -> tuple[int, int, int, int]:
    return tuple(1 if i == index else 0 for i in range(4))


def scale(c: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(c * value for value in vector)


def add(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(left[i] + right[i] for i in range(4))


def sub(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def matched_quotient(vector: tuple[int, int, int, int], target_index: int) -> tuple[int, int, int, int]:
    return sub(vector, scale(sum(vector), unit(target_index)))


def zero_lattice_coordinates(vector: tuple[int, int, int, int]) -> tuple[int, int, int] | None:
    if sum(vector) != 0:
        return None
    a, b, c = vector[1], vector[2], vector[3]
    return (a, b, c) if (-a - b - c, a, b, c) == vector else None


def inverse_exponent(value: int) -> int | None:
    return pow(value, -1, PM1) if value and gcd(value, PM1) == 1 else None


def recover_row_vector(row: BurdenRow) -> tuple[int, int, int, int] | None:
    inv = inverse_exponent(row.coefficient_sum)
    if inv is None:
        return None
    return scale(inv, sub(row.vector, row.matched_quotient))


def congruent_mod_pm1(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> bool:
    return all((left[i] - right[i]) % PM1 == 0 for i in range(4))


def reduce_mod_pm1(vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(value % PM1 for value in vector)


def recover_aggregate_from_row_and_quotient(row: BurdenRow) -> tuple[int, int, int, int]:
    return add(scale(row.coefficient_sum, unit(row.target_index)), row.matched_quotient)


def burden_rows() -> tuple[BurdenRow, ...]:
    return (
        BurdenRow(
            name="unit_sum_affine_packet",
            vector=(2, -1, 0, 0),
            target_index=0,
            matched_quotient=(1, -1, 0, 0),
            decision="accepted_intake_if_both_source_theorems_exist",
            source_burden="equivalent_to_direct_row_plus_q2_1_inverse",
            first_missing_or_falsifier="no source theorem for both R1^2/R2 and R1/R2",
        ),
        BurdenRow(
            name="unit_power_affine_packet",
            vector=(2, 1, 0, 0),
            target_index=0,
            matched_quotient=(-1, 1, 0, 0),
            decision="accepted_intake_if_both_source_theorems_exist",
            source_burden="equivalent_to_direct_row_cubed_plus_q2_1",
            first_missing_or_falsifier="no source theorem for both R1^2*R2 and R2/R1",
        ),
        BurdenRow(
            name="full_zero_basis_matched_packet",
            vector=(2, 1, 1, 1),
            target_index=0,
            matched_quotient=(-3, 1, 1, 1),
            decision="accepted_intake_if_both_source_theorems_exist",
            source_burden="equivalent_to_direct_row_fifth_power_plus_full_zero_basis",
            first_missing_or_falsifier="no source theorem for aggregate plus q2_1*q4_1*q8_1",
        ),
        BurdenRow(
            name="standard_pair_with_matched_quotient",
            vector=(1, 1, 0, 0),
            target_index=0,
            matched_quotient=(-1, 1, 0, 0),
            decision="repair_root_debt_remaining",
            source_burden="not_unique_power_because_gcd_2",
            first_missing_or_falsifier="recovers R1^2, so selected square root is still missing",
        ),
        BurdenRow(
            name="all_four_norm_with_matched_quotient",
            vector=(1, 1, 1, 1),
            target_index=0,
            matched_quotient=(-3, 1, 1, 1),
            decision="repair_fourth_root_debt_remaining",
            source_burden="not_unique_power_because_gcd_4",
            first_missing_or_falsifier="recovers R1^4, so selected fourth root is still missing",
        ),
    )


def row_ok(row: BurdenRow) -> bool:
    q = matched_quotient(row.vector, row.target_index)
    if q != row.matched_quotient:
        return False
    if zero_lattice_coordinates(q) is None:
        return False
    if recover_aggregate_from_row_and_quotient(row) != row.vector:
        return False
    inv = inverse_exponent(row.coefficient_sum)
    accepted = row.decision == "accepted_intake_if_both_source_theorems_exist"
    if accepted:
        recovered = recover_row_vector(row)
        return (
            inv is not None
            and recovered is not None
            and congruent_mod_pm1(recovered, unit(row.target_index))
            and gcd(row.coefficient_sum, PM1) == 1
        )
    return inv is None and gcd(row.coefficient_sum, PM1) in {2, 4}


def main() -> int:
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    rows = burden_rows()
    accepted = sum(row.decision == "accepted_intake_if_both_source_theorems_exist" for row in rows)
    root_debt = sum("root_debt" in row.decision for row in rows)
    row_equivalent_burdens = sum(
        row.decision == "accepted_intake_if_both_source_theorems_exist"
        and recover_aggregate_from_row_and_quotient(row) == row.vector
        for row in rows
    )
    independent_matched_source_packets_in_hand = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    all_rows_ok = all(row_ok(row) for row in rows)
    row_pass = (
        markers_ok == len(EVIDENCE_MARKERS)
        and len(rows) == 5
        and accepted == 3
        and root_debt == 2
        and row_equivalent_burdens == 3
        and all_rows_ok
        and independent_matched_source_packets_in_hand == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 matched-quotient burden audit")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("rows")
    for row in rows:
        inv = inverse_exponent(row.coefficient_sum)
        print(f"  {row.name}: decision={row.decision} ok={int(row_ok(row))}")
        print(f"    vector={row.vector}")
        print(f"    target={row.target_name}")
        print(f"    coefficient_sum={row.coefficient_sum}")
        print(f"    gcd_sum_pminus1={gcd(row.coefficient_sum, PM1)}")
        print(f"    matched_quotient={row.matched_quotient}")
        print(f"    zero_lattice_coordinates={zero_lattice_coordinates(row.matched_quotient)}")
        print(f"    inverse_exponent={inv if inv is not None else 'none'}")
        recovered = recover_row_vector(row) if inv is not None else None
        print(f"    recovered_row_vector={recovered if recovered is not None else 'none'}")
        print(f"    recovered_row_vector_mod_pminus1={reduce_mod_pm1(recovered) if recovered is not None else 'none'}")
        print(f"    aggregate_from_row_plus_quotient={recover_aggregate_from_row_and_quotient(row)}")
        print(f"    source_burden={row.source_burden}")
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"burden_rows={len(rows)}")
    print(f"accepted_intake_rows={accepted}")
    print(f"root_debt_rows={root_debt}")
    print(f"row_equivalent_burdens={row_equivalent_burdens}")
    print(f"independent_matched_source_packets_in_hand={independent_matched_source_packets_in_hand}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print("interpretation")
    print("  matched_quotient_is_intake_normalizer_not_cheaper_source_theorem=1")
    print("  accepted_packets_still_require_two_exact_arithmetic_source_theorems=1")
    print("  standard_distribution_packets_retain_root_debt=1")
    print(MARKER if row_pass else "p25_v2_matched_quotient_burden_audit_rows=0/1")
    return 0 if row_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
