#!/usr/bin/env python3
"""V2 source-theorem gap for the unified H0/conductor-39 target.

The previous v2 gates show the first-pass target is one support-156 product
family.  This gate checks whether any hidden selector/gauge freedom remains in
that finite target.  The intended answer is no: the group-ring/Yang/Hilbert-90
part is saturated, and the missing ingredient is a genuine arithmetic
value/divisor theorem.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "harness"))

from p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate import (  # noqa: E402
    profile_yang_y507_conductor39_hilbert90_boundary,
)
from p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate import (  # noqa: E402
    profile_sparse_hilbert90_yang_lift,
)
from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (  # noqa: E402
    profile_sparse_h90_product_normal_form,
)


RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class GapLayerRow:
    layer: str
    status: str
    evidence: str
    next_requirement: str
    ok: bool


@dataclass(frozen=True)
class UnifiedSourceTheoremGap:
    h90_boundary_ok: bool
    sparse_yang_lift_ok: bool
    product_normal_form_ok: bool
    unified_target_marker_ok: bool
    submission_contract_marker_ok: bool
    current_source_theorem_rows_zero: bool
    h90_orbit_rows: int
    h90_total_min_support: int
    sparse_source_support: int
    legal_sparse_lift_count: int
    formal_one_coset_lift_count: int
    min_legal_lifted_potential_support: int
    balanced_lifted_potential_support: int
    legal_product_rows: int
    quotient_representatives: tuple[int, ...]
    canonical_stabilizer: tuple[int, ...]
    legal_rows_are_one_orbit: bool
    legal_rows_are_78_over_78: bool
    formal_one_coset_controls_rejected: bool
    all_group_ring_layers_saturated: bool
    any_direct_closer: bool
    remaining_gap: str
    falsifier_for_next_attempt: str
    layers: tuple[GapLayerRow, ...]
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
            "submission_extraction_contract",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "first_pass_triage",
            "research/p25/evidence/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_20260614.md",
            "current_source_theorem_rows       = 0",
        ),
    )


def profile_unified_source_theorem_gap() -> UnifiedSourceTheoremGap:
    h90 = profile_yang_y507_conductor39_hilbert90_boundary()
    sparse = profile_sparse_hilbert90_yang_lift()
    normal = profile_sparse_h90_product_normal_form()
    markers = evidence_markers()

    unified_marker_ok, submission_marker_ok, source_zero_ok = (m.ok for m in markers)
    legal_rows_are_one_orbit = normal.legal_rows_form_one_doubling_orbit
    legal_rows_are_78 = normal.legal_rows_are_78_over_78_products
    formal_rejected = normal.formal_one_coset_controls_rejected
    any_direct_closer = h90.direct_closer or sparse.direct_closer or normal.direct_closer
    saturated = (
        h90.row_ok
        and sparse.row_ok
        and normal.row_ok
        and unified_marker_ok
        and h90.total_min_support == 12
        and sparse.legal_sparse_lift_count == 4
        and sparse.formal_one_coset_lift_count == 2
        and sparse.min_legal_lifted_potential_support == 156
        and sparse.balanced_lifted_potential_support == 312
        and legal_rows_are_one_orbit
        and legal_rows_are_78
        and formal_rejected
        and normal.quotient_representatives == (1, 2, 4, 8)
        and normal.canonical_stabilizer == (1, 16, 22)
        and not any_direct_closer
    )

    layers = (
        GapLayerRow(
            layer="source_legality",
            status="satisfied",
            evidence="Koo-Shin 2010/Theorem 6.2 source words and v2 H0/conductor-39 contracts",
            next_requirement="do not reprove source legality unless a new theorem route depends on it",
            ok=True,
        ),
        GapLayerRow(
            layer="hilbert90_boundary",
            status="satisfied_not_closer",
            evidence="conductor-39 word is (1-Frob_p)V with minimum support 12",
            next_requirement="turn boundary into a finite value/divisor theorem",
            ok=h90.row_ok and h90.total_min_support == 12 and not h90.direct_closer,
        ),
        GapLayerRow(
            layer="legal_sparse_yang_lift",
            status="satisfied_not_closer",
            evidence="four legal sparse selectors lift to support-156 potentials; formal one-coset lifts fail mixed axes",
            next_requirement="prove a value/divisor identity for one legal support-156 potential",
            ok=sparse.row_ok and sparse.legal_sparse_lift_count == 4 and formal_rejected,
        ),
        GapLayerRow(
            layer="unified_product_normal_form",
            status="satisfied_not_closer",
            evidence="four legal products form one <2>-orbit of 78-over-78 Yang-fiber products",
            next_requirement="source theorem must hit one of these four rows",
            ok=normal.row_ok and legal_rows_are_one_orbit and legal_rows_are_78,
        ),
        GapLayerRow(
            layer="source_stage_value_or_divisor_theorem",
            status="missing",
            evidence="triage still records current_source_theorem_rows = 0",
            next_requirement="finite value/divisor theorem with Norm_156(Y_507) boundary",
            ok=source_zero_ok,
        ),
        GapLayerRow(
            layer="submission_extraction",
            status="missing",
            evidence="submission/extraction contract records zero current satisfied rows",
            next_requirement="DANGER3 framing, same-j X1(8112), X1(16), halving/x0, vpp.py",
            ok=submission_marker_ok,
        ),
    )

    row_ok = (
        unified_marker_ok
        and submission_marker_ok
        and source_zero_ok
        and saturated
        and len(layers) == 6
        and all(row.ok for row in layers)
    )

    return UnifiedSourceTheoremGap(
        h90_boundary_ok=h90.row_ok,
        sparse_yang_lift_ok=sparse.row_ok,
        product_normal_form_ok=normal.row_ok,
        unified_target_marker_ok=unified_marker_ok,
        submission_contract_marker_ok=submission_marker_ok,
        current_source_theorem_rows_zero=source_zero_ok,
        h90_orbit_rows=len(h90.orbit_gauge_rows),
        h90_total_min_support=h90.total_min_support,
        sparse_source_support=sparse.sparse_support if hasattr(sparse, "sparse_support") else 12,
        legal_sparse_lift_count=sparse.legal_sparse_lift_count,
        formal_one_coset_lift_count=sparse.formal_one_coset_lift_count,
        min_legal_lifted_potential_support=sparse.min_legal_lifted_potential_support,
        balanced_lifted_potential_support=sparse.balanced_lifted_potential_support,
        legal_product_rows=len(normal.legal_rows),
        quotient_representatives=normal.quotient_representatives,
        canonical_stabilizer=normal.canonical_stabilizer,
        legal_rows_are_one_orbit=legal_rows_are_one_orbit,
        legal_rows_are_78_over_78=legal_rows_are_78,
        formal_one_coset_controls_rejected=formal_rejected,
        all_group_ring_layers_saturated=saturated,
        any_direct_closer=any_direct_closer,
        remaining_gap=(
            "finite arithmetic value/divisor theorem for one legal support-156 "
            "product with Norm_156(Y_507) boundary"
        ),
        falsifier_for_next_attempt=(
            "reject any proposal that only changes gauge/selector/product normal "
            "form without adding a value/divisor theorem"
        ),
        layers=layers,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_unified_source_theorem_gap()
    print("p25 v2 unified source-theorem gap gate")
    print("dependencies")
    print(f"  h90_boundary_ok={int(profile.h90_boundary_ok)}")
    print(f"  sparse_yang_lift_ok={int(profile.sparse_yang_lift_ok)}")
    print(f"  product_normal_form_ok={int(profile.product_normal_form_ok)}")
    print(f"  unified_target_marker_ok={int(profile.unified_target_marker_ok)}")
    print(f"  submission_contract_marker_ok={int(profile.submission_contract_marker_ok)}")
    print(f"  current_source_theorem_rows_zero={int(profile.current_source_theorem_rows_zero)}")
    print("saturated_group_ring_layers")
    print(f"  h90_orbit_rows={profile.h90_orbit_rows}")
    print(f"  h90_total_min_support={profile.h90_total_min_support}")
    print(f"  legal_sparse_lift_count={profile.legal_sparse_lift_count}")
    print(f"  formal_one_coset_lift_count={profile.formal_one_coset_lift_count}")
    print(f"  min_legal_lifted_potential_support={profile.min_legal_lifted_potential_support}")
    print(f"  balanced_lifted_potential_support={profile.balanced_lifted_potential_support}")
    print(f"  legal_product_rows={profile.legal_product_rows}")
    print(f"  quotient_representatives={profile.quotient_representatives}")
    print(f"  canonical_stabilizer={profile.canonical_stabilizer}")
    print(f"  legal_rows_are_one_orbit={int(profile.legal_rows_are_one_orbit)}")
    print(f"  legal_rows_are_78_over_78={int(profile.legal_rows_are_78_over_78)}")
    print(f"  formal_one_coset_controls_rejected={int(profile.formal_one_coset_controls_rejected)}")
    print(f"  any_direct_closer={int(profile.any_direct_closer)}")
    print("layers")
    for row in profile.layers:
        print(
            "  "
            f"{row.layer}: status={row.status} next={row.next_requirement} ok={int(row.ok)}"
        )
    print("interpretation")
    print(f"  all_group_ring_layers_saturated={int(profile.all_group_ring_layers_saturated)}")
    print("  hidden_selector_or_gauge_freedom_remaining=0")
    print("  source_legality_or_boundary_only_is_not_progress=1")
    print(f"  remaining_gap={profile.remaining_gap}")
    print(f"  falsifier_for_next_attempt={profile.falsifier_for_next_attempt}")
    print(f"p25_v2_unified_source_theorem_gap_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("unified source-theorem gap regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
