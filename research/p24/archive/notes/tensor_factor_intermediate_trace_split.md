# Tensor Factor Intermediate Trace Split

This note records the current status of trying to exploit

```text
[B:E] = 5549 = 31 * 179
```

inside one p24 tensor factor.

## Static p24 Accounting

The accounting script is:

```text
p24/tensor_factor_intermediate_accounting.py
```

It reports the unique proper intermediate subfields:

```text
E < F_{Q^31}, F_{Q^179} < B,
```

where `Q=|E|=p^5460`.

The selected axis dimensions are:

```text
constant: 1
2:        1
157:    156
211:    210
axis:   368
```

So:

```text
1 + 1 + 156 = 158 < 179,
210 = 31 + 179,
368 > 31 + 179.
```

This means the proper intermediate fields cannot certify the full axis rank by
dimension alone.  They can only hope to certify component-normality pieces.

## Trace Rather Than Containment

The right test is not whether the resolvents lie in a proper subfield.  In a
small analogue they do not.

The reusable audit is:

```text
p24/tensor_factor_subfield_trace_audit.py
```

For a subdegree `r | [B:E]`, it checks:

```text
x in F_{Q^r}             iff x^(Q^r) = x,
Tr_{B/F_{Q^r}}(x)        = sum_j x^(Q^(r*j)),
rank_E(Tr_{B/F_{Q^r}} block images).
```

If a trace image has full rank on a block, then the original block is full
rank, because trace is an E-linear map.  This is a valid way to prove
component block normality without requiring the block elements themselves to
belong to the subfield.

## Pinned Toy Row

For the dimension-possible analogue:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_subfield_trace_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12
```

the row is:

```text
D=-10919, q=11243, h=156, m=12, n=13
deg(f)=12, [E:F_q]=2, factors=2, [B:E]=6=2*3
axis_dim=6
```

No selected resolvent lies in a proper subfield:

```text
proper_subfield_membership=0
```

but the component blocks are certified by traces:

```text
block 4, size 3: trace to degree 3 has rank 3
block 3, size 2: trace to degree 2 has rank 2
constant:        every nonzero trace has rank 1
```

The full axis is not certified by proper traces alone:

```text
axis size = 6
joint proper trace rank = 4
```

So the toy row cleanly separates two facts:

1. proper traces can prove internal block normality;
2. cross-block directness still needs the full tensor factor.

The prime-degree control row:

```text
D=-8711, q=8747, h=132, m=12, n=11, [B:E]=5
```

has no nontrivial proper subfields and gives only the expected dimension-bound
axis rank.

## p24 Candidate Theorem

A sharper p24 theorem target is now:

```text
T_179 = Tr_{B/F_{Q^179}}
T_31  = Tr_{B/F_{Q^31}}
```

Prove:

```text
T_179 is injective on span_E(S_constant union S_2 union S_157),

(T_31, T_179) is injective on span_E(S_211),

span_E(S_constant union S_2 union S_157)
    intersects
span_E(S_211)
    trivially inside B.
```

The first two statements reduce component-normality to trace determinants in
degree `179` and `31+179=210`.  The third statement is the remaining
full-factor cross-block directness theorem.  It cannot be moved entirely to
proper subfields by dimension count.

## Twisted Trace Upgrade

The better use of the degree-179 subfield is not just the plain trace, but a
short twisted trace frame:

```text
T_3(x) = (
  Tr_{B/F_{Q^179}}(x),
  Tr_{B/F_{Q^179}}(theta*x),
  Tr_{B/F_{Q^179}}(theta^2*x)
).
```

This has target dimension `3*179=537`, enough to certify the full p24 axis.
The toy analogue `D=-10919` recovers full axis rank by exactly this mechanism:
for `[B:E]=6=2*3`, two traces to the degree-3 subfield or three traces to the
degree-2 subfield recover rank `6`.

The upgraded target is recorded in:

```text
p24/tensor_factor_twisted_trace_frame.md
p24/tensor_factor_twisted_trace_frame_audit.py
p24/lean/TraceFrameGate.lean
```

Conclusion: the intermediate-field split is a real refinement of the Moore
target.  Plain traces help with component normality; twisted traces are the
current best candidate for the full axis rank certificate.
