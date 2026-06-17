# P25 v2 Additive Normalization Contract

Updated: 2026-06-16

## Purpose

Make the live phrase "finite divisor/additive theorem" precise enough for
source intake. A divisor identity plus Hilbert-90 boundary is not by itself an
exact finite value theorem: multiplication by any `F_p^*` constant preserves
both the divisor and the H90 boundary. The additive side must therefore fix
that scalar by a finite additive identity, normalized value, basepoint,
branch/root, or telescoping datum.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_additive_normalization_contract_gate.py
```

The gate returned `p25_v2_additive_normalization_contract_rows=1/1`.

## Routing Decisions

```text
normalized_divisor_additive_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

period156_value_with_telescoping
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

divisor_h90_no_additive_normalization
  decision = repair_additive_normalization_missing
  missing  = finite additive/value/basepoint/telescoping normalization fixing
             the F_p^* scalar

principal_divisor_or_divisor_class_only
  decision = repair_additive_normalization_missing
  missing  = H90 boundary plus scalar-fixing finite additive/value
             normalization

additive_relation_without_selected_row
  decision = repair_selected_row_missing
  missing  = legal support-156 row selection before applying the additive
             normalization

additive_relation_up_to_constant
  decision = repair_constant_normalization_missing
  missing  = specified scalar, finite normalization, or period-156 branch/root
             context

local_numeric_normalization_no_source
  decision = repair_arithmetic_source_theorem_missing
  missing  = challenge-legal arithmetic source theorem

normalized_after_basepoint_or_telescoping_fix
  decision = normalize_additive_value_then_apply_source_snippet_intake
  missing  = same theorem data after additive/value normalization
```

## Meaning

This does not narrow the positive row away. It sharpens it: the accepted
divisor/additive route remains live only when the additive or value data fixes
the exact finite value. A source answer that proves the right divisor and the
right `Norm_156(Y_507)` boundary but leaves the scalar unspecified is a repair
row, not a source-stage close.

The pass also separates additive normalization from row selection. A finite
additive relation for a dense norm, family average, or formal control is still
not enough unless it first selects one legal support-156 H0/conductor-39 row.

## Counts

```text
source_candidate_shapes = 2
normalize_rows = 1
repair_rows = 5
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = additive-normalization intake contract
continue_first_pass = yes
intake_rule = divisor/additive means legal row + H90 boundary + scalar-fixing
              finite additive/value normalization
discard_condition = answer remains a divisor class, boundary statement,
                    dense additive relation, or up-to-scalar value
```
