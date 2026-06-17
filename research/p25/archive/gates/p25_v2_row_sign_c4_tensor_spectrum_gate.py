#!/usr/bin/env python3
"""Row-sign x C4 tensor spectrum for the p25 conductor-39 source rows."""

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
class TensorRow:
    multiplier: int
    plus_coset: str
    minus_coset: str
    row1: tuple[int, int, int, int]
    row2: tuple[int, int, int, int]
    row_symmetric: tuple[int, int, int, int]
    row_antisymmetric: tuple[int, int, int, int]
    antisymmetric_dft: tuple[GI, GI, GI, GI]
    mod3_pushforward: tuple[int, int]
    mod13_pushforward: tuple[int, int, int, int]
    tensor_support: tuple[str, ...]
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
class RowSignC4TensorSpectrum:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[TensorRow, ...]
    routes: tuple[Route, ...]
    evidence_markers_ok: int
    legal_rows_ok: int
    rows_with_zero_symmetric_part: int
    rows_with_zero_proper_pushforwards: int
    rows_with_order4_c4_phases: int
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
            "mixed_signed_column_fingerprint",
            "research/p25/evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
            "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
        ),
        marker(
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            "c4_character_spectrum",
            "research/p25/evidence/p25_v2_c4_character_spectrum_20260616.md",
            "p25_v2_c4_character_spectrum_rows=1/1",
        ),
        marker(
            "quotient_h90_idempotent_mechanism",
            "research/p25/evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
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


def add_vectors(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a + b for a, b in zip(left, right))


def subtract_vectors(left: tuple[int, ...], right: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(a - b for a, b in zip(left, right))


def tensor_rows() -> tuple[TensorRow, ...]:
    rows: list[TensorRow] = []
    for multiplier, plus_coset, minus_coset in LEGAL_EDGES:
        row1 = edge_vector(plus_coset, minus_coset)
        row2 = tuple(-value for value in row1)  # type: ignore[assignment]
        symmetric = add_vectors(row1, row2)
        antisymmetric = subtract_vectors(row1, row2)
        anti_dft = dft(antisymmetric)  # type: ignore[arg-type]
        mod3_pushforward = (sum(row1), sum(row2))
        mod13_pushforward = add_vectors(row1, row2)
        tensor_support = tuple(
            f"row_antisymmetric*C4_{character}"
            for character, value in enumerate(anti_dft)
            if value != (0, 0)
        )
        row_ok = (
            symmetric == (0, 0, 0, 0)
            and mod3_pushforward == (0, 0)
            and mod13_pushforward == (0, 0, 0, 0)
            and anti_dft[0] == (0, 0)
            and anti_dft[2] == (-4, 0)
            and anti_dft[1] != (0, 0)
            and anti_dft[3] != (0, 0)
            and len(tensor_support) == 3
        )
        rows.append(
            TensorRow(
                multiplier=multiplier,
                plus_coset=plus_coset,
                minus_coset=minus_coset,
                row1=row1,
                row2=row2,  # type: ignore[arg-type]
                row_symmetric=symmetric,  # type: ignore[arg-type]
                row_antisymmetric=antisymmetric,  # type: ignore[arg-type]
                antisymmetric_dft=anti_dft,
                mod3_pushforward=mod3_pushforward,
                mod13_pushforward=mod13_pushforward,  # type: ignore[arg-type]
                tensor_support=tensor_support,
                row_ok=row_ok,
            )
        )
    return tuple(rows)


def routes() -> tuple[Route, ...]:
    return (
        Route(
            name="row_sign_c4_edge_theorem",
            provided_shape="row-antisymmetric C4 edge with order-4 phase and finite value/divisor theorem",
            decision="source_stage_candidate_if_scalar_fixed_theorem_present",
            first_missing_or_falsifier="DANGER3 framing and extraction after theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="mod13_projection_only",
            provided_shape="sum over the two mod-3 rows or conductor-13 projection",
            decision="reject_zero_pushforward_loses_mixed_tensor",
            first_missing_or_falsifier="legal rows have zero mod-13 pushforward",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
        Route(
            name="mod3_projection_only",
            provided_shape="sum over C4 columns or conductor-3 projection",
            decision="reject_zero_pushforward_loses_edge",
            first_missing_or_falsifier="legal rows have zero mod-3 pushforward",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
        Route(
            name="row_symmetric_c4_statement",
            provided_shape="same C4 edge in both mod-3 rows",
            decision="reject_row_symmetric_wrong_tensor",
            first_missing_or_falsifier="legal rows are purely row-antisymmetric",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
        Route(
            name="row_sign_only_no_c4_phase",
            provided_shape="mod-3 row sign without selected C4 edge phase",
            decision="repair_c4_edge_phase_missing",
            first_missing_or_falsifier="order-4 C4 phase selecting one legal edge",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="c4_edge_without_row_sign",
            provided_shape="C4 edge data without opposite mod-3 row signs",
            decision="repair_or_reject_mixed_row_sign_missing",
            first_missing_or_falsifier="row-antisymmetric mixed tensor structure",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="row_sign_quadratic_only",
            provided_shape="row-antisymmetric quadratic aggregate with no order-4 phase",
            decision="repair_broad_quadratic_aggregate_boundary_2w",
            first_missing_or_falsifier="order-4 C4 phase selecting one legal edge",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="tensor_selector_without_value_theorem",
            provided_shape="correct row-sign and C4 phase but no finite value/divisor theorem",
            decision="repair_value_divisor_theorem_missing",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
    )


def build_spectrum() -> RowSignC4TensorSpectrum:
    markers = evidence_markers()
    rows = tensor_rows()
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    legal_ok = sum(row.row_ok for row in rows)
    zero_symmetric = sum(row.row_symmetric == (0, 0, 0, 0) for row in rows)
    zero_pushforwards = sum(
        row.mod3_pushforward == (0, 0) and row.mod13_pushforward == (0, 0, 0, 0)
        for row in rows
    )
    order4_rows = sum(
        row.antisymmetric_dft[1] != (0, 0) and row.antisymmetric_dft[3] != (0, 0)
        for row in rows
    )
    accepted = sum(row.source_stage_candidate for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(rows) == 4
        and legal_ok == 4
        and zero_symmetric == 4
        and zero_pushforwards == 4
        and order4_rows == 4
        and len({row.antisymmetric_dft[1] for row in rows}) == 4
        and accepted == 1
        and repairs == 4
        and rejects == 3
        and current_source_theorems == 0
        and current_submission_ready == 0
        and all(row.ok for row in route_rows)
    )
    return RowSignC4TensorSpectrum(
        evidence_markers=markers,
        rows=rows,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        legal_rows_ok=legal_ok,
        rows_with_zero_symmetric_part=zero_symmetric,
        rows_with_zero_proper_pushforwards=zero_pushforwards,
        rows_with_order4_c4_phases=order4_rows,
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
    sign = "+" if imag > 0 else "-"
    return f"{real}{sign}{abs(imag)}i"


def main() -> int:
    spectrum = build_spectrum()
    print("p25 v2 row-sign x C4 tensor spectrum")
    print("evidence")
    for row in spectrum.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} marker={row.marker}")
    print("legal_tensor_rows")
    for row in spectrum.rows:
        print(
            f"  m={row.multiplier}: {row.plus_coset}->{row.minus_coset} "
            f"row1={row.row1} row2={row.row2} sym={row.row_symmetric} "
            f"anti_dft=({', '.join(fmt_gi(v) for v in row.antisymmetric_dft)}) "
            f"support={row.tensor_support} ok={int(row.row_ok)}"
        )
    print("routes")
    for row in spectrum.routes:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source_stage={int(row.source_stage_candidate)} "
            f"repair={int(row.repair)} reject={int(row.reject)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={spectrum.evidence_markers_ok}/{len(spectrum.evidence_markers)}")
    print(f"  legal_rows_ok={spectrum.legal_rows_ok}/{len(spectrum.rows)}")
    print(f"  rows_with_zero_symmetric_part={spectrum.rows_with_zero_symmetric_part}")
    print(f"  rows_with_zero_proper_pushforwards={spectrum.rows_with_zero_proper_pushforwards}")
    print(f"  rows_with_order4_c4_phases={spectrum.rows_with_order4_c4_phases}")
    print(f"  accepted_routes={spectrum.accepted_routes}")
    print(f"  repair_rows={spectrum.repair_rows}")
    print(f"  reject_rows={spectrum.reject_rows}")
    print(f"  current_source_theorems={spectrum.current_source_theorems}")
    print(f"  current_submission_ready={spectrum.current_submission_ready}")
    print(f"p25_v2_row_sign_c4_tensor_spectrum_rows={int(spectrum.row_ok)}/1")
    return 0 if spectrum.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
