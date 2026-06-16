# Trace-Frame Sum-Rank Erasure Accounting

Date: 2026-06-05

This note records the exact p24 accounting for the stronger trace-frame
erasure theorem.

## Parameters

```text
E = F_p(mu_m),      [E:F_p] = 5460
B/C degree = 31
C/E degree = 179
dim_E W_axis(B) = 368
```

After multiplying by `g'(theta)` and expanding in the `C`-basis of `B/C`,
the axis image is an `E`-linear code:

```text
W_axis(B) subset C^31.
```

Each block has `E`-dimension `179`.

## Erasure Strengthening

The actual trace-frame certificate only needs one projection:

```text
pi_top3 : W_axis(B) -> C^3
```

to be injective.  The stronger erasure theorem asks for every `3`-block
projection to be injective.

The accounting script is:

```text
p24/trace_frame_sum_rank_erasure_accounting.py
```

It reports:

```text
relative_blocks=31
block_dimension_over_E=179
axis_dimension=368
keep_blocks=3
kept_dimension=537
erased_blocks=28
erased_dimension=5012
ambient_dimension=5549
three_block_subset_count=4495
```

Thus the erasure theorem is equivalent to excluding nonzero codewords
supported on any `28` coefficient blocks.

## Distance

A sum-rank/MSRD proof would give Singleton distance:

```text
d <= ambient_dim - axis_dim + 1
  = 5549 - 368 + 1
  = 5182.
```

The three-block erasure theorem only needs:

```text
d > 28*179 = 5012,
```

or:

```text
needed_distance = 5013.
```

So an MSRD/LRS identification has slack:

```text
5182 - 5013 = 169.
```

This is enough room that the stronger theorem is plausible as a coding-style
arithmetic target.

## Random-Subspace Warning

The random-subspace model is overwhelmingly favorable:

```text
Q = |E| = p^5460
kept_dimension - axis_dimension + 1 = 537 - 368 + 1 = 170
```

For one fixed `3`-block projection:

```text
failure ~= Q^-170.
```

A union bound over all

```text
binom(31,3)=4495
```

projections has essentially the same logarithm:

```text
log10(failure) ~= -2.227680e7.
```

Therefore small-data success of all erasure projections is not proof-like by
itself.  A p24 proof still has to identify a class-field reason:

```text
1. a p-unit Plucker coordinate for the selected top-three projection;
2. a block-equivalence to a genuine LRS/MSRD code;
3. a class-field norm/divisor identity proving the distance lower bound.
```

## Consequence

The smaller certificate surface remains the selected top-three projection.
The stronger all-three-block erasure theorem is best viewed as a possible
proof import: if the p24 relative coefficient code can be identified as a
high-distance sum-rank code, then the trace-frame certificate follows without
enumerating the class set.
