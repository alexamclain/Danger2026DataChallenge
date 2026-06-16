# Trace-Frame Residual Tail Frontier

Date: 2026-06-05

This note isolates the current smallest proof object inside the leading
trace-frame Plucker route.

## Setup

Keep the p24 trace-frame tower:

```text
E = F_p(mu_m)
[C:E] = 179
B = C(theta)
[B:C] = 31
g = minpoly_C(theta)
```

For `x in B`, write:

```text
g'(theta)*x = b_0(x) + b_1(x) theta + ... + b_30(x) theta^30.
```

Let `W = W_axis(B)` be the `368`-dimensional `E`-span of the selected axis
K-character resolvents in one tensor factor.

The intrinsic theorem is:

```text
Top_3|W is injective
<=> W cap F_27 = {0}.
```

The expected rank profile is:

```text
rank Top_1(W) = 179
rank Top_2(W) = 358
rank Top_3(W) = 368.
```

Thus:

```text
K_2 = W cap F_28 = ker(Top_2|W)
dim_E K_2 = 10.
```

## Residual Tail Statement

The intrinsic final step is:

```text
b_28 : K_2 -> C
is injective.
```

The leading-prefix Plucker coordinate is the stronger coordinate statement:
choose the normal `E`-basis

```text
nu_0, nu_1, ..., nu_178
```

of `C`, and let

```text
pi_10 : C -> E^10
```

be projection onto the first ten normal-basis coordinates.  The named
certificate target is:

```text
pi_10 o b_28 : K_2 -> E^10
is an isomorphism.
```

Equivalently, there is no nonzero axis weight `w` such that:

```text
x_w = sum_r w(r) J_r(theta)
```

and:

```text
g'(theta)*x_w =
  q_0 + q_1 theta + ... + q_27 theta^27
  + c theta^28
```

with:

```text
c in span_E{nu_10, nu_11, ..., nu_178}.
```

The intrinsic theorem is the special case `c=0`.  The selected leading
coordinate theorem allows `c` to be nonzero, but only in the normal-basis tail.

This is the cleanest failure certificate I know how to state right now:

```text
nonzero structured axis weight
+ low relative degree <= 28
+ theta^28 coefficient supported outside the first 10 normal coordinates.
```

## Relation To Trace Pairing

The same condition can be written in trace-frame form.  Vanishing of the first
two top blocks is equivalent to:

```text
Tr_{B/C}(x_w) = Tr_{B/C}(theta*x_w) = 0
```

up to the fixed dual-basis triangular convention.  The residual tail condition
is the corresponding ten selected `E`-linear coordinate tests on the third
trace/top-coefficient block.

So the proof does not need to control all `5012` coordinates of the
annihilator `F_27`.  It needs to rule out a much smaller Schubert-tail
incidence inside the 10-dimensional residual kernel `K_2`.

## Trace-Dual Form

Let:

```text
nu_0^*, nu_1^*, ..., nu_178^*
```

be the trace-dual basis to the normal basis of `C/E`, so:

```text
Tr_{C/E}(nu_i^* * nu_j) = delta_{i,j}.
```

If `k_0,...,k_9` is any `E`-basis of `K_2`, the leading residual-tail
coordinate is, up to the basis-change determinant for `K_2`,

```text
D_tail =
  det( Tr_{C/E}(nu_i^* * b_28(k_j)) )_{0 <= i,j < 10}.
```

Thus the selected coordinate is not merely an arbitrary coordinate slice.  It
is a trace-Gram minor for the residual map from `K_2` to `C`:

```text
u_j = b_28(k_j),       0 <= j < 10.
```

The direct selected theorem is that the trace-dual matrix above has full rank.
If the residual image also has full dimension, writing:

```text
U = b_28(K_2) subset C,
T = span_E{nu_10,...,nu_178},
```

this is equivalent to:

```text
U cap T = {0}.
```

If `dim_E U = 10`, then in linearized-polynomial language, if `A_U` and `A_T`
are the `E`-linearized subspace polynomials for `U` and `T`, the same
condition is:

```text
gcd_linearized(A_U, A_T) = X,
```

or nonvanishing of the corresponding linearized resultant.  The dimension
hypothesis matters: the direct selected theorem is the Moore determinant of
`A_T o b_28` on `K_2`, which proves full residual rank and tail avoidance in
one step.  The resultant form is more intrinsic than a raw Plucker coordinate,
but `T` is a normal-basis tail rather than a subfield; it is not expected to
have a small subfield-invariance proof.

