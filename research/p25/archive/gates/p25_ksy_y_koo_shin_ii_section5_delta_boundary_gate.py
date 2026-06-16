#!/usr/bin/env python3
"""Koo-Shin II Section 5 Delta-quotient boundary for the p25 KSY-y moonshot.

The supplied arXiv:1007.2318 sequel has an actual prime-power Section 5, so
it deserves more than a filename rejection.  This gate records the precise
boundary: the sequel gives Siegel-Ramachandra norms and a Delta quotient that
generates ring class fields with prime-power conductors, but it does not supply
the missing mixed C_3 x C_169 p25 product.
"""

from __future__ import annotations

from dataclasses import dataclass


SUPPLIED_PATH = "/Users/agent/Downloads/1007.2318v1.pdf"
SUPPLIED_TEXT = "/tmp/p25_lit_scout/koo_shin_supplied_1007_2318_text.txt"
TARGET_PRODUCT = (
    "P=prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK), "
    "C=(47,28), D=(22,3), K=(57,0)"
)


@dataclass(frozen=True)
class Section5Row:
    name: str
    source_window: str
    positive_payload: str
    p25_boundary: str
    verdict: str
    source_verified: bool
    direct_closer: bool
    row_ok: bool


@dataclass(frozen=True)
class Section5Profile:
    rows: tuple[Section5Row, ...]
    source_verified_rows: int
    theorem5_1_generator_rows: int
    lemma5_3_delta_product_rows: int
    theorem5_4_prime_power_rows: int
    one_axis_product_rows: int
    mixed_graph_rows: int
    normalized_y_rows: int
    theorem5_2_body_rows: int
    direct_closing_rows: int
    continue_as_context_rows: int
    still_need_2010_rows: int
    row_ok: bool


def section5_rows() -> tuple[Section5Row, ...]:
    return (
        Section5Row(
            name="jks_ii_section5_setup",
            source_window=f"{SUPPLIED_TEXT}:1516-1566",
            positive_payload=(
                "Section 5 explicitly targets generators of class fields with "
                "prime-power conductors using singular values of the Delta "
                "function and Siegel-Ramachandra invariants"
            ),
            p25_boundary=(
                "this is CM/ring-class-field generator context, not a finite "
                "normalized-y product for the p25 atoms"
            ),
            verdict="prime_power_class_field_context_not_p25_product",
            source_verified=True,
            direct_closer=False,
            row_ok=True,
        ),
        Section5Row(
            name="jks_ii_theorem5_1_siegel_ramachandra_norm",
            source_window=f"{SUPPLIED_TEXT}:1568-1649",
            positive_payload=(
                "Theorem 5.1 says a norm of the Siegel-Ramachandra invariant "
                "g_f(C0) generates an abelian extension L/K under prime-power "
                "conductor and degree hypotheses"
            ),
            p25_boundary=(
                "the output is a class-field generator via Artin characters and "
                "Kronecker limit formulas, not the p25 row-labeled product P"
            ),
            verdict="class_field_generator_not_exact_p25_product",
            source_verified=True,
            direct_closer=False,
            row_ok=True,
        ),
        Section5Row(
            name="jks_ii_lemma5_3_delta_one_axis_product",
            source_window=f"{SUPPLIED_TEXT}:1653-1705",
            positive_payload=(
                "Lemma 5.3 proves prod_{w=1..N-1} g_(0,w/N)^12 equals "
                "N^12 Delta(N tau)/Delta(tau)"
            ),
            p25_boundary=(
                "this is a one-axis full-residue Siegel product; it has no "
                "C_3 row graph, D/K trace, or p25 orientation"
            ),
            verdict="one_axis_delta_product_not_mixed_graph",
            source_verified=True,
            direct_closer=False,
            row_ok=True,
        ),
        Section5Row(
            name="jks_ii_theorem5_4_delta_prime_power_generator",
            source_window=f"{SUPPLIED_TEXT}:1707-1777",
            positive_payload=(
                "Theorem 5.4 uses the Delta quotient p^12 Delta(p^ell theta) / "
                "Delta(p^(ell-1) theta) as a real algebraic integer generating "
                "a ring class field when p is inert or ramified"
            ),
            p25_boundary=(
                "the theorem supplies a CM singular value generator for a "
                "prime-power conductor, not a challenge-legal finite-field "
                "identity or the 75-atom normalized-y p25 product"
            ),
            verdict="delta_prime_power_generator_not_p25_payload",
            source_verified=True,
            direct_closer=False,
            row_ok=True,
        ),
        Section5Row(
            name="koo_shin_2010_theorem5_2_still_missing",
            source_window="needed target: Math. Z. 264 (2010), 137-177, Section 5 / Theorem 5.2",
            positive_payload=(
                "hypothetical theorem body may contain the product/distribution "
                "statement hinted by public snippets"
            ),
            p25_boundary=(
                "only this missing target can decide whether Koo-Shin 2010 "
                "emits exact row labels, reflection center, or raw K-traced product"
            ),
            verdict="missing_2010_theorem_body_remains_live",
            source_verified=False,
            direct_closer=False,
            row_ok=True,
        ),
    )


