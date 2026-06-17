# P25 v2 Normalizer Lookup-Row Status

Updated: 2026-06-17

Marker: `p25_v2_normalizer_lookup_row_status_rows=1/1`

## Purpose

Turn the row/quartic/power normalizer row from the priority-1 source lookup
capsule into a compact source/expert checklist. This artifact does not re-audit
the row, quartic, projector, reciprocal, or power surfaces. It records when
those surfaces genuinely normalize to one scalar-fixed legal support-156 row,
and when they remain support, repair, or reject rows.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_route_priority_falsifier_matrix_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_row_orientation_candidate_sweep_20260617.md`
- `evidence/p25_v2_orbit_tuple_theorem_router_20260616.md`
- `evidence/p25_v2_quartic_selector_candidate_sweep_20260617.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_power_candidate_sweep_20260617.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_normalizer_lookup_row_status_gate.py
```

The gate returned `p25_v2_normalizer_lookup_row_status_rows=1/1`.

## Status Rows

```text
single_or_row_labeled_theorem
  current_status = live_not_in_hand
  accepted_hook  = one normalized legal row, a doubling-equivalent row, or a
                   row-labeled orbit theorem containing one legal row, plus
                   scalar-fixed finite theorem data
  first_falsifier = unordered orbit values, symmetric all-four product/norm,
                    diagonal pair, row quotient, outside-orbit tuple, or
                    all-four over-demand
  decision        = normalize_to_one_row_then_apply_source_snippet_intake

reciprocal_orientation_normalizer
  current_status = normalizer_live_not_in_hand
  accepted_hook  = reciprocal row with explicit -Norm_156(Y_507) boundary plus
                   the same scalar-fixed theorem data
  first_falsifier = outside-doubling row with unspecified orientation,
                    reciprocal row with positive boundary, or phase collision
                    without boundary sign
  decision        = normalize_reciprocal_then_apply_source_snippet_intake

quartic_character_normalizer
  current_status = selector_live_finite_theorem_missing
  accepted_hook  = exact row-antisymmetric C4_1 phase, mixed tensor row sign,
                   orientation/boundary convention, arithmetic source theorem,
                   and scalar-fixed finite theorem
  first_falsifier = quartic sign, magnitude, quadratic aggregate, row sign
                    only, C4 projection only, reciprocal phase without
                    boundary sign, or Q split without root
  decision        = continue_only_with_exact_quartic_finite_theorem

power_value_normalizer
  current_status = power_value_live_not_in_hand
  accepted_hook  = exact finite F_p theorem for R_m^e with
                   e in {3,5,13,39,75,169,507} on one legal row, with inverse recovery and
                   Norm_156(Y_507) boundary or accepted period-156 bridge
  first_falsifier = power value without row selector, boundary bridge, source
                    theorem, or scalar; ambiguous kernels; powered
                    boundary-only data; Lane B D^3=Y quotient relation
  decision        = normalize_unique_power_value_then_apply_source_snippet_intake

projector_or_square_root_normalizer
  current_status = repair_until_selected_root_and_theorem
  accepted_hook  = selected square/fourth root or projector value that
                   explicitly recovers one oriented row and then supplies the
                   finite theorem data
  first_falsifier = two-edge, doubled-edge, four-edge projector components,
                    row-square, Q split, or fourth-power data without selected
                    root/scalar
  decision        = do_not_promote_without_selected_root_and_source_theorem

source_family_prior_scan
  current_status = prior_art_negative
  accepted_hook  = none in the inspected Koo-Shin/Sprang/Kubert-Lang/Schertz
                   family summaries
  first_falsifier = source-family vocabulary, character language, projector
                    language, or power templates without the exact finite
                    theorem
  decision        = ask_narrow_normalizer_question_only
```

## Counts

```text
evidence_markers_ok = 12/12
status_rows = 6
surviving_row_intake_families = 4
surviving_quartic_intake_families = 3
surviving_future_power_intakes = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_normalizer_lookup_row_status_rows=1/1
```

## Verdict

Row, quartic, reciprocal, projector, and power language should be treated as
normalization surfaces, not independent theorem fronts. They matter only when
they end at the same object:

```text
one scalar-fixed legal support-156 row
+ Norm_156(Y_507) boundary or accepted period-156 bridge
+ arithmetic source theorem
+ finite value/divisor/additive theorem, or exact uniquely rootable power value
```

The live normalizer asks are:

```text
1. row-labeled one-row or orbit theorem containing one legal row;
2. reciprocal row with explicit -Norm_156 boundary and theorem data;
3. exact C4_1 character theorem with mixed row sign and finite theorem;
4. exact R_m^e finite theorem with inverse recovery for
   e in {3,5,13,39,75,169,507};
5. selected square/fourth-root/projector theorem only if the root and source
   theorem are both supplied.
```

Everything else is repair or reject. In particular, selector-only quartic data,
unordered orbit values, all-four aggregates, Q split without oriented root,
projector components without a selected root, powered boundary-only statements,
and Lane B quotient power relations are not source-stage closers.
