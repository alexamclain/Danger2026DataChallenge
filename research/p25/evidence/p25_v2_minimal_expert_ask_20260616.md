# P25 v2 Minimal Expert Ask

Updated: 2026-06-17

## Purpose

State the narrowest current expert question after the source-family gap matrix.
This is the page to use when asking whether the remaining H0/conductor-39 gap
is a known theorem, a repairable theorem shape, or a genuine missing result.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_minimal_expert_ask_gate.py
```

The gate returned `p25_v2_minimal_expert_ask_rows=1/1`.

## Minimal Question

```text
For p = 10^25 + 13, does a known arithmetic source theorem give either:

1. a scalar-fixed finite divisor/additive identity, or
2. a support-period-156 finite value theorem with branch/root/telescoping data
   for canonical H0 or Y_507, or
3. an exact finite power-value theorem for R_m^e with
   e in {3,5,13,39,75,169,507} and inverse-exponent recovery,

for one exact oriented quotient-C4 edge R_m, m in {1,2,4,8}, with Hilbert-90
boundary Norm_156(Y_507)?
```

Equivalent compact conductor-39 support-route question:

```text
Can the theorem instead be stated for
Q = prod_{h in <2>} E_{7h}/E_h
with Frob_p(Q)=Q^-1,
either as a finite value theorem for Q with period-156 branch/root/telescoping
context, or as a finite theorem for the Hilbert-90 preimage Q^3 with
Q^6=(1-Frob_p)(Q^3)?
```

This `Q` route is useful only if it feeds the period-156 value hook or the
source-snippet intake. `Q` source language alone, `Q^6` boundary data alone, or
the primitive character word without finite theorem data is still a repair row;
the pure degree-6 norm of the conductor-39 character is rejected because it
cancels.
If the Q route produces an exact scalar-fixed value for the resulting square
of a legal edge, it gives only a bounded two-root row-value payload. It is not
a source-stage theorem close and is not extraction-ready without an explicit
map to same-j/X_1(16)/halving data or concrete `(A,x0)` candidates.

The Q diagonal-normalization screen adds the missing follow-up: since
`Q_antisym=m1+m4=m2+m8`, a Q theorem must also supply an oriented diagonal
split/root, or directly prove one edge, before it can become a source-stage
candidate. Q plus a row quotient reaches only twice one edge until oriented
root data is supplied.

Equivalently, the answer must prove one exact support-156 H0/conductor-39
product row, not a projection, aggregate, row square, vertex, quotient,
boundary-only statement, or source-legality statement. If the answer is stated
in character language, it must also give the exact row-antisymmetric `C4_1`
phase selecting that edge, not just one sign, magnitude, quadratic component,
or boundary-visible component. The phase must also be tied to the oriented row
or boundary-sign convention: reciprocal phase with the positive
`Norm_156(Y_507)` boundary is rejected.

All accepted presentations are now routed through the source-stage
normalization spine. Direct one-edge, quartic-selector, row-labeled orbit,
reciprocal-minus-boundary, bijective-power, and support-period-156 value
answers count only when their clauses uniquely normalize to one scalar-fixed
legal support-156 row. Exact-P remains a heavier upstream route into the same
downstream extraction ladder.

## Required Clauses

```text
one_exact_oriented_edge_R_m
exact_row_antisymmetric_C4_1_phase_or_direct_edge_payload
oriented_row_data_or_boundary_sign_for_quartic_phase
arithmetic_source_theorem
hilbert90_boundary_Norm_156_Y_507
scalar_fixed_finite_divisor_additive_or_period156_value
compact_Q_route_has_period156_or_finite_Q3_theorem
Q_route_has_diagonal_split_or_direct_edge_after_value_data
Q_square_exact_value_requires_extraction_map_after_two_roots
power_normalized_route_has_bijective_exponent_and_inverse_recovery
post_theorem_extraction_routing
```

## Accepted Routes

```text
scalar_fixed_divisor_additive_theorem
  decision = source_stage_win_route_to_extraction_contract

period156_value_theorem_with_branch_context
  decision = source_stage_win_route_to_extraction_contract
  accepted = canonical H0 value with Norm_156(Y_507) boundary, or Y_507 value
             with period-156 context

exactp_upstream_theorem_via_minimal_hook
  decision = source_stage_win_route_to_extraction_contract
  accepted = compact exact-P hook with one of the four accepted orientation
             branches, or an equivalent theta2/theta2-inverse payload with
             period-156 context, feeding 75->300->12->312->156

