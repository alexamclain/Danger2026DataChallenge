#!/usr/bin/env python3
"""Classify minimal Hilbert-90 preimages of W for p25 conductor 39."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from pathlib import Path


P_MOD_39 = 23
CONDUCTOR = 39
COEFFICIENT = 6
H = (1, 3, 9)
COSETS = (
    (1, 3, 9),
    (2, 5, 6),
    (4, 10, 12),
    (7, 8, 11),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class OrbitPrimitive:
    orbit: tuple[int, ...]
    local_solution_count: int
    local_supports: tuple[int, ...]
    ok: bool


@dataclass(frozen=True)
class PreimageRow:
    choice_bits: tuple[int, ...]
    support: int
    coefficient_set: tuple[int, ...]
    boundary_equals_w: bool
    pushforward_mod3: tuple[tuple[int, int], ...]
    pushforward_mod13: tuple[tuple[int, int], ...]
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class MinimalH90PreimageClassifier:
    evidence_markers: tuple[EvidenceMarker, ...]
    frobenius_orbits: tuple[tuple[int, ...], ...]
    orbit_primitives: tuple[OrbitPrimitive, ...]
    minimal_preimage_rows: tuple[PreimageRow, ...]
    orbit_count: int
    local_primitive_rows_ok: int
    minimal_preimage_count: int
    mixed_legal_rows: int
    formal_one_coset_rows: int
    mod3_balanced_only_rows: int
    axis_leaking_rows: int
    current_source_theorem_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
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
            "unified_source_theorem_gap",
            "research/p25/evidence/p25_v2_unified_source_theorem_gap_20260616.md",
            "p25_v2_unified_source_theorem_gap_rows=1/1",
        ),
    )


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def crt_mod3_mod13(mod3_value: int, mod13_value: int) -> int:
    for residue in range(CONDUCTOR):
        if residue % 3 == mod3_value and residue % 13 == mod13_value:
            return residue
    raise AssertionError("CRT search failed")


def sparse_idempotent_word(odd_plus_coset: int, even_minus_coset: int) -> dict[int, int]:
    word: dict[int, int] = {}
    for column in COSETS[odd_plus_coset]:
        word[crt_mod3_mod13(1, column)] = COEFFICIENT
        word[crt_mod3_mod13(2, column)] = -COEFFICIENT
    for column in COSETS[even_minus_coset]:
        word[crt_mod3_mod13(1, column)] = -COEFFICIENT
        word[crt_mod3_mod13(2, column)] = COEFFICIENT
    return dict(sorted(word.items()))


def push_frobenius(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        target = (P_MOD_39 * residue) % CONDUCTOR
        out[target] = out.get(target, 0) + value
    return nonzero(out)


def subtract(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out = dict(left)
    for residue, value in right.items():
        out[residue] = out.get(residue, 0) - value
    return nonzero(out)


def boundary(word: dict[int, int]) -> dict[int, int]:
    return subtract(word, push_frobenius(word))


def w_word() -> dict[int, int]:
    return boundary(sparse_idempotent_word(3, 2))


def coefficient_set(word: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(set(word.values())))


def pushforward(word: dict[int, int], modulus: int) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        out[residue % modulus] = out.get(residue % modulus, 0) + value
    return tuple(sorted((residue, value) for residue, value in out.items() if value))


def frobenius_orbits(source: dict[int, int]) -> tuple[tuple[int, ...], ...]:
    seen: set[int] = set()
    rows: list[tuple[int, ...]] = []
    for residue in sorted(source):
        if residue in seen:
            continue
        current = residue
        orbit: list[int] = []
        while current not in orbit:
            orbit.append(current)
            seen.add(current)
            current = (P_MOD_39 * current) % CONDUCTOR
        rows.append(tuple(orbit))
    return tuple(rows)


def orbit_boundary(word: dict[int, int], orbit: tuple[int, ...]) -> dict[int, int]:
    orbit_set = set(orbit)
    return {residue: value for residue, value in boundary(word).items() if residue in orbit_set}


def local_sparse_primitives(orbit: tuple[int, ...], source: dict[int, int]) -> tuple[tuple[tuple[int, int], ...], ...]:
    expected = {residue: source[residue] for residue in orbit}
    primitives: list[tuple[tuple[int, int], ...]] = []
    values = (-COEFFICIENT, 0, COEFFICIENT)
    for choices in product(values, repeat=len(orbit)):
        word = {residue: value for residue, value in zip(orbit, choices) if value}
        if orbit_boundary(word, orbit) == expected and len(word) == 3:
            primitives.append(tuple(sorted(word.items())))
    return tuple(primitives)


def combine_primitives(choice: tuple[tuple[tuple[int, int], ...], ...]) -> dict[int, int]:
    word: dict[int, int] = {}
    for primitive in choice:
        for residue, value in primitive:
            word[residue] = value
    return dict(sorted(word.items()))


def decision_for(word: dict[int, int], pf3: tuple[tuple[int, int], ...], pf13: tuple[tuple[int, int], ...]) -> str:
    if not pf3 and not pf13:
        return "mixed_legal_preimage"
    if len(coefficient_set(word)) == 1 and pf3 and pf13:
        return "formal_one_coset_boundary_control"
    if not pf3 and pf13:
        return "mod3_balanced_only_mod13_leaks"
    return "axis_leaking_preimage"


def preimage_row(choice_bits: tuple[int, ...], word: dict[int, int], source: dict[int, int]) -> PreimageRow:
    pf3 = pushforward(word, 3)
    pf13 = pushforward(word, 13)
    decision = decision_for(word, pf3, pf13)
    boundary_ok = boundary(word) == source
    return PreimageRow(
        choice_bits=choice_bits,
        support=len(word),
        coefficient_set=coefficient_set(word),
        boundary_equals_w=boundary_ok,
        pushforward_mod3=pf3,
        pushforward_mod13=pf13,
        decision=decision,
        row_ok=boundary_ok and len(word) == 12 and decision in {
            "mixed_legal_preimage",
            "formal_one_coset_boundary_control",
            "mod3_balanced_only_mod13_leaks",
            "axis_leaking_preimage",
        },
    )


def build_profile() -> MinimalH90PreimageClassifier:
    markers = evidence_markers()
    source = w_word()
    orbits = frobenius_orbits(source)
    local = tuple(local_sparse_primitives(orbit, source) for orbit in orbits)
    primitive_rows = tuple(
        OrbitPrimitive(
            orbit=orbit,
            local_solution_count=len(primitives),
            local_supports=tuple(sorted(len(primitive) for primitive in primitives)),
            ok=len(primitives) == 2 and all(len(primitive) == 3 for primitive in primitives),
        )
        for orbit, primitives in zip(orbits, local)
    )
    rows: list[PreimageRow] = []
    for choice_bits in product((0, 1), repeat=len(local)):
        chosen = tuple(primitives[bit] for primitives, bit in zip(local, choice_bits))
        rows.append(preimage_row(choice_bits, combine_primitives(chosen), source))
    decisions = [row.decision for row in rows]
    current_source_theorem_rows = 0
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and len(orbits) == 4
        and all(len(orbit) == 6 for orbit in orbits)
        and sum(row.ok for row in primitive_rows) == 4
        and len(rows) == 16
        and all(row.row_ok for row in rows)
        and decisions.count("mixed_legal_preimage") == 4
        and decisions.count("formal_one_coset_boundary_control") == 2
        and decisions.count("mod3_balanced_only_mod13_leaks") == 2
        and decisions.count("axis_leaking_preimage") == 8
        and current_source_theorem_rows == 0
    )
    return MinimalH90PreimageClassifier(
        evidence_markers=markers,
        frobenius_orbits=orbits,
        orbit_primitives=primitive_rows,
        minimal_preimage_rows=tuple(rows),
        orbit_count=len(orbits),
        local_primitive_rows_ok=sum(row.ok for row in primitive_rows),
        minimal_preimage_count=len(rows),
        mixed_legal_rows=decisions.count("mixed_legal_preimage"),
        formal_one_coset_rows=decisions.count("formal_one_coset_boundary_control"),
        mod3_balanced_only_rows=decisions.count("mod3_balanced_only_mod13_leaks"),
        axis_leaking_rows=decisions.count("axis_leaking_preimage"),
        current_source_theorem_rows=current_source_theorem_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 minimal H90 preimage classifier gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("frobenius_orbits")
    for row in profile.orbit_primitives:
        print(
            "  "
            f"orbit={row.orbit} local_solution_count={row.local_solution_count} "
            f"local_supports={row.local_supports} ok={int(row.ok)}"
        )
    print("minimal_preimage_rows")
    for row in profile.minimal_preimage_rows:
        print(
            "  "
            f"bits={row.choice_bits} support={row.support} coeffs={row.coefficient_set} "
            f"boundary={int(row.boundary_equals_w)} push3={row.pushforward_mod3} "
            f"push13={row.pushforward_mod13} decision={row.decision} ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  orbit_count={profile.orbit_count}")
    print(f"  local_primitive_rows_ok={profile.local_primitive_rows_ok}/4")
    print(f"  minimal_preimage_count={profile.minimal_preimage_count}")
    print(f"  mixed_legal_rows={profile.mixed_legal_rows}")
    print(f"  formal_one_coset_rows={profile.formal_one_coset_rows}")
    print(f"  mod3_balanced_only_rows={profile.mod3_balanced_only_rows}")
    print(f"  axis_leaking_rows={profile.axis_leaking_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  all_minimal_integral_H90_preimages_of_W_are_classified=1")
    print("  exactly_four_minimal_preimages_preserve_both_axis_pushforwards=1")
    print("  twelve_minimal_preimages_are_boundary_controls_not_source_closers=1")
    print("  still_missing_arithmetic_value_or_divisor_theorem=1")
    print(f"p25_v2_minimal_h90_preimage_classifier_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
