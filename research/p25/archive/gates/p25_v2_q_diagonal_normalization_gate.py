#!/usr/bin/env python3
"""Projection-level diagonal normalization screen for the p25 Q route.

The compact conductor-39 quotient

    Q = prod_{h in <2>} E_{7h} / E_h

has useful Hilbert-90 boundary data after powering, but its quotient-C4
row-antisymmetric projection is not a single legal edge.  It is the same
diagonal aggregate seen by m1+m4 and m2+m8.  This gate records the exact
selector debt: a Q theorem still needs a boundary-zero split/orientation, an
oriented root, or a direct one-edge theorem before source-stage promotion.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MODULUS = 39
C4_COSETS = (
    (1, 3, 9),
    (2, 5, 6),
    (4, 10, 12),
    (7, 8, 11),
)
C4_LABELS = ("H", "2H", "4H", "7H")
EDGE_NAMES = (1, 2, 4, 8)
LEGAL_ROWS = {
    1: ((7, 17, 23, 34, 37, 38), (4, 8, 10, 11, 20, 25)),
    2: ((7, 14, 29, 34, 35, 37), (1, 8, 11, 16, 20, 22)),
    4: ((14, 19, 28, 29, 31, 35), (1, 2, 5, 16, 22, 32)),
    8: ((17, 19, 23, 28, 31, 38), (2, 4, 5, 10, 25, 32)),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ProjectionProfile:
    subgroup: tuple[int, ...]
    q_coset: tuple[int, ...]
    q_support: int
    q_row1: tuple[int, int, int, int]
    q_row2: tuple[int, int, int, int]
    q_antisym: tuple[int, int, int, int]
    edge_projections: dict[int, tuple[int, int, int, int]]
    q_equals_m1_plus_m4: bool
    q_equals_m2_plus_m8: bool
    row_ok: bool


@dataclass(frozen=True)
class SplitProfile:
    name: str
    diagonal_edges: tuple[int, int]
    diagonal_coefficients: tuple[int, int, int, int]
    split_coefficients: tuple[int, int, int, int]
    split_boundary_sum: int
    plus_recovers_twice_first: bool
    minus_recovers_twice_second: bool
    row_ok: bool


@dataclass(frozen=True)
class NormalizationRoute:
    name: str
    decision: str
    first_missing_or_falsifier: str
    source_candidate: bool
    support: bool
    normalize: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class QDiagonalNormalization:
    evidence_markers: tuple[EvidenceMarker, ...]
    projection: ProjectionProfile
    splits: tuple[SplitProfile, ...]
    routes: tuple[NormalizationRoute, ...]
    evidence_markers_ok: int
    diagonal_equalities: int
    boundary_zero_splits: int
    source_candidate_routes: int
    support_routes: int
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
            "q_route_selector_debt",
            "research/p25/evidence/p25_v2_q_route_selector_debt_20260616.md",
            "p25_v2_q_route_selector_debt_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
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
            "edge_lattice_global_minimality",
            "research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
            "p25_v2_edge_lattice_global_minimality_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
    )


def doubling_subgroup() -> tuple[int, ...]:
    values: list[int] = []
    current = 1
    while current not in values:
        values.append(current)
        current = (2 * current) % MODULUS
    return tuple(sorted(values))


def q_coset(subgroup: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted((7 * h) % MODULUS for h in subgroup))


def word_from_sets(
    positive: tuple[int, ...],
    negative: tuple[int, ...],
) -> dict[int, int]:
    word: dict[int, int] = {}
    for residue in positive:
        word[residue] = word.get(residue, 0) + 1
    for residue in negative:
        word[residue] = word.get(residue, 0) - 1
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def c4_index(residue: int) -> int:
    residue_mod_13 = residue % 13
    for index, coset in enumerate(C4_COSETS):
        if residue_mod_13 in coset:
            return index
    raise ValueError(f"residue {residue} is not prime to 13")


def row_vectors(word: dict[int, int]) -> tuple[tuple[int, int, int, int], tuple[int, int, int, int]]:
    rows = [[0, 0, 0, 0], [0, 0, 0, 0]]
    for residue, value in word.items():
        row_index = 0 if residue % 3 == 1 else 1
        rows[row_index][c4_index(residue)] += value
    return (tuple(rows[0]), tuple(rows[1]))


def subtract_vec(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(a - b for a, b in zip(left, right))


def add_vec(
    left: tuple[int, int, int, int],
    right: tuple[int, int, int, int],
) -> tuple[int, int, int, int]:
    return tuple(a + b for a, b in zip(left, right))


def scale_vec(vec: tuple[int, int, int, int], scale: int) -> tuple[int, int, int, int]:
    return tuple(scale * value for value in vec)


def legal_edge_projection(edge: int) -> tuple[int, int, int, int]:
    positive, negative = LEGAL_ROWS[edge]
    row1, row2 = row_vectors(word_from_sets(positive, negative))
    return subtract_vec(row1, row2)


def build_projection() -> ProjectionProfile:
    subgroup = doubling_subgroup()
    coset = q_coset(subgroup)
    q_word = word_from_sets(coset, subgroup)
    q_row1, q_row2 = row_vectors(q_word)
    q_antisym = subtract_vec(q_row1, q_row2)
    edge_projections = {edge: legal_edge_projection(edge) for edge in EDGE_NAMES}
    q_equals_m1_plus_m4 = q_antisym == add_vec(edge_projections[1], edge_projections[4])
    q_equals_m2_plus_m8 = q_antisym == add_vec(edge_projections[2], edge_projections[8])
    row_ok = (
        subgroup == (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)
        and coset == (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)
        and len(q_word) == 24
        and q_row1 == (-3, 3, -3, 3)
        and q_row2 == (3, -3, 3, -3)
        and q_antisym == (-6, 6, -6, 6)
        and edge_projections[1] == (0, 0, -6, 6)
        and edge_projections[2] == (-6, 0, 0, 6)
        and edge_projections[4] == (-6, 6, 0, 0)
        and edge_projections[8] == (0, 6, -6, 0)
        and q_equals_m1_plus_m4
        and q_equals_m2_plus_m8
    )
    return ProjectionProfile(
        subgroup=subgroup,
        q_coset=coset,
        q_support=len(q_word),
        q_row1=q_row1,
        q_row2=q_row2,
        q_antisym=q_antisym,
        edge_projections=edge_projections,
        q_equals_m1_plus_m4=q_equals_m1_plus_m4,
        q_equals_m2_plus_m8=q_equals_m2_plus_m8,
        row_ok=row_ok,
    )


def coefficient_vector(edge: int) -> tuple[int, int, int, int]:
    return tuple(1 if candidate == edge else 0 for candidate in EDGE_NAMES)


def split_profile(name: str, first: int, second: int) -> SplitProfile:
    first_vec = coefficient_vector(first)
    second_vec = coefficient_vector(second)
    diagonal = add_vec(first_vec, second_vec)
    split = subtract_vec(first_vec, second_vec)
    plus = add_vec(diagonal, split)
    minus = subtract_vec(diagonal, split)
    row_ok = (
        sum(split) == 0
        and plus == scale_vec(first_vec, 2)
        and minus == scale_vec(second_vec, 2)
    )
    return SplitProfile(
        name=name,
        diagonal_edges=(first, second),
        diagonal_coefficients=diagonal,
        split_coefficients=split,
        split_boundary_sum=sum(split),
        plus_recovers_twice_first=plus == scale_vec(first_vec, 2),
        minus_recovers_twice_second=minus == scale_vec(second_vec, 2),
        row_ok=row_ok,
    )


def routes() -> tuple[NormalizationRoute, ...]:
    return (
        NormalizationRoute(
            "q_diagonal_value_only",
            "support_diagonal_aggregate_selector_missing",
            "boundary-zero split/orientation data or direct one-edge theorem",
            source_candidate=False,
            support=True,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        NormalizationRoute(
            "q_plus_m1_m4_or_m2_m8_quotient_value",
            "repair_oriented_square_root_missing",
            "halving/root/orientation data after reaching twice one edge",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        NormalizationRoute(
            "q_plus_explicit_oriented_diagonal_split",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            "source-snippet intake and downstream extraction after scalar-fixed theorem",
            source_candidate=False,
            support=False,
            normalize=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        NormalizationRoute(
            "q_plus_direct_one_edge_theorem",
            "source_stage_candidate_if_scalar_fixed_theorem_present",
            "DANGER3 framing and extraction after theorem hit",
            source_candidate=True,
            support=False,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        NormalizationRoute(
            "q6_boundary_only",
            "repair_additive_or_value_normalization_missing",
            "scalar-fixed finite value/additive data plus selector, not just Hilbert-90 boundary",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        NormalizationRoute(
            "wrong_same_parity_or_zero_boundary_split",
            "reject_zero_boundary_wrong_edge",
            "split data must recover one of m1,m2,m4,m8 with the current oriented boundary",
            source_candidate=False,
            support=False,
            normalize=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_normalization() -> QDiagonalNormalization:
    markers = evidence_markers()
    projection = build_projection()
    split_rows = (
        split_profile("m1_m4_diagonal_split", 1, 4),
        split_profile("m2_m8_diagonal_split", 2, 8),
    )
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    diagonal_equalities = int(projection.q_equals_m1_plus_m4) + int(projection.q_equals_m2_plus_m8)
    boundary_zero_splits = sum(row.split_boundary_sum == 0 and row.row_ok for row in split_rows)
    source_candidates = sum(row.source_candidate for row in route_rows)
    support = sum(row.support for row in route_rows)
    normalize = sum(row.normalize for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    expected_decisions = (
        "support_diagonal_aggregate_selector_missing",
        "repair_oriented_square_root_missing",
        "normalize_to_one_edge_then_apply_source_snippet_intake",
        "source_stage_candidate_if_scalar_fixed_theorem_present",
        "repair_additive_or_value_normalization_missing",
        "reject_zero_boundary_wrong_edge",
    )
    row_ok = (
        evidence_ok == len(markers)
        and projection.row_ok
        and len(split_rows) == 2
        and all(row.row_ok for row in split_rows)
        and diagonal_equalities == 2
        and boundary_zero_splits == 2
        and tuple(row.decision for row in route_rows) == expected_decisions
        and source_candidates == 1
        and support == 1
        and normalize == 1
        and repairs == 2
        and rejects == 1
        and current_source_theorems == 0
        and all(row.ok for row in route_rows)
    )
    return QDiagonalNormalization(
        evidence_markers=markers,
        projection=projection,
        splits=split_rows,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        diagonal_equalities=diagonal_equalities,
        boundary_zero_splits=boundary_zero_splits,
        source_candidate_routes=source_candidates,
        support_routes=support,
        normalize_routes=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_normalization()
    projection = screen.projection
    print("p25 v2 Q diagonal normalization")
    for marker_row in screen.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("projection")
    print(f"  c4_labels={C4_LABELS}")
    print(f"  subgroup={projection.subgroup}")
    print(f"  q_coset={projection.q_coset}")
    print(f"  q_support={projection.q_support}")
    print(f"  q_row1={projection.q_row1}")
    print(f"  q_row2={projection.q_row2}")
    print(f"  q_antisym={projection.q_antisym}")
    for edge in EDGE_NAMES:
        print(f"  m{edge}_projection={projection.edge_projections[edge]}")
    print(f"  q_equals_m1_plus_m4={int(projection.q_equals_m1_plus_m4)}")
    print(f"  q_equals_m2_plus_m8={int(projection.q_equals_m2_plus_m8)}")
    print("splits")
    for split in screen.splits:
        print(f"  {split.name}: diagonal={split.diagonal_coefficients} split={split.split_coefficients}")
        print(f"    split_boundary_sum={split.split_boundary_sum}")
        print(f"    plus_recovers_twice_first={int(split.plus_recovers_twice_first)}")
        print(f"    minus_recovers_twice_second={int(split.minus_recovers_twice_second)}")
    print("routes")
    for route in screen.routes:
        print(f"  {route.name}: decision={route.decision}")
        print(f"    missing_or_falsifier={route.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={screen.evidence_markers_ok}/{len(screen.evidence_markers)}")
    print(f"  diagonal_equalities={screen.diagonal_equalities}")
    print(f"  boundary_zero_splits={screen.boundary_zero_splits}")
    print(f"  source_candidate_routes={screen.source_candidate_routes}")
    print(f"  support_routes={screen.support_routes}")
    print(f"  normalize_routes={screen.normalize_routes}")
    print(f"  repair_rows={screen.repair_rows}")
    print(f"  reject_rows={screen.reject_rows}")
    print(f"  current_source_theorems={screen.current_source_theorems}")
    print(f"p25_v2_q_diagonal_normalization_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