norm_one_Q_value_theorem_with_period156_context
  decision = route_through_period156_value_source_hook

explicit_Q3_hilbert90_preimage_with_finite_theorem
  decision = normalize_h90_preimage_then_apply_source_snippet_intake

Q_plus_explicit_oriented_diagonal_split
  decision = normalize_to_one_edge_then_apply_source_snippet_intake

power_normalized_row_value_theorem
  decision = normalize_unique_power_then_apply_source_snippet_intake
  accepted = exact source theorem for R_m^e with
             e in {3,5,13,39,75,169,507} on one legal row, plus
             inverse-exponent recovery modulo p-1 and the accepted
             boundary/period bridge

```

## Immediate Repair Or Reject Routes

```text
source_legality_only
  decision = repair_finite_theorem_missing

boundary_only
  decision = repair_identity_for_one_edge_missing

unspecified_fp_scalar
  decision = repair_scalar_normalization_missing

period780_or_mu11_only
  decision = repair_period156_value_selection_missing

degree6_value_without_fp_descent
  decision = repair_fp_descent_missing

nonunit_w_boundary_edge_combination
  decision = repair_boundary_zero_content_missing

aggregate_or_row_square_only
  decision = repair_oriented_edge_selection_missing

projector_values_without_fourth_root
  decision = repair_mu4_root_selection_missing

two_edge_pair_without_oriented_square_root
  decision = repair_sign_or_root_missing

Q_square_exact_value_without_extraction_map
  decision = repair_extraction_map_missing_after_two_root_row_payload

Q_square_value_up_to_scalar
  decision = repair_scalar_and_root_orientation_missing

Q_square_sign_from_divisor_h90_or_phase
  decision = reject_sign_invisible_to_current_invariants

exact_quartic_selector_without_finite_theorem
  decision = repair_value_divisor_theorem_missing

coarse_quartic_phase_or_magnitude_only
  decision = repair_quartic_edge_selection_missing

reciprocal_quartic_phase_without_boundary_sign
  decision = repair_reciprocal_orientation_or_boundary_sign_missing

reciprocal_quartic_phase_with_positive_boundary
  decision = reject_orientation_boundary_mismatch

exactp_vocabulary_without_75_atom_theorem
  decision = repair_exactp_theorem_missing

exactp_branchless_orientation_word
  decision = repair_exactp_orientation_branch_missing

exactp_theta2_without_period156_context
  decision = repair_period156_branch_selection_missing

wrong_exactp_packet
  decision = reject_wrong_exactp_payload

finite_payload_without_source
  decision = repair_arithmetic_source_missing

generic_cm_or_class_field_generation
  decision = repair_danger3_finite_framing_missing

coset_selector_or_Q_source_only
  decision = repair_finite_value_divisor_theorem_missing

Q_diagonal_value_only
  decision = support_diagonal_aggregate_selector_missing

Q_plus_row_quotient_without_root
  decision = repair_oriented_square_root_missing

Q_wrong_zero_boundary_split
  decision = reject_zero_boundary_wrong_edge

Q6_boundary_only
  decision = repair_additive_or_value_normalization_missing

primitive_U_chi_power_only
  decision = repair_yang_lift_descent_and_finite_theorem_missing

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels

ambiguous_power_value_without_selector
  decision = repair_power_root_selection_missing
```

## Counts

```text
evidence_markers_ok = 23/23
required_clauses = 11
accepted_routes = 7
repair_or_reject_routes = 30
current_source_theorems = 0
current_submission_ready = 0
p25_v2_minimal_expert_ask_rows=1/1
```

## Verdict

The live mathematical ask is now small enough to send as a yes/no theorem
question. A useful expert answer either supplies one accepted route above and
normalizes through the source-stage spine, or gives a sharp falsifier for that
exact theorem shape. If the answer takes the exact-P escape hatch, it must pass
the minimal exact-P hook: branchless `C,D,K,orientation` language, theta2
values without period-156 context, and wrong packets do not change exact-P
status. Anything else should be routed through the repair/reject rows before it
changes the H0, conductor-39, or exact-P lane status. If the answer uses the
compact `Q` quotient, it must give the value/H90 finite theorem data listed
above plus the diagonal split/root or direct one-edge data; otherwise it stays
support language, not a source-stage close.
