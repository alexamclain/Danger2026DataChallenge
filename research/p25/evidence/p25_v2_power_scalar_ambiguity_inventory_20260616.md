# P25 v2 Power / Scalar Ambiguity Inventory

Updated: 2026-06-16

## Purpose

Classify exact power-value and root-of-unity scalar statements for the current
support-156 H0/conductor-39 value.  This separates two easy-to-confuse facts:
some power maps on `F_p^*` are bijective for p25, while some scalar ambiguity
groups really do exist in `F_p` and must be fixed by branch, orientation, or
finite normalization data.

This is an intake screen, not a source theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_coefficient6_root_normalization_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_power_scalar_ambiguity_inventory_gate.py
```

The gate returned `p25_v2_power_scalar_ambiguity_inventory_rows=1/1`.

## Arithmetic Contract

```text
p mod 3   = 2
p mod 4   = 1
p mod 8   = 5
p mod 11  = 1
p mod 13  = 10
p mod 39  = 23
p mod 44  = 1
p mod 156 = 101
```

Power-map kernels on `F_p^*`:

```text
e = 2    kernel = 2    repair
e = 3    kernel = 1    unique inverse
e = 4    kernel = 4    repair
e = 5    kernel = 1    unique inverse
e = 6    kernel = 2    repair
e = 11   kernel = 11   repair
e = 13   kernel = 1    unique inverse
e = 22   kernel = 22   repair
e = 39   kernel = 1    unique inverse
e = 44   kernel = 44   repair
e = 156  kernel = 4    repair
e = 780  kernel = 4    repair
```

Root-of-unity scalar groups in `F_p`:

```text
mu_2   exists
mu_3   absent
mu_4   exists
mu_6   absent
mu_11  exists
mu_13  absent
mu_22  exists
mu_39  absent
mu_44  exists
mu_156 absent
```

## Decisions

```text
exact R^3, R^5, R^13, or R^39 value
  decision = normalize unique root, then apply source-snippet intake
  reason   = exponent is coprime to p - 1

exact R^2, R^4, R^6, R^11, R^22, R^44, R^156, or R^780 value
  decision = repair until branch/orientation/scalar data is supplied
  reason   = nontrivial kernel on F_p^*

mu_2, mu_4, mu_11, mu_22, or mu_44 scalar ambiguity
  decision = repair until scalar/branch/orientation is fixed
  reason   = those scalar groups are present in F_p

mu_3, mu_6, mu_13, mu_39, or mu_156 as F_p scalar ambiguity
  decision = reject as an F_p scalar statement
  reason   = those scalar groups are absent from F_p for p25
```

## Counts

```text
unique_power_rows = 4
ambiguous_power_rows = 8
fp_scalar_groups_present = 5
fp_scalar_groups_absent = 5
current_source_stage_closers = 0
```

## Verdict

An expert/source answer giving an exact cube, fifth, thirteenth, or
thirty-ninth power of the target value is not automatically a dead end: the
target value can be recovered uniquely in `F_p^*` and then routed through the
normal source-snippet intake.

Square, fourth, eleventh, twenty-second, forty-fourth, 156th, or 780th-power
statements remain repair rows unless the source also fixes the relevant
orientation, branch, or scalar.  In particular, `mu_11` and `mu_44` ambiguity
are real in `F_p`, while a primitive order-39 scalar is not in `F_p` even
though the 39th-power map on `F_p^*` is bijective.
