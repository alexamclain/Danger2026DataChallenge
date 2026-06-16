# Linearized Trace-GCD Certificate Boundary

Date: 2026-06-05

This note records the class-field-facing version of the representative
`140+16` p24 certificate.

## Trace-GCD Form

Let

```text
L = F_p(mu_157),        [L:F_p]=156,
R = F_p(mu_211),        [R:F_p]=35,
E = L R,
S_j = H_{157,211}(1,v_j).
```

For each right orbit define the relative trace map

```text
T_j(lambda) = Tr_{E/R}(lambda*S_j),       lambda in L.
```

The global trace-intersection theorem is equivalent to the linearized common
gcd identity:

```text
gcd_p-lin(X^(p^156)-X, T_1, ..., T_6) = X.
```

For the representative row, use the prefix

```text
B={O2,O3,O5,O6}
```

and the selected tail

```text
first 16 Lang/trace-dual coordinates of O1.
```

Let `K` be the common kernel of the four full prefix trace blocks.  The exact
representative theorem is:

```text
dim_Fp K = 16,
tail_16 has rank 16 on K.
```

Equivalently:

```text
gcd_p-lin(P_K, tail_16) = X,
```

where `P_K` is the subspace polynomial of `K`.

This is just the dual version of:

```text
four full blocks have rank 140,
and the tail contributes 16 dimensions.
```

The finite p24 number gate is now Lean-checked in:

```text
p24/lean/TraceGcdGate.lean
```

It records:

```text
kernelDim = 16, tailRankOnKernel = 16
=> trace-gcd degree = 0.
```

## Tool

Added:

```text
p24/lang_trace_gcd_kernel_audit.py
```

It builds actual small-CM Lang blocks, computes the trace-dual prefix kernel
using the `L/F_q` trace pairing, restricts the tail coordinates to that
kernel, and reports:

```text
dual_kernel_dim
tail_rank_on_kernel
trace_gcd_degree = dual_kernel_dim - tail_rank_on_kernel
```

It also checks that this agrees with the primal tail augmentation:

```text
rank(prefix + tail) - rank(prefix).
```

When the tail length equals `dim K`, the tool also reports the square
determinant of the tail trace matrix on a canonical kernel basis:

```text
tail_kernel_det.
```

This determinant is basis-dependent up to a nonzero scalar, but its
nonvanishing is intrinsic.  It is the finite-field analogue of the
linearized resultant

```text
Res_p-lin(P_K, tail_16).
```

## Pinned Actual-CM Runs

For `D=-13319`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_kernel_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --include-linear --max-factor-degree 8 \
  --max-extension-degree 8 --min-left-orbit-len 2 --max-rows 8
```

reported, among others, the nontrivial tail-only analogue:

```text
pair=(4,7), left=L2, right_lengths=[3,3]
omit0: prefix_rank=0, leading_rank=2, K=2, tailK=2, gcddeg=0, det=2125
omit1: prefix_rank=0, leading_rank=2, K=2, tailK=2, gcddeg=0, det=11423
```

and all primal/dual augmentation checks matched:

```text
match1
```

For `D=-5444`:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_kernel_audit.py \
  --only-D -5444 --only-q 2657 --q-start 2657 --q-stop 2658 \
  --only-m 12 --include-linear --max-factor-degree 8 \
  --max-extension-degree 8 --min-left-orbit-len 2 --max-rows 8
```

reported full-prefix, no-tail rows:

```text
pair=(3,4), left=L2, right_lengths=[1,1,1]
each deletion: K=0, tailK=0, gcddeg=0.
```

## Consequence

This does not prove p24, but it gives the cleanest current finite-field
identity for the missing arithmetic theorem:

```text
prove the actual p24 prefix trace kernel has dimension 16 and that the
selected tail trace map is nonsingular on it.
```

Equivalently, prove a selected-prime p-unit for the linearized resultant

```text
Res_p-lin(P_K, tail_16) != 0 mod p.
```

In determinant form, after choosing any `F_p`-basis

