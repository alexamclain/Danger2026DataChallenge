#!/usr/bin/env python3
"""Triage of the supplied arXiv:1007.2318 PDF for the p25 KSY-y moonshot.

The user supplied /Users/agent/Downloads/1007.2318v1.pdf while we were trying
to recover Koo-Shin 2010.  This gate records the important distinction: the
file is the open sequel "On some arithmetic properties of Siegel functions
(II)", not the Math. Z. 2010 target "On some arithmetic properties of Siegel
functions".
"""

from __future__ import annotations

from dataclasses import dataclass


SUPPLIED_PATH = "/Users/agent/Downloads/1007.2318v1.pdf"
SUPPLIED_BYTES = 344_510
SUPPLIED_MD5 = "6e33e28091bc1a84a7d796c9a6e3ce33"
SUPPLIED_PAGES = 24
SUPPLIED_TITLE = "On some arithmetic properties of Siegel functions (II)"
TARGET_TITLE = "On some arithmetic properties of Siegel functions"
TARGET_DOI = "10.1007/s00209-008-0456-9"
TARGET_PAGES = "Math. Z. 264 (2010), 137-177"


@dataclass(frozen=True)
class SuppliedPdfRow:
    name: str
    evidence: str
    positive_payload: str
    missing_clause: str
    verdict: str
    is_target_2010: bool
    direct_closer: bool
    row_ok: bool


@dataclass(frozen=True)
class SuppliedPdfProfile:
    rows: tuple[SuppliedPdfRow, ...]
    supplied_file_rows: int
    sequel_identity_rows: int
    target_2010_rows: int
    reference_to_target_rows: int
    theorem_body_rows: int
    direct_closing_rows: int
    keep_as_context_rows: int
    still_need_2010_rows: int
    row_ok: bool


def supplied_rows() -> tuple[SuppliedPdfRow, ...]:
    return (
        SuppliedPdfRow(
            name="supplied_pdf_metadata",
            evidence=(
                f"path={SUPPLIED_PATH}; bytes={SUPPLIED_BYTES}; md5={SUPPLIED_MD5}; "
                f"pages={SUPPLIED_PAGES}"
            ),
            positive_payload="valid PDF supplied by user and text-extractable with pypdf",
            missing_clause="does not match KOASAS 2010 target size/hash or title",
            verdict="valid_supplied_pdf_not_target_hash",
            is_target_2010=False,
            direct_closer=False,
            row_ok=True,
        ),
        SuppliedPdfRow(
            name="arxiv_1007_2318_identity",
            evidence=(
                "extracted page 1 begins with arXiv:1007.2318v1 and title "
                f"{SUPPLIED_TITLE}"
            ),
            positive_payload=(
                "open sequel gives Siegel-function context, normal-basis/ray-class "
                "material, and text extraction"
            ),
            missing_clause=(
                f"target article is {TARGET_TITLE}, {TARGET_PAGES}, DOI {TARGET_DOI}"
            ),
            verdict="open_sequel_context_not_koo_shin_2010",
            is_target_2010=False,
            direct_closer=False,
            row_ok=True,
        ),
        SuppliedPdfRow(
            name="reference_to_target_article",
            evidence=(
                "extracted references include Koo and Shin, On some arithmetic "
                "properties of Siegel functions, Math. Zeit. 264 (2010) 137-177"
            ),
            positive_payload="confirms bibliographic target and citation chain",
            missing_clause=(
                "the referenced 2010 article body, especially Section 5 / "
                "Theorem 5.2, is still not supplied"
            ),
            verdict="reference_confirms_target_but_not_theorem_body",
            is_target_2010=False,
            direct_closer=False,
            row_ok=True,
        ),
    )


def profile_supplied_1007_2318_triage() -> SuppliedPdfProfile:
    rows = supplied_rows()
    supplied_file_rows = sum(row.name == "supplied_pdf_metadata" for row in rows)
    sequel_identity_rows = sum(row.verdict == "open_sequel_context_not_koo_shin_2010" for row in rows)
    target_2010_rows = sum(row.is_target_2010 for row in rows)
    reference_to_target_rows = sum(row.verdict == "reference_confirms_target_but_not_theorem_body" for row in rows)
    theorem_body_rows = 0
    direct_closing_rows = sum(row.direct_closer for row in rows)
    keep_as_context_rows = sum("context" in row.verdict or "reference" in row.verdict for row in rows)
    still_need_2010_rows = int(target_2010_rows == 0 and theorem_body_rows == 0)
    expected_verdicts = (
        "valid_supplied_pdf_not_target_hash",
        "open_sequel_context_not_koo_shin_2010",
        "reference_confirms_target_but_not_theorem_body",
    )
    row_ok = (
        SUPPLIED_BYTES == 344_510
        and SUPPLIED_MD5 == "6e33e28091bc1a84a7d796c9a6e3ce33"
        and SUPPLIED_PAGES == 24
        and len(rows) == 3
        and supplied_file_rows == 1
        and sequel_identity_rows == 1
        and target_2010_rows == 0
        and reference_to_target_rows == 1
        and theorem_body_rows == 0
        and direct_closing_rows == 0
        and keep_as_context_rows == 2
        and still_need_2010_rows == 1
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return SuppliedPdfProfile(
        rows=rows,
        supplied_file_rows=supplied_file_rows,
        sequel_identity_rows=sequel_identity_rows,
        target_2010_rows=target_2010_rows,
        reference_to_target_rows=reference_to_target_rows,
        theorem_body_rows=theorem_body_rows,
        direct_closing_rows=direct_closing_rows,
        keep_as_context_rows=keep_as_context_rows,
        still_need_2010_rows=still_need_2010_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_supplied_1007_2318_triage()
    print("p25 KSY-y supplied arXiv 1007.2318 PDF triage gate")
    print(f"supplied_path={SUPPLIED_PATH}")
    print(f"supplied_bytes={SUPPLIED_BYTES}")
    print(f"supplied_md5={SUPPLIED_MD5}")
    print(f"supplied_pages={SUPPLIED_PAGES}")
    print(f"supplied_title={SUPPLIED_TITLE}")
    print(f"target_title={TARGET_TITLE}")
    print(f"target_doi={TARGET_DOI}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: verdict={row.verdict} "
            f"target2010={int(row.is_target_2010)} closes={int(row.direct_closer)}"
        )
        print(f"    evidence={row.evidence}")
        print(f"    missing={row.missing_clause}")
    print("counts")
    print(f"  supplied_file_rows={profile.supplied_file_rows}")
    print(f"  sequel_identity_rows={profile.sequel_identity_rows}")
    print(f"  target_2010_rows={profile.target_2010_rows}")
    print(f"  reference_to_target_rows={profile.reference_to_target_rows}")
    print(f"  theorem_body_rows={profile.theorem_body_rows}")
    print(f"  direct_closing_rows={profile.direct_closing_rows}")
    print(f"  keep_as_context_rows={profile.keep_as_context_rows}")
    print(f"  still_need_2010_rows={profile.still_need_2010_rows}")
    print("interpretation")
    print("  supplied_pdf_is_koo_shin_ii_not_koo_shin_2010=1")
    print("  supplied_pdf_confirms_reference_but_not_theorem_body=1")
    print("  still_need_math_z_264_137_177_or_section5_ocr=1")
    print(f"ksy_y_koo_shin_supplied_1007_2318_triage_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin supplied 1007.2318 triage regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
