#!/usr/bin/env python3
"""Quartic selector routing under reciprocal row orientation.

The exact C4_1 phase selects an oriented edge only together with orientation
and boundary sign.  Taking a reciprocal negates the exponent row, so it negates
both the Hilbert-90 boundary and the quartic phase.  The negated phase is also
the phase of the opposite oriented edge, which makes boundary sign a necessary
part of character-language intake.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


GI = tuple[int, int]

ORIENTED_PHASES: tuple[tuple[int, GI], ...] = (
    (1, (2, 2)),
    (2, (-2, 2)),
    (4, (-2, -2)),
    (8, (2, -2)),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ReciprocalPhaseRow:
    oriented_m: int
    oriented_phase: GI
    reciprocal_phase: GI
    reciprocal_phase_matches_oriented_m: int
    oriented_boundary: str
    reciprocal_boundary: str
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class Route:
    name: str
    provided_shape: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class QuarticReciprocalOrientation:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[ReciprocalPhaseRow, ...]
    routes: tuple[Route, ...]
    reciprocal_phase_collisions: int
    normalize_rows: int
    repair_rows: int
    reject_rows: int
    current_source_closers: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "row_orientation_reciprocal_normalizer",
            "research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
            "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "c4_character_spectrum",
            "research/p25/evidence/p25_v2_c4_character_spectrum_20260616.md",
            "p25_v2_c4_character_spectrum_rows=1/1",
        ),
        marker(
            "row_sign_c4_tensor_spectrum",
            "research/p25/evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md",
            "p25_v2_row_sign_c4_tensor_spectrum_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def neg(value: GI) -> GI:
    return (-value[0], -value[1])


def phase_to_m() -> dict[GI, int]:
    return {phase: m for m, phase in ORIENTED_PHASES}


def reciprocal_rows() -> tuple[ReciprocalPhaseRow, ...]:
    lookup = phase_to_m()
    opposite = {1: 4, 2: 8, 4: 1, 8: 2}
    rows: list[ReciprocalPhaseRow] = []
    for m, phase in ORIENTED_PHASES:
        reciprocal_phase = neg(phase)
        matched = lookup[reciprocal_phase]
        rows.append(
            ReciprocalPhaseRow(
                oriented_m=m,
                oriented_phase=phase,
                reciprocal_phase=reciprocal_phase,
                reciprocal_phase_matches_oriented_m=matched,
                oriented_boundary="+Norm_156(Y_507)",
                reciprocal_boundary="-Norm_156(Y_507)",
                decision="normalize_reciprocal_phase_with_minus_boundary",
                row_ok=matched == opposite[m],
            )
        )
    return tuple(rows)


def routes() -> tuple[Route, ...]:
    return (
        Route(
            name="oriented_exact_phase_plus_boundary",
            provided_shape="exact C4_1 phase, row-antisymmetric tensor sign, +Norm_156 boundary",
            decision="source_stage_candidate_if_finite_theorem_present",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem plus extraction",
            ok=True,
        ),
        Route(
            name="reciprocal_exact_phase_minus_boundary",
            provided_shape="exact C4_1 phase for reciprocal row, explicit -Norm_156 boundary",
            decision="normalize_reciprocal_then_apply_source_snippet_intake",
            first_missing_or_falsifier="same theorem data after orientation normalization",
            ok=True,
        ),
        Route(
            name="exact_phase_boundary_sign_unspecified",
            provided_shape="exact C4_1 phase but no orientation or boundary-sign convention",
            decision="repair_reciprocal_orientation_or_boundary_sign_missing",
            first_missing_or_falsifier="explicit oriented row or reciprocal row with -Norm_156 boundary",
            ok=True,
        ),
        Route(
            name="reciprocal_phase_plus_boundary",
            provided_shape="reciprocal row phase asserted with +Norm_156 boundary",
            decision="reject_orientation_boundary_mismatch",
            first_missing_or_falsifier="reciprocal product carries -Norm_156 boundary",
            ok=True,
        ),
        Route(
            name="phase_collision_as_different_edge",
            provided_shape="negated reciprocal phase treated as the opposite oriented edge without boundary sign",
            decision="repair_phase_orientation_collision",
            first_missing_or_falsifier="boundary sign/orientation data distinguishing reciprocal row from opposite edge",
            ok=True,
        ),
    )


def build_check() -> QuarticReciprocalOrientation:
    markers = evidence_markers()
    rows = reciprocal_rows()
    route_rows = routes()
    collisions = sum(row.reciprocal_phase_matches_oriented_m != row.oriented_m for row in rows)
    normalize = sum("normalize" in row.decision for row in route_rows)
    repair = sum(row.decision.startswith("repair") for row in route_rows)
    reject = sum(row.decision.startswith("reject") for row in route_rows)
    current_source = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 4
        and all(row.row_ok for row in rows)
        and collisions == 4
        and normalize == 1
        and repair == 2
        and reject == 1
        and current_source == 0
        and all(row.ok for row in route_rows)
    )
    return QuarticReciprocalOrientation(
        evidence_markers=markers,
        rows=rows,
        routes=route_rows,
        reciprocal_phase_collisions=collisions,
        normalize_rows=normalize,
        repair_rows=repair,
        reject_rows=reject,
        current_source_closers=current_source,
        row_ok=row_ok,
    )


def fmt_gi(value: GI) -> str:
    real, imag = value
    sign = "+" if imag >= 0 else "-"
    return f"{real}{sign}{abs(imag)}i"


def main() -> int:
    check = build_check()
    print("p25 v2 quartic reciprocal orientation")
    for marker_row in check.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in check.rows:
        print(
            f"  m={row.oriented_m}: phase={fmt_gi(row.oriented_phase)} "
            f"reciprocal_phase={fmt_gi(row.reciprocal_phase)} "
            f"matches_oriented_m={row.reciprocal_phase_matches_oriented_m} "
            f"boundary={row.reciprocal_boundary} ok={int(row.row_ok)}"
        )
    print("routes")
    for route in check.routes:
        print(f"  {route.name}: decision={route.decision}")
        print(f"    first_missing_or_falsifier={route.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={sum(row.ok for row in check.evidence_markers)}/{len(check.evidence_markers)}")
    print(f"  reciprocal_phase_collisions={check.reciprocal_phase_collisions}")
    print(f"  normalize_rows={check.normalize_rows}")
    print(f"  repair_rows={check.repair_rows}")
    print(f"  reject_rows={check.reject_rows}")
    print(f"  current_source_closers={check.current_source_closers}")
    print("interpretation")
    print("  reciprocal_rows_negate_quartic_phase_and_boundary=1")
    print("  exact_phase_requires_orientation_or_boundary_sign=1")
    print("  reciprocal_plus_positive_boundary_is_rejected=1")
    print(f"p25_v2_quartic_reciprocal_orientation_rows={int(check.row_ok)}/1")
    return 0 if check.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
