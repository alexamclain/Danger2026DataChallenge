#!/usr/bin/env python3
"""Recheck the primitive conductor-39 power relation under the v2 power intake."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10_000_000_000_000_000_000_000_013


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class PowerRecheckRow:
    name: str
    input_shape: str
    decision: str
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class PrimitiveCharacterPowerRecheck:
    markers: tuple[EvidenceMarker, ...]
    rows: tuple[PowerRecheckRow, ...]
    cube_map_bijective: bool
    sixth_root_ambiguous: bool
    old_relation_is_exponent_word: bool
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def read(path: str) -> str:
    p = Path(path)
    return p.read_text(errors="replace") if p.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    return EvidenceMarker(name=name, path=Path(path), marker=needle, ok=needle in read(path))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "primitive_character_unit_note",
            "research/p25/archive/notes/p25_ksy_y_yang_y507_conductor39_primitive_character_unit_20260614.md",
            "ksy_y_yang_y507_conductor39_primitive_character_unit_rows=1/1",
        ),
        marker(
            "power_normalized_theorem_intake",
            "research/p25/evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
            "p25_v2_power_normalized_theorem_intake_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
        marker(
            "first_pass_expert_intake_packet",
            "research/p25/evidence/p25_v2_first_pass_expert_intake_packet_20260616.md",
            "p25_v2_first_pass_expert_intake_packet_rows=1/1",
        ),
    )


def recheck_rows() -> tuple[PowerRecheckRow, ...]:
    return (
        PowerRecheckRow(
            name="primitive_unit_relation",
            input_shape="U_chi=-chi_39 with V_bal=U_chi^3 and W=U_chi^6 in exponent notation",
            decision="support_identity_not_power_value_theorem",
            first_missing_or_falsifier="old artifact explicitly says primitive normalization is not a finite-field value/divisor theorem",
            ok=True,
        ),
        PowerRecheckRow(
            name="v_bal_cube_relation",
            input_shape="V_bal=U_chi^3 source-word relation",
            decision="repair_exact_Fp_value_for_one_legal_row_missing",
            first_missing_or_falsifier="cube map is bijective, but only after an exact F_p value for a row power exists",
            ok=True,
        ),
        PowerRecheckRow(
            name="w_sixth_relation",
            input_shape="W=U_chi^6 source-word relation",
            decision="repair_sign_and_current_boundary_missing",
            first_missing_or_falsifier="sixth roots have kernel 2 and scaled-boundary data is not the current row boundary",
            ok=True,
        ),
        PowerRecheckRow(
            name="future_primitive_value_theorem",
            input_shape="exact arithmetic theorem giving an F_p value for U_chi^3, R_m^3, or another uniquely invertible row power",
            decision="route_only_if_it_names_one_legal_row_and_boundary_bridge",
            first_missing_or_falsifier="must attach the exact value to one of m={1,2,4,8} or a row-labeled theorem with Norm_156(Y_507) boundary",
            ok=True,
        ),
    )


def build_recheck() -> PrimitiveCharacterPowerRecheck:
    markers = evidence_markers()
    rows = recheck_rows()
    old_note = read("research/p25/archive/notes/p25_ksy_y_yang_y507_conductor39_primitive_character_unit_20260614.md")
    old_relation_is_exponent_word = (
        "V_bal = U_chi^3" in old_note
        and "W     = U_chi^6" in old_note
        and "not the finite-field value/divisor" in old_note
    )
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and len(rows) == 4
        and all(row.ok for row in rows)
        and gcd(3, P25 - 1) == 1
        and gcd(6, P25 - 1) == 2
        and old_relation_is_exponent_word
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )
    return PrimitiveCharacterPowerRecheck(
        markers=markers,
        rows=rows,
        cube_map_bijective=gcd(3, P25 - 1) == 1,
        sixth_root_ambiguous=gcd(6, P25 - 1) == 2,
        old_relation_is_exponent_word=old_relation_is_exponent_word,
        current_source_stage_closers=current_source_stage_closers,
        current_submission_ready=current_submission_ready,
        row_ok=row_ok,
    )


def main() -> int:
    recheck = build_recheck()
    print("p25 v2 primitive character power recheck")
    for marker_row in recheck.markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("rows")
    for row in recheck.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    input={row.input_shape}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("checks")
    print(f"  cube_map_bijective={int(recheck.cube_map_bijective)}")
    print(f"  sixth_root_ambiguous={int(recheck.sixth_root_ambiguous)}")
    print(f"  old_relation_is_exponent_word={int(recheck.old_relation_is_exponent_word)}")
    print(f"  current_source_stage_closers={recheck.current_source_stage_closers}")
    print(f"  current_submission_ready={recheck.current_submission_ready}")
    print(f"p25_v2_primitive_character_power_recheck_rows={int(recheck.row_ok)}/1")
    return 0 if recheck.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
