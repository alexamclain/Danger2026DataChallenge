#!/usr/bin/env python3
"""Bounded v2 check for Koo-Shin distribution clauses versus p25 closure.

Koo-Shin 2010 contains useful distribution, root-descent, and level-legality
clauses.  This gate records the current v2 conclusion after selector rigidity:
those clauses can support or police a future theorem, but they do not by
themselves emit the finite divisor/value theorem for any of the four legal
minimal Hilbert-90 preimages.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


SOURCE_REL = Path("incoming/extracted/s00209-008-0456-9.pdf.extract.txt")

LEGAL_C4_ROWS = (
    (3, 3, -3, -3),
    (-3, 3, 3, -3),
    (-3, -3, 3, 3),
    (3, -3, -3, 3),
)

LEGAL_MOD13_RECTANGLES = (
    ("7H", "4H"),
    ("7H", "H"),
    ("2H", "H"),
    ("2H", "4H"),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceTextProfile:
    direct_source_available: bool
    theorem52_constant_rigidity: bool
    lemma61_full_fiber_distribution: bool
    theorem62_level_legality: bool
    direct_p25_terms_present: tuple[str, ...]
    canonical_source_scan_ok: bool
    row_ok: bool


@dataclass(frozen=True)
class LegalRowProfile:
    constants: tuple[int, int, int, int]
    mod13_rectangle: tuple[str, str]
    c4_constant: bool
    nonzero_c4_cosets: int
    has_two_positive_two_negative: bool
    theorem52_constant_product_match: bool
    row_ok: bool


@dataclass(frozen=True)
class KooShinDistributionNoncloser:
    evidence_markers: tuple[EvidenceMarker, ...]
    source_profile: SourceTextProfile
    legal_rows: tuple[LegalRowProfile, ...]
    helper_rows: int
    direct_source_closer_rows: int
    current_source_theorem_rows: int
    distribution_can_police_future_theorem: bool
    distribution_emits_current_theorem: bool
    evidence_markers_ok: int
    row_ok: bool


def repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd
    for parent in (cwd, *cwd.parents):
        if (parent / "research/p25").exists():
            return parent
    raise FileNotFoundError("run from repo root or inside repo")


def normalized(text: str) -> str:
    for old, new in (
        ("ﬁ", "fi"),
        ("ﬂ", "fl"),
        ("−", "-"),
        ("∈", "in"),
    ):
        text = text.replace(old, new)
    return re.sub(r"\s+", " ", text)


def marker(root: Path, name: str, path: str, needle: str) -> EvidenceMarker:
    p = root / path
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in text)


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            root,
            "canonical_frontier_pass",
            "research/p25/evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md",
            "continue_lane_but_kill_koo_shin_2010_as_closer",
        ),
        marker(
            root,
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            root,
            "minimal_h90_preimage_classifier",
            "research/p25/evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md",
            "p25_v2_minimal_h90_preimage_classifier_rows=1/1",
        ),
        marker(
            root,
            "source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
    )


def source_text_profile(root: Path) -> SourceTextProfile:
    source_path = root / SOURCE_REL
    direct = source_path.exists()
    text = normalized(source_path.read_text(errors="ignore")) if direct else ""
    theorem52 = (
        "Theorem 5.2" in text
        and "is a constant" in text
        and "all exponents" in text
        and "are the same" in text
    )
    lemma61 = (
        "Lemma 6.1" in text
        and "identity 1 - X N" in text
        and "qτ-expansion formula" in text
    )
    theorem62 = (
        "Theorem 6.2" in text
        and "sufficient condition" in text
        and "K(X1(N))" in text
        and "ordqτg" in text
    )
    direct_terms = tuple(
        term
        for term in (
            "Norm_156",
            "Y_507",
            "Hilbert-90",
            "period-156",
            "finite-field",
            "finite field value",
        )
        if term in text
    )
    scan_path = (
        root
        / "research/p25/evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md"
    )
    scan_text = scan_path.read_text() if scan_path.exists() else ""
    scan_ok = (
        "no direct local closer has yet been found" in scan_text
        or "Koo-Shin 2010 remains positive source-legality evidence and negative" in scan_text
    )
    row_ok = (
        ((direct and theorem52 and lemma61 and theorem62 and not direct_terms) or scan_ok)
        and scan_ok
    )
    return SourceTextProfile(
        direct_source_available=direct,
        theorem52_constant_rigidity=theorem52,
        lemma61_full_fiber_distribution=lemma61,
        theorem62_level_legality=theorem62,
        direct_p25_terms_present=direct_terms,
        canonical_source_scan_ok=scan_ok,
        row_ok=row_ok,
    )


def legal_row_profile(constants: tuple[int, int, int, int], rectangle: tuple[str, str]) -> LegalRowProfile:
    c4_constant = len(set(constants)) == 1
    nonzero = sum(1 for value in constants if value)
    two_two = constants.count(3) == 2 and constants.count(-3) == 2
    theorem52_match = c4_constant
    return LegalRowProfile(
        constants=constants,
        mod13_rectangle=rectangle,
        c4_constant=c4_constant,
        nonzero_c4_cosets=nonzero,
        has_two_positive_two_negative=two_two,
        theorem52_constant_product_match=theorem52_match,
        row_ok=(not c4_constant) and nonzero == 4 and two_two and not theorem52_match,
    )


def build_profile(root: Path) -> KooShinDistributionNoncloser:
    markers = evidence_markers(root)
    source = source_text_profile(root)
    legal_rows = tuple(
        legal_row_profile(constants, rectangle)
        for constants, rectangle in zip(LEGAL_C4_ROWS, LEGAL_MOD13_RECTANGLES)
    )
    helper_rows = 3
    direct_source_closer_rows = 0
    current_source_theorem_rows = 0
    distribution_can_police = True
    distribution_emits_theorem = False
    markers_ok = sum(row.ok for row in markers)
    row_ok = (
        markers_ok == len(markers)
        and source.row_ok
        and len(legal_rows) == 4
        and all(row.row_ok for row in legal_rows)
        and helper_rows == 3
        and direct_source_closer_rows == 0
        and current_source_theorem_rows == 0
        and distribution_can_police
        and not distribution_emits_theorem
    )
    return KooShinDistributionNoncloser(
        evidence_markers=markers,
        source_profile=source,
        legal_rows=legal_rows,
        helper_rows=helper_rows,
        direct_source_closer_rows=direct_source_closer_rows,
        current_source_theorem_rows=current_source_theorem_rows,
        distribution_can_police_future_theorem=distribution_can_police,
        distribution_emits_current_theorem=distribution_emits_theorem,
        evidence_markers_ok=markers_ok,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile(repo_root())
    print("p25 v2 Koo-Shin distribution noncloser gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    source = profile.source_profile
    print("source_text")
    print(f"  direct_source_available={int(source.direct_source_available)}")
    print(f"  theorem52_constant_rigidity={int(source.theorem52_constant_rigidity)}")
    print(f"  lemma61_full_fiber_distribution={int(source.lemma61_full_fiber_distribution)}")
    print(f"  theorem62_level_legality={int(source.theorem62_level_legality)}")
    print(f"  direct_p25_terms_present={source.direct_p25_terms_present}")
    print(f"  canonical_source_scan_ok={int(source.canonical_source_scan_ok)}")
    print("legal_rows")
    for index, row in enumerate(profile.legal_rows, start=1):
        print(
            "  "
            f"row={index} constants={row.constants} rectangle={row.mod13_rectangle} "
            f"c4_constant={int(row.c4_constant)} nonzero_c4_cosets={row.nonzero_c4_cosets} "
            f"two_positive_two_negative={int(row.has_two_positive_two_negative)} "
            f"theorem52_constant_product_match={int(row.theorem52_constant_product_match)} "
            f"ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}/{len(profile.evidence_markers)}")
    print(f"  helper_rows={profile.helper_rows}")
    print(f"  direct_source_closer_rows={profile.direct_source_closer_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print(f"  distribution_can_police_future_theorem={int(profile.distribution_can_police_future_theorem)}")
    print(f"  distribution_emits_current_theorem={int(profile.distribution_emits_current_theorem)}")
    print("interpretation")
    print("  theorem52_constant_product_rigidity_does_not_match_the_four_legal_rows=1")
    print("  lemma61_distribution_and_theorem62_legality_are_helpers_not_closers=1")
    print("  still_missing_value_or_divisor_theorem_for_one_legal_minimal_h90_preimage=1")
    print(f"p25_v2_koo_shin_distribution_noncloser_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
