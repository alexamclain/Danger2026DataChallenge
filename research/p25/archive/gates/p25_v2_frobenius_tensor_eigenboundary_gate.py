#!/usr/bin/env python3
"""Frobenius eigencomponent boundary screen for p25 tensor-edge rows."""

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
class EigenRow:
    multiplier: int
    plus_coset: str
    minus_coset: str
    row_antisymmetric: tuple[int, int, int, int]
    antisymmetric_dft: tuple[GI, GI, GI, GI]
    frobenius_eigenvalues: tuple[int, int, int, int]
    boundary_multipliers: tuple[int, int, int, int]
    boundary_dft: tuple[GI, GI, GI, GI]
    killed_order4_components: int
    visible_quadratic_component: GI
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
class FrobeniusTensorEigenboundary:
    evidence_markers: tuple[EvidenceMarker, ...]
    rows: tuple[EigenRow, ...]
    routes: tuple[Route, ...]
    evidence_markers_ok: int
    legal_rows_ok: int
    rows_with_order4_components_killed: int
    rows_with_quadratic_boundary_visible: int
    common_boundary_rows: int
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
            "quotient_h90_idempotent_mechanism",
            "research/p25/evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "h0_conductor39_unified_target",
            "research/p25/evidence/p25_v2_h0_conductor39_unified_target_20260616.md",
            "p25_v2_h0_conductor39_unified_target_rows=1/1",
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


def frobenius_eigenvalue(character: int) -> int:
    row_flip_eigenvalue = -1
    c4_shift_by_two_eigenvalue = (-1) ** character
    return row_flip_eigenvalue * c4_shift_by_two_eigenvalue


def eigen_rows() -> tuple[EigenRow, ...]:
    rows: list[EigenRow] = []
    frob_eigs = tuple(frobenius_eigenvalue(character) for character in range(4))
    multipliers = tuple(1 - value for value in frob_eigs)
    for multiplier, plus_coset, minus_coset in LEGAL_EDGES:
        row1 = edge_vector(plus_coset, minus_coset)
        row2 = tuple(-value for value in row1)
        row_antisymmetric = tuple(a - b for a, b in zip(row1, row2))
        anti_dft = dft(row_antisymmetric)  # type: ignore[arg-type]
        boundary_dft = tuple(
            gi_mul_int(component, boundary_multiplier)
            for component, boundary_multiplier in zip(anti_dft, multipliers)
        )
        killed_order4 = int(
            anti_dft[1] != (0, 0)
            and anti_dft[3] != (0, 0)
            and boundary_dft[1] == (0, 0)
            and boundary_dft[3] == (0, 0)
        )
        quadratic_visible = int(anti_dft[2] != (0, 0) and boundary_dft[2] == (-8, 0))
        row_ok = (
            frob_eigs == (-1, 1, -1, 1)
            and multipliers == (2, 0, 2, 0)
            and anti_dft[0] == (0, 0)
            and anti_dft[1] != (0, 0)
            and anti_dft[2] == (-4, 0)
            and anti_dft[3] != (0, 0)
            and boundary_dft == ((0, 0), (0, 0), (-8, 0), (0, 0))
            and killed_order4 == 1
            and quadratic_visible == 1
        )
        rows.append(
            EigenRow(
                multiplier=multiplier,
                plus_coset=plus_coset,
                minus_coset=minus_coset,
                row_antisymmetric=row_antisymmetric,  # type: ignore[arg-type]
                antisymmetric_dft=anti_dft,
                frobenius_eigenvalues=frob_eigs,  # type: ignore[arg-type]
                boundary_multipliers=multipliers,  # type: ignore[arg-type]
                boundary_dft=boundary_dft,  # type: ignore[arg-type]
                killed_order4_components=2 * killed_order4,
                visible_quadratic_component=boundary_dft[2],
                row_ok=row_ok,
            )
        )
    return tuple(rows)


