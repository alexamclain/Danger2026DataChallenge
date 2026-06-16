# Jacobi Anchor Residual Factor Search

Date: 2026-06-07

## Point

The reduced-anchor split is additive/divisorial:

```text
h = h_triv + h_nontriv.
```

Multiplicatively, a separate realization of the two pieces would require:

```text
row-sum slice:       C on all C positions;
cyclotomic residual: B^{-(c-1)} at k=0 and B at k != 0.
```

The product is:

```text
k=0:     C * B^{-(c-1)}
k != 0: C * B.
```

For the selected-defect anchor correction, this product should be:

```text
k=0:     1
k != 0: s
```

where `s=(q-2)/x` and the scalar search found `x=+/-1`.

Eliminating `C` gives the exact obstruction:

```text
B^c = s.
```

So a separate base-field factorization exists only if the selected correction
scalar is a `c`-th power in the Jacobi value field.

## Result

In the exact finite Jacobi models for `c=5,11,13`, neither valid sign branch
has such a `c`-th root:

```text
plus_one_branch_has_no_base_field_residual_split_rows=3/3
minus_one_branch_has_no_base_field_residual_split_rows=3/3
no_valid_sign_has_base_field_residual_split_rows=3/3
```

## Consequence

The `R_c` residual is still the right principal divisor shape, but the proof
should not try to realize:

```text
h_triv
and
h_nontriv
```

as separate value-field multiplicative factors in the base field.

For p24, this sharpens the live theorem:

```text
realize R_179 divisorially, by an integral norm, or in an auxiliary extension
with the final product/norm descending p-integrally.
```

Trying to find independent base-field slice factors is now a tested dead end.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_anchor_residual_factor_search.py
```

Expected markers:

```text
plus_one_branch_has_no_base_field_residual_split_rows=3/3
minus_one_branch_has_no_base_field_residual_split_rows=3/3
no_valid_sign_has_base_field_residual_split_rows=3/3
c_power_root_criterion_rows=3/3
residual_unit_should_be_handled_divisorially_or_after_norm_extension=1
p24_cm_lang_proof_must_use_integral_norm_or_divisor_language_for_R_179=1
```
