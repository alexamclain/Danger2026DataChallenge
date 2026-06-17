#!/usr/bin/env python3
"""Complexity screen for the Q diagonal split quotients.

The Q diagonal-normalization route says that Q sees the diagonal aggregate
m1+m4=m2+m8.  To normalize that to one edge, the relevant boundary-zero splits
are m1-m4 and m2-m8.  This gate records a useful falsifier: those two split
quotients are not cheap one-axis or one-coset objects.  They are Frobenius
invariant and boundary-zero, but they use all twelve mod-13 columns.  The
smaller support-12 row quotients are not the diagonal splits that Q needs.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P_MOD_39 = 23
COEFFICIENT = 6
C4_COSETS = (
    (1, 3, 9),
    (2, 5, 6),
    (4, 10, 12),
    (7, 8, 11),
)
LEGAL_ROWS = {
    1: ((7, 17, 23, 34, 37, 38), (4, 8, 10, 11, 20, 25)),
    2: ((7, 14, 29, 34, 35, 37), (1, 8, 11, 16, 20, 22)),
    4: ((14, 19, 28, 29, 31, 35), (1, 2, 5, 16, 22, 32)),
    8: ((17, 19, 23, 28, 31, 38), (2, 4, 5, 10, 25, 32)),
}
DIAGONAL_SPLITS = ((1, 4), (2, 8))
NON_DIAGONAL_QUOTIENTS = ((1, 2), (1, 8), (2, 4), (4, 8))


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SplitProfile:
    name: str
    numerator: int
    denominator: int
    support: int
    coefficient_values: tuple[int, ...]
    boundary_support: int
    frobenius_invariant: bool
    mod3_pushforward_zero: bool
    mod13_pushforward_zero: bool
    live_columns: int
    row1_plus_coset_count: int
    row1_minus_coset_count: int
    c4_antisym: tuple[int, int, int, int]
    is_diagonal_q_split: bool
    is_one_coset_rectangle_edge: bool
    row_ok: bool


@dataclass(frozen=True)
class RouteRow:
    name: str
    decision: str
    first_missing_or_falsifier: str
    normalize: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class QSplitQuotientComplexity:
    evidence_markers: tuple[EvidenceMarker, ...]
    diagonal_splits: tuple[SplitProfile, ...]
    support12_controls: tuple[SplitProfile, ...]
    routes: tuple[RouteRow, ...]
    evidence_markers_ok: int
    diagonal_split_count: int
    diagonal_support24_count: int
    diagonal_all_columns_count: int
    support12_non_diagonal_count: int
    normalize_routes: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "q_plus_row_quotient_without_root",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "q_plus_explicit_oriented_diagonal_split",
        ),
    )


def normalize(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def row_word(multiplier: int) -> dict[int, int]:
    positive, negative = LEGAL_ROWS[multiplier]
    word: dict[int, int] = {}
    for residue in positive:
        word[residue] = word.get(residue, 0) + COEFFICIENT
    for residue in negative:
        word[residue] = word.get(residue, 0) - COEFFICIENT
    return normalize(word)


def add_words(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    word = dict(left)
    for residue, value in right.items():
        word[residue] = word.get(residue, 0) + value
    return normalize(word)


def scale_word(word: dict[int, int], scale: int) -> dict[int, int]:
    return normalize({residue: scale * value for residue, value in word.items()})


def subtract(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    return add_words(left, scale_word(right, -1))


def quotient(numerator: int, denominator: int) -> dict[int, int]:
    return subtract(row_word(numerator), row_word(denominator))


def frobenius_push(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        target = (P_MOD_39 * residue) % 39
        out[target] = out.get(target, 0) + value
    return normalize(out)


def boundary(word: dict[int, int]) -> dict[int, int]:
    return subtract(word, frobenius_push(word))


def pushforward(word: dict[int, int], modulus: int) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        out[residue % modulus] = out.get(residue % modulus, 0) + value
    return normalize(out)


def c4_index(residue: int) -> int:
    col = residue % 13
    for index, coset in enumerate(C4_COSETS):
        if col in coset:
            return index
    raise ValueError(f"residue {residue} is not prime to 13")


def c4_rows(word: dict[int, int]) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    rows = [[0, 0, 0, 0], [0, 0, 0, 0]]
    for residue, value in word.items():
        row = 0 if residue % 3 == 1 else 1
        rows[row][c4_index(residue)] += value
    return tuple(rows[0]), tuple(rows[1])


def column_signs(word: dict[int, int]) -> dict[int, tuple[int, int]]:
    cols: dict[int, list[int]] = {}
    for residue, value in word.items():
        col = residue % 13
        row = 0 if residue % 3 == 1 else 1
        cols.setdefault(col, [0, 0])[row] += value
    return {
        col: (values[0], values[1])
        for col, values in sorted(cols.items())
        if values != [0, 0]
    }


def coset_count(columns: tuple[int, ...]) -> int:
    present = {
        index
        for index, coset in enumerate(C4_COSETS)
        if any(column in coset for column in columns)
    }
    return len(present)


def profile(name: str, numerator: int, denominator: int, is_diagonal: bool) -> SplitProfile:
    word = quotient(numerator, denominator)
    cols = column_signs(word)
    plus_cols = tuple(col for col, values in cols.items() if values[0] > 0)
    minus_cols = tuple(col for col, values in cols.items() if values[0] < 0)
    rows = c4_rows(word)
    antisym = tuple(a - b for a, b in zip(rows[0], rows[1]))
    plus_count = coset_count(plus_cols)
    minus_count = coset_count(minus_cols)
    rectangle_edge = len(cols) == 6 and plus_count == 1 and minus_count == 1
    bdy = boundary(word)
    frob_invariant = word == frobenius_push(word)
    row_ok = (
        len(bdy) == 0
        and frob_invariant
        and pushforward(word, 3) == {}
        and pushforward(word, 13) == {}
        and set(word.values()) == {-6, 6}
        and (
            (is_diagonal and len(word) == 24 and len(cols) == 12 and plus_count == 2 and minus_count == 2)
            or ((not is_diagonal) and len(word) == 12 and len(cols) == 6 and rectangle_edge)
        )
    )
    return SplitProfile(
        name=name,
        numerator=numerator,
        denominator=denominator,
        support=len(word),
        coefficient_values=tuple(sorted(set(word.values()))),
        boundary_support=len(bdy),
        frobenius_invariant=frob_invariant,
        mod3_pushforward_zero=pushforward(word, 3) == {},
        mod13_pushforward_zero=pushforward(word, 13) == {},
        live_columns=len(cols),
        row1_plus_coset_count=plus_count,
        row1_minus_coset_count=minus_count,
        c4_antisym=antisym,
        is_diagonal_q_split=is_diagonal,
        is_one_coset_rectangle_edge=rectangle_edge,
        row_ok=row_ok,
    )


def routes() -> tuple[RouteRow, ...]:
    return (
        RouteRow(
            "q_split_value_only",
            "repair_boundary_zero_split_only",
            "Q diagonal aggregate and oriented root/direct one-edge theorem",
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_diagonal_plus_split_value_without_root",
            "repair_oriented_square_root_missing",
            "halving/root/orientation data after reaching twice one edge",
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_diagonal_plus_split_with_oriented_root",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            "same theorem data after explicit oriented split/root normalization",
            normalize=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "support12_quotient_used_as_q_diagonal_split",
            "reject_wrong_split_for_q_diagonal",
            "support-12 row quotients are not m1-m4 or m2-m8",
            normalize=False,
            repair=False,
            reject=True,
            ok=True,
        ),
        RouteRow(
            "one_axis_or_one_coset_q_split_shortcut",
            "reject_q_split_not_axis_or_one_coset",
            "diagonal Q splits use all twelve mod-13 columns",
            normalize=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_complexity() -> QSplitQuotientComplexity:
    markers = evidence_markers()
    diagonal = tuple(profile(f"q{a}_{b}", a, b, True) for a, b in DIAGONAL_SPLITS)
    controls = tuple(profile(f"q{a}_{b}", a, b, False) for a, b in NON_DIAGONAL_QUOTIENTS)
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    diagonal_support24 = sum(row.support == 24 for row in diagonal)
    diagonal_all_columns = sum(row.live_columns == 12 for row in diagonal)
    support12_nondiagonal = sum(row.support == 12 and not row.is_diagonal_q_split for row in controls)
    normalize_count = sum(row.normalize for row in route_rows)
    repair_count = sum(row.repair for row in route_rows)
    reject_count = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    expected_antisym = ((36, -36, -36, 36), (-36, -36, 36, 36))
    expected_decisions = (
        "repair_boundary_zero_split_only",
        "repair_oriented_square_root_missing",
        "normalize_to_one_edge_then_apply_source_snippet_intake",
        "reject_wrong_split_for_q_diagonal",
        "reject_q_split_not_axis_or_one_coset",
    )
    row_ok = (
        evidence_ok == len(markers)
        and len(diagonal) == 2
        and all(row.row_ok for row in diagonal)
        and tuple(row.c4_antisym for row in diagonal) == expected_antisym
        and diagonal_support24 == 2
        and diagonal_all_columns == 2
        and len(controls) == 4
        and all(row.row_ok for row in controls)
        and support12_nondiagonal == 4
        and tuple(row.decision for row in route_rows) == expected_decisions
        and normalize_count == 1
        and repair_count == 2
        and reject_count == 2
        and current_source_theorems == 0
    )
    return QSplitQuotientComplexity(
        evidence_markers=markers,
        diagonal_splits=diagonal,
        support12_controls=controls,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        diagonal_split_count=len(diagonal),
        diagonal_support24_count=diagonal_support24,
        diagonal_all_columns_count=diagonal_all_columns,
        support12_non_diagonal_count=support12_nondiagonal,
        normalize_routes=normalize_count,
        repair_rows=repair_count,
        reject_rows=reject_count,
        current_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_complexity()
    print("p25 v2 Q split quotient complexity")
    for marker_row in screen.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("diagonal_splits")
    for row in screen.diagonal_splits:
        print(
            f"  {row.name}: support={row.support} columns={row.live_columns} "
            f"coeffs={row.coefficient_values} boundary={row.boundary_support} "
            f"frob_invariant={int(row.frobenius_invariant)}"
        )
        print(
            f"    mod3_zero={int(row.mod3_pushforward_zero)} "
            f"mod13_zero={int(row.mod13_pushforward_zero)} "
            f"plus_cosets={row.row1_plus_coset_count} "
            f"minus_cosets={row.row1_minus_coset_count} "
            f"c4_antisym={row.c4_antisym}"
        )
    print("support12_controls")
    for row in screen.support12_controls:
        print(
            f"  {row.name}: support={row.support} diagonal_split={int(row.is_diagonal_q_split)} "
            f"rectangle_edge={int(row.is_one_coset_rectangle_edge)} c4_antisym={row.c4_antisym}"
        )
    print("routes")
    for row in screen.routes:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={screen.evidence_markers_ok}/{len(screen.evidence_markers)}")
    print(f"  diagonal_split_count={screen.diagonal_split_count}")
    print(f"  diagonal_support24_count={screen.diagonal_support24_count}")
    print(f"  diagonal_all_columns_count={screen.diagonal_all_columns_count}")
    print(f"  support12_non_diagonal_count={screen.support12_non_diagonal_count}")
    print(f"  normalize_routes={screen.normalize_routes}")
    print(f"  repair_rows={screen.repair_rows}")
    print(f"  reject_rows={screen.reject_rows}")
    print(f"  current_source_theorems={screen.current_source_theorems}")
    print(f"p25_v2_q_split_quotient_complexity_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
