# P25 v2 Norm-Only Descent Ambiguity

Updated: 2026-06-16

## Purpose

Record the repair rule for source snippets that identify only the dense period
norm `Norm_156(Y_507)` or its value. The p25 first-pass target is not the dense
norm by itself; it is one legal support-156 Hilbert-90 preimage/product row
whose `(1 - Frob_p)` boundary equals that norm, plus a finite value/divisor
theorem for the selected row.

This matters because boundary data alone is not selective. The legal rows have
the desired boundary, but formal one-coset controls can also share that
boundary while failing the mixed-axis tests.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `archive/gates/p25_ksy_y_yang_y507_period_norm_character_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_gate.py`
- `archive/gates/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_gate.py`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_norm_only_descent_ambiguity_gate.py
```

The gate returned `p25_v2_norm_only_descent_ambiguity_rows=1/1`.

## Arithmetic Invariants

```text
Norm_156(Y_507) support = 312
Norm_156(Y_507) coefficient counts = (-6, 156), (6, 156)
legal Hilbert-90 preimage support = 156
legal preimage count = 4
legal product shape = 78 positive / 78 negative Yang-fiber factors
formal one-coset controls with same boundary = 2
formal one-coset controls fail mixed-axis pushforwards = yes
period norm / sparse lift / product normal form direct closer = no
```

## Routing Decisions

```text
legal_support156_value_divisor_theorem
  decision = source_stage_candidate_if_theorem_present
  missing  = downstream DANGER3 framing and extraction

period_norm_identity_only
  decision = repair_norm_only_h90_descent_missing
  missing  = legal support-156 Hilbert-90 descent selecting one row

dense_unit_character_norm_value
  decision = repair_norm_only_row_selection_missing
  missing  = selected legal 78-over-78 product row and finite theorem for that
             row

norm_with_formal_one_coset_descent
  decision = reject_boundary_control_not_source_object
  missing  = proper-axis pushforward failure; not the mixed conductor-39
             source object

norm_plus_explicit_legal_h90_descent
  decision = normalize_descent_then_apply_source_snippet_intake
  missing  = same theorem data after legal H90 descent normalization
```

## Meaning

A period-norm theorem is useful context, but it is not the front-door theorem
unless it descends to one of the four legal support-156 rows and then supplies
the finite value/divisor theorem for that row. This is stricter than merely
checking the boundary, because non-source formal controls can have the same
boundary.

## Counts

```text
source_candidate_shapes = 1
normalize_rows = 1
repair_rows = 2
reject_rows = 1
current_source_stage_closers = 0
```

## Verdict

```text
positive_artifact = norm-only/descent ambiguity is now explicit
continue_first_pass = yes
intake_rule = dense norm or period-norm value claims are repair rows unless
              they include legal support-156 H90 descent and then the finite
              theorem for that selected row
discard_condition = source answer remains only a norm identity/value or
                    descends through a formal one-coset boundary control
```
