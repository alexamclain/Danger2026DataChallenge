#!/usr/bin/env python3
"""Primary-source scout packet gate for the p25 KSY-y moonshot.

This is not a theorem prover.  It guards the next literature-search step: a
fresh scout is useful only if it inspects a named primary source and returns a
payload that can be classified by the existing closing-theorem obligation gate.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceScoutContract:
    name: str
    source_anchor: str
    source_handle: str
    positive_payload: str
    first_falsifier: str
    local_classifier: str
    row_ok: bool


@dataclass(frozen=True)
class SourceScoutPacket:
    target: str
    contracts: tuple[SourceScoutContract, ...]
    exact_product_contracts: int
    value_contracts: int
    policy_or_extraction_contracts: int
    row_ok: bool


TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} "
    "y(C+jD+kK)/y(-C-jD-kK), C=(47,28), D=(22,3), K=(57,0), "
    "y(Q)=-g(2Q)/g(Q)^4"
)


def scout_contracts() -> tuple[SourceScoutContract, ...]:
    return (
        SourceScoutContract(
            name="ksy_normalized_y_exact_p",
            source_anchor="Koo-Shin-Yoon normalized wp-prime / y-coordinate ray-class construction",
            source_handle="arXiv:1007.2307, Theorem 5.3 plus Theorem 6.2 / Corollary 6.4",
            positive_payload=(
                "exact P or an exact finite-field value identity for P, not only "
                "ray-class field generation from torsion coordinates"
            ),
            first_falsifier="the source emits a broad generator or one y-value but no 75-atom mixed graph",
            local_classifier=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py"
            ),
            row_ok=True,
        ),
        SourceScoutContract(
            name="kubert_lang_mixed_graph_product",
            source_anchor="Kubert-Lang Siegel functions / modular-unit generators",
            source_handle="Kubert-Lang, Units in the Modular Function Field IV; Modular Units",
            positive_payload=(
                "exact row-labeled C_3 x C_169 pairs, reflection-center data, "
                "or the raw equal-weight K-traced product"
            ),
            first_falsifier="C169 projection, exponent congruence hygiene, or generator theorem only",
            local_classifier=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py"
            ),
            row_ok=True,
        ),
        SourceScoutContract(
            name="sprang_kronecker_d2_additive",
            source_anchor="Sprang / Kronecker section / Kato-Siegel logarithmic derivative",
            source_handle="arXiv:1801.05677, Section 5 and distribution appendix",
            positive_payload=(
                "D=2-compatible divisor/additive identity for exact P, with "
                "source-parameter hygiene separating KSY [2] from ordinary Dtheta"
            ),
            first_falsifier="ordinary Kato-Siegel Dtheta=2 claim without an even-D Kronecker clause",
            local_classifier=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate.py"
            ),
            row_ok=True,
        ),
        SourceScoutContract(
            name="siegel_robert_period_value",
            source_anchor="Schertz / Shin / Siegel-Ramachandra elliptic-unit value invariants",
            source_handle="Schertz 1997; arXiv:1009.2253",
            positive_payload=(
                "finite-field value identity for exact P with period-156 fixedness, "
                "branch, root, or telescoping context"
            ),
            first_falsifier="ambient period-780 value or class-field invariant without period-156 context",
            local_classifier=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py"
            ),
            row_ok=True,
        ),
        SourceScoutContract(
            name="danger3_framing_extraction",
            source_anchor="official DANGER3 challenge definition, vpp.py, and lean_vpp.py",
            source_handle="AndrewVSutherland/DANGER3 README and verifier files",
            positive_payload=(
                "policy acceptance for finite-field identity framing, or concrete "
                "extraction to (A,x0) followed by official vpp.py verification"
            ),
            first_falsifier="theorem-only or CM/Lang provenance without a concrete triple or policy framing",
            local_classifier=(
                "p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py"
            ),
            row_ok=True,
        ),
    )


def profile_scout_packet() -> SourceScoutPacket:
    rows = scout_contracts()
    exact_rows = sum(
        int("exact P" in row.positive_payload or "K-traced product" in row.positive_payload)
        for row in rows
    )
    value_rows = sum(int("value" in row.name or "value identity" in row.positive_payload) for row in rows)
    policy_rows = sum(int("policy" in row.positive_payload or "(A,x0)" in row.positive_payload) for row in rows)
    row_ok = (
        len(rows) == 5
        and exact_rows >= 3
        and value_rows >= 2
        and policy_rows == 1
        and all(row.row_ok for row in rows)
        and all(row.local_classifier.endswith("_gate.py") for row in rows)
    )
    return SourceScoutPacket(
        target=TARGET_PRODUCT,
        contracts=rows,
        exact_product_contracts=exact_rows,
        value_contracts=value_rows,
        policy_or_extraction_contracts=policy_rows,
        row_ok=row_ok,
    )


def print_contract(row: SourceScoutContract) -> None:
    print(
        "  "
        f"{row.name}: anchor={row.source_anchor} handle={row.source_handle} "
        f"positive_payload={row.positive_payload} first_falsifier={row.first_falsifier} "
        f"classifier={row.local_classifier}"
    )


def main() -> int:
    profile = profile_scout_packet()
    print("p25 KSY-y primary-source scout packet gate")
    print(f"target={profile.target}")
    print("contracts")
    for row in profile.contracts:
        print_contract(row)
    print("counts")
    print(f"  contract_rows={len(profile.contracts)}")
    print(f"  exact_product_contracts={profile.exact_product_contracts}")
    print(f"  value_contracts={profile.value_contracts}")
    print(f"  policy_or_extraction_contracts={profile.policy_or_extraction_contracts}")
    print("interpretation")
    print("  scouts_are_source_gated_not_time_gated=1")
    print("  broad_relevance_without_exact_P_is_rejected=1")
    print("  closing_theorem_obligation_gate_is_the_final_theory_classifier=1")
    print(f"ksy_y_primary_source_scout_packet_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("primary-source scout packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
