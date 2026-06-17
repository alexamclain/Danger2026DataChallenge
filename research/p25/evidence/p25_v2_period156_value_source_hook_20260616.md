# P25 v2 Period-156 Value Source Hook

Updated: 2026-06-16

## Purpose

State the compact intake rule for Schertz/Shin/Scholl/Siegel-Robert value-side
leads. This page starts from the already fixed H0/conductor-39 target and asks
what kind of value theorem would actually close source stage.

This is not a source theorem. It is a source-hook and first-falsifier screen
for value-side literature or expert answers.

## Pages Read

- `frontier.md`
- `sources/schertz-scholl.md`
- `evidence/p25_ksy_y_siegel_robert_period_value_primary_source_scout_20260613.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_period156_value_source_hook_gate.py
```

The gate returned `p25_v2_period156_value_source_hook_rows=1/1`.

## Required Clauses

```text
one_exact_oriented_edge_or_accepted_theta2_payload
arithmetic_value_source_theorem
support_period_156_branch_root_telescoping_context
finite_Fp_value_selected_not_ambient_mu11_class
boundary_or_bridge_to_Norm_156_Y_507
post_theorem_extraction_routing
```

## Accepted Routes

```text
period156_value_for_oriented_edge
  decision = source_stage_win_route_to_extraction

period156_theta2_payload_with_bridge
  decision = exactp_or_unified_source_win_route_to_extraction
```

The first route is the direct value-side H0/conductor-39 close. The second is
the value-side exact-P/heavy-route hook, but it still has to bridge into the
unified support-156 target or satisfy the exact-P minimal hook.

## Repair Or Reject Routes

```text
schertz_field_generation_only
  decision = repair_exact_value_theorem_missing

shin_generator_only
  decision = repair_exact_value_theorem_missing

scholl_oddD_distribution_only
  decision = repair_exact_period156_payload_missing

period156_vocabulary_no_row
  decision = repair_oriented_edge_or_theta2_payload_missing

exact_value_no_arithmetic_source
  decision = repair_arithmetic_source_theorem_missing

value_up_to_unspecified_fp_scalar
  decision = repair_scalar_or_branch_normalization_missing

ambient780_value_only
  decision = repair_ambient_period780_mu11_branch

ambient780_eleventh_power_or_mu11_quotient
  decision = repair_period156_branch_selection_missing

degree6_value_without_fp_descent
  decision = repair_fp_descent_and_row_selection_missing

direct_scholl_D2_import
  decision = reject_scholl_D2_hypothesis_mismatch

direct_fp_order39_root
  decision = reject_ord39_p_equals_6

sqrt_minus39_scalar
  decision = reject_sqrt_minus39_not_in_Fp
```

## Arithmetic Checks

```text
ord_39(p) = 6
sqrt(-39) in F_p = no
support-period-156 root in F_p^* = unique
ambient-period-780 root branches in F_p^* = 11
direct Scholl D=2 import = blocked by source-hypothesis mismatch
current_period156_value_theorems = 0
```

## Counts

```text
evidence_markers_ok = 7/7
required_clauses = 6
accepted_routes = 2
repair_or_reject_routes = 12
support_period_root_unique = 1
ambient_period_has_mu11 = 1
scholl_direct_d2_import_blocked = 1
current_period156_value_theorems = 0
p25_v2_period156_value_source_hook_rows=1/1
```

## Verdict

The value-side route is still live but narrow. A useful Schertz/Shin/Scholl or
Siegel-Robert answer must give an arithmetic finite value theorem for one
exact oriented support-156 edge, or an accepted period-156 theta2 payload with
bridge data. Class-field generation, ambient-period-780 values, 11th powers,
`mu_11` quotients, degree-6 values without descent, and direct Scholl `D=2`
imports do not close source stage.
