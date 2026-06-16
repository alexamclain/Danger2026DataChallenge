#!/usr/bin/env python3
"""Source-boundary screen for the p25 anti-invariant KSY/KL contract.

The anti-invariant producer contract is now the sharp finite target:

    C=(47,28), D=(22,3), primitive K=(57,0), orientation,
    with base=C-D and T=-2C+K derived.

This gate maps the existing primary-source families to that exact contract.  It
is a proof-search boundary: continue only sources that can plausibly emit the
equal-weight K-traced anti-invariant normalized-y product; kill sources that
only explain exponent balance, subgroup norms, generic class-field generation,
or nonuniform weights.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_producer_contract_gate import (
    profile_anti_invariant_producer_contract,
)
from p25_laneB_robert_ksy_theta2_theorem_source_screen_gate import (
    TheoremSourceRow,
    profile_theorem_source_screen,
)


@dataclass(frozen=True)
class AntiInvariantSourceBoundaryRow:
    name: str
    source_url: str
    source_family: str
    anti_invariant_transfer: str
    first_falsifier_or_debt: str
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class AntiInvariantSourceBoundaryProfile:
    anti_invariant_contract_ok: bool
    prior_source_screen_ok: bool
    continue_rows: tuple[AntiInvariantSourceBoundaryRow, ...]
    conditional_rows: tuple[AntiInvariantSourceBoundaryRow, ...]
    kill_rows: tuple[AntiInvariantSourceBoundaryRow, ...]
    continued_source_count: int
    killed_source_count: int
    exact_theorem_contract: str
    next_probe: str
    row_ok: bool


def source_by_name(rows: tuple[TheoremSourceRow, ...], name: str) -> TheoremSourceRow:
    for row in rows:
        if row.name == name:
            return row
    raise KeyError(name)


def profile_anti_invariant_source_boundary() -> AntiInvariantSourceBoundaryProfile:
    contract = profile_anti_invariant_producer_contract()
    source_screen = profile_theorem_source_screen()

    sprang = source_by_name(source_screen.continue_rows, "sprang_kronecker_d2")
    kubert_lang = source_by_name(source_screen.continue_rows, "kubert_lang_siegel_exponent_matrix")
    ksy = source_by_name(source_screen.continue_rows, "koo_shin_yoon_normalized_wp_prime")
    class_field = source_by_name(
        source_screen.conditional_rows,
        "kubert_lang_siegel_robert_class_field_units",
    )
    kato = source_by_name(source_screen.kill_rows, "scholl_kato_thetaD_direct")
    subgroup = source_by_name(source_screen.kill_rows, "scholl_robert_literal_subgroup_support")

    continue_rows = (
        AntiInvariantSourceBoundaryRow(
            "sprang_kronecker_d2_exact_anti_invariant_product",
            sprang.source_url,
            "D=2 Kronecker / elliptic-polylog differential identities",
            (
                "May continue only if it emits the exact product over "
                "A=C+jD+kK, or exact theta2/theta2^-1 data with period-156 "
                "telescoping context."
            ),
            (
                "A dlog, Eisenstein class, or value identity without the rigid "
                "C,D,K atoms is not enough."
            ),
            "continue as highest-value theorem route",
            contract.row_ok and source_screen.row_ok and sprang.row_ok,
        ),
        AntiInvariantSourceBoundaryRow(
            "kubert_lang_exact_equal_weight_exponent_matrix",
            kubert_lang.source_url,
            "Kubert-Lang Siegel-unit exponent matrices",
            (
                "May continue only as an exact exponent-matrix search for the "
                "six quotient cells, the derived factor word, or the 300-term "
                "theta2 payload."
            ),
            (
                "Raw KL sums are saturated for anti-invariant packets and do "
                "not select C, D, K, or weights."
            ),
            "continue only with finite intake plus theta2 certificate",
            (
                contract.row_ok
                and kubert_lang.row_ok
                and contract.raw_exponent_screen_saturated
                and contract.atomic_weight_rigidity_ok
            ),
        ),
        AntiInvariantSourceBoundaryRow(
            "koo_shin_yoon_normalized_y_exact_product",
            ksy.source_url,
            "normalized wp-prime / y-coordinate singular values",
            (
                "May continue because the target is literally a normalized-y "
                "anti-invariant product."
            ),
            (
                "Generic ray-class generation is not enough; it must land on "
                "the exact equal-weight K-traced product and orientation."
            ),
            "continue as value/differential source",
            contract.row_ok and ksy.row_ok and contract.anti_invariant_intake_ok,
        ),
    )

    conditional_rows = (
        AntiInvariantSourceBoundaryRow(
            "siegel_robert_value_units_with_branch_control",
            class_field.source_url,
            "Siegel-Robert class-field units",
            (
                "Conditional if the theorem supplies period-156 fixedness and "
                "branch/root selection, or outputs divisor/additive theta2 data."
            ),
            (
                "Ambient value-level normalization still has branch ambiguity; "
                "finite source masks do not select a value branch."
            ),
            "conditional continue only with explicit branch/fixedness data",
            contract.row_ok and class_field.row_ok,
        ),
    )

    kill_rows = (
        AntiInvariantSourceBoundaryRow(
            "ordinary_kato_thetaD_direct",
            kato.source_url,
            "ordinary Kato theta_D units",
            "Does not cover the needed D=2 normalized-y product.",
            "The ordinary theta_D theorem is outside the D=2 target.",
            "kill as direct proof; retain as sanity check",
            contract.row_ok and kato.row_ok,
        ),
        AntiInvariantSourceBoundaryRow(
            "literal_robert_subgroup_support",
            subgroup.source_url,
            "literal Robert finite-subgroup divisors",
            "Cannot emit the p25 short D segment.",
            "D has visible order 507, raw order 12675, and visible 3D=(0,9).",
            "kill literal subgroup/coset explanations",
            contract.row_ok and subgroup.row_ok,
        ),
        AntiInvariantSourceBoundaryRow(
            "raw_kl_exponent_balance_only",
            kubert_lang.source_url,
            "raw Kubert-Lang exponent congruence checks",
            "Explains hygiene but not the selector.",
            (
                "Missing K, collapsed K, truncated D, wrong D, and shifted "
                "center all pass raw KL exponent sums."
            ),
            "kill as a producer claim unless paired with finite intake",
            contract.raw_exponent_screen_saturated and contract.finite_contract_rejects_shortcuts,
        ),
        AntiInvariantSourceBoundaryRow(
            "nonuniform_weighted_product_variants",
            ksy.source_url,
            "weighted normalized-y subproducts",
            "Cannot change weights inside the accepted geometry.",
            (
                "D-slice and atomic support read-off force equal weights on all "
                "75 atoms."
            ),
            "kill missing/doubled/mixed-sign/nonuniform K-layer variants",
            contract.d_slice_weight_rigidity_ok and contract.atomic_weight_rigidity_ok,
        ),
    )

    all_rows = continue_rows + conditional_rows + kill_rows
    row_ok = (
        contract.row_ok
        and source_screen.row_ok
        and len(continue_rows) == 3
        and len(conditional_rows) == 1
        and len(kill_rows) == 4
        and all(row.row_ok for row in all_rows)
        and contract.derived.raw_center == (47, 28)
        and contract.derived.raw_t_from_reflection == (38, 113)
        and contract.derived.quotient_t_from_reflection == (2, 113)
        and contract.finite_contract_accepts_anti_invariant_target
        and contract.finite_contract_rejects_shortcuts
    )
    return AntiInvariantSourceBoundaryProfile(
        anti_invariant_contract_ok=contract.row_ok,
        prior_source_screen_ok=source_screen.row_ok,
        continue_rows=continue_rows,
        conditional_rows=conditional_rows,
        kill_rows=kill_rows,
        continued_source_count=len(continue_rows) + len(conditional_rows),
        killed_source_count=len(kill_rows),
        exact_theorem_contract=(
            "prove a challenge-legal identity for the exact equal-weight "
            "K-traced anti-invariant normalized-y product at "
            "C=(47,28), D=(22,3), primitive K=(57,0), orientation"
        ),
        next_probe=(
            "instantiate a D=2 Kronecker/KSY normalized-y formula or a "
            "Kubert-Lang exponent matrix, then run it through the anti-invariant "
            "producer contract gate"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY Kubert-Lang anti-invariant source-boundary gate")
    profile = profile_anti_invariant_source_boundary()
    print(f"anti_invariant_source_boundary_profile={profile}")
    print("continue_sources")
    for row in profile.continue_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("conditional_sources")
    for row in profile.conditional_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("kill_sources")
    for row in profile.kill_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("source_boundary_laws")
    print("  exact_anti_invariant_producer_contract_is_the_theorem_target=1")
    print("  sprang_kronecker_D2_kubert_lang_exact_matrix_and_KSY_y_routes_continue=1")
    print("  siegel_robert_value_units_are_conditional_on_branch_or_period_data=1")
    print("  kato_thetaD_subgroup_raw_KL_and_weighted_variants_are_killed=1")
    print("interpretation")
    print("  next_probe_should_instantiate_a_formula_and_run_the_contract_gate=1")
    print("  this_gate_is_a_source_boundary_not_the_missing_theorem=1")
    print(
        "robert_ksy_theta2_kubert_lang_anti_invariant_source_boundary_rows="
        f"{int(profile.row_ok)}/1"
    )
    print(
        "conclusion=reported_p25_laneB_robert_ksy_theta2_kubert_lang_"
        "anti_invariant_source_boundary_gate"
    )
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