def profile_koo_shin_ii_section5_delta_boundary() -> Section5Profile:
    rows = section5_rows()
    source_verified_rows = sum(row.source_verified for row in rows)
    theorem5_1_generator_rows = sum("theorem5_1" in row.name for row in rows)
    lemma5_3_delta_product_rows = sum("lemma5_3" in row.name for row in rows)
    theorem5_4_prime_power_rows = sum("theorem5_4" in row.name for row in rows)
    one_axis_product_rows = sum("one_axis" in row.verdict for row in rows)
    mixed_graph_rows = sum("mixed C_3 x C_169" in row.positive_payload for row in rows)
    normalized_y_rows = sum("normalized-y" in row.positive_payload and row.source_verified for row in rows)
    theorem5_2_body_rows = 0
    direct_closing_rows = sum(row.direct_closer for row in rows)
    continue_as_context_rows = sum(row.source_verified and not row.direct_closer for row in rows)
    still_need_2010_rows = sum(row.verdict == "missing_2010_theorem_body_remains_live" for row in rows)
    expected_verdicts = (
        "prime_power_class_field_context_not_p25_product",
        "class_field_generator_not_exact_p25_product",
        "one_axis_delta_product_not_mixed_graph",
        "delta_prime_power_generator_not_p25_payload",
        "missing_2010_theorem_body_remains_live",
    )
    row_ok = (
        TARGET_PRODUCT.startswith("P=prod_")
        and len(rows) == 5
        and source_verified_rows == 4
        and theorem5_1_generator_rows == 1
        and lemma5_3_delta_product_rows == 1
        and theorem5_4_prime_power_rows == 1
        and one_axis_product_rows == 1
        and mixed_graph_rows == 0
        and normalized_y_rows == 0
        and theorem5_2_body_rows == 0
        and direct_closing_rows == 0
        and continue_as_context_rows == 4
        and still_need_2010_rows == 1
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return Section5Profile(
        rows=rows,
        source_verified_rows=source_verified_rows,
        theorem5_1_generator_rows=theorem5_1_generator_rows,
        lemma5_3_delta_product_rows=lemma5_3_delta_product_rows,
        theorem5_4_prime_power_rows=theorem5_4_prime_power_rows,
        one_axis_product_rows=one_axis_product_rows,
        mixed_graph_rows=mixed_graph_rows,
        normalized_y_rows=normalized_y_rows,
        theorem5_2_body_rows=theorem5_2_body_rows,
        direct_closing_rows=direct_closing_rows,
        continue_as_context_rows=continue_as_context_rows,
        still_need_2010_rows=still_need_2010_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_koo_shin_ii_section5_delta_boundary()
    print("p25 KSY-y Koo-Shin II Section 5 Delta boundary gate")
    print(f"supplied_path={SUPPLIED_PATH}")
    print(f"target_product={TARGET_PRODUCT}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: verdict={row.verdict} "
            f"source={int(row.source_verified)} closes={int(row.direct_closer)}"
        )
        print(f"    window={row.source_window}")
        print(f"    boundary={row.p25_boundary}")
    print("counts")
    print(f"  source_verified_rows={profile.source_verified_rows}")
    print(f"  theorem5_1_generator_rows={profile.theorem5_1_generator_rows}")
    print(f"  lemma5_3_delta_product_rows={profile.lemma5_3_delta_product_rows}")
    print(f"  theorem5_4_prime_power_rows={profile.theorem5_4_prime_power_rows}")
    print(f"  one_axis_product_rows={profile.one_axis_product_rows}")
    print(f"  mixed_graph_rows={profile.mixed_graph_rows}")
    print(f"  normalized_y_rows={profile.normalized_y_rows}")
    print(f"  theorem5_2_body_rows={profile.theorem5_2_body_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  continue_as_context_rows={profile.continue_as_context_rows}")
    print(f"  still_need_2010_rows={profile.still_need_2010_rows}")
    print("interpretation")
    print("  koo_shin_ii_section5_is_prime_power_context_not_p25_product=1")
    print("  lemma5_3_delta_product_is_one_axis_not_mixed_graph=1")
    print("  target_2010_theorem5_2_still_needed=1")
    print(
        "ksy_y_koo_shin_ii_section5_delta_boundary_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("Koo-Shin II Section 5 Delta boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
