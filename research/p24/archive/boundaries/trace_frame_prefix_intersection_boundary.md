# Trace-Frame Prefix Intersection Boundary

Date: 2026-06-05

This note isolates the prefix-rank part of the factorized Schubert p-unit.

## p24 Prefix Split

Write the p24 axis space as:

```text
W_axis = A + B

A = W_constant + W_2 + W_157,      dim_E A = 158
B = W_211,                         dim_E B = 210
```

The prefix part of the leading trace-frame coordinate is:

```text
Top_2 : W_axis -> C^2,
dim_E C^2 = 358.
```

The desired prefix rank is:

```text
rank_E Top_2(W_axis) = 358.
```

If:

```text
rank Top_2(A) = 158
rank Top_2(B) = 210
```

then maximal prefix rank is equivalent to the minimal possible intersection:

```text
dim(Top_2(A) cap Top_2(B))
  = 158 + 210 - 358
  = 10.
```

Thus the prefix p-unit can be attacked as:

```text
component normality for A and B
+ one 10-dimensional forced-intersection theorem.
```

The residual-tail p-unit from:

```text
p24/trace_frame_factorized_schubert_punit.md
```

then separates exactly this 10-dimensional prefix kernel.

## Audit

I added:

```text
p24/trace_frame_prefix_intersection_audit.py
```

It uses the local component ordering convention:

```text
A = constant plus all but the last smooth component,
B = last smooth component.
```

Pinned command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_prefix_intersection_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 \
  --max-n 200 --max-m 40 --max-factor-degree 20 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-top-count 4 --include-linear --only-m 12 --max-cases 1
```

The p24-shaped subdegree-2 row reports:

```text
D=-10919, q=11243, h=156, m=12, n=13
A=constant+4, B=3
dims=4+2->6
prefix_target=4
rankA=4, rankB=2, rankPrefix=4
intersection=2, expected_intersection=2
component_full=1
intersection_minimal=1
prefix_max_rank=1
```

The same bounded compact rows used in the beta/tensor and kernel audits also
match:

```text
D=-1559, q=2459, h=51, m=3, n=17
  A=constant, B=3
  dims=1+2->3
  intersection=1, expected_intersection=1

D=-2207, q=2243, h=39, m=3, n=13
  A=constant, B=3
  dims=1+2->3
  intersection=1, expected_intersection=1
```

In all three p24-shaped compact checks:

```text
component_full=1
intersection_minimal=1
prefix_max_rank=1.
```

## Consequence

The trace-frame theorem now has a clean three-piece p-unit shape:

```text
1. component prefix p-unit for A;
2. component prefix p-unit for B plus minimal A/B intersection;
3. residual-tail p-unit on the 10-dimensional forced intersection.
```

Equivalently:

```text
rank Top_2(W_axis)=358
and
pi_10 o b_28 is injective on ker(Top_2|W_axis).
```

The first line is not just separate component nonvanishing.  The
intersection-minimal condition is a genuine cross-component direct-position
theorem.  The second line is the residual Schubert p-unit already isolated in
the factorized note.

The Lean gate now also records the warning in finite form:

```text
nonzero forced prefix-intersection vector
  => prefix projection alone is not injective.
```

So the prefix success in the audit is not a reason to drop the residual-tail
or full-leading determinant.  It is evidence for the exact factorization of
the obstruction.

## Boundary

This does not prove p24.  It clarifies the arithmetic burden:

```text
prove a selected-prime p-unit for the forced A/B intersection position,
then prove a selected-prime p-unit for the residual normal-head projection.
```

The small audits support the shape and rule out a one-block explanation of
failures, but the p24 proof still needs a phase-aware class-field identity,
divisor contradiction, or crossed-product reduced-norm p-unit theorem.

## Lean Gate

The finite implication is checked in:

```text
p24/lean/TraceFramePrefixIntersectionGate.lean
```

It abstracts the prefix theorem as:

```text
nonzero forced prefix-intersection vector
  => prefix projection alone is not injective;

prefix-zero source is parametrized by the forced A/B intersection;
the residual tail kills only the zero intersection parameter;
kernelLift(0)=0;
```

and proves that the selected prefix-plus-tail coordinate map is injective.
Lean does not prove the arithmetic p-unit or the dimension count; it keeps the
factorized certificate logic from drifting.
