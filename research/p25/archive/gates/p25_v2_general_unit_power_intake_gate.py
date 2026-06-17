#!/usr/bin/env python3
"""Classify arbitrary exact row-power snippets for p25."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
P_MINUS_1_FACTORS = ((2, 2), (11, 1), (23, 1), (9881422924901185770751, 1))
MARKER = "p25_v2_general_unit_power_intake_rows=1/1"


UNIQUE_SAMPLE_EXPONENTS = (3, 5, 7, 9, 13, 25, 39, 65, 75, 169, 507, 1521)
AMBIGUOUS_SAMPLE_EXPONENTS = (
    2,
    4,
    6,
    8,
    11,
    22,
    23,
    33,
    44,
    46,
    69,
    78,
    115,
    121,
    143,
    156,
    253,
    300,
    338,
    676,
    780,
    1014,
    2028,
    8112,
)

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_fpstar_branch_factorization_20260617.md",
        "p25_v2_fpstar_branch_factorization_rows=1/1",
    ),
    (
        "evidence/p25_v2_power_output_kind_router_20260616.md",
        "p25_v2_power_output_kind_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
)

REQUIRED_NOTE_FRAGMENTS = (
    "general unit-power intake rule",
    "gcd(e, p - 1) = 1",
    "exact finite F_p value for one labeled row R_m^e",
    "powered divisor/additive or H90-boundary statement is not enough",
    "23-branch warning",
    "R_m^23",
    "kernel = 23",
    "current_general_power_source_theorems = 0",
    MARKER,
)


@dataclass(frozen=True)
class GeneralPowerAudit:
    evidence_markers_ok: int
    evidence_markers_total: int
    unique_samples_ok: int
    unique_samples_total: int
    ambiguous_samples_ok: int
    ambiguous_samples_total: int
    note_fragments_ok: int
    note_fragments_total: int
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def factor_product(factors: tuple[tuple[int, int], ...]) -> int:
    product = 1
    for prime, exponent in factors:
        product *= prime**exponent
    return product


def main() -> int:
    root = research_root()
    evidence_ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        path = root / rel
        evidence_ok += int(path.exists() and marker in path.read_text())

    note = root / "evidence/p25_v2_general_unit_power_intake_20260617.md"
    note_text = note.read_text() if note.exists() else ""
    note_ok = sum(fragment in note_text for fragment in REQUIRED_NOTE_FRAGMENTS)

    unique_ok = sum(gcd(exponent, P25 - 1) == 1 for exponent in UNIQUE_SAMPLE_EXPONENTS)
    ambiguous_ok = sum(gcd(exponent, P25 - 1) > 1 for exponent in AMBIGUOUS_SAMPLE_EXPONENTS)
    row_ok = (
        factor_product(P_MINUS_1_FACTORS) == P25 - 1
        and evidence_ok == len(EVIDENCE_MARKERS)
        and unique_ok == len(UNIQUE_SAMPLE_EXPONENTS)
        and ambiguous_ok == len(AMBIGUOUS_SAMPLE_EXPONENTS)
        and gcd(23, P25 - 1) == 23
        and pow(3, -1, P25 - 1) == 6666666666666666666666675
        and pow(75, -1, P25 - 1) == 266666666666666666666667
        and note_ok == len(REQUIRED_NOTE_FRAGMENTS)
    )
    audit = GeneralPowerAudit(
        evidence_markers_ok=evidence_ok,
        evidence_markers_total=len(EVIDENCE_MARKERS),
        unique_samples_ok=unique_ok,
        unique_samples_total=len(UNIQUE_SAMPLE_EXPONENTS),
        ambiguous_samples_ok=ambiguous_ok,
        ambiguous_samples_total=len(AMBIGUOUS_SAMPLE_EXPONENTS),
        note_fragments_ok=note_ok,
        note_fragments_total=len(REQUIRED_NOTE_FRAGMENTS),
        row_ok=row_ok,
    )
    print("p25 v2 general unit-power intake")
    print(f"p_minus_1_factors={P_MINUS_1_FACTORS}")
    print(f"evidence_markers_ok={audit.evidence_markers_ok}/{audit.evidence_markers_total}")
    print(f"unique_samples_ok={audit.unique_samples_ok}/{audit.unique_samples_total}")
    print(f"ambiguous_samples_ok={audit.ambiguous_samples_ok}/{audit.ambiguous_samples_total}")
    print("ambiguous_sample_kernels")
    for exponent in AMBIGUOUS_SAMPLE_EXPONENTS:
        print(f"  e={exponent}: kernel={gcd(exponent, P25 - 1)}")
    print(f"note_fragments_ok={audit.note_fragments_ok}/{audit.note_fragments_total}")
    print(f"{MARKER if audit.row_ok else 'p25_v2_general_unit_power_intake_rows=0/1'}")
    return 0 if audit.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
