#!/usr/bin/env python3
"""Audit the v2 cockpit marker-to-gate manifest.

The lightweight cockpit validates evidence markers rather than replaying every
archived theorem gate.  This manifest gate checks the trust boundary around
that choice: each cockpit evidence marker has a matching gate file, documented
heavy recomputation gates are named in AGENTS.md, and the exact-P spine gate
has the archived harness import path needed for direct repo-root execution.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


COCKPIT_GATE = Path("research/p25/archive/gates/p25_v2_wiki_cockpit_lightweight_check_gate.py")
EXACTP_SPINE_GATE = Path("research/p25/archive/gates/p25_v2_exactp_to_unified_target_spine_gate.py")
EVIDENCE_PATH = Path("research/p25/evidence/p25_v2_cockpit_gate_manifest_20260616.md")
MARKER = "p25_v2_cockpit_gate_manifest_rows=1/1"


@dataclass(frozen=True)
class CockpitGateManifest:
    cockpit_gate_present: bool
    evidence_present: bool
    evidence_marker_present: bool
    cockpit_marker_count: int
    official_vpp_marker_present: bool
    missing_gate_files: tuple[str, ...]
    heavy_gate_count: int
    heavy_gates_documented: bool
    exactp_spine_harness_path_present: bool
    exactp_spine_sys_path_present: bool
    direct_gate_manifest_ok: bool
    row_ok: bool


def repo_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd
    for parent in (cwd, *cwd.parents):
        if (parent / "research/p25").exists():
            return parent
    raise FileNotFoundError("run from repo root or inside repo")


def cockpit_lists(root: Path) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    text = (root / COCKPIT_GATE).read_text()
    tree = ast.parse(text)
    markers: tuple[tuple[str, str], ...] = ()
    heavy: tuple[str, ...] = ()
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "EVIDENCE_MARKERS":
                markers = ast.literal_eval(node.value)
            if isinstance(target, ast.Name) and target.id == "HEAVY_RECOMPUTATION_GATES":
                heavy = ast.literal_eval(node.value)
    return markers, heavy


def expected_gate_path(root: Path, evidence_rel: str) -> Path:
    stem = Path(evidence_rel).name.removesuffix(".md")
    prefix, sep, suffix = stem.rpartition("_")
    if sep and len(suffix) == 8 and suffix.isdigit():
        stem = prefix
    return root / "research/p25/archive/gates" / f"{stem}_gate.py"


def build_manifest(root: Path) -> CockpitGateManifest:
    cockpit_present = (root / COCKPIT_GATE).exists()
    markers, heavy = cockpit_lists(root) if cockpit_present else ((), ())
    missing = tuple(
        str(expected_gate_path(root, evidence_rel).relative_to(root))
        for evidence_rel, _ in markers
        if not expected_gate_path(root, evidence_rel).exists()
    )
    agents_text = (root / "research/p25/AGENTS.md").read_text()
    heavy_documented = bool(heavy) and all(gate in agents_text for gate in heavy)
    spine_text = (root / EXACTP_SPINE_GATE).read_text() if (root / EXACTP_SPINE_GATE).exists() else ""
    harness_path_present = "HARNESS_DIR = GATE_DIR.parent / \"harness\"" in spine_text
    sys_path_present = "sys.path.insert(0, str(HARNESS_DIR))" in spine_text
    evidence_text = (root / EVIDENCE_PATH).read_text() if (root / EVIDENCE_PATH).exists() else ""
    evidence_marker = MARKER in evidence_text
    official_vpp_marker = any(
        marker == "p25_v2_official_vpp_regression_rows=1/1"
        for _, marker in markers
    )
    direct_manifest_ok = (
        cockpit_present
        and len(markers) >= 92
        and len(missing) == 0
        and len(heavy) == 2
        and heavy_documented
        and harness_path_present
        and sys_path_present
    )
    row_ok = direct_manifest_ok and (root / EVIDENCE_PATH).exists() and evidence_marker
    return CockpitGateManifest(
        cockpit_gate_present=cockpit_present,
        evidence_present=(root / EVIDENCE_PATH).exists(),
        evidence_marker_present=evidence_marker,
        cockpit_marker_count=len(markers),
        official_vpp_marker_present=official_vpp_marker,
        missing_gate_files=missing,
        heavy_gate_count=len(heavy),
        heavy_gates_documented=heavy_documented,
        exactp_spine_harness_path_present=harness_path_present,
        exactp_spine_sys_path_present=sys_path_present,
        direct_gate_manifest_ok=direct_manifest_ok,
        row_ok=row_ok,
    )


def main() -> int:
    manifest = build_manifest(repo_root())
    print("p25 v2 cockpit gate manifest")
    print(f"cockpit_gate_present={int(manifest.cockpit_gate_present)}")
    print(f"evidence_present={int(manifest.evidence_present)}")
    print(f"evidence_marker_present={int(manifest.evidence_marker_present)}")
    print(f"cockpit_marker_count={manifest.cockpit_marker_count}")
    print(f"official_vpp_marker_present={int(manifest.official_vpp_marker_present)}")
    print(f"missing_gate_files={len(manifest.missing_gate_files)}")
    for missing in manifest.missing_gate_files:
        print(f"  missing={missing}")
    print(f"heavy_gate_count={manifest.heavy_gate_count}")
    print(f"heavy_gates_documented={int(manifest.heavy_gates_documented)}")
    print(
        "exactp_spine_harness_path_present="
        f"{int(manifest.exactp_spine_harness_path_present)}"
    )
    print(f"exactp_spine_sys_path_present={int(manifest.exactp_spine_sys_path_present)}")
    print(f"direct_gate_manifest_ok={int(manifest.direct_gate_manifest_ok)}")
    print(f"p25_v2_cockpit_gate_manifest_rows={int(manifest.row_ok)}/1")
    return 0 if manifest.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
