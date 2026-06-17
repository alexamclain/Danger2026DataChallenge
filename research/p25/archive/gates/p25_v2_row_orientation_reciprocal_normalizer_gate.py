#!/usr/bin/env python3
"""Orientation and reciprocal normalizer for the p25 support-156 rows.

The row-orbit normalizer handles oriented legal rows under the doubling
subgroup. This gate adds the adjacent orientation fact: every unit outside the
doubling subgroup maps the canonical row to the reciprocal of a legal row.
That is useful for source intake, but it is not an oriented-row close unless
the snippet also supplies the reciprocal/boundary sign convention.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import gcd
from pathlib import Path


MODULUS = 39
LEVEL_LIFT = 13
CANONICAL_POSITIVE = (7, 17, 23, 34, 37, 38)
CANONICAL_NEGATIVE = (4, 8, 10, 11, 20, 25)
LEGAL_ROWS = {
    1: ((7, 17, 23, 34, 37, 38), (4, 8, 10, 11, 20, 25)),
    2: ((7, 14, 29, 34, 35, 37), (1, 8, 11, 16, 20, 22)),
    4: ((14, 19, 28, 29, 31, 35), (1, 2, 5, 16, 22, 32)),
    8: ((17, 19, 23, 28, 31, 38), (2, 4, 5, 10, 25, 32)),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class UnitOrientation:
    unit: int
    orientation: str
    normalized_representative: int
    positive: tuple[int, ...]
    negative: tuple[int, ...]
    payload_sha256: str
    row_ok: bool


@dataclass(frozen=True)
class OrientationDecision:
    name: str
    unit: int | None
    supplied_orientation: str
    normalized_representative: int | None
    decision: str
    source_candidate_if_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RowOrientationReciprocalNormalizer:
    evidence_markers: tuple[EvidenceMarker, ...]
    oriented_units: tuple[int, ...]
    reciprocal_units: tuple[int, ...]
    orientation_rows: tuple[UnitOrientation, ...]
    decisions: tuple[OrientationDecision, ...]
    evidence_markers_ok: int
    oriented_unit_count: int
    reciprocal_unit_count: int
    unclassified_unit_count: int
    source_candidate_shapes: int
    repair_rows: int
    reject_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def units_mod39() -> tuple[int, ...]:
    return tuple(value for value in range(1, MODULUS) if gcd(value, MODULUS) == 1)


def multiply(residues: tuple[int, ...], unit: int) -> tuple[int, ...]:
    return tuple(sorted((unit * residue) % MODULUS for residue in residues))


def lifted_entries(residues: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(
        sorted(residue + MODULUS * lift for residue in residues for lift in range(LEVEL_LIFT))
    )


def payload_hash(positive: tuple[int, ...], negative: tuple[int, ...]) -> str:
    lines: list[str] = []
    for entry in lifted_entries(positive):
        lines.append(f"{entry}\t6")
    for entry in lifted_entries(negative):
        lines.append(f"{entry}\t-6")
    return sha256(("\n".join(sorted(lines)) + "\n").encode()).hexdigest()


def classify_unit(unit: int) -> UnitOrientation | None:
    positive = multiply(CANONICAL_POSITIVE, unit)
    negative = multiply(CANONICAL_NEGATIVE, unit)
    for representative, (row_positive, row_negative) in LEGAL_ROWS.items():
        if positive == row_positive and negative == row_negative:
            return UnitOrientation(
                unit=unit,
                orientation="oriented",
                normalized_representative=representative,
                positive=positive,
                negative=negative,
                payload_sha256=payload_hash(positive, negative),
                row_ok=True,
            )
        if positive == row_negative and negative == row_positive:
            return UnitOrientation(
                unit=unit,
                orientation="reciprocal",
                normalized_representative=representative,
                positive=positive,
                negative=negative,
                payload_sha256=payload_hash(positive, negative),
                row_ok=True,
            )
    return None


def orientation_rows() -> tuple[UnitOrientation, ...]:
    rows = tuple(classify_unit(unit) for unit in units_mod39())
    return tuple(row for row in rows if row is not None)


def decisions() -> tuple[OrientationDecision, ...]:
    return (
        OrientationDecision(
            name="oriented_legal_row_m1",
            unit=1,
            supplied_orientation="oriented",
            normalized_representative=1,
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="finite value/divisor theorem plus downstream framing",
            ok=True,
        ),
        OrientationDecision(
            name="stabilizer_oriented_m16",
            unit=16,
            supplied_orientation="oriented",
            normalized_representative=1,
            decision="normalize_to_m1_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="same as normalized oriented m=1 row",
            ok=True,
        ),
        OrientationDecision(
            name="outside_unit_m7_orientation_unspecified",
            unit=7,
            supplied_orientation="unspecified",
            normalized_representative=8,
            decision="repair_reciprocal_orientation_or_boundary_sign_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="explicit reciprocal orientation and -Norm_156 boundary, or rewrite as the oriented legal row",
            ok=True,
        ),
        OrientationDecision(
            name="reciprocal_m8_with_minus_boundary",
            unit=7,
            supplied_orientation="reciprocal_minus_boundary",
            normalized_representative=8,
            decision="normalize_reciprocal_to_m8_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="same theorem data after reciprocal/orientation normalization",
            ok=True,
        ),
        OrientationDecision(
            name="reciprocal_row_with_plus_boundary",
            unit=7,
            supplied_orientation="reciprocal_plus_boundary",
            normalized_representative=8,
            decision="reject_orientation_boundary_mismatch",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="reciprocal product should carry the opposite Hilbert-90 boundary sign",
            ok=True,
        ),
        OrientationDecision(
            name="orientationless_product_hash",
            unit=None,
            supplied_orientation="unknown",
            normalized_representative=None,
            decision="repair_product_orientation_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="oriented product row or reciprocal row with boundary sign",
            ok=True,
        ),
    )


def build_normalizer() -> RowOrientationReciprocalNormalizer:
    markers = evidence_markers()
    rows = orientation_rows()
    oriented = tuple(row.unit for row in rows if row.orientation == "oriented")
    reciprocal = tuple(row.unit for row in rows if row.orientation == "reciprocal")
    unclassified = len(units_mod39()) - len(rows)
    decision_rows = decisions()
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    repair_count = sum(row.decision.startswith("repair_") for row in decision_rows)
    reject_count = sum(row.decision.startswith("reject_") for row in decision_rows)
    current_closers = 0
    markers_ok = sum(row.ok for row in markers)
    expected_oriented = (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)
    expected_reciprocal = (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)
    expected_decisions = (
        "source_stage_candidate_if_theorem_present",
        "normalize_to_m1_then_apply_source_snippet_intake",
        "repair_reciprocal_orientation_or_boundary_sign_missing",
        "normalize_reciprocal_to_m8_then_apply_source_snippet_intake",
        "reject_orientation_boundary_mismatch",
        "repair_product_orientation_missing",
    )
    row_ok = (
        markers_ok == len(markers)
        and oriented == expected_oriented
        and reciprocal == expected_reciprocal
        and unclassified == 0
        and len(rows) == 24
        and all(row.row_ok for row in rows)
        and classify_unit(7) is not None
        and classify_unit(7).orientation == "reciprocal"  # type: ignore[union-attr]
        and classify_unit(7).normalized_representative == 8  # type: ignore[union-attr]
        and classify_unit(38) is not None
        and classify_unit(38).orientation == "reciprocal"  # type: ignore[union-attr]
        and classify_unit(38).normalized_representative == 4  # type: ignore[union-attr]
        and len(decision_rows) == 6
        and source_candidates == 3
        and repair_count == 2
        and reject_count == 1
        and current_closers == 0
        and tuple(row.decision for row in decision_rows) == expected_decisions
        and all(row.ok for row in decision_rows)
    )
    return RowOrientationReciprocalNormalizer(
        evidence_markers=markers,
        oriented_units=oriented,
        reciprocal_units=reciprocal,
        orientation_rows=rows,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        oriented_unit_count=len(oriented),
        reciprocal_unit_count=len(reciprocal),
        unclassified_unit_count=unclassified,
        source_candidate_shapes=source_candidates,
        repair_rows=repair_count,
        reject_rows=reject_count,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    normalizer = build_normalizer()
    for marker_row in normalizer.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("orientation_summary")
    print(f"  oriented_units={normalizer.oriented_units}")
    print(f"  reciprocal_units={normalizer.reciprocal_units}")
    print(f"  unclassified_unit_count={normalizer.unclassified_unit_count}")
    print("unit_orientation_rows")
    for row in normalizer.orientation_rows:
        print(
            "  "
            f"unit={row.unit} orientation={row.orientation} "
            f"normalized_m={row.normalized_representative} sha256={row.payload_sha256}"
        )
    print("orientation_decisions")
    for row in normalizer.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} unit={row.unit} "
            f"orientation={row.supplied_orientation} normalized_m={row.normalized_representative} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(
        f"  evidence_markers_ok={normalizer.evidence_markers_ok}/"
        f"{len(normalizer.evidence_markers)}"
    )
    print(f"  oriented_unit_count={normalizer.oriented_unit_count}")
    print(f"  reciprocal_unit_count={normalizer.reciprocal_unit_count}")
    print(f"  source_candidate_shapes={normalizer.source_candidate_shapes}")
    print(f"  repair_rows={normalizer.repair_rows}")
    print(f"  reject_rows={normalizer.reject_rows}")
    print(f"  current_source_stage_closers={normalizer.current_source_stage_closers}")
    print("interpretation")
    print("  outside_doubling_units_are_reciprocal_presentations_not_oriented_rows=1")
    print("  reciprocal_rows_need_explicit_boundary_sign_or_oriented_rewrite=1")
    print("  current_source_stage_closers_remain_zero=1")
    print(f"p25_v2_row_orientation_reciprocal_normalizer_rows={int(normalizer.row_ok)}/1")
    return 0 if normalizer.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
