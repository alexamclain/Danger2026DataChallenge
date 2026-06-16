#!/usr/bin/env python3
"""Koo-Shin 2010 PDF/OCR intake contract for the p25 KSY-y moonshot.

The Koo-Shin 2010 source is the most valuable missing external theorem body.
This gate does two things:

* records exactly what supplied artifacts are acceptable;
* optionally classifies a supplied candidate path before theorem-clause intake.

The contract is deliberately stricter than "found a citation": snippets,
metadata pages, and access HTML are not theorem bodies.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


TITLE = "On some arithmetic properties of Siegel functions"
DOI = "10.1007/s00209-008-0456-9"
KOASAS_BITSTREAM = "000271750900008.pdf"
KOASAS_SIZE = 501_978
KOASAS_MD5 = "39bf3ab80a349709394165f27f0eafbf"
KNOWN_SEQUEL_1007_2318_MD5 = "6e33e28091bc1a84a7d796c9a6e3ce33"
THEOREM_TRIGGER = "Theorem 5.2"
SECTION_TRIGGER = "distribution relations"


@dataclass(frozen=True)
class IntakeRow:
    name: str
    supplied_artifact: str
    accept_condition: str
    first_action: str
    verdict: str
    acceptable: bool
    row_ok: bool


@dataclass(frozen=True)
class CandidateClassification:
    path: str
    exists: bool
    bytes_: int
    md5: str
    magic: str
    looks_pdf: bool
    looks_text: bool
    exact_koasas_match: bool
    has_title: bool
    has_doi: bool
    has_theorem_5_2: bool
    has_distribution_context: bool
    verdict: str
    next_action: str
    acceptable_for_intake: bool


@dataclass(frozen=True)
class IntakeProfile:
    rows: tuple[IntakeRow, ...]
    acceptable_rows: int
    exact_pdf_rows: int
    ocr_or_page_rows: int
    rejected_snippet_rows: int
    theorem_clause_required_rows: int
    row_ok: bool


def intake_rows() -> tuple[IntakeRow, ...]:
    return (
        IntakeRow(
            name="exact_koasas_bitstream_pdf",
            supplied_artifact=KOASAS_BITSTREAM,
            accept_condition=(
                f"PDF bytes match KOASAS size={KOASAS_SIZE} and md5={KOASAS_MD5}"
            ),
            first_action=(
                "extract or OCR pages around Section 5 and Theorem 5.2, then "
                "run p25_ksy_y_koo_shin_theorem_clause_intake_gate.py"
            ),
            verdict="accept_exact_pdf",
            acceptable=True,
            row_ok=True,
        ),
        IntakeRow(
            name="library_or_springer_pdf_variant",
            supplied_artifact="downloaded article PDF with possible watermark",
            accept_condition=(
                "file starts with %PDF and metadata/text/OCR identifies title, "
                f"DOI {DOI}, authors, and pages 137-177"
            ),
            first_action=(
                "extract/OCR Theorem 5.2 and adjacent Section 5 definitions; "
                "compare against the KOASAS target if possible"
            ),
            verdict="accept_pdf_variant_with_identity_check",
            acceptable=True,
            row_ok=True,
        ),
        IntakeRow(
            name="ocr_or_page_images",
            supplied_artifact="OCR text or page images for Section 5",
            accept_condition=(
                "contains the full Theorem 5.2 statement, hypotheses, notation, "
                "and the definitions immediately needed to parse its product"
            ),
            first_action=(
                "feed the theorem statement through the theorem-clause intake "
                "and check exact P/mixed graph/equal weights/orientation"
            ),
            verdict="accept_theorem_body_ocr",
            acceptable=True,
            row_ok=True,
        ),
        IntakeRow(
            name="snippet_metadata_or_access_html",
            supplied_artifact="search snippet, Springer metadata page, KOASAS metadata, or access HTML",
            accept_condition="not enough: no full theorem body or surrounding notation",
            first_action="keep as citation/retrieval evidence only",
            verdict="reject_not_theorem_body",
            acceptable=False,
            row_ok=True,
        ),
    )


def profile_koo_shin_pdf_intake_contract() -> IntakeProfile:
    rows = intake_rows()
    acceptable_rows = sum(row.acceptable for row in rows)
    exact_pdf_rows = sum(row.verdict == "accept_exact_pdf" for row in rows)
    ocr_or_page_rows = sum(row.verdict == "accept_theorem_body_ocr" for row in rows)
    rejected_snippet_rows = sum(row.verdict == "reject_not_theorem_body" for row in rows)
    theorem_clause_required_rows = sum(row.acceptable for row in rows)
    expected_verdicts = (
        "accept_exact_pdf",
        "accept_pdf_variant_with_identity_check",
        "accept_theorem_body_ocr",
        "reject_not_theorem_body",
    )
    row_ok = (
        DOI == "10.1007/s00209-008-0456-9"
        and KOASAS_SIZE == 501_978
        and KOASAS_MD5 == "39bf3ab80a349709394165f27f0eafbf"
        and len(rows) == 4
        and acceptable_rows == 3
        and exact_pdf_rows == 1
        and ocr_or_page_rows == 1
        and rejected_snippet_rows == 1
        and theorem_clause_required_rows == 3
        and tuple(row.verdict for row in rows) == expected_verdicts
        and all(row.row_ok for row in rows)
    )
    return IntakeProfile(
        rows=rows,
        acceptable_rows=acceptable_rows,
        exact_pdf_rows=exact_pdf_rows,
        ocr_or_page_rows=ocr_or_page_rows,
        rejected_snippet_rows=rejected_snippet_rows,
        theorem_clause_required_rows=theorem_clause_required_rows,
        row_ok=row_ok,
    )


def md5_file(path: Path) -> str:
    digest = hashlib.md5()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify_candidate(path: Path) -> CandidateClassification:
    if not path.exists():
        return CandidateClassification(
            path=str(path),
            exists=False,
            bytes_=0,
            md5="",
            magic="",
            looks_pdf=False,
            looks_text=False,
            exact_koasas_match=False,
            has_title=False,
            has_doi=False,
            has_theorem_5_2=False,
            has_distribution_context=False,
            verdict="missing_candidate",
            next_action="place the Koo-Shin PDF/OCR at this path or pass --candidate to the actual file",
            acceptable_for_intake=False,
        )

    data = path.read_bytes()
    head = data[:4096]
    text_head = head.decode("utf-8", errors="ignore")
    full_text = data.decode("utf-8", errors="ignore") if len(data) <= 5_000_000 else text_head
    bytes_ = len(data)
    md5 = md5_file(path)
    magic = head[:16].decode("latin-1", errors="replace")
    looks_pdf = head.startswith(b"%PDF")
    looks_text = not looks_pdf and bool(text_head.strip())
    exact_koasas_match = bytes_ == KOASAS_SIZE and md5 == KOASAS_MD5
    has_title = TITLE.lower() in full_text.lower()
    has_doi = DOI.lower() in full_text.lower()
    has_theorem_5_2 = THEOREM_TRIGGER.lower() in full_text.lower()
    has_distribution_context = SECTION_TRIGGER.lower() in full_text.lower()

    if exact_koasas_match:
        verdict = "accept_exact_koasas_pdf"
        next_action = "extract/OCR Section 5 and run theorem-clause intake"
        acceptable = True
    elif md5 == KNOWN_SEQUEL_1007_2318_MD5 or "1007.2318" in path.name:
        verdict = "reject_known_open_sequel_not_2010_target"
        next_action = "keep as Koo-Shin II context; still need Math. Z. 264 (2010), 137-177"
        acceptable = False
    elif looks_pdf and (has_title or has_doi or path.suffix.lower() == ".pdf"):
        verdict = "conditional_pdf_variant_needs_identity_and_text_extraction"
        next_action = "verify title/DOI/pages, extract/OCR Theorem 5.2, then run theorem-clause intake"
        acceptable = True
    elif looks_text and has_theorem_5_2 and (has_distribution_context or has_title or has_doi):
        verdict = "accept_ocr_theorem_body"
        next_action = "run theorem-clause intake on the supplied theorem body"
        acceptable = True
    elif looks_text and ("<!doctype html" in full_text[:100].lower() or "<html" in full_text[:200].lower()):
        verdict = "reject_html_or_access_page"
        next_action = "use only as retrieval evidence; still need PDF/OCR theorem body"
        acceptable = False
    else:
        verdict = "reject_insufficient_theorem_body"
        next_action = "supply full PDF, OCR, or page images around Theorem 5.2"
        acceptable = False

    return CandidateClassification(
        path=str(path),
        exists=True,
        bytes_=bytes_,
        md5=md5,
        magic=magic,
        looks_pdf=looks_pdf,
        looks_text=looks_text,
        exact_koasas_match=exact_koasas_match,
        has_title=has_title,
        has_doi=has_doi,
        has_theorem_5_2=has_theorem_5_2,
        has_distribution_context=has_distribution_context,
        verdict=verdict,
        next_action=next_action,
        acceptable_for_intake=acceptable,
    )


def print_profile(profile: IntakeProfile) -> None:
    print("p25 KSY-y Koo-Shin PDF/OCR intake contract gate")
    print(f"title={TITLE}")
    print(f"doi={DOI}")
    print(f"koasas_bitstream={KOASAS_BITSTREAM}")
    print(f"koasas_size={KOASAS_SIZE}")
    print(f"koasas_md5={KOASAS_MD5}")
    print("rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: verdict={row.verdict} acceptable={int(row.acceptable)} "
            f"artifact={row.supplied_artifact}"
        )
        print(f"    condition={row.accept_condition}")
        print(f"    first_action={row.first_action}")
    print("counts")
    print(f"  acceptable_rows={profile.acceptable_rows}")
    print(f"  exact_pdf_rows={profile.exact_pdf_rows}")
    print(f"  ocr_or_page_rows={profile.ocr_or_page_rows}")
    print(f"  rejected_snippet_rows={profile.rejected_snippet_rows}")
    print(f"  theorem_clause_required_rows={profile.theorem_clause_required_rows}")
    print("interpretation")
    print("  exact_pdf_ocr_or_section5_pages_are_acceptable=1")
    print("  metadata_snippets_and_access_html_are_rejected=1")
    print("  theorem_clause_intake_is_next_after_source_recovery=1")
    print(f"ksy_y_koo_shin_pdf_intake_contract_rows={int(profile.row_ok)}/1")


def print_candidate(candidate: CandidateClassification) -> None:
    print("candidate_classification")
    print(f"  path={candidate.path}")
    print(f"  exists={int(candidate.exists)}")
    print(f"  bytes={candidate.bytes_}")
    print(f"  md5={candidate.md5}")
    print(f"  magic={candidate.magic!r}")
    print(f"  looks_pdf={int(candidate.looks_pdf)}")
    print(f"  looks_text={int(candidate.looks_text)}")
    print(f"  exact_koasas_match={int(candidate.exact_koasas_match)}")
    print(f"  has_title={int(candidate.has_title)}")
    print(f"  has_doi={int(candidate.has_doi)}")
    print(f"  has_theorem_5_2={int(candidate.has_theorem_5_2)}")
    print(f"  has_distribution_context={int(candidate.has_distribution_context)}")
    print(f"  verdict={candidate.verdict}")
    print(f"  next_action={candidate.next_action}")
    print(f"  acceptable_for_intake={int(candidate.acceptable_for_intake)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", type=Path)
    args = parser.parse_args()

    profile = profile_koo_shin_pdf_intake_contract()
    print_profile(profile)
    if args.candidate is not None:
        print_candidate(classify_candidate(args.candidate))
    if not profile.row_ok:
        raise SystemExit("Koo-Shin PDF/OCR intake contract regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