def routes() -> tuple[Route, ...]:
    return (
        Route(
            name="full_tensor_edge_value_theorem",
            provided_shape="row-antisymmetric C4 edge, order-4 selector phase, and scalar-fixed finite theorem",
            decision="source_stage_candidate_if_scalar_fixed_theorem_present",
            first_missing_or_falsifier="DANGER3 framing and extraction after theorem hit",
            source_stage_candidate=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        Route(
            name="boundary_only_or_norm156_only",
            provided_shape="Hilbert-90 boundary W = Norm_156(Y_507), without source selector data",
            decision="repair_frobenius_boundary_collapses_edge_phase",
            first_missing_or_falsifier="Frob-invariant order-4 selector components are killed by 1-Frob",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="quadratic_boundary_component_only",
            provided_shape="row-antisymmetric quadratic component or broad odd/even aggregate",
            decision="repair_boundary_visible_but_selector_missing",
            first_missing_or_falsifier="quadratic component is common to all four legal rows",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="order4_selector_components_without_value",
            provided_shape="order-4 C4 selector phase, but no finite value/divisor theorem",
            decision="repair_value_divisor_theorem_missing",
            first_missing_or_falsifier="scalar-fixed finite value/divisor theorem",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="frob_invariant_selector_ignored",
            provided_shape="theorem descends after applying 1-Frob and forgets the Frob-invariant selector phase",
            decision="repair_selector_erased_by_boundary_map",
            first_missing_or_falsifier="source-stage theorem for the selector before Hilbert-90 boundary projection",
            source_stage_candidate=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        Route(
            name="same_parity_zero_boundary",
            provided_shape="same-parity C4 edge or row-symmetric component",
            decision="reject_wrong_boundary_or_wrong_tensor",
            first_missing_or_falsifier="boundary is zero or tensor row sign is wrong",
            source_stage_candidate=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_screen() -> FrobeniusTensorEigenboundary:
    markers = evidence_markers()
    rows = eigen_rows()
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    legal_ok = sum(row.row_ok for row in rows)
    killed = sum(row.killed_order4_components == 2 for row in rows)
    visible = sum(row.visible_quadratic_component == (-8, 0) for row in rows)
    common = sum(row.boundary_dft == ((0, 0), (0, 0), (-8, 0), (0, 0)) for row in rows)
    accepted = sum(row.source_stage_candidate for row in route_rows)
    repairs = sum(row.repair for row in route_rows)
    rejects = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        evidence_ok == len(markers)
        and len(rows) == 4
        and legal_ok == 4
        and killed == 4
        and visible == 4
        and common == 4
        and len({row.antisymmetric_dft[1] for row in rows}) == 4
        and len({row.boundary_dft for row in rows}) == 1
        and accepted == 1
        and repairs == 4
        and rejects == 1
        and current_source_theorems == 0
        and current_submission_ready == 0
        and all(row.ok for row in route_rows)
    )
    return FrobeniusTensorEigenboundary(
        evidence_markers=markers,
        rows=rows,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        legal_rows_ok=legal_ok,
        rows_with_order4_components_killed=killed,
        rows_with_quadratic_boundary_visible=visible,
        common_boundary_rows=common,
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
    screen = build_screen()
    print("p25 v2 Frobenius tensor eigenboundary screen")
    print("evidence")
    for row in screen.evidence_markers:
        print(f"  {row.name}: ok={int(row.ok)} marker={row.marker}")
    print("legal_tensor_rows")
    for row in screen.rows:
        print(
            f"  m={row.multiplier}: {row.plus_coset}->{row.minus_coset} "
            f"anti_dft=({', '.join(fmt_gi(v) for v in row.antisymmetric_dft)}) "
            f"frob_eigs={row.frobenius_eigenvalues} "
            f"boundary_multipliers={row.boundary_multipliers} "
            f"boundary_dft=({', '.join(fmt_gi(v) for v in row.boundary_dft)}) "
            f"ok={int(row.row_ok)}"
        )
    print("routes")
    for row in screen.routes:
        print(
            f"  {row.name}: decision={row.decision} "
            f"source_stage={int(row.source_stage_candidate)} "
            f"repair={int(row.repair)} reject={int(row.reject)}"
        )
    print("counts")
    print(f"  evidence_markers_ok={screen.evidence_markers_ok}/{len(screen.evidence_markers)}")
    print(f"  legal_rows_ok={screen.legal_rows_ok}/{len(screen.rows)}")
    print(f"  rows_with_order4_components_killed={screen.rows_with_order4_components_killed}")
    print(f"  rows_with_quadratic_boundary_visible={screen.rows_with_quadratic_boundary_visible}")
    print(f"  common_boundary_rows={screen.common_boundary_rows}")
    print(f"  accepted_routes={screen.accepted_routes}")
    print(f"  repair_rows={screen.repair_rows}")
    print(f"  reject_rows={screen.reject_rows}")
    print(f"  current_source_theorems={screen.current_source_theorems}")
    print(f"  current_submission_ready={screen.current_submission_ready}")
    print(f"p25_v2_frobenius_tensor_eigenboundary_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
