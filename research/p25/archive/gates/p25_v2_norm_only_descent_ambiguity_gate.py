#!/usr/bin/env python3
"""Norm-only/descent ambiguity for p25 source snippets.

The conductor-39/H0 target has a dense period norm on level 507 and four legal
support-156 Hilbert-90 preimages whose boundaries equal that norm.  A source
answer that only evaluates or identifies the dense norm has not selected one
legal preimage/product row.  This gate records that as an explicit repair row:
norm-only data must be paired with a legal Hilbert-90 descent and then with the
finite value/divisor theorem for the selected row.
"""

from __future__ import annotations

from dataclasses import dataclass
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
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (
    profile_sparse_hilbert90_yang_lift,
)
from p25_ksy_y_yang_y507_period_norm_character_gate import (
    profile_yang_y507_period_norm_character,
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class NormInvariant:
    name: str
    statement: str
    ok: bool


@dataclass(frozen=True)
class NormDecision:
    name: str
    theorem_shape: str
    decision: str
    source_candidate_if_theorem_present: bool
    normalize_then_intake: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class NormOnlyDescentAmbiguity:
    evidence_markers: tuple[EvidenceMarker, ...]
    invariants: tuple[NormInvariant, ...]
    decisions: tuple[NormDecision, ...]
    evidence_markers_ok: int
    invariants_ok: int
    source_candidate_shapes: int
    normalize_rows: int
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
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "conductor39_yang_h90_interface",
            "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
            "norm-only statement without Frobenius anti-invariance or Hilbert-90 descent",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def invariants() -> tuple[NormInvariant, ...]:
    period = profile_yang_y507_period_norm_character()
    lift = profile_sparse_hilbert90_yang_lift()
    product = profile_sparse_h90_product_normal_form()
    legal_boundaries_ok = all(row.boundary_equals_period_norm for row in lift.legal_sparse_rows)
    formal_boundaries_ok = all(row.boundary_equals_period_norm for row in lift.formal_one_coset_rows)
    return (
        NormInvariant(
            name="dense_period_norm",
            statement="Norm_156(Y_507) has support 312 with +/-6 on the two unit cosets",
            ok=(
                period.row_ok
                and period.y_summary.period_norm_support == 312
                and period.y_summary.period_norm_coefficient_counts == ((-6, 156), (6, 156))
            ),
        ),
        NormInvariant(
            name="legal_descent_rows",
            statement="four legal support-156 Hilbert-90 preimages have boundary Norm_156(Y_507)",
            ok=(
                lift.row_ok
                and len(lift.legal_sparse_rows) == 4
                and lift.min_legal_lifted_potential_support == 156
                and legal_boundaries_ok
            ),
        ),
        NormInvariant(
            name="boundary_larger_than_preimage",
            statement="the dense norm has twice the support of a legal sparse preimage",
            ok=lift.period_norm_support == 2 * lift.min_legal_lifted_potential_support,
        ),
        NormInvariant(
            name="formal_controls_same_boundary",
            statement="formal one-coset controls can share the boundary while failing mixed-axis tests",
            ok=(
                len(lift.formal_one_coset_rows) == 2
                and formal_boundaries_ok
                and lift.all_formal_lifts_have_nonzero_axis_pushforwards
            ),
        ),
        NormInvariant(
            name="legal_product_rows",
            statement="the selected legal descents are four 78-over-78 rows in one doubling orbit",
            ok=(
                product.row_ok
                and len(product.legal_rows) == 4
                and product.legal_rows_are_78_over_78_products
                and product.legal_rows_form_one_doubling_orbit
            ),
        ),
        NormInvariant(
            name="norm_only_not_direct_closer",
            statement="period norm, sparse lift, and product normal form are still not source-stage theorem closers",
            ok=not period.direct_closer and not lift.direct_closer and not product.direct_closer,
        ),
    )


def decisions() -> tuple[NormDecision, ...]:
    return (
        NormDecision(
            name="legal_support156_value_divisor_theorem",
            theorem_shape="finite value/divisor theorem for one legal support-156 preimage/product row",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        NormDecision(
            name="period_norm_identity_only",
            theorem_shape="identity or value for the dense Norm_156(Y_507) boundary only",
            decision="repair_norm_only_h90_descent_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="legal support-156 Hilbert-90 descent selecting one row",
            ok=True,
        ),
        NormDecision(
            name="dense_unit_character_norm_value",
            theorem_shape="finite theorem for the dense +/-6 unit-character period norm",
            decision="repair_norm_only_row_selection_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="selected legal 78-over-78 product row and finite theorem for that row",
            ok=True,
        ),
        NormDecision(
            name="norm_with_formal_one_coset_descent",
            theorem_shape="descent through a formal one-coset control with the same boundary",
            decision="reject_boundary_control_not_source_object",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="proper-axis pushforward failure; not the mixed conductor-39 source object",
            ok=True,
        ),
        NormDecision(
            name="norm_plus_explicit_legal_h90_descent",
            theorem_shape="dense norm plus an explicit legal support-156 Hilbert-90 preimage/product row",
            decision="normalize_descent_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after legal H90 descent normalization",
            ok=True,
        ),
    )


def build_ambiguity() -> NormOnlyDescentAmbiguity:
    markers = evidence_markers()
    invariant_rows = invariants()
    decision_rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    invariant_ok = sum(row.ok for row in invariant_rows)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    normalize = sum(row.normalize_then_intake for row in decision_rows)
    repairs = sum(row.decision.startswith("repair_") for row in decision_rows)
    rejects = sum(row.decision.startswith("reject_") for row in decision_rows)
    current_closers = 0
    expected = (
        "source_stage_candidate_if_theorem_present",
        "repair_norm_only_h90_descent_missing",
        "repair_norm_only_row_selection_missing",
        "reject_boundary_control_not_source_object",
        "normalize_descent_then_apply_source_snippet_intake",
    )
    row_ok = (
        markers_ok == len(markers)
        and invariant_ok == len(invariant_rows)
        and len(decision_rows) == 5
        and tuple(row.decision for row in decision_rows) == expected
        and source_candidates == 1
        and normalize == 1
        and repairs == 2
        and rejects == 1
        and current_closers == 0
        and all(row.ok for row in decision_rows)
    )
    return NormOnlyDescentAmbiguity(
        evidence_markers=markers,
        invariants=invariant_rows,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        invariants_ok=invariant_ok,
        source_candidate_shapes=source_candidates,
        normalize_rows=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    ambiguity = build_ambiguity()
    for marker_row in ambiguity.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("invariants")
    for row in ambiguity.invariants:
        print(f"  {row.name}: ok={int(row.ok)} statement={row.statement}")
    print("decisions")
    for row in ambiguity.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)} "
            f"normalize={int(row.normalize_then_intake)}"
        )
        print(f"    shape={row.theorem_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={ambiguity.evidence_markers_ok}/{len(ambiguity.evidence_markers)}")
    print(f"  invariants_ok={ambiguity.invariants_ok}/{len(ambiguity.invariants)}")
    print(f"  source_candidate_shapes={ambiguity.source_candidate_shapes}")
    print(f"  normalize_rows={ambiguity.normalize_rows}")
    print(f"  repair_rows={ambiguity.repair_rows}")
    print(f"  reject_rows={ambiguity.reject_rows}")
    print(f"  current_source_stage_closers={ambiguity.current_source_stage_closers}")
    print("interpretation")
    print("  dense_period_norm_is_boundary_data_not_selected_row=1")
    print("  legal_h90_descent_selects_support156_row_before_intake=1")
    print("  formal_one_coset_descent_same_boundary_is_rejected=1")
    print(f"p25_v2_norm_only_descent_ambiguity_rows={int(ambiguity.row_ok)}/1")
    return 0 if ambiguity.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
