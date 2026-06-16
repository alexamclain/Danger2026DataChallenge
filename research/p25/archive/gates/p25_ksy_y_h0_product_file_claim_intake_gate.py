#!/usr/bin/env python3
"""File-based intake for exact p25 H0 product theorem claims.

The fixture exporter writes the four exact legal H0 products as stable files.
This gate is the inverse front door: given a product file, parse it, identify
whether it is one of those four targets, and then route the claimed theorem
shape through the H0 source-theorem matcher.

It accepts canonical content even if line order differs, but it separately
records whether the raw file hash is byte-identical to the exported fixture.
"""

from __future__ import annotations

import argparse
import tempfile
from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from p25_ksy_y_h0_exact_product_fixture_export import (
    FIXTURE_DIR,
    export_fixtures,
    fixture_name,
    lifted_product_lines,
)
from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    H0SourceTheoremCandidate,
    H0SourceTheoremDecision,
    classify_candidate,
    profile_h0_source_theorem_candidate_matcher,
)
from p25_ksy_y_h0_translate_exact_product_query_packet_gate import (
    H0ExactProductQueryRow,
    profile_h0_translate_exact_product_query_packet,
)


QUOTIENT_LEVEL = 507


ProductEntries = tuple[tuple[int, int], ...]


@dataclass(frozen=True)
class ProductFileAudit:
    path: str
    parsed_ok: bool
    parse_error: str
    line_count: int
    support: int
    coefficient_counts: tuple[tuple[int, int], ...]
    raw_sha256: str
    canonical_sha256: str
    matched_multiplier: int | None
    matched_fixture_name: str
    canonical_product_match: bool
    raw_hash_matches_fixture: bool


@dataclass(frozen=True)
class ProductFileClaim:
    name: str
    product_file: Path
    theorem_body_verified: bool
    arithmetic_source_theorem: bool
    output_kind: str
    period156_context: bool
    h90_boundary: bool
    danger3_framing: bool
    same_j_x18112_bridge: bool
    x16_surface: bool
    concrete_x0: bool
    official_vpp: bool


@dataclass(frozen=True)
class ProductFileDecision:
    claim: ProductFileClaim
    audit: ProductFileAudit
    matcher_decision: H0SourceTheoremDecision | None
    decision: str
    source_stage_closed: bool
    submission_ready: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class H0ProductFileClaimIntakeProfile:
    fixture_export_ok: bool
    exact_product_query_ok: bool
    candidate_matcher_ok: bool
    target_fixture_count: int
    regression_rows: tuple[ProductFileDecision, ...]
    row_count: int
    parsed_rows: int
    exact_product_rows: int
    raw_hash_match_rows: int
    source_closing_rows: int
    conditional_rows: int
    rejected_rows: int
    submission_ready_rows: int
    row_ok: bool


def canonical_text(entries: ProductEntries) -> str:
    return "".join(f"{residue} {coefficient}\n" for residue, coefficient in entries)


def expected_entries(row: H0ExactProductQueryRow) -> ProductEntries:
    entries: list[tuple[int, int]] = []
    for line in lifted_product_lines(row):
        residue, coefficient = (int(token) for token in line.split())
        entries.append((residue, coefficient))
    return tuple(sorted(entries))


def expected_fixture_text(row: H0ExactProductQueryRow) -> str:
    return "\n".join(lifted_product_lines(row)) + "\n"


def coefficient_counts(entries: ProductEntries) -> tuple[tuple[int, int], ...]:
    counts: dict[int, int] = {}
    for _residue, coefficient in entries:
        counts[coefficient] = counts.get(coefficient, 0) + 1
    return tuple(sorted(counts.items()))


def parse_product_file(path: Path) -> tuple[bool, str, ProductEntries, str, int]:
    try:
        text = path.read_text()
    except OSError as exc:
        return False, str(exc), (), "", 0

    values: dict[int, int] = {}
    logical_lines = 0
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        logical_lines += 1
        parts = stripped.split()
        if len(parts) != 2:
            return False, f"line {line_number}: expected residue coefficient", (), text, logical_lines
        try:
            residue, coefficient = (int(part) for part in parts)
        except ValueError:
            return False, f"line {line_number}: non-integer token", (), text, logical_lines
        if not 0 <= residue < QUOTIENT_LEVEL:
            return False, f"line {line_number}: residue outside 0..506", (), text, logical_lines
        values[residue] = values.get(residue, 0) + coefficient
        if values[residue] == 0:
            del values[residue]
    entries = tuple(sorted(values.items()))
    return True, "", entries, text, logical_lines


