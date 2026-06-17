#!/usr/bin/env python3
"""Validate partial-projector / two-edge selector routing for p25."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from pathlib import Path


P25 = 10000000000000000000000013
EDGE_ORDER = ("m1", "m2", "m4", "m8")


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class PairSelector:
    name: str
    pair: tuple[str, str]
    complement: tuple[str, str]
    pair_vector: tuple[int, int, int, int]
    complement_vector: tuple[int, int, int, int]
    pair_boundary_scale: int
    complement_boundary_scale: int
    difference_boundary_scale: int
    doubled_edge_identities_ok: bool


@dataclass(frozen=True)
class IntakeRoute:
    name: str
    decision: str
    ok: bool


@dataclass(frozen=True)
class PartialProjectorSelector:
    evidence_markers: tuple[EvidenceMarker, ...]
    selectors: tuple[PairSelector, ...]
    two_edge_pairs: int
    pair_boundary_scales_ok: int
    difference_boundary_scales_ok: int
    doubled_edge_identity_count: int
    p_mod_2: int
    gcd_2_p_minus_1: int
    accepted_routes: tuple[IntakeRoute, ...]
    repair_routes: tuple[IntakeRoute, ...]
    current_source_theorems: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    marker_path = Path(path)
    text = marker_path.read_text() if marker_path.exists() else ""
    return EvidenceMarker(name=name, path=marker_path, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "edge_projector_denominator",
            "research/p25/evidence/p25_v2_edge_projector_denominator_20260616.md",
            "p25_v2_edge_projector_denominator_rows=1/1",
        ),
        marker(
            "row_quotient_invariant_bridge",
            "research/p25/evidence/p25_v2_row_quotient_invariant_bridge_20260616.md",
            "p25_v2_row_quotient_invariant_bridge_rows=1/1",
        ),
        marker(
            "row_square_root_ambiguity",
            "research/p25/evidence/p25_v2_row_square_root_ambiguity_20260616.md",
            "p25_v2_row_square_root_ambiguity_rows=1/1",
        ),
        marker(
            "minimal_expert_ask",
            "research/p25/evidence/p25_v2_minimal_expert_ask_20260616.md",
            "p25_v2_minimal_expert_ask_rows=1/1",
        ),
    )


def edge_vector(edge: str) -> tuple[int, int, int, int]:
    return tuple(1 if name == edge else 0 for name in EDGE_ORDER)


def add_vectors(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(a + b for a, b in zip(left, right))


def sub_vectors(left: tuple[int, int, int, int], right: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(a - b for a, b in zip(left, right))


def scale_vector(scale: int, vector: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    return tuple(scale * value for value in vector)


def selector_name(pair: tuple[str, str]) -> str:
    labels = {
        ("m1", "m2"): "odd_row_pair",
        ("m4", "m8"): "even_row_pair",
        ("m1", "m8"): "right_column_pair",
        ("m2", "m4"): "left_column_pair",
        ("m1", "m4"): "diagonal_pair_a",
        ("m2", "m8"): "diagonal_pair_b",
    }
    return labels.get(pair, "pair_" + "_".join(pair))


def pair_selectors() -> tuple[PairSelector, ...]:
    selectors = []
    for pair in combinations(EDGE_ORDER, 2):
        pair_vector = add_vectors(edge_vector(pair[0]), edge_vector(pair[1]))
        complement = tuple(edge for edge in EDGE_ORDER if edge not in pair)
        complement_vector = add_vectors(edge_vector(complement[0]), edge_vector(complement[1]))
        pair_difference = sub_vectors(edge_vector(pair[0]), edge_vector(pair[1]))
        doubled_first = add_vectors(pair_vector, pair_difference)
        doubled_second = sub_vectors(pair_vector, pair_difference)
        identities_ok = (
            doubled_first == scale_vector(2, edge_vector(pair[0]))
            and doubled_second == scale_vector(2, edge_vector(pair[1]))
        )
        selectors.append(
            PairSelector(
                name=selector_name(pair),
                pair=pair,
                complement=complement,
                pair_vector=pair_vector,
                complement_vector=complement_vector,
                pair_boundary_scale=sum(pair_vector),
                complement_boundary_scale=sum(complement_vector),
                difference_boundary_scale=sum(pair_difference),
                doubled_edge_identities_ok=identities_ok,
            )
        )
    return tuple(selectors)


def accepted_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("direct_one_edge_theorem", "source_stage_candidate_if_theorem_present", True),
        IntakeRoute("pair_plus_difference_with_oriented_square_root", "normalize_oriented_root_then_intake", True),
    )


def repair_routes() -> tuple[IntakeRoute, ...]:
    return (
        IntakeRoute("two_edge_pair_aggregate_only", "repair_2W_boundary_not_one_edge", True),
        IntakeRoute("pair_difference_only", "repair_zero_boundary_selector_missing", True),
        IntakeRoute("pair_plus_difference_without_square_root", "repair_sign_or_root_missing", True),
        IntakeRoute("complement_pair_choice_only", "repair_pair_selector_not_edge_selector", True),
    )


def build_screen() -> PartialProjectorSelector:
    markers = evidence_markers()
    selectors = pair_selectors()
    pair_boundary_ok = sum(
        row.pair_boundary_scale == 2 and row.complement_boundary_scale == 2
        for row in selectors
    )
    difference_boundary_ok = sum(row.difference_boundary_scale == 0 for row in selectors)
    doubled_identity_count = sum(row.doubled_edge_identities_ok for row in selectors)
    p_mod_2 = P25 % 2
    gcd_2 = 2 if (P25 - 1) % 2 == 0 else 1
    accepted = accepted_routes()
    repairs = repair_routes()
    current_source_theorems = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(selectors) == 6
        and pair_boundary_ok == 6
        and difference_boundary_ok == 6
        and doubled_identity_count == 6
        and p_mod_2 == 1
        and gcd_2 == 2
        and len(accepted) == 2
        and all(row.ok for row in accepted)
        and len(repairs) == 4
        and all(row.ok for row in repairs)
        and current_source_theorems == 0
        and current_submission_ready == 0
    )
    return PartialProjectorSelector(
        evidence_markers=markers,
        selectors=selectors,
        two_edge_pairs=len(selectors),
        pair_boundary_scales_ok=pair_boundary_ok,
        difference_boundary_scales_ok=difference_boundary_ok,
        doubled_edge_identity_count=doubled_identity_count,
        p_mod_2=p_mod_2,
        gcd_2_p_minus_1=gcd_2,
        accepted_routes=accepted,
        repair_routes=repairs,
        current_source_theorems=current_source_theorems,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    screen = build_screen()
    print("p25 v2 partial projector selector")
    for marker_row in screen.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print(f"edge_order={EDGE_ORDER}")
    print("two_edge_selectors")
    for selector in screen.selectors:
        pair = ",".join(selector.pair)
        complement = ",".join(selector.complement)
        print(
            f"  {selector.name}: pair=({pair}) complement=({complement}) "
            f"pair_boundary={selector.pair_boundary_scale}W "
            f"difference_boundary={selector.difference_boundary_scale}W "
            f"doubled_edge_identities={int(selector.doubled_edge_identities_ok)}"
        )
    print("p25_power_data")
    print(f"  p_mod_2={screen.p_mod_2}")
    print(f"  gcd_2_p_minus_1={screen.gcd_2_p_minus_1}")
    print("accepted_routes")
    for route in screen.accepted_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("repair_routes")
    for route in screen.repair_routes:
        print(f"  {route.name}: decision={route.decision}")
    print("checks")
    print(f"  evidence_markers_ok={sum(row.ok for row in screen.evidence_markers)}/{len(screen.evidence_markers)}")
    print(f"  two_edge_pairs={screen.two_edge_pairs}")
    print(f"  pair_boundary_scales_ok={screen.pair_boundary_scales_ok}/6")
    print(f"  difference_boundary_scales_ok={screen.difference_boundary_scales_ok}/6")
    print(f"  doubled_edge_identities_ok={screen.doubled_edge_identity_count}/6")
    print(f"  accepted_routes={len(screen.accepted_routes)}")
    print(f"  repair_routes={len(screen.repair_routes)}")
    print(f"  current_source_theorems={screen.current_source_theorems}")
    print(f"  current_submission_ready={screen.current_submission_ready}")
    print(f"p25_v2_partial_projector_selector_rows={int(screen.row_ok)}/1")
    return 0 if screen.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
