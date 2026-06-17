# P25 v2 Power Output-Kind Router

Updated: 2026-06-16

## Purpose

Separate exact finite power-value snippets from powered divisor/Hilbert-90
boundary snippets.  The power/scalar inventory proves that some power maps on
`F_p^*` are bijective, but that only normalizes an exact finite value for
`R^e`.  It does not by itself turn divisor or boundary data for `R^e` into a
source-stage theorem for `R`.

This is an intake router, not a source theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_coefficient6_root_normalization_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_power_output_kind_router_gate.py
```

The gate returned `p25_v2_power_output_kind_router_rows=1/1`.

## Output-Kind Decisions

```text
exact_value_power3
  decision = normalize_unique_power_value_then_apply_source_snippet_intake
  use      = raise exact value to inverse exponent 6666666666666666666666675

exact_value_power5
  decision = normalize_unique_power_value_then_apply_source_snippet_intake
  use      = raise exact value to inverse exponent 4000000000000000000000005

exact_value_power13
  decision = normalize_unique_power_value_then_apply_source_snippet_intake
  use      = raise exact value to inverse exponent 7692307692307692307692317

exact_value_power39
  decision = normalize_unique_power_value_then_apply_source_snippet_intake
  use      = raise exact value to inverse exponent 5897435897435897435897443

exact_value_power11_with_branch
  decision = normalize_selected_power_value_then_apply_source_snippet_intake
  use      = branch/scalar data selects the root despite kernel size 11

exact_value_power11_no_branch
  decision = repair_power_value_branch_or_scalar_missing
  missing  = kernel of x -> x^11 on F_p^* has size 11

divisor_additive_power3_with_value_normalization
  decision = normalize_power_divisor_with_value_data_then_intake
  use      = finite normalization converts the powered theorem to an exact
             value before rooting

divisor_h90_power3_no_value
  decision = repair_power_divisor_value_normalization_missing
  missing  = divisor/H90 data for R^3 does not by itself fix the finite value
             of R

boundary_power3_only
  decision = reject_scaled_boundary_as_current_target
  falsifier = 3W is not the current W boundary unless the theorem powers back
              to the row

divisor_h90_power11_no_branch
  decision = repair_power_divisor_value_normalization_missing
  missing  = divisor/H90 data for R^11 does not by itself fix the finite value
             of R

scaled_boundary_power11_as_current
  decision = reject_scaled_boundary_as_current_target
  falsifier = 11W is not the current W boundary unless the theorem powers back
              to the row
```

## Counts

```text
unique_value_normalize_rows = 4
ambiguous_value_repair_rows = 1
power_boundary_repair_rows = 2
scaled_boundary_reject_rows = 2
current_source_stage_closers = 0
```

## Verdict

An exact finite value for `R^e` can be normalized when the power map is
bijective on `F_p^*`, and an ambiguous-kernel value can be normalized only if
the source supplies the missing branch/scalar selector.

A powered divisor/additive or H90-boundary statement is different.  It is
useful only if it also includes finite value/additive normalization that fixes
the powered value before rooting.  Boundary-only statements such as `3W` or
`11W` are not the current `W = Norm_156(Y_507)` boundary and remain rejected
as current-target statements unless they power back to the row.