def audit_product_file(
    path: Path,
    target_rows: tuple[H0ExactProductQueryRow, ...],
) -> ProductFileAudit:
    parsed_ok, parse_error, entries, text, line_count = parse_product_file(path)
    raw_hash = sha256(text.encode()).hexdigest() if text else ""
    canonical_hash = sha256(canonical_text(entries).encode()).hexdigest() if parsed_ok else ""
    expected_by_entries = {expected_entries(row): row for row in target_rows}
    expected_hash_by_multiplier = {
        row.multiplier_from_canonical: sha256(expected_fixture_text(row).encode()).hexdigest()
        for row in target_rows
    }
    matched = expected_by_entries.get(entries) if parsed_ok else None
    matched_multiplier = matched.multiplier_from_canonical if matched else None
    matched_fixture = fixture_name(matched) if matched else ""
    raw_hash_matches = (
        matched_multiplier is not None
        and raw_hash == expected_hash_by_multiplier[matched_multiplier]
    )
    return ProductFileAudit(
        path=str(path),
        parsed_ok=parsed_ok,
        parse_error=parse_error,
        line_count=line_count,
        support=len(entries),
        coefficient_counts=coefficient_counts(entries),
        raw_sha256=raw_hash,
        canonical_sha256=canonical_hash,
        matched_multiplier=matched_multiplier,
        matched_fixture_name=matched_fixture,
        canonical_product_match=matched is not None,
        raw_hash_matches_fixture=raw_hash_matches,
    )


def decision_from_matcher(
    claim: ProductFileClaim,
    audit: ProductFileAudit,
) -> H0SourceTheoremDecision:
    return classify_candidate(
        H0SourceTheoremCandidate(
            name=claim.name,
            product_multiplier=audit.matched_multiplier,
            residue_sets_exact=audit.canonical_product_match,
            arithmetic_source_theorem=claim.arithmetic_source_theorem,
            output_kind=claim.output_kind,
            period156_context=claim.period156_context,
            h90_boundary=claim.h90_boundary,
            danger3_framing=claim.danger3_framing,
            same_j_x18112_bridge=claim.same_j_x18112_bridge,
            x16_surface=claim.x16_surface,
            concrete_x0=claim.concrete_x0,
            official_vpp=claim.official_vpp,
        )
    )


def classify_product_file_claim(
    claim: ProductFileClaim,
    target_rows: tuple[H0ExactProductQueryRow, ...],
) -> ProductFileDecision:
    audit = audit_product_file(claim.product_file, target_rows)
    if not audit.parsed_ok:
        return ProductFileDecision(
            claim=claim,
            audit=audit,
            matcher_decision=None,
            decision="reject_unparseable_product_file",
            source_stage_closed=False,
            submission_ready=False,
            first_missing_or_falsifier=audit.parse_error,
            next_action="supply a two-column residue/coefficient product file",
            ok=True,
        )
    if not audit.canonical_product_match:
        return ProductFileDecision(
            claim=claim,
            audit=audit,
            matcher_decision=None,
            decision="reject_product_file_not_exact_h0_fixture",
            source_stage_closed=False,
            submission_ready=False,
            first_missing_or_falsifier="one of the four exact legal H0 product fixtures",
            next_action="compare against h0_product_fixtures before theorem routing",
            ok=True,
        )
    if not claim.theorem_body_verified:
        return ProductFileDecision(
            claim=claim,
            audit=audit,
            matcher_decision=None,
            decision="reject_no_theorem_body",
            source_stage_closed=False,
            submission_ready=False,
            first_missing_or_falsifier="verified theorem statement or proof body",
            next_action="keep fixture match as target data only",
            ok=True,
        )

    matcher = decision_from_matcher(claim, audit)
    return ProductFileDecision(
        claim=claim,
        audit=audit,
        matcher_decision=matcher,
        decision=matcher.decision,
        source_stage_closed=matcher.source_stage_closed,
        submission_ready=matcher.submission_ready,
        first_missing_or_falsifier=matcher.first_missing_clause,
        next_action=matcher.next_action,
        ok=matcher.ok,
    )


def fixture_path(name: str) -> Path:
    return FIXTURE_DIR / name


def base_claim(name: str, path: Path, **overrides: object) -> ProductFileClaim:
    values = {
        "theorem_body_verified": True,
        "arithmetic_source_theorem": True,
        "output_kind": "source-certification",
        "period156_context": False,
        "h90_boundary": False,
        "danger3_framing": False,
        "same_j_x18112_bridge": False,
        "x16_surface": False,
        "concrete_x0": False,
        "official_vpp": False,
    }
    values.update(overrides)
    return ProductFileClaim(name=name, product_file=path, **values)


