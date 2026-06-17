#!/usr/bin/env python3
"""Route p25 source families against the v2 value/divisor interface.

The first-pass target is fixed.  This gate keeps the literature/source side
from drifting by separating accepted source-stage theorem shapes from source
families that currently provide only legality, vocabulary, or conditional
support.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceRoute:
    name: str
    source_family: str
    target: str
    accepted_only_if: str
    current_state: str
    decision: str
    first_falsifier: str
    active_frontdoor: bool
    heavy_route: bool
    direct_closer_in_hand: bool
    broad_reading_allowed: bool
    ok: bool


@dataclass(frozen=True)
class SourceFamilyRouter:
    evidence_markers: tuple[EvidenceMarker, ...]
    routes: tuple[SourceRoute, ...]
    evidence_markers_ok: int
    route_rows: int
    active_frontdoor_rows: int
    heavy_route_rows: int
    direct_closer_rows: int
    broad_reading_allowed_rows: int
    preferred_next_ask: str
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "unified_source_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "p25_v2_unified_source_theorem_gap_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "quartic_reciprocal_orientation",
            "research/p25/evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
            "p25_v2_quartic_reciprocal_orientation_rows=1/1",
        ),
        marker(
            "h0_conductor39_frontier_pass",
            "research/p25/evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md",
            "decision = continue_lane_but_kill_koo_shin_2010_as_closer",
        ),
        marker(
            "ksy_primary_source_verdict",
            "research/p25/evidence/p25_ksy_y_priority1_primary_source_verdict_20260613.md",
            "ksy_y_priority1_primary_source_verdict_rows=1/1",
        ),
        marker(
            "sprang_exact_specialization_frontier",
            "research/p25/evidence/p25_ksy_y_sprang_exact_specialization_frontier_20260614.md",
            "ksy_y_sprang_exact_specialization_frontier_rows=1/1",
        ),
        marker(
            "kubert_lang_boundary",
            "research/p25/evidence/p25_ksy_y_kubert_lang_visual_theorem_boundary_20260614.md",
            "ksy_y_kubert_lang_visual_theorem_boundary_rows=1/1",
        ),
        marker(
            "external_exact_product_bridge",
            "research/p25/evidence/p25_ksy_y_external_exact_product_bridge_scout_20260613.md",
            "ksy_y_external_exact_product_bridge_scout_rows=1/1",
        ),
        marker(
            "ksy_1007_2307_ingest",
            "research/p25/evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md",
            "decision = continue_as_exactp_vocabulary_not_closer",
        ),
        marker(
            "koo_shin_ii_scan",
            "research/p25/evidence/p25_v2_koo_shin_ii_first_pass_source_scan_20260616.md",
            "decision = kill_koo_shin_ii_as_h0_closer",
        ),
    )


def routes() -> tuple[SourceRoute, ...]:
    return (
        SourceRoute(
            name="unified_h0_conductor39_divisor_additive",
            source_family="Koo-Shin/Yang/Yu/Ray-class source language",
            target="one legal support-156 H0/conductor-39 product",
            accepted_only_if=(
                "finite divisor/additive theorem with Hilbert-90 boundary "
                "(1-Frob_p)H = Norm_156(Y_507)"
            ),
            current_state="target certified; no arithmetic value/divisor theorem in hand",
            decision="primary_frontdoor_ask_continue",
            first_falsifier="source legality, boundary, or product normal form without value/divisor theorem",
            active_frontdoor=True,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="period156_value_route",
            source_family="Schertz/Shin/Siegel-Robert/Scholl value-unit family",
            target="same legal support-156 product family",
            accepted_only_if=(
                "finite value identity for canonical H0 with Norm_156(Y_507) "
                "boundary, or for Y_507 with period-156 branch/root/telescoping context"
            ),
            current_state="value-unit vocabulary exists; ambient period-780 route keeps mu_11 ambiguity",
            decision="conditional_frontdoor_support_continue",
            first_falsifier="value theorem with no canonical H0/Y507 period-156 context or only ambient period-780 data",
            active_frontdoor=True,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="character_quartic_selector_route",
            source_family="H0/conductor-39 character or projector language",
            target="one legal quotient-C4 edge presented by character data",
            accepted_only_if=(
                "W boundary, exact row-antisymmetric C4_1 phase, mixed tensor "
                "row sign, oriented row/boundary-sign convention, and "
                "scalar-fixed finite value/divisor theorem"
            ),
            current_state="selector payload certified; no arithmetic finite theorem in hand",
            decision="active_frontdoor_shape_only",
            first_falsifier=(
                "coarse quartic phase, magnitude, quadratic component, missing row sign, "
                "or reciprocal phase with wrong/missing boundary sign"
            ),
            active_frontdoor=True,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="exactp_upstream_product",
            source_family="KSY/Kubert-Lang/Sprang/Scholl exact-product family",
            target="compact exact-P C,D,K,orientation or accepted period-156 theta2 payload",
            accepted_only_if="challenge-legal exact-P theorem feeding 75->300->12->312->156",
            current_state="rigid finite target known; no source theorem selecting the 75 atoms",
            decision="heavy_second_pass_continue_only_on_exact_theorem_hook",
            first_falsifier="field generation, exponent balance, or value-only statement without exact product",
            active_frontdoor=False,
            heavy_route=True,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="koo_shin_2010",
            source_family="Koo-Shin 2010",
            target="H0 and conductor-39 source legality",
            accepted_only_if="a new clause emits the exact finite value/divisor theorem",
            current_state="source-legality asset; killed as current source-stage closer",
            decision="use_as_evidence_not_broad_read",
            first_falsifier="another source-certification or ray-class-generation statement",
            active_frontdoor=False,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="koo_shin_ii_1007_2318",
            source_family="Koo-Shin II 1007.2318",
            target="background ray-class/Siegel context",
            accepted_only_if="an exact H0/conductor-39 period-156 value/divisor clause appears",
            current_state="screened negative for H0, conductor 39, period-156, and H90 terms",
            decision="background_only",
            first_falsifier="general sequel context without the p25 finite theorem",
            active_frontdoor=False,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="ksy_1007_2307",
            source_family="Koo-Shin-Yoon 1007.2307",
            target="normalized-y atom vocabulary for exact-P",
            accepted_only_if="exact 75-atom selector/product theorem with orientation and bridge",
            current_state="exact-P vocabulary; killed as H0/conductor-39 closer",
            decision="exactp_vocabulary_only",
            first_falsifier="single-value generator or field-generation theorem only",
            active_frontdoor=False,
            heavy_route=True,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="sprang_d2",
            source_family="Sprang D=2/Kronecker distribution family",
            target="exact-P finite P/theta2 divisor or value identity",
            accepted_only_if="named exact specialization emitting source packet, orientation, and K-traced payload",
            current_state="additive/differential vocabulary; broad D=2 readings screened out",
            decision="exact_specialization_only",
            first_falsifier="kernel distribution, torsion shadow, or cohomology statement without finite product",
            active_frontdoor=False,
            heavy_route=True,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="kubert_lang",
            source_family="Kubert-Lang modular-unit machinery",
            target="exact exponent/dependence control for the mixed p25 product",
            accepted_only_if="row-labeled exponent matrix tied to compact exact-P or period-156 payload",
            current_state="useful dependence language; no exact mixed selector or finite payload",
            decision="machinery_only",
            first_falsifier="generic modular-unit generation or tower torsion control only",
            active_frontdoor=False,
            heavy_route=True,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
        SourceRoute(
            name="schertz_scholl",
            source_family="Schertz/Shin/Scholl value-unit and distribution family",
            target="period-156 finite value identity or exact-product bridge",
            accepted_only_if="canonical H0/Y507 support-period branch/root/telescoping theorem; not ambient-only value data",
            current_state="value-unit context; direct Scholl D=2 import blocked by hypotheses",
            decision="period156_hook_only",
            first_falsifier="ambient period-780 claim or direct D=2 import under odd-D hypotheses",
            active_frontdoor=False,
            heavy_route=False,
            direct_closer_in_hand=False,
            broad_reading_allowed=False,
            ok=True,
        ),
    )


def build_router() -> SourceFamilyRouter:
    ms = evidence_markers()
    rs = routes()
    evidence_ok = sum(m.ok for m in ms)
    active_frontdoor = sum(r.active_frontdoor for r in rs)
    heavy = sum(r.heavy_route for r in rs)
    direct = sum(r.direct_closer_in_hand for r in rs)
    broad = sum(r.broad_reading_allowed for r in rs)
    row_ok = (
        evidence_ok == len(ms)
        and len(rs) == 10
        and active_frontdoor == 3
        and heavy == 4
        and direct == 0
        and broad == 0
        and all(r.ok and r.first_falsifier and r.accepted_only_if for r in rs)
    )
    return SourceFamilyRouter(
        evidence_markers=ms,
        routes=rs,
        evidence_markers_ok=evidence_ok,
        route_rows=len(rs),
        active_frontdoor_rows=active_frontdoor,
        heavy_route_rows=heavy,
        direct_closer_rows=direct,
        broad_reading_allowed_rows=broad,
        preferred_next_ask=(
            "finite divisor/additive theorem for one legal support-156 "
            "H0/conductor-39 product with Norm_156(Y_507) boundary, or the "
            "same theorem stated with exact C4_1 selector and orientation data"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    router = build_router()
    for m in router.evidence_markers:
        print(f"marker {m.name}: {'ok' if m.ok else 'MISSING'}")
    for r in router.routes:
        print(f"route {r.name}: {r.decision}; closer={int(r.direct_closer_in_hand)}")
    print(f"evidence_markers_ok={router.evidence_markers_ok}/{len(router.evidence_markers)}")
    print(f"route_rows={router.route_rows}")
    print(f"active_frontdoor_rows={router.active_frontdoor_rows}")
    print(f"heavy_route_rows={router.heavy_route_rows}")
    print(f"direct_closer_rows={router.direct_closer_rows}")
    print(f"broad_reading_allowed_rows={router.broad_reading_allowed_rows}")
    print(f"preferred_next_ask={router.preferred_next_ask}")
    print(f"p25_v2_value_divisor_source_family_router_rows={int(router.row_ok)}/1")
    return 0 if router.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
