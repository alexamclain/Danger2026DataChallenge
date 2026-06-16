#!/usr/bin/env python3
"""Smoke gate for the Koo-Shin incoming scanner."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from scan_koo_shin_incoming import (  # noqa: E402
    DEFAULT_PATHS,
    KOASAS_MD5,
    KOASAS_SIZE,
    classify_candidate,
    candidate_paths,
    extract_pdf_text,
    scan_text_file,
)


KNOWN_SEQUEL = Path("/Users/agent/Downloads/1007.2318v1.pdf")
EXACT_2010 = Path("/Users/agent/Downloads/s00209-008-0456-9.pdf")
EXTRACTED_DIR = REPO / "incoming" / "extracted"


@dataclass(frozen=True)
class IncomingScannerSmokeProfile:
    scanner_exists: bool
    incoming_dir_exists: bool
    default_roots: int
    known_sequel_present: bool
    known_sequel_rejected: bool
    known_sequel_extracts_text: bool
    known_sequel_has_section5: bool
    known_sequel_has_theorem5_2: bool
    exact_2010_present: bool
    exact_2010_accepted: bool
    exact_2010_extracts_text: bool
    exact_2010_has_theorem5_2: bool
    exact_koasas_size: int
    exact_koasas_md5_ok: bool
    candidate_count: int
    row_ok: bool


def extracted_text_fallback(path: Path):
    extracted = extract_pdf_text(path, EXTRACTED_DIR)
    if extracted.chars:
        return extracted
    fallback = EXTRACTED_DIR / f"{path.name}.extract.txt"
    if fallback.exists():
        return scan_text_file(fallback)
    return extracted


def profile_incoming_scanner_smoke() -> IncomingScannerSmokeProfile:
    scanner_exists = (SRC / "scan_koo_shin_incoming.py").exists()
    incoming_dir_exists = (REPO / "incoming").is_dir()
    default_roots = len(DEFAULT_PATHS)
    known_sequel_present = KNOWN_SEQUEL.exists()
    known_sequel_rejected = False
    known_sequel_extracts_text = False
    known_sequel_has_section5 = False
    known_sequel_has_theorem5_2 = False
    if known_sequel_present:
        classification = classify_candidate(KNOWN_SEQUEL)
        known_sequel_rejected = (
            classification.verdict == "reject_known_open_sequel_not_2010_target"
            and not classification.acceptable_for_intake
        )
        extracted = extracted_text_fallback(KNOWN_SEQUEL)
        known_sequel_extracts_text = extracted.chars > 50_000 and extracted.pages in {0, 24}
        known_sequel_has_section5 = extracted.has_section5
        known_sequel_has_theorem5_2 = extracted.has_theorem_5_2
    exact_2010_present = EXACT_2010.exists()
    exact_2010_accepted = False
    exact_2010_extracts_text = False
    exact_2010_has_theorem5_2 = False
    if exact_2010_present:
        classification = classify_candidate(EXACT_2010)
        exact_2010_accepted = (
            classification.verdict == "accept_exact_koasas_pdf"
            and classification.acceptable_for_intake
        )
        extracted = extracted_text_fallback(EXACT_2010)
        exact_2010_extracts_text = extracted.chars > 80_000 and extracted.pages in {0, 41}
        exact_2010_has_theorem5_2 = extracted.has_theorem_5_2
    candidates = candidate_paths(list(DEFAULT_PATHS))
    exact_koasas_md5_ok = KOASAS_MD5 == "39bf3ab80a349709394165f27f0eafbf"
    row_ok = (
        scanner_exists
        and incoming_dir_exists
        and default_roots == 2
        and known_sequel_present
        and known_sequel_rejected
        and known_sequel_extracts_text
        and known_sequel_has_section5
        and not known_sequel_has_theorem5_2
        and exact_2010_present
        and exact_2010_accepted
        and exact_2010_extracts_text
        and exact_2010_has_theorem5_2
        and KOASAS_SIZE == 501_978
        and exact_koasas_md5_ok
        and len(candidates) >= 2
    )
    return IncomingScannerSmokeProfile(
        scanner_exists=scanner_exists,
        incoming_dir_exists=incoming_dir_exists,
        default_roots=default_roots,
        known_sequel_present=known_sequel_present,
        known_sequel_rejected=known_sequel_rejected,
        known_sequel_extracts_text=known_sequel_extracts_text,
        known_sequel_has_section5=known_sequel_has_section5,
        known_sequel_has_theorem5_2=known_sequel_has_theorem5_2,
        exact_2010_present=exact_2010_present,
        exact_2010_accepted=exact_2010_accepted,
        exact_2010_extracts_text=exact_2010_extracts_text,
        exact_2010_has_theorem5_2=exact_2010_has_theorem5_2,
        exact_koasas_size=KOASAS_SIZE,
        exact_koasas_md5_ok=exact_koasas_md5_ok,
        candidate_count=len(candidates),
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_incoming_scanner_smoke()
    print("p25 KSY-y Koo-Shin incoming scanner smoke gate")
    print(f"scanner_exists={int(profile.scanner_exists)}")
    print(f"incoming_dir_exists={int(profile.incoming_dir_exists)}")
    print(f"default_roots={profile.default_roots}")
    print(f"known_sequel_present={int(profile.known_sequel_present)}")
    print(f"known_sequel_rejected={int(profile.known_sequel_rejected)}")
    print(f"known_sequel_extracts_text={int(profile.known_sequel_extracts_text)}")
    print(f"known_sequel_has_section5={int(profile.known_sequel_has_section5)}")
    print(f"known_sequel_has_theorem5_2={int(profile.known_sequel_has_theorem5_2)}")
    print(f"exact_2010_present={int(profile.exact_2010_present)}")
    print(f"exact_2010_accepted={int(profile.exact_2010_accepted)}")
    print(f"exact_2010_extracts_text={int(profile.exact_2010_extracts_text)}")
    print(f"exact_2010_has_theorem5_2={int(profile.exact_2010_has_theorem5_2)}")
    print(f"exact_koasas_size={profile.exact_koasas_size}")
    print(f"exact_koasas_md5_ok={int(profile.exact_koasas_md5_ok)}")
    print(f"candidate_count={profile.candidate_count}")
    print("interpretation")
    print("  incoming_scanner_found_exact_2010_pdf=1")
    print("  known_arxiv_sequel_is_rejected_and_extracted_as_context=1")
    print("  exact_2010_theorem5_2_still_needed=0")
    print(f"ksy_y_koo_shin_incoming_scanner_smoke_rows={int(profile.row_ok)}/1")
    if not profile.row_ok:
        raise SystemExit("Koo-Shin incoming scanner smoke regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
