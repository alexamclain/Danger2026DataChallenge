#!/usr/bin/env python3
"""Halving-certificate payload contract for p25 X_1(16) extraction.

The active search obtains x0 from A,xP16 by repeated halving.  A future theorem
or extraction routine does not need to reproduce the C square-root branch order
to be independently checkable: it may instead provide the x-coordinate chain
x4=xP16, x5, ..., x42=x0, where each x_{i+1} doubles back to x_i on the same
Montgomery curve.  Official vpp.py remains the final submission boundary.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_x1_16_halving_chain_contract_gate import (
    profile_x1_16_halving_chain_contract,
)


START_DEPTH = 4
FINAL_DEPTH = 42
HALVING_LINKS = FINAL_DEPTH - START_DEPTH
X_CHAIN_POINTS = HALVING_LINKS + 1
VPP_DOUBLINGS = FINAL_DEPTH


@dataclass(frozen=True)
class CertificateFormulaRow:
    name: str
    formula: str
    checkable_from_x_chain: bool
    needs_square_root_branch_provenance: bool
    official_submission_boundary: bool
    ok: bool


@dataclass(frozen=True)
class CertificatePayloadRow:
    name: str
    supplies_A: bool
    supplies_xP16: bool
    supplies_x_chain: bool
    supplies_sqrt_witnesses: bool
    supplies_active_branch_provenance: bool
    supplies_x0: bool
    supplies_vpp_verified: bool
    decision: str
    first_missing_clause: str
    ok: bool


@dataclass(frozen=True)
class HalvingCertificatePayloadContract:
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    vpp_doublings: int
    halving_chain_contract_ok: bool
    formula_rows: tuple[CertificateFormulaRow, ...]
    payload_rows: tuple[CertificatePayloadRow, ...]
    x_chain_formula_rows: int
    sqrt_branch_formula_rows: int
    official_boundary_formula_rows: int
    x_chain_payload_rows: int
    active_provenance_payload_rows: int
    direct_x0_payload_rows: int
    vpp_verified_payload_rows: int
    row_ok: bool


def formula_rows() -> tuple[CertificateFormulaRow, ...]:
    return (
        CertificateFormulaRow(
            name="x_chain_shape",
            formula="payload contains x_4=xP16, x_5, ..., x_42=x0",
            checkable_from_x_chain=True,
            needs_square_root_branch_provenance=False,
            official_submission_boundary=False,
            ok=True,
        ),
        CertificateFormulaRow(
            name="montgomery_doubling_link",
            formula=(
                "for each i=4..41, xDBL(x_{i+1}:1) has affine x-coordinate x_i "
                "on By^2=x^3+A*x^2+x"
            ),
            checkable_from_x_chain=True,
            needs_square_root_branch_provenance=False,
            official_submission_boundary=False,
            ok=True,
        ),
        CertificateFormulaRow(
            name="projective_link_equation",
            formula=(
                "with C=(A+2)/4, U=(X+Z)^2, V=(X-Z)^2, W=U-V, "
                "X'=U*V, Z'=W*(V+C*W), require X'-x_i*Z'=0 and Z'!=0"
            ),
            checkable_from_x_chain=True,
            needs_square_root_branch_provenance=False,
            official_submission_boundary=False,
            ok=True,
        ),
        CertificateFormulaRow(
            name="active_branch_witnesses",
            formula=(
                "to prove active C-path provenance, include sqrt(d), chosen u branch, "
                "sqrt(w), candidate order, and first-nonzero choice for each step"
            ),
            checkable_from_x_chain=False,
            needs_square_root_branch_provenance=True,
            official_submission_boundary=False,
            ok=True,
        ),
        CertificateFormulaRow(
            name="x0_vpp_boundary",
            formula="official vpp.py verifies (p,A,x0) by 42 doublings with Z_42=0 and gcd(Z_41,p)=1",
            checkable_from_x_chain=False,
            needs_square_root_branch_provenance=False,
            official_submission_boundary=True,
            ok=True,
        ),
    )


def payload_rows() -> tuple[CertificatePayloadRow, ...]:
    return (
        CertificatePayloadRow(
            name="surface_only",
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=False,
            supplies_vpp_verified=False,
            decision="surface_reached_certificate_missing",
            first_missing_clause="x-chain, sqrt-witness chain, direct x0, or vpp-verified triple",
            ok=True,
        ),
        CertificatePayloadRow(
            name="branch_word_without_values",
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=True,
            supplies_x0=False,
            supplies_vpp_verified=False,
            decision="reject_branch_word_without_values",
            first_missing_clause="actual square-root witnesses, x-chain, or x0",
            ok=True,
        ),
        CertificatePayloadRow(
            name="sqrt_witness_chain",
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=True,
            supplies_active_branch_provenance=True,
            supplies_x0=True,
            supplies_vpp_verified=False,
            decision="active_path_provenance_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        CertificatePayloadRow(
            name="x_coordinate_chain",
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=True,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_vpp_verified=False,
            decision="checkable_x_chain_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        CertificatePayloadRow(
            name="direct_A_x0",
            supplies_A=True,
            supplies_xP16=False,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_vpp_verified=False,
            decision="direct_x0_vpp_missing",
            first_missing_clause="official vpp.py verification",
            ok=True,
        ),
        CertificatePayloadRow(
            name="vpp_verified_triple",
            supplies_A=True,
            supplies_xP16=False,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_vpp_verified=True,
            decision="submission_ready",
            first_missing_clause="none",
            ok=True,
        ),
    )


def profile_halving_certificate_payload_contract() -> HalvingCertificatePayloadContract:
    halving = profile_x1_16_halving_chain_contract()
    formulas = formula_rows()
    payloads = payload_rows()
    x_chain_formulas = sum(row.checkable_from_x_chain for row in formulas)
    sqrt_branch_formulas = sum(row.needs_square_root_branch_provenance for row in formulas)
    official_formulas = sum(row.official_submission_boundary for row in formulas)
    x_chain_payloads = sum(row.supplies_x_chain for row in payloads)
    active_payloads = sum(row.supplies_active_branch_provenance for row in payloads)
    direct_x0_payloads = sum(row.supplies_x0 for row in payloads)
    vpp_payloads = sum(row.supplies_vpp_verified for row in payloads)
    decisions = tuple(row.decision for row in payloads)
    row_ok = (
        halving.row_ok
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and HALVING_LINKS == 38
        and X_CHAIN_POINTS == 39
        and VPP_DOUBLINGS == 42
        and halving.active_halving_steps == HALVING_LINKS
        and len(formulas) == 5
        and x_chain_formulas == 3
        and sqrt_branch_formulas == 1
        and official_formulas == 1
        and all(row.ok for row in formulas)
        and len(payloads) == 6
        and x_chain_payloads == 1
        and active_payloads == 2
        and direct_x0_payloads == 4
        and vpp_payloads == 1
        and decisions
        == (
            "surface_reached_certificate_missing",
            "reject_branch_word_without_values",
            "active_path_provenance_vpp_missing",
            "checkable_x_chain_vpp_missing",
            "direct_x0_vpp_missing",
            "submission_ready",
        )
        and all(row.ok for row in payloads)
    )
    return HalvingCertificatePayloadContract(
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        x_chain_points=X_CHAIN_POINTS,
        vpp_doublings=VPP_DOUBLINGS,
        halving_chain_contract_ok=halving.row_ok,
        formula_rows=formulas,
        payload_rows=payloads,
        x_chain_formula_rows=x_chain_formulas,
        sqrt_branch_formula_rows=sqrt_branch_formulas,
        official_boundary_formula_rows=official_formulas,
        x_chain_payload_rows=x_chain_payloads,
        active_provenance_payload_rows=active_payloads,
        direct_x0_payload_rows=direct_x0_payloads,
        vpp_verified_payload_rows=vpp_payloads,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_halving_certificate_payload_contract()
    print("p25 KSY-y X1(16) halving-certificate payload gate")
    print("shape")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print(f"  vpp_doublings={profile.vpp_doublings}")
    print(f"  halving_chain_contract_ok={int(profile.halving_chain_contract_ok)}")
    print("formula_rows")
    for row in profile.formula_rows:
        print(
            "  "
            f"{row.name}: x_chain={int(row.checkable_from_x_chain)} "
            f"branch={int(row.needs_square_root_branch_provenance)} "
            f"vpp={int(row.official_submission_boundary)} formula={row.formula}"
        )
    print("payload_rows")
    for row in profile.payload_rows:
        print(
            "  "
            f"{row.name}: A={int(row.supplies_A)} xP16={int(row.supplies_xP16)} "
            f"x_chain={int(row.supplies_x_chain)} "
            f"sqrt_witnesses={int(row.supplies_sqrt_witnesses)} "
            f"active_prov={int(row.supplies_active_branch_provenance)} "
            f"x0={int(row.supplies_x0)} vpp={int(row.supplies_vpp_verified)} "
            f"decision={row.decision} missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  x_chain_formula_rows={profile.x_chain_formula_rows}")
    print(f"  sqrt_branch_formula_rows={profile.sqrt_branch_formula_rows}")
    print(f"  official_boundary_formula_rows={profile.official_boundary_formula_rows}")
    print(f"  x_chain_payload_rows={profile.x_chain_payload_rows}")
    print(f"  active_provenance_payload_rows={profile.active_provenance_payload_rows}")
    print(f"  direct_x0_payload_rows={profile.direct_x0_payload_rows}")
    print(f"  vpp_verified_payload_rows={profile.vpp_verified_payload_rows}")
    print("interpretation")
    print("  x_coordinate_chain_is_checkable_without_sqrt_branch_provenance=1")
    print("  branch_word_without_values_is_not_a_certificate=1")
    print("  official_vpp_verified_triple_is_submission_ready=1")
    print(f"ksy_y_x1_16_halving_certificate_payload_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("X1(16) halving-certificate payload regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
