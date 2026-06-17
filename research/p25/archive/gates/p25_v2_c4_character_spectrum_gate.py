#!/usr/bin/env python3
"""C4 character spectrum for the p25 quotient-C4 edge target.

The mod-13 rectangle screen says a legal row is one odd C4 coset against one
even C4 coset.  This gate records the Fourier obstruction behind that rule:
every legal edge has essential order-4 C4 character components.  The
quadratic character component alone is the broad odd-minus-even aggregate, not
one selected edge.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


# Represent Gaussian integers as (real, imag).
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
class SpectrumRow:
    multiplier: int
    plus_coset: str
    minus_coset: str
    vector: tuple[int, int, int, int]
    fourier: tuple[GI, GI, GI, GI]
    constant_zero: bool
    quadratic_component: GI
    order4_components_nonzero: bool
    row_ok: bool


@dataclass(frozen=True)
class ControlRow:
    name: str
    vector: tuple[int, int, int, int]
    fourier: tuple[GI, GI, GI, GI]
    decision: str
    row_ok: bool


@dataclass(frozen=True)
class C4CharacterSpectrum:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[SpectrumRow, ...]
    controls: tuple[ControlRow, ...]
    evidence_markers_ok: int
    legal_rows_ok: int
    controls_ok: int
    rows_with_order4_components: int
    pure_quadratic_controls: int
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
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
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
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
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


def spectrum_rows() -> tuple[SpectrumRow, ...]:
    rows: list[SpectrumRow] = []
    for multiplier, plus_coset, minus_coset in LEGAL_EDGES:
        vector = edge_vector(plus_coset, minus_coset)
        fourier = dft(vector)
        row_ok = (
            sum(vector) == 0
            and fourier[0] == (0, 0)
            and fourier[2] == (-2, 0)
            and fourier[1] != (0, 0)
            and fourier[3] != (0, 0)
            and {abs(fourier[1][0]), abs(fourier[1][1])} == {1}
            and fourier[3] == (fourier[1][0], -fourier[1][1])
        )
        rows.append(
            SpectrumRow(
                multiplier=multiplier,
                plus_coset=plus_coset,
                minus_coset=minus_coset,
                vector=vector,
                fourier=fourier,
                constant_zero=fourier[0] == (0, 0),
                quadratic_component=fourier[2],
                order4_components_nonzero=fourier[1] != (0, 0) and fourier[3] != (0, 0),
                row_ok=row_ok,
            )
        )
    return tuple(rows)


def control_rows() -> tuple[ControlRow, ...]:
    pure_quadratic = (-1, 1, -1, 1)
    same_parity_odd = (0, 1, 0, -1)
    same_parity_even = (1, 0, -1, 0)
    controls = (
        ControlRow(
            name="pure_quadratic_odd_minus_even",
            vector=pure_quadratic,
            fourier=dft(pure_quadratic),
            decision="repair_broad_quadratic_aggregate_boundary_2w",
            row_ok=dft(pure_quadratic) == ((0, 0), (0, 0), (-4, 0), (0, 0)),
        ),
        ControlRow(
            name="same_parity_odd_difference",
            vector=same_parity_odd,
            fourier=dft(same_parity_odd),
            decision="reject_zero_boundary_same_parity_edge",
            row_ok=dft(same_parity_odd)[2] == (0, 0),
        ),
        ControlRow(
            name="same_parity_even_difference",
            vector=same_parity_even,
            fourier=dft(same_parity_even),
            decision="reject_zero_boundary_same_parity_edge",
            row_ok=dft(same_parity_even)[2] == (0, 0),
        ),
    )
    return controls


def build_spectrum() -> C4CharacterSpectrum:
    markers = evidence_markers()
    rows = spectrum_rows()
    controls = control_rows()
    evidence_ok = sum(row.ok for row in markers)
    legal_ok = sum(row.row_ok for row in rows)
    controls_ok = sum(row.row_ok for row in controls)
    order4_rows = sum(row.order4_components_nonzero for row in rows)
    pure_quadratic_controls = sum(
        row.name == "pure_quadratic_odd_minus_even"
        and row.fourier == ((0, 0), (0, 0), (-4, 0), (0, 0))
        for row in controls
    )
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(rows) == 4
        and legal_ok == 4
        and len({row.fourier[1] for row in rows}) == 4
        and all(row.quadratic_component == (-2, 0) for row in rows)
        and order4_rows == 4
        and len(controls) == 3
        and controls_ok == 3
        and pure_quadratic_controls == 1
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return C4CharacterSpectrum(
        evidence_markers=markers,
        rows=rows,
        controls=controls,
        evidence_markers_ok=evidence_ok,
        legal_rows_ok=legal_ok,
        controls_ok=controls_ok,
        rows_with_order4_components=order4_rows,
        pure_quadratic_controls=pure_quadratic_controls,
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
    print("p25 v2 C4 character spectrum")
    print("evidence")
    for row in spectrum.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} marker={row.marker}")
    print("legal_edge_spectra")
    for row in spectrum.rows:
        print(
            f"  m={row.multiplier}: {row.plus_coset}->{row.minus_coset} "
            f"vector={row.vector} dft=({', '.join(fmt_gi(v) for v in row.fourier)}) "
            f"order4={int(row.order4_components_nonzero)} ok={int(row.row_ok)}"
        )
    print("controls")
    for row in spectrum.controls:
        print(
            f"  {row.name}: vector={row.vector} "
            f"dft=({', '.join(fmt_gi(v) for v in row.fourier)}) "
            f"decision={row.decision} ok={int(row.row_ok)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={spectrum.evidence_markers_ok}/{len(spectrum.evidence_markers)}")
    print(f"  legal_rows_ok={spectrum.legal_rows_ok}/{len(spectrum.rows)}")
    print(f"  controls_ok={spectrum.controls_ok}/{len(spectrum.controls)}")
    print(f"  rows_with_order4_components={spectrum.rows_with_order4_components}")
    print(f"  pure_quadratic_controls={spectrum.pure_quadratic_controls}")
    print(f"  current_source_theorems={spectrum.current_source_theorems}")
    print(f"  current_submission_ready={spectrum.current_submission_ready}")
    print(f"p25_v2_c4_character_spectrum_rows={int(spectrum.row_ok)}/1")
    return 0 if spectrum.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
