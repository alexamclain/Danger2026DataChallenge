#!/usr/bin/env python3
"""Primary-source screening for the p25 normalized-y KSY theorem target.

This gate maps the current theorem-interface target to the nearest primary
literature sources.  It does not prove the missing product identity.  It records
which source families are still useful, which ones are only finite shadows, and
which familiar shortcuts are already falsified by the p25 arithmetic shape.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_laneB_robert_ksy_theta2_theorem_interface_gate import (
    profile_theorem_interface,
)


@dataclass(frozen=True)
class TheoremSourceRow:
    name: str
    source_url: str
    source_fact: str
    p25_transfer: str
    first_falsifier_or_debt: str
    recommendation: str
    row_ok: bool


@dataclass(frozen=True)
class TheoremSourceScreenProfile:
    theorem_interface_ok: bool
    continue_rows: tuple[TheoremSourceRow, ...]
    conditional_rows: tuple[TheoremSourceRow, ...]
    kill_rows: tuple[TheoremSourceRow, ...]
    primary_source_count: int
    best_next_probe: str
    lit_search_brief: str
    row_ok: bool


def profile_theorem_source_screen() -> TheoremSourceScreenProfile:
    interface = profile_theorem_interface()

    continue_rows = (
        TheoremSourceRow(
            "sprang_kronecker_d2",
            "https://arxiv.org/pdf/1802.04996",
            (
                "Kronecker-section / elliptic-polylogarithm machinery gives "
                "algebraic D-variant differential forms, and D=2 is not excluded "
                "the way ordinary Kato theta_D units are."
            ),
            (
                "Use as the main source family for a D=2 differential or "
                "value-level theta2 identity, especially if it can be paired "
                "with the period-156 telescoping context."
            ),
            (
                "A dlog or Eisenstein-class formula alone is not enough; it must "
                "emit theta2/theta2^-1 for the normalized-y product over the "
                "specific K trace, short D segment, and T edge."
            ),
            "continue as the highest-value D=2 theorem source",
            interface.row_ok
            and interface.support_denominator_gcd_p25_minus_1 == 1
            and interface.d_segment_is_not_subgroup_norm,
        ),
        TheoremSourceRow(
            "kubert_lang_siegel_exponent_matrix",
            "https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_4",
            (
                "Kubert-Lang's Siegel-unit framework is the primary modular-unit "
                "source for representing unit payloads by products of Siegel "
                "functions."
            ),
            (
                "Continue only as an exponent-matrix search whose finite divisor "
                "is the exact six-cell packet or exact 300-term theta2 payload."
            ),
            (
                "Generic generation of modular units is too broad; the exponent "
                "matrix must satisfy the p25 packet, T edge, and period-156 "
                "certificate constraints."
            ),
            "continue as a finite exponent-matrix producer search",
            interface.quotient_packet_exact
            and interface.theta2_support == 300
            and interface.expanded_support_resolvent_budget == 46800,
        ),
        TheoremSourceRow(
            "koo_shin_yoon_normalized_wp_prime",
            "https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf",
            (
                "Koo-Shin-Yoon use normalized Weierstrass wp-prime / y-coordinate "
                "singular values and Siegel-Ramachandra-style invariants to "
                "generate ray class fields."
            ),
            (
                "This keeps the y/differential sign-breaking route alive, because "
                "our finite product is literally built from normalized-y factors."
            ),
            (
                "Class-field generation is not a payload.  A candidate still must "
                "land on y(A)/y(A+T), the nontrivial T=(2,113) edge, and the "
                "period-156 theta2 certificate."
            ),
            "continue as value/differential source, not as a generic CM transfer",
            interface.forward_product_is_theta2_inverse
            and interface.t_edge_not_absorbed_by_k
            and interface.bridge_fixed_by_support_period,
        ),
    )

    conditional_rows = (
        TheoremSourceRow(
            "kubert_lang_siegel_robert_class_field_units",
            "https://link.springer.com/chapter/10.1007/978-1-4757-1741-9_11",
            (
                "Kubert-Lang's Siegel-Robert class-field chapter constructs "
                "units from modular-function values and explicitly keeps powers "
                "that avoid root ambiguities."
            ),
            (
                "This is compatible with our value-level warning: ambient-order "
                "values need branch control, while support-period values have a "
                "unique F_p root if fixedness is proved."
            ),
            (
                "Conditional on producing the period-156 fixedness/telescoping "
                "data; otherwise it falls back to the ambient 780 branch problem."
            ),
            "conditional continue for value-level theorem hits with branch control",
            interface.ambient_denominator_gcd_p25_minus_1 == 11
            and interface.support_denominator_gcd_p25_minus_1 == 1,
        ),
    )

    kill_rows = (
        TheoremSourceRow(
            "scholl_kato_thetaD_direct",
            "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            (
                "Scholl's exposition of Kato theta_D functions assumes "
                "(6,D)=1 and gives the theta(u)^D^2/theta(Du) unit and "
                "distribution relation in that setting."
            ),
            (
                "This is the correct odd-D control, but it is not the p25 D=2 "
                "normalized-y theorem."
            ),
            "D=2 is outside the ordinary theta_D unit theorem's prime-to-6 gate.",
            "kill as a direct D=2 proof; retain as odd-D sanity check",
            interface.forward_product_is_theta2_inverse,
        ),
        TheoremSourceRow(
            "scholl_robert_literal_subgroup_support",
            "https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf",
            (
                "The Robert generalization uses finite subgroup divisors of "
                "order prime to 6."
            ),
            (
                "Our D_segment is a length-3 arithmetic segment in a point of "
                "visible order 507 and raw order 12675, not subgroup support."
            ),
            "visible 3D=(0,9) and raw 3D=(66,9) reject an order-3 subgroup norm.",
            "kill literal subgroup/coset explanations for D_segment",
            interface.d_segment_is_not_subgroup_norm,
        ),
    )

    all_rows = continue_rows + conditional_rows + kill_rows
    row_ok = (
        interface.row_ok
        and len(continue_rows) == 3
        and len(conditional_rows) == 1
        and len(kill_rows) == 2
        and all(row.row_ok for row in all_rows)
        and interface.source_centers_support == 75
        and interface.y_evaluation_support == 150
        and interface.theta2_support == 300
        and interface.support_denominator_gcd_p25_minus_1 == 1
        and interface.ambient_denominator_gcd_p25_minus_1 == 11
    )

    return TheoremSourceScreenProfile(
        theorem_interface_ok=interface.row_ok,
        continue_rows=continue_rows,
        conditional_rows=conditional_rows,
        kill_rows=kill_rows,
        primary_source_count=len(all_rows),
        best_next_probe=(
            "Try a Sprang/Kronecker D=2 differential or value identity and force "
            "it through the period-156 theta2 interface; in parallel, search a "
            "Kubert-Lang Siegel exponent matrix for the exact six-cell packet."
        ),
        lit_search_brief=(
            "Look for a D=2 normalized-y / Kronecker / Siegel-unit product "
            "identity over a true 25-point K trace, a short non-subgroup "
            "D segment, and the nontrivial T edge; reject direct odd-D Kato "
            "theta_D and literal Robert subgroup support."
        ),
        row_ok=row_ok,
    )


def main() -> int:
    print("p25 Lane B Robert KSY normalized-y theorem-source screen gate")
    profile = profile_theorem_source_screen()
    print(f"theorem_source_screen_profile={profile}")
    print("continue_sources")
    for row in profile.continue_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("conditional_sources")
    for row in profile.conditional_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("kill_sources")
    for row in profile.kill_rows:
        print(f"  {row.name}: ok={int(row.row_ok)} recommendation={row.recommendation}")
    print("source_screen_laws")
    print("  sprang_kronecker_D2_is_highest_value_D2_theorem_source=1")
    print("  kubert_lang_siegel_units_continue_only_as_exact_exponent_matrix_search=1")
    print("  koo_shin_yoon_wp_prime_keeps_y_value_route_alive=1")
    print("  ordinary_kato_thetaD_direct_route_is_killed_for_D2=1")
    print("  literal_robert_subgroup_support_is_killed_by_non_subgroup_D_segment=1")
    print("interpretation")
    print("  next_probe_should_target_D2_normalized_y_identity_or_exact_siegel_exponent_matrix=1")
    print("  this_gate_is_a_source_screen_not_the_missing_theorem=1")
    print(f"robert_ksy_theta2_theorem_source_screen_rows={int(profile.row_ok)}/1")
    print("conclusion=reported_p25_laneB_robert_ksy_theta2_theorem_source_screen_gate")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
