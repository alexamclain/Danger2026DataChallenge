# P25 v2 Row/Orientation Candidate Sweep

Updated: 2026-06-17

Marker: `p25_v2_row_orientation_candidate_sweep_rows=1/1`

## Purpose

Audit row normalization, reciprocal orientation, row-labeled orbit, and
orientationless aggregate artifacts as one intake surface. The question is
whether any row/orbit/orientation artifact already supplies a source-stage
closer. The answer remains no.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_orbit_tuple_theorem_router_20260616.md`
- `evidence/p25_v2_k22_automorphism_quotient_falsifier_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_row_orientation_candidate_sweep_gate.py
```

The gate returned `p25_v2_row_orientation_candidate_sweep_rows=1/1`.

## Sweep Rows

```text
single_normalized_legal_row
  prior_shape = one row m in {1,2,4,8} with row label/hash/edge
  decision    = source_stage_candidate_if_scalar_fixed_theorem_present
  missing     = finite value/divisor or period-156 value theorem

stabilizer_or_doubling_equivalent_row
  prior_shape = unit in doubling subgroup or stabilizer presentation
  decision    = normalize_to_legal_row_then_apply_source_snippet_intake
  missing     = same theorem data after normalization

outside_doubling_orientation_unspecified
  prior_shape = outside-doubling unit row with no reciprocal orientation or
                boundary sign
  decision    = repair_reciprocal_orientation_or_boundary_sign_missing
  missing     = rewrite to oriented row or reciprocal with -Norm_156 boundary

reciprocal_row_with_minus_boundary
  prior_shape = outside-doubling reciprocal row with -Norm_156(Y_507) boundary
  decision    = normalize_reciprocal_then_apply_source_snippet_intake
  missing     = same theorem data after reciprocal normalization

reciprocal_row_with_plus_boundary
  prior_shape = reciprocal row asserted with positive Norm_156(Y_507) boundary
  decision    = reject_orientation_boundary_mismatch
  falsifier   = reciprocal product carries the opposite Hilbert-90 boundary

row_labeled_four_edge_tuple
  prior_shape = four row-labeled divisor/additive or period-156 value identities
  decision    = choose_any_labeled_row_then_route_to_extraction
  missing     = not present as a current source theorem; downstream extraction
                still needed

parametric_doubling_orbit_theorem
  prior_shape = uniform theorem for m in {1,2,4,8} with row labels
  decision    = normalize_m_then_apply_positive_clause_matcher
  missing     = not present as a current source theorem

unordered_four_values
  prior_shape = set of four values without row labels
  decision    = repair_row_labeling_missing
  missing     = assignment to one exact oriented edge

symmetric_all_four_product_or_norm
  prior_shape = all-four product, norm, trace, or quotient-invariant aggregate
  decision    = repair_oriented_edge_selection_missing
  missing     = selected root/scalar/row label or direct one-edge theorem

diagonal_pair_or_row_quotient_tuple
  prior_shape = diagonal pair, pair tuple, row quotient, or boundary-zero tuple
  decision    = repair_square_root_pair_selector_or_one_edge_value_missing
  missing     = oriented root/selector or direct one-edge finite theorem

outside_doubling_orbit_tuple
  prior_shape = tuple or theorem on units outside the current doubling orbit
                target
  decision    = reject_not_current_legal_four_row_target
  falsifier   = row orbit normalization fixes the legal representatives

all_four_rows_required
  prior_shape = claim that a source-stage theorem must prove all four rows
  decision    = repair_overdemand_one_legal_row_is_enough
  missing     = one normalized legal row is sufficient for the first-pass ask
```

## Counts

```text
evidence_markers_ok = 8/8
newly_promoted_prior_candidates = 0
surviving_row_intake_families = 4
legal_orbit_complete = 1
reciprocal_split_complete = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_row_orientation_candidate_sweep_rows=1/1
```

The four surviving row/orientation intake families are:

```text
single normalized legal row with theorem data
stabilizer/doubling-equivalent row normalized to one legal row
reciprocal row with explicit -Norm_156 boundary normalized to one legal row
row-labeled four-row or parametric orbit theorem containing one legal row
```

## Verdict

```text
positive_artifact = row/orientation prior-art candidate sweep
continue_first_pass = yes, but only after row/orientation normalization
new_candidate_from_prior_art = no
surviving_row_ask = normalized legal row, normalized reciprocal with opposite
                    boundary, or row-labeled orbit theorem, plus scalar-fixed
                    finite theorem data
discard_condition = answer only supplies outside-doubling row without
                    orientation, reciprocal row with positive boundary,
                    unordered orbit values, all-four aggregate, diagonal/pair
                    aggregate, boundary-zero quotient, outside-orbit tuple, or
                    a demand for all four rows
```

This closes the row/orientation "maybe already enough" family. Row and orbit
normalization remain mandatory intake steps, but none of the existing
normalization artifacts is the missing finite value/divisor theorem.
