#!/usr/bin/env python3
"""Constant-normalization ambiguity for p25 theorem snippets.

This gate records a small but important repair rule for future source answers.
A divisor theorem plus Hilbert-90 boundary does not determine the exact finite
value if the result is only specified up to multiplication by an F_p^* scalar:
such constants have zero divisor and zero Hilbert-90 boundary.  Accepted
source-stage value/divisor snippets must therefore include an additive/value
normalization, period-156 branch/root/telescoping context, or a DANGER3-ready
finite framing that fixes the scalar.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P = 10000000000000000000000013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ConstantInvariant:
    name: str
    statement: str
    ok: bool


@dataclass(frozen=True)
class ConstantDecision:
    name: str
    theorem_shape: str
    decision: str
    source_candidate_if_theorem_present: bool
    normalize_then_intake: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ConstantNormalizationAmbiguity:
    evidence_markers: tuple[EvidenceMarker, ...]
    invariants: tuple[ConstantInvariant, ...]
    decisions: tuple[ConstantDecision, ...]
    evidence_markers_ok: int
    invariants_ok: int
    source_candidate_shapes: int
    normalize_rows: int
    repair_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "period156_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
    )


def invariants() -> tuple[ConstantInvariant, ...]:
    return (
        ConstantInvariant(
            name="many_nonzero_constants",
            statement="F_p^* has p-1 possible nonzero constants, not only a sign",
            ok=P - 1 > 2,
        ),
        ConstantInvariant(
            name="constant_has_zero_divisor",
            statement="multiplying a modular-unit value by c in F_p^* changes no divisor",
            ok=True,
        ),
        ConstantInvariant(
            name="constant_has_zero_h90_boundary",
            statement="c / Frob_p(c) = 1 for c in F_p^*, so c has zero H90 boundary",
            ok=True,
        ),
        ConstantInvariant(
            name="scalar_multiple_preserves_divisor_and_boundary",
            statement="R and cR have the same divisor and Hilbert-90 boundary for c in F_p^*",
            ok=True,
        ),
        ConstantInvariant(
            name="scalar_ambiguity_not_exact_value",
            statement="divisor plus H90 boundary alone does not select the exact finite value",
            ok=True,
        ),
    )


def decisions() -> tuple[ConstantDecision, ...]:
    return (
        ConstantDecision(
            name="divisor_additive_or_normalized_value_theorem",
            theorem_shape="finite divisor/additive theorem or normalized finite value theorem for one legal row",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        ConstantDecision(
            name="period156_value_with_branch_root_context",
            theorem_shape="period-156 finite value theorem with branch/root/telescoping context fixing the value",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        ConstantDecision(
            name="divisor_only_with_h90_boundary",
            theorem_shape="divisor identity plus Hilbert-90 boundary, but no finite additive/value normalization",
            decision="repair_constant_normalization_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="additive/value normalization or finite framing fixing the F_p^* scalar",
            ok=True,
        ),
        ConstantDecision(
            name="value_up_to_fp_scalar",
            theorem_shape="finite value theorem stated only up to multiplication by an unspecified F_p^* scalar",
            decision="repair_constant_normalization_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="specified scalar, branch/root/telescoping context, or normalized value",
            ok=True,
        ),
        ConstantDecision(
            name="normalized_value_after_constant_fix",
            theorem_shape="same theorem data after an explicit scalar or normalization fixes the F_p^* ambiguity",
            decision="normalize_value_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after value normalization",
            ok=True,
        ),
    )


def build_ambiguity() -> ConstantNormalizationAmbiguity:
    markers = evidence_markers()
    invariant_rows = invariants()
    decision_rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    invariant_ok = sum(row.ok for row in invariant_rows)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    normalize = sum(row.normalize_then_intake for row in decision_rows)
    repairs = sum(row.decision.startswith("repair_") for row in decision_rows)
    current_closers = 0
    expected = (
        "source_stage_candidate_if_theorem_present",
        "source_stage_candidate_if_theorem_present",
        "repair_constant_normalization_missing",
        "repair_constant_normalization_missing",
        "normalize_value_then_apply_source_snippet_intake",
    )
    row_ok = (
        markers_ok == len(markers)
        and invariant_ok == len(invariant_rows)
        and len(decision_rows) == 5
        and tuple(row.decision for row in decision_rows) == expected
        and source_candidates == 2
        and normalize == 1
        and repairs == 2
        and current_closers == 0
        and all(row.ok for row in decision_rows)
    )
    return ConstantNormalizationAmbiguity(
        evidence_markers=markers,
        invariants=invariant_rows,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        invariants_ok=invariant_ok,
        source_candidate_shapes=source_candidates,
        normalize_rows=normalize,
        repair_rows=repairs,
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
    print(f"  current_source_stage_closers={ambiguity.current_source_stage_closers}")
    print("interpretation")
    print("  fp_scalars_have_zero_divisor_and_h90_boundary=1")
    print("  divisor_plus_h90_boundary_without_value_normalization_is_not_source_close=1")
    print("  explicit_scalar_or_value_normalization_routes_back_to_intake=1")
    print(f"p25_v2_constant_normalization_ambiguity_rows={int(ambiguity.row_ok)}/1")
    return 0 if ambiguity.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
