#!/usr/bin/env python3
"""Primary-source exactness map for the p25 KL/KSY theorem target.

The theorem-hit router classifies candidate outputs.  This gate maps the live
primary-source families to those output types, so a future literature hit is
tested by what it actually emits rather than by the prestige of the source
family.

It is deliberately conservative: Sprang/Kronecker and Koo-Shin-Yoon stay alive,
but only after instantiating the exact p25 C/D/K/orientation payload.  Generic
ray-class generation, ordinary odd-D Kato-Siegel theta_D, and raw
Kubert-Lang exponent hygiene do not by themselves pass the router.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate import (
    profile_theorem_hit_router,
)


@dataclass(frozen=True)
class PrimarySourceExactnessRow:
    name: str
    primary_source_url: str
    source_fact: str
    natural_router_lane: str
    accepted_by_router_if_instantiated: bool
    first_obligation_or_falsifier: str
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class PrimarySourceExactnessProfile:
    theorem_hit_router_ok: bool
    source_boundary_ok: bool
    continue_rows: tuple[PrimarySourceExactnessRow, ...]
    conditional_rows: tuple[PrimarySourceExactnessRow, ...]
    kill_rows: tuple[PrimarySourceExactnessRow, ...]
    exact_instantiation_target: str
    next_probe: str
    row_ok: bool


def profile_primary_source_exactness() -> PrimarySourceExactnessProfile:
    router = profile_theorem_hit_router()

    continue_rows = (
        PrimarySourceExactnessRow(
            "sprang_kronecker_d_variant_differential",
            "https://arxiv.org/abs/1802.04996",
            (
                "Sprang constructs algebraic D-variant Kronecker/polylogarithm "
                "differential representatives; Kato-Siegel dlog appears as a "
                "specialization only in the ordinary theta_D setting."
            ),
            "raw-divisor-or-additive",
            router.raw_orientation_router_ok,
            (
                "Must emit the exact anti-invariant product or theta2/theta2^-1 "
                "divisor/additive data for C=(47,28), D=(22,3), primitive K."
            ),
            "continue as differential/additive route, not as value-only proof",
            router.raw_orientation_router_ok and router.anti_invariant_contract_ok,
        ),
        PrimarySourceExactnessRow(
            "koo_shin_yoon_normalized_y_value",
            "https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf",
            (
                "Koo-Shin-Yoon define normalized y as a Siegel quotient "
                "y(r1,r2)=-g(2r1,2r2)/g(r1,r2)^4 and use singular y-values "
                "to generate ray class fields."
            ),
            "raw-value-with-period-156-context",
            router.raw_value_route_ok and router.value_support_root_unique_fp,
            (
                "Must supply the exact 75-atom K-traced product plus period-156 "
                "theta2 fixedness/telescoping; field generation alone is not a "
                "certificate payload."
            ),
            "continue as value route only with period-156 context",
            router.raw_value_route_ok
            and router.value_support_period == 156
            and router.anti_invariant_contract_ok,
        ),
        PrimarySourceExactnessRow(
            "kubert_lang_exact_siegel_exponent_matrix",
            "https://eudml.org/doc/162977",
            (
                "Kubert-Lang/Siegel products give the modular-unit exponent "
                "language; the p25 finite target must be the exact six-cell "
                "packet, factor word, or 300-term theta2 payload."
            ),
            "finite-spine-verifier-target",
            router.finite_spine_intake_ok,
            (
                "Elementary congruences are saturated by wrong packets; the "
                "matrix must preserve the mixed C3 x C169 row graph and then "
                "feed the finite intake."
            ),
            "continue only as exact exponent-matrix instantiation",
            router.finite_spine_intake_ok and router.anti_invariant_contract_ok,
        ),
    )

    conditional_rows = (
        PrimarySourceExactnessRow(
            "siegel_robert_value_units_with_branch_control",
            "https://eudml.org/doc/162977",
            (
                "Siegel-Robert value-unit constructions are compatible with "
                "the target only if branch/root data is part of the theorem "
                "output or if the output is divisor/additive data."
            ),
            "raw-value-with-period-156-context",
            router.raw_value_route_ok and router.value_support_root_unique_fp,
            (
                "Ambient 780-period values have 11 F_p branches; period-156 "
                "theta2 fixedness is the required branch-control substitute."
            ),
            "conditional continue with explicit period/branch data",
            router.raw_value_route_ok
            and router.ambient_value_branch_count_fp == 11
            and router.value_support_root_unique_fp,
        ),
    )

    kill_rows = (
        PrimarySourceExactnessRow(
            "ordinary_kato_siegel_thetaD_direct",
            "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            (
                "The ordinary theta_D/Kato-Siegel unit has the prime-to-6 "
                "hypothesis in the direct theta_D setting."
            ),
            "rejected-or-not-instantiated",
            False,
            "D=2 is outside the direct odd-D theta_D theorem route.",
            "kill as direct D=2 proof; retain only as odd-D control",
            router.source_boundary_ok,
        ),
        PrimarySourceExactnessRow(
            "koo_shin_yoon_generic_ray_class_generation",
            "https://arxiv.org/abs/1007.2307",
            (
                "Theorem 5.3 and Theorem 6.2/Corollary 6.4 are field-generation "
                "statements from torsion or y singular values."
            ),
            "rejected-or-not-instantiated",
            False,
            (
                "Generating K(N) is too broad; it does not select the p25 "
                "C/D/K/orientation product or bridge certificate."
            ),
            "kill until instantiated as exact product or theta2 payload",
            router.source_boundary_ok,
        ),
        PrimarySourceExactnessRow(
            "raw_kl_exponent_balance_only",
            "https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf",
            (
                "The Siegel-product congruence screen is necessary modular-unit "
                "hygiene but not a selector."
            ),
            "rejected-or-not-instantiated",
            False,
            (
                "Missing K, collapsed K, truncated D, wrong D, and shifted "
                "center controls also pass raw exponent congruences."
            ),
            "kill unless paired with finite intake geometry",
            router.source_boundary_ok,
        ),
    )

    all_rows = continue_rows + conditional_rows + kill_rows
    row_ok = (
        router.row_ok
        and router.source_boundary_ok
        and len(continue_rows) == 3
        and len(conditional_rows) == 1
        and len(kill_rows) == 3
        and all(row.row_ok for row in all_rows)
        and sum(int(row.accepted_by_router_if_instantiated) for row in continue_rows) == 3
        and sum(int(row.accepted_by_router_if_instantiated) for row in conditional_rows) == 1
        and not any(row.accepted_by_router_if_instantiated for row in kill_rows)
        and router.value_support_period == 156
        and router.ambient_value_branch_count_fp == 11
    )
    return PrimarySourceExactnessProfile(
        theorem_hit_router_ok=router.row_ok,
        source_boundary_ok=router.source_boundary_ok,
        continue_rows=continue_rows,
        conditional_rows=conditional_rows,
        kill_rows=kill_rows,
        exact_instantiation_target=(
            "prove a challenge-legal identity for the exact equal-weight "
            "K-traced anti-invariant normalized-y product at "
            "C=(47,28), D=(22,3), primitive K=(57,0), orientation"
        ),
        next_probe=(
            "instantiate either a Sprang/Kronecker differential formula or a "
            "Koo-Shin-Yoon/Kubert-Lang exact y/Siegel product, then feed its "
            "actual output type to the theorem-hit router"
        ),
        row_ok=row_ok,
    )


def print_row(prefix: str, row: PrimarySourceExactnessRow) -> None:
    print(
        "  "
        f"{prefix}: lane={row.natural_router_lane} "
        f"accepts_if_instantiated={int(row.accepted_by_router_if_instantiated)} "
        f"recommendation={row.recommendation}"
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang primary-source exactness gate")
    profile = profile_primary_source_exactness()
    print(f"primary_source_exactness_profile={profile}")
    print("continue_sources")
    for row in profile.continue_rows:
        print_row(row.name, row)
    print("conditional_sources")
    for row in profile.conditional_rows:
        print_row(row.name, row)
    print("kill_sources")
    for row in profile.kill_rows:
        print_row(row.name, row)
    print("source_exactness_laws")
    print("  source_family_claims_are_routed_by_output_type=1")
    print("  sprang_is_differential_additive_not_direct_value_branch=1")
    print("  ksy_y_values_need_period_156_context_and_exact_product=1")
    print("  kubert_lang_congruence_hygiene_is_not_a_selector=1")
    print("interpretation")
    print("  next_probe_must_instantiate_exact_C_D_K_payload_before_claiming_progress=1")
    print(
        "robert_ksy_theta2_kubert_lang_primary_source_exactness_rows="
        f"{int(profile.row_ok)}/1"
    )
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_primary_source_exactness_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
