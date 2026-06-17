# P25 v2 Exact-P Minimal Hook

Updated: 2026-06-16

## Purpose

State the narrowest current exact-P question. Exact-P remains the heavier
upstream moonshot, but the finite side is now rigid enough that source search
should ask for a compact hook, not for generic normalized-y, ray-class, or
Kubert-Lang vocabulary.

This page does not claim an exact-P theorem exists. It records what would
activate the heavy route and what remains repair or reject.

## Pages Read

- `frontier.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_exactp_finite_geometry_rigidity_20260616.md`
- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_exactp_to_unified_target_spine_20260616.md`
- `evidence/p25_v2_reverse_exactp_information_loss_20260616.md`
- `evidence/p25_v2_ksy_1007_2307_source_ingest_scan_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_exactp_minimal_hook_gate.py
```

The gate returned `p25_v2_exactp_minimal_hook_rows=1/1`.

## Minimal Question

```text
Does a known arithmetic source theorem emit the compact exact-P packet

  C = (47, 28), D = (22, 3), primitive K = (57, 0), orientation

or an accepted equivalent theta2 / theta2^-1 divisor-additive payload,
where orientation means one of the four raw center/reverse branches accepted
by the branch router, with exact equal-weight 75-atom normalized-y product
data and period-156 or divisor/additive context, so that it feeds the verified
75 -> 300 -> 12 -> 312 -> 156 bridge?
```

## Required Clauses

```text
arithmetic_source_theorem
compact_C_D_K_orientation_or_accepted_theta2_payload
one_of_four_exactp_orientation_branches_or_equivalent_theta2_payload
exact_equal_weight_75_atom_product
period156_or_divisor_additive_context
feeds_75_to_300_to_12_to_312_to_156_bridge
post_theorem_extraction_routing
```

## Accepted Routes

```text
compact_C_D_K_orientation_theorem
  decision = exactp_source_stage_win_route_to_extraction

one_of_four_C_D_K_orientation_branches
  decision = exactp_source_stage_win_route_to_extraction

accepted_theta2_divisor_additive_payload
  decision = exactp_source_stage_win_route_to_extraction

exact_equal_weight_75_atom_theorem
  decision = exactp_source_stage_win_route_to_extraction

explicit_reverse_reconstruction_theorem
  decision = normalize_reverse_then_exactp_intake
```

## Repair Or Reject Routes

```text
ksy_normalized_y_vocabulary_only
  decision = repair_exact_selector_theorem_missing

raw_kubert_lang_exponent_balance_only
  decision = repair_theta2_intake_missing

branchless_C_D_K_orientation_word
  decision = repair_exactp_orientation_branch_missing

theta2_value_without_period156_context
  decision = repair_period156_branch_selection_missing

missing_or_nonprimitive_K_trace
  decision = reject_wrong_exactp_payload

wrong_C_D_or_orientation
  decision = reject_wrong_exactp_payload

nonuniform_or_missing_atom_weights
  decision = reject_by_finite_geometry_rigidity

ambient_period780_value_only
  decision = repair_period156_branch_selection_missing

unified_theorem_without_exactp_selector
  decision = repair_reverse_selector_structure_missing

finite_payload_without_arithmetic_source
  decision = repair_arithmetic_source_missing

generic_ray_class_generation
  decision = repair_exact_finite_identity_missing
```

## Counts

```text
evidence_markers_ok = 7/7
required_clauses = 7
accepted_routes = 5
repair_or_reject_routes = 11
current_exactp_source_theorems = 0
current_submission_ready = 0
p25_v2_exactp_minimal_hook_rows=1/1
```

## Verdict

Exact-P is still live, but the ask is now compact. A source answer must emit
the `C,D,K,orientation` packet with one of the four accepted raw branches, the
exact equal-weight 75-atom theorem, an accepted theta2 payload with period-156
context, or an explicit reverse reconstruction theorem. KSY normalized-y
vocabulary, raw Kubert-Lang balance, branchless orientation words, generic
ray-class generation, or a unified support-156 theorem without exact-P
selector data does not activate this route.
