# Trace-Frame Block-Moduli Boundary

Date: 2026-06-05

This note explains why the next proposed hidden-MSRD falsifier, a normalized
block cross-ratio, is not available on the current pinned small rows.

## Motivation

The support-profile audit:

```text
p24/trace_frame_msrd_invariant_audit.py
p24/trace_frame_msrd_invariant_boundary.md
```

found that the pinned CM rows satisfy the projection-rank and shortening
profiles expected of an MSRD-profile code.  But random controls with the same
shapes satisfy them identically.  The natural next invariant would be a
block-equivalence modulus:

```text
given four block kernels K_0,K_1,K_2,K_3 in a 2b-dimensional source,
normalize K_0,K_1,K_2 and compute the conjugacy class / eigen-data of the
cross-ratio operator defined by K_3.
```

Such an invariant is preserved by row operations and independent basis changes
inside the blocks.  A mismatch against LRS/MSRD controls would be a genuine
falsifier for hidden MSRD.

## Why The Pinned Rows Cannot Test It

The pinned `D=-10919, m=12` trace-frame analogues have:

```text
relative_degree = 3, subdegree = 2
```

or:

```text
relative_degree = 2, subdegree = 3.
```

The richer `m=3` and `m=4` rows for the same discriminant still have only:

```text
relative_degree = 3
```

in the subdegree-2 split.  These rows are too small for a four-block
cross-ratio.

More importantly, several of the tested MDS-profile rows are in a
no-moduli regime.  For example:

```text
dim C = 2b,     C subset V_0 + V_1 + V_2,     dim V_i = b,
```

and every two-block projection is an isomorphism.  Writing the code as a
graph over `V_0 + V_1` gives:

```text
v_2 = A v_0 + B v_1
```

where `A` and `B` are invertible.  Independent block changes

```text
v_0' = A v_0,
v_1' = B v_1,
v_2' = v_2
```

put the code in the standard form:

```text
v_2' = v_0' + v_1'.
```

So every such three-block MDS-profile row is block-equivalent at this coarse
level.  There is no cross-ratio or projective modulus to mine.

The other pinned profiles are similarly too small:

```text
dim C = 3, relative_degree = 3, subdegree = 2
```

has only three kernel lines in a 3-dimensional source; three generic lines
carry no stable cross-ratio.  At least a fourth block is needed before a
projective invariant can appear.

## Bounded Discovery Attempt

I tried a bounded discovery pass for a row with more relative blocks:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_relative_block_erasure_audit.py \
  --max-cases 5 --max-abs-D 30000 --min-h 24 --max-h 260 \
  --max-n 240 --max-m 80 --max-factor-degree 36 \
  --max-extension-degree 8 --max-tensor-factor-degree 24 \
  --max-subsets 2000 --include-linear --max-rows 30
```

It did not produce a useful row within a minute, so I stopped it.  That is
not mathematical evidence against such rows; it only says this is not a cheap
next falsifier in the current dataset.

## Consequence

The current small CM rows support the high-distance trace-frame shape, but
they cannot probe the real block-equivalence moduli needed for hidden MSRD.
Therefore more computation of the same projection/shortening style is unlikely
to move the theorem.

The proof search should return to the arithmetic local-unit target:

```text
delta_all in A_all^*
```

or, if hidden MSRD is pursued, it needs either:

```text
1. a dimension-rich toy row with at least four relative blocks and
   dim C = 2 * block_size; or
2. an explicit class-field block-equivalence construction rather than
   invariant mining on the pinned three-block rows.
```
