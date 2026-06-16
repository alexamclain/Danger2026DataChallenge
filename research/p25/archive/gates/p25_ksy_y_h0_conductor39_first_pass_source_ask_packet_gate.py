#!/usr/bin/env python3
"""Combined first-pass source ask packet for H0 and conductor-39.

The obligation matrix selects H0 and conductor-39 as the first-pass source
theorem targets.  The triage gate classifies candidate snippets.  This packet
turns those classifications into the compact ask/reject surface to use with an
expert, literature subagent, or theorem snippet before any DANGER3 extraction
work starts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from p25_ksy_y_h0_conductor39_first_pass_theorem_triage_gate import (
    FirstPassTheoremTriageRow,
    profile_h0_conductor39_first_pass_theorem_triage,
)


RESEARCH = Path("research/p25")

DEPENDENCY_MARKERS = (
    (
        RESEARCH / "p25_ksy_y_external_source_theorem_obligation_matrix_20260614.md",
        "ksy_y_external_source_theorem_obligation_matrix_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_minimal_closing_ask_packet_20260614.md",
        "ksy_y_h0_minimal_closing_ask_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_conductor39_minimal_theorem_query_packet_20260614.md",
        "ksy_y_conductor39_minimal_theorem_query_packet_rows=1/1",
    ),
    (
        RESEARCH / "p25_ksy_y_h0_conductor39_first_pass_theorem_triage_20260614.md",
        "ksy_y_h0_conductor39_first_pass_theorem_triage_rows=1/1",
    ),
)

ASK_TEXT = {
    "h0_source_certification_only": (
        "Does the source do more than certify a legal H0 product?"
    ),
    "h0_value_without_period156": (
        "If it gives an H0 value, does it also give support-period-156 "
        "branch/root/telescoping context?"
    ),
    "h0_divisor_missing_h90_boundary": (
        "If it gives an H0 divisor/additive statement, does it include the "
        "Hilbert-90 boundary to Norm_156(Y_507)?"
    ),
    "h0_divisor_additive_source_yes": (
        "Does it prove an exact divisor/additive identity for one exact legal "
        "78-over-78 H0 product, with Hilbert-90 boundary?"
    ),
    "conductor39_source_object_only": (
        "Does the source do more than identify the legal mixed U_chi/W object?"
    ),
    "conductor39_value_without_period156": (
        "If it gives a conductor-39 value, does it also give support-period-156 "
        "branch/root/telescoping context?"
    ),
    "conductor39_projection_shortcut": (
        "Does the claim collapse to prime-13, C169, projection, or axis-only data?"
    ),
    "conductor39_divisor_additive_source_yes": (
        "Does it prove a U_chi/W mixed divisor/additive theorem preserving the "
        "chi_3 tensor chi_13 object, Yang lift, and descent?"
    ),
}

ACCEPT_TEXT = {
    "h0_source_certification_only": "not enough; needs value-period156 or divisor/additive upgrade",
    "h0_value_without_period156": "repair by adding period-156 fixedness/telescoping",
    "h0_divisor_missing_h90_boundary": "repair by adding exact H90 boundary to Norm_156(Y_507)",
    "h0_divisor_additive_source_yes": "source-stage yes; route to DANGER3 framing and same-j bridge",
    "conductor39_source_object_only": "not enough; needs finite value or divisor/additive theorem",
    "conductor39_value_without_period156": "repair by adding period-156 fixedness/telescoping",
    "conductor39_projection_shortcut": "reject unless the mixed tensor is restored",
    "conductor39_divisor_additive_source_yes": "source-stage yes; route to DANGER3 framing and same-j bridge",
}


@dataclass(frozen=True)
class FirstPassSourceAskRow:
    name: str
    lane: str
    ask: str
    accept_or_repair: str
    candidate_command: str
    decision: str
    source_stage_closes: bool
    source_certified_only: bool
    period156_repair: bool
    boundary_repair: bool
    kill_route: bool
    first_missing_or_falsifier: str
    next_action: str
    ok: bool


@dataclass(frozen=True)
class FirstPassSourceAskPacket:
    dependency_markers_present: int
    dependency_markers_total: int
    triage_ok: bool
    rows: tuple[FirstPassSourceAskRow, ...]
    row_count: int
    h0_rows: int
    conductor39_rows: int
    source_stage_closing_rows: int
    source_certified_only_rows: int
    period156_repair_rows: int
    boundary_repair_rows: int
    kill_route_rows: int
    candidate_command_rows: int
    current_source_theorem_rows: int
    row_ok: bool


def marker_present(path: Path, marker: str) -> bool:
    return path.exists() and path.stat().st_size > 0 and marker in path.read_text()


def ask_row(row: FirstPassTheoremTriageRow) -> FirstPassSourceAskRow:
    return FirstPassSourceAskRow(
        name=row.name,
        lane=row.lane,
        ask=ASK_TEXT[row.name],
        accept_or_repair=ACCEPT_TEXT[row.name],
        candidate_command=row.candidate_command,
        decision=row.actual_decision,
        source_stage_closes=row.source_stage_closes,
        source_certified_only=row.source_certified_only,
        period156_repair=row.period156_repair,
        boundary_repair=row.boundary_repair,
        kill_route=row.kill_route,
        first_missing_or_falsifier=row.first_missing_or_falsifier,
        next_action=row.next_action,
        ok=row.ok and bool(row.candidate_command),
    )


def profile_h0_conductor39_first_pass_source_ask_packet() -> FirstPassSourceAskPacket:
    markers_present = sum(marker_present(path, marker) for path, marker in DEPENDENCY_MARKERS)
    triage = profile_h0_conductor39_first_pass_theorem_triage()
    rows = tuple(ask_row(row) for row in triage.rows)
    h0_rows = sum(row.lane == "H0" for row in rows)
    conductor_rows = sum(row.lane == "conductor39" for row in rows)
    closes = sum(row.source_stage_closes for row in rows)
    source_cert = sum(row.source_certified_only for row in rows)
    period_repair = sum(row.period156_repair for row in rows)
    boundary_repair = sum(row.boundary_repair for row in rows)
    kill = sum(row.kill_route for row in rows)
    commands = sum(bool(row.candidate_command) for row in rows)
    current_source = 0
    row_ok = (
        markers_present == len(DEPENDENCY_MARKERS)
        and triage.row_ok
        and len(rows) == 8
        and h0_rows == 4
        and conductor_rows == 4
        and closes == 2
        and source_cert == 2
        and period_repair == 2
        and boundary_repair == 1
        and kill == 1
        and commands == 8
        and current_source == 0
        and all(row.ok for row in rows)
    )
    return FirstPassSourceAskPacket(
        dependency_markers_present=markers_present,
        dependency_markers_total=len(DEPENDENCY_MARKERS),
        triage_ok=triage.row_ok,
        rows=rows,
        row_count=len(rows),
        h0_rows=h0_rows,
        conductor39_rows=conductor_rows,
        source_stage_closing_rows=closes,
        source_certified_only_rows=source_cert,
        period156_repair_rows=period_repair,
        boundary_repair_rows=boundary_repair,
        kill_route_rows=kill,
        candidate_command_rows=commands,
        current_source_theorem_rows=current_source,
        row_ok=row_ok,
    )


def main() -> int:
    profile = profile_h0_conductor39_first_pass_source_ask_packet()
    print("p25 KSY-y H0/conductor-39 first-pass source ask packet gate")
    print("dependencies")
    print(f"  dependency_markers_present={profile.dependency_markers_present}")
    print(f"  dependency_markers_total={profile.dependency_markers_total}")
    print(f"  triage_ok={int(profile.triage_ok)}")
    print("ask_rows")
    for row in profile.rows:
        print(
            "  "
            f"{row.name}: lane={row.lane} decision={row.decision} "
            f"closes={int(row.source_stage_closes)} cert_only={int(row.source_certified_only)} "
            f"period_repair={int(row.period156_repair)} "
            f"boundary_repair={int(row.boundary_repair)} kill={int(row.kill_route)}"
        )
        print(f"    ask={row.ask}")
        print(f"    accept={row.accept_or_repair}")
        print(f"    missing={row.first_missing_or_falsifier}")
        print(f"    next={row.next_action}")
        print(f"    command={row.candidate_command}")
    print("counts")
    print(f"  row_count={profile.row_count}")
    print(f"  h0_rows={profile.h0_rows}")
    print(f"  conductor39_rows={profile.conductor39_rows}")
    print(f"  source_stage_closing_rows={profile.source_stage_closing_rows}")
    print(f"  source_certified_only_rows={profile.source_certified_only_rows}")
    print(f"  period156_repair_rows={profile.period156_repair_rows}")
    print(f"  boundary_repair_rows={profile.boundary_repair_rows}")
    print(f"  kill_route_rows={profile.kill_route_rows}")
    print(f"  candidate_command_rows={profile.candidate_command_rows}")
    print(f"  current_source_theorem_rows={profile.current_source_theorem_rows}")
    print("interpretation")
    print("  first_pass_ask_has_two_source_stage_yes_shapes=1")
    print("  bare_source_certification_remains_nonclosing=1")
    print("  value_rows_need_period156_context=1")
    print("  h0_divisor_rows_need_h90_boundary=1")
    print("  conductor39_projection_shortcut_is_killed=1")
    print(
        "ksy_y_h0_conductor39_first_pass_source_ask_packet_rows="
        f"{int(profile.row_ok)}/1"
    )
    if not profile.row_ok:
        raise SystemExit("H0/conductor-39 first-pass source ask packet regression failed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
