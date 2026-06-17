#!/usr/bin/env python3
"""Boundary-zero row quotient bridge for the p25 rectangle rows.

The rectangle diagonal aggregate shows that products of opposite rectangle
edges give a broad 2W-boundary object.  This gate checks the complementary
factorization data: quotients of legal rows have zero Hilbert-90 boundary, and
the diagonal quotient plus the diagonal aggregate recovers twice a legal row.

That is real structure, but not a source-stage close.  At value level it gives
a row square unless a source also supplies the missing halving/root/orientation
data, or directly proves the one-row value/divisor theorem.
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
class QuotientProfile:
    name: str
    numerator: int
    denominator: int
    support: int
    coefficient_values: tuple[int, ...]
    boundary_support: int
    frobenius_invariant: bool
    payload_sha256: str
    row_ok: bool


@dataclass(frozen=True)
class FactorizationProfile:
    name: str
    diagonal_pair: tuple[int, int]
    quotient_pair: tuple[int, int]
    recovered_row: int
    opposite_row: int
    plus_recovers_twice_row: bool
    minus_recovers_twice_opposite: bool
    recovered_support: int
    recovered_coefficients: tuple[int, ...]
    row_ok: bool


@dataclass(frozen=True)
class QuotientDecision:
    name: str
    decision: str
    source_candidate_if_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class RowQuotientInvariantBridge:
    evidence_markers: tuple[EvidenceMarker, ...]
    quotients: tuple[QuotientProfile, ...]
    factorizations: tuple[FactorizationProfile, ...]
    decisions: tuple[QuotientDecision, ...]
    evidence_markers_ok: int
    nontrivial_quotients: int
    boundary_zero_quotients: int
    row_square_bridges: int
    source_candidate_shapes: int
    repair_rows: int
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
            "row_orientation_reciprocal_normalizer",
            "research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
            "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
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


def add_words(*words: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for word in words:
        for residue, value in word.items():
            out[residue] = out.get(residue, 0) + value
    return normalize(out)


def scale_word(word: dict[int, int], scale: int) -> dict[int, int]:
    return normalize({residue: scale * value for residue, value in word.items()})


def subtract(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    return add_words(left, scale_word(right, -1))


def frobenius_push(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        target = (P_MOD_39 * residue) % 39
        out[target] = out.get(target, 0) + value
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


def quotient(numerator: int, denominator: int) -> QuotientProfile:
    word = subtract(row_word(numerator), row_word(denominator))
    bdy = boundary(word)
    invariant = word == frobenius_push(word)
    return QuotientProfile(
        name=f"q{numerator}_{denominator}",
        numerator=numerator,
        denominator=denominator,
        support=len(word),
        coefficient_values=coefficient_values(word),
        boundary_support=len(bdy),
        frobenius_invariant=invariant,
        payload_sha256=lifted_hash(word),
        row_ok=(len(bdy) == 0 and invariant),
    )


def factorization(
    name: str,
    left: int,
    right: int,
    recovered: int,
    opposite: int,
) -> FactorizationProfile:
    diagonal = add_words(row_word(left), row_word(right))
    quotient_word = subtract(row_word(recovered), row_word(opposite))
    plus = add_words(diagonal, quotient_word)
    minus = subtract(diagonal, quotient_word)
    twice_recovered = scale_word(row_word(recovered), 2)
    twice_opposite = scale_word(row_word(opposite), 2)
    plus_ok = plus == twice_recovered
    minus_ok = minus == twice_opposite
    return FactorizationProfile(
        name=name,
        diagonal_pair=(left, right),
        quotient_pair=(recovered, opposite),
        recovered_row=recovered,
        opposite_row=opposite,
        plus_recovers_twice_row=plus_ok,
        minus_recovers_twice_opposite=minus_ok,
        recovered_support=len(plus),
        recovered_coefficients=coefficient_values(plus),
        row_ok=plus_ok and minus_ok,
    )


def decisions() -> tuple[QuotientDecision, ...]:
    return (
        QuotientDecision(
            name="one_legal_row_theorem",
            decision="source_stage_candidate_if_theorem_present",
            source_candidate_if_theorem_present=True,
            first_missing_or_falsifier="finite value/divisor theorem plus downstream framing",
            ok=True,
        ),
        QuotientDecision(
            name="row_quotient_only",
            decision="repair_boundary_zero_quotient_only",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="one-row value/divisor theorem; quotient has zero H90 boundary",
            ok=True,
        ),
        QuotientDecision(
            name="diagonal_aggregate_plus_quotient",
            decision="repair_row_square_bridge_halving_missing",
            source_candidate_if_theorem_present=False,
            first_missing_or_falsifier="halving/root/orientation data selecting the legal row, or direct one-row theorem",
            ok=True,
        ),
    )


def build_bridge() -> RowQuotientInvariantBridge:
    markers = evidence_markers()
    quotient_rows = tuple(
        quotient(a, b)
        for a, b in ((1, 2), (1, 4), (1, 8), (2, 4), (2, 8), (4, 8))
    )
    factor_rows = (
        factorization("diagonal_m1_m4_with_q1_4", 1, 4, 1, 4),
        factorization("diagonal_m1_m4_with_q4_1", 1, 4, 4, 1),
        factorization("diagonal_m2_m8_with_q2_8", 2, 8, 2, 8),
        factorization("diagonal_m2_m8_with_q8_2", 2, 8, 8, 2),
    )
    decision_rows = decisions()
    markers_ok = sum(row.ok for row in markers)
    boundary_zero = sum(row.boundary_support == 0 and row.frobenius_invariant for row in quotient_rows)
    row_square_bridges = sum(row.plus_recovers_twice_row and row.minus_recovers_twice_opposite for row in factor_rows)
    source_candidates = sum(row.source_candidate_if_theorem_present for row in decision_rows)
    repair_count = sum(row.decision.startswith("repair_") for row in decision_rows)
    current_closers = 0
    support_profile = tuple(row.support for row in quotient_rows)
    row_ok = (
        markers_ok == len(markers)
        and len(quotient_rows) == 6
        and boundary_zero == 6
        and support_profile == (12, 24, 12, 12, 24, 12)
        and all(row.coefficient_values == (-6, 6) for row in quotient_rows)
        and all(row.row_ok for row in quotient_rows)
        and len(factor_rows) == 4
        and row_square_bridges == 4
        and all(row.recovered_support == 12 for row in factor_rows)
        and all(row.recovered_coefficients == (-12, 12) for row in factor_rows)
        and all(row.row_ok for row in factor_rows)
        and len(decision_rows) == 3
        and source_candidates == 1
        and repair_count == 2
        and current_closers == 0
        and all(row.ok for row in decision_rows)
    )
    return RowQuotientInvariantBridge(
        evidence_markers=markers,
        quotients=quotient_rows,
        factorizations=factor_rows,
        decisions=decision_rows,
        evidence_markers_ok=markers_ok,
        nontrivial_quotients=len(quotient_rows),
        boundary_zero_quotients=boundary_zero,
        row_square_bridges=row_square_bridges,
        source_candidate_shapes=source_candidates,
        repair_rows=repair_count,
        current_source_stage_closers=current_closers,
        row_ok=row_ok,
    )


def main() -> int:
    bridge = build_bridge()
    for marker_row in bridge.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("quotients")
    for row in bridge.quotients:
        print(
            "  "
            f"{row.name}: pair=({row.numerator},{row.denominator}) "
            f"support={row.support} coeffs={row.coefficient_values} "
            f"boundary_support={row.boundary_support} "
            f"frob_invariant={int(row.frobenius_invariant)} "
            f"sha256={row.payload_sha256}"
        )
    print("factorizations")
    for row in bridge.factorizations:
        print(
            "  "
            f"{row.name}: diagonal={row.diagonal_pair} quotient={row.quotient_pair} "
            f"plus_recovers_2row={int(row.plus_recovers_twice_row)} "
            f"minus_recovers_2opposite={int(row.minus_recovers_twice_opposite)} "
            f"support={row.recovered_support} coeffs={row.recovered_coefficients}"
        )
    print("decisions")
    for row in bridge.decisions:
        print(
            "  "
            f"{row.name}: decision={row.decision} "
            f"source_candidate={int(row.source_candidate_if_theorem_present)}"
        )
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={bridge.evidence_markers_ok}/{len(bridge.evidence_markers)}")
    print(f"  nontrivial_quotients={bridge.nontrivial_quotients}")
    print(f"  boundary_zero_quotients={bridge.boundary_zero_quotients}")
    print(f"  row_square_bridges={bridge.row_square_bridges}")
    print(f"  source_candidate_shapes={bridge.source_candidate_shapes}")
    print(f"  repair_rows={bridge.repair_rows}")
    print(f"  current_source_stage_closers={bridge.current_source_stage_closers}")
    print("interpretation")
    print("  row_quotients_are_frobenius_invariant_boundary_zero=1")
    print("  diagonal_aggregate_plus_quotient_recovers_twice_one_row=1")
    print("  quotient_or_square_bridge_alone_is_not_source_close=1")
    print(f"p25_v2_row_quotient_invariant_bridge_rows={int(bridge.row_ok)}/1")
    return 0 if bridge.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
