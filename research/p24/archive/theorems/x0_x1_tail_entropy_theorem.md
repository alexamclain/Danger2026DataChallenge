# X0/X1 Tail Entropy Theorem

This note makes the half-level orientation obstruction exact in the local
2-adic model.

## Setup

Let `p = 10^24+7`, so

```text
v2(p-1)=1.
```

For an `X0(2^a)` eigenline, Frobenius acts by an odd eigenvalue `lambda`, and

```text
t(lambda) = lambda + p/lambda mod 2^a.
```

The curve-side DANGER branch wants

```text
lambda == 1 mod 2^k,        k=40.
```

Suppose a half-level construction has already produced the oriented branch

```text
lambda == 1 mod 2^h.
```

This is stronger than plain `X0(2^h)`: it is already half-level `X1` data.

## Exact Count

Inside this half-level branch there are

```text
2^(k-h)
```

lifts modulo `2^k`.

Among these lifts:

```text
one lift has lambda == 1 mod 2^k;
two lifts satisfy t(lambda) == p+1 mod 2^k.
```

The second strict-trace lift is `lambda = 1 + 2^(k-1)`, which has
`v2(lambda-1)=k-1`; it is an `X0` trace root but not a true `X1` orientation.

## Proof

Write

```text
lambda = 1 + 2^h u,        u mod 2^(k-h),
p = 1 + 2c,                c odd.
```

The strict trace residue is equivalent to

```text
lambda + p/lambda == p+1 mod 2^k
```

or, after multiplying by `lambda`,

```text
(lambda-1)(lambda-p) == 0 mod 2^k.
```

For `h>=2`,

```text
lambda-p = 2(2^(h-1)u-c)
```

has exact 2-adic valuation `1`, because `c` is odd.  Therefore the strict
trace condition becomes

```text
v2(2^h u) + 1 >= k,
```

so

```text
u == 0 or 2^(k-h-1) mod 2^(k-h).
```

These are the two strict-trace lifts.  Only `u=0` gives
`lambda == 1 mod 2^k`.

For the trace-residue image size, expand

```text
lambda + p/lambda - (p+1)
  = (1-p)2^h u + p 2^(2h)u^2 - ...
```

and divide by `2^(h+1)`.  The resulting power series in `u` has linear
coefficient

```text
(1-p)/2,
```

which is odd.  Hence it is a bijection modulo `2^(k-h-1)` as a function of
`u mod 2^(k-h-1)`, and the original `u mod 2^(k-h)` map is exactly 2-to-1.
Thus the branch has

```text
2^(k-h-1)
```

distinct trace residues.

The audit script is:

```text
p24/x0_x1_tail_entropy_audit.py
```

For `h=20`, it reports:

```text
lifts = 1048576
strict_trace_lifts = 2
true_x1_lifts = 1
true_tail_cost = 1048576
trace_tail_cost = 524288
```

## Consequence

A half-level `X0` or even half-level oriented `X1` construction does not make
the remaining verifier condition free.  The missing high tail is exactly a
`2^(k-h)` choice for true `X1`, or `2^(k-h-1)` if one only asks for the
coarser strict trace residue.

Thus the product accounting in `half_level_x0_lift_sidecar.md` is not just a
heuristic density argument.  It is exact local 2-adic entropy:

```text
half-level branch cost * remaining true-tail cost
```

cannot beat the exponent unless a proposed construction supplies new
p-specific information about the tail `u` in

```text
lambda = 1 + 2^h u.
```

No such tail predictor is visible in the current low-degree character,
chain-label, dataset, or near-square audits.
