#!/usr/bin/env python3
"""Pure quartic-selector structure of the Q diagonal split.

The Q split complexity screen shows that the needed splits m1-m4 and m2-m8
are full 24-support boundary-zero quotients.  This gate records the more
positive structure: in row-antisymmetric quotient-C4 Fourier coordinates,
those splits are pure order-4 selector data.  The Q diagonal aggregate carries
the quadratic component; the split carries the quartic phase.  Together they
recover twice one edge, so a value theorem still needs an oriented root/sign
or a direct one-edge theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


GI = tuple[int, int]
V4 = tuple[int, int, int, int]

EDGE_VECTORS: dict[int, V4] = {
    1: (0, 0, -36, 36),
    2: (-36, 0, 0, 36),
    4: (-36, 36, 0, 0),
    8: (0, 36, -36, 0),
}
DIAGONALS: dict[str, tuple[int, int]] = {
    "m1_plus_m4": (1, 4),
    "m2_plus_m8": (2, 8),
}
SPLITS: dict[str, tuple[int, int]] = {
    "m1_minus_m4": (1, 4),
    "m2_minus_m8": (2, 8),
}


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class FourierProfile:
    name: str
    vector: V4
    dft: tuple[GI, GI, GI, GI]
    constant_zero: bool
    order4_nonzero: bool
    quadratic_component: GI
    pure_quartic: bool
    pure_quadratic: bool
    row_ok: bool


@dataclass(frozen=True)
class ReconstructionProfile:
    name: str
    diagonal_name: str
    split_name: str
    recovered_edge: int
    opposite_edge: int
    plus_recovers_twice_edge: bool
    minus_recovers_twice_opposite: bool
    recovered_dft: tuple[GI, GI, GI, GI]
    row_ok: bool


@dataclass(frozen=True)
class RouteRow:
    name: str
    decision: str
    first_missing_or_falsifier: str
    support: bool
    normalize: bool
    repair: bool
    reject: bool
    ok: bool


@dataclass(frozen=True)
class QSplitQuarticSelector:
    evidence_markers: tuple[EvidenceMarker, ...]
    edge_profiles: tuple[FourierProfile, ...]
    diagonal_profiles: tuple[FourierProfile, ...]
    split_profiles: tuple[FourierProfile, ...]
    reconstructions: tuple[ReconstructionProfile, ...]
    routes: tuple[RouteRow, ...]
    evidence_markers_ok: int
    edge_profiles_ok: int
    pure_quadratic_diagonals: int
    pure_quartic_splits: int
    reconstruction_rows_ok: int
    support_routes: int
    normalize_routes: int
    repair_rows: int
    reject_rows: int
    current_source_theorems: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_split_quotient_complexity",
            "research/p25/evidence/p25_v2_q_split_quotient_complexity_20260616.md",
            "p25_v2_q_split_quotient_complexity_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "row_sign_c4_tensor_spectrum",
            "research/p25/evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md",
            "p25_v2_row_sign_c4_tensor_spectrum_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "q_plus_explicit_oriented_diagonal_split",
        ),
    )


def gi_add(left: GI, right: GI) -> GI:
    return (left[0] + right[0], left[1] + right[1])


def gi_mul_int(value: GI, scalar: int) -> GI:
    return (value[0] * scalar, value[1] * scalar)


def i_power(exp: int) -> GI:
    return ((1, 0), (0, 1), (-1, 0), (0, -1))[exp % 4]


def dft(vector: V4) -> tuple[GI, GI, GI, GI]:
    out: list[GI] = []
    for character in range(4):
        total = (0, 0)
        for index, coefficient in enumerate(vector):
            total = gi_add(total, gi_mul_int(i_power(-character * index), coefficient))
        out.append(total)
    return tuple(out)  # type: ignore[return-value]


def add_vec(left: V4, right: V4) -> V4:
    return tuple(a + b for a, b in zip(left, right))  # type: ignore[return-value]


def sub_vec(left: V4, right: V4) -> V4:
    return tuple(a - b for a, b in zip(left, right))  # type: ignore[return-value]


def scale_vec(vector: V4, scalar: int) -> V4:
    return tuple(scalar * value for value in vector)  # type: ignore[return-value]


def profile(name: str, vector: V4, expected: str) -> FourierProfile:
    spectrum = dft(vector)
    constant_zero = spectrum[0] == (0, 0)
    order4_nonzero = spectrum[1] != (0, 0) and spectrum[3] != (0, 0)
    pure_quartic = constant_zero and order4_nonzero and spectrum[2] == (0, 0)
    pure_quadratic = constant_zero and not order4_nonzero and spectrum[2] != (0, 0)
    edge_like = constant_zero and order4_nonzero and spectrum[2] != (0, 0)
    row_ok = (
        (expected == "edge" and edge_like)
        or (expected == "pure_quadratic" and pure_quadratic)
        or (expected == "pure_quartic" and pure_quartic)
    )
    return FourierProfile(
        name=name,
        vector=vector,
        dft=spectrum,
        constant_zero=constant_zero,
        order4_nonzero=order4_nonzero,
        quadratic_component=spectrum[2],
        pure_quartic=pure_quartic,
        pure_quadratic=pure_quadratic,
        row_ok=row_ok,
    )


def edge_profiles() -> tuple[FourierProfile, ...]:
    return tuple(profile(f"m{edge}", vector, "edge") for edge, vector in EDGE_VECTORS.items())


def diagonal_profiles() -> tuple[FourierProfile, ...]:
    return tuple(
        profile(name, add_vec(EDGE_VECTORS[first], EDGE_VECTORS[second]), "pure_quadratic")
        for name, (first, second) in DIAGONALS.items()
    )


def split_profiles() -> tuple[FourierProfile, ...]:
    return tuple(
        profile(name, sub_vec(EDGE_VECTORS[first], EDGE_VECTORS[second]), "pure_quartic")
        for name, (first, second) in SPLITS.items()
    )


def reconstruction(
    name: str,
    diagonal_name: str,
    split_name: str,
    first: int,
    second: int,
) -> ReconstructionProfile:
    diagonal = add_vec(EDGE_VECTORS[first], EDGE_VECTORS[second])
    split = sub_vec(EDGE_VECTORS[first], EDGE_VECTORS[second])
    plus = add_vec(diagonal, split)
    minus = sub_vec(diagonal, split)
    twice_first = scale_vec(EDGE_VECTORS[first], 2)
    twice_second = scale_vec(EDGE_VECTORS[second], 2)
    plus_ok = plus == twice_first
    minus_ok = minus == twice_second
    return ReconstructionProfile(
        name=name,
        diagonal_name=diagonal_name,
        split_name=split_name,
        recovered_edge=first,
        opposite_edge=second,
        plus_recovers_twice_edge=plus_ok,
        minus_recovers_twice_opposite=minus_ok,
        recovered_dft=dft(plus),
        row_ok=plus_ok and minus_ok,
    )


def reconstructions() -> tuple[ReconstructionProfile, ...]:
    return (
        reconstruction("q_m1_m4_plus_split", "m1_plus_m4", "m1_minus_m4", 1, 4),
        reconstruction("q_m2_m8_plus_split", "m2_plus_m8", "m2_minus_m8", 2, 8),
    )


def routes() -> tuple[RouteRow, ...]:
    return (
        RouteRow(
            "q_diagonal_pure_quadratic_only",
            "support_diagonal_aggregate_selector_missing",
            "pure quartic split or direct one-edge theorem",
            support=True,
            normalize=False,
            repair=False,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_split_pure_quartic_only",
            "repair_boundary_zero_selector_only",
            "Q diagonal aggregate value and oriented root/direct one-edge theorem",
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_diagonal_plus_pure_quartic_split_without_root",
            "repair_oriented_square_root_missing",
            "oriented root/sign data after reaching twice one edge",
            support=False,
            normalize=False,
            repair=True,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_diagonal_plus_pure_quartic_split_with_oriented_root",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            "same theorem data after explicit oriented split/root normalization",
            support=False,
            normalize=True,
            repair=False,
            reject=False,
            ok=True,
        ),
        RouteRow(
            "q_split_wrong_quartic_phase",
            "reject_wrong_q_split_phase",
            "split phase must match m1-m4 or m2-m8 for the chosen diagonal",
            support=False,
            normalize=False,
            repair=False,
            reject=True,
            ok=True,
        ),
    )


def build_selector() -> QSplitQuarticSelector:
    markers = evidence_markers()
    edges = edge_profiles()
    diagonals = diagonal_profiles()
    splits = split_profiles()
    reconstruction_rows = reconstructions()
    route_rows = routes()
    evidence_ok = sum(row.ok for row in markers)
    edges_ok = sum(row.row_ok for row in edges)
    pure_diagonals = sum(row.pure_quadratic for row in diagonals)
    pure_splits = sum(row.pure_quartic for row in splits)
    recon_ok = sum(row.row_ok for row in reconstruction_rows)
    support_count = sum(row.support for row in route_rows)
    normalize_count = sum(row.normalize for row in route_rows)
    repair_count = sum(row.repair for row in route_rows)
    reject_count = sum(row.reject for row in route_rows)
    current_source_theorems = 0
    expected_edge_dfts = (
        ((0, 0), (36, 36), (-72, 0), (36, -36)),
        ((0, 0), (-36, 36), (-72, 0), (-36, -36)),
        ((0, 0), (-36, -36), (-72, 0), (-36, 36)),
        ((0, 0), (36, -36), (-72, 0), (36, 36)),
    )
    expected_diagonal_dfts = (
        ((0, 0), (0, 0), (-144, 0), (0, 0)),
        ((0, 0), (0, 0), (-144, 0), (0, 0)),
    )
    expected_split_dfts = (
        ((0, 0), (72, 72), (0, 0), (72, -72)),
        ((0, 0), (-72, 72), (0, 0), (-72, -72)),
    )
    expected_decisions = (
        "support_diagonal_aggregate_selector_missing",
        "repair_boundary_zero_selector_only",
        "repair_oriented_square_root_missing",
        "normalize_to_one_edge_then_apply_source_snippet_intake",
        "reject_wrong_q_split_phase",
    )
    row_ok = (
        evidence_ok == len(markers)
        and edges_ok == 4
        and tuple(row.dft for row in edges) == expected_edge_dfts
        and len(diagonals) == 2
        and pure_diagonals == 2
        and tuple(row.dft for row in diagonals) == expected_diagonal_dfts
        and len(splits) == 2
        and pure_splits == 2
        and tuple(row.dft for row in splits) == expected_split_dfts
        and len(reconstruction_rows) == 2
        and recon_ok == 2
        and tuple(row.decision for row in route_rows) == expected_decisions
        and support_count == 1
        and normalize_count == 1
        and repair_count == 2
        and reject_count == 1
        and current_source_theorems == 0
    )
    return QSplitQuarticSelector(
        evidence_markers=markers,
        edge_profiles=edges,
        diagonal_profiles=diagonals,
        split_profiles=splits,
        reconstructions=reconstruction_rows,
        routes=route_rows,
        evidence_markers_ok=evidence_ok,
        edge_profiles_ok=edges_ok,
        pure_quadratic_diagonals=pure_diagonals,
        pure_quartic_splits=pure_splits,
        reconstruction_rows_ok=recon_ok,
        support_routes=support_count,
        normalize_routes=normalize_count,
        repair_rows=repair_count,
        reject_rows=reject_count,
        current_source_theorems=current_source_theorems,
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


def fmt_dft(values: tuple[GI, GI, GI, GI]) -> str:
    return "(" + ", ".join(fmt_gi(value) for value in values) + ")"


def main() -> int:
    selector = build_selector()
    print("p25 v2 Q split quartic selector")
    for marker_row in selector.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("edge_profiles")
    for row in selector.edge_profiles:
        print(f"  {row.name}: vector={row.vector} dft={fmt_dft(row.dft)}")
    print("diagonal_profiles")
    for row in selector.diagonal_profiles:
        print(f"  {row.name}: vector={row.vector} dft={fmt_dft(row.dft)} pure_quadratic={int(row.pure_quadratic)}")
    print("split_profiles")
    for row in selector.split_profiles:
        print(f"  {row.name}: vector={row.vector} dft={fmt_dft(row.dft)} pure_quartic={int(row.pure_quartic)}")
    print("reconstructions")
    for row in selector.reconstructions:
        print(
            f"  {row.name}: diagonal={row.diagonal_name} split={row.split_name} "
            f"plus_twice_edge={int(row.plus_recovers_twice_edge)} "
            f"minus_twice_opposite={int(row.minus_recovers_twice_opposite)} "
            f"recovered_dft={fmt_dft(row.recovered_dft)}"
        )
    print("routes")
    for row in selector.routes:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={selector.evidence_markers_ok}/{len(selector.evidence_markers)}")
    print(f"  edge_profiles_ok={selector.edge_profiles_ok}/4")
    print(f"  pure_quadratic_diagonals={selector.pure_quadratic_diagonals}")
    print(f"  pure_quartic_splits={selector.pure_quartic_splits}")
    print(f"  reconstruction_rows_ok={selector.reconstruction_rows_ok}/2")
    print(f"  support_routes={selector.support_routes}")
    print(f"  normalize_routes={selector.normalize_routes}")
    print(f"  repair_rows={selector.repair_rows}")
    print(f"  reject_rows={selector.reject_rows}")
    print(f"  current_source_theorems={selector.current_source_theorems}")
    print(f"p25_v2_q_split_quartic_selector_rows={int(selector.row_ok)}/1")
    return 0 if selector.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
