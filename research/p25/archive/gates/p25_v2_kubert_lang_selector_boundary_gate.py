#!/usr/bin/env python3
"""Kubert-Lang selector boundary for the p25 exact-P route.

This wrapper promotes three older finite KL gates into one v2 research verdict:
the exact p25 packet passes necessary KL exponent congruences, the primitive
word is the already-rigid bridge word, and the quotient selector is rigid in
C_3 x C_169.  The result is still not an arithmetic producer; it names the
source theorem that would be needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys


GATE_DIR = Path(__file__).resolve().parent
HARNESS_DIR = GATE_DIR.parent / "harness"
sys.path.insert(0, str(GATE_DIR))
sys.path.insert(0, str(HARNESS_DIR))

from p25_laneB_robert_ksy_theta2_kubert_lang_anti_invariant_selector_rigidity_gate import (  # noqa: E501
    profile_anti_invariant_selector_rigidity,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_exponent_matrix_gate import (
    profile_kl_exponent_matrix_screen,
)
from p25_laneB_robert_ksy_theta2_kubert_lang_primitive_word_gate import (
    profile_primitive_word,
)


@dataclass(frozen=True)
class KubertLangSelectorBoundary:
    exponent_matrix_screen_ok: bool
    exact_payloads_survive_congruence_screen: bool
    c169_projection_is_finite_insufficient: bool
    controls_rejected: bool
    source_packet_level: int
    source_packet_support: int
    theta2_raw_level: int
    theta2_raw_support: int
    primitive_word_ok: bool
    primitive_forward_word: tuple[tuple[int, int], ...]
    primitive_normalized_word: tuple[tuple[int, int], ...]
    inherited_product_rigidity_ok: bool
    quotient_selector_is_rigid: bool
    quotient_pairs_scanned: int
    forward_match_count: int
    reverse_match_count: int
    support_only_match_count: int
    zero_d_support_match_count: int
    current_kl_source_theorems: int
    accepted_theorem_shape: str
    rejected_shortcuts: tuple[str, ...]
    decision: str
    row_ok: bool


def build_boundary() -> KubertLangSelectorBoundary:
    exponent = profile_kl_exponent_matrix_screen()
    primitive = profile_primitive_word()
    selector = profile_anti_invariant_selector_rigidity()

    controls_rejected = (
        exponent.truncated_d_rejected
        and exponent.wrong_d_rejected
        and exponent.wrong_t_rejected
        and exponent.positive_only_rejected
    )
    current_kl_source_theorems = 0
    row_ok = (
        exponent.row_ok
        and primitive.row_ok
        and selector.row_ok
        and exponent.exact_payloads_survive_congruence_screen
        and exponent.prime_power_projection_is_finite_insufficient
        and controls_rejected
        and primitive.inherited_product_rigidity_ok
        and selector.quotient_selector_is_rigid
        and selector.quotient_pairs_scanned == 257049
        and len(selector.forward_matches) == 2
        and len(selector.reverse_matches) == 2
        and len(selector.support_only_matches) == 4
        and len(selector.zero_d_support_matches) == 0
        and current_kl_source_theorems == 0
    )

    return KubertLangSelectorBoundary(
        exponent_matrix_screen_ok=exponent.row_ok,
        exact_payloads_survive_congruence_screen=(
            exponent.exact_payloads_survive_congruence_screen
        ),
        c169_projection_is_finite_insufficient=(
            exponent.prime_power_projection_is_finite_insufficient
        ),
        controls_rejected=controls_rejected,
        source_packet_level=exponent.source_packet_profile.level,
        source_packet_support=exponent.source_packet_profile.support,
        theta2_raw_level=exponent.theta2_profile.level,
        theta2_raw_support=exponent.theta2_profile.support,
        primitive_word_ok=primitive.row_ok,
        primitive_forward_word=primitive.quotient_word,
        primitive_normalized_word=primitive.normalized_word,
        inherited_product_rigidity_ok=primitive.inherited_product_rigidity_ok,
        quotient_selector_is_rigid=selector.quotient_selector_is_rigid,
        quotient_pairs_scanned=selector.quotient_pairs_scanned,
        forward_match_count=len(selector.forward_matches),
        reverse_match_count=len(selector.reverse_matches),
        support_only_match_count=len(selector.support_only_matches),
        zero_d_support_match_count=len(selector.zero_d_support_matches),
        current_kl_source_theorems=current_kl_source_theorems,
        accepted_theorem_shape=(
            "theorem-legal mixed C3 x C169 KL/Siegel/Kronecker product "
            "emitting the exact row-labeled selector, primitive word, or "
            "accepted theta2/theta2-inverse payload"
        ),
        rejected_shortcuts=(
            "prime-power C169 projection loses right-class and T-edge data",
            "raw exponent balance is only a necessary KL screen",
            "generic KL generation/dependence theorems do not select p25 rows",
            "wrong, truncated, or unoriented D/T/center packets are controls",
        ),
        decision="finite_selector_rigid_but_kl_source_theorem_missing",
        row_ok=row_ok,
    )


def main() -> int:
    boundary = build_boundary()
    print("p25 v2 Kubert-Lang selector boundary")
    print(f"exponent_matrix_screen_ok={int(boundary.exponent_matrix_screen_ok)}")
    print(
        "exact_payloads_survive_congruence_screen="
        f"{int(boundary.exact_payloads_survive_congruence_screen)}"
    )
    print(
        "c169_projection_is_finite_insufficient="
        f"{int(boundary.c169_projection_is_finite_insufficient)}"
    )
    print(f"controls_rejected={int(boundary.controls_rejected)}")
    print(
        "source_packet "
        f"level={boundary.source_packet_level} support={boundary.source_packet_support}"
    )
    print(
        "theta2_raw "
        f"level={boundary.theta2_raw_level} support={boundary.theta2_raw_support}"
    )
    print(f"primitive_word_ok={int(boundary.primitive_word_ok)}")
    print(f"primitive_forward_word={boundary.primitive_forward_word}")
    print(f"primitive_normalized_word={boundary.primitive_normalized_word}")
    print(
        "inherited_product_rigidity_ok="
        f"{int(boundary.inherited_product_rigidity_ok)}"
    )
    print(f"quotient_selector_is_rigid={int(boundary.quotient_selector_is_rigid)}")
    print(f"quotient_pairs_scanned={boundary.quotient_pairs_scanned}")
    print(f"forward_match_count={boundary.forward_match_count}")
    print(f"reverse_match_count={boundary.reverse_match_count}")
    print(f"support_only_match_count={boundary.support_only_match_count}")
    print(f"zero_d_support_match_count={boundary.zero_d_support_match_count}")
    print(f"current_kl_source_theorems={boundary.current_kl_source_theorems}")
    print(f"accepted_theorem_shape={boundary.accepted_theorem_shape}")
    print("rejected_shortcuts")
    for shortcut in boundary.rejected_shortcuts:
        print(f"  {shortcut}")
    print(f"decision={boundary.decision}")
    print(f"p25_v2_kubert_lang_selector_boundary_rows={int(boundary.row_ok)}/1")
    return 0 if boundary.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
