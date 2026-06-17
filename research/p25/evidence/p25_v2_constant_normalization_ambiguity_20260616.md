# P25 v2 Constant Normalization Ambiguity

Updated: 2026-06-16

## Purpose

Record the repair rule for source snippets that determine a target value only
up to multiplication by a nonzero `F_p` constant. Such constants have zero
divisor and zero Hilbert-90 boundary, so divisor plus boundary data alone does
not select the exact finite value.

This is the scalar analogue of the row-square sign ambiguity: `R` and `cR`
look identical to divisor/H90 data for every `c in F_p^*`, unless the theorem
also fixes an additive/value normalization, period-156 branch data, or a
DANGER3-ready finite framing.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_constant_normalization_ambiguity_gate.py
```

The gate returned `p25_v2_constant_normalization_ambiguity_rows=1/1`.

## Arithmetic Invariants

```text
F_p^* constants available = p - 1
constant divisor = zero
constant Hilbert-90 boundary = zero
c / Frob_p(c) = 1 for c in F_p^*
divisor(cR) = divisor(R)
boundary(cR) = boundary(R)
```

The key distinction is not computational. It is logical: a theorem stated only
up to an unspecified `F_p^*` scalar is not an exact finite p25 value theorem.

## Routing Decisions

```text
divisor_additive_or_normalized_value_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

period156_value_with_branch_root_context
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

divisor_only_with_h90_boundary
  decision = repair_constant_normalization_missing
  missing  = additive/value normalization or finite framing fixing the F_p^*
             scalar

value_up_to_fp_scalar
  decision = repair_constant_normalization_missing
  missing  = specified scalar, branch/root/telescoping context, or normalized
             value

normalized_value_after_constant_fix
  decision = normalize_value_then_apply_source_snippet_intake
  missing  = same theorem data after value normalization
```

## Meaning

The accepted "divisor/additive" source row is unchanged: it remains a source
candidate when the additive/value side fixes the finite identity. What this
screen rejects is the weaker shape "same divisor and Hilbert-90 boundary, but
value only up to scalar."

That weaker shape can still be useful if a source also provides the missing
normalization. Once the scalar is fixed, the answer should re-enter the normal
source-snippet intake.

## Counts

```text
source_candidate_shapes = 2
normalize_rows = 1
repair_rows = 2
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = scalar-normalization ambiguity is now explicit
continue_first_pass = yes
intake_rule = divisor/H90 data without finite additive or value normalization
              is repair, not source-stage close
discard_condition = source answer remains only up to unspecified F_p^* scalar
```
