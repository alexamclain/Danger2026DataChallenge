#!/usr/bin/env python3
"""H0/X_1(16) final certificate boundary for the p25 moonshot.

The H0 source route can now be routed as far as an order-8112 bridge and the
practical X_1(16) Montgomery chart.  This gate records the final certificate
boundary for that specific route: an H0 chart surface is not a DANGER3
submission until it supplies either a checkable halving chain/direct x0 and,
finally, an official vpp.py-verified (p,A,x0) triple.
"""

from __future__ import annotations

from dataclasses import dataclass

from p25_ksy_y_h0_order8112_x16_chart_specialization_gate import (
    P25,
    profile_h0_order8112_x16_chart_specialization,
)
from p25_ksy_y_x1_16_halving_certificate_payload_gate import (
    FINAL_DEPTH,
    HALVING_LINKS,
    START_DEPTH,
    VPP_DOUBLINGS,
    X_CHAIN_POINTS,
    profile_halving_certificate_payload_contract,
)


@dataclass(frozen=True)
class H0X16FinalCertificateRow:
    name: str
    has_h0_source_closure: bool
    has_order8112_bridge: bool
    has_x16_chart_surface: bool
    supplies_A: bool
    supplies_xP16: bool
    supplies_x_chain: bool
    supplies_sqrt_witnesses: bool
    supplies_active_branch_provenance: bool
    supplies_x0: bool
    supplies_internal_verify: bool
    supplies_official_vpp: bool
    decision: str
    first_missing_clause: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0X16FinalCertificateBoundary:
    chart_specialization_ok: bool
    halving_payload_ok: bool
    p_mod_8: int
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    vpp_doublings: int
    rows: tuple[H0X16FinalCertificateRow, ...]
    row_count: int
    surface_reached_rows: int
    rejected_rows: int
    x_chain_rows: int
    sqrt_witness_rows: int
    direct_x0_rows: int
    internal_verify_rows: int
    official_vpp_rows: int
    non_submission_rows: int
    submission_ready_rows: int
    row_ok: bool


def boundary_rows() -> tuple[H0X16FinalCertificateRow, ...]:
    return (
        H0X16FinalCertificateRow(
            name="h0_order8112_chart_surface_only",
            has_h0_source_closure=True,
            has_order8112_bridge=True,
            has_x16_chart_surface=True,
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=False,
            supplies_internal_verify=False,
            supplies_official_vpp=False,
            decision="surface_reached_certificate_missing",
            first_missing_clause="x-chain, sqrt-witness chain, direct x0, or vpp-verified triple",
            next_action="derive a depth-4-to-depth-42 halving chain or direct x0",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_branch_word_without_values",
            has_h0_source_closure=True,
            has_order8112_bridge=True,
            has_x16_chart_surface=True,
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=True,
            supplies_x0=False,
            supplies_internal_verify=False,
            supplies_official_vpp=False,
            decision="reject_branch_word_without_values",
            first_missing_clause="actual square-root witnesses, x-chain, or x0",
            next_action="discard as a certificate unless concrete values are attached",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_sqrt_witness_chain",
            has_h0_source_closure=True,
            has_order8112_bridge=True,
            has_x16_chart_surface=True,
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=True,
            supplies_active_branch_provenance=True,
            supplies_x0=True,
            supplies_internal_verify=False,
            supplies_official_vpp=False,
            decision="active_path_provenance_vpp_missing",
            first_missing_clause="official vpp.py verification",
            next_action="run official vpp.py on the resulting (p,A,x0)",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_x_coordinate_chain",
            has_h0_source_closure=True,
            has_order8112_bridge=True,
            has_x16_chart_surface=True,
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=True,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_internal_verify=False,
            supplies_official_vpp=False,
            decision="checkable_x_chain_vpp_missing",
            first_missing_clause="official vpp.py verification",
            next_action="check each xDBL link, then run official vpp.py",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_direct_A_x0",
            has_h0_source_closure=True,
            has_order8112_bridge=False,
            has_x16_chart_surface=False,
            supplies_A=True,
            supplies_xP16=False,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_internal_verify=False,
            supplies_official_vpp=False,
            decision="direct_x0_vpp_missing",
            first_missing_clause="official vpp.py verification",
            next_action="run official vpp.py; upstream provenance is useful but not required for verification",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_internal_verify_only",
            has_h0_source_closure=True,
            has_order8112_bridge=True,
            has_x16_chart_surface=True,
            supplies_A=True,
            supplies_xP16=True,
            supplies_x_chain=True,
            supplies_sqrt_witnesses=True,
            supplies_active_branch_provenance=True,
            supplies_x0=True,
            supplies_internal_verify=True,
            supplies_official_vpp=False,
            decision="internal_verify_not_submission",
            first_missing_clause="official vpp.py verification and archived output",
            next_action="treat as extraction-ready, then verify and archive with official tooling",
            ok=True,
        ),
        H0X16FinalCertificateRow(
            name="h0_vpp_verified_triple",
            has_h0_source_closure=True,
            has_order8112_bridge=False,
            has_x16_chart_surface=False,
            supplies_A=True,
            supplies_xP16=False,
            supplies_x_chain=False,
            supplies_sqrt_witnesses=False,
            supplies_active_branch_provenance=False,
            supplies_x0=True,
            supplies_internal_verify=True,
            supplies_official_vpp=True,
            decision="submission_ready",
            first_missing_clause="none",
            next_action="archive command, logs, environment, and generate the Lean certificate",
            ok=True,
        ),
    )


