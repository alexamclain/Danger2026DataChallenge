#!/usr/bin/env python3
"""Route possible post-theorem payloads toward a DANGER3 p25 submission.

The unified group-ring payload is now pinned.  This gate records what would
happen after an arithmetic theorem hits that payload: which partial payloads
are progress, which are submission-ready, and what the first missing clause is
at each stage.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd, isqrt
from pathlib import Path


P25 = 10**25 + 13
X16_LEVEL = 16
ODD_LEVEL = 507
CROSS_LEVEL = 8112
START_DEPTH = 4
FINAL_DEPTH = 42


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ExtractionRoute:
    name: str
    payload: str
    has_source_theorem: bool
    has_danger3_framing: bool
    has_same_j_bridge: bool
    has_x16_surface: bool
    has_halving_or_x0: bool
    has_vpp: bool
    decision: str
    first_missing: str
    progress: bool
    submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class PostTheoremExtractionRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    p: int
    p_mod_8: int
    k: int
    inv_507_mod_16: int
    inv_16_mod_507: int
    p16_multiplier: int
    q507_multiplier: int
    projection_sum_mod_8112: int
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    routes: tuple[ExtractionRoute, ...]
    evidence_markers_ok: int
    progress_rows: int
    current_payload_rows: int
    current_submission_ready_rows: int
    row_ok: bool


def compute_k(p: int) -> int:
    q = isqrt(p)
    bound = q + 1 + 2 * isqrt(q)
    return bound.bit_length()


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "submission_extraction_contract",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "current_submission_ready_rows = 0",
        ),
    )


def routes() -> tuple[ExtractionRoute, ...]:
    return (
        ExtractionRoute(
            name="group_ring_payload_only",
            payload="the four support-156 product rows and hashes",
            has_source_theorem=False,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
            decision="target_pinned_source_theorem_missing",
            first_missing="arithmetic finite value/divisor theorem",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="source_theorem_no_framing",
            payload="arithmetic theorem for one legal support-156 product",
            has_source_theorem=True,
            has_danger3_framing=False,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
            decision="source_stage_win_danger3_framing_missing",
            first_missing="DANGER3 finite-identity / non-CM framing",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="danger3_framed_source_no_bridge",
            payload="DANGER3-framed finite identity for the theorem hit",
            has_source_theorem=True,
            has_danger3_framing=True,
            has_same_j_bridge=False,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
            decision="framed_source_same_j_bridge_missing",
            first_missing="same-j X_1(8112) bridge or equivalent fiber product",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="same_j_bridge_no_x16",
            payload="same-curve P16/Q507 pair or order-8112 generator R",
            has_source_theorem=True,
            has_danger3_framing=True,
            has_same_j_bridge=True,
            has_x16_surface=False,
            has_halving_or_x0=False,
            has_vpp=False,
            decision="same_j_bridge_x16_surface_missing",
            first_missing="X_1(16) y/x/A/xP16 surface or direct A,xP16",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="x16_surface_no_halving",
            payload="A and xP16 on the active x16halvenonsplit surface",
            has_source_theorem=True,
            has_danger3_framing=True,
            has_same_j_bridge=True,
            has_x16_surface=True,
            has_halving_or_x0=False,
            has_vpp=False,
            decision="active_surface_reached_halving_missing",
            first_missing="38-link halving chain from depth 4 to x0 or direct x0",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="x0_extracted_vpp_missing",
            payload="concrete A and x0, or valid halving chain ending at x0",
            has_source_theorem=True,
            has_danger3_framing=True,
            has_same_j_bridge=True,
            has_x16_surface=True,
            has_halving_or_x0=True,
            has_vpp=False,
            decision="extraction_ready_vpp_missing",
            first_missing="official src/vpp.py verification",
            progress=True,
            submission_ready=False,
            ok=True,
        ),
        ExtractionRoute(
            name="official_vpp_verified_triple",
            payload="concrete p25 (p,A,x0) accepted by official vpp.py",
            has_source_theorem=True,
            has_danger3_framing=True,
            has_same_j_bridge=True,
            has_x16_surface=True,
            has_halving_or_x0=True,
            has_vpp=True,
            decision="submission_ready",
            first_missing="none",
            progress=True,
            submission_ready=True,
            ok=True,
        ),
    )


def build_router() -> PostTheoremExtractionRouter:
    inv_507 = pow(ODD_LEVEL, -1, X16_LEVEL)
    inv_16 = pow(X16_LEVEL, -1, ODD_LEVEL)
    p16 = (ODD_LEVEL * inv_507) % CROSS_LEVEL
    q507 = (X16_LEVEL * inv_16) % CROSS_LEVEL
    projection_sum = (p16 + q507) % CROSS_LEVEL
    ms = evidence_markers()
    rs = routes()
    evidence_ok = sum(m.ok for m in ms)
    progress = sum(r.progress for r in rs)
    current_payload_rows = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(ms)
        and P25 % 8 == 5
        and compute_k(P25) == 42
        and gcd(X16_LEVEL, ODD_LEVEL) == 1
        and CROSS_LEVEL == X16_LEVEL * ODD_LEVEL
        and inv_507 == 3
        and inv_16 == 412
        and p16 == 1521
        and q507 == 6592
        and projection_sum == 1
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and FINAL_DEPTH - START_DEPTH == 38
        and FINAL_DEPTH - START_DEPTH + 1 == 39
        and len(rs) == 7
        and progress == 7
        and sum(r.submission_ready for r in rs) == 1
        and rs[-1].decision == "submission_ready"
        and current_payload_rows == 0
        and current_submission_ready == 0
        and all(r.ok and r.first_missing for r in rs)
    )
    return PostTheoremExtractionRouter(
        evidence_markers=ms,
        p=P25,
        p_mod_8=P25 % 8,
        k=compute_k(P25),
        inv_507_mod_16=inv_507,
        inv_16_mod_507=inv_16,
        p16_multiplier=p16,
        q507_multiplier=q507,
        projection_sum_mod_8112=projection_sum,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=FINAL_DEPTH - START_DEPTH,
        x_chain_points=FINAL_DEPTH - START_DEPTH + 1,
        routes=rs,
        evidence_markers_ok=evidence_ok,
        progress_rows=progress,
        current_payload_rows=current_payload_rows,
        current_submission_ready_rows=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    for m in router.evidence_markers:
        print(f"marker {m.name}: {'ok' if m.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  p_mod_8={router.p_mod_8}")
    print(f"  k={router.k}")
    print(f"  inv_507_mod_16={router.inv_507_mod_16}")
    print(f"  inv_16_mod_507={router.inv_16_mod_507}")
    print(f"  p16_multiplier={router.p16_multiplier}")
    print(f"  q507_multiplier={router.q507_multiplier}")
    print(f"  projection_sum_mod_8112={router.projection_sum_mod_8112}")
    print(f"  halving_links={router.halving_links}")
    print(f"  x_chain_points={router.x_chain_points}")
    print("routes")
    for row in router.routes:
        print(
            "  "
            f"{row.name}: decision={row.decision} missing={row.first_missing} "
            f"submission={int(row.submission_ready)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={router.evidence_markers_ok}/{len(router.evidence_markers)}")
    print(f"  progress_rows={router.progress_rows}")
    print(f"  current_payload_rows={router.current_payload_rows}")
    print(f"  current_submission_ready_rows={router.current_submission_ready_rows}")
    print(f"p25_v2_post_theorem_extraction_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
