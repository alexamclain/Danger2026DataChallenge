#!/usr/bin/env python3
"""Normalize the four legal support-156 p25 product rows.

The unified H0/conductor-39 target has four displayed rows.  This gate records
the precise doubling-orbit action behind them so source snippets can be
normalized before review: a theorem for one legal normalized row is enough for
the first-pass source ask, while multipliers outside the doubling orbit are a
new claim rather than a presentation of the current target.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from math import gcd
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)


MODULUS = 39
LEVEL = 507
LIFT_LENGTH = 13
LEGAL_REPRESENTATIVES = (1, 2, 4, 8)
STABILIZER = (1, 16, 22)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OrbitClass:
    representative: int
    units: tuple[int, ...]
    positive_mod39: tuple[int, ...]
    negative_mod39: tuple[int, ...]
    payload_sha256: str
    units_all_match_representative: bool
    row_ok: bool


@dataclass(frozen=True)
class NormalizationClaim:
    name: str
    multiplier: int | None
    normalized_representative: int | None
    decision: str
    closes_source_stage_if_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RowOrbitNormalization:
    evidence_markers: tuple[EvidenceMarker, ...]
    unit_count_mod39: int
    doubling_subgroup: tuple[int, ...]
    doubling_subgroup_size: int
    stabilizer: tuple[int, ...]
    legal_representatives: tuple[int, ...]
    orbit_classes: tuple[OrbitClass, ...]
    outside_doubling_units: tuple[int, ...]
    outside_units_matching_legal_rows: int
    all_legal_units: tuple[int, ...]
    legal_unit_actions: int
    claims: tuple[NormalizationClaim, ...]
    evidence_markers_ok: int
    orbit_classes_ok: int
    source_stage_candidate_shapes: int
    repair_rows: int
    reject_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_target",
            "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
            "p25_v2_h0_conductor39_unified_target_rows=1/1",
        ),
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def units_mod39() -> tuple[int, ...]:
    return tuple(value for value in range(1, MODULUS) if gcd(value, MODULUS) == 1)


def doubling_subgroup() -> tuple[int, ...]:
    values: list[int] = []
    value = 1
    while value not in values:
        values.append(value)
        value = (value * 2) % MODULUS
    return tuple(sorted(values))


def multiply_residues(residues: tuple[int, ...], unit: int) -> tuple[int, ...]:
    return tuple(sorted((residue * unit) % MODULUS for residue in residues))


def lifted_entries(residues: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(residue + MODULUS * k_value for residue in residues for k_value in range(LIFT_LENGTH)))


def payload_hash(positive: tuple[int, ...], negative: tuple[int, ...]) -> str:
    lines: list[str] = []
    for entry in lifted_entries(positive):
        lines.append(f"{entry}\t6")
    for entry in lifted_entries(negative):
        lines.append(f"{entry}\t-6")
    return sha256(("\n".join(sorted(lines)) + "\n").encode()).hexdigest()


def coset_for_representative(representative: int) -> tuple[int, ...]:
    return tuple(sorted((representative * unit) % MODULUS for unit in STABILIZER))


def normalize_multiplier(multiplier: int) -> int | None:
    for representative in LEGAL_REPRESENTATIVES:
        if multiplier % MODULUS in coset_for_representative(representative):
            return representative
    return None


def build_orbit_classes(product) -> tuple[OrbitClass, ...]:
    rows_by_multiplier = {
        row.multiplier_from_canonical: row for row in product.legal_rows
    }
    canonical = rows_by_multiplier[1]
    classes: list[OrbitClass] = []
    for representative in LEGAL_REPRESENTATIVES:
        row = rows_by_multiplier[representative]
        units = coset_for_representative(representative)
        all_match = all(
            multiply_residues(canonical.source_positive_residues, unit) == row.source_positive_residues
            and multiply_residues(canonical.source_negative_residues, unit) == row.source_negative_residues
            for unit in units
        )
        digest = payload_hash(row.source_positive_residues, row.source_negative_residues)
        row_ok = (
            all_match
            and digest
            and row.lifted_positive_count == 78
            and row.lifted_negative_count == 78
            and row.lifted_support == 156
            and row.boundary_equals_period_norm
            and row.row_ok
        )
        classes.append(
            OrbitClass(
                representative=representative,
                units=units,
                positive_mod39=row.source_positive_residues,
                negative_mod39=row.source_negative_residues,
                payload_sha256=digest,
                units_all_match_representative=all_match,
                row_ok=row_ok,
            )
        )
    return tuple(classes)


def claim_rows() -> tuple[NormalizationClaim, ...]:
    return (
        NormalizationClaim(
            name="exact_legal_row_m1",
            multiplier=1,
            normalized_representative=normalize_multiplier(1),
            decision="source_stage_candidate_if_theorem_present",
            closes_source_stage_if_theorem_present=True,
            first_missing_or_falsifier="finite value/divisor theorem plus DANGER3 framing",
            ok=True,
        ),
        NormalizationClaim(
            name="stabilizer_equivalent_m16",
            multiplier=16,
            normalized_representative=normalize_multiplier(16),
            decision="normalize_to_m1_then_apply_source_snippet_intake",
            closes_source_stage_if_theorem_present=True,
            first_missing_or_falsifier="same as normalized m=1 row",
            ok=True,
        ),
        NormalizationClaim(
            name="doubling_coset_m32",
            multiplier=32,
            normalized_representative=normalize_multiplier(32),
            decision="normalize_to_m2_then_apply_source_snippet_intake",
            closes_source_stage_if_theorem_present=True,
            first_missing_or_falsifier="same as normalized m=2 row",
            ok=True,
        ),
        NormalizationClaim(
            name="outside_doubling_unit_m7",
            multiplier=7,
            normalized_representative=normalize_multiplier(7),
            decision="reject_not_current_legal_four_row_target",
            closes_source_stage_if_theorem_present=False,
            first_missing_or_falsifier="one of the four normalized support-156 rows or a new theorem target",
            ok=True,
        ),
        NormalizationClaim(
            name="all_four_rows_required",
            multiplier=None,
            normalized_representative=None,
            decision="repair_overdemand_one_legal_row_is_enough_for_source_stage",
            closes_source_stage_if_theorem_present=False,
            first_missing_or_falsifier="only one normalized legal row is required by the first-pass ask",
            ok=True,
        ),
        NormalizationClaim(
            name="one_row_without_boundary",
            multiplier=8,
            normalized_representative=normalize_multiplier(8),
            decision="repair_boundary_or_theorem_missing",
            closes_source_stage_if_theorem_present=False,
            first_missing_or_falsifier="Norm_156(Y_507) boundary and finite value/divisor theorem",
            ok=True,
        ),
    )


def build_normalization() -> RowOrbitNormalization:
    markers = evidence_markers()
    product = profile_sparse_h90_product_normal_form()
    unit_values = units_mod39()
    subgroup = doubling_subgroup()
    orbit_classes = build_orbit_classes(product)
    legal_units = tuple(sorted(unit for row in orbit_classes for unit in row.units))
    legal_products = {
        (row.positive_mod39, row.negative_mod39)
        for row in orbit_classes
    }
    canonical = {row.multiplier_from_canonical: row for row in product.legal_rows}[1]
    outside = tuple(unit for unit in unit_values if unit not in legal_units)
    outside_matches = sum(
        (
            multiply_residues(canonical.source_positive_residues, unit),
            multiply_residues(canonical.source_negative_residues, unit),
        )
        in legal_products
        for unit in outside
    )
    claims = claim_rows()
    source_candidates = sum(row.closes_source_stage_if_theorem_present for row in claims)
    repairs = sum(row.decision.startswith("repair_") for row in claims)
    rejects = sum(row.decision.startswith("reject_") for row in claims)
    current_closers = 0
    markers_ok = sum(row.ok for row in markers)
    classes_ok = sum(row.row_ok for row in orbit_classes)
    row_ok = (
        markers_ok == len(markers)
        and product.row_ok
        and len(unit_values) == 24
        and subgroup == legal_units
        and len(subgroup) == 12
        and STABILIZER == product.canonical_stabilizer == (1, 16, 22)
        and LEGAL_REPRESENTATIVES == product.quotient_representatives == (1, 2, 4, 8)
        and len(orbit_classes) == 4
        and classes_ok == 4
        and len(outside) == 12
        and outside_matches == 0
        and normalize_multiplier(1) == 1
        and normalize_multiplier(16) == 1
        and normalize_multiplier(22) == 1
        and normalize_multiplier(32) == 2
        and normalize_multiplier(25) == 4
        and normalize_multiplier(20) == 8
        and normalize_multiplier(7) is None
        and len(claims) == 6
        and source_candidates == 3
        and repairs == 2
        and rejects == 1
        and current_closers == 0
        and all(row.ok for row in claims)
    )
    return RowOrbitNormalization(
        evidence_markers=markers,
        unit_count_mod39=len(unit_values),
        doubling_subgroup=subgroup,
        doubling_subgroup_size=len(subgroup),
        stabilizer=STABILIZER,
        legal_representatives=LEGAL_REPRESENTATIVES,
        orbit_classes=orbit_classes,
        outside_doubling_units=outside,
        outside_units_matching_legal_rows=outside_matches,
        all_legal_units=legal_units,
        legal_unit_actions=len(legal_units),
        claims=claims,
        evidence_markers_ok=markers_ok,
        orbit_classes_ok=classes_ok,
        source_stage_candidate_shapes=source_candidates,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_normalization()
    for row in profile.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("orbit")
    print(f"  unit_count_mod39={profile.unit_count_mod39}")
    print(f"  doubling_subgroup={profile.doubling_subgroup}")
    print(f"  doubling_subgroup_size={profile.doubling_subgroup_size}")
    print(f"  stabilizer={profile.stabilizer}")
    print(f"  legal_representatives={profile.legal_representatives}")
    print(f"  legal_unit_actions={profile.legal_unit_actions}")
    print(f"  outside_doubling_units={profile.outside_doubling_units}")
    print(f"  outside_units_matching_legal_rows={profile.outside_units_matching_legal_rows}")
    print("orbit_classes")
    for row in profile.orbit_classes:
        print(
            "  "
            f"m={row.representative} units={row.units} "
            f"pos={row.positive_mod39} neg={row.negative_mod39} "
            f"sha256={row.payload_sha256} "
            f"all_match={int(row.units_all_match_representative)} ok={int(row.row_ok)}"
        )
    print("claim_rows")
    for row in profile.claims:
        print(
            "  "
            f"{row.name}: multiplier={row.multiplier} "
            f"normalized={row.normalized_representative} decision={row.decision} "
            f"candidate_if_theorem={int(row.closes_source_stage_if_theorem_present)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}/{len(profile.evidence_markers)}")
    print(f"  orbit_classes_ok={profile.orbit_classes_ok}/{len(profile.orbit_classes)}")
    print(f"  source_stage_candidate_shapes={profile.source_stage_candidate_shapes}")
    print(f"  repair_rows={profile.repair_rows}")
    print(f"  reject_rows={profile.reject_rows}")
    print(f"  current_source_stage_closers={profile.current_source_stage_closers}")
    print("interpretation")
    print("  one_normalized_legal_row_is_enough_for_the_first_pass_source_ask=1")
    print("  stabilizer_equivalent_multipliers_should_be_normalized_before_snippet_intake=1")
    print("  outside_doubling_orbit_multipliers_are_new_claims_not_current_target_rows=1")
    print(f"p25_v2_row_orbit_normalization_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
