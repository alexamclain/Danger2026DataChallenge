#!/usr/bin/env python3
"""Numeric halving-chain intake for H0/X_1(16) extraction payloads.

After a chart payload reaches A,xP16, the active p25 route needs a concrete
x-coordinate chain

    x_4=xP16, x_5, ..., x_42=x0

where each x_{i+1} doubles back to x_i on the same Montgomery curve.  This
gate checks such chains over F_p and keeps official vpp.py verification as the
final submission boundary.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_h0_x16_chart_payload_intake_gate import (
    P25,
    SAMPLE_A,
    SAMPLE_X32,
    SAMPLE_XP16,
    affine_double,
    pp_verify,
)
from p25_ksy_y_x1_16_halving_certificate_payload_gate import (
    FINAL_DEPTH,
    HALVING_LINKS,
    START_DEPTH,
    X_CHAIN_POINTS,
    profile_halving_certificate_payload_contract,
)


ChainValues = tuple[int, ...]


@dataclass(frozen=True)
class HalvingChainPayloadClaim:
    name: str
    A: int | None
    xP16: int | None
    chain: ChainValues
    x0: int | None
    start_depth: int
    final_depth: int
    run_vpp: bool


@dataclass(frozen=True)
class HalvingChainAudit:
    has_A: bool
    has_xP16: bool
    has_chain: bool
    has_x0: bool
    chain_len: int
    expected_chain_len: int
    start_matches_xP16: bool
    links_checked: int
    links_ok: int
    first_bad_link_depth: int | None
    full_length_chain: bool
    tail_matches_x0: bool
    vpp_executed: bool
    vpp_result: bool


@dataclass(frozen=True)
class HalvingChainDecision:
    claim: HalvingChainPayloadClaim
    audit: HalvingChainAudit
    decision: str
    partial_chain_verified: bool
    extraction_ready: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class HalvingChainPayloadIntakeProfile:
    halving_certificate_contract_ok: bool
    p: int
    start_depth: int
    final_depth: int
    halving_links: int
    x_chain_points: int
    regression_rows: tuple[HalvingChainDecision, ...]
    row_count: int
    rejected_rows: int
    surface_missing_rows: int
    partial_chain_rows: int
    full_chain_rows: int
    direct_x0_rows: int
    extraction_ready_rows: int
    vpp_executed_rows: int
    submission_ready_rows: int
    row_ok: bool


def normalize(value: int) -> int:
    return value % P25


def check_chain_links(A: int, chain: ChainValues, start_depth: int) -> tuple[int, int, int | None]:
    checked = max(0, len(chain) - 1)
    ok = 0
    first_bad: int | None = None
    for offset, (parent, child) in enumerate(zip(chain, chain[1:])):
        doubled = affine_double(A, child)
        if doubled == parent:
            ok += 1
            continue
        first_bad = start_depth + offset
        break
    return checked, ok, first_bad


def audit_claim(claim: HalvingChainPayloadClaim) -> HalvingChainAudit:
    A = normalize(claim.A) if claim.A is not None else None
    xP16 = normalize(claim.xP16) if claim.xP16 is not None else None
    x0 = normalize(claim.x0) if claim.x0 is not None else None
    chain = tuple(normalize(value) for value in claim.chain)
    expected_len = claim.final_depth - claim.start_depth + 1
    start_matches = bool(chain and xP16 is not None and chain[0] == xP16)
    checked = ok = 0
    first_bad: int | None = None
    if A is not None and len(chain) >= 2:
        checked, ok, first_bad = check_chain_links(A, chain, claim.start_depth)
    full_length = len(chain) == expected_len
    tail_matches = bool(chain and x0 is not None and chain[-1] == x0)
    vpp_executed = claim.run_vpp and A is not None and x0 is not None
    vpp_result = pp_verify(A, x0) if vpp_executed else False
    return HalvingChainAudit(
        has_A=A is not None,
        has_xP16=xP16 is not None,
        has_chain=bool(chain),
        has_x0=x0 is not None,
        chain_len=len(chain),
        expected_chain_len=expected_len,
        start_matches_xP16=start_matches,
        links_checked=checked,
        links_ok=ok,
        first_bad_link_depth=first_bad,
        full_length_chain=full_length,
        tail_matches_x0=tail_matches,
        vpp_executed=vpp_executed,
        vpp_result=vpp_result,
    )


def classify_claim(claim: HalvingChainPayloadClaim) -> HalvingChainDecision:
    audit = audit_claim(claim)

    if audit.vpp_executed:
        if audit.vpp_result:
            return HalvingChainDecision(
                claim,
                audit,
                "submission_ready",
                audit.links_checked > 0 and audit.links_checked == audit.links_ok,
                True,
                True,
                "none",
                "archive official vpp output, command, environment, and certificate",
                True,
            )
        return HalvingChainDecision(
            claim,
            audit,
            "reject_vpp_failed",
            False,
            False,
            False,
            "official vpp.py rejected the supplied A,x0",
            "do not treat this payload as extraction-ready",
            True,
        )

    if not audit.has_A:
        return HalvingChainDecision(
            claim,
            audit,
            "reject_missing_A",
            False,
            False,
            False,
            "Montgomery A",
            "supply A before checking halving links",
            True,
        )

    if audit.has_x0 and not audit.has_chain:
        return HalvingChainDecision(
            claim,
            audit,
            "direct_x0_vpp_missing",
            False,
            True,
            False,
            "official vpp.py verification",
            "run official vpp.py on the concrete p25 A,x0 pair",
            True,
        )

    if not audit.has_chain:
        return HalvingChainDecision(
            claim,
            audit,
            "surface_reached_certificate_missing",
            False,
            False,
            False,
            "x-chain, sqrt-witness chain, direct x0, or vpp-verified triple",
            "supply x_4=xP16 through x_42=x0 or a direct x0",
            True,
        )

    if not audit.has_xP16:
        return HalvingChainDecision(
            claim,
            audit,
            "conditional_chain_without_xP16_start",
            False,
            False,
            False,
            "xP16 start value for x_4",
            "attach the chart surface start xP16 before accepting the chain",
            True,
        )

    if not audit.start_matches_xP16:
        return HalvingChainDecision(
            claim,
            audit,
            "reject_chain_start_mismatch",
            False,
            False,
            False,
            "chain first value must equal xP16",
            "replace x_4 with the verified chart xP16",
            True,
        )

    if audit.chain_len < 2:
        return HalvingChainDecision(
            claim,
            audit,
            "reject_chain_too_short",
            False,
            False,
            False,
            "at least one xDBL link",
            "supply x_5 or a direct x0",
            True,
        )

    if audit.links_ok != audit.links_checked:
        return HalvingChainDecision(
            claim,
            audit,
            "reject_chain_link_mismatch",
            False,
            False,
            False,
            f"xDBL link at depth {audit.first_bad_link_depth} failed",
            "repair the first failing child coordinate",
            True,
        )

    if audit.has_x0 and not audit.tail_matches_x0:
        return HalvingChainDecision(
            claim,
            audit,
            "reject_x0_tail_mismatch",
            True,
            False,
            False,
            "x0 must equal the final chain value",
            "make x0 equal x_42 or omit x0",
            True,
        )

    if not audit.full_length_chain:
        return HalvingChainDecision(
            claim,
            audit,
            "partial_x_chain_verified_not_extraction",
            True,
            False,
            False,
            "full 39-point chain x_4 through x_42",
            "extend the verified prefix to depth 42 or supply direct x0",
            True,
        )

    return HalvingChainDecision(
        claim,
        audit,
        "checkable_x_chain_vpp_missing",
        True,
        True,
        False,
        "official vpp.py verification",
        "run official vpp.py on A and x_42",
        True,
    )


def parse_chain_file(path: Path, start_depth: int) -> ChainValues:
    values: list[int] = []
    for line_number, line in enumerate(path.read_text().splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.split()
        if len(parts) == 1:
            values.append(int(parts[0]))
            continue
        if len(parts) == 2:
            depth = int(parts[0])
            expected_depth = start_depth + len(values)
            if depth != expected_depth:
                raise ValueError(
                    f"line {line_number}: expected depth {expected_depth}, got {depth}"
                )
            values.append(int(parts[1]))
            continue
        raise ValueError(f"line {line_number}: expected value or depth value")
    return tuple(values)


def base_claim(name: str, **overrides: object) -> HalvingChainPayloadClaim:
    values = {
        "A": SAMPLE_A,
        "xP16": SAMPLE_XP16,
        "chain": (),
        "x0": None,
        "start_depth": START_DEPTH,
        "final_depth": FINAL_DEPTH,
        "run_vpp": False,
    }
    values.update(overrides)
    return HalvingChainPayloadClaim(name=name, **values)


def regression_claims() -> tuple[HalvingChainPayloadClaim, ...]:
    return (
        base_claim("surface_only"),
        base_claim("one_link_verified_prefix", chain=(SAMPLE_XP16, SAMPLE_X32)),
        base_claim("chain_without_xP16", xP16=None, chain=(SAMPLE_XP16, SAMPLE_X32)),
        base_claim("chain_start_mismatch", chain=(SAMPLE_X32, SAMPLE_XP16)),
        base_claim("chain_link_mismatch", chain=(SAMPLE_XP16, SAMPLE_X32 + 1)),
        base_claim("chain_x0_tail_mismatch", chain=(SAMPLE_XP16, SAMPLE_X32), x0=42),
        base_claim("direct_A_x0_no_vpp", xP16=None, x0=42),
        base_claim("direct_A_x0_vpp_fails", xP16=None, x0=42, run_vpp=True),
        base_claim("missing_A", A=None, chain=(SAMPLE_XP16, SAMPLE_X32)),
    )


def profile_halving_chain_payload_intake() -> HalvingChainPayloadIntakeProfile:
    contract = profile_halving_certificate_payload_contract()
    rows = tuple(classify_claim(claim) for claim in regression_claims())
    decisions = tuple(row.decision for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    surface_missing = sum(row.decision == "surface_reached_certificate_missing" for row in rows)
    partial = sum(row.decision == "partial_x_chain_verified_not_extraction" for row in rows)
    full = sum(row.decision == "checkable_x_chain_vpp_missing" for row in rows)
    direct = sum(row.decision == "direct_x0_vpp_missing" for row in rows)
    extraction = sum(row.extraction_ready for row in rows)
    vpp_executed = sum(row.audit.vpp_executed for row in rows)
    submission = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "surface_reached_certificate_missing",
        "partial_x_chain_verified_not_extraction",
        "conditional_chain_without_xP16_start",
        "reject_chain_start_mismatch",
        "reject_chain_link_mismatch",
        "reject_x0_tail_mismatch",
        "direct_x0_vpp_missing",
        "reject_vpp_failed",
        "reject_missing_A",
    )
    row_ok = (
        contract.row_ok
        and P25 == 10**25 + 13
        and START_DEPTH == 4
        and FINAL_DEPTH == 42
        and HALVING_LINKS == 38
        and X_CHAIN_POINTS == 39
        and len(rows) == 9
        and rejected == 5
        and surface_missing == 1
        and partial == 1
        and full == 0
        and direct == 1
        and extraction == 1
        and vpp_executed == 1
        and submission == 0
        and decisions == expected_decisions
        and rows[1].audit.links_checked == 1
        and rows[1].audit.links_ok == 1
        and all(row.ok for row in rows)
    )
    return HalvingChainPayloadIntakeProfile(
        halving_certificate_contract_ok=contract.row_ok,
        p=P25,
        start_depth=START_DEPTH,
        final_depth=FINAL_DEPTH,
        halving_links=HALVING_LINKS,
        x_chain_points=X_CHAIN_POINTS,
        regression_rows=rows,
        row_count=len(rows),
        rejected_rows=rejected,
        surface_missing_rows=surface_missing,
        partial_chain_rows=partial,
        full_chain_rows=full,
        direct_x0_rows=direct,
        extraction_ready_rows=extraction,
        vpp_executed_rows=vpp_executed,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def claim_from_args(args: argparse.Namespace) -> HalvingChainPayloadClaim:
    chain: ChainValues = ()
    if args.chain_file:
        chain = parse_chain_file(Path(args.chain_file), args.start_depth)
    elif args.chain:
        chain = tuple(int(value) for value in args.chain)
    return HalvingChainPayloadClaim(
        name=args.name,
        A=args.A,
        xP16=args.xP16,
        chain=chain,
        x0=args.x0,
        start_depth=args.start_depth,
        final_depth=args.final_depth,
        run_vpp=args.run_vpp,
    )


def print_decision(row: HalvingChainDecision) -> None:
    audit = row.audit
    print(
        "  "
        f"{row.claim.name}: A={int(audit.has_A)} xP16={int(audit.has_xP16)} "
        f"chain={int(audit.has_chain)} len={audit.chain_len}/{audit.expected_chain_len} "
        f"start={int(audit.start_matches_xP16)} "
        f"links={audit.links_ok}/{audit.links_checked} "
        f"full={int(audit.full_length_chain)} x0={int(audit.has_x0)} "
        f"tail={int(audit.tail_matches_x0)} "
        f"vpp_run={int(audit.vpp_executed)} vpp={int(audit.vpp_result)} "
        f"decision={row.decision} missing={row.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", action="store_true")
    parser.add_argument("--name", default="halving_chain_payload")
    parser.add_argument("--A", type=int)
    parser.add_argument("--xP16", type=int)
    parser.add_argument("--chain", type=int, nargs="*")
    parser.add_argument("--chain-file")
    parser.add_argument("--x0", type=int)
    parser.add_argument("--start-depth", type=int, default=START_DEPTH)
    parser.add_argument("--final-depth", type=int, default=FINAL_DEPTH)
    parser.add_argument("--run-vpp", action="store_true")
    args = parser.parse_args()

    if args.candidate:
        row = classify_claim(claim_from_args(args))
        print("p25 KSY-y H0 X1(16) halving-chain payload intake candidate")
        print_decision(row)
        print(f"next_action={row.next_action}")
        print(f"ksy_y_h0_x16_halving_chain_payload_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_halving_chain_payload_intake()
    print("p25 KSY-y H0 X1(16) halving-chain payload intake gate")
    print("shape")
    print(f"  halving_certificate_contract_ok={int(profile.halving_certificate_contract_ok)}")
    print(f"  p={profile.p}")
    print(f"  start_depth={profile.start_depth}")
    print(f"  final_depth={profile.final_depth}")
    print(f"  halving_links={profile.halving_links}")
    print(f"  x_chain_points={profile.x_chain_points}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  surface_missing_rows={profile.surface_missing_rows}")
    print(f"  partial_chain_rows={profile.partial_chain_rows}")
    print(f"  full_chain_rows={profile.full_chain_rows}")
    print(f"  direct_x0_rows={profile.direct_x0_rows}")
    print(f"  extraction_ready_rows={profile.extraction_ready_rows}")
    print(f"  vpp_executed_rows={profile.vpp_executed_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  x_chain_links_are_checked_by_montgomery_xDBL=1")
    print("  verified_prefix_is_progress_but_not_extraction_ready=1")
    print("  full_x4_to_x42_chain_or_direct_x0_still_requires_official_vpp=1")
    print(f"ksy_y_h0_x16_halving_chain_payload_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 X1(16) halving-chain payload intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