def wrong_product_control_path(target_rows: tuple[H0ExactProductQueryRow, ...]) -> Path:
    row = target_rows[0]
    entries = list(expected_entries(row))
    residue, coefficient = entries[0]
    entries[0] = (residue, -coefficient)
    tmp = tempfile.NamedTemporaryFile("w", prefix="h0_wrong_product_", suffix=".txt", delete=False)
    with tmp:
        tmp.write(canonical_text(tuple(entries)))
    return Path(tmp.name)


def regression_claims(
    target_rows: tuple[H0ExactProductQueryRow, ...],
) -> tuple[ProductFileClaim, ...]:
    wrong_path = wrong_product_control_path(target_rows)
    return (
        base_claim("m1_source_certification_only", fixture_path("h0_m1_canonical_lifted_product.txt")),
        base_claim(
            "m2_value_period156_no_framing",
            fixture_path("h0_m2_translate_lifted_product.txt"),
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
        ),
        base_claim(
            "m4_divisor_h90_no_framing",
            fixture_path("h0_m4_translate_lifted_product.txt"),
            output_kind="divisor-additive",
            h90_boundary=True,
        ),
        base_claim(
            "m8_submission_ready_control",
            fixture_path("h0_m8_translate_lifted_product.txt"),
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
            danger3_framing=True,
            same_j_x18112_bridge=True,
            x16_surface=True,
            concrete_x0=True,
            official_vpp=True,
        ),
        base_claim(
            "m2_bare_value_missing_period156",
            fixture_path("h0_m2_translate_lifted_product.txt"),
            output_kind="value",
            h90_boundary=True,
        ),
        base_claim(
            "m4_divisor_missing_h90",
            fixture_path("h0_m4_translate_lifted_product.txt"),
            output_kind="divisor-additive",
        ),
        base_claim(
            "m1_payload_without_source",
            fixture_path("h0_m1_canonical_lifted_product.txt"),
            arithmetic_source_theorem=False,
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
        ),
        base_claim(
            "m1_exact_file_no_theorem_body",
            fixture_path("h0_m1_canonical_lifted_product.txt"),
            theorem_body_verified=False,
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
        ),
        base_claim("wrong_product_file", wrong_path, output_kind="value", period156_context=True),
        base_claim(
            "manifest_is_not_product_file",
            fixture_path("h0_exact_product_manifest.tsv"),
            output_kind="value",
            period156_context=True,
        ),
    )


def profile_h0_product_file_claim_intake() -> H0ProductFileClaimIntakeProfile:
    export = export_fixtures()
    query = profile_h0_translate_exact_product_query_packet()
    matcher = profile_h0_source_theorem_candidate_matcher()
    target_rows = query.exact_product_rows
    rows = tuple(
        classify_product_file_claim(claim, target_rows)
        for claim in regression_claims(target_rows)
    )
    parsed = sum(row.audit.parsed_ok for row in rows)
    exact = sum(row.audit.canonical_product_match for row in rows)
    raw_hash = sum(row.audit.raw_hash_matches_fixture for row in rows)
    source_closed = sum(row.source_stage_closed for row in rows)
    conditional = sum(row.decision.startswith("conditional_") for row in rows)
    rejected = sum(row.decision.startswith("reject_") for row in rows)
    submission = sum(row.submission_ready for row in rows)
    expected_decisions = (
        "source_certified_value_or_divisor_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "source_theorem_closed_policy_or_framing_missing",
        "submission_ready",
        "conditional_missing_period_156_context",
        "conditional_divisor_identity_missing_h90_boundary",
        "conditional_finite_payload_without_source_theorem",
        "reject_no_theorem_body",
        "reject_product_file_not_exact_h0_fixture",
        "reject_unparseable_product_file",
    )
    row_ok = (
        export.row_ok
        and query.row_ok
        and matcher.row_ok
        and len(target_rows) == 4
        and len(rows) == 10
        and parsed == 9
        and exact == 8
        and raw_hash == 8
        and source_closed == 3
        and conditional == 3
        and rejected == 3
        and submission == 1
        and tuple(row.decision for row in rows) == expected_decisions
        and all(row.ok for row in rows)
    )
    return H0ProductFileClaimIntakeProfile(
        fixture_export_ok=export.row_ok,
        exact_product_query_ok=query.row_ok,
        candidate_matcher_ok=matcher.row_ok,
        target_fixture_count=len(target_rows),
        regression_rows=rows,
        row_count=len(rows),
        parsed_rows=parsed,
        exact_product_rows=exact,
        raw_hash_match_rows=raw_hash,
        source_closing_rows=source_closed,
        conditional_rows=conditional,
        rejected_rows=rejected,
        submission_ready_rows=submission,
        row_ok=row_ok,
    )


