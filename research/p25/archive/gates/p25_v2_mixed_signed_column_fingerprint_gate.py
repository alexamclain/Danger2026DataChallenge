#!/usr/bin/env python3
"""Mixed signed-column fingerprint for the p25 conductor-39 target.

The group-ring payload fixes four legal support-156 rows.  This lightweight
gate records a sharper mixed-tensor fingerprint of their conductor-39 source
potentials: each legal sparse row is a six-column signed matching in the
CRT grid C_3 x C_13, has zero proper pushforwards, and has the same
Hilbert-90 boundary W.  Formal one-coset gauges have the same boundary but fail
this fingerprint.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


CONDUCTOR = 39
P_MOD_39 = 23
COEFFICIENT = 6
UNITS_13 = tuple(range(1, 13))

LEGAL_ROWS = (
    (1, (3, 3, -3, -3), (7, 17, 23, 34, 37, 38), (4, 8, 10, 11, 20, 25)),
    (2, (-3, 3, 3, -3), (7, 14, 29, 34, 35, 37), (1, 8, 11, 16, 20, 22)),
    (4, (-3, -3, 3, 3), (14, 19, 28, 29, 31, 35), (1, 2, 5, 16, 22, 32)),
    (8, (3, -3, -3, 3), (17, 19, 23, 28, 31, 38), (2, 4, 5, 10, 25, 32)),
)

CANONICAL_W_POSITIVE = (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)
CANONICAL_W_NEGATIVE = (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class Column:
    mod13: int
    row_mod3_1: int
    row_mod3_2: int
    ok: bool


@dataclass(frozen=True)
class FingerprintRow:
    multiplier: int
    constants: tuple[int, int, int, int]
    positive: tuple[int, ...]
    negative: tuple[int, ...]
    support: int
    boundary_equals_w: bool
    pushforward_mod3: tuple[tuple[int, int], ...]
    pushforward_mod13: tuple[tuple[int, int], ...]
    proper_pushforwards_vanish: bool
    live_columns: tuple[Column, ...]
    live_column_count: int
    signed_column_count: int
    row1_positive_columns: tuple[int, ...]
    row1_negative_columns: tuple[int, ...]
    empty_column_count: int
    pullback_mod3: bool
    pullback_mod13: bool
    additive_separable: bool
    row_ok: bool


@dataclass(frozen=True)
class ControlRow:
    name: str
    support: int
    boundary_equals_w: bool
    pushforward_mod3: tuple[tuple[int, int], ...]
    pushforward_mod13: tuple[tuple[int, int], ...]
    signed_column_fingerprint: bool
    reject_as_formal_one_coset: bool
    row_ok: bool


@dataclass(frozen=True)
class MixedSignedColumnFingerprint:
    evidence_markers: tuple[EvidenceMarker, ...]
    legal_rows: tuple[FingerprintRow, ...]
    control_rows: tuple[ControlRow, ...]
    w_positive: tuple[int, ...]
    w_negative: tuple[int, ...]
    legal_rows_ok: int
    control_rows_ok: int
    all_rows_same_h90_boundary: bool
    all_rows_zero_proper_pushforwards: bool
    all_rows_six_signed_columns: bool
    formal_one_coset_controls_rejected: bool
    current_source_theorem_rows: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "unified_group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "conductor39_yang_h90_interface",
            "research/p25/evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md",
            "mixed tensor + coset selector + sparse Yang/H90 product",
        ),
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "current_source_stage_closers = 0",
        ),
    )


def nonzero(word: dict[int, int]) -> dict[int, int]:
    return dict(sorted((residue, value) for residue, value in word.items() if value))


def word_from_row(positive: tuple[int, ...], negative: tuple[int, ...]) -> dict[int, int]:
    word = {residue: COEFFICIENT for residue in positive}
    for residue in negative:
        word[residue] = -COEFFICIENT
    return dict(sorted(word.items()))


def w_word() -> dict[int, int]:
    return word_from_row(CANONICAL_W_POSITIVE, CANONICAL_W_NEGATIVE)


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


def pushforward(word: dict[int, int], modulus: int) -> tuple[tuple[int, int], ...]:
    out: dict[int, int] = {}
    for residue, value in word.items():
        out[residue % modulus] = out.get(residue % modulus, 0) + value
    return tuple(sorted((residue, value) for residue, value in out.items() if value))


def crt_mod3_mod13(mod3_value: int, mod13_value: int) -> int:
    for residue in range(CONDUCTOR):
        if residue % 3 == mod3_value and residue % 13 == mod13_value:
            return residue
    raise AssertionError("CRT search failed")


def normalized_value(word: dict[int, int], residue: int) -> int:
    value = word.get(residue, 0)
    if value % COEFFICIENT:
        raise AssertionError("unexpected coefficient")
    return value // COEFFICIENT


def columns(word: dict[int, int]) -> tuple[Column, ...]:
    rows: list[Column] = []
    for mod13_value in UNITS_13:
        row1 = normalized_value(word, crt_mod3_mod13(1, mod13_value))
        row2 = normalized_value(word, crt_mod3_mod13(2, mod13_value))
        if row1 or row2:
            rows.append(
                Column(
                    mod13=mod13_value,
                    row_mod3_1=row1,
                    row_mod3_2=row2,
                    ok=(row1, row2) in ((1, -1), (-1, 1)),
                )
            )
    return tuple(rows)


def is_pullback(word: dict[int, int], modulus: int) -> bool:
    residues = [residue for residue in range(CONDUCTOR) if gcd(residue, CONDUCTOR) == 1]
    for left in residues:
        for right in residues:
            if left < right and left % modulus == right % modulus:
                if word.get(left, 0) != word.get(right, 0):
                    return False
    return True


def additive_separable(word: dict[int, int]) -> bool:
    columns_full = [
        (
            normalized_value(word, crt_mod3_mod13(1, mod13_value)),
            normalized_value(word, crt_mod3_mod13(2, mod13_value)),
        )
        for mod13_value in UNITS_13
    ]
    differences = {row2 - row1 for row1, row2 in columns_full}
    return len(differences) == 1


def fingerprint_row(
    multiplier: int,
    constants: tuple[int, int, int, int],
    positive: tuple[int, ...],
    negative: tuple[int, ...],
) -> FingerprintRow:
    word = word_from_row(positive, negative)
    column_rows = columns(word)
    row1_pos = tuple(col.mod13 for col in column_rows if col.row_mod3_1 == 1)
    row1_neg = tuple(col.mod13 for col in column_rows if col.row_mod3_1 == -1)
    pf3 = pushforward(word, 3)
    pf13 = pushforward(word, 13)
    row_ok = (
        len(word) == 12
        and boundary(word) == w_word()
        and not pf3
        and not pf13
        and len(column_rows) == 6
        and sum(col.ok for col in column_rows) == 6
        and len(row1_pos) == 3
        and len(row1_neg) == 3
        and not is_pullback(word, 3)
        and not is_pullback(word, 13)
        and not additive_separable(word)
    )
    return FingerprintRow(
        multiplier=multiplier,
        constants=constants,
        positive=positive,
        negative=negative,
        support=len(word),
        boundary_equals_w=boundary(word) == w_word(),
        pushforward_mod3=pf3,
        pushforward_mod13=pf13,
        proper_pushforwards_vanish=not pf3 and not pf13,
        live_columns=column_rows,
        live_column_count=len(column_rows),
        signed_column_count=sum(col.ok for col in column_rows),
        row1_positive_columns=row1_pos,
        row1_negative_columns=row1_neg,
        empty_column_count=len(UNITS_13) - len(column_rows),
        pullback_mod3=is_pullback(word, 3),
        pullback_mod13=is_pullback(word, 13),
        additive_separable=additive_separable(word),
        row_ok=row_ok,
    )


def control_row(name: str, word: dict[int, int]) -> ControlRow:
    column_rows = columns(word)
    signed = len(column_rows) == 6 and all(col.ok for col in column_rows)
    pf3 = pushforward(word, 3)
    pf13 = pushforward(word, 13)
    boundary_ok = boundary(word) == w_word()
    reject = boundary_ok and (pf3 or pf13) and not signed
    return ControlRow(
        name=name,
        support=len(word),
        boundary_equals_w=boundary_ok,
        pushforward_mod3=pf3,
        pushforward_mod13=pf13,
        signed_column_fingerprint=signed,
        reject_as_formal_one_coset=reject,
        row_ok=reject,
    )


def build_profile() -> MixedSignedColumnFingerprint:
    markers = evidence_markers()
    rows = tuple(fingerprint_row(*row) for row in LEGAL_ROWS)
    controls = (
        control_row(
            "positive_one_coset_boundary_control",
            {residue: COEFFICIENT for residue in CANONICAL_W_POSITIVE},
        ),
        control_row(
            "negative_one_coset_boundary_control",
            {residue: -COEFFICIENT for residue in CANONICAL_W_NEGATIVE},
        ),
    )
    legal_ok = sum(row.row_ok for row in rows)
    control_ok = sum(row.row_ok for row in controls)
    markers_ok = sum(marker_row.ok for marker_row in markers)
    current_source_theorem_rows = 0
    row_ok = (
        markers_ok == len(markers)
        and legal_ok == 4
        and control_ok == 2
        and all(row.boundary_equals_w for row in rows)
        and all(row.proper_pushforwards_vanish for row in rows)
        and all(row.live_column_count == 6 and row.signed_column_count == 6 for row in rows)
        and all(row.reject_as_formal_one_coset for row in controls)
        and current_source_theorem_rows == 0
    )
    return MixedSignedColumnFingerprint(
        evidence_markers=markers,
        legal_rows=rows,
        control_rows=controls,
        w_positive=CANONICAL_W_POSITIVE,
        w_negative=CANONICAL_W_NEGATIVE,
        legal_rows_ok=legal_ok,
        control_rows_ok=control_ok,
        all_rows_same_h90_boundary=all(row.boundary_equals_w for row in rows),
        all_rows_zero_proper_pushforwards=all(row.proper_pushforwards_vanish for row in rows),
        all_rows_six_signed_columns=all(
            row.live_column_count == 6 and row.signed_column_count == 6 for row in rows
        ),
        formal_one_coset_controls_rejected=all(row.reject_as_formal_one_coset for row in controls),
        current_source_theorem_rows=current_source_theorem_rows,
        row_ok=row_ok,
    )


def main() -> int:
    profile = build_profile()
    print("p25 v2 mixed signed-column fingerprint gate")
    for marker_row in profile.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"W_positive={profile.w_positive}")
    print(f"W_negative={profile.w_negative}")
    print("legal_rows")
    for row in profile.legal_rows:
        live_columns = tuple(
            (col.mod13, col.row_mod3_1, col.row_mod3_2) for col in row.live_columns
        )
        print(
            "  "
            f"m={row.multiplier} constants={row.constants} support={row.support} "
            f"boundary={int(row.boundary_equals_w)} push3={row.pushforward_mod3} "
            f"push13={row.pushforward_mod13} live_columns={live_columns} "
            f"row1_plus={row.row1_positive_columns} row1_minus={row.row1_negative_columns} "
            f"empty_columns={row.empty_column_count} pullback3={int(row.pullback_mod3)} "
            f"pullback13={int(row.pullback_mod13)} additive_separable={int(row.additive_separable)} "
            f"ok={int(row.row_ok)}"
        )
    print("control_rows")
    for row in profile.control_rows:
        print(
            "  "
            f"{row.name}: support={row.support} boundary={int(row.boundary_equals_w)} "
            f"push3={row.pushforward_mod3} push13={row.pushforward_mod13} "
            f"signed_column_fingerprint={int(row.signed_column_fingerprint)} "
            f"reject={int(row.reject_as_formal_one_coset)} ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  legal_rows_ok={profile.legal_rows_ok}/4")
    print(f"  control_rows_ok={profile.control_rows_ok}/2")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  legal_rows_are_six_signed_C3_by_C13_columns=1")
    print("  legal_rows_have_zero_mod3_and_mod13_pushforwards=1")
    print("  legal_rows_share_the_same_H90_boundary_W=1")
    print("  formal_one_coset_boundary_controls_are_rejected=1")
    print("  still_missing_arithmetic_value_or_divisor_theorem=1")
    print(f"p25_v2_mixed_signed_column_fingerprint_rows={int(profile.row_ok)}/1")
    return 0 if profile.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