```text
k_1,...,k_16 of K
```

and the selected tail trace functionals

```text
tau_1,...,tau_16,
```

the arithmetic theorem is:

```text
det(tau_a(k_b))_{1<=a,b<=16} != 0 mod p.
```

This formulation is more class-field-facing than a raw Moore determinant,
because the objects are relative trace maps `T_j(lambda)=Tr_{E/R}(lambda*S_j)`
and the kernel `K` they cut out.

## Two-Orbit Compression Update

After the unit-2/diamond compression, the remaining p24 theorem is not seven
independent linearized resultants.  It is:

```text
1. the fixed-orbit resultant Res_0 is a p-unit;
2. one nonzero degree-35 Frobenius/crossed norm Norm_O1(Res_t) is a p-unit;
3. diamond determinant-line equivariance propagates that nonzero norm to the
   other five nonzero right orbits.
```

This sharper target is recorded in:

```text
p24/trace_gcd_two_linearized_resultant_target.md
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/lean/TraceGcdLinearizedResultantNormGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

The distinction matters: `Xi_O0` is a single selected linearized resultant,
whereas `Xi_O1` is a degree-35 orbit norm of such resultants.

The bounded actual-CM holdout audit:

```text
p24/trace_gcd_two_resultant_holdout_audit.py
```

now checks this exact shape on the pinned `D=-13319` row and the independent
`D=-26759` holdout:

```text
selected_two_punit_groups=4/4
all_nonzero_groups=4/4
punit_transport_edges=8/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

The last two lines are important: the nonzero representative is genuinely a
crossed/Frobenius norm, not an ordinary base-field resultant.

## Origin-Action Product Package

The selected determinant depends on the embedded CM origin.  For `h=m*n`,
write an origin shift as:

```text
shift == n*alpha + m*beta mod h.
```

The current small actual-CM audit suggests the trace-gcd determinant has the
Hermitian origin-action shape:

```text
Delta_i(alpha,beta) = unit * F_i(alpha mod right_component),
```

so beta cancels and the alpha motion reduces to the right component.

This is recorded in:

```text
p24/lang_trace_gcd_origin_action_audit.py
p24/lang_trace_gcd_origin_action_boundary.md
```

Pinned row:

```text
D=-13319, q=13463, h=140, m=28, n=5, pair=(4,7):
  omitted=0: zeros=0, alpha_value_period=7, beta_value_period=1
  omitted=1: zeros=0, alpha_value_period=7, beta_value_period=1.
```

For p24 this suggests the stronger 211-factor p-unit target:

```text
Pi_trace,i = prod_{t mod 211} det(tail_i on K_t) != 0 mod p.
```

This product is stronger than the selected-origin theorem but much smaller
than the class set.  It can be viewed as a cyclic resultant over the
right-translation sequence.  Proving this p-unit, or proving every factor
directly, would supply the missing determinant nonvanishing without
enumerating the class set.

The finite implication from the right-component product and covariance to the
selected representative determinant is Lean-checked in:

```text
p24/lean/TraceOriginProductGate.lean
```

## Schur / Pluecker Packaging

The determinant `det(tau_a(k_b))` can be repackaged in two standard finite
linear-algebra ways:

```text
Pluecker quotient:
  det(leading) = det(prefix pivot) * det(tail on K);

Gram Schur complement:
  det(leading Gram) * det(kernel Gram)
    = det(prefix Gram) * det(tail on K)^2
```

under the usual nondegeneracy hypotheses for the Gram form.  This is recorded
in:

```text
p24/kernel_tail_schur_identity_toy.py
p24/kernel_tail_schur_identity_boundary.md
```

The Pluecker quotient is an exact restatement of the same p-unit.  The Gram
Schur route is a possible stronger arithmetic target, but finite-field random
controls show full prefix rank often has singular prefix Gram, so it is not a
formal shortcut.

The route comparison against the trace-frame determinant-line front is:

```text
p24/punit_route_comparison_frontier.md
```
