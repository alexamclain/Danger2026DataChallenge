# Trace-Frame Arithmetic P-Unit Frontier

Date: 2026-06-05

This note consolidates the current arithmetic proof target after the CS/MSRD,
divisor, Toeplitz, and kernel-shape boundaries.

## Live Theorem

For the third strict p24 trace, the smallest trace-frame proof target is:

```text
A_all = O_E[Y]/(Y^3107441 - 1)
delta_all = det(T_lead,all)
delta_all in A_all^*
```

Equivalently, orbitwise:

```text
delta_Omega in A_Omega^*
```

or, in selected Schubert-tail form:

```text
K_sel,Omega =
  { x in W_axis(A_Omega) cap F_28(A_Omega) :
      pi_10(b_28(x)) = 0 }
  = {0}
```

for every beta orbit `Omega`.

The intrinsic full-top-three condition

```text
W_axis(A_Omega) cap F_27(A_Omega) = {0}
```

is a necessary consequence but not a sufficient replacement for the selected
`179+179+10` leading coordinate.  This correction is recorded in:

```text
p24/trace_frame_selected_lead_failure_module.md
p24/lean/TraceFrameSelectedLeadFailureGate.lean
```

The finite implication from a nonzero global reduced norm to all trace-frame
certificates is already checked in:

```text
p24/lean/TraceFrameBetaResultantGate.lean
p24/lean/TraceFrameLeadingNormGate.lean
p24/lean/TraceFrameNormCompressedCertificateGate.lean
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
```

The open input is arithmetic: prove the named determinant-line element is a
p-unit at the selected prime over:

```text
p = 10^24 + 7.
```

## Equivalent Arithmetic Faces

The same theorem has several exact forms.

### Local Fitting Unit

```text
Fitt_0(coker T_lead,Omega) = A_Omega.
```

This is the cleanest module statement.  A proof would construct the leading
trace-frame map integrally over the orbit algebra and show it is an
isomorphism after reduction at the selected prime.

### Crossed-Product Reduced Norm

For beta-shifted leading determinants:

```text
D_beta = Delta_lead(theta^(-beta)),
```

the orbit factor is:

```text
R_lead,Omega = product_{gamma in Omega} D_gamma.
```

Equivalently, it is the reduced norm of `delta_Omega`.  The theorem is:

```text
R_lead,Omega is a p-unit for every Omega.
```

This is recorded in:

```text
p24/trace_frame_lead_crossed_product_norm.md
```

### Weighted Fourier / Toeplitz Minor

The determinant is also a CM-weighted Fourier minor:

```text
det( (F * diag(Lambda_CM) * F^{-1})_{T,S} )
```

or, after inverse DFT, a selected cyclic translate/Toeplitz minor of the
singular-moduli torsor:

```text
det(j_{t_i-s_j})_{i,j=1}^{368}.
```

The theorem is therefore a selected-minor p-unit statement, not a full
normality statement.

## Shortcuts Now Closed

The following proof shapes have been tested and are not sufficient.

```text
component-only p-units:
  forced kernels in small rows are cross-axis;

sparse low-tail annihilator:
  forced low-degree congruences fill the allowed low tail;

plain selected-j divisor:
  leading determinant norms have generic rational degree and no small
  Heegner support in moving rows;

single oriented-edge low-bidegree relation:
  no bounded bidegree relation was found in moving rows;

ordinary Fourier/Chebotarev support:
  nonzero Fourier coefficients and nonzero CM weights do not prevent
  full-support cancellation;

ordinary cyclic Toeplitz symbol nonzero:
  all symbol coefficients and full translate determinant can be nonzero while
  a selected minor vanishes;

full reduced normality plus Jacobi complement:
  transfers the problem to a huge complementary inverse minor;

principal archimedean dominance:
  proves characteristic-zero nonvanishing only, not p-unitness;

visible MSRD/LRS structure:
  no low-displacement signature appears in the natural basis;

coarse hidden-MSRD support profiles:
  pinned CM rows pass, but random controls pass identically.
```

## What Would Count As Progress

The next useful theorem candidate must supply genuinely p-adic arithmetic,
for example:

```text
1. determinant-line unit theorem:
   construct T_lead,Omega over a p-integral crossed-product order and prove
   the reduced map is an isomorphism;

2. divisor/intersection theorem:
   identify the Schubert degeneracy divisor of delta_Omega and prove the
   selected CM prime has zero local intersection with it;

3. CM-weighted minor identity:
   collapse the Cauchy-Binet/Toeplitz exterior polynomial for the actual
   singular-moduli weights to a known p-unit;

4. explicit p-unit block equivalence:
   produce class-field coordinate changes taking W_axis(B) to a known
   high-distance MSRD/LRS code.
```

Without one of these, computation should remain limited to tiny falsifiers.
The current finite artifacts are enough to verify a supplied arithmetic
p-unit theorem; they do not themselves prove it.

The Borcherds/local-intersection specialization is recorded in:

```text
p24/trace_frame_borcherds_punit_boundary.md
p24/lean/TraceFrameBorcherdsPUnitGate.lean
```

It makes the missing product-formula input explicit: construct a phase-aware
Borcherds/divisor value whose CM value is the leading determinant-line norm
up to p-units, and prove the selected p-local intersection term vanishes.

The comparison with the mixed representative trace-GCD front is recorded in:

```text
p24/punit_route_comparison_frontier.md
```

That note keeps the trace-frame route as the payload-optimal backend, while
selecting the mixed trace-GCD determinant as the sharper next proof-facing
arithmetic target.

## Current Best Bet

The most direct route is still:

```text
prove delta_all in A_all^*
```

via the local Fitting/determinant-line statement.  This avoids selected-chain
branch construction, avoids packetwise kernel denominators, and matches the
degree-8 norm-compressed certificate surface already Lean-gated.

The denominator-safe Fitting attack is now stated explicitly in:

```text
p24/trace_frame_denominator_safe_fitting_attack.md
```

It packages the proof as:

```text
Fitt_0(coker T_lead,all) = A_all
```

after localization at the selected prime over `p`, with
`Xi_A`, `Xi_B`, `Xi_AB`, and `Xi_lead` as the descended p-unit objects.

The CRT-axis support polynomial should be viewed as a mixed Plucker /
representable-matroid basis polynomial:

```text
det(A diag(Lambda_CM) B).
```

That name is useful, but the ordinary matrix-tree/Pfaffian escape route is
closed by:

```text
p24/axis_crt_matrix_tree_factorization_toy.py
```

which violates the pair-sum identities required for edge-product tree
weights in exact `m=6,10,15` analogues and in a sampled tripartite `m=30`
analogue.  The remaining theorem is p-unit noncancellation of the actual
mixed Plucker pairing, not generic matroid support.
