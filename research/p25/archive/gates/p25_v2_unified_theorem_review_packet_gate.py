#!/usr/bin/env python3
"""Build the v2 expert-review packet for the unified theorem gap.

This gate does not claim a source theorem exists.  It freezes the exact
statement an expert or source snippet would need to address: one of four legal
support-156 products, a Norm_156(Y_507) boundary, and either a divisor/additive
identity or a period-156 value identity with branch/telescoping control.
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
class TargetRow:
    m: int
    source_h0: str
    source_conductor39: str
    constants: tuple[int, int, int, int]
    positive_residues: tuple[int, ...]
    negative_residues: tuple[int, ...]
    lifted_positive_factors: int
    lifted_negative_factors: int
    boundary: str
    ok: bool


@dataclass(frozen=True)
class ReviewClause:
    name: str
    role: str
    statement: str
    accepted: bool
    required_for_source_stage: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ExpertAsk:
    name: str
    question: str
    would_count_as_progress: str
    stop_sign: str
    priority: int
    ok: bool


@dataclass(frozen=True)
class ReviewPacket:
    evidence_markers: tuple[EvidenceMarker, ...]
    target_rows: tuple[TargetRow, ...]
    clauses: tuple[ReviewClause, ...]
    asks: tuple[ExpertAsk, ...]
    evidence_markers_ok: int
    target_rows_ok: int
    accepted_source_stage_clauses: int
    current_source_theorems: int
    submission_ready_rows: int
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
            "source_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "hidden_selector_or_gauge_freedom_remaining = no",
        ),
        marker(
            "value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
        marker(
            "source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "research/p25/evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
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
            "submission_extraction",
            "research/p25/evidence/p25_v2_unified_submission_extraction_contract_20260616.md",
            "p25_v2_unified_submission_extraction_contract_rows=1/1",
        ),
        marker(
            "orbit_minimality",
            "research/p25/evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md",
            "p25_v2_conductor39_doubling_orbit_minimality_rows=1/1",
        ),
        marker(
            "theorem52_constant_span_obstruction",
            "research/p25/evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
            "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "additive_normalizer_source_scan",
            "research/p25/evidence/p25_v2_additive_normalizer_source_scan_20260616.md",
            "p25_v2_additive_normalizer_source_scan_rows=1/1",
        ),
    )


def target_rows() -> tuple[TargetRow, ...]:
    return (
        TargetRow(
            m=1,
            source_h0="canonical_H0",
            source_conductor39="legal_sparse_selector_0",
            constants=(3, 3, -3, -3),
            positive_residues=(7, 17, 23, 34, 37, 38),
            negative_residues=(4, 8, 10, 11, 20, 25),
            lifted_positive_factors=78,
            lifted_negative_factors=78,
            boundary="Norm_156(Y_507)",
            ok=True,
        ),
        TargetRow(
            m=2,
            source_h0="H0_translate",
            source_conductor39="legal_sparse_selector_2",
            constants=(-3, 3, 3, -3),
            positive_residues=(7, 14, 29, 34, 35, 37),
            negative_residues=(1, 8, 11, 16, 20, 22),
            lifted_positive_factors=78,
            lifted_negative_factors=78,
            boundary="Norm_156(Y_507)",
            ok=True,
        ),
        TargetRow(
            m=4,
            source_h0="H0_translate",
            source_conductor39="legal_sparse_selector_3",
            constants=(-3, -3, 3, 3),
            positive_residues=(14, 19, 28, 29, 31, 35),
            negative_residues=(1, 2, 5, 16, 22, 32),
            lifted_positive_factors=78,
            lifted_negative_factors=78,
            boundary="Norm_156(Y_507)",
            ok=True,
        ),
        TargetRow(
            m=8,
            source_h0="H0_translate",
            source_conductor39="legal_sparse_selector_1",
            constants=(3, -3, -3, 3),
            positive_residues=(17, 19, 23, 28, 31, 38),
            negative_residues=(2, 4, 5, 10, 25, 32),
            lifted_positive_factors=78,
            lifted_negative_factors=78,
            boundary="Norm_156(Y_507)",
            ok=True,
        ),
    )


def review_clauses() -> tuple[ReviewClause, ...]:
    return (
        ReviewClause(
            name="target_object",
            role="required_target",
            statement=(
                "Choose one m in {1,2,4,8}; prove the theorem for the matching "
                "legal support-156, 78-over-78 H0/conductor-39 product row."
            ),
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier="row not equal to one of the four legal products",
            ok=True,
        ),
        ReviewClause(
            name="divisor_additive_closer",
            role="preferred_source_stage_closer",
            statement=(
                "Arithmetic finite divisor/additive identity for that row, with "
                "(1-Frob_p)H = Norm_156(Y_507)."
            ),
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier="identity absent, boundary absent, or scalar-fixing additive/value data absent",
            ok=True,
        ),
        ReviewClause(
            name="additive_normalization_required",
            role="required_normalization",
            statement=(
                "The additive side must fix the invisible F_p^* scalar by a "
                "finite additive/value/basepoint/branch/telescoping datum."
            ),
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier="principal-divisor, divisor-class, dense additive, or up-to-scalar statement only",
            ok=True,
        ),
        ReviewClause(
            name="quartic_character_closer",
            role="accepted_source_stage_closer",
            statement=(
                "If the theorem is stated in character/projector language, it "
                "must provide W boundary, exact row-antisymmetric C4_1 phase, "
                "mixed tensor row sign, oriented row/boundary-sign convention, "
                "arithmetic source theorem, and the same scalar-fixed finite "
                "divisor/additive identity."
            ),
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier=(
                "coarse quartic phase, magnitude/quadratic data, missing row sign, "
                "wrong reciprocal boundary sign, or selector data without finite theorem"
            ),
            ok=True,
        ),
        ReviewClause(
            name="period156_value_closer",
            role="accepted_source_stage_closer",
            statement=(
                "Finite value identity for that row with period-156 "
                "branch/root/telescoping context and Norm_156(Y_507) boundary."
            ),
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier="ambient period-780 or branch-free value statement",
            ok=True,
        ),
        ReviewClause(
            name="source_theorem",
            role="required_provenance",
            statement="The identity must be emitted by an arithmetic source theorem.",
            accepted=True,
            required_for_source_stage=True,
            first_missing_or_falsifier="finite-payload computation with no source theorem",
            ok=True,
        ),
        ReviewClause(
            name="source_legality_only",
            role="reject",
            statement="Koo-Shin/Yang legality or unit generation without value/divisor content.",
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="finite value/divisor theorem",
            ok=True,
        ),
        ReviewClause(
            name="boundary_only",
            role="reject",
            statement="Hilbert-90 or Norm_156 boundary without identity for a legal row.",
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="finite value/divisor identity for the row",
            ok=True,
        ),
        ReviewClause(
            name="up_to_scalar_or_divisor_class_only",
            role="repair",
            statement=(
                "Divisor/H90 or additive/value statement only up to an unspecified "
                "F_p^* scalar, or only as a principal-divisor/divisor-class equality."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="scalar-fixing finite additive/value/basepoint/telescoping datum",
            ok=True,
        ),
        ReviewClause(
            name="projection_or_suborbit",
            role="reject",
            statement="Prime-axis projection, one-coset gauge, or proper doubling suborbit.",
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="lost mixed tensor or failed standalone X_1(39) legality",
            ok=True,
        ),
        ReviewClause(
            name="quartic_selector_without_theorem",
            role="repair",
            statement="Exact C4_1 selector or edge phase data without a scalar-fixed finite theorem.",
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="finite value/divisor theorem for the selected row",
            ok=True,
        ),
        ReviewClause(
            name="coarse_quartic_or_missing_row_sign",
            role="repair",
            statement=(
                "One quartic sign, quartic magnitude, quadratic component, or "
                "quotient-C4 phase without mixed tensor row sign."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="exact row-antisymmetric C4_1 phase and mixed tensor row sign",
            ok=True,
        ),
        ReviewClause(
            name="same_parity_quartic_phase",
            role="reject",
            statement="Same-parity quartic edge or phase data.",
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="zero W boundary or wrong mixed tensor target",
            ok=True,
        ),
        ReviewClause(
            name="reciprocal_quartic_phase_wrong_boundary",
            role="repair_or_reject",
            statement=(
                "Exact C4_1 phase data stated in a reciprocal orientation, or "
                "reciprocal phase asserted with the positive Norm_156(Y_507) boundary."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier=(
                "oriented row data or reciprocal -Norm_156(Y_507) boundary; "
                "reciprocal phase with positive boundary is rejected"
            ),
            ok=True,
        ),
        ReviewClause(
            name="mu11_power_or_quotient_value",
            role="reject",
            statement=(
                "Ambient-period-780 value theorem only after taking an 11th "
                "power or quotienting by mu_11."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier=(
                "actual period-156 branch/root/telescoping data selecting one F_p value"
            ),
            ok=True,
        ),
        ReviewClause(
            name="theorem52_constant_span_repair",
            role="reject",
            statement=(
                "Koo-Shin Theorem 5.2 constant-product repair by multiplying "
                "powers of the four legal rows."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier=(
                "legal quotient-C4 row span has no nonzero constant-exponent vector"
            ),
            ok=True,
        ),
        ReviewClause(
            name="local_source_stack_as_written",
            role="repair",
            statement=(
                "Local Koo-Shin 2010, KSY 1007.2307, and Koo-Shin II extracts "
                "contain helper vocabulary but no scalar-fixing additive normalizer."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="new source snippet or expert theorem beyond the inspected extracts",
            ok=True,
        ),
        ReviewClause(
            name="post_source_extraction",
            role="downstream_boundary",
            statement=(
                "Even an accepted source theorem still needs DANGER3 framing, "
                "same-j X1(8112), X1(16), halving/direct x0, and vpp.py."
            ),
            accepted=False,
            required_for_source_stage=False,
            first_missing_or_falsifier="not submission-ready without extraction",
            ok=True,
        ),
    )


def expert_asks() -> tuple[ExpertAsk, ...]:
    return (
        ExpertAsk(
            name="primary_divisor_additive",
            question=(
                "Is there a known finite divisor/additive theorem for one legal "
                "support-156 H0/conductor-39 product with (1-Frob_p)H = Norm_156(Y_507)?"
            ),
            would_count_as_progress="named theorem or formula that emits the scalar-fixed row identity",
            stop_sign="source legality, generation, boundary, divisor-class, or up-to-scalar statement only",
            priority=1,
            ok=True,
        ),
        ExpertAsk(
            name="additive_normalization",
            question=(
                "If the theorem is divisor/additive, what datum fixes the F_p^* scalar: "
                "finite additive value, basepoint, branch/root, or telescoping product?"
            ),
            would_count_as_progress="explicit scalar-fixing normalizer for one legal row",
            stop_sign="principal divisor, divisor class, dense relation, or value only up to scalar",
            priority=2,
            ok=True,
        ),
        ExpertAsk(
            name="period156_value",
            question=(
                "Is there a period-156 value theorem with branch/root/telescoping "
                "control for the same product family?"
            ),
            would_count_as_progress="support-period value identity avoiding the mu_11 ambient ambiguity",
            stop_sign="ambient period-780 value statement with no period-156 branch control",
            priority=3,
            ok=True,
        ),
        ExpertAsk(
            name="character_selector_language",
            question=(
                "If the theorem is stated in character/projector language, does it "
                "give the exact row-antisymmetric C4_1 phase and mixed tensor row sign, "
                "not just quartic magnitude, one sign, or quadratic data?"
            ),
            would_count_as_progress="exact C4_1 selector plus row sign paired with a scalar-fixed finite theorem",
            stop_sign="selector-only, coarse phase/magnitude, missing row sign, or same-parity phase statement",
            priority=4,
            ok=True,
        ),
        ExpertAsk(
            name="source_language_equivalence",
            question=(
                "Would H0/H0-translate language or mixed U_chi/W conductor-39 "
                "language make the same finite theorem cheaper to prove?"
            ),
            would_count_as_progress="source theorem preserving one of the four finite rows",
            stop_sign="a source presentation that changes the finite target row",
            priority=5,
            ok=True,
        ),
        ExpertAsk(
            name="challenge_framing",
            question=(
                "If the theorem is class-field or unit-theoretic, can it be framed "
                "as a finite non-CM identity acceptable for DANGER3 extraction?"
            ),
            would_count_as_progress="finite-field identity framing plus downstream extraction plan",
            stop_sign="CM/source theorem with no finite identity payload",
            priority=6,
            ok=True,
        ),
    )


def build_packet() -> ReviewPacket:
    ms = evidence_markers()
    rows = target_rows()
    clauses = review_clauses()
    asks = expert_asks()
    evidence_ok = sum(m.ok for m in ms)
    target_ok = sum(r.ok for r in rows)
    accepted_source_stage = sum(c.accepted and c.required_for_source_stage for c in clauses)
    current_source_theorems = 0
    submission_ready = 0
    row_ok = (
        evidence_ok == len(ms)
        and len(rows) == 4
        and target_ok == 4
        and all(r.lifted_positive_factors == 78 and r.lifted_negative_factors == 78 for r in rows)
        and all(r.boundary == "Norm_156(Y_507)" for r in rows)
        and len(clauses) == 18
        and accepted_source_stage == 6
        and current_source_theorems == 0
        and submission_ready == 0
        and len(asks) == 6
        and [a.priority for a in asks] == [1, 2, 3, 4, 5, 6]
        and all(a.ok and a.would_count_as_progress and a.stop_sign for a in asks)
    )
    return ReviewPacket(
        evidence_markers=ms,
        target_rows=rows,
        clauses=clauses,
        asks=asks,
        evidence_markers_ok=evidence_ok,
        target_rows_ok=target_ok,
        accepted_source_stage_clauses=accepted_source_stage,
        current_source_theorems=current_source_theorems,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    packet = build_packet()
    for m in packet.evidence_markers:
        print(f"marker {m.name}: {'ok' if m.ok else 'MISSING'}")
    for row in packet.target_rows:
        print(
            f"target m={row.m}: +{row.lifted_positive_factors}/"
            f"-{row.lifted_negative_factors} boundary={row.boundary}"
        )
    for clause in packet.clauses:
        print(f"clause {clause.name}: role={clause.role} accepted={int(clause.accepted)}")
    for ask in packet.asks:
        print(f"ask p{ask.priority} {ask.name}: ok={int(ask.ok)}")
    print(f"evidence_markers_ok={packet.evidence_markers_ok}/{len(packet.evidence_markers)}")
    print(f"target_rows_ok={packet.target_rows_ok}/{len(packet.target_rows)}")
    print(f"accepted_source_stage_clauses={packet.accepted_source_stage_clauses}")
    print(f"current_source_theorems={packet.current_source_theorems}")
    print(f"submission_ready_rows={packet.submission_ready_rows}")
    print(f"p25_v2_unified_theorem_review_packet_rows={int(packet.row_ok)}/1")
    return 0 if packet.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