A more verifier-facing version avoids computing a full gcd.  Let `A_T` be the
monic `E`-linearized annihilator polynomial of `T`, so:

```text
ker(A_T : C -> C) = T,
qdeg_E(A_T) = 179 - 10 = 169.
```

Then:

```text
U cap T = {0}
<=> A_T|U is injective
<=> rank_E A_T(U) = 10.
```

For any `E`-basis `u_0,...,u_9` of `U`, this can be expressed as the Moore
determinant:

```text
M_tail =
  det( A_T(u_j)^(Q^i) )_{0 <= i,j < 10},      Q = |E|.
```

Thus a coordinate-free selected-origin p-unit target is:

```text
Norm_{C/E}(M_tail) != 0.
```

This is equivalent to the trace-dual leading minor as a zero test.  It is not
the same scalar, but it is a more intrinsic rank-metric package for the same
Schubert-tail incidence.

There is also an explicit projection form that avoids constructing `A_T`.
Define:

```text
P_10(X) =
  sum_{i=0}^9 nu_i * Tr_{C/E}(nu_i^* * X).
```

Equivalently, since:

```text
Tr_{C/E}(aX) = sum_{j=0}^{178} a^(Q^j) X^(Q^j),
```

this is the `E`-linearized polynomial:

```text
P_10(X) =
  sum_{j=0}^{178}
    ( sum_{i=0}^9 nu_i * (nu_i^*)^(Q^j) )
    X^(Q^j).
```

It is the projection:

```text
C -> H = span_E{nu_0,...,nu_9}
```

with kernel `T`.  Therefore:

```text
U cap T = {0}
<=> P_10|U is injective.
```

For any basis `u_0,...,u_9` of `U`, the Moore determinant:

```text
M_proj =
  det( P_10(u_j)^(Q^i) )_{0 <= i,j < 10}
```

is nonzero exactly when the leading trace-dual determinant is nonzero.  More
precisely, it differs from the `10 x 10` trace-dual coordinate determinant by
the fixed Moore determinant of the head basis `nu_0,...,nu_9`, which is a
nonzero basis constant.  This gives the cleanest named operator:

```text
fixed normal-head projection P_10
applied to the CM residual image U=b_28(K_2).
```

## Audit

I added:

```text
p24/trace_frame_residual_tail_audit.py
```

It computes:

```text
prefix_rank       = rank of the first top_count-1 C-blocks,
residual_dim      = raw_rank - prefix_rank,
tail_rank         = rank of the next C-block on that residual kernel,
leading_tail_rank = rank of the first residual_dim normal coordinates,
```

and checks whether the residual tail image is stable under cyclic shifts of the
normal basis, the visible form of `E`-Frobenius on `C`.
It also constructs the annihilator `A_T` of the normal-basis tail and checks:

```text
qdeg(A_T) = subdegree - residual_dim,
rank_E A_T(U) = leading_tail_rank.
```

Finally it records q-polynomial support:

```text
support(A_T)
support(P_head)
```

where `P_head` is the projection onto the first `residual_dim` normal-basis
coordinates.

Pinned partial-tail run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_residual_tail_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --scan-origins --max-rows 8 \
  --target constant_plus_4 --target constant_plus_3
```

reported:

```text
rows=8
residual_rows=8
proper_partial_tail_rows=4
full_tail_rank_rows=8
leading_tail_failures=0
trace_dual_mismatch_rows=0
tail_annihilator_degree_mismatch_rows=0
tail_annihilator_image_rank_mismatch_rows=0
frobenius_invariant_residual_rows=4
proper_frobenius_invariant_residual_rows=0
proper_full_qsupport_rows=4
```

The invariant rows are exactly the uninteresting cases where the residual
image fills the whole tail block.  In the p24-shaped partial cases
`residual_dim < subdegree`, the residual image is not Frobenius/subfield
stable, but the leading tail coordinate still separates it.

The trace-dual mismatch count verifies in actual small CM tensor rows that the
normal-coordinate tail determinant is exactly the trace-dual minor above.
The annihilator counts verify the equivalent linearized-resultant/Moore
formulation on the same residual-tail objects.
The support count is a useful boundary: in every proper partial-tail toy row,
both the tail annihilator and the head projection have full q-polynomial
support.  Thus the projection theorem is not becoming easy because `P_head`
is sparse or low-support.  The p24 analogue should be treated as a
full-support fixed projection of q-degree up to `178`, with:

```text
qdeg(A_T)=169, support(A_T) likely 170,
support(P_10) likely 179.
```

The missing arithmetic remains the CM transversality of `U=b_28(K_2)` against
this fixed full-support operator.

## Origin-Action Boundary

The residual-tail determinant was then audited across a full small CM origin
orbit in:

```text
p24/trace_frame_residual_tail_origin_action_audit.py
p24/trace_frame_residual_tail_origin_boundary.md
```

On the pinned `D=-10919, m=12, n=13` proper residual-tail rows, alpha shifts
left the base norm constant, while beta shifts moved through all `13` beta
values.  No residual-tail zeros occurred, and the product of base norms over
all beta shifts was alpha-constant and nonzero.

Thus the pointwise beta-invariance shortcut is not supported.  The two live
origin statements are:

```text
selected beta:
  Norm_{E/F_p}(D_tail(beta_0)) != 0

