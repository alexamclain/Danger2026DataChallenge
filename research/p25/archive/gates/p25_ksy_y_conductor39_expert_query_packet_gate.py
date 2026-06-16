#!/usr/bin/env python3
"""Expert-query packet for the current conductor-39 p25 moonshot frontier.

This is a routing artifact for conversations with a domain expert.  It keeps
the questions narrow enough that an answer can be fed back into the existing
source-theorem, DANGER3 framing, and extraction gates.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P = 10_000_000_000_000_000_000_000_013
SQRT_FLOOR = 3_162_277_660_168
RESEARCH = Path("research/p25")


@dataclass(frozen=True)
class ExpertQueryRow:
    name: str
    question_for_expert: str
    answer_shape_that_advances: str
    local_router: Path
    local_probe: str
    expected_decision_if_yes: str
    first_falsifier_or_missing_clause: str
    closes_source_stage_if_yes: bool
    policy_or_extraction_question: bool
    rejection_or_guardrail: bool
    submission_only: bool
    ok: bool


@dataclass(frozen=True)
class ExpertQueryPacket:
    prerequisite_markers_present: int
    p_order_mod39: int
    p_cubed_is_minus_one_mod39: bool
    sqrt_minus39_in_fp: bool
    support_period_gcd: int
    ambient_period_gcd: int
    count_ladder: tuple[int, int, int, int, int]
    max_current_budget: int
    max_budget_below_sqrt: bool
    query_rows: tuple[ExpertQueryRow, ...]
    source_closing_yes_rows: int
    policy_or_extraction_rows: int
    rejection_or_guardrail_rows: int
    submission_only_rows: int
    local_probe_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def multiplicative_order_mod(n: int, modulus: int) -> int:
    if gcd(n, modulus) != 1:
        raise ValueError("order is defined only for units")
    value = 1
    for order in range(1, modulus + 1):
        value = (value * n) % modulus
        if value == 1:
            return order
    raise ValueError("order search exhausted")


def conductor39_source_probe(source_object: str, output_kind: str = "divisor-additive") -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py "
        f"--candidate --name expert_{source_object}_theorem "
        f"--source-object {source_object} --output-kind {output_kind} "
        "--theorem-body --emits-conductor39 --mixed-tensor --legal-unit "
        "--yang-lift --descent --finite-or-divisor --period-156"
    )


def h90_probe(target_object: str, output_kind: str = "divisor-additive") -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_h90_value_theorem_intake_gate.py "
        f"--candidate --name expert_{target_object}_theorem "
        f"--target-object {target_object} --output-kind {output_kind} "
        "--theorem-body --exact-target --bridge-spine --legal-yang-h90 "
        "--boundary-context --finite-or-divisor --period-156 --arithmetic-source"
    )


def x1_8112_probe() -> str:
    return (
        "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
        "research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py "
        "--candidate --name expert_x1_8112_to_x16 "
        "--odd-payload-object Y_507 --theorem-body --exact-p25 "
        "--odd-value-or-divisor --fiber-product --j-gluing --x16-relation "
        "--emit-y --emit-model-root-xp16 --danger3-framing"
    )


def query_rows() -> tuple[ExpertQueryRow, ...]:
    conductor_router = RESEARCH / "p25_ksy_y_conductor39_source_theorem_intake_gate.py"
    h90_router = RESEARCH / "p25_ksy_y_h90_value_theorem_intake_gate.py"
    x1_router = RESEARCH / "p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py"
    vpp_router = RESEARCH / "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py"
    return (
        ExpertQueryRow(
            name="finite_Uchi_or_W_value_or_divisor_identity",
            question_for_expert=(
                "Is there a finite-field value identity or divisor/additive "
                "identity for U_chi=-chi_3*chi_13 on X_1(39), W=6*U_chi, "
                "or Norm_156(Y_507)=distribution_lift_39_to_507(W)?"
            ),
            answer_shape_that_advances=(
                "exact conductor-39 mixed tensor object, Yang 13-fiber lift, "
                "finite value/divisor theorem, and period-156 context for values"
            ),
            local_router=conductor_router,
            local_probe=conductor39_source_probe("U_chi"),
            expected_decision_if_yes="source_theorem_closed_policy_or_framing_missing",
            first_falsifier_or_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_source_stage_if_yes=True,
            policy_or_extraction_question=False,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="degree6_cyclotomic_norm_descent",
            question_for_expert=(
                "If the identity naturally lives over F_{p^6}, does it give a "
                "conjugate product, norm, trace, or Hilbert-90 descent back to F_p?"
            ),
            answer_shape_that_advances=(
                "degree-6 cyclotomic computation plus explicit descent to F_p "
                "and period-156 branch context for value outputs"
            ),
            local_router=conductor_router,
            local_probe=conductor39_source_probe("W", output_kind="value"),
            expected_decision_if_yes="source_theorem_closed_policy_or_framing_missing",
            first_falsifier_or_missing_clause="conjugate/norm descent back to F_p",
            closes_source_stage_if_yes=True,
            policy_or_extraction_question=False,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="hilbert90_ratio_or_H0_value_identity",
            question_for_expert=(
                "Is there a Hilbert-90 or ratio theorem evaluating canonical H0 "
                "or a legal <2>-translate with (1-Frob_p)H0=Norm_156(Y_507)?"
            ),
            answer_shape_that_advances=(
                "legal sparse Yang-fiber H0, exact boundary to Norm_156(Y_507), "
                "finite value/divisor theorem, and period-156 context for values"
            ),
            local_router=h90_router,
            local_probe=h90_probe("canonical_H0"),
            expected_decision_if_yes="source_theorem_closed_policy_or_framing_missing",
            first_falsifier_or_missing_clause="DANGER3 finite-identity/non-CM framing",
            closes_source_stage_if_yes=True,
            policy_or_extraction_question=False,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="period156_branch_control",
            question_for_expert=(
                "For any value theorem, is the branch fixed at support period 156 "
                "rather than the ambient period 780?"
            ),
            answer_shape_that_advances=(
                "period-156 fixedness/telescoping context; gcd(4^156-1,p-1)=1"
            ),
            local_router=h90_router,
            local_probe=h90_probe("Y_507", output_kind="value"),
            expected_decision_if_yes="source_theorem_closed_policy_or_framing_missing",
            first_falsifier_or_missing_clause="period-156 branch/root/telescoping context",
            closes_source_stage_if_yes=True,
            policy_or_extraction_question=False,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="danger3_finite_identity_policy",
            question_for_expert=(
                "Would DANGER3 accept the result if it is framed as a concrete "
                "finite-field identity for the p25 object, even if the source "
                "theorem is motivated by modular units?"
            ),
            answer_shape_that_advances=(
                "policy/framing yes for finite-field identity; still requires "
                "cross-level extraction to A,x0"
            ),
            local_router=RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_gate.py",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_ksy_y_conductor39_to_danger3_acceptance_ladder_gate.py"
            ),
            expected_decision_if_yes="policy_unblocked_extraction_missing",
            first_falsifier_or_missing_clause="X_1(8112)/X_1(16) extraction and official vpp.py",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=True,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="x1_8112_to_x16_extraction",
            question_for_expert=(
                "Can the odd-level Y_507/H0/U_chi theorem be glued to the "
                "X_1(8112) / X_1(16) surface and emit A, xP16, and a halving chain?"
            ),
            answer_shape_that_advances=(
                "fiber-product/j-gluing theorem, X_1(16) relation, model root "
                "xP16, and concrete x0 or checkable halvings"
            ),
            local_router=x1_router,
            local_probe=x1_8112_probe(),
            expected_decision_if_yes="x16_surface_reached_halving_or_vpp_missing",
            first_falsifier_or_missing_clause="valid halving chain from xP16 to concrete x0",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=True,
            rejection_or_guardrail=False,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="reject_direct_Fp_order39_root",
            question_for_expert="Can we just choose a primitive order-39 root in F_p?",
            answer_shape_that_advances="none; this is arithmetically impossible for p25",
            local_router=RESEARCH / "p25_ksy_y_conductor39_degree6_value_descent_packet_gate.py",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_ksy_y_conductor39_degree6_value_descent_packet_gate.py"
            ),
            expected_decision_if_yes="reject_direct_Fp_order39_root_shortcut",
            first_falsifier_or_missing_clause="ord_39(p)=6",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=False,
            rejection_or_guardrail=True,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="reject_sqrt_minus39_scalar",
            question_for_expert="Can sqrt(-39) be used as a scalar in F_p to collapse the character?",
            answer_shape_that_advances="none; sqrt(-39) is not in F_p for p25",
            local_router=RESEARCH / "p25_ksy_y_conductor39_degree6_value_descent_packet_gate.py",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_ksy_y_conductor39_degree6_value_descent_packet_gate.py"
            ),
            expected_decision_if_yes="reject_sqrt_minus39_scalar_shortcut",
            first_falsifier_or_missing_clause="(-39/p)=-1",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=False,
            rejection_or_guardrail=True,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="reject_generator_or_projection_only",
            question_for_expert=(
                "Is a ray-class generator, C169 projection, or prime-13/prime-3 "
                "axis theorem enough?"
            ),
            answer_shape_that_advances=(
                "only if upgraded to the exact mixed conductor-39 tensor or "
                "exact P/Y_507/H0 finite identity"
            ),
            local_router=RESEARCH / "p25_ksy_y_koo_shin_conductor39_distribution_bridge_gate.py",
            local_probe=(
                "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
                "research/p25/p25_ksy_y_koo_shin_conductor39_distribution_bridge_gate.py"
            ),
            expected_decision_if_yes="reject_loses_mixed_tensor",
            first_falsifier_or_missing_clause="mixed chi_3 tensor chi_13 source on X_1(39)",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=False,
            rejection_or_guardrail=True,
            submission_only=False,
            ok=True,
        ),
        ExpertQueryRow(
            name="verified_pomerance_triple",
            question_for_expert="Do we have a concrete p25 (p,A,x0) triple?",
            answer_shape_that_advances="official DANGER3 vpp.py verifies the concrete p25 triple",
            local_router=vpp_router,
            local_probe=(
                "python3 research/p25/"
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py "
                "--p 10000000000000000000000013 --A <A> --x0 <x0>"
            ),
            expected_decision_if_yes="closing_vpp_verified_submission",
            first_falsifier_or_missing_clause="official vpp.py verification",
            closes_source_stage_if_yes=False,
            policy_or_extraction_question=False,
            rejection_or_guardrail=False,
            submission_only=True,
            ok=True,
        ),
    )


def profile_expert_query_packet() -> ExpertQueryPacket:
    marker_specs = (
        (
            RESEARCH / "p25_ksy_y_conductor39_value_theorem_source_route_packet_20260614.md",
            "ksy_y_conductor39_value_theorem_source_route_packet_rows=1/1",
        ),
        (
            RESEARCH / "p25_ksy_y_conductor39_degree6_value_descent_packet_20260614.md",
            "ksy_y_conductor39_degree6_value_descent_packet_rows=1/1",
        ),
        (
            RESEARCH / "p25_ksy_y_conductor39_to_danger3_acceptance_ladder_20260614.md",
            "ksy_y_conductor39_to_danger3_acceptance_ladder_rows=1/1",
        ),
        (
            RESEARCH / "p25_ksy_y_subsqrt_moonshot_budget_ladder_20260614.md",
            "ksy_y_subsqrt_moonshot_budget_ladder_rows=1/1",
        ),
    )
    markers = sum(marker_present(path, marker) for path, marker in marker_specs)
    order39 = multiplicative_order_mod(P % 39, 39)
    sqrt_minus39_in_fp = pow((-39) % P, (P - 1) // 2, P) == 1
    rows = query_rows()
    source_closing = sum(row.closes_source_stage_if_yes for row in rows)
    policy_or_extraction = sum(row.policy_or_extraction_question for row in rows)
    rejection = sum(row.rejection_or_guardrail for row in rows)
    submission = sum(row.submission_only for row in rows)
    local_probe_rows = sum(bool(row.local_probe) for row in rows)
    count_ladder = (75, 300, 12, 312, 156)
    max_current_budget = 46_800
    row_ok = (
        markers == len(marker_specs)
        and order39 == 6
        and pow(P, 3, 39) == 38
        and not sqrt_minus39_in_fp
        and gcd(4**156 - 1, P - 1) == 1
        and gcd(4**780 - 1, P - 1) == 11
        and count_ladder == (75, 300, 12, 312, 156)
        and max_current_budget < SQRT_FLOOR
        and len(rows) == 10
        and source_closing == 4
        and policy_or_extraction == 2
        and rejection == 3
        and submission == 1
        and local_probe_rows == 10
        and all(row.local_router.exists() and row.local_router.stat().st_size > 0 for row in rows)
        and all(row.ok for row in rows)
    )
    return ExpertQueryPacket(
        prerequisite_markers_present=markers,
        p_order_mod39=order39,
        p_cubed_is_minus_one_mod39=pow(P, 3, 39) == 38,
        sqrt_minus39_in_fp=sqrt_minus39_in_fp,
        support_period_gcd=gcd(4**156 - 1, P - 1),
        ambient_period_gcd=gcd(4**780 - 1, P - 1),
        count_ladder=count_ladder,
        max_current_budget=max_current_budget,
        max_budget_below_sqrt=max_current_budget < SQRT_FLOOR,
        query_rows=rows,
        source_closing_yes_rows=source_closing,
        policy_or_extraction_rows=policy_or_extraction,
        rejection_or_guardrail_rows=rejection,
        submission_only_rows=submission,
        local_probe_rows=local_probe_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_expert_query_packet()
    print("p25 KSY-y conductor-39 expert-query packet gate")
    print("prerequisites")
    print(f"  prerequisite_markers_present={profile.prerequisite_markers_present}")
    print("arithmetic")
    print(f"  p_order_mod39={profile.p_order_mod39}")
    print(f"  p_cubed_is_minus_one_mod39={int(profile.p_cubed_is_minus_one_mod39)}")
    print(f"  sqrt_minus39_in_fp={int(profile.sqrt_minus39_in_fp)}")
    print(f"  gcd_4_156_minus_1_p_minus_1={profile.support_period_gcd}")
    print(f"  gcd_4_780_minus_1_p_minus_1={profile.ambient_period_gcd}")
    print(f"  count_ladder={profile.count_ladder}")
    print(f"  max_current_budget={profile.max_current_budget}")
    print(f"  max_budget_below_sqrt={int(profile.max_budget_below_sqrt)}")
    print("query_rows")
    for row in profile.query_rows:
        print(
            "  "
            f"{row.name}: expected={row.expected_decision_if_yes} "
            f"source_closes={int(row.closes_source_stage_if_yes)} "
            f"policy_or_extraction={int(row.policy_or_extraction_question)} "
            f"guardrail={int(row.rejection_or_guardrail)} "
            f"submission={int(row.submission_only)}"
        )
        print(f"    question={row.question_for_expert}")
        print(f"    advances={row.answer_shape_that_advances}")
        print(f"    missing_or_falsifier={row.first_falsifier_or_missing_clause}")
        print(f"    router={row.local_router}")
        print(f"    probe={row.local_probe}")
    print("counts")
    print(f"  query_rows={len(profile.query_rows)}")
    print(f"  source_closing_yes_rows={profile.source_closing_yes_rows}")
    print(f"  policy_or_extraction_rows={profile.policy_or_extraction_rows}")
    print(f"  rejection_or_guardrail_rows={profile.rejection_or_guardrail_rows}")
    print(f"  submission_only_rows={profile.submission_only_rows}")
    print(f"  local_probe_rows={profile.local_probe_rows}")
    print("interpretation")
    print("  expert_conversation_has_four_source_closing_yes_shapes=1")
    print("  source_closure_still_needs_policy_extraction_and_vpp=1")
    print("  direct_order39_and_sqrt_minus39_shortcuts_are_dead=1")
    print(f"ksy_y_conductor39_expert_query_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("conductor-39 expert-query packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
