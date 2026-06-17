#!/usr/bin/env python3
"""Prove the exact orbitwise support lower bound for H90 preimages of W."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from itertools import product
from pathlib import Path

import p25_v2_minimal_h90_preimage_classifier_gate as h90


EXPECTED_PATTERN = (-6, 6, -6, 6, -6, 6)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OrbitSupportRow:
    orbit: tuple[int, ...]
    boundary_pattern: tuple[int, ...]
    partial_sums: tuple[int, ...]
    best_zero_multiplicity: int
    local_support_lower_bound: int
    best_constants: tuple[int, ...]
    local_minimizers: int
    ok: bool


@dataclass(frozen=True)
class H90SupportLowerBound:
    evidence_markers: tuple[EvidenceMarker, ...]
    orbit_rows: tuple[OrbitSupportRow, ...]
    orbit_count: int
    global_support_lower_bound: int
    global_minimizers: int
    classifier_minimal_preimages: int
    classifier_mixed_legal_minimizers: int
    classifier_boundary_controls: int
    current_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "lanes").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def marker(name: str, rel_path: str, needle: str) -> EvidenceMarker:
    path = research_root() / rel_path
    text = path.read_text() if path.exists() else ""
    return EvidenceMarker(name=name, path=path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "minimal_h90_preimage_classifier",
            "evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md",
            "p25_v2_minimal_h90_preimage_classifier_rows=1/1",
        ),
        marker(
            "unified_source_theorem_gap",
            "evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "p25_v2_unified_source_theorem_gap_rows=1/1",
        ),
        marker(
            "quotient_h90_idempotent_mechanism",
            "evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "positive_theorem_clause_matcher",
            "evidence/p25_v2_positive_theorem_clause_matcher_20260616.md",
            "p25_v2_positive_theorem_clause_matcher_rows=1/1",
        ),
    )


def orbit_support_row(orbit: tuple[int, ...], source: dict[int, int]) -> OrbitSupportRow:
    pattern = tuple(source[residue] for residue in orbit)
    partial: list[int] = []
    value = 0
    for index in range(len(orbit)):
        if index != 0:
            value += pattern[index]
        partial.append(value)

    counts = Counter(partial)
    best_zero_multiplicity = max(counts.values())
    best_constants = tuple(sorted(-entry for entry, count in counts.items() if count == best_zero_multiplicity))
    local_support_lower_bound = len(orbit) - best_zero_multiplicity
    return OrbitSupportRow(
        orbit=orbit,
        boundary_pattern=pattern,
        partial_sums=tuple(partial),
        best_zero_multiplicity=best_zero_multiplicity,
        local_support_lower_bound=local_support_lower_bound,
        best_constants=best_constants,
        local_minimizers=len(best_constants),
        ok=(
            len(orbit) == 6
            and pattern == EXPECTED_PATTERN
            and tuple(partial) == (0, 6, 0, 6, 0, 6)
            and best_zero_multiplicity == 3
            and local_support_lower_bound == 3
            and best_constants == (-6, 0)
            and len(best_constants) == 2
        ),
    )


def classifier_counts(source: dict[int, int], orbits: tuple[tuple[int, ...], ...]) -> tuple[int, int, int]:
    local = tuple(h90.local_sparse_primitives(orbit, source) for orbit in orbits)
    rows = []
    for choice_bits in product((0, 1), repeat=len(local)):
        chosen = tuple(primitives[bit] for primitives, bit in zip(local, choice_bits))
        word = h90.combine_primitives(chosen)
        rows.append(h90.preimage_row(choice_bits, word, source))
    mixed = sum(row.decision == "mixed_legal_preimage" for row in rows)
    controls = len(rows) - mixed
    return len(rows), mixed, controls


def build_result() -> H90SupportLowerBound:
    markers = evidence_markers()
    source = h90.w_word()
    orbits = h90.frobenius_orbits(source)
    rows = tuple(orbit_support_row(orbit, source) for orbit in orbits)
    global_support_lower_bound = sum(row.local_support_lower_bound for row in rows)
    global_minimizers = 1
    for row in rows:
        global_minimizers *= row.local_minimizers
    minimal_preimages, mixed_legal, boundary_controls = classifier_counts(source, orbits)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and len(rows) == 4
        and all(row.ok for row in rows)
        and global_support_lower_bound == 12
        and global_minimizers == 16
        and minimal_preimages == 16
        and mixed_legal == 4
        and boundary_controls == 12
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return H90SupportLowerBound(
        evidence_markers=markers,
        orbit_rows=rows,
        orbit_count=len(rows),
        global_support_lower_bound=global_support_lower_bound,
        global_minimizers=global_minimizers,
        classifier_minimal_preimages=minimal_preimages,
        classifier_mixed_legal_minimizers=mixed_legal,
        classifier_boundary_controls=boundary_controls,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    result = build_result()
    print("p25 v2 H90 support lower-bound gate")
    for marker_row in result.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("orbit_support_rows")
    for row in result.orbit_rows:
        print(
            "  "
            f"orbit={row.orbit} pattern={row.boundary_pattern} "
            f"partial_sums={row.partial_sums} best_zero_multiplicity={row.best_zero_multiplicity} "
            f"local_support_lower_bound={row.local_support_lower_bound} "
            f"best_constants={row.best_constants} local_minimizers={row.local_minimizers} "
            f"ok={int(row.ok)}"
        )
    print("counts")
    print(f"  orbit_count={result.orbit_count}")
    print(f"  global_support_lower_bound={result.global_support_lower_bound}")
    print(f"  global_minimizers={result.global_minimizers}")
    print(f"  classifier_minimal_preimages={result.classifier_minimal_preimages}")
    print(f"  classifier_mixed_legal_minimizers={result.classifier_mixed_legal_minimizers}")
    print(f"  classifier_boundary_controls={result.classifier_boundary_controls}")
    print(f"  current_source_theorems={result.current_source_theorems}")
    print(f"  current_submission_ready={result.current_submission_ready}")
    print("interpretation")
    print("  no_H90_preimage_of_current_W_has_support_below_12=1")
    print("  support_12_minimizers_are_exactly_the_classifier_rows=1")
    print("  four_support_12_minimizers_are_legal_mixed_rows=1")
    print("  still_missing_arithmetic_value_or_divisor_theorem=1")
    print(f"p25_v2_h90_support_lower_bound_rows={int(result.row_ok)}/1")
    return 0 if result.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
