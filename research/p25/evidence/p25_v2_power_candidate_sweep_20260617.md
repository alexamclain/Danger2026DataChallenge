# P25 v2 Power Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_power_candidate_sweep_rows=1/1`

## Purpose

Audit prior power-shaped artifacts after promoting the power-normalized intake.
The question is whether any older artifact already contains an exact finite
`F_p` value theorem for `R_m^e` with
`e in {3,5,13,39,75,169,507}` on one legal row. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_power_projector_extraction_boundary_20260616.md`
- `evidence/p25_v2_coefficient6_root_normalization_20260616.md`
- `evidence/p25_v2_primitive_character_power_recheck_20260617.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `archive/notes/subsqrt_moonshot_laneB_square_axis_raw_shift_lift.md`
- `archive/notes/subsqrt_moonshot_laneB_square_axis_bridge_factor_kummer.md`
- `archive/notes/subsqrt_moonshot_laneB_square_axis_kernel_character_trace.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_power_candidate_sweep_gate.py
```

The gate returned `p25_v2_power_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
router_exact_power_templates
  prior_shape = exact_value_power3/exact_value_power39 and
                exact_R3_value/exact_R39_value rows
  decision    = intake_templates_not_source_discoveries
  missing     = the router pages classify hypothetical snippets and record
                current source theorem count zero

coefficient_root_shapes
  prior_shape = coefficient-1/2/3 exact root rows powering to coefficient 6
  decision    = conditional_power_back_shape_not_prior_candidate
  missing     = the page states it is an arithmetic screen, not a source theorem

primitive_character_power_relation
  prior_shape = V_bal=U_chi^3 and W=U_chi^6
  decision    = support_identity_not_exact_Fp_row_power_value
  missing     = primitive-character recheck classifies it as
                exponent-word/source-unit support

lane_b_d_cubed_relation
  prior_shape = Lane B D^3=Y after quotienting or trace-down
  decision    = quotient_kernel_monodromy_not_legal_row_value_theorem
  falsifier   = raw D^3 and Y differ by one B=25 trace-kernel layer and
                nontrivial kernel characters trace to zero

source_family_prior_scan
  prior_shape = inspected Koo-Shin/Sprang/Kubert-Lang/Schertz source families
  decision    = no_prior_exact_power_source_theorem_found
  missing     = source-family gap matrix still has scalar_fixed_finite_theorems=0
                and first_pass_closers=0

surviving_future_power_intake
  prior_shape = future exact F_p theorem for R_m^e with
                e in {3,5,13,39,75,169,507}
  decision    = keep_as_live_expert_ask
  missing     = must name one legal row or row-labeled theorem and the
                Norm_156(Y_507) boundary/period bridge
```

## Counts

```text
evidence_markers_ok = 6/6
newly_promoted_prior_candidates = 0
surviving_future_power_intakes = 1
lane_b_kernel_monodromy_confirmed = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_power_candidate_sweep_rows=1/1
```

## Verdict

```text
positive_artifact = power-shaped prior-art sweep
continue_first_pass = yes
new_candidate_from_prior_art = no
surviving_power_ask = exact finite F_p theorem for R_m^e with
                      e in {3,5,13,39,75,169,507} on one legal row, with
                      source theorem provenance and the Norm_156(Y_507)
                      boundary/period bridge
discard_condition = answer only restates intake templates, lower-coefficient
                    arithmetic screens, U_chi/V_bal exponent relations,
                    Lane B quotient D^3=Y, kernel phases, or a source-family
                    vocabulary match without the exact finite theorem
```
