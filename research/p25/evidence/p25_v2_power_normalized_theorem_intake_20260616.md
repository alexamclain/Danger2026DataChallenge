# P25 v2 Power-Normalized Theorem Intake

Updated: 2026-06-16

Marker: `p25_v2_power_normalized_theorem_intake_rows=1/1`

## Purpose

Record a controlled widening of the first-pass theorem intake. A source theorem
does not have to emit the row value `R_m` literally if it emits an exact power
of `R_m` whose root is unique in `F_p^*`. For p25, this is true for exponents
`3`, `5`, `13`, `39`, `75`, `169`, and `507`, and false for the
square/fourth/eleventh/156th/780th near misses.

This is not a theorem hit. It is a router for future expert or source answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_power_normalized_theorem_intake_gate.py
```

The gate returned `p25_v2_power_normalized_theorem_intake_rows=1/1`.

## Accepted Power-Normalized Routes

For one exact oriented row `R_m`, `m in {1,2,4,8}`, a challenge-legal source
theorem for any of these exact finite values can be normalized back to `R_m`
before ordinary source-snippet intake:

```text
R_m^3   kernel on F_p^* = 1, inverse exponent = 6666666666666666666666675
R_m^5   kernel on F_p^* = 1, inverse exponent = 4000000000000000000000005
R_m^13  kernel on F_p^* = 1, inverse exponent = 7692307692307692307692317
R_m^39  kernel on F_p^* = 1, inverse exponent = 5897435897435897435897443
R_m^75  kernel on F_p^* = 1, inverse exponent = 266666666666666666666667
R_m^169 kernel on F_p^* = 1, inverse exponent = 5207100591715976331360953
R_m^507 kernel on F_p^* = 1, inverse exponent = 5069033530571992110453655
```

Thus an exact finite value for `R_m^e` recovers the row value by raising it to
the listed inverse exponent modulo `p - 1`.

Required clauses:

```text
one exact oriented row R_m
arithmetic source theorem
exact finite F_p value for R_m^e, e in {3,5,13,39,75,169,507}
Norm_156(Y_507) boundary or accepted period-156 bridge
post-root source-snippet intake
```

The downstream boundary is unchanged: after root normalization, the theorem
still needs DANGER3 framing, same-`j` extraction, `X_1(16)` payload, halving or
direct `x0`, and official `vpp.py`.

## Repair Routes

These exact powers do not determine `R_m` without extra branch, orientation, or
scalar data:

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

They remain repair rows unless the same source supplies the missing
branch/orientation/scalar selection. In particular, ambient-period-780 power
data still has the `mu_11` branch issue unless it descends to the support-156
row with explicit branch data.

## Near Misses

```text
exact_power_value_without_source
  decision = repair_arithmetic_source_theorem_missing

exact_power_value_without_row
  decision = repair_oriented_row_selection_missing

power_value_up_to_fp_scalar
  decision = repair_constant_normalization_missing

ambient_period780_power_only
  decision = repair_period156_branch_selection_missing
```

## Counts

```text
source_power_routes = 7
ambiguous_power_routes = 8
current_power_source_theorems = 0
current_submission_ready = 0
p25_v2_power_normalized_theorem_intake_rows=1/1
```

## Verdict

```text
positive_artifact = power-normalized source-theorem router
continue_first_pass = yes
new_expert_ask = an exact source theorem for R_m^3, R_m^5, R_m^13, R_m^39,
                 R_m^75, R_m^169, or R_m^507 is acceptable if it names one
                 legal row and the boundary
discard_condition = source answer gives only R_m^2, R_m^4, R_m^11, R_m^22,
                    R_m^44, R_m^156, R_m^780, an ambient-period value, a rowless
                    power, or a value only up to scalar
```
