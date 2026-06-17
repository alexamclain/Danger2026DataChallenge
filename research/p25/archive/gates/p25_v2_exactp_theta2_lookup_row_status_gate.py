#!/usr/bin/env python3
"""Validate the exact-P/theta2 heavy lookup-row status artifact."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel: str
    marker: str
    ok: bool


@dataclass(frozen=True)
class StatusRow:
    name: str
    accepted_hook: str
    current_status: str
    first_falsifier: str
    decision: str


EVIDENCE_INPUTS = (
    (
        "priority1_source_lookup_capsule",
        "evidence/p25_v2_priority1_source_lookup_capsule_20260617.md",
        "p25_v2_priority1_source_lookup_capsule_rows=1/1",
    ),
    (
        "exactp_minimal_hook",
        "evidence/p25_v2_exactp_minimal_hook_20260616.md",
        "p25_v2_exactp_minimal_hook_rows=1/1",
    ),
    (
        "exactp_orientation_branch_router",
        "evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
        "p25_v2_exactp_orientation_branch_router_rows=1/1",
    ),
    (
        "exactp_candidate_sweep",
        "evidence/p25_v2_exactp_candidate_sweep_20260617.md",
        "p25_v2_exactp_candidate_sweep_rows=1/1",
    ),
    (
        "exactp_to_unified_target_spine",
        "evidence/p25_v2_exactp_to_unified_target_spine_20260616.md",
        "p25_v2_exactp_to_unified_target_spine_rows=1/1",
    ),
    (
        "reverse_exactp_information_loss",
        "evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
        "p25_v2_reverse_exactp_information_loss_rows=1/1",
    ),
    (
        "theta2_period156_support_contract",
        "evidence/p25_v2_theta2_period156_support_contract_20260616.md",
        "p25_v2_theta2_period156_support_contract_rows=1/1",
    ),
    (
        "sprang_theta2_source_intake",
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
    (
        "sprang_distribution_instantiation_falsifier",
        "evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md",
        "p25_v2_sprang_distribution_instantiation_falsifier_rows=1/1",
    ),
    (
        "kubert_lang_selector_boundary",
        "evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
        "p25_v2_kubert_lang_selector_boundary_rows=1/1",
    ),
    (
        "kubert_lang_external_source_boundary",
        "evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
        "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
    ),
    (
        "source_family_gap_matrix",
        "evidence/p25_v2_source_family_gap_matrix_20260616.md",
        "p25_v2_source_family_gap_matrix_rows=1/1",
    ),
    (
        "source_action_registry",
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
)


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def evidence_markers(root: Path) -> tuple[EvidenceMarker, ...]:
    markers: list[EvidenceMarker] = []
    for name, rel, marker in EVIDENCE_INPUTS:
        text = read(root / rel)
        markers.append(EvidenceMarker(name, rel, marker, marker in text))
    return tuple(markers)


def status_rows() -> tuple[StatusRow, ...]:
    return (
        StatusRow(
            "compact_cdk_orientation_theorem",
            "arithmetic source theorem emitting compact C,D,K,orientation with one accepted raw center/reverse branch, exact equal-weight 75-atom data, and the 75->300->12->312->156 bridge",
            "live_not_in_hand",
            "branchless orientation word, wrong center, wrong D, nonprimitive K, nonuniform atoms, raw KL exponent balance, or finite packet without source",
            "continue_only_on_exact_branch_theorem",
        ),
        StatusRow(
            "equal_weight_75_atom_theorem",
            "challenge-legal theorem for the exact equal-weight 75-atom normalized-y product with orientation and bridge data",
            "live_not_in_hand",
            "normalized-y vocabulary, ray-class generation, atom fixture, or finite support rigidity without arithmetic producer theorem",
            "continue_only_with_arithmetic_source",
        ),
        StatusRow(
            "theta2_or_theta2_inverse_payload",
            "exact theta2/theta2-inverse divisor-additive payload or compact KSY theta2 certificate with period-156 branch/root/telescoping and bridge data",
            "support_payload_live_not_in_hand",
            "theta2 value-only unit, ambient-period-780 value, branchless payload, Sprang D=2 support, or theta vocabulary without sparse p25 packet",
            "continue_only_on_exact_theta2_payload",
        ),
        StatusRow(
            "kubert_lang_primitive_selector",
            "theorem-legal primitive word z^121*(1+z+z^2)*(1-z^263) or row-labeled mixed C3 x C169 selector with p25 orientation",
            "finite_selector_boundary_not_source_closer",
            "generic KL generator theorem, theorem-K congruence context, raw exponent balance, C169 projection, or unoriented primitive word",
            "continue_only_if_kl_source_emits_exact_selector",
        ),
        StatusRow(
            "sprang_sparse_specialization",
            "Sprang/Kronecker specialization selecting base, K_trace, D_segment, T edge, theta2 direction, and p25 branch/orientation for the sparse payload",
            "support_source_no_specialization",
            "full kernel/torsion distribution theorem, broad D=2 support, p-adic theta, de Rham polylog, or cohomology vocabulary without sparse selector",
            "continue_only_on_sparse_specialization",
        ),
        StatusRow(
            "reverse_reconstruction_theorem",
            "explicit theorem reconstructing C,D,K,orientation, equal-weight 75 atoms, or accepted theta2 payload from a unified support-156 theorem",
            "reverse_not_proved",
            "unified H0/conductor-39 theorem alone, Y_507 bridge alone, or support-156 value/divisor theorem without exact-P selector data",
            "route_unified_hits_to_extraction_not_exactp",
        ),
    )


def evidence_consistency(root: Path) -> bool:
    exactp = read(root / "evidence/p25_v2_exactp_candidate_sweep_20260617.md")
    minimal = read(root / "evidence/p25_v2_exactp_minimal_hook_20260616.md")
    theta2 = read(root / "evidence/p25_v2_theta2_period156_support_contract_20260616.md")
    sprang = read(root / "evidence/p25_v2_sprang_theta2_source_intake_20260616.md")
    sprang_dist = read(root / "evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md")
    kl = read(root / "evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md")
    source_gap = read(root / "evidence/p25_v2_source_family_gap_matrix_20260616.md")
    action = read(root / "evidence/p25_v2_source_action_registry_20260616.md")
    reverse = read(root / "evidence/p25_v2_reverse_exactp_information_loss_20260616.md")
    interface = read(root / "evidence/p25_v2_exactp_theorem_interface_contract_20260616.md")
    return (
        "surviving_exactp_intake_families = 4" in exactp
        and "current_exactp_source_theorems = 0" in exactp
        and "current_source_stage_closers = 0" in exactp
        and "accepted_routes = 5" in minimal
        and "current_exactp_source_theorems = 0" in minimal
        and "current_arithmetic_producers = 0" in theta2
        and "source_stage_closers = 0" in theta2
        and "exact_theta2_payload_named = no" in sprang
        and "source_stage_closers = 0" in sprang
        and "direct_instantiation_closers = 0" in sprang_dist
        and "current_kl_source_theorems = 0" in kl
        and "exactp_upstream_theorems = 0" in source_gap
        and "exactp_heavy_route" in action
        and "current_source_stage_closers = 0" in action
        and "reverse_unified_to_exactp = rejected without extra selector structure" in reverse
        and "still_missing = challenge-legal Robert/Siegel/Kubert-Lang/KSY identity" in interface
    )


def build_check(root: Path) -> tuple[tuple[EvidenceMarker, ...], tuple[StatusRow, ...], bool]:
    markers = evidence_markers(root)
    rows = status_rows()
    row_ok = (
        all(marker.ok for marker in markers)
        and evidence_consistency(root)
        and len(rows) == 6
        and sum(row.current_status == "live_not_in_hand" for row in rows) == 2
        and sum("theta2" in row.name for row in rows) == 1
        and sum("kubert" in row.name for row in rows) == 1
        and sum("sprang" in row.name for row in rows) == 1
        and sum(row.current_status == "reverse_not_proved" for row in rows) == 1
    )
    return markers, rows, row_ok


def main() -> int:
    root = research_root()
    markers, rows, row_ok = build_check(root)
    print("p25 v2 exact-P/theta2 lookup-row status")
    for marker in markers:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'missing'}")
    print(f"evidence_consistency={int(evidence_consistency(root))}")
    print("rows")
    for row in rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    current_status={row.current_status}")
        print(f"    accepted_hook={row.accepted_hook}")
        print(f"    first_falsifier={row.first_falsifier}")
    print("counts")
    print(f"evidence_markers_ok={sum(marker.ok for marker in markers)}/{len(markers)}")
    print(f"status_rows={len(rows)}")
    print("surviving_exactp_intake_families=4")
    print("current_exactp_source_theorems=0")
    print("current_theta2_arithmetic_producers=0")
    print("current_kl_source_theorems=0")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_exactp_theta2_lookup_row_status_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
