#!/usr/bin/env python3
"""Root/sign ambiguity for row-square p25 theorem shapes.

The row quotient invariant bridge shows that diagonal aggregate plus quotient
recovers twice one legal row in the exponent lattice.  This gate records the
first falsifier for promoting that to a one-row source theorem: a row-square
value has the two roots R and -R, and the constant sign has zero divisor and
zero Hilbert-90 boundary.  Therefore a square theorem is still a repair row
unless it supplies explicit root/sign/orientation data or a direct one-row
value/divisor theorem.
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
class AmbiguityInvariant:
    name: str
    statement: str
    ok: bool


@dataclass(frozen=True)
class SquareRootDecision:
    name: str
    theorem_shape: str
    decision: str
    source_candidate_if_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RowSquareRootAmbiguity:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_mod_4: int
    p_is_odd: bool
    invariants: tuple[AmbiguityInvariant, ...]
    decisions: tuple[SquareRootDecision, ...]
    evidence_markers_ok: int
    invariants_ok: int
    source_candidate_shapes: int
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
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
        ),
        marker(
            "period156_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def invariants() -> tuple[AmbiguityInvariant, ...]:
    p_is_odd = P % 2 == 1
    return (
        AmbiguityInvariant(
            name="two_roots_for_nonzero_square",
            statement="over odd F_p, a nonzero square has roots R and -R",
            ok=p_is_odd,
        ),
        AmbiguityInvariant(
            name="constant_sign_has_zero_divisor",
            statement="multiplying a modular-unit value by -1 changes no divisor",
            ok=True,
        ),
        AmbiguityInvariant(
            name="constant_sign_has_zero_h90_boundary",
            statement="(-1) / Frob_p(-1) = 1, so the sign has zero H90 boundary",
            ok=True,
        ),
        AmbiguityInvariant(
            name="same_square_after_sign_flip",
            statement="(-R)^2 = R^2",
            ok=True,
        ),
        AmbiguityInvariant(
            name="same_boundary_after_sign_flip",
            statement="R and -R have the same divisor and H90 boundary",
            ok=True,
        ),
    )


def decisions() -> tuple[SquareRootDecision, ...]:
    return (
        SquareRootDecision(
            name="one_row_value_or_divisor_theorem",
            theorem_shape="finite value/divisor theorem for one legal support-156 row with W boundary",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        SquareRootDecision(
            name="row_square_value_theorem",
            theorem_shape="finite theorem for the square of one legal row, equivalently 2*row in exponent notation",
            decision="repair_row_square_root_sign_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="explicit root/sign/orientation data selecting R rather than -R, or direct one-row theorem",
            ok=True,
        ),
        SquareRootDecision(
            name="aggregate_plus_quotient_square_bridge",
            theorem_shape="broad diagonal aggregate plus matching row quotient, recovering 2*row",
            decision="repair_row_square_bridge_halving_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="halving/root/orientation data selecting the legal row, or direct one-row theorem",
            ok=True,
        ),
        SquareRootDecision(
            name="row_square_with_h90_boundary_2w",
            theorem_shape="row-square theorem with doubled H90 boundary 2W",
            decision="repair_boundary_scale_and_root_sign_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="one-row W-boundary theorem plus explicit root/sign/orientation",
            ok=True,
        ),
        SquareRootDecision(
            name="row_square_with_explicit_oriented_root",
            theorem_shape="row-square theorem plus explicit oriented root equal to one legal row",
            decision="normalize_root_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="same theorem data after oriented-root normalization",
            ok=True,
        ),
    )


def build_ambiguity() -> RowSquareRootAmbiguity:
    markers = evidence_markers()
    invariant_rows = invariants()
    decision_rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    invariant_ok = sum(row.ok for row in invariant_rows)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    repairs = sum(row.decision.startswith("repair_") for row in decision_rows)
    current_closers = 0
    expected = (
        "source_stage_candidate_if_theorem_present",
        "repair_row_square_root_sign_missing",
        "repair_row_square_bridge_halving_missing",
        "repair_boundary_scale_and_root_sign_missing",
        "normalize_root_then_apply_source_snippet_intake",
    )
    row_ok = (
        markers_ok == len(markers)
        and P % 4 == 1
        and P % 2 == 1
        and invariant_ok == len(invariant_rows)
        and len(decision_rows) == 5
        and tuple(row.decision for row in decision_rows) == expected
        and source_candidates == 2
        and repairs == 3
        and current_closers == 0
        and all(row.ok for row in decision_rows)
    )
    return RowSquareRootAmbiguity(
        evidence_markers=markers,
        p_mod_4=P % 4,
        p_is_odd=P % 2 == 1,
        invariants=invariant_rows,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        invariants_ok=invariant_ok,
        source_candidate_shapes=source_candidates,
        repair_rows=repairs,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    ambiguity = build_ambiguity()
    for marker_row in ambiguity.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mod_4={ambiguity.p_mod_4}")
    print(f"  p_is_odd={int(ambiguity.p_is_odd)}")
    print("invariants")
    for row in ambiguity.invariants:
        print(f"  {row.name}: ok={int(row.ok)} statement={row.statement}")
    print("decisions")
    for row in ambiguity.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)}"
        )
        print(f"    shape={row.theorem_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={ambiguity.evidence_markers_ok}/{len(ambiguity.evidence_markers)}")
    print(f"  invariants_ok={ambiguity.invariants_ok}/{len(ambiguity.invariants)}")
    print(f"  source_candidate_shapes={ambiguity.source_candidate_shapes}")
    print(f"  repair_rows={ambiguity.repair_rows}")
    print(f"  current_source_stage_closers={ambiguity.current_source_stage_closers}")
    print("interpretation")
    print("  row_square_theorem_has_root_sign_ambiguity=1")
    print("  sign_flip_preserves_divisor_and_h90_boundary=1")
    print("  square_or_2W_boundary_alone_is_not_source_close=1")
    print(f"p25_v2_row_square_root_ambiguity_rows={int(ambiguity.row_ok)}/1")
    return 0 if ambiguity.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