def claim_from_args(args: argparse.Namespace) -> ProductFileClaim:
    return ProductFileClaim(
        name=args.name,
        product_file=Path(args.product_file),
        theorem_body_verified=args.theorem_body,
        arithmetic_source_theorem=args.source_theorem,
        output_kind=args.output_kind,
        period156_context=args.period_156,
        h90_boundary=args.h90_boundary,
        danger3_framing=args.danger3,
        same_j_x18112_bridge=args.same_j,
        x16_surface=args.x16,
        concrete_x0=args.x0,
        official_vpp=args.vpp,
    )


def print_decision(row: ProductFileDecision) -> None:
    print(
        "  "
        f"{row.claim.name}: file={row.audit.path} parsed={int(row.audit.parsed_ok)} "
        f"lines={row.audit.line_count} support={row.audit.support} "
        f"coeffs={row.audit.coefficient_counts} "
        f"match={int(row.audit.canonical_product_match)} "
        f"raw_hash={int(row.audit.raw_hash_matches_fixture)} "
        f"multiplier={row.audit.matched_multiplier} "
        f"fixture={row.audit.matched_fixture_name} "
        f"kind={row.claim.output_kind} source={int(row.claim.arithmetic_source_theorem)} "
        f"period156={int(row.claim.period156_context)} h90={int(row.claim.h90_boundary)} "
        f"decision={row.decision} closed={int(row.source_stage_closed)} "
        f"submission={int(row.submission_ready)} "
        f"missing={row.first_missing_or_falsifier}"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify H0 product files against exact fixtures.")
    parser.add_argument("--product-file")
    parser.add_argument("--name", default="cli_product_file_claim")
    parser.add_argument("--theorem-body", action="store_true")
    parser.add_argument("--source-theorem", action="store_true")
    parser.add_argument(
        "--output-kind",
        default="source-certification",
        choices=("source-certification", "value", "divisor-additive", "computed-payload", "other"),
    )
    parser.add_argument("--period-156", action="store_true")
    parser.add_argument("--h90-boundary", action="store_true")
    parser.add_argument("--danger3", action="store_true")
    parser.add_argument("--same-j", action="store_true")
    parser.add_argument("--x16", action="store_true")
    parser.add_argument("--x0", action="store_true")
    parser.add_argument("--vpp", action="store_true")
    args = parser.parse_args()

    print("p25 KSY-y H0 product-file claim intake gate")
    if args.product_file:
        query = profile_h0_translate_exact_product_query_packet()
        row = classify_product_file_claim(claim_from_args(args), query.exact_product_rows)
        print("candidate_decision")
        print_decision(row)
        print(f"ksy_y_h0_product_file_claim_intake_candidate_rows={int(row.ok)}/1")
        return 0 if row.ok else 1

    profile = profile_h0_product_file_claim_intake()
    print("dependencies")
    print(f"  fixture_export_ok={int(profile.fixture_export_ok)}")
    print(f"  exact_product_query_ok={int(profile.exact_product_query_ok)}")
    print(f"  candidate_matcher_ok={int(profile.candidate_matcher_ok)}")
    print(f"  target_fixture_count={profile.target_fixture_count}")
    print("regression_rows")
    for row in profile.regression_rows:
        print_decision(row)
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  parsed_rows={profile.parsed_rows}")
    print(f"  exact_product_rows={profile.exact_product_rows}")
    print(f"  raw_hash_match_rows={profile.raw_hash_match_rows}")
    print(f"  source_closing_rows={profile.source_closing_rows}")
    print(f"  conditional_rows={profile.conditional_rows}")
    print(f"  rejected_rows={profile.rejected_rows}")
    print(f"  submission_ready_rows={profile.submission_ready_rows}")
    print("interpretation")
    print("  exact_H0_product_files_now_have_a_file_based_intake=1")
    print("  byte_hash_match_is_recorded_but_canonical_content_match_routes_claims=1")
    print("  fixture_match_without_theorem_body_or_source_theorem_does_not_close=1")
    print("  source_closing_product_file_claims_still_route_to_DANGER3_extraction=1")
    print(f"ksy_y_h0_product_file_claim_intake_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("H0 product-file claim intake regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
