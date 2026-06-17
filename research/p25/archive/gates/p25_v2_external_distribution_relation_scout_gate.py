#!/usr/bin/env python3
"""Classify external Siegel-unit distribution sources against p25 hooks."""

from __future__ import annotations

from dataclasses import dataclass


MARKER = "p25_v2_external_distribution_relation_scout_rows=1/1"


@dataclass(frozen=True)
class SourceRow:
    key: str
    url: str
    useful: str
    missing: tuple[str, ...]
    decision: str


ROWS = (
    SourceRow(
        key="polylog_eisenstein_distribution_2025",
        url="https://arxiv.org/pdf/2309.10938",
        useful="integral distribution relations for Eisenstein classes",
        missing=(
            "one legal support-156 row",
            "Norm_156(Y_507) boundary",
            "scalar-fixed finite F_p payload",
        ),
        decision="support_distribution_relations_not_p25_row_theorem",
    ),
    SourceRow(
        key="beilinson_kato_modular_symbol_distributions",
        url="https://arxiv.org/html/2311.14620v2",
        useful="Siegel distribution and Manin-relation framework",
        missing=(
            "row label in {1,2,4,8}",
            "finite additive/value specialization",
            "DANGER3 extraction bridge",
        ),
        decision="support_k_theory_distribution_not_finite_row_payload",
    ),
    SourceRow(
        key="kato_siegel_theta_function_notes",
        url="https://swc-math.github.io/notes/files/01MazurPW.pdf",
        useful="canonical theta_D divisor and isogeny compatibility",
        missing=(
            "p25 row selector",
            "D=2-compatible period-156 branch",
            "explicit finite value or additive normalizer",
        ),
        decision="repair_divisor_distribution_not_scalar_fixed_value",
    ),
    SourceRow(
        key="kubert_lang_modular_units",
        url="https://link.springer.com/book/10.1007/978-1-4757-1741-9",
        useful="modular-unit generator and distribution theory",
        missing=(
            "exact p25 selector",
            "arithmetic source theorem",
            "scalar or branch normalization",
        ),
        decision="support_generators_not_selected_finite_identity",
    ),
)

ACCEPTED_DECISIONS = {
    "support_distribution_relations_not_p25_row_theorem",
    "support_k_theory_distribution_not_finite_row_payload",
    "repair_divisor_distribution_not_scalar_fixed_value",
    "support_generators_not_selected_finite_identity",
}


def main() -> int:
    urls_ok = all(row.url.startswith("https://") for row in ROWS)
    decisions_ok = all(row.decision in ACCEPTED_DECISIONS for row in ROWS)
    missing_ok = all(len(row.missing) == 3 for row in ROWS)
    support_rows = sum(1 for row in ROWS if row.decision.startswith("support_"))
    repair_rows = sum(1 for row in ROWS if row.decision.startswith("repair_"))
    source_stage_closers = sum("source_stage_close" in row.decision for row in ROWS)
    row_ok = (
        len(ROWS) == 4
        and urls_ok
        and decisions_ok
        and missing_ok
        and support_rows == 3
        and repair_rows == 1
        and source_stage_closers == 0
    )

    print("p25 v2 external distribution-relation scout")
    print(f"source_rows={len(ROWS)}")
    print(f"source_urls_ok={int(urls_ok)}")
    print(f"decisions_ok={int(decisions_ok)}")
    print(f"missing_clauses_ok={int(missing_ok)}")
    print(f"support_rows={support_rows}")
    print(f"repair_rows={repair_rows}")
    print(f"current_source_stage_closers={source_stage_closers}")
    print(MARKER if row_ok else "p25_v2_external_distribution_relation_scout_rows=0/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
