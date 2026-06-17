#!/usr/bin/env python3
"""Screen aggregate distribution relations against the p25 row target.

The first-pass source target is one oriented edge in the quotient-C4 K_{2,2}
graph, hence a coefficient vector with boundary scale 1 in the edge basis
(m1, m2, m4, m8).  This gate checks the common distribution/norm relation
shapes that appear in the nearby literature and in our local p25 artifacts:
vertex sums, opposite-edge diagonals, all-four aggregates, and boundary-zero
quotients.  Their integer closure has even boundary scale, so it cannot itself
produce one legal W-boundary row.  Rational reconstruction reaches a row only
after division by 2 or 4, which is exactly the already-recorded root/selector
debt.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd
from pathlib import Path
from functools import reduce


Vector = tuple[int, int, int, int]
RationalVector = tuple[Fraction, Fraction, Fraction, Fraction]

EDGE_ORDER = (1, 2, 4, 8)
UNIT_EDGE_M1: Vector = (1, 0, 0, 0)

COMMON_DISTRIBUTION_GENERATORS: tuple[tuple[str, Vector], ...] = (
    ("odd_vertex_7H_sum_m1_m2", (1, 1, 0, 0)),
    ("odd_vertex_2H_sum_m4_m8", (0, 0, 1, 1)),
    ("even_vertex_H_sum_m2_m4", (0, 1, 1, 0)),
    ("even_vertex_4H_sum_m1_m8", (1, 0, 0, 1)),
    ("opposite_diagonal_m1_m4", (1, 0, 1, 0)),
    ("opposite_diagonal_m2_m8", (0, 1, 0, 1)),
    ("all_four_norm", (1, 1, 1, 1)),
)

BOUNDARY_ZERO_GENERATORS: tuple[tuple[str, Vector], ...] = (
    ("m2_minus_m1", (-1, 1, 0, 0)),
    ("m4_minus_m1", (-1, 0, 1, 0)),
    ("m8_minus_m1", (-1, 0, 0, 1)),
    ("m1_minus_m4", (1, 0, -1, 0)),
    ("m2_minus_m8", (0, 1, 0, -1)),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class RelationRow:
    name: str
    vector: Vector
    boundary_scale: int
    l1_norm: int
    is_unit_edge: bool
    is_boundary_zero: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class ReconstructionRow:
    name: str
    formula_terms: tuple[tuple[str, int, Vector], ...]
    numerator: Vector
    denominator: int
    normalized_vector: RationalVector
    recovers_unit_edge: bool
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class DistributionClosureScreen:
    evidence_markers: tuple[EvidenceMarker, ...]
    relation_rows: tuple[RelationRow, ...]
    reconstruction_rows: tuple[ReconstructionRow, ...]
    distribution_generators_even_boundary: bool
    zero_boundary_generators_ok: bool
    integer_closure_can_have_boundary_one: bool
    direct_edge_rows: int
    aggregate_or_distribution_rows: int
    zero_boundary_rows: int
    root_or_selector_repair_rows: int
    current_distribution_source_closers: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name, marker_path, needle, needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "edge_lattice_global_minimality",
            "research/p25/evidence/p25_v2_edge_lattice_global_minimality_20260616.md",
            "p25_v2_edge_lattice_global_minimality_rows=1/1",
        ),
        marker(
            "row_value_reconstruction_basis",
            "research/p25/evidence/p25_v2_row_value_reconstruction_basis_20260617.md",
            "p25_v2_row_value_reconstruction_basis_rows=1/1",
        ),
        marker(
            "q_split_quartic_selector",
            "research/p25/evidence/p25_v2_q_split_quartic_selector_20260616.md",
            "p25_v2_q_split_quartic_selector_rows=1/1",
        ),
        marker(
            "external_distribution_relation_scout",
            "research/p25/evidence/p25_v2_external_distribution_relation_scout_20260617.md",
            "p25_v2_external_distribution_relation_scout_rows=1/1",
        ),
    )


def add_vec(left: Vector, right: Vector) -> Vector:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def scale_vec(vector: Vector, scalar: int) -> Vector:
    return tuple(scalar * value for value in vector)  # type: ignore[return-value]


def boundary_scale(vector: Vector) -> int:
    return sum(vector)


def l1_norm(vector: Vector) -> int:
    return sum(abs(value) for value in vector)


def is_unit_edge(vector: Vector) -> bool:
    return vector in {
        (1, 0, 0, 0),
        (0, 1, 0, 0),
        (0, 0, 1, 0),
        (0, 0, 0, 1),
    }


def lcm(left: int, right: int) -> int:
    return abs(left * right) // gcd(left, right)


def denominator(vector: RationalVector) -> int:
    return reduce(lcm, (entry.denominator for entry in vector), 1)


def relation_row(
    name: str,
    vector: Vector,
    decision: str,
    first_missing_or_falsifier: str,
) -> RelationRow:
    scale = boundary_scale(vector)
    unit = is_unit_edge(vector)
    zero = scale == 0
    ok = (
        (decision == "source_stage_candidate_if_source_theorem_present" and unit and scale == 1)
        or (decision == "repair_even_boundary_aggregate" and scale % 2 == 0 and scale > 0 and not unit)
        or (decision == "transfer_boundary_zero_only" and zero and not unit)
    )
    return RelationRow(
        name=name,
        vector=vector,
        boundary_scale=scale,
        l1_norm=l1_norm(vector),
        is_unit_edge=unit,
        is_boundary_zero=zero,
        decision=decision,
        first_missing_or_falsifier=first_missing_or_falsifier,
        ok=ok,
    )


def relation_rows() -> tuple[RelationRow, ...]:
    rows: list[RelationRow] = [
        relation_row(
            "direct_oriented_edge_theorem",
            UNIT_EDGE_M1,
            "source_stage_candidate_if_source_theorem_present",
            "the arithmetic finite value/divisor/additive theorem is absent",
        )
    ]
    rows.extend(
        relation_row(
            name,
            vector,
            "repair_even_boundary_aggregate",
            "even W-boundary aggregate needs selector/root or a direct one-edge theorem",
        )
        for name, vector in COMMON_DISTRIBUTION_GENERATORS
    )
    rows.extend(
        relation_row(
            name,
            vector,
            "transfer_boundary_zero_only",
            "boundary-zero relation has no scalar-fixed W-boundary row anchor",
        )
        for name, vector in BOUNDARY_ZERO_GENERATORS
    )
    return tuple(rows)


def reconstruct(
    name: str,
    terms: tuple[tuple[str, int, Vector], ...],
    denominator_value: int,
    decision: str,
    first_missing_or_falsifier: str,
) -> ReconstructionRow:
    numerator = (0, 0, 0, 0)
    for _, coefficient, vector in terms:
        numerator = add_vec(numerator, scale_vec(vector, coefficient))
    normalized = tuple(Fraction(value, denominator_value) for value in numerator)
    recovers = normalized == tuple(Fraction(value, 1) for value in UNIT_EDGE_M1)
    ok = recovers and denominator(normalized) == 1 and denominator_value in (2, 4)
    return ReconstructionRow(
        name=name,
        formula_terms=terms,
        numerator=numerator,
        denominator=denominator_value,
        normalized_vector=normalized,  # type: ignore[arg-type]
        recovers_unit_edge=recovers,
        decision=decision,
        first_missing_or_falsifier=first_missing_or_falsifier,
        ok=ok,
    )


def reconstruction_rows() -> tuple[ReconstructionRow, ...]:
    odd_sum = ("odd_vertex_7H_sum_m1_m2", 1, (1, 1, 0, 0))
    adjacent_diff = ("m1_minus_m2", 1, (1, -1, 0, 0))
    diagonal = ("opposite_diagonal_m1_m4", 1, (1, 0, 1, 0))
    diagonal_split = ("m1_minus_m4", 1, (1, 0, -1, 0))
    all_four = ("all_four_norm", 1, (1, 1, 1, 1))
    row_sign = ("odd_vertex_sign", 1, (1, 1, -1, -1))
    col_sign = ("even_vertex_sign", 1, (1, -1, -1, 1))
    c4_phase = ("quotient_c4_phase", 1, (1, -1, 1, -1))
    return (
        reconstruct(
            "vertex_sum_plus_boundary_zero_quotient",
            (odd_sum, adjacent_diff),
            2,
            "repair_square_root_or_direct_edge_theorem_missing",
            "aggregate plus quotient recovers 2*edge, not scalar-fixed edge",
        ),
        reconstruct(
            "diagonal_plus_quartic_split",
            (diagonal, diagonal_split),
            2,
            "repair_oriented_square_root_missing",
            "Q/diagonal split reaches 2*edge unless a source orients the root",
        ),
        reconstruct(
            "full_k22_projector_idempotent",
            (all_four, row_sign, col_sign, c4_phase),
            4,
            "repair_projector_denominator_missing",
            "projector isolates edge only after denominator/root/scalar data",
        ),
    )


def build_screen() -> DistributionClosureScreen:
    markers = evidence_markers()
    rows = relation_rows()
    recon = reconstruction_rows()
    generator_sums = [boundary_scale(vector) for _, vector in COMMON_DISTRIBUTION_GENERATORS]
    zero_sums = [boundary_scale(vector) for _, vector in BOUNDARY_ZERO_GENERATORS]
    distribution_even = all(scale % 2 == 0 for scale in generator_sums)
    zero_ok = all(scale == 0 for scale in zero_sums)
    integer_closure_can_have_boundary_one = not (distribution_even and zero_ok)
    direct_rows = sum(row.decision == "source_stage_candidate_if_source_theorem_present" for row in rows)
    aggregate_rows = sum(row.decision == "repair_even_boundary_aggregate" for row in rows)
    zero_rows = sum(row.decision == "transfer_boundary_zero_only" for row in rows)
    root_repairs = sum(row.decision.startswith("repair_") for row in recon)
    current_distribution_source_closers = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and len(rows) == 1 + len(COMMON_DISTRIBUTION_GENERATORS) + len(BOUNDARY_ZERO_GENERATORS)
        and all(row.ok for row in rows)
        and len(recon) == 3
        and all(row.ok for row in recon)
        and distribution_even
        and zero_ok
        and not integer_closure_can_have_boundary_one
        and direct_rows == 1
        and aggregate_rows == 7
        and zero_rows == 5
        and root_repairs == 3
        and current_distribution_source_closers == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return DistributionClosureScreen(
        evidence_markers=markers,
        relation_rows=rows,
        reconstruction_rows=recon,
        distribution_generators_even_boundary=distribution_even,
        zero_boundary_generators_ok=zero_ok,
        integer_closure_can_have_boundary_one=integer_closure_can_have_boundary_one,
        direct_edge_rows=direct_rows,
        aggregate_or_distribution_rows=aggregate_rows,
        zero_boundary_rows=zero_rows,
        root_or_selector_repair_rows=root_repairs,
        current_distribution_source_closers=current_distribution_source_closers,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_screen()
    print("p25 v2 distribution relation closure screen")
    print(f"edge_order={EDGE_ORDER}")
    for marker_row in screen.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("relation_rows")
    for row in screen.relation_rows:
        print(
            "  "
            f"{row.name}: vector={row.vector} boundary={row.boundary_scale} "
            f"l1={row.l1_norm} unit={int(row.is_unit_edge)} "
            f"zero={int(row.is_boundary_zero)} decision={row.decision}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("reconstruction_rows")
    for row in screen.reconstruction_rows:
        formula = " + ".join(
            f"{coefficient}*{name}" for name, coefficient, _ in row.formula_terms
        )
        print(
            "  "
            f"{row.name}: ({formula})/{row.denominator} -> "
            f"{tuple(str(value) for value in row.normalized_vector)} "
            f"recovers_unit={int(row.recovers_unit_edge)} decision={row.decision}"
        )
        print(f"    first_missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker_row.ok for marker_row in screen.evidence_markers)}/{len(screen.evidence_markers)}")
    print(f"distribution_generators_even_boundary={int(screen.distribution_generators_even_boundary)}")
    print(f"zero_boundary_generators_ok={int(screen.zero_boundary_generators_ok)}")
    print(f"integer_closure_can_have_boundary_one={int(screen.integer_closure_can_have_boundary_one)}")
    print(f"direct_edge_rows={screen.direct_edge_rows}")
    print(f"aggregate_or_distribution_rows={screen.aggregate_or_distribution_rows}")
    print(f"zero_boundary_rows={screen.zero_boundary_rows}")
    print(f"root_or_selector_repair_rows={screen.root_or_selector_repair_rows}")
    print(f"current_distribution_source_closers={screen.current_distribution_source_closers}")
    print(f"current_source_stage_closers={screen.current_source_stage_closers}")
    print(f"current_submission_ready={screen.current_submission_ready}")
    print("interpretation")
    print("  distribution_norm_closure_has_even_boundary_scale_only=1")
    print("  boundary_zero_quotients_are_transfer_not_row_anchor=1")
    print("  row_reconstruction_requires_division_by_2_or_4_root_selector_debt=1")
    print(f"p25_v2_distribution_relation_closure_screen_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
