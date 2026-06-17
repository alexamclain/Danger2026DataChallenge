# P25 v2 Quartic Reciprocal Orientation

Updated: 2026-06-16

## Purpose

Combine the row-orientation normalizer with the exact quartic selector. The
exact row-antisymmetric `C4_1` phase selects an oriented edge only when the
orientation and Hilbert-90 boundary sign are also known. A reciprocal row
negates the exponent vector, so it negates both the boundary and the quartic
phase. That negated phase is also the phase of the opposite oriented edge.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_c4_character_spectrum_20260616.md`
- `evidence/p25_v2_row_sign_c4_tensor_spectrum_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_quartic_reciprocal_orientation_gate.py
```

The gate returned `p25_v2_quartic_reciprocal_orientation_rows=1/1`.

## Reciprocal Phase Table

```text
oriented m=1  phase =  2+2i
  reciprocal phase = -2-2i = oriented m=4 phase
  reciprocal boundary = -Norm_156(Y_507)

oriented m=2  phase = -2+2i
  reciprocal phase =  2-2i = oriented m=8 phase
  reciprocal boundary = -Norm_156(Y_507)

oriented m=4  phase = -2-2i
  reciprocal phase =  2+2i = oriented m=1 phase
  reciprocal boundary = -Norm_156(Y_507)

oriented m=8  phase =  2-2i
  reciprocal phase = -2+2i = oriented m=2 phase
  reciprocal boundary = -Norm_156(Y_507)
```

## Routing Rows

```text
oriented_exact_phase_plus_boundary
  decision = source_stage_candidate_if_finite_theorem_present
  missing  = scalar-fixed finite value/divisor theorem plus extraction

reciprocal_exact_phase_minus_boundary
  decision = normalize_reciprocal_then_apply_source_snippet_intake
  missing  = same theorem data after orientation normalization

exact_phase_boundary_sign_unspecified
  decision = repair_reciprocal_orientation_or_boundary_sign_missing
  missing  = explicit oriented row or reciprocal row with -Norm_156 boundary

reciprocal_phase_plus_boundary
  decision = reject_orientation_boundary_mismatch
  falsifier = reciprocal product carries -Norm_156 boundary

phase_collision_as_different_edge
  decision = repair_phase_orientation_collision
  missing  = boundary sign/orientation data distinguishing reciprocal row
             from opposite edge
```

## Counts

```text
evidence_markers_ok = 6/6
reciprocal_phase_collisions = 4
normalize_rows = 1
repair_rows = 2
reject_rows = 1
current_source_closers = 0
p25_v2_quartic_reciprocal_orientation_rows=1/1
```

## Verdict

```text
positive_artifact = reciprocal-orientation screen for quartic character data
continue_first_pass = yes
intake_rule = an exact C4_1 phase must carry oriented row data or the correct
              boundary sign; reciprocal rows normalize only with -Norm_156
discard_condition = reciprocal phase asserted with the positive boundary, or
                    phase collision used as a different edge without
                    orientation data
```
