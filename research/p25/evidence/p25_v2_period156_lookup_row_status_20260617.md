# P25 v2 Period-156 Lookup-Row Status

Updated: 2026-06-17

Marker: `p25_v2_period156_lookup_row_status_rows=1/1`

## Purpose

Turn the second row of the priority-1 source lookup capsule into a compact
source/expert checklist. This artifact does not re-audit all value-side prior
art; it summarizes the already validated period-156 branch contract, source
hook, H0/Y507 compatibility screen, Schertz/Shin/Scholl boundary, theta2
support contract, Sprang intake, and value-side candidate sweep.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/schertz-scholl.md`
- `sources/sprang.md`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_period156_value_candidate_sweep_20260617.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_source_action_registry_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_period156_lookup_row_status_gate.py
```

The gate returned `p25_v2_period156_lookup_row_status_rows=1/1`.

## Status Rows

```text
canonical_h0_period156_value
  current_status = live_not_in_hand
  accepted_hook  = arithmetic finite F_p value theorem for canonical H0 with
                   Norm_156(Y_507) boundary and period-156 branch/root/
                   telescoping data
  first_falsifier = ambient-period-780 value, mu_11 quotient, value up to
                    scalar, or source vocabulary without exact H0 row
  decision        = continue_only_on_exact_value_theorem

y507_period156_value
  current_status = live_not_in_hand
  accepted_hook  = arithmetic finite F_p value theorem for Y_507 with
                   period-156 context and bridge to one legal support-156 row
  first_falsifier = Y_507 name, norm identity, or boundary-only statement
                    without finite value and legal-row bridge
  decision        = continue_only_on_exact_value_theorem

canonical_h0_divisor_additive_backup
  current_status = same_branch_free_backup_as_priority1
  accepted_hook  = scalar-fixed finite divisor/additive identity for canonical
                   H0 with Norm_156(Y_507) boundary
  first_falsifier = divisor class, H90 boundary, or up-to-scalar value without
                    additive/basepoint/telescoping normalization
  decision        = route_back_to_priority1_divisor_additive

theta2_or_theta2_inverse_payload
  current_status = support_confirmed_but_no_arithmetic_producer
  accepted_hook  = exact theta2/theta2-inverse divisor/additive payload with
                   period-156 bridge into the support-156 target
  first_falsifier = theta2 support certificate, Sprang D=2 support, or
                    branchless theta value without sparse payload and bridge
  decision        = continue_only_on_exact_theta2_payload

schertz_shin_scholl_framework_sources
  current_status = framework_not_current_hook
  accepted_hook  = source theorem specializing framework/value-unit language
                   to the exact p25 H0/Y507/theta2 hook
  first_falsifier = ray-class generation, Siegel-Ramachandra generator
                    language, generic norm relation, or direct Scholl D=2
                    import
  decision        = ask_narrow_source_question_only

ambient_or_shortcut_values
  current_status = repair_or_reject
  accepted_hook  = none
  first_falsifier = ambient 780 branch ambiguity, degree-6 value without F_p
                    descent, direct order-39 root, or sqrt(-39) scalar shortcut
  decision        = discard_without_new_branch_descent_data
```

## Counts

```text
evidence_markers_ok = 10/10
status_rows = 6
surviving_value_intake_families = 3
current_period156_value_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_period156_lookup_row_status_rows=1/1
```

## Verdict

The period-156 row remains live, but only through exact theorem hooks:

```text
1. canonical H0 finite value with Norm_156(Y_507) boundary and period-156
   branch/root/telescoping data;
2. Y_507 finite value with period-156 context and bridge to one legal row;
3. exact theta2/theta2-inverse divisor/additive payload with period-156 bridge.
```

Everything else is support, repair, or reject. In particular, Schertz/Shin/
Scholl-style field generation or value-unit framework language is useful only
if it specializes to one of these exact hooks.
