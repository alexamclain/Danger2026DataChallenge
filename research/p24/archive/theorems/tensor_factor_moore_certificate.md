# Tensor Factor Moore Certificate

This note replaces the coordinate-minor wording of the one-factor tensor
target with an intrinsic Moore determinant.

## Setup

For a p24 H-packet, after adjoining

```text
E = F_p(mu_m),
```

one tensor factor is a finite field

```text
B/E,       [B:E] = 5549.
```

Let

```text
Q = |E| = p^5460.
```

For the 368 selected K-character resolvents

```text
R_s in B,       s in S_axis,
```

form the Moore matrix

```text
M_{s,j} = R_s^(Q^j),       0 <= j < 368.
```

Then

```text
det(M) != 0 in B
```

is equivalent to E-linear independence of the 368 resolvents in `B`.

This is the coordinate-free one-factor certificate.  A coordinate minor in a
power basis is still a valid finite certificate, but the Moore determinant is
the cleaner class-field object.

## Audit

I added:

```text
p24/tensor_factor_moore_audit.py
```

Pinned dimension-possible row:

```text
D=-10919, q=11243, h=156, m=12, n=13
deg=12, [E:F_q]=2, factor_degree=6, axis_dim=6
coordinate_rank=6
moore_rank=6
```

Pinned dimension-bound row:

```text
D=-8711, q=8747, h=132, m=12, n=11
deg=10, [E:F_q]=2, factor_degree=5, axis_dim=6
coordinate_rank=5
moore_rank=5
```

So the Moore rank matches the coordinate rank in the expected way, and the
first one-factor dimension-possible row has full Moore rank.

## p24 Theorem Target

For every one of the eight p24 H-character packets, prove:

```text
Delta_axis,tensor =
det( R_s^(Q^j) )_{s in S_axis, 0 <= j < 368}
```

is nonzero in one, equivalently every, degree-5549 tensor factor `B/E`.

Because semilinear Frobenius permutes the factors and the axis frequency set,
factor rank is independent of the chosen factor:

```text
p24/tensor_factor_rank_symmetry.md
```

Because scalar extension and factor projection preserve the finite implication
chain:

```text
p24/lean/ScalarExtensionGate.lean
p24/lean/TensorFactorProjectionGate.lean
```

this Moore nonvanishing implies the original base packet axis injectivity.

## Norm Packaging

The determinant itself lies in `B`.  A scalar certificate is:

```text
Norm_{B/E}(Delta_axis,tensor) != 0.
```

For p24 this is a norm from degree `5549`, over the coefficient field
`E=F_p(mu_m)` of degree `5460` over `F_p`.  It is still large, but much
smaller and more intrinsic than the original degree-388430 packet determinant.

The remaining arithmetic input is a p-unit theorem for this Moore determinant
at the selected split prime.  The small data supports the statement, but no
known class-field identity here proves it yet.

## Intermediate Trace Split

Because `5549 = 31 * 179`, one tensor factor has two proper intermediate
subfields over `E`.  This is recorded in:

```text
p24/tensor_factor_intermediate_accounting.py
p24/tensor_factor_subfield_trace_audit.py
p24/tensor_factor_intermediate_trace_split.md
```

The split does not prove the full axis theorem by itself: the total dimension
of the proper trace targets is `31+179=210`, while the axis dimension is `368`.
However, small analogue data shows that proper traces can certify component
blocks even when the resolvents themselves are not contained in proper
subfields.  The refined p24 target is therefore:

```text
Tr_{B/F_{Q^179}} injective on constant + 2 + 157 blocks,
(Tr_{B/F_{Q^31}}, Tr_{B/F_{Q^179}}) injective on the 211 block,
cross-block directness still proved inside B.
```

The sharper version uses twisted traces to the degree-179 subfield:

```text
p24/tensor_factor_twisted_trace_frame.md
p24/tensor_factor_twisted_trace_frame_audit.py
p24/lean/TraceFrameGate.lean
```

For `C=F_{Q^179}`, prove full rank of

```text
R_s |-> (
  Tr_{B/C}(R_s),
  Tr_{B/C}(theta R_s),
  Tr_{B/C}(theta^2 R_s)
)
```

on the 368 selected axis resolvents.  This moves the certificate surface from
dimension `5549` over `E` to dimension `3*179=537` over `E`.

## Relation To Norm/Hermitian Packaging

The norm and Hermitian boundary is recorded in:

```text
p24/tensor_factor_norm_packaging_boundary.md
p24/tensor_factor_pairing_accounting.py
```

The Moore determinant is intrinsic for one-factor E-linear rank.  By contrast,
coordinate minors are Pluecker-coordinate certificates, and Hermitian
inversion pairs tensor factors `B_i` and `B_{i+35}` rather than acting inside
one factor.  Thus the one-factor Moore determinant is the smallest clean rank
surface, while the paired-factor Hermitian determinant is the more canonical
trace-form surface.
