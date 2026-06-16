#!/usr/bin/env python3
"""KSY normalized-y formula-to-product upgrade frontier.

The active KL/KSY lane needs an exact product theorem, not another broad source
pass.  Koo-Shin-Yoon arXiv:1007.2307 supplies the atom-level normalized-y
formula and several field-generation statements.  This gate records the exact
boundary between those source clauses and the p25 payload we need.

The gate is intentionally lightweight: it scans the local TeX source for the
primary clauses and uses only fixed p25 product checksums.  It does not re-run
the heavy theta2/value-root harness.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


SOURCE_TEX = Path("/tmp/p25_lit_scout/1007.2307/source.tex")

P25_C = (47, 28)
P25_D = (22, 3)
P25_K = (57, 0)
K_TRACE_LENGTH = 25
D_SEGMENT_LENGTH = 3
ANTI_INVARIANT_LAYERS = 2
KSY_ATOMS = K_TRACE_LENGTH * D_SEGMENT_LENGTH
THETA_FOOTPRINT_TERMS = KSY_ATOMS * 4
SUPPORT_PERIOD = 156


@dataclass(frozen=True)
class KsyUpgradeRow:
    name: str
    source_window: str
    source_clause_present: bool
    source_output: str
    p25_product_payload: bool
    first_missing_clause: str
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class KsyNormalizedYProductUpgradeFrontier:
    source_present: bool
    rows: tuple[KsyUpgradeRow, ...]
    p25_atoms: int
    theta_footprint_terms: int
    support_period: int
    formula_language_rows: int
    generation_or_single_value_rows: int
    exact_product_rows_present: int
    direct_closing_rows: int
    hypothetical_closing_rows: int
    heavy_theta2_harness_required_for_this_gate: bool
    row_ok: bool


def source_text() -> str:
    if not SOURCE_TEX.exists():
        return ""
    return SOURCE_TEX.read_text(encoding="utf-8", errors="replace")


def has_all(text: str, needles: tuple[str, ...]) -> bool:
    return all(needle in text for needle in needles)


def upgrade_rows(text: str) -> tuple[KsyUpgradeRow, ...]:
    atom_formula = has_all(
        text,
        (
            "y_{(r_1,~r_2)}(\\tau)=-\\frac{g_{(2r_1,~2r_2)}(\\tau)}",
            "g_{(r_1,~r_2)}(\\tau)^4",
        ),
    )
    theorem_53 = has_all(
        text,
        (
            "\\begin{theorem}\\label{main}",
            "K_{(N)}=K\\bigg(x_{(0,~\\frac{1}{N})}(\\theta)",
            "y_{(0,~\\frac{1}{N})}(\\theta)^\\frac{4}{\\gcd(4,~N)}",
        ),
    )
    schertz_generator = has_all(
        text,
        (
            "\\begin{theorem}\\label{generator}",
            "\\varepsilon=\\frac{g_\\mathfrak{f}(C')}{g_\\mathfrak{f}(C_0)^4}",
            "generates $K_\\mathfrak{f}$ over $K$",
        ),
    )
    schertz_corollary = has_all(
        text,
        (
            "\\begin{corollary}\\label{Schertz}",
            "y_{(0,~\\frac{1}{N})}(\\theta)^4",
            "generates $K_{(N)}$ over $K$",
        ),
    )

    return (
        KsyUpgradeRow(
            name="ksy_equation_3_4_atom_formula",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:420-466",
            source_clause_present=atom_formula,
            source_output="atom formula y(Q)=-g(2Q)/g(Q)^4",
            p25_product_payload=False,
            first_missing_clause="product/distribution theorem over the exact 75 p25 atoms",
            decision="conditional_atom_formula_not_product_theorem",
            row_ok=atom_formula,
        ),
        KsyUpgradeRow(
            name="ksy_theorem_5_3_ray_class_generation",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1000-1080",
            source_clause_present=theorem_53,
            source_output="ray-class generation from one torsion point coordinate pair",
            p25_product_payload=False,
            first_missing_clause="exact divisor/additive identity for P",
            decision="reject_generation_theorem_as_direct_p25_closer",
            row_ok=theorem_53,
        ),
        KsyUpgradeRow(
            name="ksy_theorem_6_2_schertz_ratio",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1160-1235",
            source_clause_present=schertz_generator,
            source_output="single Siegel-Ramachandra ratio generates a ray class field",
            p25_product_payload=False,
            first_missing_clause="mixed C3 x C169 K-traced row graph and orientation",
            decision="reject_single_ratio_generation_as_direct_p25_closer",
            row_ok=schertz_generator,
        ),
        KsyUpgradeRow(
            name="ksy_corollary_6_4_single_y_generator",
            source_window="/tmp/p25_lit_scout/1007.2307/source.tex:1235-1280",
            source_clause_present=schertz_corollary,
            source_output="single y(0,1/N)^4 generator under odd-N Schertz hypotheses",
            p25_product_payload=False,
            first_missing_clause="exact P and full 75-atom distribution",
            decision="conditional_single_y_value_not_product_theorem",
            row_ok=schertz_corollary,
        ),
        KsyUpgradeRow(
            name="future_ksy_exact_product_distribution",
            source_window="not present in inspected KSY source",
            source_clause_present=False,
            source_output="hypothetical exact K-traced normalized-y product theorem",
            p25_product_payload=True,
            first_missing_clause="none if it also records orientation and challenge-legal framing",
            decision="accept_only_if_new_theorem_emits_exact_P",
            row_ok=True,
        ),
    )


def profile_ksy_normalized_y_product_upgrade_frontier() -> KsyNormalizedYProductUpgradeFrontier:
    text = source_text()
    rows = upgrade_rows(text)
    formula_rows = sum(row.name == "ksy_equation_3_4_atom_formula" for row in rows)
    generation_rows = sum(
        row.name
        in {
            "ksy_theorem_5_3_ray_class_generation",
            "ksy_theorem_6_2_schertz_ratio",
            "ksy_corollary_6_4_single_y_generator",
        }
        for row in rows
    )
    exact_present = sum(row.source_clause_present and row.p25_product_payload for row in rows)
    direct_closing = sum(row.source_clause_present and row.p25_product_payload for row in rows)
    hypothetical_closing = sum((not row.source_clause_present) and row.p25_product_payload for row in rows)
    row_ok = (
        SOURCE_TEX.exists()
        and formula_rows == 1
        and generation_rows == 3
        and exact_present == 0
        and direct_closing == 0
        and hypothetical_closing == 1
        and KSY_ATOMS == 75
        and THETA_FOOTPRINT_TERMS == 300
        and SUPPORT_PERIOD == 156
        and all(row.row_ok for row in rows)
        and tuple(row.decision for row in rows)
        == (
            "conditional_atom_formula_not_product_theorem",
            "reject_generation_theorem_as_direct_p25_closer",
            "reject_single_ratio_generation_as_direct_p25_closer",
            "conditional_single_y_value_not_product_theorem",
            "accept_only_if_new_theorem_emits_exact_P",
        )
    )
    return KsyNormalizedYProductUpgradeFrontier(
        source_present=SOURCE_TEX.exists(),
        rows=rows,
        p25_atoms=KSY_ATOMS,
        theta_footprint_terms=THETA_FOOTPRINT_TERMS,
        support_period=SUPPORT_PERIOD,
        formula_language_rows=formula_rows,
        generation_or_single_value_rows=generation_rows,
        exact_product_rows_present=exact_present,
        direct_closing_rows=direct_closing,
        hypothetical_closing_rows=hypothetical_closing,
        heavy_theta2_harness_required_for_this_gate=False,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_ksy_normalized_y_product_upgrade_frontier()
    print("p25 KSY-y normalized-y product-upgrade frontier gate")
    print(f"source_tex={SOURCE_TEX}")
    print(f"source_present={int(profile.source_present)}")
    print("p25_product_checksums")
    print(f"  C={P25_C} D={P25_D} K={P25_K}")
    print(f"  p25_atoms={profile.p25_atoms}")
    print(f"  theta_footprint_terms={profile.theta_footprint_terms}")
    print(f"  support_period={profile.support_period}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: present={int(row.source_clause_present)} "
            f"payload={int(row.p25_product_payload)} decision={row.decision}"
        )
        print(f"    window={row.source_window}")
        print(f"    output={row.source_output}")
        print(f"    missing={row.first_missing_clause}")
    print("counts")
    print(f"  formula_language_rows={profile.formula_language_rows}")
    print(f"  generation_or_single_value_rows={profile.generation_or_single_value_rows}")
    print(f"  exact_product_rows_present={profile.exact_product_rows_present}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  hypothetical_closing_rows={profile.hypothetical_closing_rows}")
    print(
        "  heavy_theta2_harness_required_for_this_gate="
        f"{int(profile.heavy_theta2_harness_required_for_this_gate)}"
    )
    print("interpretation")
    print("  KSY_3_4_is_atom_formula_not_product_theorem=1")
    print("  KSY_generation_and_single_y_results_are_not_p25_closers=1")
    print("  active_KSY_lane_requires_exact_75_atom_product_distribution=1")
    print(
        "ksy_y_normalized_y_product_upgrade_frontier_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("KSY normalized-y product-upgrade frontier regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
