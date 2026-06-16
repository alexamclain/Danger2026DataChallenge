#!/usr/bin/env python3
"""Primary-source anchor packet for the exact p25 KSY-y source audit.

This is the cheap handoff layer after the executable source-clause audit.  It
records which primary-source theorem anchors should be checked next, what each
anchor currently supplies, and what missing clause would have to be found in
that source to close the KSY-y route.

The heavy finite checks live in the formula/period/closure/source-audit gates;
this packet is deliberately static and fast.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PrimarySourceAnchorRow:
    name: str
    source_url: str
    anchor: str
    supplies: str
    does_not_supply_yet: str
    exact_question: str
    status: str
    row_ok: bool


@dataclass(frozen=True)
class PrimarySourceAnchorPacketProfile:
    rows: tuple[PrimarySourceAnchorRow, ...]
    ksy_anchor_count: int
    siegel_robert_anchor_count: int
    sprang_anchor_count: int
    kubert_lang_anchor_count: int
    challenge_policy_count: int
    closing_anchor_count: int
    conditional_anchor_count: int
    rejected_anchor_count: int
    handoff_rule: str
    row_ok: bool


def anchor_row(
    name: str,
    source_url: str,
    anchor: str,
    supplies: str,
    does_not_supply_yet: str,
    exact_question: str,
    status: str,
) -> PrimarySourceAnchorRow:
    return PrimarySourceAnchorRow(
        name=name,
        source_url=source_url,
        anchor=anchor,
        supplies=supplies,
        does_not_supply_yet=does_not_supply_yet,
        exact_question=exact_question,
        status=status,
        row_ok=status in ("conditional", "rejected", "policy"),
    )


def profile_primary_source_anchor_packet() -> PrimarySourceAnchorPacketProfile:
    rows = (
        anchor_row(
            "ksy_theorem_5_3_ray_class_generation",
            "https://arxiv.org/pdf/1007.2307",
            "Koo-Shin-Yoon Theorem 5.3 / ray-class generation by torsion data",
            "ray-class-field generation context for normalized torsion coordinates",
            "the exact p25 product P with C=(47,28), D=(22,3), K=(57,0)",
            "Can Theorem 5.3 be specialized or strengthened to emit the exact P identity?",
            "conditional",
        ),
        anchor_row(
            "ksy_normalized_y_siegel_formula",
            "https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf",
            "normalized y/Siegel-function formula y(Q)=-g(2Q)/g(Q)^4",
            "the formula language locally instantiated as the 300-term footprint",
            "selection of the 75 atoms, mixed source graph, and period-156 context",
            "Can the normalized-y formula be promoted from language to exact product theorem?",
            "conditional",
        ),
        anchor_row(
            "siegel_robert_value_units",
            "https://eudml.org/doc/162977",
            "Siegel-Robert value units / branch-control value route",
            "value-unit language compatible with the value closure shape",
            "period-156 branch/root/telescoping data for the exact product P",
            "Can a value theorem include support-period 156 fixedness so the F_p^* root is unique?",
            "conditional",
        ),
        anchor_row(
            "sprang_prop_5_4_kato_siegel_dlog",
            "https://arxiv.org/pdf/1802.04996",
            "Sprang Proposition 5.4: Kato-Siegel dlog as Kronecker-section specialization",
            "a differential/additive output family compatible with the divisor route",
            "the D=2 exact p25 anti-invariant product P",
            "Can the D-variant/Kronecker identity be instantiated at D=2 to emit P?",
            "conditional",
        ),
        anchor_row(
            "kubert_lang_siegel_functions_generators",
            "https://eudml.org/doc/162977",
            "Kubert-Lang, Units in the Modular Function Field IV: Siegel functions are generators",
            "Siegel-function generator and exponent-matrix language",
            "the mixed C_75 x C_169 graph selector and exact finite intake",
            "Can generator/exponent data be tied to the exact p25 mixed graph, not only congruences?",
            "conditional",
        ),
        anchor_row(
            "danger3_policy_finite_field_identity",
            "https://github.com/AndrewVSutherland/DANGER3",
            "challenge-policy question, not a theorem source",
            "the decision boundary for whether a finite-field identity avoids the no-CM concern",
            "acceptance criterion for a KSY/Siegel/Kronecker finite-field proof",
            "Would an identity for P over finite fields be considered challenge-legal?",
            "policy",
        ),
        anchor_row(
            "generic_field_generation_or_ambient_value",
            "https://arxiv.org/abs/1007.2307",
            "broad ray-class generation / ambient value-only shadows",
            "diagnostic context only",
            "exact finite-field identity, exact product, and period-156 branch data",
            "Discard unless reframed as a closure-template theorem.",
            "rejected",
        ),
    )

    ksy_count = sum(int(row.name.startswith("ksy_")) for row in rows)
    siegel_robert_count = sum(int(row.name.startswith("siegel_robert_")) for row in rows)
    sprang_count = sum(int(row.name.startswith("sprang_")) for row in rows)
    kubert_lang_count = sum(int(row.name.startswith("kubert_lang_")) for row in rows)
    policy_count = sum(int(row.status == "policy") for row in rows)
    closing_count = sum(int(row.status == "closing") for row in rows)
    conditional_count = sum(int(row.status == "conditional") for row in rows)
    rejected_count = sum(int(row.status == "rejected") for row in rows)

    row_ok = (
        len(rows) == 7
        and ksy_count == 2
        and siegel_robert_count == 1
        and sprang_count == 1
        and kubert_lang_count == 1
        and policy_count == 1
        and closing_count == 0
        and conditional_count == 5
        and rejected_count == 1
        and all(row.row_ok for row in rows)
    )
    return PrimarySourceAnchorPacketProfile(
        rows=rows,
        ksy_anchor_count=ksy_count,
        siegel_robert_anchor_count=siegel_robert_count,
        sprang_anchor_count=sprang_count,
        kubert_lang_anchor_count=kubert_lang_count,
        challenge_policy_count=policy_count,
        closing_anchor_count=closing_count,
        conditional_anchor_count=conditional_count,
        rejected_anchor_count=rejected_count,
        handoff_rule=(
            "a literature hit must name one anchor row and supply its missing "
            "closure-template clause before it counts as moonshot progress"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang KSY-y primary-source anchor packet gate")
    profile = profile_primary_source_anchor_packet()
    print(f"primary_source_anchor_packet_profile={profile}")
    print("anchor_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: status={row.status} anchor={row.anchor} "
            f"missing={row.does_not_supply_yet}"
        )
    print("anchor_counts")
    print(f"  ksy_anchor_count={profile.ksy_anchor_count}")
    print(f"  siegel_robert_anchor_count={profile.siegel_robert_anchor_count}")
    print(f"  sprang_anchor_count={profile.sprang_anchor_count}")
    print(f"  kubert_lang_anchor_count={profile.kubert_lang_anchor_count}")
    print(f"  challenge_policy_count={profile.challenge_policy_count}")
    print(f"  closing_anchor_count={profile.closing_anchor_count}")
    print(f"  conditional_anchor_count={profile.conditional_anchor_count}")
    print(f"  rejected_anchor_count={profile.rejected_anchor_count}")
    print("interpretation")
    print("  primary_source_anchors_are_now_named_for_handoff=1")
    print("  no_anchor_is_a_closure_theorem_yet=1")
    print("  each_live_anchor_has_one_named_missing_clause=1")
    print(
        "robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
