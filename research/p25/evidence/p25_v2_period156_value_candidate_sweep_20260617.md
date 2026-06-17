# P25 v2 Period-156 Value Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_period156_value_candidate_sweep_rows=1/1`

## Purpose

Audit prior period-156, H0/Y507, Schertz/Shin/Scholl, theta2, Sprang, norm,
and degree-6 value artifacts after the value-side route became a front-door
theorem shape. The question is whether any older value-side artifact already
supplies the accepted arithmetic source theorem. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `sources/schertz-scholl.md`
- `sources/sprang.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_period156_value_source_hook_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md`
- `evidence/p25_v2_norm_only_descent_ambiguity_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_source_action_registry_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_period156_value_candidate_sweep_gate.py
```

The gate returned `p25_v2_period156_value_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
canonical_h0_period156_value
  prior_shape = canonical H0 value with Norm_156(Y_507) boundary and
                period-156 branch context
  decision    = live_value_route_not_prior_theorem
  missing     = no current arithmetic source theorem emits this finite value

y507_period156_value
  prior_shape = Y_507 value theorem with period-156 context
  decision    = live_value_route_not_prior_theorem
  missing     = no current arithmetic source theorem emits the p25 Y_507 value

canonical_h0_divisor_additive
  prior_shape = canonical H0 divisor/additive identity with boundary
  decision    = live_branch_free_route_not_prior_theorem
  missing     = scalar-fixed finite divisor/additive identity still missing

ambient780_or_mu11_value
  prior_shape = ambient-period-780 value, eleventh power, or mu_11 quotient
  decision    = repair_period156_branch_selection_missing
  missing     = ambient route leaves 11 F_p branches and does not select one
                value

degree6_value_without_fp_descent
  prior_shape = degree-6 primitive-root expression, value orbit, or norm
                without selected F_p row
  decision    = repair_fp_descent_and_row_selection_missing
  missing     = descent to F_p plus selected legal support-156 row

norm_only_or_boundary_only
  prior_shape = Norm_156(Y_507), dense period norm value, or H90 boundary only
  decision    = repair_legal_h90_descent_and_finite_theorem_missing
  missing     = boundary/norm data does not choose one legal preimage row

schertz_shin_scholl_framework
  prior_shape = ray-class generation, Siegel-Ramachandra generator,
                Kato-Siegel norm vocabulary
  decision    = support_source_not_period156_hook
  missing     = exact p25 support-156 value/divisor theorem or theta2 payload

theta2_factor_certificate
  prior_shape = period-156 theta2/theta2-inverse finite support contract
  decision    = support_payload_not_arithmetic_producer
  missing     = challenge-legal arithmetic identity emitting exact theta2
                divisor/additive data

sprang_d2_theta_support
  prior_shape = D=2 Poincare/Kronecker/theta source machinery
  decision    = support_source_not_theta2_closer
  missing     = p25 theta2 payload, bridge, and branch/telescoping data

direct_order39_or_sqrt_minus39_shortcuts
  prior_shape = direct F_p order-39 root or sqrt(-39) scalar shortcut
  decision    = reject_arithmetic_shortcut
  falsifier   = ord_39(p)=6 and sqrt(-39) is not in F_p
```

## Counts

```text
evidence_markers_ok = 11/11
newly_promoted_prior_candidates = 0
surviving_value_intake_families = 3
theta2_support_confirmed = 1
current_period156_value_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_period156_value_candidate_sweep_rows=1/1
```

The three surviving value-side intake families are:

```text
canonical H0 or Y_507 period-156 value theorem with branch/root/telescoping
canonical H0 divisor/additive identity with the Norm_156(Y_507) boundary
exact theta2/theta2-inverse divisor/additive payload with period-156 bridge
```

## Verdict

```text
positive_artifact = period-156 value-side prior-art sweep
continue_value_side = yes, but only through exact theorem hooks
new_candidate_from_prior_art = no
surviving_value_ask = arithmetic source theorem for canonical H0/Y507
                      period-156 value, scalar-fixed H0 divisor/additive
                      identity, or exact theta2/theta2-inverse payload with
                      period-156 bridge and branch/additive normalization
discard_condition = answer only supplies source generation vocabulary,
                    ambient period-780 value, mu_11 quotient, degree-6 value
                    without F_p descent, dense norm identity, H90 boundary
                    only, theta2 support certificate, Sprang D=2 vocabulary,
                    direct F_p order-39 root, or sqrt(-39) shortcut
```

This closes the value-side "maybe already enough" family. The period-156 route
is still one of the real theorem doors, but no current value-side artifact is
the missing arithmetic theorem.
