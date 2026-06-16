#!/usr/bin/env python3
"""Actual Koo-Shin 2010 Theorem 5.2 verdict for the p25 KSY-y lane.

The supplied Springer/KOASAS PDF resolves the earlier access blocker.  This
gate records what Theorem 5.2 actually gives and routes it through the existing
Koo-Shin theorem-clause intake.

Verdict: The theorem is useful rigidity/root-descent context for prime-level
Siegel products, but it does not close p25 directly.  The p25 product needs the
mixed C_3 x C_169 graph, equal 75 atoms, orientation, and T edge; Theorem 5.2
is stated for odd-prime level products modulo +/- and does not provide that
mixed-level lift.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_koo_shin_pdf_intake_contract_gate import (
    KOASAS_MD5,
    KOASAS_SIZE,
    classify_candidate,
)
from p25_ksy_y_koo_shin_theorem_clause_intake_gate import (
    KooShinTheoremClauseClaim,
    classify_claim,
)


PDF_CANDIDATES = (
    Path("/Users/agent/Downloads/s00209-008-0456-9.pdf"),
    Path("/Users/agent/Documents/Codex/pomerance-p25-run/incoming/s00209-008-0456-9.pdf"),
    Path("/Users/agent/Documents/Codex/pomerance-p25-run/incoming/000271750900008.pdf"),
)


@dataclass(frozen=True)
class KooShin2010Theorem52VerdictProfile:
    exact_pdf_path: str
    exact_pdf_bytes: int
    exact_pdf_md5: str
    intake_verdict: str
    theorem_body_verified: bool
    theorem_surface: str
    prime_level_product_rigidity: bool
    root_descent_statement: bool
    exact_p25_product_emitted: bool
    mixed_c3_c169_graph_emitted: bool
    t_edge_emitted: bool
    normalized_y_product_emitted: bool
    intake_decision: str
    exact_product_decision: str | None
    first_missing_clause: str
    recommendation: str
    positive_use: str
    row_ok: bool


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_exact_pdf() -> tuple[Path, int, str]:
    for path in PDF_CANDIDATES:
        if not path.exists():
            continue
        bytes_ = path.stat().st_size
        md5 = md5_file(path)
        if bytes_ == KOASAS_SIZE and md5 == KOASAS_MD5:
            return path, bytes_, md5
    return Path(""), 0, ""


def actual_theorem52_claim() -> KooShinTheoremClauseClaim:
    return KooShinTheoremClauseClaim(
        name="koo_shin_2010_theorem_5_2_actual",
        theorem_body_verified=True,
        product_or_distribution_theorem=True,
        modularity_hygiene_only=False,
        odd_prime_or_prime_power_only=True,
        mixed_level_lift=False,
        exact_product_p=False,
        mixed_graph_selector=False,
        equal_weight_atoms=False,
        orientation_branch=False,
        arithmetic_producer=True,
        output_kind="divisor-additive",
        finite_field_identity_for_p=False,
        period_156_context=False,
        danger3_framing=False,
        extraction_to_A_x0=False,
        concrete_vpp_verified_triple=False,
    )


def profile_actual_theorem52_verdict() -> KooShin2010Theorem52VerdictProfile:
    pdf_path, pdf_bytes, pdf_md5 = find_exact_pdf()
    classification = classify_candidate(pdf_path) if pdf_path else None
    decision = classify_claim(actual_theorem52_claim())

    exact_pdf_ok = (
        bool(pdf_path)
        and pdf_bytes == KOASAS_SIZE
        and pdf_md5 == KOASAS_MD5
        and classification is not None
        and classification.verdict == "accept_exact_koasas_pdf"
    )
    row_ok = (
        exact_pdf_ok
        and decision.decision == "reject_prime_power_only_missing_mixed_lift"
        and decision.exact_product_decision == "conditional_missing_exact_product"
        and decision.first_missing_clause == "mixed-level lift preserving C_3 row graph and T edge"
    )
    return KooShin2010Theorem52VerdictProfile(
        exact_pdf_path=str(pdf_path),
        exact_pdf_bytes=pdf_bytes,
        exact_pdf_md5=pdf_md5,
        intake_verdict=classification.verdict if classification is not None else "missing_exact_pdf",
        theorem_body_verified=True,
        theorem_surface=(
            "prime-level Siegel-product rigidity and l-th-root descent over "
            "(1/p Z^2/Z^2)^*/+/-"
        ),
        prime_level_product_rigidity=True,
        root_descent_statement=True,
        exact_p25_product_emitted=False,
        mixed_c3_c169_graph_emitted=False,
        t_edge_emitted=False,
        normalized_y_product_emitted=False,
        intake_decision=decision.decision,
        exact_product_decision=decision.exact_product_decision,
        first_missing_clause=decision.first_missing_clause,
        recommendation=(
            "kill as a direct p25 closer; keep as a rigidity/root-descent "
            "lemma if a separate mixed-level KSY/Kubert-Lang producer appears"
        ),
        positive_use=(
            "can police constant-product ambiguity and l-th-root descent for a "
            "future source theorem, but cannot by itself produce P"
        ),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_actual_theorem52_verdict()
    print("p25 KSY-y Koo-Shin 2010 Theorem 5.2 actual-verdict gate")
    print(f"exact_pdf_path={profile.exact_pdf_path}")
    print(f"exact_pdf_bytes={profile.exact_pdf_bytes}")
    print(f"exact_pdf_md5={profile.exact_pdf_md5}")
    print(f"intake_verdict={profile.intake_verdict}")
    print(f"theorem_surface={profile.theorem_surface}")
    print("theorem52_payload")
    print(f"  prime_level_product_rigidity={int(profile.prime_level_product_rigidity)}")
    print(f"  root_descent_statement={int(profile.root_descent_statement)}")
    print(f"  exact_p25_product_emitted={int(profile.exact_p25_product_emitted)}")
    print(f"  mixed_c3_c169_graph_emitted={int(profile.mixed_c3_c169_graph_emitted)}")
    print(f"  t_edge_emitted={int(profile.t_edge_emitted)}")
    print(f"  normalized_y_product_emitted={int(profile.normalized_y_product_emitted)}")
    print("intake_decision")
    print(f"  decision={profile.intake_decision}")
    print(f"  exact_product_decision={profile.exact_product_decision}")
    print(f"  first_missing_clause={profile.first_missing_clause}")
    print("interpretation")
    print("  koo_shin_2010_theorem52_is_not_direct_p25_closer=1")
    print("  theorem52_remains_useful_as_root_descent_and_constant_rigidity_context=1")
    print(f"  recommendation={profile.recommendation}")
    print(f"ksy_y_koo_shin_2010_theorem52_actual_verdict_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin 2010 Theorem 5.2 verdict regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
