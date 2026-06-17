#!/usr/bin/env python3
"""Diagonal aggregate relation among the four p25 rectangle rows.

The four legal rows are rectangle edges. This gate checks the diagonal product
relation m1*m4 = m2*m8 and classifies the resulting broad quadratic aggregate:
it has boundary 2W, so it is adjacent structure but not a first-pass closer for
the sparse W target.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path


P_MOD_39 = 23
COEFFICIENT = 6
LIFT_LENGTH = 13
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
class AggregateProfile:
    name: str
    multipliers: tuple[int, ...]
    support: int
    coefficient_values: tuple[int, ...]
    boundary_support: int
    boundary_coefficient_values: tuple[int, ...]
    boundary_scale_w: int | None
    payload_sha256: str
    row_ok: bool


@dataclass(frozen=True)
class AggregateDecision:
    name: str
    decision: str
    source_candidate_if_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RectangleDiagonalAggregate:
    evidence_markers: tuple[EvidenceMarker, ...]
    diagonal_m1_m4: AggregateProfile
    diagonal_m2_m8: AggregateProfile
    all_four: AggregateProfile
    diagonals_equal: bool
    all_four_is_double_diagonal: bool
    decisions: tuple[AggregateDecision, ...]
    evidence_markers_ok: int
    source_candidate_shapes: int
    repair_rows: int
    relation_rows: int
    current_source_stage_closers: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "quotient_h90_idempotent_mechanism",
            "research/p25/evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
    )


def row_word(multiplier: int) -> dict[int, int]:
    positive, negative = LEGAL_ROWS[multiplier]
    word: dict[int, int] = {}
    for residue in positive:
        word[residue] = word.get(residue, 0) + COEFFICIENT
    for residue in negative:
        word[residue] = word.get(residue, 0) - COEFFICIENT
    return normalize(word)


def normalize(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def add_words(*words: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for word in words:
        for residue, value in word.items():
            out[residue] = out.get(residue, 0) + value
    return normalize(out)


def scale_word(word: dict[int, int], scale: int) -> dict[int, int]:
    return normalize({residue: scale * value for residue, value in word.items()})


def frobenius_push(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        target = (P_MOD_39 * residue) % 39
        out[target] = out.get(target, 0) + value
    return normalize(out)


def subtract(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for residue, value in right.items():
        out[residue] = out.get(residue, 0) - value
    return normalize(out)


def boundary(word: dict[int, int]) -> dict[int, int]:
    return subtract(word, frobenius_push(word))


def coefficient_values(word: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(set(word.values())))


def lifted_hash(word: dict[int, int]) -> str:
    lines: list[str] = []
    for residue, value in word.items():
        for lift in range(LIFT_LENGTH):
            lines.append(f"{residue + 39 * lift}\t{value}")
    return sha256(("\n".join(sorted(lines)) + "\n").encode()).hexdigest()


def boundary_scale_against_w(word: dict[int, int], w: dict[int, int]) -> int | None:
    bdy = boundary(word)
    for scale in range(-8, 9):
        if bdy == scale_word(w, scale):
            return scale
    return None


def aggregate(name: str, multipliers: tuple[int, ...], w: dict[int, int]) -> AggregateProfile:
    word = add_words(*(row_word(multiplier) for multiplier in multipliers))
    bdy = boundary(word)
    scale = boundary_scale_against_w(word, w)
    return AggregateProfile(
        name=name,
        multipliers=multipliers,
        support=len(word),
        coefficient_values=coefficient_values(word),
        boundary_support=len(bdy),
        boundary_coefficient_values=coefficient_values(bdy),
        boundary_scale_w=scale,
        payload_sha256=lifted_hash(word),
        row_ok=True,
    )


def decisions() -> tuple[AggregateDecision, ...]:
    return (
        AggregateDecision(
            name="single_legal_row",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="finite value/divisor theorem plus downstream framing",
            ok=True,
        ),
        AggregateDecision(
            name="diagonal_pair_m1_m4",
            decision="repair_broad_quadratic_aggregate_boundary_2w",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="selector/factorization to one sparse edge with W boundary",
            ok=True,
        ),
        AggregateDecision(
            name="diagonal_pair_m2_m8",
            decision="repair_broad_quadratic_aggregate_boundary_2w",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="selector/factorization to one sparse edge with W boundary",
            ok=True,
        ),
        AggregateDecision(
            name="diagonal_identity_m1m4_equals_m2m8",
            decision="relation_not_source_close",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="arithmetic theorem for one sparse edge, not just the shared diagonal aggregate",
            ok=True,
        ),
        AggregateDecision(
            name="all_four_rows_product",
            decision="repair_overdemand_square_of_broad_quadratic",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="one legal support-156 row with W boundary is enough and still missing",
            ok=True,
        ),
    )


def build_profile() -> RectangleDiagonalAggregate:
    markers = evidence_markers()
    w = boundary(row_word(1))
    diag_14 = aggregate("diagonal_m1_m4", (1, 4), w)
    diag_28 = aggregate("diagonal_m2_m8", (2, 8), w)
    all_four = aggregate("all_four_rows", (1, 2, 4, 8), w)
    diagonal_equal = (
        add_words(row_word(1), row_word(4)) == add_words(row_word(2), row_word(8))
    )
    all_four_double = add_words(*(row_word(m) for m in (1, 2, 4, 8))) == scale_word(
        add_words(row_word(1), row_word(4)),
        2,
    )
    decision_rows = decisions()
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    repair_count = sum(row.decision.startswith("repair_") for row in decision_rows)
    relation_count = sum(row.decision == "relation_not_source_close" for row in decision_rows)
    current_closers = 0
    markers_ok = sum(row.ok for row in markers)
    row_ok = (
        markers_ok == len(markers)
        and len(w) == 24
        and coefficient_values(w) == (-6, 6)
        and diag_14.support == 24
        and diag_28.support == 24
        and diag_14.coefficient_values == (-6, 6)
        and diag_28.coefficient_values == (-6, 6)
        and diag_14.boundary_scale_w == 2
        and diag_28.boundary_scale_w == 2
        and diagonal_equal
        and all_four.support == 24
        and all_four.coefficient_values == (-12, 12)
        and all_four.boundary_scale_w == 4
        and all_four_double
        and len(decision_rows) == 5
        and source_candidates == 1
        and repair_count == 3
        and relation_count == 1
        and current_closers == 0
        and all(row.ok for row in decision_rows)
    )
    return RectangleDiagonalAggregate(
        evidence_markers=markers,
        diagonal_m1_m4=diag_14,
        diagonal_m2_m8=diag_28,
        all_four=all_four,
        diagonals_equal=diagonal_equal,
        all_four_is_double_diagonal=all_four_double,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        source_candidate_shapes=source_candidates,
        repair_rows=repair_count,
        relation_rows=relation_count,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def print_aggregate(row: AggregateProfile) -> None:
    print(
        "  "
        f"{row.name}: multipliers={row.multipliers} support={row.support} "
        f"coeffs={row.coefficient_values} boundary_support={row.boundary_support} "
        f"boundary_coeffs={row.boundary_coefficient_values} "
        f"boundary_scale_w={row.boundary_scale_w} sha256={row.payload_sha256}"
    )


def main() -> int:
    profile = build_profile()
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("aggregates")
    print_aggregate(profile.diagonal_m1_m4)
    print_aggregate(profile.diagonal_m2_m8)
    print_aggregate(profile.all_four)
    print("relations")
    print(f"  diagonals_equal={int(profile.diagonals_equal)}")
    print(f"  all_four_is_double_diagonal={int(profile.all_four_is_double_diagonal)}")
    print("decisions")
    for row in profile.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(
        f"  evidence_markers_ok={profile.evidence_markers_ok}/"
        f"{len(profile.evidence_markers)}"
    )
    print(f"  source_candidate_shapes={profile.source_candidate_shapes}")
    print(f"  repair_rows={profile.repair_rows}")
    print(f"  relation_rows={profile.relation_rows}")
    print(f"  current_source_stage_closers={profile.current_source_stage_closers}")
    print("interpretation")
    print("  diagonal_products_equal_broad_quadratic_aggregate=1")
    print("  broad_quadratic_aggregate_has_boundary_2W_not_W=1")
    print("  all_four_product_is_square_of_broad_quadratic_boundary_4W=1")
    print("  current_source_stage_closers_remain_zero=1")
    print(f"p25_v2_rectangle_diagonal_aggregate_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
