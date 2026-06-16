# Trace-GCD Prefix Gram Self-Orthogonal Obstruction

Date: 2026-06-06

This note sharpens the missing theorem in the prefix/full Gram route.

## Linear-Algebra Translation

For each trace-GCD right-orbit parameter `t`, let:

```text
L = F_p(mu_157)
<x,y> = Tr_{L/F_p}(xy)
U_t = span of the 140 prefix trace-coordinate elements in L.
```

The prefix Gram determinant is:

```text
P_t = det(<u_i,u_j>)_{u_i,u_j in prefix basis}
    = det(A_t G^{-1} A_t^T),
```

where `A_t` is the trace-functional row matrix and `G` is the trace-pairing
matrix on the chosen basis of `L`.  The metric-aware form is important:
ordinary `det(A_t A_t^T)` is coordinate-dependent for lower-dimensional
prefixes.

Therefore:

```text
P_t = 0
  <=> exists 0 != u in U_t such that <u,v> = 0 for every v in U_t
  <=> U_t cap U_t^perp != 0.
```

This is the exact obstruction that a prefix-Gram p-unit theorem must exclude.
It is stronger than ordinary prefix rank.  A full-rank prefix map can still have
a self-orthogonal prefix row space over a finite field.

## Kernel Complement

The ambient trace pairing on `L` is nondegenerate.  The trace-GCD prefix kernel
is:

```text
K_t = U_t^perp.
```

For a nondegenerate ambient pairing:

```text
rad(U_t) = U_t cap U_t^perp = rad(K_t).
```

Thus:

```text
P_t != 0  =>  the kernel Gram determinant is nonzero.
```

This is why the refined Schur payload can carry prefix and full Gram products,
without carrying a separate basis-dependent kernel Gram scalar.

## Orbit Product Theorem

The current prefix/full Gram arithmetic target is now:

```text
For every right Frobenius orbit O modulo 211:

1. prod_{t in O} det(<full_i(t), full_j(t)>) is a p-unit;
2. prod_{t in O} det(<prefix_i(t), prefix_j(t)>) is a p-unit.
```

Equivalently, for the prefix part:

```text
No t in any selected right orbit has a nonzero self-orthogonal vector
inside the 140-dimensional trace-GCD prefix row space U_t.
```

The full Gram factor is a full-window Moore determinant.  The prefix Gram factor
is the genuine new obstruction.

## Proof Directions

The prefix obstruction can be attacked as one of the following equivalent
forms:

```text
self-orthogonal prefix vector
  <=> nonzero prefix-supported trace word with vanishing prefix correlations;

self-orthogonal prefix vector
  <=> isotropic line in a selected Schubert cell for the trace pairing;

self-orthogonal prefix vector
  <=> local intersection of the determinant section with the trace-dual
      Schubert divisor.
```

The last form is closest to the direct Fitting route.  It suggests that the
cleaner theorem may still be the direct statement:

```text
the seven tail-on-kernel/Fitting orbit products Pi_O are p-units.
```

But if the Gram route is used, the missing theorem should be stated as the
absence of these prefix self-orthogonal lines, not merely as a rank condition.

## Checks

Finite logic:

```text
p24/lean/PrefixGramSelfOrthogonalGate.lean
p24/lean/PrefixGramErasureBridgeGate.lean
p24/lean/TraceGcdSchurBridgeGate.lean
p24/trace_gcd_metric_schur_refinement.md
```

Small finite-field guardrail:

```text
p24/prefix_gram_obstruction_toy.py
p24/kernel_tail_schur_identity_toy.py
p24/metric_schur_identity_toy.py
```

The toy is not an arithmetic proof.  It checks that the obstruction language
matches the Gram determinant and kernel-complement logic in ordinary finite
linear algebra.
