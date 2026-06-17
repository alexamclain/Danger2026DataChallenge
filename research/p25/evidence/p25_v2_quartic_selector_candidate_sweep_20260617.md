# P25 v2 Quartic Selector Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_quartic_selector_candidate_sweep_rows=1/1`

## Purpose

Audit prior quartic, projector, and Q-split artifacts after promoting the
exact `C4_1` character-language route. The question is whether any older
artifact already contains the accepted source-stage theorem:

```text
one legal W-boundary row
+ exact row-antisymmetric C4_1 phase
+ mixed tensor row sign and orientation/boundary convention
+ scalar-fixed finite value/divisor theorem
```

The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_c4_character_spectrum_20260616.md`
- `evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_power_projector_extraction_boundary_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_quartic_selector_candidate_sweep_gate.py
```

The gate returned `p25_v2_quartic_selector_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
exact_c4_phase_selector
  prior_shape = exact row-antisymmetric C4_1 phase table for the four legal rows
  decision    = live_selector_contract_not_prior_source_theorem
  missing     = scalar-fixed finite value/divisor theorem for the selected row

coarse_quartic_or_quadratic_data
  prior_shape = phase sign, magnitude, or quadratic character aggregate
  decision    = repair_quartic_edge_selection_missing
  missing     = coarse data leaves a two-edge or all-four ambiguity

row_sign_or_c4_projection_only
  prior_shape = row sign without C4 phase, C4 edge without row sign, or
                projection-only theorem
  decision    = repair_or_reject_mixed_tensor_missing
  missing     = legal conductor-39 row is row-antisymmetric tensor times one
                C4 edge

reciprocal_phase_presentations
  prior_shape = exact phase on a reciprocal row or phase collision with the
                opposite oriented edge
  decision    = normalize_only_with_orientation_and_minus_boundary
  falsifier   = reciprocal rows carry -Norm_156(Y_507), not the positive
                boundary

two_edge_or_doubled_edge_projectors
  prior_shape = row/column/diagonal pair data or pair plus difference reaching
                2*edge
  decision    = repair_oriented_square_root_missing
  missing     = p25 has a real sign ambiguity when recovering one edge from a
                doubled edge

four_edge_projector_components
  prior_shape = constant, row, column, checkerboard components reconstructing
                4*edge
  decision    = repair_mu4_root_or_scalar_missing
  missing     = p25 has a four-element fourth-power kernel for projector
                division by 4

q_split_quartic_support
  prior_shape = Q diagonal pure quadratic plus pure quartic split
  decision    = support_normalization_not_prior_closer
  missing     = diagonal plus split reaches 2*edge and still needs oriented
                root/sign or direct theorem

selected_root_projector_value
  prior_shape = future exact R4/projector value with selected fourth root
  decision    = normalize_then_apply_source_snippet_intake
  missing     = no current source theorem supplies the selected root and
                finite row theorem

source_family_prior_scan
  prior_shape = inspected Koo-Shin/Sprang/Kubert-Lang/Schertz source families
  decision    = no_prior_exact_quartic_finite_theorem_found
  missing     = source-family gap matrix still has
                scalar_fixed_finite_theorems=0 and first_pass_closers=0
```

## Counts

```text
evidence_markers_ok = 10/10
newly_promoted_prior_candidates = 0
surviving_quartic_intake_families = 3
q_split_normalization_confirmed = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_quartic_selector_candidate_sweep_rows=1/1
```

The three surviving intake families are normalization variants of the same
one-edge target, not three independent theorem targets:

```text
direct exact C4_1 character-language theorem
projector/fourth-power theorem with selected fourth root
Q diagonal + correct pure quartic split + oriented root/sign
```

## Verdict

```text
positive_artifact = quartic/projector prior-art sweep
continue_first_pass = yes
new_candidate_from_prior_art = no
surviving_quartic_ask = exact row-antisymmetric C4_1 phase plus mixed tensor
                        row sign, orientation/boundary convention, arithmetic
                        source theorem, and scalar-fixed finite value/divisor
                        theorem for one legal row
discard_condition = answer only supplies quartic sign, magnitude, quadratic
                    aggregate, row sign, projector components, reciprocal
                    phase without boundary sign, Q split without oriented
                    root, or source-family vocabulary without the exact finite
                    theorem
```

This sweep closes the most plausible "maybe we already had it" quartic gap:
the existing artifacts define the selector boundary well, but none contains the
missing finite arithmetic theorem.
