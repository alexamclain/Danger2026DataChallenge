# Actual-CM Value-Identity Boundary

Date: 2026-06-07

## Point

The new packet-facing theorem asks for three value-side identities after
`Tr_{B/C}`:

```text
1. C-row sums are independent of the right coordinate;
2. the C-zero fiber vanishes;
3. f(r,c)+f(-r,-c) is constant for all c != 0.
```

This boundary tests nearby actual-CM rows to see whether those identities are
generic.  They are not.

## Result

On the raw projector row:

```text
D=-5000, q=3851, h=30, right_degree=2, c_degree=5

row_sum_independent_origins=0/30
c_zero_fiber_origins=0/30
inversion_constant_origins=0/30
structural_zero_plus_inversion_origins=0/30
all_three_value_identities_origins=0/30
```

On the pinned right-combo row:

```text
D=-13319, q=13463, h=140, right_degree=2, c_degree=5
```

the right-combo resolvent and raw weighted coefficients both have:

```text
row_sum_independent_origins=0/140
c_zero_fiber_origins=0/140
inversion_constant_origins=0/140
all_three_value_identities_origins=0/140
```

The selected-defect coefficients have the tautological C-zero property:

```text
c_zero_fiber_origins=140/140
```

but still fail:

```text
row_sum_independent_origins=0/140
inversion_constant_origins=0/140
structural_zero_plus_inversion_origins=0/140
all_three_value_identities_origins=0/140
```

## Consequence

The split proof target is not generic actual-CM symmetry.

Selected-section subtraction can force:

```text
f(r,0)=0
```

but it does not force:

```text
f(r,c)+f(-r,-c)=constant
```

or the row-sum/global-balance identities.  So the p24 proof still needs the
specific selected weighted trace-GCD packet, an explicit admissible-carry
decomposition, or a genuine CM/Lang product formula.

## Check

This is a slower PARI-backed diagnostic, not a default cheap gate:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.py
```

Observed:

```text
actual_cm_projector_fails_value_identities_generically=1
actual_cm_right_combo_fails_value_identities_generically=1
actual_cm_weighted_coefficients_fail_value_identities_generically=1
actual_cm_selected_defects_fail_value_identities_generically=1
selected_defects_only_force_c_zero_fiber_not_inversion_or_row_balance=1
```
