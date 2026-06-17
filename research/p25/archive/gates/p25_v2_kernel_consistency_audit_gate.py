#!/usr/bin/env python3
"""Cross-check the current p25 theorem-kernel surfaces for drift."""

from __future__ import annotations

import importlib.util
import sys
from dataclasses import dataclass
from math import gcd
from pathlib import Path
from types import ModuleType


REPO = Path(__file__).resolve().parents[4]
RESEARCH = REPO / "research" / "p25"
P25 = 10**25 + 13
PM1 = P25 - 1
UNIQUE_POWERS = (3, 5, 13, 39, 75, 169, 507)
INVERSES = (
    (3, 6666666666666666666666675),
    (5, 4000000000000000000000005),
    (13, 7692307692307692307692317),
    (39, 5897435897435897435897443),
    (75, 266666666666666666666667),
    (169, 5207100591715976331360953),
    (507, 5069033530571992110453655),
)
SET_NEEDLE = "e in {3,5,13,39,75,169,507}"
MATCHED_NEEDLE = "matched_quotient"
BAD_INVERSE_NEEDLES = (
    "5333333333333333333333340",
    "3668639053254437869822490",
    "1222879684418145956607497",
)


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    rel_path: str
    marker: str

    @property
    def ok(self) -> bool:
        path = RESEARCH / self.rel_path
        return path.exists() and self.marker in path.read_text(errors="replace")


def load_gate(name: str) -> ModuleType:
    path = RESEARCH / "archive" / "gates" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


EVIDENCE_MARKERS = (
    EvidenceMarker(
        "current_theorem_kernel",
        "evidence/p25_v2_current_theorem_kernel_20260617.md",
        "p25_v2_current_theorem_kernel_rows=1/1",
    ),
    EvidenceMarker(
        "drew_kernel_review_packet",
        "evidence/p25_v2_drew_kernel_review_packet_20260617.md",
        "p25_v2_drew_kernel_review_packet_rows=1/1",
    ),
    EvidenceMarker(
        "source_stage_normalization_spine",
        "evidence/p25_v2_source_stage_normalization_spine_20260617.md",
        "p25_v2_source_stage_normalization_spine_rows=1/1",
    ),
    EvidenceMarker(
        "repair_debt_closure_matrix",
        "evidence/p25_v2_repair_debt_closure_matrix_20260617.md",
        "p25_v2_repair_debt_closure_matrix_rows=1/1",
    ),
    EvidenceMarker(
        "extended_unique_power_intake",
        "evidence/p25_v2_extended_unique_power_intake_20260617.md",
        "p25_v2_extended_unique_power_intake_rows=1/1",
    ),
    EvidenceMarker(
        "affine_row_normal_form",
        "evidence/p25_v2_affine_row_normal_form_20260617.md",
        "p25_v2_affine_row_normal_form_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_closure_packet",
        "evidence/p25_v2_matched_quotient_closure_packet_20260617.md",
        "p25_v2_matched_quotient_closure_packet_rows=1/1",
    ),
    EvidenceMarker(
        "matched_quotient_source_feasibility",
        "evidence/p25_v2_matched_quotient_source_feasibility_20260617.md",
        "p25_v2_matched_quotient_source_feasibility_rows=1/1",
    ),
    EvidenceMarker(
        "period156_feasibility_supersession",
        "evidence/p25_v2_period156_feasibility_supersession_20260617.md",
        "p25_v2_period156_feasibility_supersession_rows=1/1",
    ),
    EvidenceMarker(
        "live_theorem_ask_packet",
        "evidence/p25_v2_live_theorem_ask_packet_20260617.md",
        "p25_v2_live_theorem_ask_packet_rows=1/1",
    ),
    EvidenceMarker(
        "source_theorem_acceptance_automaton",
        "evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md",
        "p25_v2_source_theorem_acceptance_automaton_rows=1/1",
    ),
)


def read(rel_path: str) -> str:
    return (RESEARCH / rel_path).read_text(errors="replace")


