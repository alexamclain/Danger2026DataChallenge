# Centered Marginal Cyclic-Code Boundary

Date: 2026-06-05

The p24 product route gives a cyclic sequence of consecutive minors, but this
does not mean the underlying row space is a cyclic code.

## Question

For the point matrix

```text
P_b(a) = M(a,b) - M(a,0) - M(0,b) + M(0,0),
b mod right,
```

the right-translation factors are:

```text
F(t) = det(P_{t+1}-P_t, ..., P_{t+left-1}-P_t).
```

A tempting shortcut is to treat the row space of `P` as a cyclic code and
apply BCH/MDS-style theorems.  This requires row-space stability under cyclic
right shifts.

## Audit

Added:

```text
p24/centered_marginal_cyclic_code_boundary.py
```

Small actual-CM rows:

```text
D=-6719, q=6863, pair=(3,7):
  row_rank=2
  max_shift_span_rank=4
  shift_stable_count=0/6
  window_zero_count=0
  window_distinct_count=7.

D=-13319, q=13463, pair=(4,7):
  row_rank=3
  max_shift_span_rank=6
  shift_stable_count=0/6
  window_zero_count=0
  window_distinct_count=7.

D=-10919, q=11243, pair=(3,13):
  row_rank=2
  max_shift_span_rank=4
  shift_stable_count=0/12
  window_zero_count=0
  window_distinct_count=13.
```

## Consequence

The cyclic minor product is a product over an orbit of coordinate windows, but
the row space itself is not a cyclic linear code in these analogues.
Therefore ordinary BCH, Reed-Solomon, cyclic-MDS, or cyclic-superregular code
theorems do not apply directly.

The surviving cyclic formulation is the resultant:

```text
Res_Y(Y^211 - 1, f_C(Y)) != 0,
```

where `f_C` interpolates the determinant sequence.  Proving this still needs
CM arithmetic or a new exterior trace-form identity, not just the abstract
cyclic-code structure.
