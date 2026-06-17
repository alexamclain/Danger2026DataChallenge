#!/usr/bin/env python3
"""Q square payload router for the p25 conductor-39 route.

The Q split quartic-selector screen shows that Q diagonal plus the matching
pure quartic split recovers twice one legal edge.  This gate records the
distinction that follows: exact F_p value data for that square gives a
two-root row-value payload, but it still needs an extraction map before vpp.py
can test concrete DANGER3 candidates.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RootInvariant:
    name: str
    value: str
    ok: bool


@dataclass(frozen=True)
class PayloadRoute:
    name: str
    theorem_shape: str
    decision: str
    source_stage_candidate: bool
    bounded_operational_payload: bool
    normalize_then_intake: bool
    repair: bool
    reject: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class QSquarePayloadRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    invariants: tuple[RootInvariant, ...]
    routes: tuple[PayloadRoute, ...]
    evidence_markers_ok: int
    invariants_ok: int
    source_stage_candidates: int
    bounded_payload_rows: int
    normalize_rows: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "q_split_quartic_selector",
            "research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md",
            "p25_v2_q_split_quartic_selector_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "coefficient6_root_normalization",
            "research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md",
            "p25_v2_coefficient6_root_normalization_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "row_square_value_theorem",
        ),
    )


def invariants() -> tuple[RootInvariant, ...]:
    root_kernel = gcd(2, P25 - 1)
    return (
        RootInvariant("p_mod_4", str(P25 % 4), P25 % 4 == 1),
        RootInvariant("p_odd", str(P25 % 2 == 1), P25 % 2 == 1),
        RootInvariant("square_root_kernel_size", str(root_kernel), root_kernel == 2),
        RootInvariant("modular_unit_values_nonzero", "F_p^*", True),
        RootInvariant(
            "constant_sign_invisible_to_divisor_h90_phase",
            "(-1)^2=1 and (-1)/Frob_p(-1)=1",
            True,
        ),
    )


def routes() -> tuple[PayloadRoute, ...]:
    return (
        PayloadRoute(
            name="q_square_exact_fp_value",
            theorem_shape="Q diagonal plus correct pure quartic split gives an exact nonzero F_p value for 2*edge",
            decision="repair_extraction_map_missing_after_two_root_row_payload",
            source_stage_candidate=False,
            bounded_operational_payload=True,
            normalize_then_intake=False,
            repair=True,
            reject=False,
            first_missing_or_falsifier="two F_p row roots exist; DANGER3 framing and same-j/X_1(16)/halving or direct A,x0 extraction map still missing",
            ok=True,
        ),
        PayloadRoute(
            name="q_square_divisor_or_boundary_only",
            theorem_shape="Q diagonal plus split proves only divisor/H90 boundary data for 2*edge",
            decision="repair_exact_fp_value_or_oriented_root_missing",
            source_stage_candidate=False,
            bounded_operational_payload=False,
            normalize_then_intake=False,
            repair=True,
            reject=False,
            first_missing_or_falsifier="exact finite value or oriented one-edge theorem",
            ok=True,
        ),
        PayloadRoute(
            name="q_square_value_up_to_scalar",
            theorem_shape="Q square value is known only up to an unspecified F_p^* scalar",
            decision="repair_scalar_and_root_orientation_missing",
            source_stage_candidate=False,
            bounded_operational_payload=False,
            normalize_then_intake=False,
            repair=True,
            reject=False,
            first_missing_or_falsifier="specified scalar before the two-root payload is concrete",
            ok=True,
        ),
        PayloadRoute(
            name="q_square_with_oriented_root",
            theorem_shape="Q square theorem also supplies the oriented root equal to one legal row",
            decision="normalize_root_then_apply_source_snippet_intake",
            source_stage_candidate=True,
            bounded_operational_payload=False,
            normalize_then_intake=True,
            repair=False,
            reject=False,
            first_missing_or_falsifier="same theorem data after oriented-root normalization",
            ok=True,
        ),
        PayloadRoute(
            name="q_direct_one_edge_theorem",
            theorem_shape="direct finite value/divisor theorem for one legal support-156 row",
            decision="source_stage_candidate_if_theorem_present",
            source_stage_candidate=True,
            bounded_operational_payload=False,
            normalize_then_intake=False,
            repair=False,
            reject=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        PayloadRoute(
            name="sign_from_divisor_h90_or_quartic_phase",
            theorem_shape="try to choose R versus -R using only divisor, H90 boundary, or quotient-C4 phase",
            decision="reject_sign_invisible_to_current_invariants",
            source_stage_candidate=False,
            bounded_operational_payload=False,
            normalize_then_intake=False,
            repair=False,
            reject=True,
            first_missing_or_falsifier="constant sign has zero divisor/H90 boundary and does not alter exponent-character data",
            ok=True,
        ),
    )


def build_router() -> QSquarePayloadRouter:
    markers = evidence_markers()
    invariant_rows = invariants()
    route_rows = routes()
    markers_ok = sum(row.ok for row in markers)
    invariants_ok = sum(row.ok for row in invariant_rows)
    source_candidates = sum(row.source_stage_candidate for row in route_rows)
    bounded_payloads = sum(row.bounded_operational_payload for row in route_rows)
    normalize = sum(row.normalize_then_intake for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    expected = (
        "repair_extraction_map_missing_after_two_root_row_payload",
        "repair_exact_fp_value_or_oriented_root_missing",
        "repair_scalar_and_root_orientation_missing",
        "normalize_root_then_apply_source_snippet_intake",
        "source_stage_candidate_if_theorem_present",
        "reject_sign_invisible_to_current_invariants",
    )
    row_ok = (
        markers_ok == len(markers)
        and invariants_ok == len(invariant_rows)
        and len(route_rows) == 6
        and tuple(row.decision for row in route_rows) == expected
        and source_candidates == 2
        and bounded_payloads == 1
        and normalize == 1
        and repairs == 3
        and rejects == 1
        and current_source_theorems == 0
        and all(row.ok for row in route_rows)
    )
    return QSquarePayloadRouter(
        evidence_markers=markers,
        invariants=invariant_rows,
        routes=route_rows,
        evidence_markers_ok=markers_ok,
        invariants_ok=invariants_ok,
        source_stage_candidates=source_candidates,
        bounded_payload_rows=bounded_payloads,
        normalize_rows=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    print("p25 v2 Q square payload router")
    for marker_row in router.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("invariants")
    for row in router.invariants:
        print(f"  {row.name}: {row.value} ok={int(row.ok)}")
    print("routes")
    for row in router.routes:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    bounded_operational_payload={int(row.bounded_operational_payload)}")
        print(f"    source_stage_candidate={int(row.source_stage_candidate)}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={router.evidence_markers_ok}/{len(router.evidence_markers)}")
    print(f"  invariants_ok={router.invariants_ok}/{len(router.invariants)}")
    print(f"  source_stage_candidates={router.source_stage_candidates}")
    print(f"  bounded_payload_rows={router.bounded_payload_rows}")
    print(f"  normalize_rows={router.normalize_rows}")
    print(f"  repair_rows={router.repair_rows}")
    print(f"  reject_rows={router.reject_rows}")
    print(f"  current_source_theorems={router.current_source_theorems}")
    print(f"p25_v2_q_square_payload_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
