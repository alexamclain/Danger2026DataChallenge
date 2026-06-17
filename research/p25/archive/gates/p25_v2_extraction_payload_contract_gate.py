#!/usr/bin/env python3
"""V2 extraction payload contract after a p25 source theorem hit.

The source theorem target is now precise, but a theorem-stage win is still not
a DANGER3 certificate.  This gate pins the constructive payload ladder from a
framed source theorem to the practical X_1(16) surface, halving/direct x0, and
official vpp.py verification.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013
X16_LEVEL = 16
ODD_LEVEL = 507
CROSS_LEVEL = 8112
ACTIVE_MODE = "x16halvenonsplit"
OPTIONAL_DGATE_MODE = "x16halvenonsplitdgate"
ACTIVE_START_DEPTH = 4
OPTIONAL_DGATE_START_DEPTH = 5


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ExtractionPayloadRow:
    name: str
    payload_shape: str
    source_theorem: bool
    danger3_framed: bool
    same_j_bridge: bool
    independent_components: bool
    same_j_invariant_only: bool
    order8112_generator: bool
    x16_y: bool
    model_root_x: bool
    direct_A_xP16: bool
    optional_dgate_surface: bool
    branch_word_only: bool
    x_chain: bool
    direct_x0: bool
    official_vpp: bool
    decision: str
    first_missing_or_falsifier: str
    submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class ExtractionPayloadContract:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_mod_8: int
    sqrt_floor: int
    hasse_bound: int
    k: int
    levels_coprime: bool
    inv_507_mod_16: int
    inv_16_mod_507: int
    p16_multiplier: int
    q507_multiplier: int
    projection_sum_mod_8112: int
    p16_order: int
    q507_order: int
    active_mode: str
    active_start_depth: int
    active_halving_links: int
    active_x_chain_points: int
    optional_mode: str
    optional_start_depth: int
    optional_halving_links: int
    rows: tuple[ExtractionPayloadRow, ...]
    evidence_markers_ok: int
    bridge_stage_rows: int
    x16_surface_rows: int
    optional_dgate_rows: int
    extraction_ready_rows: int
    submission_ready_rows: int
    repair_rows: int
    reject_rows: int
    current_live_payload_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "post_theorem_router",
            "research/p25/evidence/p25_v2_post_theorem_extraction_router_20260616.md",
            "p25_v2_post_theorem_extraction_router_rows=1/1",
        ),
        marker(
            "submission_contract",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "h0_bridge_contract",
            "research/p25/archive/notes/p25_ksy_y_h0_x18112_bridge_payload_contract_20260614.md",
            "ksy_y_h0_x18112_bridge_payload_contract_rows=1/1",
        ),
        marker(
            "x16_chart_contract",
            "research/p25/archive/notes/p25_ksy_y_x1_16_montgomery_chart_contract_20260614.md",
            "ksy_y_x1_16_montgomery_chart_contract_rows=1/1",
        ),
        marker(
            "halving_payload_contract",
            "research/p25/archive/notes/p25_ksy_y_x1_16_halving_certificate_payload_20260614.md",
            "ksy_y_x1_16_halving_certificate_payload_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def order_of_multiple(order: int, multiplier: int) -> int:
    return order // gcd(order, multiplier)


def compute_k_and_bound(p: int) -> tuple[int, int, int]:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return q, bound, bound.bit_length()


def payload_row(
    name: str,
    payload_shape: str,
    *,
    source: bool = False,
    framed: bool = False,
    same_j: bool = False,
    independent: bool = False,
    same_j_invariant: bool = False,
    order8112: bool = False,
    y: bool = False,
    root: bool = False,
    direct_surface: bool = False,
    dgate: bool = False,
    branch_word: bool = False,
    x_chain: bool = False,
    x0: bool = False,
    vpp: bool = False,
) -> ExtractionPayloadRow:
    if vpp:
        decision = "submission_ready"
        missing = "none"
        ready = True
    elif independent:
        decision = "reject_unglued_components"
        missing = "same j-invariant / same elliptic curve bridge"
        ready = False
    elif same_j_invariant:
        decision = "repair_same_j_invariant_only"
        missing = "explicit same-curve P16/Q507 pair, order-8112 generator, or direct A,xP16"
        ready = False
    elif branch_word:
        decision = "reject_branch_word_without_values"
        missing = "actual square-root witnesses, x-chain, direct x0, or vpp.py"
        ready = False
    elif not source:
        decision = "target_or_bridge_claim_without_source_theorem"
        missing = "source-stage finite value/divisor theorem"
        ready = False
    elif not framed:
        decision = "source_stage_win_danger3_framing_missing"
        missing = "DANGER3 finite-identity / non-CM framing"
        ready = False
    elif not same_j and not order8112 and not direct_surface and not x0:
        decision = "framed_source_same_j_bridge_missing"
        missing = "same-j X_1(8112) bridge or equivalent fiber product"
        ready = False
    elif same_j and not order8112 and not direct_surface and not x0:
        decision = "same_j_components_order8112_or_x16_missing"
        missing = "order-8112 generator, same-curve P16/Q507 pair, or direct X_1(16) payload"
        ready = False
    elif order8112 and not y and not root and not direct_surface and not x0:
        decision = "order8112_bridge_x16_surface_missing"
        missing = "X_1(16) y/model-root/A/xP16 surface or direct A,xP16"
        ready = False
    elif y and not root and not direct_surface:
        decision = "x16_y_chart_missing_model_root"
        missing = "model root x satisfying the X_1(16) quadratic"
        ready = False
    elif dgate and not x_chain and not x0:
        decision = "optional_depth5_surface_reached_halving_missing"
        missing = "37-link halving chain from x32 to x0 or direct x0"
        ready = False
    elif (root or direct_surface) and not x_chain and not x0:
        decision = "active_surface_reached_halving_missing"
        missing = "38-link halving chain from xP16 to x0 or direct x0"
        ready = False
    elif x_chain and not vpp:
        decision = "checkable_x_chain_vpp_missing"
        missing = "official src/vpp.py verification"
        ready = False
    elif x0 and not vpp:
        decision = "extraction_ready_vpp_missing"
        missing = "official src/vpp.py verification"
        ready = False
    else:
        decision = "repair_incomplete_extraction_payload"
        missing = "source theorem, bridge, X_1(16) surface, halving/x0, or vpp.py"
        ready = False

    return ExtractionPayloadRow(
        name=name,
        payload_shape=payload_shape,
        source_theorem=source,
        danger3_framed=framed,
        same_j_bridge=same_j,
        independent_components=independent,
        same_j_invariant_only=same_j_invariant,
        order8112_generator=order8112,
        x16_y=y,
        model_root_x=root,
        direct_A_xP16=direct_surface,
        optional_dgate_surface=dgate,
        branch_word_only=branch_word,
        x_chain=x_chain,
        direct_x0=x0,
        official_vpp=vpp,
        decision=decision,
        first_missing_or_falsifier=missing,
        submission_ready=ready,
        ok=True,
    )


def payload_rows() -> tuple[ExtractionPayloadRow, ...]:
    return (
        payload_row("source_theorem_no_framing", "source theorem for one legal row", source=True),
        payload_row(
            "framed_source_no_bridge",
            "DANGER3-framed finite identity with no same-j bridge",
            source=True,
            framed=True,
        ),
        payload_row(
            "independent_p16_q507",
            "independent X_1(16) and odd-level data with no same-j proof",
            source=True,
            framed=True,
            independent=True,
        ),
        payload_row(
            "same_j_invariant_only",
            "matching j-invariant or isomorphism class but no glued torsion points",
            source=True,
            framed=True,
            same_j_invariant=True,
        ),
        payload_row(
            "same_j_components_no_surface",
            "same-curve P16/Q507 bridge but no X_1(16) chart payload",
            source=True,
            framed=True,
            same_j=True,
        ),
        payload_row(
            "order8112_generator_only",
            "order-8112 generator R tied to Q507 but no practical chart data",
            source=True,
            framed=True,
            same_j=True,
            order8112=True,
        ),
        payload_row(
            "x16_y_only",
            "same-j bridge emits X_1(16) y but no model root",
            source=True,
            framed=True,
            same_j=True,
            order8112=True,
            y=True,
        ),
        payload_row(
            "x16_y_model_root_surface",
            "same-j bridge emits y, model root x, A, and xP16",
            source=True,
            framed=True,
            same_j=True,
            order8112=True,
            y=True,
            root=True,
            direct_surface=True,
        ),
        payload_row(
            "direct_A_xP16_surface",
            "bridge emits direct practical A and xP16",
            source=True,
            framed=True,
            direct_surface=True,
        ),
        payload_row(
            "optional_dgate_surface",
            "bridge emits optional d-gate first-half surface",
            source=True,
            framed=True,
            same_j=True,
            order8112=True,
            y=True,
            root=True,
            direct_surface=True,
            dgate=True,
        ),
        payload_row(
            "branch_word_without_values",
            "halving branch word without square-root witnesses or x-values",
            source=True,
            framed=True,
            direct_surface=True,
            branch_word=True,
        ),
        payload_row(
            "x_coordinate_chain",
            "A,xP16 plus 39-point x-coordinate chain x4..x42",
            source=True,
            framed=True,
            direct_surface=True,
            x_chain=True,
            x0=True,
        ),
        payload_row(
            "direct_A_x0",
            "direct A,x0 extraction",
            source=True,
            framed=True,
            x0=True,
        ),
        payload_row(
            "official_vpp_verified_triple",
            "official vpp.py verifies concrete p25 (p,A,x0)",
            source=True,
            framed=True,
            x0=True,
            vpp=True,
        ),
    )


def build_contract() -> ExtractionPayloadContract:
    markers = evidence_markers()
    sqrt_floor, hasse_bound, k = compute_k_and_bound(P25)
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    p16_multiplier = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    q507_multiplier = (X16_LEVEL * inv_16) % CROSS_LEVEL
    rows = payload_rows()
    markers_ok = sum(row.ok for row in markers)
    bridge_rows = sum(row.same_j_bridge or row.order8112_generator for row in rows)
    x16_rows = sum(row.model_root_x or row.direct_A_xP16 for row in rows)
    optional_rows = sum(row.optional_dgate_surface for row in rows)
    extraction_ready = sum(row.x_chain or row.direct_x0 for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    repair_rows = sum(
        row.decision.startswith("source_")
        or row.decision.startswith("repair_")
        or row.decision.startswith("framed_")
        or row.decision.startswith("same_j_")
        or row.decision.startswith("order8112_")
        or row.decision.startswith("x16_")
        or row.decision.startswith("active_")
        or row.decision.startswith("optional_")
        or row.decision.startswith("checkable_")
        or row.decision.startswith("extraction_")
        for row in rows
    )
    reject_rows = sum(row.decision.startswith("reject_") for row in rows)
    current_live = 0
    expected_decisions = (
        "source_stage_win_danger3_framing_missing",
        "framed_source_same_j_bridge_missing",
        "reject_unglued_components",
        "repair_same_j_invariant_only",
        "same_j_components_order8112_or_x16_missing",
        "order8112_bridge_x16_surface_missing",
        "x16_y_chart_missing_model_root",
        "active_surface_reached_halving_missing",
        "active_surface_reached_halving_missing",
        "optional_depth5_surface_reached_halving_missing",
        "reject_branch_word_without_values",
        "checkable_x_chain_vpp_missing",
        "extraction_ready_vpp_missing",
        "submission_ready",
    )
    row_ok = (
        markers_ok == len(markers)
        and P25 % 8 == 5
        and sqrt_floor == 3_162_277_660_168
        and k == 42
        and hasse_bound.bit_length() == 42
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and inv_507 == 3
        and inv_16 == 412
        and p16_multiplier == 1521
        and q507_multiplier == 6592
        and (p16_multiplier + q507_multiplier) % CROSS_LEVEL == 1
        and order_of_multiple(CROSS_LEVEL, p16_multiplier) == X16_LEVEL
        and order_of_multiple(CROSS_LEVEL, q507_multiplier) == ODD_LEVEL
        and ACTIVE_START_DEPTH == 4
        and OPTIONAL_DGATE_START_DEPTH == 5
        and k - ACTIVE_START_DEPTH == 38
        and k - OPTIONAL_DGATE_START_DEPTH == 37
        and len(rows) == 14
        and tuple(row.decision for row in rows) == expected_decisions
        and bridge_rows == 5
        and x16_rows == 5
        and optional_rows == 1
        and extraction_ready == 3
        and submission_ready == 1
        and repair_rows == 11
        and reject_rows == 2
        and current_live == 0
        and all(row.ok for row in rows)
    )
    return ExtractionPayloadContract(
        evidence_markers=markers,
        p_mod_8=P25 % 8,
        sqrt_floor=sqrt_floor,
        hasse_bound=hasse_bound,
        k=k,
        levels_coprime=gcd(X16_LEVEL, ODD_LEVEL) == 1,
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        p16_multiplier=p16_multiplier,
        q507_multiplier=q507_multiplier,
        projection_sum_mod_8112=(p16_multiplier + q507_multiplier) % CROSS_LEVEL,
        p16_order=order_of_multiple(CROSS_LEVEL, p16_multiplier),
        q507_order=order_of_multiple(CROSS_LEVEL, q507_multiplier),
        active_mode=ACTIVE_MODE,
        active_start_depth=ACTIVE_START_DEPTH,
        active_halving_links=k - ACTIVE_START_DEPTH,
        active_x_chain_points=k - ACTIVE_START_DEPTH + 1,
        optional_mode=OPTIONAL_DGATE_MODE,
        optional_start_depth=OPTIONAL_DGATE_START_DEPTH,
        optional_halving_links=k - OPTIONAL_DGATE_START_DEPTH,
        rows=rows,
        evidence_markers_ok=markers_ok,
        bridge_stage_rows=bridge_rows,
        x16_surface_rows=x16_rows,
        optional_dgate_rows=optional_rows,
        extraction_ready_rows=extraction_ready,
        submission_ready_rows=submission_ready,
        repair_rows=repair_rows,
        reject_rows=reject_rows,
        current_live_payload_rows=current_live,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_contract()
    for row in profile.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  sqrt_floor={profile.sqrt_floor}")
    print(f"  hasse_bound={profile.hasse_bound}")
    print(f"  k={profile.k}")
    print(f"  levels_coprime={int(profile.levels_coprime)}")
    print(f"  inv_507_mod_16={profile.inv_507_mod_16}")
    print(f"  inv_16_mod_507={profile.inv_16_mod_507}")
    print(f"  p16_multiplier={profile.p16_multiplier}")
    print(f"  q507_multiplier={profile.q507_multiplier}")
    print(f"  projection_sum_mod_8112={profile.projection_sum_mod_8112}")
    print(f"  p16_order={profile.p16_order}")
    print(f"  q507_order={profile.q507_order}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  active_start_depth={profile.active_start_depth}")
    print(f"  active_halving_links={profile.active_halving_links}")
    print(f"  active_x_chain_points={profile.active_x_chain_points}")
    print(f"  optional_mode={profile.optional_mode}")
    print(f"  optional_start_depth={profile.optional_start_depth}")
    print(f"  optional_halving_links={profile.optional_halving_links}")
    print("payload_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source={int(row.source_theorem)} framed={int(row.danger3_framed)} "
            f"same_j={int(row.same_j_bridge)} "
            f"same_j_invariant={int(row.same_j_invariant_only)} "
            f"order8112={int(row.order8112_generator)} "
            f"y={int(row.x16_y)} root={int(row.model_root_x)} "
            f"A_xP16={int(row.direct_A_xP16)} x_chain={int(row.x_chain)} "
            f"x0={int(row.direct_x0)} vpp={int(row.official_vpp)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}/{len(profile.evidence_markers)}")
    print(f"  bridge_stage_rows={profile.bridge_stage_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  optional_dgate_rows={profile.optional_dgate_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print(f"  repair_rows={profile.repair_rows}")
    print(f"  reject_rows={profile.reject_rows}")
    print(f"  current_live_payload_rows={profile.current_live_payload_rows}")
    print("interpretation")
    print("  source_theorem_hit_still_needs_framing_bridge_x16_halving_and_vpp=1")
    print("  independent_p16_q507_components_are_rejected_without_same_j_gluing=1")
    print("  active_x16_payload_is_A_xP16_or_y_plus_model_root=1")
    print("  optional_dgate_surface_is_not_required_for_current_production=1")
    print("  official_vpp_py_remains_submission_boundary=1")
    print(f"p25_v2_extraction_payload_contract_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
