# P25 v2 Extended Unique-Power Intake

Updated: 2026-06-17

Marker: `p25_v2_extended_unique_power_intake_rows=1/1`

## Purpose

Record the small intake consequence of the `F_p^*` branch factorization. The
power-normalized theorem ask now accepts exact finite values of `R_m^e` for
`e in {3,5,13,39,75,169,507}`, because those powers uniquely recover `R_m` in
`F_p^*` when the source gives one exact legal row.

The branch audit shows three additional checked exponents are also uniquely
invertible:

```text
R_m^75
R_m^169
R_m^507
```

This is not a new source route and not a reason for broad literature search.
It is an intake addendum: if an expert or source theorem unexpectedly emits
one exact finite value in these shapes for one legal row, it should normalize
to the same source-stage row rather than be discarded.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_fpstar_branch_factorization_20260617.md`
- `evidence/p25_v2_power_normalized_theorem_intake_20260616.md`
- `evidence/p25_v2_normalizer_lookup_row_status_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_extended_unique_power_intake_gate.py
```

The gate returned `p25_v2_extended_unique_power_intake_rows=1/1`.

## Unique Power Rows

Already named live power normalizers:

```text
R_m^3   inverse exponent = 6666666666666666666666675
R_m^5   inverse exponent = 4000000000000000000000005
R_m^13  inverse exponent = 7692307692307692307692317
R_m^39  inverse exponent = 5897435897435897435897443
```

Extended exact-power intake rows:

```text
R_m^75   inverse exponent = 266666666666666666666667
R_m^169  inverse exponent = 5207100591715976331360953
R_m^507  inverse exponent = 5069033530571992110453655
```

Required clauses are unchanged:

```text
one exact oriented legal row R_m
arithmetic source theorem
exact finite F_p value for R_m^e
Norm_156(Y_507) boundary or accepted period-156 bridge
post-root source-snippet intake
```

## Non-Promotion Boundary

The original source-route-pinned power hooks were `3`, `5`, `13`, and `39`.
The full accepted exact row-power intake is now
`e in {3,5,13,39,75,169,507}`; the added `75/169/507` rows are intake-only
unless a theorem arrives already carrying the exact finite row-power value.

Do not open a broad search for arbitrary unique powers. Do not promote a
rowless `75`, `169`, or `507` power, a value up to scalar, or a boundary-only
powered divisor statement.

Repair powers remain:

```text
R_m^2    kernel = 2
R_m^4    kernel = 4
R_m^6    kernel = 2
R_m^11   kernel = 11
R_m^22   kernel = 22
R_m^44   kernel = 44
R_m^156  kernel = 4
R_m^780  kernel = 4
```

## Counts

```text
evidence_markers_ok = 4/4
standard_named_power_hooks = 4
extended_exact_power_hooks = 3
current_extended_power_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_extended_unique_power_intake_rows=1/1
```

## Verdict

The live theorem ask does not change: the best target is still a
scalar-fixed finite theorem for one legal support-156 row. This addendum only
prevents a future exact `R_m^75`, `R_m^169`, or `R_m^507` theorem from being
misclassified as a dead ambient-power near miss.
