#!/usr/bin/env python3
"""Coefficient-6 root normalization for the p25 support-156 target.

All four current H0/conductor-39 product rows have coefficients +/-6.  This
gate records which lower-coefficient root statements can be normalized back to
the current target and which root-extraction shortcuts remain ambiguous over
F_p^*.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate import (
    profile_sparse_h90_product_normal_form,
)


P25 = 10_000_000_000_000_000_000_000_013
CURRENT_COEFFICIENT = 6


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RootDecision:
    name: str
    shape: str
    decision: str
    source_candidate_if_theorem_present: bool
    normalize_then_intake: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class Coefficient6RootNormalization:
    evidence_markers: tuple[EvidenceMarker, ...]
    p_minus_1_gcd_2: int
    p_minus_1_gcd_3: int
    p_minus_1_gcd_6: int
    cube_map_bijective: bool
    square_root_kernel_size: int
    sixth_root_kernel_size: int
    current_coefficient: int
    legal_rows: int
    row_coefficients_all_six: bool
    divide_by_2_integer: bool
    divide_by_3_integer: bool
    divide_by_6_integer: bool
    decisions: tuple[RootDecision, ...]
    evidence_markers_ok: int
    source_candidate_shapes: int
    normalize_rows: int
    repair_rows: int
    reject_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "p25_v2_current_expert_response_rubric_rows=1/1",
        ),
    )


def decisions() -> tuple[RootDecision, ...]:
    return (
        RootDecision(
            name="current_coefficient6_row_theorem",
            shape="finite value/divisor theorem for the current coefficient-6 support-156 row",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            normalize_then_intake=False,
            first_missing_or_falsifier="downstream DANGER3 framing and extraction",
            ok=True,
        ),
        RootDecision(
            name="coefficient2_exact_root_value",
            shape="exact theorem for the coefficient-2 root row; cubing gives the current row",
            decision="normalize_cube_power_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after cubing to coefficient 6",
            ok=True,
        ),
        RootDecision(
            name="coefficient3_exact_root_value",
            shape="exact theorem for the coefficient-3 root row; squaring gives the current row",
            decision="normalize_square_power_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after squaring to coefficient 6",
            ok=True,
        ),
        RootDecision(
            name="coefficient1_exact_root_value",
            shape="exact theorem for the coefficient-1 root row; sixth power gives the current row",
            decision="normalize_sixth_power_then_apply_source_snippet_intake",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=True,
            first_missing_or_falsifier="same theorem data after taking the sixth power to coefficient 6",
            ok=True,
        ),
        RootDecision(
            name="infer_square_or_sixth_root_from_current_value",
            shape="try to infer a coefficient-3 or coefficient-1 root from the coefficient-6 value",
            decision="repair_coefficient6_root_orientation_missing",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="explicit oriented root/sign data; square and sixth roots have a two-element kernel",
            ok=True,
        ),
        RootDecision(
            name="scaled_boundary_as_current_target",
            shape="treat a coefficient-1, coefficient-2, or coefficient-3 boundary as the current Norm_156(Y_507) boundary",
            decision="reject_boundary_scale_mismatch",
            source_candidate_if_theorem_present=False,
            normalize_then_intake=False,
            first_missing_or_falsifier="power back to the coefficient-6 row or prove the current boundary directly",
            ok=True,
        ),
    )


def build_contract() -> Coefficient6RootNormalization:
    markers = evidence_markers()
    product = profile_sparse_h90_product_normal_form()
    row_counts = tuple(row.lifted_coefficient_counts for row in product.legal_rows)
    all_six = all(counts == ((-6, 78), (6, 78)) for counts in row_counts)
    rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in rows)
    normalize = sum(row.normalize_then_intake for row in rows)
    repairs = sum(row.decision.startswith("repair_") for row in rows)
    rejects = sum(row.decision.startswith("reject_") for row in rows)
    current_closers = 0
    expected = (
        "source_stage_candidate_if_theorem_present",
        "normalize_cube_power_then_apply_source_snippet_intake",
        "normalize_square_power_then_apply_source_snippet_intake",
        "normalize_sixth_power_then_apply_source_snippet_intake",
        "repair_coefficient6_root_orientation_missing",
        "reject_boundary_scale_mismatch",
    )
    row_ok = (
        markers_ok == len(markers)
        and product.row_ok
        and gcd(2, P25 - 1) == 2
        and gcd(3, P25 - 1) == 1
        and gcd(6, P25 - 1) == 2
        and all_six
        and len(product.legal_rows) == 4
        and CURRENT_COEFFICIENT == 6
        and CURRENT_COEFFICIENT % 2 == 0
        and CURRENT_COEFFICIENT % 3 == 0
        and CURRENT_COEFFICIENT % 6 == 0
        and len(rows) == 6
        and tuple(row.decision for row in rows) == expected
        and source_candidates == 1
        and normalize == 3
        and repairs == 1
        and rejects == 1
        and current_closers == 0
        and all(row.ok for row in rows)
    )
    return Coefficient6RootNormalization(
        evidence_markers=markers,
        p_minus_1_gcd_2=gcd(2, P25 - 1),
        p_minus_1_gcd_3=gcd(3, P25 - 1),
        p_minus_1_gcd_6=gcd(6, P25 - 1),
        cube_map_bijective=gcd(3, P25 - 1) == 1,
        square_root_kernel_size=gcd(2, P25 - 1),
        sixth_root_kernel_size=gcd(6, P25 - 1),
        current_coefficient=CURRENT_COEFFICIENT,
        legal_rows=len(product.legal_rows),
        row_coefficients_all_six=all_six,
        divide_by_2_integer=CURRENT_COEFFICIENT % 2 == 0,
        divide_by_3_integer=CURRENT_COEFFICIENT % 3 == 0,
        divide_by_6_integer=CURRENT_COEFFICIENT % 6 == 0,
        decisions=rows,
        evidence_markers_ok=markers_ok,
        source_candidate_shapes=source_candidates,
        normalize_rows=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    contract = build_contract()
    for row in contract.evidence_markers:
        print(f"marker {row.name}: {'ok' if row.ok else 'MISSING'}")
    print("arithmetic")
    print(f"  gcd_2_pminus1={contract.p_minus_1_gcd_2}")
    print(f"  gcd_3_pminus1={contract.p_minus_1_gcd_3}")
    print(f"  gcd_6_pminus1={contract.p_minus_1_gcd_6}")
    print(f"  cube_map_bijective={int(contract.cube_map_bijective)}")
    print(f"  square_root_kernel_size={contract.square_root_kernel_size}")
    print(f"  sixth_root_kernel_size={contract.sixth_root_kernel_size}")
    print("row_payload")
    print(f"  current_coefficient={contract.current_coefficient}")
    print(f"  legal_rows={contract.legal_rows}")
    print(f"  row_coefficients_all_six={int(contract.row_coefficients_all_six)}")
    print(f"  divide_by_2_integer={int(contract.divide_by_2_integer)}")
    print(f"  divide_by_3_integer={int(contract.divide_by_3_integer)}")
    print(f"  divide_by_6_integer={int(contract.divide_by_6_integer)}")
    print("decisions")
    for row in contract.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)} "
            f"normalize={int(row.normalize_then_intake)}"
        )
        print(f"    shape={row.shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={contract.evidence_markers_ok}/{len(contract.evidence_markers)}")
    print(f"  source_candidate_shapes={contract.source_candidate_shapes}")
    print(f"  normalize_rows={contract.normalize_rows}")
    print(f"  repair_rows={contract.repair_rows}")
    print(f"  reject_rows={contract.reject_rows}")
    print(f"  current_source_stage_closers={contract.current_source_stage_closers}")
    print("interpretation")
    print("  exact_lower_coefficient_root_theorem_can_power_to_current_row=1")
    print("  cube_root_in_Fp_star_is_unique_for_p25=1")
    print("  square_or_sixth_root_inference_has_sign_kernel=1")
    print("  scaled_boundary_is_not_current_norm_boundary=1")
    print(f"p25_v2_coefficient6_root_normalization_rows={int(contract.row_ok)}/1")
    return 0 if contract.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
