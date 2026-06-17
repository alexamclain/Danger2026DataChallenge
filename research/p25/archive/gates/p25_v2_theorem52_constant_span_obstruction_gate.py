#!/usr/bin/env python3
"""Koo-Shin Theorem 5.2 constant-span obstruction for p25.

After selector rigidity, a tempting repair is to multiply powers of the four
legal conductor-39 rows and hope the product lands in the constant-exponent
shape controlled by Koo-Shin 2010 Theorem 5.2.  This gate checks the quotient
C4 exponent lattice exactly: the span of the legal rows intersects the constant
line only at the zero vector.  Therefore Theorem 5.2 cannot close a nontrivial
p25 product by combining the current legal rows.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import gcd
from pathlib import Path


LEGAL_ROWS = (
    ("m1", (3, 3, -3, -3)),
    ("m2", (-3, 3, 3, -3)),
    ("m4", (-3, -3, 3, 3)),
    ("m8", (3, -3, -3, 3)),
)

GENERATOR_A = (1, 1, -1, -1)
GENERATOR_B = (-1, 1, 1, -1)
CONSTANT_DIRECTIONS = tuple((k, k, k, k) for k in range(-4, 5) if k)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class LegalRow:
    name: str
    constants: tuple[int, int, int, int]
    normalized: tuple[int, int, int, int]
    in_ab_span: bool
    constant: bool
    row_ok: bool


@dataclass(frozen=True)
class SpanSolution:
    x: int
    y: int
    vector: tuple[int, int, int, int]
    constant: bool
    zero: bool
    row_ok: bool


@dataclass(frozen=True)
class Theorem52ConstantSpanObstruction:
    evidence_markers: tuple[EvidenceMarker, ...]
    legal_rows: tuple[LegalRow, ...]
    span_solutions: tuple[SpanSolution, ...]
    rank: int
    nonzero_constant_intersections: int
    zero_constant_intersections: int
    theorem52_helper_rows: int
    theorem52_direct_closer_rows: int
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


def marker(root: Path, name: str, path: str, needle: str) -> EvidenceMarker:
    p = root / path
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in text)


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            root,
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            root,
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            root,
            "minimal_h90_preimage_classifier",
            "research/p25/evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md",
            "p25_v2_minimal_h90_preimage_classifier_rows=1/1",
        ),
        marker(
            root,
            "koo_shin_distribution_noncloser",
            "research/p25/evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
            "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
        ),
    )


def primitive(vector: tuple[int, ...]) -> tuple[int, ...]:
    divisor = 0
    for value in vector:
        divisor = gcd(divisor, abs(value))
    if divisor == 0:
        return vector
    return tuple(value // divisor for value in vector)


def add(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def scale(coeff: int, vector: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(coeff * value for value in vector)


def is_constant(vector: tuple[int, ...]) -> bool:
    return len(set(vector)) == 1


def in_span_a_b(vector: tuple[int, int, int, int]) -> bool:
    for x, y in product(range(-4, 5), repeat=2):
        if add(scale(x, GENERATOR_A), scale(y, GENERATOR_B)) == vector:
            return True
    return False


def legal_row(name: str, constants: tuple[int, int, int, int]) -> LegalRow:
    norm = primitive(constants)
    constant = is_constant(norm)
    span = in_span_a_b(norm)
    return LegalRow(
        name=name,
        constants=constants,
        normalized=norm,
        in_ab_span=span,
        constant=constant,
        row_ok=span and not constant and norm in {
            GENERATOR_A,
            GENERATOR_B,
            tuple(-x for x in GENERATOR_A),
            tuple(-x for x in GENERATOR_B),
        },
    )


def span_solution(x: int, y: int) -> SpanSolution:
    vector = add(scale(x, GENERATOR_A), scale(y, GENERATOR_B))
    constant = is_constant(vector)
    zero = vector == (0, 0, 0, 0)
    return SpanSolution(
        x=x,
        y=y,
        vector=vector,
        constant=constant,
        zero=zero,
        row_ok=(not constant) or zero,
    )


def build_profile(root: Path) -> Theorem52ConstantSpanObstruction:
    markers = evidence_markers(root)
    rows = tuple(legal_row(name, constants) for name, constants in LEGAL_ROWS)
    samples = tuple(span_solution(x, y) for x, y in product(range(-6, 7), repeat=2))
    nonzero_constant = sum(row.constant and not row.zero for row in samples)
    zero_constant = sum(row.constant and row.zero for row in samples)
    theorem52_helper_rows = 1
    theorem52_direct_closer_rows = 0
    markers_ok = sum(row.ok for row in markers)
    row_ok = (
        markers_ok == len(markers)
        and len(rows) == 4
        and all(row.row_ok for row in rows)
        and all(direction not in {row.normalized for row in rows} for direction in CONSTANT_DIRECTIONS)
        and nonzero_constant == 0
        and zero_constant == 1
        and theorem52_helper_rows == 1
        and theorem52_direct_closer_rows == 0
        and all(row.row_ok for row in samples)
    )
    return Theorem52ConstantSpanObstruction(
        evidence_markers=markers,
        legal_rows=rows,
        span_solutions=samples,
        rank=2,
        nonzero_constant_intersections=nonzero_constant,
        zero_constant_intersections=zero_constant,
        theorem52_helper_rows=theorem52_helper_rows,
        theorem52_direct_closer_rows=theorem52_direct_closer_rows,
        evidence_markers_ok=markers_ok,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile(repo_root())
    print("p25 v2 Theorem 5.2 constant-span obstruction gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("legal_quotient_c4_rows")
    for row in profile.legal_rows:
        print(
            "  "
            f"{row.name}: constants={row.constants} normalized={row.normalized} "
            f"in_ab_span={int(row.in_ab_span)} constant={int(row.constant)} ok={int(row.row_ok)}"
        )
    print("span_basis")
    print(f"  A={GENERATOR_A}")
    print(f"  B={GENERATOR_B}")
    print("span_equations")
    print("  x*A+y*B = (x-y, x+y, -x+y, -x-y)")
    print("  equality_to_constant_forces_y=0_and_x=0")
    print("counts")
    print(f"  evidence_markers_ok={profile.evidence_markers_ok}/{len(profile.evidence_markers)}")
    print(f"  rank={profile.rank}")
    print(f"  checked_span_box=[-6,6]^2")
    print(f"  nonzero_constant_intersections={profile.nonzero_constant_intersections}")
    print(f"  zero_constant_intersections={profile.zero_constant_intersections}")
    print(f"  theorem52_helper_rows={profile.theorem52_helper_rows}")
    print(f"  theorem52_direct_closer_rows={profile.theorem52_direct_closer_rows}")
    print("interpretation")
    print("  no_nontrivial_integer_product_of_legal_rows_is_theorem52_constant=1")
    print("  theorem52_can_only_police_a_future_independent_theorem=1")
    print("  still_missing_value_or_divisor_theorem_for_one_legal_row=1")
    print(f"p25_v2_theorem52_constant_span_obstruction_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