def canonical_pages_ok() -> bool:
    checks = (
        ("frontier.md", SET_NEEDLE),
        ("lanes/h0.md", SET_NEEDLE),
        ("lanes/conductor39.md", SET_NEEDLE),
    )
    return all(needle in read(rel_path) for rel_path, needle in checks)


def evidence_pages_ok() -> bool:
    checks = (
        ("evidence/p25_v2_current_theorem_kernel_20260617.md", SET_NEEDLE),
        ("evidence/p25_v2_drew_kernel_review_packet_20260617.md", SET_NEEDLE),
        ("evidence/p25_v2_source_stage_normalization_spine_20260617.md", SET_NEEDLE),
        ("evidence/p25_v2_repair_debt_closure_matrix_20260617.md", SET_NEEDLE),
    )
    texts = [read(rel_path) for rel_path, _ in checks]
    matched_texts = (
        read("evidence/p25_v2_current_theorem_kernel_20260617.md"),
        read("evidence/p25_v2_drew_kernel_review_packet_20260617.md"),
        read("evidence/p25_v2_source_theorem_acceptance_automaton_20260617.md"),
        read("evidence/p25_v2_matched_quotient_closure_packet_20260617.md"),
        read("evidence/p25_v2_matched_quotient_source_feasibility_20260617.md"),
    )
    return (
        all(needle in text for text, (_, needle) in zip(texts, checks))
        and all(MATCHED_NEEDLE in text for text in matched_texts)
        and all(str(inverse) in read("evidence/p25_v2_source_stage_normalization_spine_20260617.md") for _, inverse in INVERSES)
        and all(str(inverse) in read("evidence/p25_v2_extended_unique_power_intake_20260617.md") for _, inverse in INVERSES)
        and not any(bad in "\n".join(texts) for bad in BAD_INVERSE_NEEDLES)
    )


