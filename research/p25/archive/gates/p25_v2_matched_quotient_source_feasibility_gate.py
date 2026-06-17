#!/usr/bin/env python3
"""Classify source-family aggregate shapes against matched-quotient intake."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
MARKER = "p25_v2_matched_quotient_source_feasibility_rows=1/1"
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
class SourceShape:
    name: str
    source_family: str
    vector: tuple[int, int, int, int] | None
    target_index: int
    matched_quotient_supplied: bool
    finite_payload_supplied: bool
    arithmetic_source_supplied: bool
    decision: str
    first_missing_or_falsifier: str

    @property
    def coefficient_sum(self) -> int | None:
        return None if self.vector is None else sum(self.vector)

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
        "distribution_relation_closure_screen",
        "evidence/p25_v2_distribution_relation_closure_screen_20260617.md",
        "p25_v2_distribution_relation_closure_screen_rows=1/1",
    ),
    EvidenceMarker(
        "external_distribution_relation_scout",
        "evidence/p25_v2_external_distribution_relation_scout_20260617.md",
        "p25_v2_external_distribution_relation_scout_rows=1/1",
    ),
    EvidenceMarker(
        "koo_shin_distribution_noncloser",
        "evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
        "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
    ),
    EvidenceMarker(
        "theorem52_constant_span_obstruction",
        "evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
        "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
    ),
    EvidenceMarker(
        "affine_row_normal_form",
        "evidence/p25_v2_affine_row_normal_form_20260617.md",
        "p25_v2_affine_row_normal_form_rows=1/1",
    ),
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
)


def unit(index: int) -> tuple[int, int, int, int]:
    return tuple(1 if i == index else 0 for i in range(4))


def sub(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(left[i] - right[i] for i in range(4))


def scale(c: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(c * value for value in vector)


def matched_quotient(vector: tuple[int, int, int, int], target_index: int) -> tuple[int, int, int, int]:
    return sub(vector, scale(sum(vector), unit(target_index)))


def zero_lattice(vector: tuple[int, int, int, int] | None) -> bool:
    return vector is not None and sum(vector) == 0


def source_shapes() -> tuple[SourceShape, ...]:
    return (
        SourceShape(
            name="direct_edge_baseline",
            source_family="current_kernel",
            vector=(1, 0, 0, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="direct_current_kernel_if_source_theorem_present",
            first_missing_or_falsifier="current source theorem not in hand",
        ),
        SourceShape(
            name="unit_sum_affine_packet",
            source_family="nonstandard_affine_aggregate",
            vector=(2, -1, 0, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="viable_matched_quotient_packet_if_source_supplies_both",
            first_missing_or_falsifier="no known source emits both the affine aggregate and matched quotient",
        ),
        SourceShape(
            name="unit_power_affine_packet",
            source_family="nonstandard_affine_aggregate",
            vector=(2, 1, 0, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="viable_matched_quotient_packet_if_source_supplies_both",
            first_missing_or_falsifier="no known source emits both the affine aggregate and matched quotient",
        ),
        SourceShape(
            name="standard_vertex_pair_with_quotient",
            source_family="distribution_vertex_sum",
            vector=(1, 1, 0, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="repair_even_sum_root_debt",
            first_missing_or_falsifier="matched quotient recovers R_m^2, so oriented square root is still missing",
        ),
        SourceShape(
            name="standard_diagonal_pair_with_quotient",
            source_family="distribution_diagonal_sum",
            vector=(1, 0, 1, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="repair_even_sum_root_debt",
            first_missing_or_falsifier="matched quotient recovers R_m^2, so oriented square root is still missing",
        ),
        SourceShape(
            name="all_four_norm_with_zero_basis",
            source_family="distribution_all_four_norm",
            vector=(1, 1, 1, 1),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="repair_fourth_root_debt",
            first_missing_or_falsifier="matched quotient recovers R_m^4, so selected fourth root is still missing",
        ),
        SourceShape(
            name="aggregate_only_distribution",
            source_family="generic_distribution_relation",
            vector=(1, 1, 0, 0),
            target_index=0,
            matched_quotient_supplied=False,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="repair_matched_zero_lattice_value_missing",
            first_missing_or_falsifier="aggregate theorem alone leaves zero-lattice debt unpaid",
        ),
        SourceShape(
            name="quotient_only_zero_lattice",
            source_family="boundary_zero_relation",
            vector=(-1, 1, 0, 0),
            target_index=0,
            matched_quotient_supplied=True,
            finite_payload_supplied=True,
            arithmetic_source_supplied=True,
            decision="transfer_only_not_first_anchor",
            first_missing_or_falsifier="coefficient sum zero cannot create the first absolute row value",
        ),
        SourceShape(
            name="koo_shin_constant_span",
            source_family="koo_shin_theorem52",
            vector=None,
            target_index=0,
            matched_quotient_supplied=False,
            finite_payload_supplied=False,
            arithmetic_source_supplied=True,
            decision="reject_constant_span_not_current_target",
            first_missing_or_falsifier="legal quotient-C4 span has no nonzero constant vector",
        ),
        SourceShape(
            name="external_distribution_cluster",
            source_family="external_distribution_relations",
            vector=None,
            target_index=0,
            matched_quotient_supplied=False,
            finite_payload_supplied=False,
            arithmetic_source_supplied=True,
            decision="support_framework_not_finite_matched_packet",
            first_missing_or_falsifier="no p25 row label, matched quotient theorem, scalar-fixed finite payload, or boundary bridge",
        ),
    )


def shape_ok(shape: SourceShape) -> bool:
    if shape.vector is None:
        return shape.decision in {
            "reject_constant_span_not_current_target",
            "support_framework_not_finite_matched_packet",
        }
    q = matched_quotient(shape.vector, shape.target_index)
    s = shape.coefficient_sum
    if shape.name == "direct_edge_baseline":
        return q == (0, 0, 0, 0) and s == 1
    if shape.decision == "viable_matched_quotient_packet_if_source_supplies_both":
        return (
            shape.matched_quotient_supplied
            and zero_lattice(q)
            and s is not None
            and gcd(s, PM1) == 1
        )
    if shape.decision == "repair_even_sum_root_debt":
        return shape.matched_quotient_supplied and s == 2 and gcd(s, PM1) == 2
    if shape.decision == "repair_fourth_root_debt":
        return shape.matched_quotient_supplied and s == 4 and gcd(s, PM1) == 4
    if shape.decision == "repair_matched_zero_lattice_value_missing":
        return not shape.matched_quotient_supplied and s == 2
    if shape.decision == "transfer_only_not_first_anchor":
        return s == 0 and zero_lattice(shape.vector)
    return False


def main() -> int:
    markers_ok = sum(marker.ok for marker in EVIDENCE_MARKERS)
    shapes = source_shapes()
    viable = sum(shape.decision == "viable_matched_quotient_packet_if_source_supplies_both" for shape in shapes)
    root_debt = sum(shape.decision in {"repair_even_sum_root_debt", "repair_fourth_root_debt"} for shape in shapes)
    missing_quotient = sum(shape.decision == "repair_matched_zero_lattice_value_missing" for shape in shapes)
    transfer_only = sum(shape.decision == "transfer_only_not_first_anchor" for shape in shapes)
    reject_rows = sum(shape.decision.startswith("reject") for shape in shapes)
    support_rows = sum(shape.decision.startswith("support") for shape in shapes)
    current_viable_source_packets_in_hand = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        markers_ok == len(EVIDENCE_MARKERS)
        and len(shapes) == 10
        and viable == 2
        and root_debt == 3
        and missing_quotient == 1
        and transfer_only == 1
        and reject_rows == 1
        and support_rows == 1
        and all(shape_ok(shape) for shape in shapes)
        and current_viable_source_packets_in_hand == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 matched-quotient source feasibility")
    print(f"p={P25}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print("source_shapes")
    for shape in shapes:
        q = matched_quotient(shape.vector, shape.target_index) if shape.vector is not None else "n/a"
        s = shape.coefficient_sum if shape.coefficient_sum is not None else "n/a"
        gcd_s = gcd(shape.coefficient_sum, PM1) if shape.coefficient_sum not in (None, 0) else "n/a"
        print(f"  {shape.name}: family={shape.source_family} decision={shape.decision}")
        print(f"    vector={shape.vector if shape.vector is not None else 'n/a'} target={shape.target_name}")
        print(f"    coefficient_sum={s} gcd_sum_pminus1={gcd_s}")
        print(f"    matched_quotient={q} supplied={int(shape.matched_quotient_supplied)}")
        print(f"    first_missing_or_falsifier={shape.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={markers_ok}/{len(EVIDENCE_MARKERS)}")
    print(f"source_shapes={len(shapes)}")
    print(f"viable_matched_packet_shapes={viable}")
    print(f"root_debt_standard_aggregate_rows={root_debt}")
    print(f"missing_quotient_rows={missing_quotient}")
    print(f"transfer_only_rows={transfer_only}")
    print(f"reject_rows={reject_rows}")
    print(f"support_rows={support_rows}")
    print(f"current_viable_source_packets_in_hand={current_viable_source_packets_in_hand}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"{MARKER if row_ok else 'p25_v2_matched_quotient_source_feasibility_rows=0/1'}")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
