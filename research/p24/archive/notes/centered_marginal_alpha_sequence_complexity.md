# Centered Marginal Alpha-Sequence Complexity

Date: 2026-06-05

This note tests whether the reduced right-translation sequence

```text
F(t), t mod right,
```

from `p24/centered_marginal_origin_product_theorem.md` has low linear
complexity.  Low complexity would support a compact recurrence/resultant
certificate for the product:

```text
prod_t F(t).
```

## Script

Added:

```text
p24/centered_marginal_alpha_sequence_complexity.py
```

It reuses the origin-product audit, divides out the left translation
determinant, extracts the sequence indexed by `alpha mod right`, and runs
Berlekamp-Massey on two periods.

## Results

Small actual-CM rows:

```text
D=-6719, q=6863, pair=(3,7):
  sequence_length=7
  zero_count=0
  distinct_values=7
  linear_complexity_on_two_periods=7.

D=-13319, q=13463, pair=(4,7):
  sequence_length=7
  zero_count=0
  distinct_values=7
  linear_complexity_on_two_periods=7.

D=-10919, q=11243, pair=(3,13):
  sequence_length=13
  zero_count=0
  distinct_values=13
  linear_complexity_on_two_periods=13.
```

## Consequence

The reduced alpha sequence looks full-complexity in these rows.  This does
not rule out a class-field norm theorem, but it rules out the simplest
low-recurrence/resultant shortcut in the natural alpha coordinate.

For p24, the 211-factor right-translation product should be treated as a
full-support cyclic exterior product unless a new CM-adapted coordinate
system is found.