def profile_h0_x16_final_certificate_boundary() -> H0X16FinalCertificateBoundary:
    chart = profile_h0_order8112_x16_chart_specialization()
    halving = profile_halving_certificate_payload_contract()
    rows = boundary_rows()
    decisions = tuple(row.decision for row in rows)
    surface_rows = sum(row.has_x16_chart_surface for row in rows)
    rejected_rows = sum(row.decision.startswith("reject_") for row in rows)
    x_chain_rows = sum(row.supplies_x_chain for row in rows)
    sqrt_witness_rows = sum(row.supplies_sqrt_witnesses for row in rows)
    direct_x0_rows = sum(row.supplies_x0 for row in rows)
    internal_rows = sum(row.supplies_internal_verify for row in rows)
    vpp_rows = sum(row.supplies_official_vpp for row in rows)
    submission_rows = sum(row.decision == "submission_ready" for row in rows)
    non_submission_rows = len(rows) - submission_rows
    row_ok = (
        chart.row_ok
        and halving.row_ok
        and P25 % 8 == 5
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and HALVING_LINKS == 38
        and X_CHAIN_POINTS == 39
        and VPP_DOUBLINGS == 42
        and len(rows) == 7
        and surface_rows == 5
        and rejected_rows == 1
        and x_chain_rows == 2
        and sqrt_witness_rows == 2
        and direct_x0_rows == 5
        and internal_rows == 2
        and vpp_rows == 1
        and non_submission_rows == 6
        and submission_rows == 1
        and decisions
        == (
            "surface_reached_certificate_missing",
            "reject_branch_word_without_values",
            "active_path_provenance_vpp_missing",
            "checkable_x_chain_vpp_missing",
            "direct_x0_vpp_missing",
            "internal_verify_not_submission",
            "submission_ready",
        )
        and all(row.ok for row in rows)
    )
    return H0X16FinalCertificateBoundary(
        chart_specialization_ok=chart.row_ok,
        halving_payload_ok=halving.row_ok,
        p_mod_8=P25 % 8,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        x_chain_points=X_CHAIN_POINTS,
        vpp_doublings=VPP_DOUBLINGS,
        rows=rows,
        row_count=len(rows),
        surface_reached_rows=surface_rows,
        rejected_rows=rejected_rows,
        x_chain_rows=x_chain_rows,
        sqrt_witness_rows=sqrt_witness_rows,
        direct_x0_rows=direct_x0_rows,
        internal_verify_rows=internal_rows,
        official_vpp_rows=vpp_rows,
        non_submission_rows=non_submission_rows,
        submission_ready_rows=submission_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_x16_final_certificate_boundary()
    print("p25 KSY-y H0/X1(16) final certificate boundary gate")
    print("dependencies")
    print(f"  chart_specialization_ok={int(profile.chart_specialization_ok)}")
    print(f"  halving_payload_ok={int(profile.halving_payload_ok)}")
    print("shape")
    print(f"  p_mod_8={profile.p_mod_8}")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print(f"  vpp_doublings={profile.vpp_doublings}")
    print("boundary_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: h0={int(row.has_h0_source_closure)} "
            f"R8112={int(row.has_order8112_bridge)} "
            f"x16={int(row.has_x16_chart_surface)} A={int(row.supplies_A)} "
            f"xP16={int(row.supplies_xP16)} x_chain={int(row.supplies_x_chain)} "
            f"sqrt={int(row.supplies_sqrt_witnesses)} "
            f"branch={int(row.supplies_active_branch_provenance)} "
            f"x0={int(row.supplies_x0)} internal={int(row.supplies_internal_verify)} "
            f"vpp={int(row.supplies_official_vpp)} decision={row.decision} "
            f"missing={row.first_missing_clause}"
        )
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  surface_reached_rows={profile.surface_reached_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  x_chain_rows={profile.x_chain_rows}")
    print(f"  sqrt_witness_rows={profile.sqrt_witness_rows}")
    print(f"  direct_x0_rows={profile.direct_x0_rows}")
    print(f"  internal_verify_rows={profile.internal_verify_rows}")
    print(f"  official_vpp_rows={profile.official_vpp_rows}")
    print(f"  non_submission_rows={profile.non_submission_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  H0_chart_surface_is_not_a_submission_without_x0_and_vpp=1")
    print("  branch_word_without_values_is_rejected=1")
    print("  x_chain_or_sqrt_chain_is_extraction_ready_but_vpp_missing=1")
    print("  only_official_vpp_verified_A_x0_is_submission_ready=1")
    print(f"ksy_y_h0_x16_final_certificate_boundary_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0/X1(16) final certificate boundary regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
