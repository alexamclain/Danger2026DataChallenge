# Axis Sliding-Window Sequence Complexity

This note checks whether the coefficient-minor product

```text
Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a)
```

might be computable from a short recurrence or low-degree resultant.

## Audit

I added:

```text
p24/axis_sliding_window_sequence_complexity.py
```

It measures the Berlekamp-Massey complexity of

```text
a_beta = det(P_0 X^(-beta) V_a)
```

and compares it with random full-rank subspaces in the same packet.

## Dimension-Forced Row

For

```text
D=-1431, q=1447, h=30, m=6, n=5
factor_degree=4, axis_dim=4
```

the sequence is constant for both CM and random subspaces:

```text
cm_axis:
  distinct_values=1
  bm_complexity=1

random_baseline:
  bm_min=1
  bm_max=1
```

This is a dimension artifact: when `factor_degree = axis_dim`, monomial
multiplication changes the leading determinant by a fixed determinant factor.

## First Extra-Dimension Row

For

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
factor_degree=10, axis_dim=6
```

the sequence has full cyclic complexity:

```text
cm_axis:
  distinct_values=11
  zero_count=0
  bm_complexity=11
  bm_over_n=1.000000
  product=1465

random_baseline:
  bm_min=11
  bm_max=11
  bm_avg=11.000000
  full_or_near_full_bm=200
```

So the first nontrivial row behaves exactly like random subspaces: full
complexity, no visible recurrence compression.

## Second Extra-Dimension Row

A sidecar reran the same test on the next composite row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_sliding_window_sequence_complexity.py \
  --only-D -10919 --random-trials 20 --max-cases 1 \
  --min-h 100 --max-h 180 --max-abs-D 12000 \
  --max-prime-quotients 8 --max-composite-quotients 20 \
  --min-n 3 --max-n 60 --q-stop 500000 \
  --max-splitting-primes 1 --max-axis-dim 12 \
  --max-factor-degree 20 --include-linear --require-composite-m
```

It reported:

```text
D=-10919, q=11243, h=156, m=12=4*3, n=13
factor_degree=12, axis_dim=6

cm_axis:
  zero_count=0
  bm_complexity=13
  bm_over_n=1.000000
  product=11031

random_baseline:
  full BM complexity in all 20 controls
```

This repeats the same pattern: the product is nonzero, but the beta sequence
has full cyclic complexity rather than a short recurrence.

## Consequence

The sliding-window product is now a clean p-unit target, but not a low-order
one.  It retains the full beta phase in small data.  Any proof or computation
of `Pi_axis,a` without class-set enumeration would need new arithmetic
structure; a generic recurrence/resultant compression is not visible.
