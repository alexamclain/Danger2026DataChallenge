#!/usr/bin/env python3
"""Finite-field intake for H0/order-8112 X_1(16) chart payloads.

The bridge-component intake decides whether odd-level H0/Y507 data is glued to
the level-16 side.  This gate checks the next claim type: actual p25
Montgomery-chart numbers for the production `x16halvenonsplit` surface.

It verifies the X_1(16) y/x equations over F_p, recomputes A and xP16, checks
the nonsplit filter used by the production fleet, and optionally checks the
first-half d-gate and official vpp.py logic when x0 is supplied.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd, isqrt

from p25_ksy_y_h0_order8112_x16_chart_specialization_gate import (
    ACTIVE_MODE,
    OPTIONAL_DGATE_MODE,
    P25,
    profile_h0_order8112_x16_chart_specialization,
)


SAMPLE_Y = 21
SAMPLE_X = 3056787867540315204387750
SAMPLE_A = 5001921875000000000039606
SAMPLE_XP16 = 5641277106015054878246206
SAMPLE_Z = 7810871300106318158204546
SAMPLE_X32 = 8473620875806245623307779


@dataclass(frozen=True)
class X16ChartPayloadClaim:
    name: str
    has_h0_order8112_bridge: bool
    y: int | None
    x: int | None
    A: int | None
    xP16: int | None
    z: int | None
    x32: int | None
    x0: int | None
    run_vpp: bool


@dataclass(frozen=True)
class X16ChartPayloadAudit:
    has_y: bool
    has_x: bool
    has_A: bool
    has_xP16: bool
    has_z: bool
    has_x32: bool
    has_x0: bool
    y_denominators_ok: bool
    model_discriminant_square: bool
    model_root_ok: bool
    nonsplit_filter_ok: bool
    computed_A: int | None
    computed_xP16: int | None
    A_matches: bool
    xP16_matches: bool
    direct_A_xP16_surface_ok: bool
    optional_first_half_square: bool
    z_matches_first_half: bool
    computed_x32: int | None
    x32_matches: bool
    vpp_executed: bool
    vpp_result: bool


@dataclass(frozen=True)
class X16ChartPayloadDecision:
    claim: X16ChartPayloadClaim
    audit: X16ChartPayloadAudit
    decision: str
    x16_surface_reached: bool
    optional_dgate_surface_reached: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class X16ChartPayloadIntakeProfile:
    chart_specialization_ok: bool
    p: int
    k: int
    active_mode: str
    optional_dgate_mode: str
    regression_rows: tuple[X16ChartPayloadDecision, ...]
    row_count: int
    rejected_rows: int
    bridge_missing_rows: int
    y_only_rows: int
    x16_surface_rows: int
    optional_dgate_rows: int
    extraction_ready_rows: int
    vpp_executed_rows: int
    submission_ready_rows: int
    row_ok: bool


def modp(value: int) -> int:
    return value % P25


def inv_mod(value: int) -> int | None:
    value %= P25
    if gcd(value, P25) != 1:
        return None
    return pow(value, -1, P25)


def legendre(value: int) -> int:
    value %= P25
    if value == 0:
        return 0
    out = pow(value, (P25 - 1) // 2, P25)
    return -1 if out == P25 - 1 else out


def sqrt_mod(value: int) -> int | None:
    value %= P25
    if value == 0:
        return 0
    if legendre(value) != 1:
        return None
    root = pow(value, (P25 + 3) // 8, P25)
    if root * root % P25 != value:
        root = root * pow(2, (P25 - 1) // 4, P25) % P25
    if root * root % P25 != value:
        return None
    return root


def x16_A_numerator(y: int) -> int:
    return (
        pow(y, 8, P25)
        - 8 * pow(y, 7, P25)
        + 24 * pow(y, 6, P25)
        - 32 * pow(y, 5, P25)
        + 8 * pow(y, 4, P25)
        + 32 * pow(y, 3, P25)
        - 48 * pow(y, 2, P25)
        + 32 * y
        - 8
    ) % P25


def compute_A_xP16(y: int, x: int) -> tuple[int | None, int | None]:
    den_A = 4 * pow((y - 1) % P25, 4, P25) % P25
    den_x = (x - y) % P25
    inv_den_A = inv_mod(den_A)
    inv_den_x = inv_mod(den_x)
    if inv_den_A is None or inv_den_x is None:
        return None, None
    A = x16_A_numerator(y) * inv_den_A % P25
    xP16 = x * inv_den_x % P25
    if not (2 < A < P25 - 2):
        return None, xP16
    return A, xP16


def y_denominators_ok(y: int) -> bool:
    y2 = y * y % P25
    return y != 0 and y != 1 and (y2 - 2 * y) % P25 != 0


def model_discriminant(y: int) -> int:
    y2 = y * y % P25
    y3 = y2 * y % P25
    qa = (y2 - 2 * y) % P25
    qb = (2 * y2 - y3) % P25
    qc = (1 - y) % P25
    return (qb * qb - 4 * qa * qc) % P25


def model_equation_ok(y: int, x: int) -> bool:
    y2 = y * y % P25
    y3 = y2 * y % P25
    qa = (y2 - 2 * y) % P25
    qb = (2 * y2 - y3) % P25
    qc = (1 - y) % P25
    return (qa * x * x + qb * x + qc) % P25 == 0


def nonsplit_filter_ok(y: int) -> bool:
    y2 = y * y % P25
    value = (y2 - 2) * (y2 - 4 * y + 2) % P25
    return value != 0 and legendre(value) == -1


def first_half_value(y: int) -> int:
    y2 = y * y % P25
    return (y - 1) * (y2 - 2) * (y2 - 2 * y + 2) % P25


def affine_double(A: int, x: int) -> int | None:
    numerator = (x * x - 1) % P25
    denominator = 4 * x % P25 * ((x * x + A * x + 1) % P25) % P25
    inv_denominator = inv_mod(denominator)
    if inv_denominator is None:
        return None
    return numerator * numerator % P25 * inv_denominator % P25


def halve_once_known_d(A: int, x: int, sd: int) -> int | None:
    inv2 = (P25 + 1) // 2
    for root_d in (sd % P25, (-sd) % P25):
        u = (2 * x + 2 * root_d) % P25
        w = (u * u - 4) % P25
        sw = sqrt_mod(w)
        if sw is None:
            continue
        for candidate in ((u + sw) * inv2 % P25, (u - sw) * inv2 % P25):
            if candidate:
                doubled = affine_double(A, candidate)
                if doubled == x:
                    return candidate
    return None


def compute_x32_from_z(A: int, y: int, x: int, xP16: int, z: int) -> int | None:
    den = 2 * (x - y) % P25 * pow((y - 1) % P25, 2, P25) % P25
    inv_den = inv_mod(den)
    if inv_den is None:
        return None
    sd = y * z % P25 * inv_den % P25
    d = (xP16 * xP16 + A * xP16 + 1) % P25
    if sd * sd % P25 != d:
        return None
    return halve_once_known_d(A, xP16, sd)


def pp_verify(A: int, x0: int) -> bool:
    if P25 < 5 or P25 % 2 == 0:
        return False
    q = isqrt(P25)
    k = (q + 1 + isqrt(4 * q)).bit_length()
    if gcd(A * A - 4, P25) != 1:
        return False
    x_coord, z_coord = x0 % P25, 1
    z_prev = None
    inv4 = (P25 + 1) // 4 if P25 % 4 == 3 else (3 * P25 + 1) // 4
    c_value = (A + 2) * inv4 % P25
    for _ in range(k):
        z_prev = z_coord
        u_value = (x_coord + z_coord) * (x_coord + z_coord) % P25
        v_value = (x_coord - z_coord) * (x_coord - z_coord) % P25
        w_value = (u_value - v_value) % P25
        x_coord = u_value * v_value % P25
        z_coord = w_value * (v_value + c_value * w_value) % P25
    return z_coord % P25 == 0 and gcd(z_prev, P25) == 1


def audit_payload(claim: X16ChartPayloadClaim) -> X16ChartPayloadAudit:
    y = modp(claim.y) if claim.y is not None else None
    x = modp(claim.x) if claim.x is not None else None
    A_arg = modp(claim.A) if claim.A is not None else None
    xP_arg = modp(claim.xP16) if claim.xP16 is not None else None
    z = modp(claim.z) if claim.z is not None else None
    x32_arg = modp(claim.x32) if claim.x32 is not None else None
    x0 = modp(claim.x0) if claim.x0 is not None else None

    y_ok = y is not None and y_denominators_ok(y)
    discr_square = y is not None and y_ok and sqrt_mod(model_discriminant(y)) is not None
    root_ok = y is not None and x is not None and y_ok and model_equation_ok(y, x)
    nonsplit_ok = y is not None and y_ok and nonsplit_filter_ok(y)
    computed_A, computed_xP = (None, None)
    if y is not None and x is not None and root_ok:
        computed_A, computed_xP = compute_A_xP16(y, x)
    A_matches = computed_A is not None and (A_arg is None or A_arg == computed_A)
    xP_matches = computed_xP is not None and (xP_arg is None or xP_arg == computed_xP)
    direct_surface = (
        A_arg is not None
        and xP_arg is not None
        and gcd(A_arg * A_arg - 4, P25) == 1
        and 2 < A_arg < P25 - 2
    )
    first_value = first_half_value(y) if y is not None and y_ok else 0
    first_square = first_value != 0 and legendre(first_value) == 1
    z_matches = z is not None and first_square and z * z % P25 == first_value
    x32 = None
    if z_matches and computed_A is not None and computed_xP is not None and y is not None and x is not None:
        x32 = compute_x32_from_z(computed_A, y, x, computed_xP, z)
    x32_matches = x32 is not None and (x32_arg is None or x32_arg == x32)
    vpp_executed = claim.run_vpp and A_arg is not None and x0 is not None
    vpp_result = pp_verify(A_arg, x0) if vpp_executed else False
    return X16ChartPayloadAudit(
        has_y=y is not None,
        has_x=x is not None,
        has_A=A_arg is not None,
        has_xP16=xP_arg is not None,
        has_z=z is not None,
        has_x32=x32_arg is not None,
        has_x0=x0 is not None,
        y_denominators_ok=y_ok,
        model_discriminant_square=discr_square,
        model_root_ok=root_ok,
        nonsplit_filter_ok=nonsplit_ok,
        computed_A=computed_A,
        computed_xP16=computed_xP,
        A_matches=A_matches,
        xP16_matches=xP_matches,
        direct_A_xP16_surface_ok=direct_surface,
        optional_first_half_square=first_square,
        z_matches_first_half=z_matches,
        computed_x32=x32,
        x32_matches=x32_matches,
        vpp_executed=vpp_executed,
        vpp_result=vpp_result,
    )


def decision_from_audit(claim: X16ChartPayloadClaim) -> X16ChartPayloadDecision:
    audit = audit_payload(claim)

    if audit.vpp_executed:
        if audit.vpp_result:
            return X16ChartPayloadDecision(
                claim,
                audit,
                "submission_ready",
                True,
                audit.computed_x32 is not None,
                True,
                True,
                "none",
                "archive official vpp output, command, environment, and certificate",
                True,
            )
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_vpp_failed",
            False,
            False,
            False,
            False,
            "official vpp.py rejected the supplied A,x0",
            "do not treat this payload as extraction-ready",
            True,
        )

    if audit.has_A and audit.has_x0:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "extraction_ready_vpp_missing",
            audit.direct_A_xP16_surface_ok or audit.computed_A is not None,
            audit.computed_x32 is not None,
            True,
            False,
            "official vpp.py verification",
            "run official vpp.py on the concrete p25 A,x0 pair",
            True,
        )

    if not audit.has_y:
        if audit.direct_A_xP16_surface_ok:
            return X16ChartPayloadDecision(
                claim,
                audit,
                "active_surface_reached_halving_missing",
                True,
                False,
                False,
                False,
                "halve chain from xP16 at depth 4 to x0",
                "derive the 38-step halving chain or direct x0",
                True,
            )
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_no_chart_payload",
            False,
            False,
            False,
            False,
            "X_1(16) y/x or direct A,xP16 payload",
            "supply chart data before X_1(16) routing",
            True,
        )

    if not audit.y_denominators_ok:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_bad_y_denominators",
            False,
            False,
            False,
            False,
            "y denominator or y^2-2y vanished",
            "supply a nonsingular X_1(16) y parameter",
            True,
        )

    if not audit.model_discriminant_square:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_model_discriminant_nonsquare",
            False,
            False,
            False,
            False,
            "model quadratic has no F_p root",
            "supply a y whose X_1(16) model root lies in F_p",
            True,
        )

    if not audit.has_x:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "y_chart_missing_model_root",
            False,
            False,
            False,
            False,
            "model root x satisfying the X_1(16) quadratic",
            "supply x, or direct A,xP16",
            True,
        )

    if not audit.model_root_ok:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_model_root_equation",
            False,
            False,
            False,
            False,
            "x does not satisfy the X_1(16) model quadratic",
            "recompute x from the y discriminant",
            True,
        )

    if not audit.nonsplit_filter_ok:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_split_x16_filter",
            False,
            False,
            False,
            False,
            "production nonsplit filter is not satisfied",
            "use an X_1(16) y in the x16halvenonsplit class",
            True,
        )

    if not audit.A_matches or not audit.xP16_matches:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_A_or_xP16_mismatch",
            False,
            False,
            False,
            False,
            "supplied A or xP16 does not match the y/x chart formula",
            "replace A,xP16 with the recomputed chart values",
            True,
        )

    if audit.has_z and (not audit.z_matches_first_half or not audit.x32_matches):
        return X16ChartPayloadDecision(
            claim,
            audit,
            "reject_optional_first_half_payload",
            True,
            False,
            False,
            False,
            "z or x32 does not match the optional first-half d-gate",
            "drop the optional d-gate claim or supply matching z/x32",
            True,
        )

    if not claim.has_h0_order8112_bridge:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "conditional_chart_payload_without_order8112_bridge",
            True,
            audit.computed_x32 is not None,
            False,
            False,
            "same-j H0/order-8112 bridge provenance",
            "route this chart payload back through the H0 X1(8112) bridge intake",
            True,
        )

    if audit.computed_x32 is not None:
        return X16ChartPayloadDecision(
            claim,
            audit,
            "optional_depth5_surface_reached_halving_missing",
            True,
            True,
            False,
            False,
            "halve chain from x32 at depth 5 to x0",
            "derive the 37-step optional d-gate halving chain or direct x0",
            True,
        )

    return X16ChartPayloadDecision(
        claim,
        audit,
        "active_surface_reached_halving_missing",
        True,
        False,
        False,
        False,
        "halve chain from xP16 at depth 4 to x0",
        "derive the 38-step active halving chain or direct x0",
        True,
    )


def base_claim(name: str, **overrides: object) -> X16ChartPayloadClaim:
    values = {
        "has_h0_order8112_bridge": True,
        "y": None,
        "x": None,
        "A": None,
        "xP16": None,
        "z": None,
        "x32": None,
        "x0": None,
        "run_vpp": False,
    }
    values.update(overrides)
    return X16ChartPayloadClaim(name=name, **values)


def regression_claims() -> tuple[X16ChartPayloadClaim, ...]:
    return (
        base_claim("no_chart_payload"),
        base_claim("valid_y_only", y=SAMPLE_Y),
        base_claim(
            "valid_y_x_without_bridge",
            has_h0_order8112_bridge=False,
            y=SAMPLE_Y,
            x=SAMPLE_X,
        ),
        base_claim("valid_y_x_active_surface", y=SAMPLE_Y, x=SAMPLE_X),
        base_claim(
            "valid_y_x_bad_A",
            y=SAMPLE_Y,
            x=SAMPLE_X,
            A=SAMPLE_A + 1,
            xP16=SAMPLE_XP16,
        ),
        base_claim(
            "valid_y_x_optional_dgate",
            y=SAMPLE_Y,
            x=SAMPLE_X,
            A=SAMPLE_A,
            xP16=SAMPLE_XP16,
            z=SAMPLE_Z,
            x32=SAMPLE_X32,
        ),
        base_claim("direct_A_xP16_surface", A=SAMPLE_A, xP16=SAMPLE_XP16),
        base_claim("direct_A_x0_no_vpp", A=SAMPLE_A, x0=42),
        base_claim("direct_A_x0_vpp_fails", A=SAMPLE_A, x0=42, run_vpp=True),
    )


def profile_x16_chart_payload_intake() -> X16ChartPayloadIntakeProfile:
    chart = profile_h0_order8112_x16_chart_specialization()
    rows = tuple(decision_from_audit(claim) for claim in regression_claims())
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    bridge_missing = sum(row.decision == "conditional_chart_payload_without_order8112_bridge" for row in rows)
    y_only = sum(row.decision == "y_chart_missing_model_root" for row in rows)
    x16_surface = sum(row.x16_surface_reached for row in rows)
    optional_dgate = sum(row.optional_dgate_surface_reached for row in rows)
    extraction_ready = sum(row.extraction_ready for row in rows)
    vpp_executed = sum(row.audit.vpp_executed for row in rows)
    submission_ready = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "reject_no_chart_payload",
        "y_chart_missing_model_root",
        "conditional_chart_payload_without_order8112_bridge",
        "active_surface_reached_halving_missing",
        "reject_A_or_xP16_mismatch",
        "optional_depth5_surface_reached_halving_missing",
        "active_surface_reached_halving_missing",
        "extraction_ready_vpp_missing",
        "reject_vpp_failed",
    )
    row_ok = (
        chart.row_ok
        and P25 == 10**25 + 13
        and P25 % 8 == 5
        and ACTIVE_MODE == "x16halvenonsplit"
        and OPTIONAL_DGATE_MODE == "x16halvenonsplitdgate"
        and len(rows) == 9
        and rejected == 3
        and bridge_missing == 1
        and y_only == 1
        and x16_surface == 4
        and optional_dgate == 1
        and extraction_ready == 1
        and vpp_executed == 1
        and submission_ready == 0
        and decisions == expected_decisions
        and all(row.ok for row in rows)
        and rows[3].audit.computed_A == SAMPLE_A
        and rows[3].audit.computed_xP16 == SAMPLE_XP16
        and rows[5].audit.computed_x32 == SAMPLE_X32
    )
    q = isqrt(P25)
    k = (q + 1 + isqrt(4 * q)).bit_length()
    return X16ChartPayloadIntakeProfile(
        chart_specialization_ok=chart.row_ok,
        p=P25,
        k=k,
        active_mode=ACTIVE_MODE,
        optional_dgate_mode=OPTIONAL_DGATE_MODE,
        regression_rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        bridge_missing_rows=bridge_missing,
        y_only_rows=y_only,
        x16_surface_rows=x16_surface,
        optional_dgate_rows=optional_dgate,
        extraction_ready_rows=extraction_ready,
        vpp_executed_rows=vpp_executed,
        submission_ready_rows=submission_ready,
        row_ok=row_ok,
    )


def claim_from_args(args: argparse.Namespace) -> X16ChartPayloadClaim:
    return X16ChartPayloadClaim(
        name=args.name,
        has_h0_order8112_bridge=args.h0_order8112_bridge,
        y=args.y,
        x=args.x,
        A=args.A,
        xP16=args.xP16,
        z=args.z,
        x32=args.x32,
        x0=args.x0,
        run_vpp=args.run_vpp,
    )


def print_decision(row: X16ChartPayloadDecision) -> None:
    audit = row.audit
    print(
        "  "
        f"{row.claim.name}: bridge={int(row.claim.has_h0_order8112_bridge)} "
        f"y={int(audit.has_y)} x={int(audit.has_x)} "
        f"A={int(audit.has_A)} xP16={int(audit.has_xP16)} "
        f"z={int(audit.has_z)} x32={int(audit.has_x32)} x0={int(audit.has_x0)} "
        f"denoms={int(audit.y_denominators_ok)} discr={int(audit.model_discriminant_square)} "
        f"root={int(audit.model_root_ok)} nonsplit={int(audit.nonsplit_filter_ok)} "
        f"A_match={int(audit.A_matches)} xP_match={int(audit.xP16_matches)} "
        f"dgate={int(row.optional_dgate_surface_reached)} "
        f"vpp_run={int(audit.vpp_executed)} vpp={int(audit.vpp_result)} "
        f"decision={row.decision} missing={row.first_missing_or_falsifier}"
    )
    if audit.computed_A is not None or audit.computed_xP16 is not None or audit.computed_x32 is not None:
        print(
            "    "
            f"computed_A={audit.computed_A} "
            f"computed_xP16={audit.computed_xP16} "
            f"computed_x32={audit.computed_x32}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="x16_chart_payload")
    parser.add_argument("--h0-order8112-bridge", action="store_true")
    parser.add_argument("--y", type=int)
    parser.add_argument("--x", type=int)
    parser.add_argument("--A", type=int)
    parser.add_argument("--xP16", type=int)
    parser.add_argument("--z", type=int)
    parser.add_argument("--x32", type=int)
    parser.add_argument("--x0", type=int)
    parser.add_argument("--run-vpp", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        row = decision_from_audit(claim_from_args(args))
        print("p25 KSY-y H0 X1(16) chart-payload intake candidate")
        print_decision(row)
        print(f"next_action={row.next_action}")
        print(f"ksy_y_h0_x16_chart_payload_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_x16_chart_payload_intake()
    print("p25 KSY-y H0 X1(16) chart-payload intake gate")
    print("production")
    print(f"  chart_specialization_ok={int(profile.chart_specialization_ok)}")
    print(f"  p={profile.p}")
    print(f"  k={profile.k}")
    print(f"  active_mode={profile.active_mode}")
    print(f"  optional_dgate_mode={profile.optional_dgate_mode}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  bridge_missing_rows={profile.bridge_missing_rows}")
    print(f"  y_only_rows={profile.y_only_rows}")
    print(f"  x16_surface_rows={profile.x16_surface_rows}")
    print(f"  optional_dgate_rows={profile.optional_dgate_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  vpp_executed_rows={profile.vpp_executed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  y_x_payloads_are_checked_against_the_production_X1_16_chart=1")
    print("  valid_chart_payload_without_H0_order8112_bridge_is_not_extraction_progress=1")
    print("  direct_A_x0_requires_official_vpp_before_submission=1")
    print(f"ksy_y_h0_x16_chart_payload_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 X1(16) chart-payload intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
