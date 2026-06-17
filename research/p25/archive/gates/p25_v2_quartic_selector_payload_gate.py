#!/usr/bin/env python3
"""Minimal quartic selector payload screen for the p25 edge target."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


GI = tuple[int, int]

C4_COSETS = ("H", "2H", "4H", "7H")
LEGAL_EDGES = (
    (1, "7H", "4H"),
    (2, "7H", "H"),
    (4, "2H", "H"),
    (8, "2H", "4H"),
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SelectorRow:
    multiplier: int
    plus_coset: str
    minus_coset: str
    row_antisymmetric: tuple[int, int, int, int]
    antisymmetric_dft: tuple[GI, GI, GI, GI]
    boundary_dft: tuple[GI, GI, GI, GI]
    quartic_selector: GI
    conjugate_selector: GI
    real_sign: int
    imag_sign: int
    selector_label: str
    row_ok: bool


@dataclass(frozen=True)
class CoarseSelector:
    name: str
    surviving_edges: tuple[int, ...]
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class Route:
    name: str
    provided_shape: str
    decision: str
    first_missing_or_falsifier: str
    source_stage_candidate: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class QuarticSelectorPayload:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SelectorRow, ...]
    coarse_selectors: tuple[CoarseSelector, ...]
    routes: tuple[Route, ...]
    evidence_markers_ok: int
    legal_rows_ok: int
    unique_quartic_selectors: int
    unique_boundaries: int
    coarse_selectors_ok: int
    accepted_routes: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "c4_character_spectrum",
            "research/p25/evidence/p25_v2_c4_character_spectrum_20260616.md",
            "p25_v2_c4_character_spectrum_rows=1/1",
        ),
        marker(
            "row_sign_c4_tensor_spectrum",
            "research/p25/evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md",
            "p25_v2_row_sign_c4_tensor_spectrum_rows=1/1",
        ),
        marker(
            "frobenius_tensor_eigenboundary",
            "research/p25/evidence/p25_v2_frobenius_tensor_eigenboundary_20260616.md",
            "p25_v2_frobenius_tensor_eigenboundary_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "partial_projector_selector",
            "research/p25/evidence/p25_v2_partial_projector_selector_20260616.md",
            "p25_v2_partial_projector_selector_rows=1/1",
        ),
        marker(
            "current_expert_response_rubric",
            "research/p25/evidence/p25_v2_current_expert_response_rubric_20260616.md",
            "current_source_stage_closers = 0",
        ),
    )


def gi_add(left: GI, right: GI) -> GI:
    return (left[0] + right[0], left[1] + right[1])


def gi_mul_int(value: GI, scalar: int) -> GI:
    return (value[0] * scalar, value[1] * scalar)


def i_power(exp: int) -> GI:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[exp % 4]


def dft(vector: tuple[int, int, int, int]) -> tuple[GI, GI, GI, GI]:
    out: list[GI] = []
    for character in range(4):
        total = (0, 0)
        for index, coefficient in enumerate(vector):
            total = gi_add(total, gi_mul_int(i_power(-character * index), coefficient))
        out.append(total)
    return tuple(out)  # type: ignore[return-value]


def edge_vector(plus_coset: str, minus_coset: str) -> tuple[int, int, int, int]:
    values = [0, 0, 0, 0]
    values[C4_COSETS.index(plus_coset)] = 1
    values[C4_COSETS.index(minus_coset)] = -1
    return tuple(values)  # type: ignore[return-value]


def sign(value: int) -> int:
    if value < 0:
        return -1
    if value > 0:
        return 1
    return 0


def selector_label(value: GI) -> str:
    real, imag = value
    return ("R+" if real > 0 else "R-") + ("I+" if imag > 0 else "I-")


def selector_rows() -> tuple[SelectorRow, ...]:
    rows: list[SelectorRow] = []
    boundary = ((0, 0), (0, 0), (-8, 0), (0, 0))
    for multiplier, plus_coset, minus_coset in LEGAL_EDGES:
        row1 = edge_vector(plus_coset, minus_coset)
        row2 = tuple(-value for value in row1)
        row_antisymmetric = tuple(a - b for a, b in zip(row1, row2))
        anti_dft = dft(row_antisymmetric)  # type: ignore[arg-type]
        quartic = anti_dft[1]
        conjugate = anti_dft[3]
        row_ok = (
            anti_dft[0] == (0, 0)
            and anti_dft[2] == (-4, 0)
            and quartic[0] in {-2, 2}
            and quartic[1] in {-2, 2}
            and conjugate == (quartic[0], -quartic[1])
            and selector_label(quartic) in {"R+I+", "R-I+", "R-I-", "R+I-"}
        )
        rows.append(
            SelectorRow(
                multiplier=multiplier,
                plus_coset=plus_coset,
                minus_coset=minus_coset,
                row_antisymmetric=row_antisymmetric,  # type: ignore[arg-type]
                antisymmetric_dft=anti_dft,
                boundary_dft=boundary,  # type: ignore[arg-type]
                quartic_selector=quartic,
                conjugate_selector=conjugate,
                real_sign=sign(quartic[0]),
                imag_sign=sign(quartic[1]),
                selector_label=selector_label(quartic),
                row_ok=row_ok,
            )
        )
    return tuple(rows)


def coarse_selectors(rows: tuple[SelectorRow, ...]) -> tuple[CoarseSelector, ...]:
    by_real_pos = tuple(row.multiplier for row in rows if row.real_sign > 0)
    by_real_neg = tuple(row.multiplier for row in rows if row.real_sign < 0)
    by_imag_pos = tuple(row.multiplier for row in rows if row.imag_sign > 0)
    by_imag_neg = tuple(row.multiplier for row in rows if row.imag_sign < 0)
    by_abs = tuple(row.multiplier for row in rows if abs(row.quartic_selector[0]) == 2 and abs(row.quartic_selector[1]) == 2)
    rows_out = (
        CoarseSelector(
            name="real_sign_positive_only",
            surviving_edges=by_real_pos,
            decision="repair_two_edge_column_pair",
            row_ok=by_real_pos == (1, 8),
        ),
        CoarseSelector(
            name="real_sign_negative_only",
            surviving_edges=by_real_neg,
            decision="repair_two_edge_column_pair",
            row_ok=by_real_neg == (2, 4),
        ),
        CoarseSelector(
            name="imag_sign_positive_only",
            surviving_edges=by_imag_pos,
            decision="repair_two_edge_row_pair",
            row_ok=by_imag_pos == (1, 2),
        ),
        CoarseSelector(
            name="imag_sign_negative_only",
            surviving_edges=by_imag_neg,
            decision="repair_two_edge_row_pair",
            row_ok=by_imag_neg == (4, 8),
        ),
        CoarseSelector(
            name="quartic_magnitude_only",
            surviving_edges=by_abs,
            decision="repair_all_four_edges",
            row_ok=by_abs == (1, 2, 4, 8),
        ),
    )
    return rows_out


def routes() -> tuple[Route, ...]:
    return (
        Route(
            name="boundary_plus_exact_quartic_selector_value",
            provided_shape="W boundary plus exact row-antisymmetric C4_1 phase and scalar-fixed finite theorem",
            decision="source_stage_candidate_if_finite_theorem_present",
            first_missing_or_falsifier="DANGER3 framing and extraction after theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="exact_quartic_selector_without_value_theorem",
            provided_shape="exact C4_1 phase selecting one edge, but no finite value/divisor theorem",
            decision="repair_value_divisor_theorem_missing",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem for the selected row",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="boundary_plus_one_sign_of_phase",
            provided_shape="W boundary plus only real-sign or imag-sign of the quartic phase",
            decision="repair_two_edge_ambiguity",
            first_missing_or_falsifier="the remaining quartic sign or direct one-edge theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="quartic_magnitude_or_quadratic_only",
            provided_shape="quartic magnitude, quadratic character, or boundary-visible component only",
            decision="repair_all_four_edge_ambiguity",
            first_missing_or_falsifier="exact order-4 phase selecting one legal edge",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="quartic_phase_without_row_sign",
            provided_shape="C4 phase on the mod-13 quotient without row-antisymmetric mod-3 tensor sign",
            decision="repair_mixed_tensor_missing",
            first_missing_or_falsifier="row-antisymmetric mod-3 sign and zero proper pushforwards",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="same_parity_quartic_phase",
            provided_shape="order-4 phase attached to same-parity edge",
            decision="reject_zero_boundary_wrong_edge",
            first_missing_or_falsifier="same-parity edges have zero W boundary",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_payload() -> QuarticSelectorPayload:
    markers = evidence_markers()
    rows = selector_rows()
    coarse = coarse_selectors(rows)
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    legal_ok = sum(row.row_ok for row in rows)
    unique_quartic = len({row.quartic_selector for row in rows})
    unique_boundaries = len({row.boundary_dft for row in rows})
    coarse_ok = sum(row.row_ok for row in coarse)
    accepted = sum(row.source_stage_candidate for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(rows) == 4
        and legal_ok == 4
        and unique_quartic == 4
        and unique_boundaries == 1
        and coarse_ok == len(coarse)
        and {row.selector_label for row in rows} == {"R+I+", "R-I+", "R-I-", "R+I-"}
        and accepted == 1
        and repairs == 4
        and rejects == 1
        and current_source_theorems == 0
        and current_submission_ready == 0
        and all(row.ok for row in route_rows)
    )
    return QuarticSelectorPayload(
        evidence_markers=markers,
        rows=rows,
        coarse_selectors=coarse,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        legal_rows_ok=legal_ok,
        unique_quartic_selectors=unique_quartic,
        unique_boundaries=unique_boundaries,
        coarse_selectors_ok=coarse_ok,
        accepted_routes=accepted,
        repair_rows=repairs,
        reject_rows=rejects,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def fmt_gi(value: GI) -> str:
    real, imag = value
    if imag == 0:
        return str(real)
    if real == 0:
        return f"{imag}i"
    sign_text = "+" if imag > 0 else "-"
    return f"{real}{sign_text}{abs(imag)}i"


def main() -> int:
    payload = build_payload()
    print("p25 v2 quartic selector payload")
    print("evidence")
    for row in payload.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} marker={row.marker}")
    print("legal_selector_rows")
    for row in payload.rows:
        print(
            f"  m={row.multiplier}: {row.plus_coset}->{row.minus_coset} "
            f"boundary_dft=({', '.join(fmt_gi(v) for v in row.boundary_dft)}) "
            f"C4_1={fmt_gi(row.quartic_selector)} C4_3={fmt_gi(row.conjugate_selector)} "
            f"selector={row.selector_label} ok={int(row.row_ok)}"
        )
    print("coarse_selectors")
    for row in payload.coarse_selectors:
        print(
            f"  {row.name}: surviving_edges={row.surviving_edges} "
            f"decision={row.decision} ok={int(row.row_ok)}"
        )
    print("routes")
    for row in payload.routes:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source_stage={int(row.source_stage_candidate)} "
            f"repair={int(row.repair)} reject={int(row.reject)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={payload.evidence_markers_ok}/{len(payload.evidence_markers)}")
    print(f"  legal_rows_ok={payload.legal_rows_ok}/{len(payload.rows)}")
    print(f"  unique_quartic_selectors={payload.unique_quartic_selectors}")
    print(f"  unique_boundaries={payload.unique_boundaries}")
    print(f"  coarse_selectors_ok={payload.coarse_selectors_ok}/{len(payload.coarse_selectors)}")
    print(f"  accepted_routes={payload.accepted_routes}")
    print(f"  repair_rows={payload.repair_rows}")
    print(f"  reject_rows={payload.reject_rows}")
    print(f"  current_source_theorems={payload.current_source_theorems}")
    print(f"  current_submission_ready={payload.current_submission_ready}")
    print(f"p25_v2_quartic_selector_payload_rows={int(payload.row_ok)}/1")
    return 0 if payload.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
