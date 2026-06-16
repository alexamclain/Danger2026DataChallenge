# Trace-Frame Axis/Prefix Overlap Boundary

Date: 2026-06-05

This note tests the most direct principal-product dominance idea for the
selected leading Plucker coordinate.

## Question

In the cyclic Toeplitz/translate-minor model, a principal singular-modulus
factor appears when a selected row index equals the matched selected column
index, up to cyclic origin.  If the leading-prefix row set and the smooth-axis
column set had a large diagonal overlap, one might hope for a determinant term
containing many principal factors and dominating all other terms.

For p24 the smooth-axis character support is:

```text
S_axis = {0}
  union nonzero 2-axis frequencies
  union nonzero 157-axis frequencies
  union nonzero 211-axis frequencies
subset Z/66254Z.
```

The leading-prefix coordinate has size:

```text
368 = 1 + (2-1) + (157-1) + (211-1).
```

The naive dominance check asks:

```text
how many smooth-axis frequencies can lie in any cyclic interval of length 368?
```

## Audit

I added:

```text
p24/trace_frame_axis_prefix_overlap_audit.py
```

It reports:

```text
m=66254
axis_dim=368
axis_support_size=368
leading_prefix_overlap_count=2
leading_prefix_overlap_points=[0,314]
max_cyclic_interval_overlap=3
max_overlap_ratio=3/368
```

Example best shifts:

```text
start=261 points=[314,422,628]
components=['211','157','211']
```

So no cyclic translate of the leading prefix can align with more than three
smooth-axis frequencies.

## Consequence

The obvious principal-diagonal dominance theorem is not available for the
selected leading coordinate:

```text
at most 3 out of 368 factors can be principal by row=column matching.
```

This does not disprove a subtler dominance theorem.  A determinant term could
still be distinguished by a more complicated reduced-form statistic, or by a
p-adic property invisible in the row/column overlap.  But the easy
principal-product route:

```text
many principal singular moduli in one determinant term
```

is closed for this index set.

The remaining p-unit theorem must use nonprincipal arithmetic, a hidden basis
change, or a selected-prime divisor/p-adic argument rather than diagonal
principal dominance of the current leading prefix.
