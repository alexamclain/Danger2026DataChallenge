#!/usr/bin/env python3
"""Mod-13 coset rectangle for the p25 conductor-39 signed-column rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


H = (1, 3, 9)
COSETS = (
    (1, 3, 9),
    (2, 5, 6),
    (4, 10, 12),
    (7, 8, 11),
)
SQUARE_COSET_IDS = (0, 2)
NONSQUARE_COSET_IDS = (1, 3)

LEGAL_ROWS = (
    (1, (7, 8, 11), (4, 10, 12)),
    (2, (7, 8, 11), (1, 3, 9)),
    (4, (2, 5, 6), (1, 3, 9)),
    (8, (2, 5, 6), (4, 10, 12)),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RectangleRow:
    multiplier: int
    row1_plus_columns: tuple[int, ...]
    row1_minus_columns: tuple[int, ...]
    plus_coset_id: int
    minus_coset_id: int
    plus_is_nonsquare_coset: bool
    minus_is_square_coset: bool
    row_ok: bool


@dataclass(frozen=True)
class ControlRow:
    name: str
    row1_plus_columns: tuple[int, ...]
    row1_minus_columns: tuple[int, ...]
    accepted_rectangle_edge: bool
    reject_reason: str
    row_ok: bool


@dataclass(frozen=True)
class Mod13CosetRectangle:
    evidence_markers: tuple[EvidenceMarker, ...]
    h_subgroup: tuple[int, ...]
    cosets: tuple[tuple[int, ...], ...]
    square_cosets: tuple[tuple[int, ...], ...]
    nonsquare_cosets: tuple[tuple[int, ...], ...]
    legal_rows: tuple[RectangleRow, ...]
    control_rows: tuple[ControlRow, ...]
    legal_rows_ok: int
    control_rows_ok: int
    rectangle_edges: tuple[tuple[int, int], ...]
    expected_rectangle_edges: tuple[tuple[int, int], ...]
    doubling_edge_cycle: tuple[tuple[int, int], ...]
    current_source_theorem_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "mixed_signed_column_fingerprint",
            "research/p25/evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
            "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
        ),
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "unified_theorem_review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
    )


def coset_id(columns: tuple[int, ...]) -> int:
    normalized = tuple(sorted(columns))
    if normalized not in COSETS:
        return -1
    return COSETS.index(normalized)


def multiply_coset(coset_id_value: int, multiplier: int) -> int:
    image = tuple(sorted((multiplier * value) % 13 for value in COSETS[coset_id_value]))
    return coset_id(image)


def rectangle_row(
    multiplier: int,
    row1_plus_columns: tuple[int, ...],
    row1_minus_columns: tuple[int, ...],
) -> RectangleRow:
    plus_id = coset_id(row1_plus_columns)
    minus_id = coset_id(row1_minus_columns)
    plus_non = plus_id in NONSQUARE_COSET_IDS
    minus_sq = minus_id in SQUARE_COSET_IDS
    return RectangleRow(
        multiplier=multiplier,
        row1_plus_columns=row1_plus_columns,
        row1_minus_columns=row1_minus_columns,
        plus_coset_id=plus_id,
        minus_coset_id=minus_id,
        plus_is_nonsquare_coset=plus_non,
        minus_is_square_coset=minus_sq,
        row_ok=plus_non and minus_sq,
    )


def control_row(
    name: str,
    row1_plus_columns: tuple[int, ...],
    row1_minus_columns: tuple[int, ...],
    reject_reason: str,
) -> ControlRow:
    plus_id = coset_id(row1_plus_columns)
    minus_id = coset_id(row1_minus_columns)
    accepted = plus_id in NONSQUARE_COSET_IDS and minus_id in SQUARE_COSET_IDS
    return ControlRow(
        name=name,
        row1_plus_columns=row1_plus_columns,
        row1_minus_columns=row1_minus_columns,
        accepted_rectangle_edge=accepted,
        reject_reason=reject_reason,
        row_ok=not accepted,
    )


def build_profile() -> Mod13CosetRectangle:
    markers = evidence_markers()
    rows = tuple(rectangle_row(*row) for row in LEGAL_ROWS)
    controls = (
        control_row(
            "pure_quadratic_character_all_nonsquares_vs_squares",
            (2, 5, 6, 7, 8, 11),
            (1, 3, 4, 9, 10, 12),
            "uses two cosets on each side rather than one order-3 coset edge",
        ),
        control_row(
            "same_parity_cosets",
            (2, 5, 6),
            (7, 8, 11),
            "plus and minus are both nonsquare cosets",
        ),
        control_row(
            "non_coset_triple",
            (2, 5, 7),
            (1, 3, 9),
            "plus columns are not an order-3 coset",
        ),
    )
    expected_edges = ((3, 2), (3, 0), (1, 0), (1, 2))
    edges = tuple((row.plus_coset_id, row.minus_coset_id) for row in rows)
    # Multiplication by 2 swaps the C_3 row and therefore cycles the row edges
    # in the order recorded by row-orbit normalization.
    cycle = tuple(
        (
            multiply_coset(row.plus_coset_id, 2),
            multiply_coset(row.minus_coset_id, 2),
        )
        for row in rows
    )
    legal_ok = sum(row.row_ok for row in rows)
    control_ok = sum(row.row_ok for row in controls)
    current_source_theorem_rows = 0
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and H == (1, 3, 9)
        and COSETS == ((1, 3, 9), (2, 5, 6), (4, 10, 12), (7, 8, 11))
        and legal_ok == 4
        and control_ok == 3
        and edges == expected_edges
        and cycle == ((0, 3), (0, 1), (2, 1), (2, 3))
        and current_source_theorem_rows == 0
    )
    return Mod13CosetRectangle(
        evidence_markers=markers,
        h_subgroup=H,
        cosets=COSETS,
        square_cosets=tuple(COSETS[index] for index in SQUARE_COSET_IDS),
        nonsquare_cosets=tuple(COSETS[index] for index in NONSQUARE_COSET_IDS),
        legal_rows=rows,
        control_rows=controls,
        legal_rows_ok=legal_ok,
        control_rows_ok=control_ok,
        rectangle_edges=edges,
        expected_rectangle_edges=expected_edges,
        doubling_edge_cycle=cycle,
        current_source_theorem_rows=current_source_theorem_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 mod-13 coset rectangle gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"H={profile.h_subgroup}")
    print(f"cosets={profile.cosets}")
    print(f"square_cosets={profile.square_cosets}")
    print(f"nonsquare_cosets={profile.nonsquare_cosets}")
    print("legal_rows")
    for row in profile.legal_rows:
        print(
            "  "
            f"m={row.multiplier} plus={row.row1_plus_columns} "
            f"minus={row.row1_minus_columns} edge=({row.plus_coset_id},{row.minus_coset_id}) "
            f"plus_nonsquare={int(row.plus_is_nonsquare_coset)} "
            f"minus_square={int(row.minus_is_square_coset)} ok={int(row.row_ok)}"
        )
    print("control_rows")
    for row in profile.control_rows:
        print(
            "  "
            f"{row.name}: accepted={int(row.accepted_rectangle_edge)} "
            f"reject_reason={row.reject_reason} ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  legal_rows_ok={profile.legal_rows_ok}/4")
    print(f"  control_rows_ok={profile.control_rows_ok}/3")
    print(f"  rectangle_edges={profile.rectangle_edges}")
    print(f"  expected_rectangle_edges={profile.expected_rectangle_edges}")
    print(f"  doubling_edge_cycle={profile.doubling_edge_cycle}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  legal_rows_are_rectangle_edges_between_nonsquare_and_square_order3_cosets=1")
    print("  pure_quadratic_character_is_too_broad=1")
    print("  non_coset_or_same_parity_column_claims_are_rejected=1")
    print("  still_missing_arithmetic_value_or_divisor_theorem=1")
    print(f"p25_v2_mod13_coset_rectangle_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