beta product:
  prod_{beta mod n} Norm_{E/F_p}(D_tail(beta)) != 0.
```

The beta-product statement is stronger but may be more class-field natural if
it can be expressed as a norm/resultant in the packet algebra without
enumerating all beta translates.

The finite resultant package is recorded in:

```text
p24/trace_frame_beta_product_resultant_boundary.md
p24/trace_frame_trace_sum_crossed_product_boundary.md
```

Small proper residual-tail rows confirm:

```text
prod_beta D_tail(beta)
  = Res_Y(Y^n - 1, f_tail(Y))
```

inside the tensor factor.  The same rows also show that `f_tail` is dense in
the beta coordinate and does not descend to `E[Y]`.  The coefficients do,
however, satisfy the semilinear covariance:

```text
c_l = c_{l / Q}^Q,       Q = |E|.
```

Thus the useful theorem surface is a twisted orbit packet-norm p-unit
statement, not a sparse-interpolant statement and not an ordinary
`E[Y]`-norm statement.

The same audit verifies the explicit orbit-trace expansion:

```text
D_beta = c_0 + sum_j Tr_{B/E}(c_j * theta^(-beta*ell_j))
```

for nonzero exponent orbits.  In the pinned proper residual-tail toy rows the
nonzero orbit seeds are full-normal over the tensor factor:

```text
seed_rank_hist=[1:1,6:2].
```

So the p24 proof should treat the `560` nonzero orbit seeds as full
`B/E`-normal trace seeds unless a new class-field identity proves otherwise.

## Consequence

This downgrades a tempting proof route:

```text
residual image is Frobenius-stable
=> leading normal coordinate is automatic.
```

That route is not supported by the small CM tensor rows and would not match
the p24 geometry, where:

```text
residual_dim = 10 << subdegree = 179.
```

The live theorem is therefore a genuine selected-prime Schubert p-unit:

```text
det(pi_10 o b_28 | K_2) != 0 in E
```

or in trace-dual form:

```text
det(Tr_{C/E}(nu_i^* * b_28(k_j)))_{0 <= i,j < 10} != 0.
```

or in linearized-resultant form:

```text
rank_E {A_T(b_28(k_j)) : 0 <= j < 10} = 10,
```

equivalently:

```text
det(A_T(b_28(k_j))^(Q^i))_{0 <= i,j < 10} != 0.
```

or, for the embedded selected origin in each H-packet:

```text
Norm_{E/F_p}(det(pi_10 o b_28 | K_2)) != 0.
```

An origin-stable beta product would be stronger.  The residual-tail statement
is the smallest selected-origin theorem currently visible.

The prefix-plus-tail factorization of the leading Schubert coordinate is
recorded in:

```text
p24/trace_frame_factorized_schubert_punit.md
```

It separates the theorem into:

```text
rank Top_2(W)=358,
pi_10 o b_28 injective on K_2=ker(Top_2|W).
```

The same note records the boundary from small value audits: the full leading
determinant norm is the cleaner invariant, while separate prefix/tail factors
are proof surfaces tied to the fixed normal-basis and pivot convention.

## Lean Gate

The direct selected-tail theorem and finite implications are checked in:

```text
p24/lean/TraceFrameResidualTailGate.lean
```

It proves the abstract gates:

```text
selected-tail operator p-unit
=> residual-tail avoidance

linearized resultant p-unit for A_U and A_T
=> U cap T = {0}

prefix coordinates equal
+ selected tail-head coordinates equal
+ residual-tail avoidance for source differences
=> selected leading coordinate map is injective.
```

It also checks that injectivity of the selected coordinate map implies
injectivity of the underlying factor evaluation.  The Lean gate does not prove
the p24 arithmetic nonvanishing; it prevents the finite reduction from drifting
while the missing theorem is attacked.
