#!/usr/bin/env python3
"""Theorem-query packet for the legal H0-translate source obligation.

The source-obligation gate says what kind of theorem would close the upstream
H0-translate stage.  This packet turns that into an expert/search query
surface: exact positive answer shapes, first falsifiers, and the local smoke
row that already classifies each answer shape.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_translate_source_obligation_gate import (
    H0TranslateSourceObligationRow,
    profile_h0_translate_source_obligation,
)


@dataclass(frozen=True)
class H0TranslateTheoremQueryRow:
    name: str
    theorem_query: str
    accepted_answer_shape: str
    source_obligation_row: str
    expected_decision: str
    actual_decision: str
    source_theorem_closes: bool
    downstream_relevant: bool
    first_falsifier: str
    continue_recommendation: str
    ok: bool


@dataclass(frozen=True)
class H0TranslateTheoremQueryPacket:
    source_obligation_ok: bool
    query_rows: tuple[H0TranslateTheoremQueryRow, ...]
    query_count: int
    source_closing_yes_rows: int
    source_certification_only_rows: int
    conditional_rows: int
    rejected_rows: int
    downstream_relevant_rows: int
    submission_ready_rows: int
    row_ok: bool


def row_by_name(
    rows: tuple[H0TranslateSourceObligationRow, ...],
    name: str,
) -> H0TranslateSourceObligationRow:
    return next(row for row in rows if row.name == name)


def query_row(
    *,
    name: str,
    theorem_query: str,
    accepted_answer_shape: str,
    obligation_row: H0TranslateSourceObligationRow,
    source_theorem_closes: bool,
    downstream_relevant: bool,
    first_falsifier: str,
    continue_recommendation: str,
) -> H0TranslateTheoremQueryRow:
    return H0TranslateTheoremQueryRow(
        name=name,
        theorem_query=theorem_query,
        accepted_answer_shape=accepted_answer_shape,
        source_obligation_row=obligation_row.name,
        expected_decision=obligation_row.expected_decision,
        actual_decision=obligation_row.actual_decision,
        source_theorem_closes=source_theorem_closes,
        downstream_relevant=downstream_relevant,
        first_falsifier=first_falsifier,
        continue_recommendation=continue_recommendation,
        ok=(
            obligation_row.ok
            and obligation_row.source_theorem_closes == source_theorem_closes
            and obligation_row.expected_decision == obligation_row.actual_decision
        ),
    )


def query_rows(
    obligation_rows: tuple[H0TranslateSourceObligationRow, ...]
) -> tuple[H0TranslateTheoremQueryRow, ...]:
    source_only = row_by_name(obligation_rows, "koo_shin_62_certifies_w_source_only")
    boundary_only = row_by_name(obligation_rows, "legal_h0_translate_boundary_only")
    value_missing_period = row_by_name(obligation_rows, "legal_h0_translate_value_missing_period156")
    value_period = row_by_name(obligation_rows, "legal_h0_translate_value_period156")
    divisor_boundary = row_by_name(obligation_rows, "legal_h0_translate_divisor_boundary")
    verifier_no_source = row_by_name(obligation_rows, "legal_h0_translate_finite_payload_no_source")
    nonlegal = row_by_name(obligation_rows, "nonlegal_h0_translate_source_claim")
    formal = row_by_name(obligation_rows, "formal_one_coset_h_source_claim")
    return (
        query_row(
            name="ask_norm156_y507_value_or_divisor",
            theorem_query=(
                "Does a source theorem evaluate or identify Norm_156(Y_507), "
                "not merely certify the conductor-39 word W?"
            ),
            accepted_answer_shape=(
                "finite-field value identity with period-156 context, or "
                "divisor/additive identity, tied to the certified conductor-39 source"
            ),
            obligation_row=source_only,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="answer only cites Koo-Shin 6.2 source certification for W",
            continue_recommendation="continue only if upgraded to value/divisor content",
        ),
        query_row(
            name="ask_boundary_only_h0_translate",
            theorem_query=(
                "Does the theorem only produce a legal H0 translate and its "
                "Hilbert-90 boundary to Norm_156(Y_507)?"
            ),
            accepted_answer_shape=(
                "useful target identification, but not source closure without "
                "a finite-field value or divisor/additive theorem"
            ),
            obligation_row=boundary_only,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="claim stops at (1-Frob_p)H0=Norm_156(Y_507)",
            continue_recommendation="ask for exact value/divisor identity for the same legal H0 product",
        ),
        query_row(
            name="ask_value_missing_period156",
            theorem_query=(
                "Does the theorem give a finite value for a legal H0 translate "
                "without period-156 branch/root/telescoping control?"
            ),
            accepted_answer_shape=(
                "conditional verifier payload; still needs period-156 context "
                "before the F_p branch is unique"
            ),
            obligation_row=value_missing_period,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="ambient-period or bare value statement",
            continue_recommendation="ask for support-period 156 fixedness or equivalent branch data",
        ),
        query_row(
            name="ask_value_with_period156",
            theorem_query=(
                "Does the theorem give an exact finite-field value identity for "
                "one legal H0 product with period-156 context?"
            ),
            accepted_answer_shape=(
                "source-stage closer; next blocker is DANGER3 finite-identity/non-CM framing"
            ),
            obligation_row=value_period,
            source_theorem_closes=True,
            downstream_relevant=True,
            first_falsifier="wrong product, missing legal translate, or missing period-156 context",
            continue_recommendation="route immediately to DANGER3 framing and X1(8112)/X1(16) extraction",
        ),
        query_row(
            name="ask_divisor_additive_identity",
            theorem_query=(
                "Does the theorem give an exact divisor/additive identity for "
                "one legal H0 product with the Hilbert-90 boundary?"
            ),
            accepted_answer_shape=(
                "source-stage closer without a multiplicative value branch; "
                "next blocker is DANGER3 finite-identity/non-CM framing"
            ),
            obligation_row=divisor_boundary,
            source_theorem_closes=True,
            downstream_relevant=True,
            first_falsifier="identity is for a formal H, projection, or nonlegal sparse gauge",
            continue_recommendation="route immediately to DANGER3 framing and X1(8112)/X1(16) extraction",
        ),
        query_row(
            name="ask_finite_payload_without_source",
            theorem_query=(
                "Is the answer only a computed finite payload or verifier table "
                "for a legal H0 translate?"
            ),
            accepted_answer_shape=(
                "diagnostic payload only; it needs a challenge-legal arithmetic source theorem"
            ),
            obligation_row=verifier_no_source,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="finite computation is not emitted by a theorem",
            continue_recommendation="keep as verifier data, but do not call source closed",
        ),
        query_row(
            name="reject_nonlegal_h0_translate",
            theorem_query="Does the proposed H0 translate fail legal Yang/H90 selection?",
            accepted_answer_shape="reject before source or X1 routing",
            obligation_row=nonlegal,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="fails Yang/Yu legality or legal sparse H90 selector",
            continue_recommendation="discard unless remapped to one of the four legal products",
        ),
        query_row(
            name="reject_formal_one_coset_h",
            theorem_query="Is the proposed H object a formal one-coset H lookalike?",
            accepted_answer_shape="reject before source or X1 routing",
            obligation_row=formal,
            source_theorem_closes=False,
            downstream_relevant=False,
            first_falsifier="target is formal_one_coset_H rather than exact P/Y507/H0/U_chi",
            continue_recommendation="discard as a closer",
        ),
    )


def profile_h0_translate_theorem_query_packet() -> H0TranslateTheoremQueryPacket:
    obligation = profile_h0_translate_source_obligation()
    rows = query_rows(obligation.source_rows)
    source_closing_yes = sum(row.source_theorem_closes for row in rows)
    source_only = sum(row.actual_decision == "period_norm_source_certified_theorem_missing" for row in rows)
    conditional = sum(row.actual_decision.startswith(("conditional_", "live_target_identified_")) for row in rows)
    rejected = sum(row.actual_decision.startswith("reject_") for row in rows)
    downstream = sum(row.downstream_relevant for row in rows)
    submission_ready = 0
    row_ok = (
        obligation.row_ok
        and len(rows) == 8
        and source_closing_yes == 2
        and source_only == 1
        and conditional == 3
        and rejected == 2
        and downstream == 2
        and submission_ready == 0
        and tuple(row.actual_decision for row in rows)
        == (
            "period_norm_source_certified_theorem_missing",
            "live_target_identified_value_or_divisor_theorem_missing",
            "conditional_missing_period_156_context",
            "source_theorem_closed_policy_or_framing_missing",
            "source_theorem_closed_policy_or_framing_missing",
            "conditional_finite_payload_without_source_theorem",
            "reject_target_fails_yang_or_h90_legality",
            "reject_illegal_or_insufficient_target",
        )
        and all(row.ok for row in rows)
    )
    return H0TranslateTheoremQueryPacket(
        source_obligation_ok=obligation.row_ok,
        query_rows=rows,
        query_count=len(rows),
        source_closing_yes_rows=source_closing_yes,
        source_certification_only_rows=source_only,
        conditional_rows=conditional,
        rejected_rows=rejected,
        downstream_relevant_rows=downstream,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_translate_theorem_query_packet()
    print("p25 KSY-y H0 translate theorem-query packet gate")
    print("dependencies")
    print(f"  source_obligation_ok={int(profile.source_obligation_ok)}")
    print("query_rows")
    for row in profile.query_rows:
        print(
            "  "
            f"{row.name}: source_row={row.source_obligation_row} "
            f"decision={row.actual_decision} closes={int(row.source_theorem_closes)} "
            f"downstream={int(row.downstream_relevant)}"
        )
        print(f"    query={row.theorem_query}")
        print(f"    accepts={row.accepted_answer_shape}")
        print(f"    falsifier={row.first_falsifier}")
    print("counts")
    print(f"  query_count={profile.query_count}")
    print(f"  source_closing_yes_rows={profile.source_closing_yes_rows}")
    print(f"  source_certification_only_rows={profile.source_certification_only_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  downstream_relevant_rows={profile.downstream_relevant_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  expert_yes_must_be_value_period156_or_divisor_identity_for_legal_H0_product=1")
    print("  source_certification_boundary_only_and_finite_payloads_are_not_enough=1")
    print("  only_source_closing_yes_rows_enter_DANGER3_framing_and_X1_extraction=1")
    print("  no_verified_pomerance_triple_or_DANGER3_extraction_yet=1")
    print(f"ksy_y_h0_translate_theorem_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 translate theorem-query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
