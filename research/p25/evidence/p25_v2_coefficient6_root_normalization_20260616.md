# P25 v2 Coefficient-6 Root Normalization

Updated: 2026-06-16

## Purpose

Classify root statements around the current support-156 product rows.  All four
legal H0/conductor-39 rows use coefficients `+/-6`; a source theorem for a
lower-coefficient exact root row can be powered back to the current target, but
extracting a square or sixth root from coefficient-6 data without orientation
leaves a sign ambiguity.

This is a p25 arithmetic screen, not a source theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_coefficient6_root_normalization_gate.py
```

The gate returned `p25_v2_coefficient6_root_normalization_rows=1/1`.

## Arithmetic Contract

```text
gcd(2, p - 1) = 2
gcd(3, p - 1) = 1
gcd(6, p - 1) = 2
cube map on F_p^* = bijective
square root kernel size = 2
sixth root kernel size = 2
```

The four legal support-156 rows all have coefficient counts:

```text
(-6, 78), (6, 78)
```

The coefficient vector is divisible by `2`, `3`, and `6`, but the current
source-stage target remains the coefficient-6 row with boundary
`Norm_156(Y_507)`.

## Decisions

```text
current_coefficient6_row_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

coefficient2_exact_root_value
  decision = normalize_cube_power_then_apply_source_snippet_intake
  missing  = same theorem data after cubing to coefficient 6

coefficient3_exact_root_value
  decision = normalize_square_power_then_apply_source_snippet_intake
  missing  = same theorem data after squaring to coefficient 6

coefficient1_exact_root_value
  decision = normalize_sixth_power_then_apply_source_snippet_intake
  missing  = same theorem data after taking the sixth power to coefficient 6

infer_square_or_sixth_root_from_current_value
  decision = repair_coefficient6_root_orientation_missing
  missing  = explicit oriented root/sign data; square and sixth roots have a
             two-element kernel

scaled_boundary_as_current_target
  decision = reject_boundary_scale_mismatch
  falsifier = power back to the coefficient-6 row or prove the current boundary
              directly
```

## Counts

```text
source_candidate_shapes = 1
normalize_rows = 3
repair_rows = 1
reject_rows = 1
current_source_stage_closers = 0
```

## Verdict

An exact theorem for a coefficient-1, coefficient-2, or coefficient-3 root row
can be useful only if it gives the finite value/divisor data precisely enough
to power back to the coefficient-6 current row.  A claim that merely extracts a
square or sixth root from the current row is repair until it supplies oriented
root/sign data.  A scaled boundary is not the current `Norm_156(Y_507)`
boundary unless the source powers back to coefficient `6` or proves the
current boundary directly.
