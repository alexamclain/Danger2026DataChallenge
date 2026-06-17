#!/usr/bin/env python3
"""Current expert/source-answer rubric for the p25 v2 frontier.

This gate consolidates the live v2 contracts into one response classifier.  It
does not prove the missing theorem; it says how to route a future expert answer
or source snippet against the now-current target, row normalizer, conductor-39
selector rigidity, Koo-Shin Theorem 5.2 obstruction, rectangle aggregate,
row-quotient bridge, and row-square root repair cases, value-branch contract,
degree-6 value descent ambiguity, reverse exact-P information loss, and
extraction payload contract.  It also includes the source-graph normal form
and edge-lattice intake rule, and routes H0/Y507 value claims through the
period-156 compatibility screen.  It also rejects support-below-12 H90
selector claims using the exact orbitwise lower bound, and routes exact-P
leads through the minimal exact-P hook.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class EvidenceMarker:
    name: str
    path: Path
    marker: str
    ok: bool


@dataclass(frozen=True)
class ExpertResponseRow:
    name: str
    answer_shape: str
    category: str
    decision: str
    first_missing_or_falsifier: str
    continue_lane: str
    source_stage_closed: bool
    extraction_stage_reached: bool
    submission_ready: bool
    ok: bool


@dataclass(frozen=True)
class CurrentExpertResponseRubric:
    evidence_markers: tuple[EvidenceMarker, ...]
    response_rows: tuple[ExpertResponseRow, ...]
    evidence_markers_ok: int
    frontdoor_source_closing_rows: int
    heavy_upstream_rows: int
    normalize_then_intake_rows: int
    repair_rows: int
    reject_rows: int
    extraction_progress_rows: int
    submission_ready_rows: int
    current_source_stage_closers: int
    current_submission_ready: int
    row_ok: bool


def marker(name: str, path: str, needle: str) -> EvidenceMarker:
    p = Path(path)
    text = p.read_text() if p.exists() else ""
    return EvidenceMarker(name=name, path=p, marker=needle, ok=needle in text)


def evidence_markers() -> tuple[EvidenceMarker, ...]:
    return (
        marker(
            "review_packet",
            "research/p25/evidence/p25_v2_unified_theorem_review_packet_20260616.md",
            "p25_v2_unified_theorem_review_packet_rows=1/1",
        ),
        marker(
            "group_ring_payload",
            "research/p25/evidence/p25_v2_unified_group_ring_payload_20260616.md",
            "p25_v2_unified_group_ring_payload_rows=1/1",
        ),
        marker(
            "row_orbit_normalization",
            "research/p25/evidence/p25_v2_row_orbit_normalization_20260616.md",
            "p25_v2_row_orbit_normalization_rows=1/1",
        ),
        marker(
            "row_orientation_reciprocal_normalizer",
            "research/p25/evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md",
            "p25_v2_row_orientation_reciprocal_normalizer_rows=1/1",
        ),
        marker(
            "mixed_signed_column_fingerprint",
            "research/p25/evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md",
            "p25_v2_mixed_signed_column_fingerprint_rows=1/1",
        ),
        marker(
            "mod13_coset_rectangle",
            "research/p25/evidence/p25_v2_mod13_coset_rectangle_20260616.md",
            "p25_v2_mod13_coset_rectangle_rows=1/1",
        ),
        marker(
            "quotient_h90_idempotent_mechanism",
            "research/p25/evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md",
            "p25_v2_quotient_h90_idempotent_mechanism_rows=1/1",
        ),
        marker(
            "minimal_h90_preimage_classifier",
            "research/p25/evidence/p25_v2_minimal_h90_preimage_classifier_20260616.md",
            "p25_v2_minimal_h90_preimage_classifier_rows=1/1",
        ),
        marker(
            "h90_support_lower_bound",
            "research/p25/evidence/p25_v2_h90_support_lower_bound_20260616.md",
            "p25_v2_h90_support_lower_bound_rows=1/1",
        ),
        marker(
            "source_graph_normal_form",
            "research/p25/evidence/p25_v2_source_graph_normal_form_20260616.md",
            "p25_v2_source_graph_normal_form_rows=1/1",
        ),
        marker(
            "edge_lattice_intake_classifier",
            "research/p25/evidence/p25_v2_edge_lattice_intake_classifier_20260616.md",
            "p25_v2_edge_lattice_intake_classifier_rows=1/1",
        ),
        marker(
            "quartic_selector_payload",
            "research/p25/evidence/p25_v2_quartic_selector_payload_20260616.md",
            "p25_v2_quartic_selector_payload_rows=1/1",
        ),
        marker(
            "quartic_reciprocal_orientation",
            "research/p25/evidence/p25_v2_quartic_reciprocal_orientation_20260616.md",
            "p25_v2_quartic_reciprocal_orientation_rows=1/1",
        ),
        marker(
            "koo_shin_distribution_noncloser",
            "research/p25/evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md",
            "p25_v2_koo_shin_distribution_noncloser_rows=1/1",
        ),
        marker(
            "theorem52_constant_span_obstruction",
            "research/p25/evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md",
            "p25_v2_theorem52_constant_span_obstruction_rows=1/1",
        ),
        marker(
            "rectangle_diagonal_aggregate",
            "research/p25/evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md",
            "p25_v2_rectangle_diagonal_aggregate_rows=1/1",
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
            "constant_normalization_ambiguity",
            "research/p25/evidence/p25_v2_constant_normalization_ambiguity_20260616.md",
            "p25_v2_constant_normalization_ambiguity_rows=1/1",
        ),
        marker(
            "norm_only_descent_ambiguity",
            "research/p25/evidence/p25_v2_norm_only_descent_ambiguity_20260616.md",
            "p25_v2_norm_only_descent_ambiguity_rows=1/1",
        ),
        marker(
            "period156_branch_contract",
            "research/p25/evidence/p25_v2_period156_value_branch_contract_20260616.md",
            "p25_v2_period156_value_branch_contract_rows=1/1",
        ),
        marker(
            "h0_y507_period156_compatibility",
            "research/p25/evidence/p25_v2_h0_y507_period156_compatibility_20260616.md",
            "p25_v2_h0_y507_period156_compatibility_rows=1/1",
        ),
        marker(
            "degree6_value_descent_ambiguity",
            "research/p25/evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md",
            "p25_v2_degree6_value_descent_ambiguity_rows=1/1",
        ),
        marker(
            "yang_lift_descent_boundary_contract",
            "research/p25/evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md",
            "p25_v2_yang_lift_descent_boundary_contract_rows=1/1",
        ),
        marker(
            "conductor39_norm_one_quotient_route",
            "research/p25/evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md",
            "p25_v2_conductor39_norm_one_quotient_route_rows=1/1",
        ),
        marker(
            "q_diagonal_normalization",
            "research/p25/evidence/p25_v2_q_diagonal_normalization_20260616.md",
            "p25_v2_q_diagonal_normalization_rows=1/1",
        ),
        marker(
            "q_square_payload_router",
            "research/p25/evidence/p25_v2_q_square_payload_router_20260616.md",
            "p25_v2_q_square_payload_router_rows=1/1",
        ),
        marker(
            "q_square_extraction_boundary",
            "research/p25/evidence/p25_v2_q_square_extraction_boundary_20260616.md",
            "p25_v2_q_square_extraction_boundary_rows=1/1",
        ),
        marker(
            "coefficient6_root_normalization",
            "research/p25/evidence/p25_v2_coefficient6_root_normalization_20260616.md",
            "p25_v2_coefficient6_root_normalization_rows=1/1",
        ),
        marker(
            "power_scalar_ambiguity_inventory",
            "research/p25/evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md",
            "p25_v2_power_scalar_ambiguity_inventory_rows=1/1",
        ),
        marker(
            "power_output_kind_router",
            "research/p25/evidence/p25_v2_power_output_kind_router_20260616.md",
            "p25_v2_power_output_kind_router_rows=1/1",
        ),
        marker(
            "additive_normalization_contract",
            "research/p25/evidence/p25_v2_additive_normalization_contract_20260616.md",
            "p25_v2_additive_normalization_contract_rows=1/1",
        ),
        marker(
            "source_family_router",
            "research/p25/evidence/p25_v2_value_divisor_source_family_router_20260616.md",
            "p25_v2_value_divisor_source_family_router_rows=1/1",
        ),
        marker(
            "source_snippet_intake",
            "research/p25/evidence/p25_v2_source_snippet_intake_20260616.md",
            "p25_v2_source_snippet_intake_rows=1/1",
        ),
        marker(
            "danger3_finite_identity_framing",
            "research/p25/evidence/p25_v2_danger3_finite_identity_framing_contract_20260616.md",
            "p25_v2_danger3_finite_identity_framing_contract_rows=1/1",
        ),
        marker(
            "reverse_exactp_information_loss",
            "research/p25/evidence/p25_v2_reverse_exactp_information_loss_20260616.md",
            "p25_v2_reverse_exactp_information_loss_rows=1/1",
        ),
        marker(
            "exactp_minimal_hook",
            "research/p25/evidence/p25_v2_exactp_minimal_hook_20260616.md",
            "p25_v2_exactp_minimal_hook_rows=1/1",
        ),
        marker(
            "exactp_orientation_branch_router",
            "research/p25/evidence/p25_v2_exactp_orientation_branch_router_20260616.md",
            "p25_v2_exactp_orientation_branch_router_rows=1/1",
        ),
        marker(
            "extraction_payload_contract",
            "research/p25/evidence/p25_v2_extraction_payload_contract_20260616.md",
            "p25_v2_extraction_payload_contract_rows=1/1",
        ),
    )


def row(
    name: str,
    answer_shape: str,
    category: str,
    decision: str,
    missing: str,
    lane: str,
    *,
    source_closed: bool = False,
    extraction: bool = False,
    submission: bool = False,
) -> ExpertResponseRow:
    return ExpertResponseRow(
        name=name,
        answer_shape=answer_shape,
        category=category,
        decision=decision,
        first_missing_or_falsifier=missing,
        continue_lane=lane,
        source_stage_closed=source_closed,
        extraction_stage_reached=extraction,
        submission_ready=submission,
        ok=True,
    )


def response_rows() -> tuple[ExpertResponseRow, ...]:
    return (
        row(
            "normalized_divisor_additive_theorem",
            "finite divisor/additive theorem for one normalized legal row, equivalently one of the four legal minimal H90 preimages, with Norm_156(Y_507) boundary",
            "frontdoor_source_close",
            "source_stage_win_route_to_extraction_contract",
            "DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py",
            "H0/conductor39",
            source_closed=True,
        ),
        row(
            "normalized_period156_value_theorem",
            "finite value theorem for canonical H0 with Norm_156(Y_507) boundary, or for Y_507 with period-156 context, equivalently one normalized legal support-156 row with branch/root/telescoping context",
            "frontdoor_source_close",
            "source_stage_win_route_to_extraction_contract",
            "DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py",
            "H0/conductor39",
            source_closed=True,
        ),
        row(
            "quartic_selector_finite_theorem",
            "character-language theorem giving W boundary, exact row-antisymmetric C4_1 phase, mixed tensor row sign, and a scalar-fixed finite value/divisor theorem",
            "frontdoor_source_close",
            "source_stage_win_route_to_extraction_contract",
            "DANGER3 framing, same-j bridge, X_1(16), halving/x0, vpp.py",
            "H0/conductor39",
            source_closed=True,
        ),
        row(
            "exactp_upstream_theorem",
            "challenge-legal exact-P theorem selecting the compact exact-P payload and feeding 75->300->12->312->156",
            "heavy_upstream_close",
            "source_stage_win_route_to_extraction_contract",
            "DANGER3 framing and extraction after upstream theorem",
            "exact-P",
            source_closed=True,
        ),
        row(
            "unified_target_as_exactp_recovery",
            "unified support-156 theorem presented as an exact-P proof without C,D,K,orientation, 75-atom selector data, theta2 payload, or an explicit reverse theorem",
            "repair",
            "repair_reverse_exactp_selector_missing",
            "exact-P C,D,K,orientation, equal-weight 75-atom selector theorem, period-156 theta2 payload, or explicit reverse reconstruction theorem",
            "exact-P",
        ),
        row(
            "ksy_normalized_y_vocabulary_only",
            "KSY normalized-y, torsion, or ray-class vocabulary without the exact equal-weight 75-atom product theorem",
            "repair",
            "repair_exact_selector_theorem_missing",
            "compact C,D,K,orientation packet or exact equal-weight 75-atom theorem",
            "exact-P",
        ),
        row(
            "raw_kubert_lang_exponent_balance_only",
            "Kubert-Lang exponent balance, dependence, or unit-generation statement without theorem-legal theta2 intake",
            "repair",
            "repair_theta2_intake_missing",
            "accepted theta2/theta2-inverse divisor-additive payload or compact KSY theta2 certificate",
            "exact-P",
        ),
        row(
            "exactp_branchless_orientation_word",
            "C,D,K,orientation wording that does not identify one of the four raw center/reverse branches or theta2/theta2-inverse output",
            "repair",
            "repair_exactp_orientation_branch_missing",
            "one of the four raw center/reverse branches and theta2/theta2^-1 output",
            "exact-P",
        ),
        row(
            "theta2_value_without_period156_context",
            "theta2 or theta2-inverse value claim without support-period-156 fixedness, branch/root, or telescoping context",
            "repair",
            "repair_period156_branch_selection_missing",
            "period-156 theta2 fixedness, branch/root, or telescoping context",
            "exact-P",
        ),
        row(
            "wrong_exactp_packet",
            "wrong C, D, K, orientation, nonprimitive K trace, truncated D segment, or shifted center",
            "reject",
            "reject_wrong_exactp_payload",
            "compact exact-P packet C=(47,28), D=(22,3), primitive K=(57,0), with accepted orientation",
            "kill",
        ),
        row(
            "nonuniform_or_missing_exactp_atoms",
            "nonuniform K-layer weights, missing atoms, doubled atoms, or reweighted exact-P payload",
            "reject",
            "reject_by_finite_geometry_rigidity",
            "finite geometry forces the exact equal-weight 75-atom payload",
            "kill",
        ),
        row(
            "exactp_ambient_period780_value_only",
            "exact-P or theta2 value-only theorem at ambient period 780 with no support-period-156 branch selection",
            "repair",
            "repair_period156_branch_selection_missing",
            "period-156 branch/root/telescoping context or divisor/additive normalization",
            "exact-P",
        ),
        row(
            "exactp_finite_payload_without_source",
            "local exact-P finite payload, hash match, or computed theta2 data with no arithmetic source theorem",
            "repair",
            "repair_arithmetic_source_missing",
            "challenge-legal arithmetic source theorem",
            "exact-P",
        ),
        row(
            "exactp_generic_ray_class_generation",
            "generic ray-class, KSY, KL, or Siegel-Robert generation statement without the exact finite p25 identity",
            "repair",
            "repair_exact_finite_identity_missing",
            "exact finite p25 identity emitting the compact exact-P packet or accepted theta2 payload",
            "exact-P",
        ),
        row(
            "stabilizer_or_doubling_equivalent_row",
            "row presentation using a stabilizer-equivalent or doubling-coset multiplier",
            "normalize_then_intake",
            "normalize_row_then_apply_source_snippet_intake",
            "normalized legal row plus source theorem",
            "H0/conductor39",
        ),
        row(
            "reciprocal_row_minus_boundary",
            "reciprocal of a legal row with explicit reciprocal orientation and -Norm_156(Y_507) boundary sign",
            "normalize_then_intake",
            "normalize_reciprocal_then_apply_source_snippet_intake",
            "same theorem data after reciprocal/orientation normalization",
            "H0/conductor39",
        ),
        row(
            "row_square_with_explicit_oriented_root",
            "row-square theorem plus explicit oriented root equal to one normalized legal row",
            "normalize_then_intake",
            "normalize_root_then_apply_source_snippet_intake",
            "same theorem data after oriented-root normalization",
            "H0/conductor39",
        ),
        row(
            "normalized_value_after_constant_fix",
            "theorem data plus an explicit F_p^* scalar, branch/root context, or finite normalization fixing the exact value",
            "normalize_then_intake",
            "normalize_value_then_apply_source_snippet_intake",
            "same theorem data after value normalization",
            "H0/conductor39",
        ),
        row(
            "normalized_additive_value_after_basepoint",
            "theorem data plus a basepoint, finite additive identity, or telescoping product fixing the exact value",
            "normalize_then_intake",
            "normalize_additive_value_then_apply_source_snippet_intake",
            "same theorem data after additive/value normalization",
            "H0/conductor39",
        ),
        row(
            "norm_plus_explicit_legal_h90_descent",
            "dense norm plus an explicit legal support-156 Hilbert-90 preimage or product row",
            "normalize_then_intake",
            "normalize_descent_then_apply_source_snippet_intake",
            "same theorem data after legal H90 descent normalization",
            "H0/conductor39",
        ),
        row(
            "degree6_value_with_explicit_fp_descent",
            "degree-6 value/orbit theorem plus explicit F_p descent, selected legal support-156 row, and period-156 or H90 boundary context",
            "normalize_then_intake",
            "normalize_value_descent_then_apply_source_snippet_intake",
            "same theorem data after explicit F_p descent and row selection",
            "H0/conductor39",
        ),
        row(
            "norm_one_Q_value_theorem_with_period156_context",
            "finite theorem for Q=prod_{h in <2>} E_{7h}/E_h with period-156 branch/root/telescoping context",
            "normalize_then_intake",
            "route_through_period156_value_source_hook",
            "period-156 value source hook, then downstream DANGER3 framing and extraction",
            "H0/conductor39",
        ),
        row(
            "explicit_Q3_hilbert90_preimage_with_finite_theorem",
            "finite theorem for the Hilbert-90 preimage Q^3 with Q^6=(1-Frob_p)(Q^3)",
            "normalize_then_intake",
            "normalize_h90_preimage_then_apply_source_snippet_intake",
            "same theorem data after legal Hilbert-90 descent normalization",
            "H0/conductor39",
        ),
        row(
            "coefficient2_exact_root_value",
            "exact theorem for the coefficient-2 root row; cubing gives the current coefficient-6 row",
            "normalize_then_intake",
            "normalize_cube_power_then_apply_source_snippet_intake",
            "same theorem data after cubing to coefficient 6",
            "H0/conductor39",
        ),
        row(
            "coefficient3_exact_root_value",
            "exact theorem for the coefficient-3 root row; squaring gives the current coefficient-6 row",
            "normalize_then_intake",
            "normalize_square_power_then_apply_source_snippet_intake",
            "same theorem data after squaring to coefficient 6",
            "H0/conductor39",
        ),
        row(
            "coefficient1_exact_root_value",
            "exact theorem for the coefficient-1 root row; sixth power gives the current coefficient-6 row",
            "normalize_then_intake",
            "normalize_sixth_power_then_apply_source_snippet_intake",
            "same theorem data after taking the sixth power to coefficient 6",
            "H0/conductor39",
        ),
        row(
            "exact_unique_power_value",
            "exact finite theorem for R^3, R^5, R^13, or R^39 for one normalized legal row",
            "normalize_then_intake",
            "normalize_unique_power_root_then_apply_source_snippet_intake",
            "same theorem data after unique root recovery in F_p^*",
            "H0/conductor39",
        ),
        row(
            "selected_ambiguous_power_value",
            "exact finite theorem for R^11 or another non-bijective power plus branch/scalar data selecting the root",
            "normalize_then_intake",
            "normalize_selected_power_value_then_apply_source_snippet_intake",
            "same theorem data after selected-root recovery",
            "H0/conductor39",
        ),
        row(
            "power_divisor_with_value_normalization",
            "divisor/additive theorem for R^e plus finite value/additive normalization fixing the powered value",
            "normalize_then_intake",
            "normalize_power_divisor_with_value_data_then_apply_source_snippet_intake",
            "same theorem data after finite normalization and root recovery",
            "H0/conductor39",
        ),
        row(
            "reciprocal_orientation_unspecified",
            "outside-doubling or reciprocal-looking row with no explicit reciprocal orientation or boundary sign",
            "repair",
            "repair_reciprocal_orientation_or_boundary_sign_missing",
            "explicit reciprocal orientation and -Norm_156 boundary, or rewrite as the oriented legal row",
            "H0/conductor39",
        ),
        row(
            "legal_minimal_h90_preimage_only",
            "one of the four legal support-12 H90 preimages or mod-13 rectangle edges, but no finite value/divisor theorem",
            "repair",
            "repair_selector_only",
            "finite value/divisor theorem for the corresponding support-156 Yang product",
            "H0/conductor39",
        ),
        row(
            "exact_quartic_selector_without_value_theorem",
            "exact row-antisymmetric C4_1 phase selecting one legal edge, but no finite value/divisor theorem",
            "repair",
            "repair_value_divisor_theorem_missing",
            "scalar-fixed finite value/divisor theorem for the selected row",
            "H0/conductor39",
        ),
        row(
            "coarse_quartic_phase_or_magnitude_only",
            "one sign of the quartic phase, quartic magnitude, quadratic component, or boundary-visible component only",
            "repair",
            "repair_quartic_edge_selection_missing",
            "exact row-antisymmetric C4_1 phase selecting one legal edge",
            "H0/conductor39",
        ),
        row(
            "quartic_phase_without_row_sign",
            "quotient-C4 order-4 phase without the row-antisymmetric mod-3 tensor sign and zero proper pushforwards",
            "repair",
            "repair_mixed_tensor_missing",
            "row-antisymmetric mixed tensor structure for the conductor-39 source row",
            "H0/conductor39",
        ),
        row(
            "same_parity_quartic_phase",
            "order-4 phase attached to a same-parity edge or wrong sparse quotient edge",
            "reject",
            "reject_zero_boundary_wrong_edge",
            "same-parity edges have zero W boundary or the wrong mixed tensor target",
            "kill",
        ),
        row(
            "quartic_phase_boundary_sign_unspecified",
            "exact C4_1 phase stated without oriented row data or boundary-sign convention",
            "repair",
            "repair_reciprocal_orientation_or_boundary_sign_missing",
            "oriented row data or reciprocal row with -Norm_156 boundary",
            "H0/conductor39",
        ),
        row(
            "quartic_phase_collision_as_different_edge",
            "negated reciprocal C4_1 phase treated as the opposite oriented edge without boundary sign",
            "repair",
            "repair_phase_orientation_collision",
            "boundary sign/orientation data distinguishing reciprocal row from opposite edge",
            "H0/conductor39",
        ),
        row(
            "quartic_reciprocal_phase_plus_boundary",
            "reciprocal C4_1 phase asserted with the positive Norm_156(Y_507) boundary",
            "reject",
            "reject_orientation_boundary_mismatch",
            "reciprocal phase carries -Norm_156 boundary, not the positive boundary",
            "kill",
        ),
        row(
            "support12_h90_preimage_boundary_control",
            "one of the twelve support-12 H90 preimages with the current W boundary, but not a legal mixed source object",
            "reject",
            "reject_boundary_control_not_source_object",
            "proper-axis pushforward failure; only the four mixed support-12 minimizers are legal",
            "kill",
        ),
        row(
            "support_below_12_h90_selector",
            "claimed H90 preimage of the current W with support below 12",
            "reject",
            "reject_h90_support_below_lower_bound",
            "orbitwise Hilbert-90 lower bound forces support at least 12",
            "kill",
        ),
        row(
            "w_boundary_nonunit_edge_combination",
            "integer combination of the four source-graph edges with coefficient sum 1 but not a unit edge vector",
            "repair",
            "repair_edge_plus_boundary_zero_lattice",
            "finite value for the boundary-zero lattice part, selector/orientation data, or direct one-edge theorem",
            "H0/conductor39",
        ),
        row(
            "source_legality_or_generation_only",
            "Koo-Shin/Yang/Kubert-Lang/class-field generation, distribution/root-descent, or source-legality statement only",
            "repair",
            "repair_source_legality_only",
            "finite value/divisor theorem for one normalized legal row",
            "sources",
        ),
        row(
            "mixed_unit_without_yang_lift",
            "mixed conductor-39 U_chi/W or chi_3 tensor chi_13 source word, but no level-507 Yang lift",
            "repair",
            "repair_yang_lift_missing",
            "level-507 Yang lift to the support-156 product",
            "H0/conductor39",
        ),
        row(
            "mixed_yang_without_h90_descent",
            "mixed conductor-39 Yang lift to level 507, but no Hilbert-90 descent or Norm_156(Y_507) boundary",
            "repair",
            "repair_h90_descent_boundary_missing",
            "Hilbert-90 descent with boundary Norm_156(Y_507)",
            "H0/conductor39",
        ),
        row(
            "yang_h90_source_without_finite_theorem",
            "legal support-156 Yang/H90 product with Norm_156(Y_507) boundary, but no finite value/divisor theorem",
            "repair",
            "repair_value_divisor_theorem_missing",
            "finite value/divisor theorem for the selected support-156 row",
            "H0/conductor39",
        ),
        row(
            "coset_selector_or_Q_source_only",
            "compact conductor-39 Q quotient, coset selector, or source word without a finite theorem",
            "repair",
            "repair_finite_value_divisor_theorem_missing",
            "finite value/divisor theorem for Q, Q^3, Q^6, or the selected Yang lift",
            "H0/conductor39",
        ),
        row(
            "Q6_boundary_only",
            "Q^6 Hilbert-90 boundary identity with no scalar-fixed finite value/additive data",
            "repair",
            "repair_additive_or_value_normalization_missing",
            "scalar-fixed finite value/additive data, not just the Hilbert-90 boundary",
            "H0/conductor39",
        ),
        row(
            "primitive_U_chi_power_only",
            "primitive U_chi=-chi_39 or a power of the compact quotient, but no Yang/H90 finite theorem",
            "repair",
            "repair_yang_lift_descent_and_finite_theorem_missing",
            "Yang lift, Hilbert-90 descent, and finite theorem for the selected row",
            "H0/conductor39",
        ),
        row(
            "pure_character_degree6_norm",
            "degree-6 norm of the pure conductor-39 character word offered as the value theorem",
            "reject",
            "reject_pure_character_degree6_norm_cancels",
            "Frobenius alternation makes the degree-6 norm zero",
            "kill",
        ),
        row(
            "generic_cm_generation_as_framing",
            "generic CM, ray-class, class-field, or unit-generation statement presented as DANGER3 framing without an exact p25 finite identity and non-CM/policy framing",
            "reject",
            "reject_generic_cm_generation_not_framing",
            "explicit p25 finite identity plus non-CM finite-field framing or external policy yes",
            "kill",
        ),
        row(
            "boundary_only",
            "Hilbert-90 boundary, period norm, or Norm_156(Y_507) identity with no value/divisor theorem",
            "repair",
            "repair_boundary_only",
            "finite value/divisor identity for one normalized legal row",
            "H0/conductor39",
        ),
        row(
            "divisor_only_with_h90_boundary",
            "divisor identity plus Hilbert-90 boundary, but no finite additive/value normalization fixing the F_p^* scalar",
            "repair",
            "repair_constant_normalization_missing",
            "additive/value normalization or finite framing fixing the F_p^* scalar",
            "H0/conductor39",
        ),
        row(
            "principal_divisor_or_divisor_class_only",
            "principal-divisor or divisor-class equality for the legal row, with no scalar-fixing finite additive/value normalization",
            "repair",
            "repair_additive_normalization_missing",
            "H90 boundary plus scalar-fixing finite additive/value normalization",
            "H0/conductor39",
        ),
        row(
            "value_up_to_fp_scalar",
            "finite value theorem stated only up to multiplication by an unspecified F_p^* scalar",
            "repair",
            "repair_constant_normalization_missing",
            "specified scalar, branch/root/telescoping context, or normalized value",
            "H0/conductor39",
        ),
        row(
            "additive_relation_without_selected_row",
            "finite additive relation for a dense norm, family average, or formal control, but no selected legal support-156 row",
            "repair",
            "repair_selected_row_missing",
            "legal support-156 row selection before applying the additive normalization",
            "H0/conductor39",
        ),
        row(
            "period_norm_identity_only",
            "identity or value for the dense Norm_156(Y_507) boundary only",
            "repair",
            "repair_norm_only_h90_descent_missing",
            "legal support-156 Hilbert-90 descent selecting one row",
            "H0/conductor39",
        ),
        row(
            "dense_unit_character_norm_value",
            "finite theorem for the dense +/-6 unit-character period norm",
            "repair",
            "repair_norm_only_row_selection_missing",
            "selected legal 78-over-78 product row and finite theorem for that row",
            "H0/conductor39",
        ),
        row(
            "ambient780_or_value_without_period156",
            "ambient-period-780 value theorem, formal one-coset value, or bare H0/Y507 value theorem without period-156 context",
            "repair",
            "repair_period156_branch_context_missing",
            "support-period-156 branch/root/telescoping context",
            "value-route",
        ),
        row(
            "ambient780_mu11_power_or_quotient",
            "ambient-period-780 value theorem only after taking an 11th power or quotienting by mu_11",
            "repair",
            "repair_mu11_power_or_quotient_not_value",
            "actual period-156 branch/root/telescoping data selecting one F_p value",
            "value-route",
        ),
        row(
            "degree6_value_orbit_without_descent",
            "degree-6 value/orbit or primitive-root expression with no conjugate/norm descent to F_p",
            "repair",
            "repair_degree6_orbit_without_descent",
            "conjugate/norm descent back to F_p or Hilbert-90 ratio boundary",
            "value-route",
        ),
        row(
            "degree6_norm_without_selected_row",
            "degree-6 norm/descent to F_p, but no selected legal support-156 row",
            "repair",
            "repair_descent_without_selected_legal_row",
            "legal support-156 row selection after descent",
            "value-route",
        ),
        row(
            "finite_payload_without_source",
            "local finite product payload or hash match with no arithmetic source theorem",
            "repair",
            "repair_arithmetic_source_theorem_missing",
            "challenge-legal arithmetic source theorem",
            "H0/conductor39",
        ),
        row(
            "coefficient6_root_without_orientation",
            "attempt to infer a coefficient-3 or coefficient-1 root from coefficient-6 value data",
            "repair",
            "repair_coefficient6_root_orientation_missing",
            "explicit oriented root/sign data; square and sixth roots have a two-element kernel",
            "H0/conductor39",
        ),
        row(
            "ambiguous_power_value_without_branch",
            "exact theorem for R^2, R^4, R^6, R^11, R^22, R^44, R^156, or R^780 with no branch or scalar selector",
            "repair",
            "repair_power_kernel_orientation_or_branch_missing",
            "explicit orientation, branch, or scalar data selecting one root",
            "H0/conductor39",
        ),
        row(
            "mu11_or_mu44_scalar_unspecified",
            "finite value theorem only up to a mu_11, mu_22, or mu_44 scalar",
            "repair",
            "repair_root_of_unity_scalar_missing",
            "explicit scalar/branch/orientation selecting one F_p value",
            "H0/conductor39",
        ),
        row(
            "power_divisor_without_value_normalization",
            "divisor/Hilbert-90 theorem for R^e or boundary eW, but no finite value/additive normalization",
            "repair",
            "repair_power_divisor_value_normalization_missing",
            "finite value/additive normalization fixing the powered value before rooting",
            "H0/conductor39",
        ),
        row(
            "outside_doubling_or_projection",
            "outside-doubling multiplier used as an oriented row, prime-axis projection, one-coset gauge, or proper suborbit",
            "reject",
            "reject_not_current_legal_target",
            "one normalized oriented row, reciprocal orientation repair, or a new theorem target",
            "kill",
        ),
        row(
            "yang_lift_wrong_boundary_or_target",
            "level-507 lift, projection, suborbit, or altered product whose boundary is not Norm_156(Y_507) for the current legal target",
            "reject",
            "reject_yang_lift_boundary_or_target_mismatch",
            "legal mixed conductor-39 target with Norm_156(Y_507) boundary",
            "kill",
        ),
        row(
            "scaled_boundary_as_current_target",
            "coefficient-1, coefficient-2, or coefficient-3 boundary treated as the current Norm_156(Y_507) boundary",
            "reject",
            "reject_boundary_scale_mismatch",
            "power back to the coefficient-6 row or prove the current boundary directly",
            "kill",
        ),
        row(
            "reciprocal_plus_boundary",
            "reciprocal product asserted with the positive Norm_156(Y_507) boundary",
            "reject",
            "reject_orientation_boundary_mismatch",
            "reciprocal product should carry the opposite Hilbert-90 boundary sign",
            "kill",
        ),
        row(
            "theorem52_constant_product_repair",
            "Koo-Shin 2010 Theorem 5.2 constant-product repair using powers of the four legal rows",
            "reject",
            "reject_theorem52_constant_span_repair",
            "legal quotient-C4 row span has no nonzero constant-exponent vector",
            "kill",
        ),
        row(
            "boundary_control_minimal_preimage",
            "formal one-coset, mod3-balanced-only, axis-leaking, same-parity, or full quadratic-character H90 preimage",
            "reject",
            "reject_boundary_control_not_source_object",
            "proper-axis pushforward failure, zero boundary, or boundary 2W instead of sparse active boundary W",
            "kill",
        ),
        row(
            "norm_with_formal_one_coset_descent",
            "dense norm descended through a formal one-coset control with the same boundary",
            "reject",
            "reject_boundary_control_not_source_object",
            "proper-axis pushforward failure; not the mixed conductor-39 source object",
            "kill",
        ),
        row(
            "broad_quadratic_aggregate_boundary_2w",
            "diagonal product m1*m4 or m2*m8, or equivalent broad quadratic-character aggregate, with boundary 2W",
            "repair",
            "repair_broad_quadratic_aggregate_boundary_2w",
            "selector/factorization to one sparse rectangle edge with W boundary",
            "H0/conductor39",
        ),
        row(
            "all_four_rows_product_boundary_4w",
            "product of all four legal rows, equivalently the square of the broad quadratic aggregate, with boundary 4W",
            "repair",
            "repair_overdemand_square_of_broad_quadratic",
            "one legal support-156 row with W boundary is enough and still missing",
            "H0/conductor39",
        ),
        row(
            "row_quotient_boundary_zero",
            "quotient of two legal rows, hence a Frobenius-invariant boundary-zero relation",
            "repair",
            "repair_boundary_zero_quotient_only",
            "one-row value/divisor theorem; quotient has zero H90 boundary",
            "H0/conductor39",
        ),
        row(
            "aggregate_plus_quotient_row_square",
            "broad diagonal aggregate plus matching row quotient, recovering twice one legal row in the exponent lattice",
            "repair",
            "repair_row_square_bridge_halving_missing",
            "halving/root/orientation data selecting the legal row, or direct one-row theorem",
            "H0/conductor39",
        ),
        row(
            "q_diagonal_value_only",
            "Q value theorem for the diagonal aggregate projection Q_antisym=m1+m4=m2+m8, without split/orientation data",
            "repair",
            "support_diagonal_aggregate_selector_missing",
            "boundary-zero split/orientation data or direct one-edge theorem",
            "H0/conductor39",
        ),
        row(
            "q_plus_row_quotient_without_root",
            "Q diagonal aggregate plus matching boundary-zero row quotient, reaching twice one edge",
            "repair",
            "repair_oriented_square_root_missing",
            "halving/root/orientation data after reaching twice one edge",
            "H0/conductor39",
        ),
        row(
            "q_plus_explicit_oriented_diagonal_split",
            "Q theorem plus explicit oriented diagonal split normalizing to one legal edge",
            "normalize_then_intake",
            "normalize_to_one_edge_then_apply_source_snippet_intake",
            "same theorem data after explicit oriented diagonal-split normalization",
            "H0/conductor39",
        ),
        row(
            "q_wrong_zero_boundary_split",
            "Q theorem paired with a same-parity or otherwise wrong zero-boundary split",
            "reject",
            "reject_zero_boundary_wrong_edge",
            "split data must recover one of m1,m2,m4,m8 with the current oriented boundary",
            "kill",
        ),
        row(
            "q_square_exact_fp_value",
            "exact scalar-fixed F_p value for the Q diagonal plus matching pure quartic split, hence a square of one legal edge",
            "repair",
            "repair_extraction_map_missing_after_two_root_row_payload",
            "two F_p row roots exist; DANGER3 framing and same-j/X_1(16)/halving or direct A,x0 extraction map still missing",
            "H0/conductor39",
        ),
        row(
            "q_square_value_up_to_scalar",
            "Q-square value theorem with an unspecified F_p^* scalar",
            "repair",
            "repair_scalar_and_root_orientation_missing",
            "specified scalar before the two-root payload is concrete",
            "H0/conductor39",
        ),
        row(
            "q_square_sign_from_divisor_h90_or_phase",
            "attempt to choose the Q-square root sign from divisor, Hilbert-90 boundary, or quotient-character phase",
            "reject",
            "reject_sign_invisible_to_current_invariants",
            "constant sign has zero divisor/H90 boundary and does not alter exponent-character data",
            "kill",
        ),
        row(
            "row_square_value_theorem",
            "finite theorem for the square of one legal row, equivalently 2*row in exponent notation",
            "repair",
            "repair_row_square_root_sign_missing",
            "explicit root/sign/orientation data selecting R rather than -R, or direct one-row theorem",
            "H0/conductor39",
        ),
        row(
            "row_square_with_h90_boundary_2w",
            "row-square theorem with doubled Hilbert-90 boundary 2W",
            "repair",
            "repair_boundary_scale_and_root_sign_missing",
            "one-row W-boundary theorem plus explicit root/sign/orientation",
            "H0/conductor39",
        ),
        row(
            "direct_root_or_sqrt_shortcut",
            "direct F_p primitive order-39 root or sqrt(-39) scalar shortcut",
            "reject",
            "reject_arithmetic_shortcut",
            "ord_39(p)=6 and sqrt(-39) not in F_p",
            "kill",
        ),
        row(
            "mu39_scalar_as_fp",
            "primitive order-39 root of unity used as an F_p scalar normalizer",
            "reject",
            "reject_root_of_unity_not_in_fp",
            "mu_39 is not contained in F_p^* for p25",
            "kill",
        ),
        row(
            "power_boundary_as_current_target",
            "powered Hilbert-90 boundary eW treated as the current W boundary",
            "reject",
            "reject_scaled_boundary_as_current_target",
            "eW is not the current W boundary unless the theorem powers back to the row",
            "kill",
        ),
        row(
            "independent_p16_q507",
            "independent level-16 and level-507 data with no same-j gluing",
            "reject",
            "reject_unglued_components",
            "same j-invariant / same elliptic curve bridge",
            "extraction",
        ),
        row(
            "same_j_invariant_only",
            "matching j-invariant or isomorphism class but no glued torsion points",
            "repair",
            "repair_same_j_invariant_only",
            "explicit same-curve P16/Q507 pair, order-8112 generator, or direct A,xP16",
            "extraction",
        ),
        row(
            "same_j_bridge_only",
            "same-j X_1(8112) bridge or order-8112 generator with no practical X_1(16) payload",
            "extraction_progress",
            "bridge_progress_x16_payload_missing",
            "X_1(16) y plus model root or direct A,xP16",
            "extraction",
            extraction=True,
        ),
        row(
            "x16_surface_no_x0",
            "practical A,xP16 or y plus model root, but no halving/x0 payload",
            "extraction_progress",
            "x16_surface_reached_halving_missing",
            "38-link x-chain, active witness chain, direct x0, or vpp.py",
            "extraction",
            extraction=True,
        ),
        row(
            "branch_word_without_values",
            "halving branch word without concrete square-root witnesses, x-chain, or x0",
            "reject",
            "reject_branch_word_without_values",
            "actual square-root witnesses, x-chain, direct x0, or vpp.py",
            "extraction",
        ),
        row(
            "official_vpp_verified_triple",
            "official vpp.py verifies concrete p25 (p,A,x0)",
            "submission",
            "submission_ready",
            "none",
            "submission",
            source_closed=True,
            extraction=True,
            submission=True,
        ),
    )


def build_rubric() -> CurrentExpertResponseRubric:
    markers = evidence_markers()
    rows = response_rows()
    markers_ok = sum(marker_row.ok for marker_row in markers)
    frontdoor = sum(row.category == "frontdoor_source_close" for row in rows)
    heavy = sum(row.category == "heavy_upstream_close" for row in rows)
    normalize = sum(row.category == "normalize_then_intake" for row in rows)
    repairs = sum(row.category == "repair" for row in rows)
    rejects = sum(row.category == "reject" for row in rows)
    extraction = sum(row.category == "extraction_progress" for row in rows)
    submission = sum(row.submission_ready for row in rows)
    current_source = 0
    current_submission = 0
    expected = (
        "source_stage_win_route_to_extraction_contract",
        "source_stage_win_route_to_extraction_contract",
        "source_stage_win_route_to_extraction_contract",
        "source_stage_win_route_to_extraction_contract",
        "repair_reverse_exactp_selector_missing",
        "repair_exact_selector_theorem_missing",
        "repair_theta2_intake_missing",
        "repair_exactp_orientation_branch_missing",
        "repair_period156_branch_selection_missing",
        "reject_wrong_exactp_payload",
        "reject_by_finite_geometry_rigidity",
        "repair_period156_branch_selection_missing",
        "repair_arithmetic_source_missing",
        "repair_exact_finite_identity_missing",
        "normalize_row_then_apply_source_snippet_intake",
        "normalize_reciprocal_then_apply_source_snippet_intake",
        "normalize_root_then_apply_source_snippet_intake",
        "normalize_value_then_apply_source_snippet_intake",
        "normalize_additive_value_then_apply_source_snippet_intake",
        "normalize_descent_then_apply_source_snippet_intake",
        "normalize_value_descent_then_apply_source_snippet_intake",
        "route_through_period156_value_source_hook",
        "normalize_h90_preimage_then_apply_source_snippet_intake",
        "normalize_cube_power_then_apply_source_snippet_intake",
        "normalize_square_power_then_apply_source_snippet_intake",
        "normalize_sixth_power_then_apply_source_snippet_intake",
        "normalize_unique_power_root_then_apply_source_snippet_intake",
        "normalize_selected_power_value_then_apply_source_snippet_intake",
        "normalize_power_divisor_with_value_data_then_apply_source_snippet_intake",
        "repair_reciprocal_orientation_or_boundary_sign_missing",
        "repair_selector_only",
        "repair_value_divisor_theorem_missing",
        "repair_quartic_edge_selection_missing",
        "repair_mixed_tensor_missing",
        "reject_zero_boundary_wrong_edge",
        "repair_reciprocal_orientation_or_boundary_sign_missing",
        "repair_phase_orientation_collision",
        "reject_orientation_boundary_mismatch",
        "reject_boundary_control_not_source_object",
        "reject_h90_support_below_lower_bound",
        "repair_edge_plus_boundary_zero_lattice",
        "repair_source_legality_only",
        "repair_yang_lift_missing",
        "repair_h90_descent_boundary_missing",
        "repair_value_divisor_theorem_missing",
        "repair_finite_value_divisor_theorem_missing",
        "repair_additive_or_value_normalization_missing",
        "repair_yang_lift_descent_and_finite_theorem_missing",
        "reject_pure_character_degree6_norm_cancels",
        "reject_generic_cm_generation_not_framing",
        "repair_boundary_only",
        "repair_constant_normalization_missing",
        "repair_additive_normalization_missing",
        "repair_constant_normalization_missing",
        "repair_selected_row_missing",
        "repair_norm_only_h90_descent_missing",
        "repair_norm_only_row_selection_missing",
        "repair_period156_branch_context_missing",
        "repair_mu11_power_or_quotient_not_value",
        "repair_degree6_orbit_without_descent",
        "repair_descent_without_selected_legal_row",
        "repair_arithmetic_source_theorem_missing",
        "repair_coefficient6_root_orientation_missing",
        "repair_power_kernel_orientation_or_branch_missing",
        "repair_root_of_unity_scalar_missing",
        "repair_power_divisor_value_normalization_missing",
        "reject_not_current_legal_target",
        "reject_yang_lift_boundary_or_target_mismatch",
        "reject_boundary_scale_mismatch",
        "reject_orientation_boundary_mismatch",
        "reject_theorem52_constant_span_repair",
        "reject_boundary_control_not_source_object",
        "reject_boundary_control_not_source_object",
        "repair_broad_quadratic_aggregate_boundary_2w",
        "repair_overdemand_square_of_broad_quadratic",
        "repair_boundary_zero_quotient_only",
        "repair_row_square_bridge_halving_missing",
        "support_diagonal_aggregate_selector_missing",
        "repair_oriented_square_root_missing",
        "normalize_to_one_edge_then_apply_source_snippet_intake",
        "reject_zero_boundary_wrong_edge",
        "repair_extraction_map_missing_after_two_root_row_payload",
        "repair_scalar_and_root_orientation_missing",
        "reject_sign_invisible_to_current_invariants",
        "repair_row_square_root_sign_missing",
        "repair_boundary_scale_and_root_sign_missing",
        "reject_arithmetic_shortcut",
        "reject_root_of_unity_not_in_fp",
        "reject_scaled_boundary_as_current_target",
        "reject_unglued_components",
        "repair_same_j_invariant_only",
        "bridge_progress_x16_payload_missing",
        "x16_surface_reached_halving_missing",
        "reject_branch_word_without_values",
        "submission_ready",
    )
    row_ok = (
        markers_ok == len(markers)
        and len(rows) == 95
        and frontdoor == 3
        and heavy == 1
        and normalize == 16
        and repairs == 50
        and rejects == 22
        and extraction == 2
        and submission == 1
        and current_source == 0
        and current_submission == 0
        and tuple(row.decision for row in rows) == expected
        and all(row.ok for row in rows)
    )
    return CurrentExpertResponseRubric(
        evidence_markers=markers,
        response_rows=rows,
        evidence_markers_ok=markers_ok,
        frontdoor_source_closing_rows=frontdoor,
        heavy_upstream_rows=heavy,
        normalize_then_intake_rows=normalize,
        repair_rows=repairs,
        reject_rows=rejects,
        extraction_progress_rows=extraction,
        submission_ready_rows=submission,
        current_source_stage_closers=current_source,
        current_submission_ready=current_submission,
        row_ok=row_ok,
    )


def main() -> int:
    rubric = build_rubric()
    for marker_row in rubric.evidence_markers:
        print(f"marker {marker_row.name}: {'ok' if marker_row.ok else 'MISSING'}")
    print("response_rows")
    for row_item in rubric.response_rows:
        print(
            "  "
            f"{row_item.name}: category={row_item.category} decision={row_item.decision} "
            f"source_closed={int(row_item.source_stage_closed)} "
            f"extraction={int(row_item.extraction_stage_reached)} "
            f"submission={int(row_item.submission_ready)} lane={row_item.continue_lane}"
        )
        print(f"    shape={row_item.answer_shape}")
        print(f"    missing_or_falsifier={row_item.first_missing_or_falsifier}")
    print("counts")
    print(f"  evidence_markers_ok={rubric.evidence_markers_ok}/{len(rubric.evidence_markers)}")
    print(f"  frontdoor_source_closing_rows={rubric.frontdoor_source_closing_rows}")
    print(f"  heavy_upstream_rows={rubric.heavy_upstream_rows}")
    print(f"  normalize_then_intake_rows={rubric.normalize_then_intake_rows}")
    print(f"  repair_rows={rubric.repair_rows}")
    print(f"  reject_rows={rubric.reject_rows}")
    print(f"  extraction_progress_rows={rubric.extraction_progress_rows}")
    print(f"  submission_ready_rows={rubric.submission_ready_rows}")
    print(f"  current_source_stage_closers={rubric.current_source_stage_closers}")
    print(f"  current_submission_ready={rubric.current_submission_ready}")
    print("interpretation")
    print("  expert_answers_should_first_match_source_close_or_named_falsifier=1")
    print("  row_presentations_normalize_before_source_snippet_intake=1")
    print("  extraction_answers_route_through_extraction_payload_contract=1")
    print("  current_frontier_still_has_zero_source_closers_and_zero_submissions=1")
    print(f"p25_v2_current_expert_response_rubric_rows={int(rubric.row_ok)}/1")
    return 0 if rubric.row_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
