# Tensor Factor Marginal Random Support

This note compares CM marginal beta Plucker support with random controls.

## Question

The projected `D=-10919, m=12` marginal determinants have recurrence order
`7` for a period-`13` beta sequence.  Is that a CM-specific support collapse,
or is it forced by the representation shape of the chosen determinant?

## Audit

The script is:

```text
p24/tensor_factor_marginal_random_support_audit.py
```

It keeps the same tensor factor, top-coefficient map, CRT marginal determinant,
and beta-shift action, but replaces the quotient-fiber elements `J_r(theta)`
by random elements of the same tensor factor `B/E`.

Pinned `4`-component projected determinant:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_marginal_random_support_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1 \
  --target 4 --without-constant --random-trials 40
```

reported:

```text
cm_sequence:
  distinct=13
  zero_count=0
  recurrence_order=7
  characteristic_divides_T^n_minus_1=1

random_baseline:
  order_min=7
  order_max=7
  order_avg=7.000000
  order_hist={7: 40}
  distinct_min=13
  distinct_max=13
  trials_with_any_zero=0
  characteristic_divides_count=40
```

The `constant+3` determinant gives the same result:

```text
cm_order=7
random_order_hist={7: 40}
```

## Consequence

The toy recurrence order is not a visible CM-specific support collapse.  It is
generic for that projected determinant shape.  Therefore the p24 route should
not expect sparse support merely from the marginal/Top window construction.

This leaves two meaningful possibilities:

```text
1. prove a p-unit/superregularity theorem for full-support Plucker products;
2. find a much more special CM-derived Plucker coordinate or identity whose
   support collapse is not shared by random tensor-factor data.
```

The current evidence favors the first framing: a selected-prime
rank-condenser / Plucker p-unit theorem, not a sparse-support shortcut.
