#!/usr/bin/env python3
"""Quotient-C4 Hilbert-90 mechanism for the p25 conductor-39 rows."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


P_MOD_39 = 23
COEFFICIENT = 6
H = (1, 3, 9)
COSETS = (
    (1, 3, 9),
    (2, 5, 6),
    (4, 10, 12),
    (7, 8, 11),
)
ODD_COSET_IDS = (1, 3)
EVEN_COSET_IDS = (0, 2)
LEGAL_EDGES = (
    (1, 3, 2),
    (2, 3, 0),
    (4, 1, 0),
    (8, 1, 2),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class MechanismRow:
    multiplier: int
    odd_plus_coset: int
    even_minus_coset: int
    support: int
    boundary_equals_w: bool
    frobenius_plus_coset: int
    frobenius_minus_coset: int
    row_ok: bool


@dataclass(frozen=True)
class ControlRow:
    name: str
    support: int
    boundary_support: int
    boundary_coefficients: tuple[int, ...]
    boundary_equals_w: bool
    reject_reason: str
    row_ok: bool


@dataclass(frozen=True)
class QuotientH90IdempotentMechanism:
    evidence_markers: tuple[EvidenceMarker, ...]
    h_subgroup: tuple[int, ...]
    quotient_order: int
    frobenius_coset_shift: int
    frobenius_flips_mod3_row: bool
    w_support: int
    w_coefficients: tuple[int, ...]
    legal_rows: tuple[MechanismRow, ...]
    control_rows: tuple[ControlRow, ...]
    legal_rows_ok: int
    control_rows_ok: int
    odd_even_edges_exhausted: bool
    current_source_theorem_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            "mixed_signed_column_fingerprint",
            "research/p25/evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
            "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
        ),
        marker(
            "unified_value_divisor_interface",
            "research/p25/evidence/p25_v2_unified_value_divisor_interface_20260616.md",
            "p25_v2_unified_value_divisor_interface_rows=1/1",
        ),
    )


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def crt_mod3_mod13(mod3_value: int, mod13_value: int) -> int:
    for residue in range(39):
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


def broad_quadratic_word() -> dict[int, int]:
    word: dict[int, int] = {}
    for coset_id, coset in enumerate(COSETS):
        column_sign = 1 if coset_id in ODD_COSET_IDS else -1
        for column in coset:
            word[crt_mod3_mod13(1, column)] = COEFFICIENT * column_sign
            word[crt_mod3_mod13(2, column)] = -COEFFICIENT * column_sign
    return dict(sorted(word.items()))


def push_frobenius(word: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        target = (P_MOD_39 * residue) % 39
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


def multiply_coset(coset_id: int, multiplier_mod13: int) -> int:
    image = tuple(sorted((multiplier_mod13 * value) % 13 for value in COSETS[coset_id]))
    return COSETS.index(image)


def mechanism_row(multiplier: int, odd_plus_coset: int, even_minus_coset: int) -> MechanismRow:
    word = sparse_idempotent_word(odd_plus_coset, even_minus_coset)
    w = w_word()
    return MechanismRow(
        multiplier=multiplier,
        odd_plus_coset=odd_plus_coset,
        even_minus_coset=even_minus_coset,
        support=len(word),
        boundary_equals_w=boundary(word) == w,
        frobenius_plus_coset=multiply_coset(odd_plus_coset, P_MOD_39 % 13),
        frobenius_minus_coset=multiply_coset(even_minus_coset, P_MOD_39 % 13),
        row_ok=(
            len(word) == 12
            and odd_plus_coset in ODD_COSET_IDS
            and even_minus_coset in EVEN_COSET_IDS
            and boundary(word) == w
        ),
    )


def control_row(name: str, word: dict[int, int], reject_reason: str) -> ControlRow:
    bdy = boundary(word)
    return ControlRow(
        name=name,
        support=len(word),
        boundary_support=len(bdy),
        boundary_coefficients=coefficient_set(bdy),
        boundary_equals_w=bdy == w_word(),
        reject_reason=reject_reason,
        row_ok=bdy != w_word(),
    )


def build_profile() -> QuotientH90IdempotentMechanism:
    markers = evidence_markers()
    legal_rows = tuple(mechanism_row(*edge) for edge in LEGAL_EDGES)
    controls = (
        control_row(
            "same_parity_odd_odd",
            sparse_idempotent_word(1, 3),
            "same-parity cosets have zero Hilbert-90 boundary, not W",
        ),
        control_row(
            "same_parity_even_even",
            sparse_idempotent_word(0, 2),
            "same-parity cosets have zero Hilbert-90 boundary, not W",
        ),
        control_row(
            "broad_quadratic_character",
            broad_quadratic_word(),
            "pure quadratic character gives 2W and support 24, not the sparse W potential",
        ),
    )
    legal_ok = sum(row.row_ok for row in legal_rows)
    control_ok = sum(row.row_ok for row in controls)
    current_source_theorem_rows = 0
    w = w_word()
    row_ok = (
        sum(marker_row.ok for marker_row in markers) == len(markers)
        and H == (1, 3, 9)
        and len(COSETS) == 4
        and P_MOD_39 % 13 == 10
        and multiply_coset(0, P_MOD_39 % 13) == 2
        and P_MOD_39 % 3 == 2
        and legal_ok == 4
        and control_ok == 3
        and len(w) == 24
        and coefficient_set(w) == (-6, 6)
        and current_source_theorem_rows == 0
    )
    return QuotientH90IdempotentMechanism(
        evidence_markers=markers,
        h_subgroup=H,
        quotient_order=4,
        frobenius_coset_shift=2,
        frobenius_flips_mod3_row=P_MOD_39 % 3 == 2,
        w_support=len(w),
        w_coefficients=coefficient_set(w),
        legal_rows=legal_rows,
        control_rows=controls,
        legal_rows_ok=legal_ok,
        control_rows_ok=control_ok,
        odd_even_edges_exhausted={
            (row.odd_plus_coset, row.even_minus_coset) for row in legal_rows
        }
        == {(odd, even) for odd in ODD_COSET_IDS for even in EVEN_COSET_IDS},
        current_source_theorem_rows=current_source_theorem_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 quotient-H90 idempotent mechanism gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"H={profile.h_subgroup}")
    print(f"quotient_order={profile.quotient_order}")
    print(f"frobenius_coset_shift={profile.frobenius_coset_shift}")
    print(f"frobenius_flips_mod3_row={int(profile.frobenius_flips_mod3_row)}")
    print(f"W_support={profile.w_support}")
    print(f"W_coefficients={profile.w_coefficients}")
    print("legal_rows")
    for row in profile.legal_rows:
        print(
            "  "
            f"m={row.multiplier} odd_plus={row.odd_plus_coset} "
            f"even_minus={row.even_minus_coset} support={row.support} "
            f"boundary_equals_W={int(row.boundary_equals_w)} "
            f"frob_plus={row.frobenius_plus_coset} "
            f"frob_minus={row.frobenius_minus_coset} ok={int(row.row_ok)}"
        )
    print("control_rows")
    for row in profile.control_rows:
        print(
            "  "
            f"{row.name}: support={row.support} boundary_support={row.boundary_support} "
            f"boundary_coefficients={row.boundary_coefficients} "
            f"boundary_equals_W={int(row.boundary_equals_w)} "
            f"reject_reason={row.reject_reason} ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  legal_rows_ok={profile.legal_rows_ok}/4")
    print(f"  control_rows_ok={profile.control_rows_ok}/3")
    print(f"  odd_even_edges_exhausted={int(profile.odd_even_edges_exhausted)}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  frobenius_shift_by_two_plus_mod3_flip_explains_common_boundary=1")
    print("  legal_rows_are_sparse_odd_even_C4_idempotent_differences=1")
    print("  same_parity_edges_and_broad_quadratic_character_are_rejected=1")
    print("  still_missing_arithmetic_value_or_divisor_theorem=1")
    print(f"p25_v2_quotient_h90_idempotent_mechanism_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
