# Trace-GCD Prefix/Full Gram Payload Refinement

Date: 2026-06-05

This note refines the Hermitian-Schur route after the kernel-Gram
basis-dependence audit.

## Finite Payload

For each right Frobenius orbit `O` on `Z/211Z`, the metric-aware Schur bridge
uses:

```text
Pi_O = prod_{t in O} det(B_t | ker A_t)
P_O  = prod_{t in O} det(A_t G^{-1} A_t^T)
L_O  = prod_{t in O} det([A_t;B_t] G^{-1} [A_t;B_t]^T)
K_O  = prod_{t in O} det(N_t^T G N_t)
```

where `G` is the trace-pairing matrix on `L=F_p(mu_157)` in the chosen
coordinate basis.  The earlier ordinary-dot version is a finite plumbing
check, but the arithmetic payload should be this metric-aware version.

with:

```text
L_O K_O = P_O Pi_O^2.
```

The kernel determinant `K_O` is not a natural arithmetic payload because
`N_t` is a chosen kernel basis.  If `N_t` is replaced by `N_t C_t`, then:

```text
det((N_t C_t)^T(N_t C_t)) = det(C_t)^2 det(N_t^T N_t),
det(B_t N_t C_t)          = det(C_t) det(B_t N_t).
```

Zero/nonzero is invariant, but the scalar is determinant-line dependent.

For the ambient nondegenerate trace pairing, `ker A_t` is the orthogonal
complement of the prefix row space.  Therefore:

```text
P_O != 0  =>  K_O != 0.
```

The natural Gram payload is thus:

```text
P_O, P_O_inv, L_O, L_O_inv     for seven right orbits
```

with size:

```text
28 F_p elements = 2.8e-11 * sqrt(p).
```

The conservative payload that also carries `K_O,K_O_inv` has `42` elements,
but should be viewed as a debugging/honesty payload rather than the clean
arithmetic target.

The finite implication is Lean-checked in:

```text
p24/lean/TraceGcdSchurBridgeGate.lean
```

and the prefix/kernel complement guardrail is exercised by:

```text
p24/kernel_tail_schur_identity_toy.py
```

which reports:

```text
prefix_kernel_gram_zero_mismatches=0.
```

The metric correction is recorded in:

```text
p24/trace_gcd_metric_schur_refinement.md
p24/metric_schur_identity_toy.py
```

## Full Gram Factor

The full Gram factor `L_O` is a full-square trace-Gram determinant.  For any
`156` elements `x_1,...,x_156` in `L=F_p(mu_157)`, the trace-Gram matrix

```text
Gamma_{i,j}=Tr_{L/F_p}(x_i x_j)
```

satisfies:

```text
det(Gamma) = det(x_j^(p^i))^2.
```

So `L_O` is a Moore-determinant p-unit in disguise.  This is the same finite
identity used by the centered-profile route:

```text
p24/hermitian_mixed_centered_right_profile_theorem.md
p24/centered_profile_moore_trace_gram_identity_toy.py
p24/centered_profile_trace_gram_basefield_formula.md
p24/lean/CenteredProfileGate.lean
```

The actual Schur full window is the specific `140+16` trace-GCD window, not
necessarily the first `156` centered right-profile positions.  But the
finite Moore/trace-Gram identity applies to any full `156`-window after the
right coordinate transform.  Thus the full Gram p-unit is a natural
class-field/Moore determinant target.

## Prefix Gram Factor

The prefix Gram factor `P_O` is different.  It is a trace form restricted to a
`140`-dimensional prefix row space.  Unlike a full `156 x 156` trace-Gram
determinant, its nonzero-ness is not equivalent to ordinary rank over finite
fields.

The random finite-field controls in:

```text
p24/kernel_tail_schur_identity_boundary.md
p24/opposite_prefix_gram_boundary.md
```

show that full prefix rank can coexist with a singular prefix Gram.  Thus
`P_O` is the genuinely stronger arithmetic part of the Gram route.

The sharp obstruction form is recorded in:

```text
p24/trace_gcd_prefix_gram_self_orthogonal_obstruction.md
p24/lean/PrefixGramSelfOrthogonalGate.lean
```

It says that prefix Gram zero is exactly a nonzero vector in
`U_t cap U_t^perp` for the transported prefix row space.

## Current Theorem Candidate

The refined Hermitian-Schur arithmetic theorem is:

```text
For the actual p24 trace-GCD prefix/full windows,
the seven prefix Gram orbit products P_O
and the seven full Gram orbit products L_O
are p-units.
```

Then:

```text
P_O p-unit       => K_O p-unit,
L_O p-unit       => full Gram nondegenerate,
Schur identity   => Pi_O p-unit,
Pi_O p-unit      => every local Delta(t) nonzero,
Delta selected   => trace-GCD representative good.
```

This route is still stronger than the direct crossed-product/Fitting norm
theorem.  It becomes preferable only if `P_O` and `L_O` can be identified
with explicit Hermitian packet/autocorrelation norm values, where p-adic
unit methods have a better chance than for the raw tail-on-kernel determinant.

## Boundary

The current direct Fitting theorem remains cleaner:

```text
prove the seven trace-GCD block-cycle/Fitting orbit products Pi_O are p-units.
```

The Gram route is a bridge to Hermitian packet norms, not a free shortcut.
Its value is that `L_O` is a full-window Moore/trace-Gram object and `P_O`
is an intrinsic prefix trace-form determinant, avoiding a separate
kernel-basis determinant-line theorem.