def main() -> int:
    kernel = load_gate("p25_v2_current_theorem_kernel_gate")
    drew = load_gate("p25_v2_drew_kernel_review_packet_gate")
    spine = load_gate("p25_v2_source_stage_normalization_spine_gate")
    repair = load_gate("p25_v2_repair_debt_closure_matrix_gate")
    extended = load_gate("p25_v2_extended_unique_power_intake_gate")
    automaton = load_gate("p25_v2_source_theorem_acceptance_automaton_gate")
    live = load_gate("p25_v2_live_theorem_ask_packet_gate")
    matched_feasibility = load_gate("p25_v2_matched_quotient_source_feasibility_gate")
    period_supersession = load_gate("p25_v2_period156_feasibility_supersession_gate")

    powers_consistent = (
        tuple(kernel.UNIQUE_ROW_POWERS) == UNIQUE_POWERS
        and tuple(drew.UNIQUE_ROW_POWERS) == UNIQUE_POWERS
        and tuple(spine.UNIQUE_POWER_EXPONENTS) == UNIQUE_POWERS
        and tuple((*extended.STANDARD_POWER_HOOKS, *extended.EXTENDED_POWER_HOOKS)) == UNIQUE_POWERS
    )
    inverses_consistent = (
        spine.inverse_exponents() == INVERSES
        and tuple((row.exponent, row.inverse_exponent) for row in extended.unique_power_rows()) == INVERSES
        and all((exponent * inverse) % PM1 == 1 for exponent, inverse in INVERSES)
    )
    repair_kernels = dict(repair.power_kernels())
    repair_consistent = (
        all(repair_kernels[exponent] == 1 for exponent in UNIQUE_POWERS)
        and all(repair_kernels[exponent] > 1 for exponent in extended.REPAIR_POWER_HOOKS)
        and any(SET_NEEDLE in row.theorem_shape for row in repair.debt_rows(repair_kernels, dict(repair.period_branch_gcds())))
    )
    row_counts_consistent = (
        kernel.kernel_rows()[1].decision == "normalize_by_inverse_exponent_then_source_stage"
        and drew.review_rows()[1].decision == "normalize_to_source_stage_if_present"
        and sum("support_route" in row.decision for row in kernel.kernel_rows()) == 2
        and sum(row.status.startswith("support") for row in drew.review_rows()) == 2
        and spine.build_spine().current_source_stage_closers == 0
        and repair.build_matrix().current_source_stage_closers == 0
        and spine.build_spine().current_submission_ready == 0
        and repair.build_matrix().current_submission_ready == 0
    )
    automaton_rows = tuple((row, automaton.classify(row)) for row in automaton.candidates())
    automaton_consistent = (
        len(automaton_rows) == 25
        and sum(decision.startswith("normalize_") for _row, decision in automaton_rows) == 2
        and sum(row.kind == "matched_quotient_packet" for row, _decision in automaton_rows) == 3
        and any(decision == "normalize_matched_quotient_then_accept" for _row, decision in automaton_rows)
        and any(decision == "repair_zero_lattice_value_missing" for _row, decision in automaton_rows)
        and any(decision == "repair_root_debt_remaining" for _row, decision in automaton_rows)
    )
    live_rows = live.ask_rows()
    live_action_consistent = (
        len(live_rows) == 3
        and {row.status for row in live_rows} == {"live_primary", "live_support_value", "live_heavy"}
        and live.canonical_pages_ok(RESEARCH)
        and live.broad_reread_closed(RESEARCH)
    )
    source_shapes = matched_feasibility.source_shapes()
    matched_source_feasibility_consistent = (
        len(source_shapes) == 10
        and sum(
            shape.decision == "viable_matched_quotient_packet_if_source_supplies_both"
            for shape in source_shapes
        )
        == 2
        and sum(
            shape.decision in {"repair_even_sum_root_debt", "repair_fourth_root_debt"}
            for shape in source_shapes
        )
        == 3
        and sum(shape.decision == "repair_matched_zero_lattice_value_missing" for shape in source_shapes)
        == 1
        and all(matched_feasibility.shape_ok(shape) for shape in source_shapes)
    )
    period_rows = period_supersession.rows()
    period156_supersession_consistent = (
        len(period_rows) == 6
        and sum(row.status.endswith("accept_shape") for row in period_rows) == 3
        and sum(row.status.endswith("repair_shape") for row in period_rows) == 3
        and gcd(pow(4, 156, PM1) - 1, PM1) == 1
        and gcd(pow(4, 780, PM1) - 1, PM1) == 11
    )
    marker_count = sum(marker.ok for marker in EVIDENCE_MARKERS)
    overall_ok = (
        P25 % 8 == 5
        and marker_count == len(EVIDENCE_MARKERS)
        and powers_consistent
        and inverses_consistent
        and repair_consistent
        and evidence_pages_ok()
        and canonical_pages_ok()
        and row_counts_consistent
        and automaton_consistent
        and live_action_consistent
        and matched_source_feasibility_consistent
        and period156_supersession_consistent
    )

    print("p25 v2 kernel consistency audit")
    print(f"p={P25}")
    print(f"unique_powers={UNIQUE_POWERS}")
    print("inverse_exponents")
    for exponent, inverse in INVERSES:
        print(f"  e={exponent}: inverse={inverse}")
    for marker in EVIDENCE_MARKERS:
        print(f"marker {marker.name}: {'ok' if marker.ok else 'MISSING'}")
    print(f"powers_consistent={int(powers_consistent)}")
    print(f"inverses_consistent={int(inverses_consistent)}")
    print(f"repair_consistent={int(repair_consistent)}")
    print(f"evidence_pages_ok={int(evidence_pages_ok())}")
    print(f"canonical_pages_ok={int(canonical_pages_ok())}")
    print(f"row_counts_consistent={int(row_counts_consistent)}")
    print(f"automaton_consistent={int(automaton_consistent)}")
    print(f"live_action_consistent={int(live_action_consistent)}")
    print(f"matched_source_feasibility_consistent={int(matched_source_feasibility_consistent)}")
    print(f"period156_supersession_consistent={int(period156_supersession_consistent)}")
    print("current_source_stage_closers=0")
    print("current_submission_ready=0")
    print(f"p25_v2_kernel_consistency_audit_rows={int(overall_ok)}/1")
    return 0 if overall_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
