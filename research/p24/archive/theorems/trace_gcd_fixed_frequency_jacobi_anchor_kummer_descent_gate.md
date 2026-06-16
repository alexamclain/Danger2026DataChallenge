# Jacobi Anchor Kummer Descent Gate

Date: 2026-06-07

## Point

The residual-factor search showed a negative result:

```text
h_triv
and
h_nontriv
```

do not split as separate base-field multiplicative factors in the small
Jacobi value fields.  The obstruction is exactly the missing `c`-th root of
the selected anchor scalar.

This gate records the positive replacement.  Work in an auxiliary Kummer
extension with:

```text
beta^c = s
```

where `s=(q-2)/x` and the scalar search left only `x=+/-1`.

For the `R_c^e` family, use:

```text
row-sum slice exponent:       (c-1)e       at every C coordinate
R_c residual exponent:       -(c-1)e       at k=0
R_c residual exponent:           e         at k != 0
```

Their product is:

```text
k=0:     beta^0    = 1
k != 0: beta^(ce) = s^e
```

So the product descends to the base field.  The selected correction requires:

```text
s^e = s,
```

hence the formal exponent is:

```text
e = 1.
```

## Result

For the exact finite Jacobi models `c=5,11,13`, both sign branches satisfy:

```text
kummer_selected_descent_rows=6/6
kummer_Rc_exponent_unique_e_one_rows=6/6
kummer_row_sum_and_residual_nonbase_rows=6/6
kummer_no_base_field_split_rows=6/6
```

## Consequence

For p24, the live theorem should be stated as:

```text
construct an auxiliary Kummer/norm/divisor realization of
R_179 = Phi_179(X)/(X-1)^178,
with exponent e=1 and a final +/- sign normalization,
whose product descends p-integrally to the selected anchor correction.
```

This is narrower than "find an anchor unit" and avoids the tested dead end of
separate base-field slice factors.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate.py
```

Expected markers:

```text
kummer_selected_descent_rows=6/6
kummer_Rc_exponent_unique_e_one_rows=6/6
kummer_row_sum_and_residual_nonbase_rows=6/6
kummer_no_base_field_split_rows=6/6
p24_kummer_auxiliary_degree=179
p24_R179_exponent_for_selected_correction=1
selected_correction_forces_R_c_exponent_e_equals_1=1
p24_target_is_auxiliary_kummer_or_norm_descent_for_R_179_with_sign=1
```
