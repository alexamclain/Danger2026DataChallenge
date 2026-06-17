#!/usr/bin/env python3
"""Validate the exact-P/theta2 producer-obstruction matrix.

This gate keeps the heavy exact-P route honest after the finite packet became
rigid.  It checks that the promoted evidence separates theorem-producing
clauses from support vocabulary, finite selector data, and value-only claims.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


MARKER = "p25_v2_exactp_theta2_producer_obstruction_rows=1/1"

EVIDENCE_MARKERS = (
    (
        "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
        "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
    ),
    (
        "evidence/p25_v2_theta2_period156_support_contract_20260616.md",
        "p25_v2_theta2_period156_support_contract_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
        "p25_v2_exactp_orientation_branch_router_rows=1/1",
    ),
    (
        "evidence/p25_v2_sprang_theta2_source_intake_20260616.md",
        "p25_v2_sprang_theta2_source_intake_rows=1/1",
    ),
    (
        "evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md",
        "p25_v2_sprang_distribution_instantiation_falsifier_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_primitive_word_source_split_20260617.md",
        "p25_v2_kl_primitive_word_source_split_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_source_split_local_scan_20260617.md",
        "p25_v2_kl_source_split_local_scan_rows=1/1",
    ),
    (
        "evidence/p25_v2_kl_cyclotomic_norm_route_audit_20260617.md",
        "p25_v2_kl_cyclotomic_norm_route_audit_rows=1/1",
    ),
    (
        "evidence/p25_v2_exactp_spine_payload_separation_20260617.md",
        "p25_v2_exactp_spine_payload_separation_rows=1/1",
    ),
    (
        "evidence/p25_v2_source_action_registry_20260616.md",
        "p25_v2_source_action_registry_rows=1/1",
    ),
)


@dataclass(frozen=True)
class ProducerRow:
    name: str
    accepted_if: str
    still_missing: str
    decision: str


@dataclass(frozen=True)
class ObstructionRow:
    name: str
    overclaim: str
    falsifier: str
    decision: str


def research_root() -> Path:
    cwd = Path.cwd()
    if (cwd / "research/p25").exists():
        return cwd / "research/p25"
    if (cwd / "frontier.md").exists() and (cwd / "evidence").exists():
        return cwd
    raise FileNotFoundError("run from repo root or research/p25")


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def evidence_markers_ok(root: Path) -> tuple[int, int]:
    ok = 0
    for rel, marker in EVIDENCE_MARKERS:
        text = read(root / rel)
        ok += int(marker in text)
    return ok, len(EVIDENCE_MARKERS)


def producer_rows() -> tuple[ProducerRow, ...]:
    return (
        ProducerRow(
            name="compact_cdk_orientation_branch",
            accepted_if=(
                "arithmetic theorem emits C,D,K plus one accepted raw branch "
                "and the theta2/theta2-inverse divisor-additive payload"
            ),
            still_missing="source theorem for one accepted branch",
            decision="positive_exactp_producer_if_source_theorem_exists",
        ),
        ProducerRow(
            name="equal_weight_75_atom_theorem",
            accepted_if=(
                "challenge-legal theorem emits the exact equal-weight 75-atom "
                "normalized-y product with orientation and bridge"
            ),
            still_missing="arithmetic source theorem selecting the fixed atoms",
            decision="positive_exactp_producer_if_source_theorem_exists",
        ),
        ProducerRow(
            name="theta2_divisor_additive_payload",
            accepted_if=(
                "exact theta2 or theta2-inverse divisor/additive data includes "
                "period-156 branch/root/telescoping and the bridge"
            ),
            still_missing="theta2 arithmetic producer, not only finite support",
            decision="positive_theta2_producer_if_source_theorem_exists",
        ),
        ProducerRow(
            name="kl_primitive_word_or_h90_chain",
            accepted_if=(
                "theorem-legal oriented word z^121*(1+z+z^2)*(1-z^263), "
                "or the three-term H90 chain with boundary step and K-trace"
            ),
            still_missing="arithmetic source theorem plus raw K-trace/theta2 bridge",
            decision="positive_kl_producer_if_source_theorem_exists",
        ),
        ProducerRow(
            name="sprang_sparse_specialization",
            accepted_if=(
                "Sprang/Kronecker specialization selects base, K_trace, "
                "D_segment, T edge, theta2 direction, and p25 branch"
            ),
            still_missing="collapse from full distribution to sparse p25 packet",
            decision="positive_sprang_producer_if_source_theorem_exists",
        ),
        ProducerRow(
            name="explicit_reverse_reconstruction",
            accepted_if=(
                "theorem reconstructs C,D,K/orientation, the 75 atoms, or an "
                "accepted theta2 payload from a unified support-156 theorem"
            ),
            still_missing="reverse selector theorem",
            decision="positive_reverse_route_if_explicit_selector_theorem_exists",
        ),
    )


def obstruction_rows() -> tuple[ObstructionRow, ...]:
    return (
        ObstructionRow(
            name="finite_payload_without_source",
            overclaim="rigid finite support or local fixture already proves exact-P",
            falsifier="finite payloads are targets; no arithmetic producer theorem is present",
            decision="repair_arithmetic_source_missing",
        ),
        ObstructionRow(
            name="generic_kl_or_modular_unit_source",
            overclaim="KL generator, cyclotomic-unit, or Robert-unit context emits the p25 selector",
            falsifier="no exact oriented primitive word, mixed selector, or theta2 payload theorem",
            decision="support_not_source_closer",
        ),
        ObstructionRow(
            name="sprang_distribution_as_sparse_packet",
            overclaim="full Sprang distribution relation is the p25 sparse theta2 packet",
            falsifier="full kernel/torsion trace lacks the base*K_trace*D_segment*(1-T) selector",
            decision="repair_sparse_specialization_missing",
        ),
        ObstructionRow(
            name="value_only_theta_claim",
            overclaim="theta2 or period value without branch data is enough",
            falsifier="ambient-period-780 value claims keep the F_p mu_11 ambiguity",
            decision="repair_period156_branch_missing",
        ),
        ObstructionRow(
            name="source_chain_without_k_trace",
            overclaim="three-term H90 or cyclotomic compression alone closes KL",
            falsifier="raw K-trace, orientation, and theta2 bridge are still absent",
            decision="repair_k_trace_theta2_context_missing",
        ),
        ObstructionRow(
            name="unified_target_as_exactp_recovery",
            overclaim="H0/conductor-39 support-156 theorem automatically recovers exact-P",
            falsifier="C,D,K/orientation and atom selector data are lost in the forward bridge",
            decision="repair_reverse_selector_theorem_missing",
        ),
    )


def evidence_consistency(root: Path) -> bool:
    lookup = read(root / "evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md")
    theta2 = read(root / "evidence/p25_v2_theta2_period156_support_contract_20260616.md")
    orientation = read(root / "evidence/p25_v2_exactp_orientation_branch_router_20260616.md")
    sprang = read(root / "evidence/p25_v2_sprang_theta2_source_intake_20260616.md")
    sprang_dist = read(root / "evidence/p25_v2_sprang_distribution_instantiation_falsifier_20260616.md")
    kl_split = read(root / "evidence/p25_v2_kl_primitive_word_source_split_20260617.md")
    kl_local = read(root / "evidence/p25_v2_kl_source_split_local_scan_20260617.md")
    kl_cyclo = read(root / "evidence/p25_v2_kl_cyclotomic_norm_route_audit_20260617.md")
    spine = read(root / "evidence/p25_v2_exactp_spine_payload_separation_20260617.md")
    action = read(root / "evidence/p25_v2_source_action_registry_20260616.md")
    return (
        "current_exactp_source_theorems = 0" in lookup
        and "current_theta2_arithmetic_producers = 0" in lookup
        and "current_kl_source_theorems = 0" in lookup
        and "current_source_stage_closers = 0" in lookup
        and "current_arithmetic_producers = 0" in theta2
        and "source_stage_closers = 0" in theta2
        and "accepted_orientation_branches = 4" in orientation
        and "current_exactp_source_theorems = 0" in orientation
        and "exact_theta2_payload_named = no" in sprang
        and "source_stage_closers = 0" in sprang
        and "direct_instantiation_closers = 0" in sprang_dist
        and "accepted_source_hook_rows = 2" in kl_split
        and "current_kl_source_theorems = 0" in kl_split
        and "exact_split_source_hooks = 0" in kl_local
        and "current_exactp_source_theorems = 0" in kl_local
        and "finite_p25_row_theorems_found = 0" in kl_cyclo
        and "current_exactp_upstream_theorems = 0" in kl_cyclo
        and "current_source_stage_closers = 0" in kl_cyclo
        and "atom_count = 75" in spine
        and "theta2_payload_support = 300" in spine
        and "period_norm_support = 312" in spine
        and "unified_h90_support = 156" in spine
        and "support_ladder_ok = 1" in spine
        and "current_source_stage_closers = 0" in action
    )


def main() -> int:
    root = research_root()
    marker_ok, marker_total = evidence_markers_ok(root)
    producers = producer_rows()
    obstructions = obstruction_rows()
    current_exactp_source_theorems = 0
    current_theta2_arithmetic_producers = 0
    current_kl_source_theorems = 0
    current_sprang_sparse_specializations = 0
    current_reverse_reconstruction_theorems = 0
    current_source_stage_closers = 0
    current_submission_ready = 0
    row_ok = (
        marker_ok == marker_total
        and evidence_consistency(root)
        and len(producers) == 6
        and len(obstructions) == 6
        and current_exactp_source_theorems == 0
        and current_theta2_arithmetic_producers == 0
        and current_kl_source_theorems == 0
        and current_sprang_sparse_specializations == 0
        and current_reverse_reconstruction_theorems == 0
        and current_source_stage_closers == 0
        and current_submission_ready == 0
    )

    print("p25 v2 exact-P/theta2 producer obstruction")
    print(f"evidence_markers_ok={marker_ok}/{marker_total}")
    print(f"evidence_consistency={int(evidence_consistency(root))}")
    print("producer_rows")
    for row in producers:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    accepted_if={row.accepted_if}")
        print(f"    still_missing={row.still_missing}")
    print("obstruction_rows")
    for row in obstructions:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    overclaim={row.overclaim}")
        print(f"    falsifier={row.falsifier}")
    print("counts")
    print(f"producer_rows={len(producers)}")
    print(f"obstruction_rows={len(obstructions)}")
    print(f"current_exactp_source_theorems={current_exactp_source_theorems}")
    print(f"current_theta2_arithmetic_producers={current_theta2_arithmetic_producers}")
    print(f"current_kl_source_theorems={current_kl_source_theorems}")
    print(f"current_sprang_sparse_specializations={current_sprang_sparse_specializations}")
    print(f"current_reverse_reconstruction_theorems={current_reverse_reconstruction_theorems}")
    print(f"current_source_stage_closers={current_source_stage_closers}")
    print(f"current_submission_ready={current_submission_ready}")
    print(f"p25_v2_exactp_theta2_producer_obstruction_rows={int(row_ok)}/1")
    return 0 if row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
