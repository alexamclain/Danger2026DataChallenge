#!/usr/bin/env python3
"""Validate the extended unique-power intake addendum for p25."""

from __future__ import annotations

from dataclasses import dataclass
from math import gcd
from pathlib import Path


P25 = 10**25 + 13
STANDARD_POWER_HOOKS = (3, 5, 13, 39)
EXTENDED_POWER_HOOKS = (75, 169, 507)
REPAIR_POWER_HOOKS = (2, 4, 6, 11, 22, 44, 156, 780)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class UniquePowerRow:
    exponent: int
    inverse_exponent: int
    source_route_pinned: bool
    intake_decision: str


EVIDENCE_INPUTS = (
    (
        "fpstar_branch_factorization",
        "evidence/p25_v2_fpstar_branch_factorization_20260617.md",
        "p25_v2_fpstar_branch_factorization_rows=1/1",
    ),
    (
        "power_normalized_intake",
        "evidence/p25_v2_power_normalized_theorem_intake_20260616.md",
        "p25_v2_power_normalized_theorem_intake_rows=1/1",
    ),
    (
        "normalizer_lookup_status",
        "evidence/p25_v2_normalizer_lookup_row_status_20260617.md",
        "p25_v2_normalizer_lookup_row_status_rows=1/1",
    ),
    (
        "source_stage_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    rows: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        path = root / rel
        text = path.read_text() if path.exists() else ""
        rows.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(rows)


def unique_power_rows() -> tuple[UniquePowerRow, ...]:
    rows: list[UniquePowerRow] = []
    for exponent in STANDARD_POWER_HOOKS:
        rows.append(
            UniquePowerRow(
                exponent,
                pow(exponent, -1, P25 - 1),
                True,
                "live_named_power_normalizer",
            )
        )
    for exponent in EXTENDED_POWER_HOOKS:
        rows.append(
            UniquePowerRow(
                exponent,
                pow(exponent, -1, P25 - 1),
                False,
                "accept_if_exact_source_theorem_arrives_but_do_not_search_broadly",
            )
        )
    return tuple(rows)


def canonical_pages_ok(root: Path) -> bool:
    checks = (
        ("frontier.md", "extended unique-power intake"),
        ("lanes/h0.md", "extended unique-power intake"),
        ("lanes/conductor39.md", "extended unique-power intake"),
    )
    for rel, needle in checks:
        path = root / rel
        if not path.exists() or needle not in path.read_text():
            return False
    return True


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[UniquePowerRow, ...], bool]:
    markers = evidence_markers(root)
    rows = unique_power_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and canonical_pages_ok(root)
        and tuple(row.exponent for row in rows)
        == (*STANDARD_POWER_HOOKS, *EXTENDED_POWER_HOOKS)
        and all(gcd(row.exponent, P25 - 1) == 1 for row in rows)
        and all((row.exponent * row.inverse_exponent) % (P25 - 1) == 1 for row in rows)
        and all(gcd(exponent, P25 - 1) > 1 for exponent in REPAIR_POWER_HOOKS)
        and sum(row.source_route_pinned for row in rows) == len(STANDARD_POWER_HOOKS)
        and sum(not row.source_route_pinned for row in rows) == len(EXTENDED_POWER_HOOKS)
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 extended unique-power intake")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"canonical_pages_ok={int(canonical_pages_ok(root))}")
    print("unique_power_rows")
    for row in rows:
        print(
            f"  e={row.exponent}: inverse={row.inverse_exponent} "
            f"source_route_pinned={int(row.source_route_pinned)} "
            f"decision={row.intake_decision}"
        )
    print("repair_power_hooks")
    for exponent in REPAIR_POWER_HOOKS:
        print(f"  e={exponent}: kernel={gcd(exponent, P25 - 1)}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"standard_named_power_hooks={len(STANDARD_POWER_HOOKS)}")
    print(f"extended_exact_power_hooks={len(EXTENDED_POWER_HOOKS)}")
    print("current_extended_power_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_extended_unique_power_intake_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
