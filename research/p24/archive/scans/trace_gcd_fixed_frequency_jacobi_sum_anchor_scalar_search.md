# Jacobi Anchor Scalar Search

Date: 2026-06-07

## Point

The anchor-correction gate showed that replacing

```text
U(0,0)=J(1,1)=q-2
```

by `1` repairs the finite-field Jacobi product identities.  This search asks
which scalars work if only the degenerate anchor value is allowed to vary.

For each tested small row, it exhaustively tries every value-field scalar
`x` as:

```text
U'(0,0)=x
U'(r,k)=U(r,k) otherwise.
```

It requires the corrected packet to satisfy both:

```text
U'(r,0)U'(-r,0) = constant
prod_k U'(r,k)/U'(r,0)^c = constant in r
```

for every right-mixed admissible pair.

## Result

The exhaustive scalar search collapses to:

```text
x = +1 or x = -1.
```

The `+1` branch is the reduced `Jdagger(1,1)=1` anchor used by the
cyclotomic-divisor residual.  The `-1` branch is a scalar sign ambiguity: it
also satisfies the pair-product and row-ratio tests, but it is not a new
right-zero divisor shape.

This matches the quick constraints:

```text
x^2 = 1       from C-zero pair-products
x^(c-1) = 1   from selected row-product ratios
```

with `c` odd.

## Consequence

For the p24 proof search, the anchor ambiguity is much smaller than it looked:

```text
find the selected CM/Lang realization of the R_179 residual;
then fix the remaining +/- sign normalization.
```

This is still not a p24 certificate, but it is a real reduction in the
computational search space around the anchor.

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_scalar_search.py
```

Expected markers:

```text
exhaustive_anchor_scalar_search_rows=3/3
valid_anchor_scalars_are_plus_minus_one_rows=3/3
reduced_packet_plus_one_anchor_rows=3/3
raw_q_minus_2_anchor_rejected_rows=3/3
finite_jacobi_anchor_scalar_search_space_collapses_to_two_signs=1
p24_anchor_search_should_focus_on_cm_lang_realization_plus_sign_normalization=1
```
