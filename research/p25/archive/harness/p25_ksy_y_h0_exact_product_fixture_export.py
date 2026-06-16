#!/usr/bin/env python3
"""Export stable fixtures for the four exact p25 H0 products.

The H0 theorem hunt now has a small finite target family: four legal
78-over-78 Yang-fiber products in one conductor-39 doubling orbit.  This
exporter writes those targets as byte-stable text fixtures and verifies that
the H0 source-theorem candidate matcher accepts the corresponding value and
divisor answer shapes while rejecting a wrong product.

These fixtures are matching targets for future paper snippets, expert answers,
or subagent reports.  They are not arithmetic source theorems by themselves.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path

from p25_ksy_y_h0_source_theorem_candidate_matcher_gate import (
    H0SourceTheoremCandidate,
    classify_candidate,
    profile_h0_source_theorem_candidate_matcher,
)
from p25_ksy_y_h0_translate_exact_product_query_packet_gate import (
    H0ExactProductQueryRow,
    profile_h0_translate_exact_product_query_packet,
)


FIXTURE_DIR = Path(__file__).with_name("h0_product_fixtures")


@dataclass(frozen=True)
class FixtureFile:
    name: str
    path: str
    line_count: int
    sha256: str


@dataclass(frozen=True)
class H0ExactProductFixtureExportProfile:
    fixture_dir: str
    written_files: tuple[FixtureFile, ...]
    exact_product_query_ok: bool
    candidate_matcher_ok: bool
    lifted_product_fixture_count: int
    manifest_row_count: int
    lifted_product_line_counts: tuple[int, ...]
    value_candidate_rows_ok: int
    divisor_candidate_rows_ok: int
    wrong_product_rejected: bool
    row_ok: bool


def tuple_text(values: tuple[int, ...]) -> str:
    return ",".join(str(value) for value in values)


def lifted_product_lines(row: H0ExactProductQueryRow) -> tuple[str, ...]:
    entries: list[tuple[int, int]] = []
    for residue in row.positive_residues_mod39:
        entries.extend((residue + 39 * k_value, 6) for k_value in range(13))
    for residue in row.negative_residues_mod39:
        entries.extend((residue + 39 * k_value, -6) for k_value in range(13))
    return tuple(f"{residue} {coefficient}" for residue, coefficient in sorted(entries))


def write_text(path: Path, text: str) -> FixtureFile:
    path.write_text(text)
    return FixtureFile(
        name=path.name,
        path=str(path),
        line_count=len(text.splitlines()),
        sha256=sha256(text.encode()).hexdigest(),
    )


def fixture_name(row: H0ExactProductQueryRow) -> str:
    target = "canonical" if row.multiplier_from_canonical == 1 else "translate"
    return f"h0_m{row.multiplier_from_canonical}_{target}_lifted_product.txt"


def manifest_text(rows: tuple[H0ExactProductQueryRow, ...]) -> str:
    header = "\t".join(
        (
            "multiplier",
            "target",
            "constants",
            "positive_mod39",
            "negative_mod39",
            "lifted_positive",
            "lifted_negative",
            "support",
            "boundary_norm156",
        )
    )
    lines = [header]
    for row in rows:
        lines.append(
            "\t".join(
                (
                    str(row.multiplier_from_canonical),
                    row.target_object,
                    tuple_text(row.source_constants),
                    tuple_text(row.positive_residues_mod39),
                    tuple_text(row.negative_residues_mod39),
                    str(row.lifted_positive_count),
                    str(row.lifted_negative_count),
                    str(row.lifted_support),
                    str(int(row.boundary_equals_norm156_y507)),
                )
            )
        )
    return "\n".join(lines) + "\n"


def commands_text(rows: tuple[H0ExactProductQueryRow, ...]) -> str:
    lines = [
        "# P25 H0 exact-product theorem matcher fixture commands",
        "",
    ]
    for row in rows:
        base = (
            "PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 "
            "research/p25/p25_ksy_y_h0_source_theorem_candidate_matcher_gate.py "
            f"--product-multiplier {row.multiplier_from_canonical} "
            "--residue-exact --source-theorem"
        )
        lines.append(f"{base} --output-kind value --period-156")
        lines.append(f"{base} --output-kind divisor-additive --h90-boundary")
        lines.append("")
    return "\n".join(lines)


def value_candidate_ok(row: H0ExactProductQueryRow) -> bool:
    decision = classify_candidate(
        H0SourceTheoremCandidate(
            name=f"value_m{row.multiplier_from_canonical}",
            product_multiplier=row.multiplier_from_canonical,
            residue_sets_exact=True,
            arithmetic_source_theorem=True,
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
            danger3_framing=False,
            same_j_x18112_bridge=False,
            x16_surface=False,
            concrete_x0=False,
            official_vpp=False,
        )
    )
    return (
        decision.legal_h0_product
        and decision.source_stage_closed
        and decision.decision == "source_theorem_closed_policy_or_framing_missing"
    )


def divisor_candidate_ok(row: H0ExactProductQueryRow) -> bool:
    decision = classify_candidate(
        H0SourceTheoremCandidate(
            name=f"divisor_m{row.multiplier_from_canonical}",
            product_multiplier=row.multiplier_from_canonical,
            residue_sets_exact=True,
            arithmetic_source_theorem=True,
            output_kind="divisor-additive",
            period156_context=False,
            h90_boundary=True,
            danger3_framing=False,
            same_j_x18112_bridge=False,
            x16_surface=False,
            concrete_x0=False,
            official_vpp=False,
        )
    )
    return (
        decision.legal_h0_product
        and decision.source_stage_closed
        and decision.decision == "source_theorem_closed_policy_or_framing_missing"
    )


def wrong_product_rejected() -> bool:
    decision = classify_candidate(
        H0SourceTheoremCandidate(
            name="wrong_product_fixture_control",
            product_multiplier=3,
            residue_sets_exact=True,
            arithmetic_source_theorem=True,
            output_kind="value",
            period156_context=True,
            h90_boundary=True,
            danger3_framing=False,
            same_j_x18112_bridge=False,
            x16_surface=False,
            concrete_x0=False,
            official_vpp=False,
        )
    )
    return (
        not decision.legal_h0_product
        and decision.decision == "reject_wrong_or_nonlegal_h0_product"
    )


def export_fixtures() -> H0ExactProductFixtureExportProfile:
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    query = profile_h0_translate_exact_product_query_packet()
    matcher = profile_h0_source_theorem_candidate_matcher()
    rows = query.exact_product_rows
    files: list[FixtureFile] = []

    for row in rows:
        text = "\n".join(lifted_product_lines(row)) + "\n"
        files.append(write_text(FIXTURE_DIR / fixture_name(row), text))

    files.append(write_text(FIXTURE_DIR / "h0_exact_product_manifest.tsv", manifest_text(rows)))
    files.append(write_text(FIXTURE_DIR / "h0_candidate_matcher_commands.sh", commands_text(rows)))

    value_ok = sum(value_candidate_ok(row) for row in rows)
    divisor_ok = sum(divisor_candidate_ok(row) for row in rows)
    wrong_rejected = wrong_product_rejected()
    lifted_line_counts = tuple(file.line_count for file in files[: len(rows)])
    manifest_rows = files[-2].line_count - 1
    row_ok = (
        query.row_ok
        and matcher.row_ok
        and len(rows) == 4
        and len(files) == 6
        and lifted_line_counts == (156, 156, 156, 156)
        and manifest_rows == 4
        and value_ok == 4
        and divisor_ok == 4
        and wrong_rejected
        and tuple(row.multiplier_from_canonical for row in rows) == (1, 2, 4, 8)
    )
    return H0ExactProductFixtureExportProfile(
        fixture_dir=str(FIXTURE_DIR),
        written_files=tuple(files),
        exact_product_query_ok=query.row_ok,
        candidate_matcher_ok=matcher.row_ok,
        lifted_product_fixture_count=len(rows),
        manifest_row_count=manifest_rows,
        lifted_product_line_counts=lifted_line_counts,
        value_candidate_rows_ok=value_ok,
        divisor_candidate_rows_ok=divisor_ok,
        wrong_product_rejected=wrong_rejected,
        row_ok=row_ok,
    )


def main() -> int:
    profile = export_fixtures()
    print("p25 KSY-y H0 exact-product fixture export")
    print(f"fixture_dir={profile.fixture_dir}")
    print("dependencies")
    print(f"  exact_product_query_ok={int(profile.exact_product_query_ok)}")
    print(f"  candidate_matcher_ok={int(profile.candidate_matcher_ok)}")
    print("written_files")
    for file in profile.written_files:
        print(
            "  "
            f"{file.name}: lines={file.line_count} sha256={file.sha256}"
        )
    print("checks")
    print(f"  lifted_product_fixture_count={profile.lifted_product_fixture_count}")
    print(f"  manifest_row_count={profile.manifest_row_count}")
    print(f"  lifted_product_line_counts={profile.lifted_product_line_counts}")
    print(f"  value_candidate_rows_ok={profile.value_candidate_rows_ok}")
    print(f"  divisor_candidate_rows_ok={profile.divisor_candidate_rows_ok}")
    print(f"  wrong_product_rejected={int(profile.wrong_product_rejected)}")
    print("interpretation")
    print("  future_H0_theorem_hits_can_be_compared_to_stable_product_files=1")
    print("  fixtures_are_exact_targets_not_arithmetic_source_theorems=1")
    print("  value_or_divisor_answer_still_needs_DANGER3_framing_and_extraction=1")
    print(f"ksy_y_h0_exact_product_fixture_export_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
