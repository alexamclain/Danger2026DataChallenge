#!/usr/bin/env python3
"""Source-facing split of the exact-P Kubert-Lang primitive word.

The exact-P/KL finite selector is already rigid.  This gate records a narrower
source intake form for that selector: the six-term primitive word, its
cyclotomic-unit factorization, and the equivalent three-term Hilbert-90 source
chain with unique primitive boundary step.  These are theorem hooks only when
paired with the p25 orientation, K-trace/theta2 context, and arithmetic source
theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
for import_dir in (GATE_DIR, HARNESS_DIR):
    if str(import_dir) not in sys.path:
        sys.path.insert(0, str(import_dir))

from p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate import (  # noqa: E402
    profile_primitive_word as profile_kl_primitive_word,
)
from p25_laneB_square_axis_bridge_hilbert90_source_chain_primitive_word_gate import (  # noqa: E402
    primitive_word_profile as profile_h90_source_chain_word,
)


LEVEL = 507
EXPECTED_BRIDGE_WORD = (
    (121, 1),
    (122, 1),
    (123, 1),
    (384, -1),
    (385, -1),
    (386, -1),
)
EXPECTED_NORMALIZED_WORD = (
    (0, 1),
    (1, 1),
    (2, 1),
    (263, -1),
    (264, -1),
    (265, -1),
)
EXPECTED_CHAIN_WORD = ((0, -1), (1, -1), (386, -1))
EXPECTED_FIRST_BOUNDARY = ((0, -1), (122, 1), (123, 1), (386, -1))


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class SourceSplitRow:
    name: str
    shape: str
    decision: str
    accepted_if_source_theorem_present: bool
    first_missing_or_falsifier: str
    ok: bool


@dataclass(frozen=True)
class KlPrimitiveWordSourceSplit:
    evidence_markers: tuple[EvidenceMarker, ...]
    bridge_word: tuple[tuple[int, int], ...]
    normalized_word: tuple[tuple[int, int], ...]
    shifted_factorization_ok: bool
    cyclotomic_unit_form_ok: bool
    primitive_center_shift: int
    primitive_t_step: int
    h90_chain_word: tuple[tuple[int, int], ...]
    h90_first_boundary: tuple[tuple[int, int], ...]
    h90_unique_boundary_steps: tuple[int, ...]
    h90_rows_recover_bridge: bool
    h90_rows_have_unique_step: bool
    rows: tuple[SourceSplitRow, ...]
    evidence_markers_ok: int
    accepted_source_hook_rows: int
    support_compression_rows: int
    repair_rows: int
    current_kl_source_theorems: int
    current_exactp_source_theorems: int
    current_source_stage_closers: int
    row_ok: bool


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in read(p))


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "exactp_theta2_lookup_row_status",
            "research/p25/evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md",
            "p25_v2_exactp_theta2_lookup_row_status_rows=1/1",
        ),
        marker(
            "kubert_lang_selector_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_selector_boundary_20260616.md",
            "p25_v2_kubert_lang_selector_boundary_rows=1/1",
        ),
        marker(
            "kubert_lang_external_source_boundary",
            "research/p25/evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md",
            "p25_v2_kubert_lang_external_source_boundary_rows=1/1",
        ),
        marker(
            "exactp_theorem_interface",
            "research/p25/evidence/p25_v2_exactp_theorem_interface_contract_20260616.md",
            "still_missing = challenge-legal Robert/Siegel/Kubert-Lang/KSY identity",
        ),
        marker(
            "source_action_registry",
            "research/p25/evidence/p25_v2_source_action_registry_20260616.md",
            "p25_v2_source_action_registry_rows=1/1",
        ),
    )


def as_poly(items: tuple[tuple[int, int], ...]) -> dict[int, int]:
    return {exponent % LEVEL: coefficient for exponent, coefficient in items}


def poly_mul(left: dict[int, int], right: dict[int, int]) -> dict[int, int]:
    out: dict[int, int] = {}
    for e_left, c_left in left.items():
        for e_right, c_right in right.items():
            exponent = (e_left + e_right) % LEVEL
            out[exponent] = out.get(exponent, 0) + c_left * c_right
            if out[exponent] == 0:
                del out[exponent]
    return dict(sorted(out.items()))


def shift(poly: dict[int, int], amount: int) -> dict[int, int]:
    return dict(sorted(((exponent + amount) % LEVEL, coefficient) for exponent, coefficient in poly.items()))


def as_items(poly: dict[int, int]) -> tuple[tuple[int, int], ...]:
    return tuple(sorted(poly.items()))


def split_rows() -> tuple[SourceSplitRow, ...]:
    return (
        SourceSplitRow(
            name="six_term_primitive_word",
            shape="z^121*(1+z+z^2)*(1-z^263), with p25 orientation and theta2/K-trace context",
            decision="continue_if_arithmetic_source_emits_exact_oriented_word",
            accepted_if_source_theorem_present=True,
            first_missing_or_falsifier="arithmetic source theorem and DANGER3 framing after theorem hit",
            ok=True,
        ),
        SourceSplitRow(
            name="three_term_h90_source_chain",
            shape="canonical chain -(1+z+z^-121) plus unique primitive boundary step 122 recovering the bridge word",
            decision="continue_if_source_emits_chain_boundary_step_and_k_trace",
            accepted_if_source_theorem_present=True,
            first_missing_or_falsifier="raw K-trace/theta2 period-156 context and arithmetic source theorem",
            ok=True,
        ),
        SourceSplitRow(
            name="cyclotomic_unit_factorization",
            shape="normalized word (1+z+z^2)*(1-z^263) = (1-z^3)*(1-z^263)/(1-z)",
            decision="support_compression_not_source_theorem",
            accepted_if_source_theorem_present=False,
            first_missing_or_falsifier="theorem-legal Siegel/Kronecker/KSY lift with orientation and p25 payload",
            ok=True,
        ),
        SourceSplitRow(
            name="generic_kl_generator_or_congruence_theorem",
            shape="KL generator, theorem-K congruence, or raw exponent balance without the exact word",
            decision="repair_exact_selector_theorem_missing",
            accepted_if_source_theorem_present=False,
            first_missing_or_falsifier="exact primitive word, mixed selector, or accepted theta2 payload",
            ok=True,
        ),
        SourceSplitRow(
            name="source_chain_without_k_trace_or_theta2_context",
            shape="three-term primitive source chain without K-trace, orientation, or period-156 theta2 bridge",
            decision="repair_k_trace_theta2_context_missing",
            accepted_if_source_theorem_present=False,
            first_missing_or_falsifier="raw K-trace, orientation, and theta2/theta2-inverse bridge data",
            ok=True,
        ),
    )


def build_split() -> KlPrimitiveWordSourceSplit:
    markers = evidence_markers()
    kl = profile_kl_primitive_word()
    h90 = profile_h90_source_chain_word()
    normalized_factor = poly_mul({0: 1, 1: 1, 2: 1}, {0: 1, 263: -1})
    shifted_factor = shift(normalized_factor, 121)
    rows = split_rows()
    h90_steps = tuple(sorted({row.boundary_step_d for row in h90.rows}))
    support_rows = sum(row.decision.startswith("support_") for row in rows)
    repair_rows = sum(row.decision.startswith("repair_") for row in rows)
    accepted = sum(row.accepted_if_source_theorem_present for row in rows)
    current_kl_source_theorems = 0
    current_exactp_source_theorems = 0
    current_source_stage_closers = 0
    row_ok = (
        sum(row.ok for row in markers) == len(markers)
        and kl.row_ok
        and kl.quotient_word == EXPECTED_BRIDGE_WORD
        and kl.normalized_word == EXPECTED_NORMALIZED_WORD
        and kl.base_primitive_exponent == 121
        and kl.t_primitive_exponent == 263
        and as_items(normalized_factor) == EXPECTED_NORMALIZED_WORD
        and as_items(shifted_factor) == EXPECTED_BRIDGE_WORD
        and h90.bridge_word == EXPECTED_BRIDGE_WORD
        and h90.canonical_chain_word == EXPECTED_CHAIN_WORD
        and h90.canonical_boundary_step == 122
        and h90.canonical_first_boundary_word == EXPECTED_FIRST_BOUNDARY
        and h90.all_rows_recover_bridge
        and h90.all_rows_have_unique_recovery_step
        and h90.all_rows_have_sparse_boundary_distribution
        and h90_steps == (122, 385)
        and len(rows) == 5
        and accepted == 2
        and support_rows == 1
        and repair_rows == 2
        and current_kl_source_theorems == 0
        and current_exactp_source_theorems == 0
        and current_source_stage_closers == 0
        and all(row.ok for row in rows)
    )
    return KlPrimitiveWordSourceSplit(
        evidence_markers=markers,
        bridge_word=kl.quotient_word,
        normalized_word=kl.normalized_word,
        shifted_factorization_ok=as_items(shifted_factor) == EXPECTED_BRIDGE_WORD,
        cyclotomic_unit_form_ok=as_items(normalized_factor) == EXPECTED_NORMALIZED_WORD,
        primitive_center_shift=kl.base_primitive_exponent,
        primitive_t_step=kl.t_primitive_exponent,
        h90_chain_word=h90.canonical_chain_word,
        h90_first_boundary=h90.canonical_first_boundary_word,
        h90_unique_boundary_steps=h90_steps,
        h90_rows_recover_bridge=h90.all_rows_recover_bridge,
        h90_rows_have_unique_step=h90.all_rows_have_unique_recovery_step,
        rows=rows,
        evidence_markers_ok=sum(row.ok for row in markers),
        accepted_source_hook_rows=accepted,
        support_compression_rows=support_rows,
        repair_rows=repair_rows,
        current_kl_source_theorems=current_kl_source_theorems,
        current_exactp_source_theorems=current_exactp_source_theorems,
        current_source_stage_closers=current_source_stage_closers,
        row_ok=row_ok,
    )


def main() -> int:
    split = build_split()
    print("p25 v2 KL primitive-word source split")
    for marker_row in split.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("primitive_word")
    print(f"  bridge_word={split.bridge_word}")
    print(f"  normalized_word={split.normalized_word}")
    print(f"  primitive_center_shift={split.primitive_center_shift}")
    print(f"  primitive_t_step={split.primitive_t_step}")
    print(f"  shifted_factorization_ok={int(split.shifted_factorization_ok)}")
    print(f"  cyclotomic_unit_form_ok={int(split.cyclotomic_unit_form_ok)}")
    print("h90_source_chain")
    print(f"  chain_word={split.h90_chain_word}")
    print(f"  first_boundary={split.h90_first_boundary}")
    print(f"  unique_boundary_steps={split.h90_unique_boundary_steps}")
    print(f"  rows_recover_bridge={int(split.h90_rows_recover_bridge)}")
    print(f"  rows_have_unique_step={int(split.h90_rows_have_unique_step)}")
    print("rows")
    for row in split.rows:
        print(f"  {row.name}: decision={row.decision}")
        print(f"    shape={row.shape}")
        print(f"    accepted_if_source_theorem_present={int(row.accepted_if_source_theorem_present)}")
        print(f"    missing_or_falsifier={row.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={split.evidence_markers_ok}/{len(split.evidence_markers)}")
    print(f"  accepted_source_hook_rows={split.accepted_source_hook_rows}")
    print(f"  support_compression_rows={split.support_compression_rows}")
    print(f"  repair_rows={split.repair_rows}")
    print(f"  current_kl_source_theorems={split.current_kl_source_theorems}")
    print(f"  current_exactp_source_theorems={split.current_exactp_source_theorems}")
    print(f"  current_source_stage_closers={split.current_source_stage_closers}")
    print("interpretation")
    print("  exactp_kl_word_has_source_facing_h90_chain_form=1")
    print("  cyclotomic_factorization_is_support_not_a_source_theorem=1")
    print("  source_hit_still_needs_orientation_k_trace_theta2_context=1")
    print(f"p25_v2_kl_primitive_word_source_split_rows={int(split.row_ok)}/1")
    return 0 if split.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
