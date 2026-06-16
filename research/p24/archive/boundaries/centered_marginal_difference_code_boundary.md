# Centered Marginal Difference-Code Boundary

Date: 2026-06-06

This note records the cyclic-difference form of the centered consecutive
window determinant.

## Difference Reformulation

For centered point columns

```text
P_b in F_q^(left-1),     b mod right,
P_0 = 0,
```

define cyclic differences

```text
Q_b = P_b - P_{b-1}.
```

Then:

```text
P_{t+i} - P_t = Q_{t+1} + Q_{t+2} + ... + Q_{t+i}.
```

The change from consecutive difference columns

```text
Q_{t+1}, ..., Q_{t+left-1}
```

to affine columns

```text
P_{t+1}-P_t, ..., P_{t+left-1}-P_t
```

is triangular with diagonal entries `1`.  Therefore:

```text
det(P_{t+1}-P_t, ..., P_{t+left-1}-P_t)
  = det(Q_{t+1}, ..., Q_{t+left-1}).
```

This is a finite determinant-line identity, not a new arithmetic theorem.

## Dual Support Form

In the dual word space, the cyclic difference map sends a plateau condition
to a coordinate-erasure support condition.  A word constant on a plateau of
length `left` has cyclic difference zero on the `left-1` edges inside that
plateau.

For p24:

```text
right = 211,
left = 157,
left - 1 = 156.
```

So the centered Fitting theorem can be restated as:

```text
no nonzero word in delta(W_C) is supported on the complementary 55 edges
with total sum zero.
```

The support subspace has dimension `54`, matching the centered Schubert
dimension count:

```text
dim delta(W_C) = 156,
dim support_subspace = 54,
156 + 54 = 210.
```

Thus the difference reformulation is exactly the same complementary
Schubert/Fitting problem inside the zero-sum hyperplane.

## Audit

Added:

```text
p24/centered_marginal_difference_code_audit.py
```

Pinned rows:

```text
D=-6719, q=6863, pair=(3,7):
  point_row_rank=2
  diff_row_rank=2
  diff_rows_sum_zero_count=2/2
  determinant_mismatches=0
  diff_shift_stable_count=0/6
  diff_max_shift_span_rank=4

D=-13319, q=13463, pair=(4,7):
  point_row_rank=3
  diff_row_rank=3
  diff_rows_sum_zero_count=3/3
  determinant_mismatches=0
  diff_shift_stable_count=0/6
  diff_max_shift_span_rank=6

D=-10919, q=11243, pair=(3,13):
  point_row_rank=2
  diff_row_rank=2
  diff_rows_sum_zero_count=2/2
  determinant_mismatches=0
  diff_shift_stable_count=0/12
  diff_max_shift_span_rank=4
```

The determinant identity is exact in the tested rows.  The cyclic-code
shortcut is not.

## Consequence

If the difference rowspace were a cyclic MDS code of length `211`, dimension
`156`, and distance `56`, the p24 theorem would follow from ordinary coding
theory.  The small actual-CM rows show that even after cyclic differencing the
rowspace is not shift-stable:

```text
diff_shift_stable_count = 0.
```

Thus BCH/cyclic-code theorems still do not apply.  The useful surviving
statement is a support-specific Fitting theorem:

```text
delta(W_C) avoids the 211 cyclic 54-dimensional zero-sum erasure subspaces.
```

This is the same theorem as the centered Schubert quotient map

```text
W_C -> H/B_t
```

being a p-unit determinant, but it gives a cleaner bridge to any future
sum-rank/MSRD or skew-polynomial proof attempt.

A stronger full scalar-MDS version was tested in:

```text
p24/centered_marginal_difference_mds_boundary.md
p24/centered_marginal_difference_mds_audit.py
```

It holds in the small actual-CM rows, but random controls also hold almost
always, so it currently gives no distinctive CM product formula.

## Boundary

The difference-code view moves the bad event from "dense plateau Schubert
subspace" to "coordinate support after a non-cyclic change of rowspace."  That
is not enough for an off-the-shelf distance theorem.  A successful CS import
would still need to prove the actual CM difference rowspace is p-unit
equivalent to an MDS/MSRD object, or prove the 211 named erasure determinants
directly.
