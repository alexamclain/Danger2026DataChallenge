#!/usr/bin/env python3
"""General affine normal form for products of the four p25 legal rows."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
ROW_NAMES = ("m1", "m2", "m4", "m8")
ZERO_BASIS = {
    "q2_1": (-1, 1, 0, 0),
    "q4_1": (-1, 0, 1, 0),
    "q8_1": (-1, 0, 0, 1),
}


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
class NormalForm:
    vector: tuple[int, int, int, int]
    target_index: int
    coeff_sum: int
    quotient_vector: tuple[int, int, int, int]
    quotient_coordinates: tuple[int, int, int]
    scalar_gcd: int
    decision: str

    @property
    def target_name(self) -> str:
        return ROW_NAMES[self.target_index]


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "row_value_reconstruction_basis",
        "evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
        "p25_v2_row_value_reconstruction_basis_rows=1/1",
    ),
    EvidenceMarker(
        "common_scalar_anchor_filter",
        "evidence/p25_v2_common_scalar_anchor_filter_20260617.md",
        "p25_v2_common_scalar_anchor_filter_rows=1/1",
    ),
    EvidenceMarker(
        "basis_sensitive_anchor_sieve",
        "evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md",
        "p25_v2_basis_sensitive_anchor_sieve_rows=1/1",
    ),
    EvidenceMarker(
        "zero_lattice_transfer_contract",
        "evidence/p25_v2_zero_lattice_transfer_contract_20260616.md",
        "p25_v2_zero_lattice_transfer_contract_rows=1/1",
    ),
    EvidenceMarker(
        "affine_row_product_classifier",
        "evidence/p25_v2_affine_row_product_classifier_20260617.md",
        "p25_v2_affine_row_product_classifier_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
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


def sub(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def zero_lattice_coordinates(vector: tuple[int, int, int, int]) -> tuple[int, int, int] | None:
    if sum(vector) != 0:
        return None
    # vector = a*q2_1 + b*q4_1 + c*q8_1 = (-a-b-c, a, b, c)
    a, b, c = vector[1], vector[2], vector[3]
    if (-a - b - c, a, b, c) != vector:
        return None
    return (a, b, c)


def normal_form(vector: tuple[int, int, int, int], target_index: int) -> NormalForm:
    coeff_sum = sum(vector)
    quotient_vector = sub(vector, scale(coeff_sum, unit(target_index)))
    quotient_coordinates = zero_lattice_coordinates(quotient_vector)
    if quotient_coordinates is None:
        raise ValueError(f"non-zero-lattice quotient for {vector} -> {target_index}")

    scalar_gcd = gcd(coeff_sum, PM1)
    if coeff_sum == 0:
        decision = "transfer_only"
    elif scalar_gcd == 1 and quotient_vector == (0, 0, 0, 0):
        decision = "direct_row_power"
    elif scalar_gcd == 1:
        decision = "matched_quotient_then_inverse_power"
    else:
        decision = "matched_quotient_still_root_debt"

    return NormalForm(
        vector=vector,
        target_index=target_index,
        coeff_sum=coeff_sum,
        quotient_vector=quotient_vector,
        quotient_coordinates=quotient_coordinates,
        scalar_gcd=scalar_gcd,
        decision=decision,
    )


def sample_forms() -> tuple[NormalForm, ...]:
    return tuple(
        normal_form(vector, target_index)
        for vector in product(range(-2, 3), repeat=4)
        for target_index in range(4)
    )


def main() -> int:
    examples = {
        "direct_unit_row": normal_form((1, 0, 0, 0), 0),
        "row_labeled_power_75": normal_form((75, 0, 0, 0), 0),
        "unit_sum_nonedge_minus_q": normal_form((2, -1, 0, 0), 0),
        "unit_power_nonedge_plus_q": normal_form((2, 1, 0, 0), 0),
        "zero_lattice_quotient": normal_form((-1, 1, 0, 0), 0),
        "nonunit_pair_sum": normal_form((1, 1, 0, 0), 0),
        "all_four_product": normal_form((1, 1, 1, 1), 0),
    }
    expected_examples = {
        "direct_unit_row": ("direct_row_power", (0, 0, 0), 1),
        "row_labeled_power_75": ("direct_row_power", (0, 0, 0), 1),
        "unit_sum_nonedge_minus_q": ("matched_quotient_then_inverse_power", (-1, 0, 0), 1),
        "unit_power_nonedge_plus_q": ("matched_quotient_then_inverse_power", (1, 0, 0), 1),
        "zero_lattice_quotient": ("transfer_only", (1, 0, 0), PM1),
        "nonunit_pair_sum": ("matched_quotient_still_root_debt", (1, 0, 0), 2),
        "all_four_product": ("matched_quotient_still_root_debt", (1, 1, 1), 4),
    }

    forms = sample_forms()
    decision_counts = {decision: 0 for decision in {
        "direct_row_power",
        "matched_quotient_then_inverse_power",
        "matched_quotient_still_root_debt",
        "transfer_only",
    }}
    for form in forms:
        decision_counts[form.decision] += 1

    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    current_matched_zero_lattice_packets = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    overall_ok = (
        P25 % 8 == 5
        and markers_ok == len(EVIDENCE_MARKERS)
        and len(forms) == 2500
        and all(zero_lattice_coordinates(form.quotient_vector) is not None for form in forms)
        and decision_counts == {
            "direct_row_power": 8,
            "matched_quotient_then_inverse_power": 1240,
            "matched_quotient_still_root_debt": 912,
            "transfer_only": 340,
        }
        and all(
            (
                form.decision,
                form.quotient_coordinates,
                form.scalar_gcd,
            )
            == expected_examples[name]
            for name, form in examples.items()
        )
        and current_matched_zero_lattice_packets == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 affine row normal form")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("zero_lattice_basis")
    for name, vector in ZERO_BASIS.items():
        print(f"  {name}={vector}")
    print("examples")
    for name, form in examples.items():
        print(
            f"  {name}: vector={form.vector} target={form.target_name} "
            f"s={form.coeff_sum} q={form.quotient_vector} "
            f"q_coords={form.quotient_coordinates} gcd={form.scalar_gcd} "
            f"decision={form.decision}"
        )
    print("sample_counts")
    print("  vectors=625")
    print(f"  target_normal_forms={len(forms)}")
    for decision in sorted(decision_counts):
        print(f"  {decision}={decision_counts[decision]}")
    print(f"current_matched_zero_lattice_packets={current_matched_zero_lattice_packets}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"p25_v2_affine_row_normal_form_rows={1 if overall_ok else 0}/1")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
