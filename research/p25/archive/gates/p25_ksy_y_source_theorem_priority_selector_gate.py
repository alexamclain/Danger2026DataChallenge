#!/usr/bin/env python3
"""Priority selector for the next p25 KSY/Yang/H90 source-theorem ask."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_value_payload_reality_check_20260614.md",
        "ksy_y_value_payload_reality_check_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_minimal_theorem_query_packet_20260614.md",
        "ksy_y_conductor39_minimal_theorem_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_minimal_closing_ask_packet_20260614.md",
        "ksy_y_h0_minimal_closing_ask_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_translate_theorem_query_packet_20260614.md",
        "ksy_y_h0_translate_theorem_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_twisted_h90_minimal_closing_ask_packet_20260614.md",
        "ksy_y_twisted_h90_minimal_closing_ask_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_curved_corner_minimal_closing_ask_packet_20260614.md",
        "ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_atom_enumeration_falsifier_20260614.md",
        "ksy_y_atom_enumeration_falsifier_rows=1/1",
    ),
)


@dataclass(frozen=True)
class SourceTheoremPriorityRow:
    name: str
    source_language: str
    decision: str
    priority_rank: int
    source_stage_closes_if_yes: bool
    avoids_period_value_branch: bool
    source_object_certified: bool
    current_evidence_only: bool
    conditional: bool
    rejected: bool
    downstream_after_yes: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class SourceTheoremPriorityProfile:
    dependency_markers_present: int
    dependency_markers_total: int
    rows: tuple[SourceTheoremPriorityRow, ...]
    row_count: int
    source_closing_yes_rows: int
    priority1_rows: int
    priority2_rows: int
    source_certified_rows: int
    current_evidence_only_rows: int
    conditional_rows: int
    rejected_rows: int
    downstream_rows: int
    preferred_first_asks: tuple[str, ...]
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def priority_rows() -> tuple[SourceTheoremPriorityRow, ...]:
    return (
        SourceTheoremPriorityRow(
            name="conductor39_source_certification_only",
            source_language="X_1(39) mixed tensor source",
            decision="source_certified_value_or_divisor_missing",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=True,
            current_evidence_only=True,
            conditional=True,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="finite-field value identity or divisor/additive theorem",
            next_action="use only as the certified source object, not as closure",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="h0_source_certification_only",
            source_language="four legal H0/H0-translate products",
            decision="source_certified_value_or_divisor_missing",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=True,
            current_evidence_only=True,
            conditional=True,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="exact H0 value or divisor/additive identity",
            next_action="use Koo-Shin 6.2 legality as setup, not a win",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="h0_or_conductor39_divisor_additive_boundary_identity",
            source_language="H0/H0-translate or conductor-39 source",
            decision="priority1_source_ask",
            priority_rank=1,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=True,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="exact divisor/additive theorem with legal H90 boundary",
            next_action="ask sources/experts for a divisor or additive identity before value branches",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="twisted_h90_divisor_identity",
            source_language="twisted ratio / Hilbert-90 boundary",
            decision="priority1_source_ask",
            priority_rank=1,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=True,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="finite divisor/additive theorem for the twisted/H90 object",
            next_action="route theorem snippets through twisted/H90 candidate-packet intake",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="curved_corner_divisor_additive_identity",
            source_language="unit-triangle curved K-traced corner",
            decision="priority1_source_ask",
            priority_rank=1,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=True,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="finite divisor/additive theorem for the exact unit-triangle curved corner",
            next_action="route through curved-corner producer intake, then DANGER3 framing",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="exact_p_value_with_period156_context",
            source_language="exact P, Y_507, or legal H0 value",
            decision="priority2_source_ask",
            priority_rank=2,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=False,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="period-156 branch/root/telescoping context",
            next_action="accept only with exact object, mixed graph/boundary, finite identity, and period-156 context",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="twisted_h90_value_with_period156_context",
            source_language="twisted ratio / Hilbert-90 value",
            decision="priority2_source_ask",
            priority_rank=2,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=False,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="finite value theorem plus period-156 branch/root/telescoping context",
            next_action="route through twisted/H90 source classifier and then DANGER3 framing",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="curved_corner_value_with_period156_context",
            source_language="unit-triangle curved K-traced corner value",
            decision="priority2_source_ask",
            priority_rank=2,
            source_stage_closes_if_yes=True,
            avoids_period_value_branch=False,
            source_object_certified=True,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="finite value theorem plus period-156 context for the curved corner",
            next_action="accept only with unit-triangle payload, period-156 context, and arithmetic source theorem",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="finite_payload_fixture_without_source",
            source_language="finite verifier payload",
            decision="conditional_finite_payload_without_source_theorem",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=False,
            current_evidence_only=True,
            conditional=True,
            rejected=False,
            downstream_after_yes=False,
            first_missing_or_falsifier="challenge-legal arithmetic source theorem",
            next_action="use as exact target fixture only",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="ambient_780_value",
            source_language="ambient value shadow",
            decision="reject_ambient_780_mu11_branch",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=False,
            current_evidence_only=True,
            conditional=False,
            rejected=True,
            downstream_after_yes=False,
            first_missing_or_falsifier="gcd(4^780 - 1, p - 1) = 11",
            next_action="discard unless descended to support period 156",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="literal_75_atom_enumeration",
            source_language="misread exact-P atom list",
            decision="reject_atom_enumeration_not_a_route",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=False,
            current_evidence_only=True,
            conditional=False,
            rejected=True,
            downstream_after_yes=False,
            first_missing_or_falsifier="75 atoms are fixed product factors, not 75 candidate tries",
            next_action="replace with an all-75 product identity or verified concrete payload",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="generic_generation_or_cm_language",
            source_language="generic generator / CM provenance",
            decision="reject_generic_generation_not_source_closure",
            priority_rank=0,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=False,
            current_evidence_only=True,
            conditional=False,
            rejected=True,
            downstream_after_yes=False,
            first_missing_or_falsifier="exact p25 finite product/value/divisor identity",
            next_action="keep only as vocabulary",
            ok=True,
        ),
        SourceTheoremPriorityRow(
            name="after_source_yes",
            source_language="DANGER3 / extraction",
            decision="downstream_not_a_source_search",
            priority_rank=3,
            source_stage_closes_if_yes=False,
            avoids_period_value_branch=False,
            source_object_certified=False,
            current_evidence_only=False,
            conditional=False,
            rejected=False,
            downstream_after_yes=True,
            first_missing_or_falsifier="DANGER3 framing, same-j bridge, X_1(16), A,x0, official vpp.py",
            next_action="run only after a source-stage yes or practical hit",
            ok=True,
        ),
    )


def profile_source_theorem_priority_selector() -> SourceTheoremPriorityProfile:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    rows = priority_rows()
    source_yes = sum(row.source_stage_closes_if_yes for row in rows)
    priority1 = sum(row.priority_rank == 1 for row in rows)
    priority2 = sum(row.priority_rank == 2 for row in rows)
    certified = sum(row.source_object_certified for row in rows)
    evidence_only = sum(row.current_evidence_only for row in rows)
    conditional = sum(row.conditional for row in rows)
    rejected = sum(row.rejected for row in rows)
    downstream = sum(row.downstream_after_yes for row in rows)
    preferred = tuple(row.name for row in rows if row.priority_rank == 1)
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and len(rows) == 13
        and source_yes == 6
        and priority1 == 3
        and priority2 == 3
        and certified == 8
        and evidence_only == 6
        and conditional == 3
        and rejected == 3
        and downstream == 1
        and preferred
        == (
            "h0_or_conductor39_divisor_additive_boundary_identity",
            "twisted_h90_divisor_identity",
            "curved_corner_divisor_additive_identity",
        )
        and all(row.ok for row in rows)
    )
    return SourceTheoremPriorityProfile(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        rows=rows,
        row_count=len(rows),
        source_closing_yes_rows=source_yes,
        priority1_rows=priority1,
        priority2_rows=priority2,
        source_certified_rows=certified,
        current_evidence_only_rows=evidence_only,
        conditional_rows=conditional,
        rejected_rows=rejected,
        downstream_rows=downstream,
        preferred_first_asks=preferred,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_source_theorem_priority_selector()
    print("p25 KSY-y source-theorem priority selector gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print("priority_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: lang={row.source_language} decision={row.decision} "
            f"rank={row.priority_rank} "
            f"closes={int(row.source_stage_closes_if_yes)} "
            f"avoids_value_branch={int(row.avoids_period_value_branch)} "
            f"certified={int(row.source_object_certified)} "
            f"evidence_only={int(row.current_evidence_only)} "
            f"conditional={int(row.conditional)} "
            f"rejected={int(row.rejected)} "
            f"downstream={int(row.downstream_after_yes)} "
            f"missing={row.first_missing_or_falsifier}"
        )
        print(f"    next={row.next_action}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  source_closing_yes_rows={profile.source_closing_yes_rows}")
    print(f"  priority1_rows={profile.priority1_rows}")
    print(f"  priority2_rows={profile.priority2_rows}")
    print(f"  source_certified_rows={profile.source_certified_rows}")
    print(f"  current_evidence_only_rows={profile.current_evidence_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  downstream_rows={profile.downstream_rows}")
    print(f"  preferred_first_asks={profile.preferred_first_asks}")
    print("interpretation")
    print("  prioritize_divisor_or_additive_identities_before_value_branches=1")
    print("  keep_exact_value_routes_only_with_period156_context=1")
    print("  finite_payloads_and_source_certification_are_not_source_closure=1")
    print(f"ksy_y_source_theorem_priority_selector_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("source-theorem priority selector regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
