# Trace-Frame Factorized Schubert P-Unit

Date: 2026-06-05

This note isolates the factorized form of the leading trace-frame Plucker
coordinate after the annihilator-kernel boundary.

The finite certificate/accounting surface is specified in:

```text
p24/trace_frame_factorized_schubert_certificate_spec.md
p24/trace_frame_factorized_schubert_accounting.py
p24/trace_frame_single_leading_punit.md
```

## p24 Shape

Keep:

```text
E = F_p(mu_m)
C/E has degree 179
B/C has degree 31
W = W_axis(B),      dim_E W = 368
```

The leading coordinate keeps:

```text
Top_3 = C block 30 + C block 29 + first 10 coordinates of C block 28.
```

Equivalently:

```text
358 = 2*179 prefix coordinates,
10  = residual tail coordinates.
```

Thus the leading Schubert p-unit can be factored as:

```text
prefix theorem:
  rank_E Top_2(W) = 358,
  K_2 = ker(Top_2|W), dim_E K_2 = 10;

tail theorem:
  pi_10 o b_28 : K_2 -> E^10 is injective.
```

Together:

```text
Top_3,lead : W -> E^368
is injective.
```

This is exactly the finite implication checked by:

```text
p24/lean/TraceFrameResidualTailGate.lean
```

## P-Unit Form

After choosing the fixed normal basis of `C/E` and the deterministic leading
coordinate order, the finite certificate can be named as:

```text
Delta_lead = Delta_prefix * Delta_tail
```

up to the unit/sign from the chosen row-basis convention.

Here:

```text
Delta_prefix
  is a nonzero 358 x 358 prefix Plucker coordinate for Top_2(W);

Delta_tail
  is the 10 x 10 residual Schubert determinant on K_2.
```

The residual factor has several equivalent zero tests:

```text
det(pi_10 o b_28 | K_2) != 0
U=b_28(K_2) satisfies U cap span_E{nu_10,...,nu_178} = {0}
A_T|U is injective for the linearized annihilator of the tail
Moore(A_T(U)) != 0.
```

So the selected-prime theorem can be stated either as:

```text
Norm_{E/F_p}(Delta_lead) != 0,
```

or as the pair of p-unit statements:

```text
Norm_{E/F_p}(Delta_prefix) != 0,
Norm_{E/F_p}(Delta_tail)   != 0.
```

The second form is better for proof search because `Delta_tail` names the
actual cross-block obstruction isolated in:

```text
p24/trace_frame_annihilator_kernel_boundary.md
```

The prefix factor is itself split in:

```text
p24/trace_frame_prefix_intersection_boundary.md
```

There, `Top_2(W_axis)` is written as the sum of the images of:

```text
A = W_constant + W_2 + W_157,
B = W_211.
```

After component-normality, the prefix p-unit is exactly the minimal forced
intersection condition:

```text
dim(Top_2(A) cap Top_2(B)) = 10.
```

## Evidence And Boundary

The value audit:

```text
p24/trace_frame_leading_residual_value_audit.py
```

on the pinned `D=-10919, m=12` row reports:

```text
rows=12
nonzero_determinant_rows=12
zero_det_norms=0
```

For the full-axis row:

```text
subdegree=2, top_count=3:
  det_norm=11069 across tested origins,
  zero_blocks=[0,0,0];

subdegree=3, top_count=2:
  det_norm=8644 across tested origins,
  zero_blocks=[0,0].
```

However the block residual norms vary with origin:

```text
block_norm_shape_hist has no repetitions in the 12 displayed rows.
```

Therefore the full leading determinant norm is the cleaner invariant.  The
factorization is still a valid finite proof surface, but individual
`Delta_prefix` and `Delta_tail` factors depend on the chosen basis/pivot rule
unless stated intrinsically as:

```text
rank Top_2(W)=358,
U=b_28(K_2) avoids the fixed normal-basis tail.
```

The denominator-free version is now recorded in:

```text
p24/trace_frame_single_leading_punit.md
```

It uses `Delta_lead` itself as the descended object.  Nonzero `Delta_lead`
forces the prefix rank and residual-tail injectivity by the dimension count
`358 + 10 = 368`, so it avoids constructing a packetwise kernel basis before
descent.

The prefix-intersection audit:

```text
p24/trace_frame_prefix_intersection_audit.py
```

checks the intrinsic prefix statement directly in compact rows:

```text
component_full=1,
intersection_minimal=1,
prefix_max_rank=1.
```

## Relation To The Kernel Boundary

The forced-kernel audit shows why the tail factor is necessary.  In the
pinned row, a near-final forced kernel has:

```text
single_block_kernel_dims=[constant:0,4:0,3:0]
pair_kernel_dims=[4+3:1]
```

So component p-units can all hold while a cross-block residual kernel remains.
The `Delta_tail` p-unit is precisely the missing cross-block Schubert
transversality condition.

## Relation To The Beta/Tensor Bridge

For p24, the beta/tensor bridge says:

```text
560 beta orbits = 8 H-packets * 70 E-tensor factors.
```

So an origin-stable stronger theorem can be stated factorwise:

```text
for each H-packet and each of its 70 E-tensor factors,
the crossed-product reduced norm of Delta_lead is a p-unit.
```

The factorized version asks for the corresponding prefix and residual-tail
reduced norms.  Small beta-product audits suggest the ordinary-norm collapse
and sparse-interpolant shortcuts are false, so this remains a genuine
crossed-product p-unit theorem.

## Decomposition-Field Packet Norm

The four Schubert factors can also be packaged in the H-packet direction.  Let

```text
K_m = Q(mu_m),
M   = Q(zeta_n)^<p>,        [M:Q]=8,
S   = K_m M.
```

If the determinant construction is equivariant over `S`, then for each

```text
F in {A, B, AB, tail}
```

there is an element:

```text
Xi_F in S
```

whose eight residues at the primes above `p` are the packet determinants
`Delta_F(a) in E=F_p(mu_m)`.  Thus:

```text
Norm_{S/K_m}(Xi_F) mod p = product_a Delta_F(a) in E.
```

Nonvanishing of this relative norm certifies the factor in all eight
H-packets at once.  With tensor-factor rank symmetry, the 32 packetwise
Schubert p-unit obligations therefore become:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail are p-units.
```

The specialized statement is recorded in:

```text
p24/trace_frame_schubert_packet_norm.md
p24/trace_frame_schubert_equivariant_descent.md
p24/lean/SchubertEquivariantDescentGate.lean
p24/lean/TraceFrameSchubertPacketNormGate.lean
```

## Current Best Theorem Target

The cleanest proof target after this split is:

```text
1. construct the denominator-free leading element Xi_lead in
   K_m Q(zeta_n)^<p>, or construct the four compatible Schubert elements
   Xi_A, Xi_B, Xi_AB, Xi_tail;
2. prove the relevant relative norms to K_m are p-units at the selected prime
   over p;
3. decode those p-units as trace-frame injectivity, with the four-factor split
   giving the sharper prefix/residual-tail explanation.
```

This is a sharper statement than full random-rank transversality and a
stronger, sufficient replacement for component nonvanishing.  It still needs
new arithmetic: a phase-aware class-field p-unit, divisor contradiction, or
explicit split-cycle identity for the selected CM packet.
