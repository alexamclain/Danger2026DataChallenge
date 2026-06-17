# P25 V2 Positive Theorem Clause Matcher

Date: 2026-06-16

Marker: `p25_v2_positive_theorem_clause_matcher_rows=1/1`

## Purpose

Give future expert answers and source snippets a positive clause matcher for
the current H0/Y507 theorem front door. This page is narrower than the full
expert-response rubric: it records exactly what must be present before an
answer can be promoted to a source-stage theorem candidate, and names the
nearest repair/reject cases.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_positive_theorem_clause_matcher_gate.py
```

## Positive Routes

```text
canonical_h0_divisor_additive_identity
  requires = one_exact_oriented_edge_R_m
             arithmetic_source_theorem
             Norm_156_Y_507_boundary
             scalar_fixed_finite_divisor_additive_identity
  then missing = DANGER3 finite-identity / non-CM framing

quartic_character_finite_theorem
  requires = Norm_156_Y_507_or_W_boundary
             exact_row_antisymmetric_C4_1_phase
             mixed_tensor_row_sign
             arithmetic_source_theorem
             scalar_fixed_finite_divisor_additive_identity
  then missing = DANGER3 finite-identity / non-CM framing

canonical_h0_period156_value_identity
  requires = canonical_H0_value
             one_exact_oriented_edge_R_m
             arithmetic_source_theorem
             Norm_156_Y_507_boundary
             period156_branch_root_telescoping_context
  then missing = DANGER3 finite-identity / non-CM framing

Y_507_period156_value_identity
  requires = Y_507_value
             arithmetic_source_theorem
             period156_branch_root_telescoping_context
             H0_Y507_compatibility_bridge
  then missing = DANGER3 finite-identity / non-CM framing

power_normalized_row_value_theorem
  requires = one_exact_oriented_edge_R_m
             arithmetic_source_theorem
             exact_finite_Fp_value_for_R_m_power_e_with_e_in_3_5_13_39_75_169_507
             inverse_exponent_recovery_mod_pminus1
             Norm_156_Y_507_boundary_or_accepted_period156_bridge
  then missing = DANGER3 finite-identity / non-CM framing

exactp_upstream_bridge_theorem
  requires = exact_75_atom_or_theta2_payload
             orientation_and_bridge_data
             arithmetic_source_theorem
             bridge_75_300_12_312_156
  then missing = DANGER3 framing and extraction after upstream theorem
```

The first five are the first-pass H0/conductor-39/H0-Y507 front-door routes.
The exact-P route remains a
heavier upstream theorem route, not the first-pass default.

## Near Misses

```text
source_legality_only
  decision = repair_finite_theorem_missing
  missing  = finite scalar-fixed value/divisor theorem

boundary_only
  decision = repair_identity_for_one_edge_missing
  missing  = finite identity for one exact oriented edge

h0_value_without_boundary
  decision = repair_boundary_missing
  missing  = H0/Y507 boundary compatibility

h0_or_y507_value_without_period156_context
  decision = repair_period156_branch_context_missing
  missing  = period-156 branch/root/telescoping context

ambient780_or_mu11_value
  decision = repair_period156_value_selection_missing
  missing  = one selected F_p value on the support-period-156 branch

ambiguous_power_value_without_selector
  decision = repair_power_root_selection_missing
  missing  = kernel root selector or one of the bijective exponents 3, 5, 13,
             39, 75, 169, 507

formal_one_coset_value
  decision = reject_boundary_control_not_source_object
  falsifier = proper-axis pushforward and mixed-source fingerprint

projector_or_two_edge_value
  decision = repair_oriented_edge_selection_missing
  missing  = fourth-root or oriented-square-root selector for one edge

exact_quartic_selector_without_finite_theorem
  decision = repair_value_divisor_theorem_missing
  missing  = scalar-fixed finite value/divisor theorem for the selected row

coarse_quartic_phase_or_magnitude_only
  decision = repair_quartic_edge_selection_missing
  missing  = exact row-antisymmetric C4_1 phase selecting one legal edge

quartic_phase_without_row_sign
  decision = repair_mixed_tensor_missing
  missing  = row-antisymmetric mixed tensor structure for the conductor-39
             source row

same_parity_quartic_phase
  decision = reject_zero_boundary_wrong_edge
  falsifier = same-parity edges have zero W boundary or the wrong mixed
              tensor target

finite_payload_without_source
  decision = repair_arithmetic_source_missing
  missing  = challenge-legal arithmetic source theorem

exactp_vocabulary_only
  decision = repair_exactp_theorem_missing
  missing  = exact 75-atom/theta2 payload with bridge and orientation
```

## Counts

```text
evidence_markers_ok = 9/9
h0_y507_frontdoor_routes = 5
exactp_heavy_routes = 1
source_stage_shapes = 6
current_source_theorems = 0
current_submission_ready = 0
near_miss_rows = 14
p25_v2_positive_theorem_clause_matcher_rows=1/1
```

## Verdict

The positive side is now mechanically checkable. A future lead can be promoted
only if it supplies all required clauses for one of the positive routes above.
The closest first-pass route remains the scalar-fixed divisor/additive theorem
for one exact oriented edge. A character-language answer is equivalent only if
it supplies exact row-antisymmetric `C4_1` phase data, mixed tensor row sign,
and the same scalar-fixed finite theorem. The power-normalized row-value route
is equivalent only for exact `R_m^e` source theorems with
`e in {3,5,13,39,75,169,507}` and the row and boundary/period bridge fixed.
The H0/Y507 value route is live only with period-156 branch/root/telescoping
context; exact-P remains the heavier upstream bridge.
