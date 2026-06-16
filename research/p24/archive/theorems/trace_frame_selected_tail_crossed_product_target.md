# Trace-Frame Selected-Tail Crossed-Product Target

Date: 2026-06-06

This note splices the corrected selected-tail theorem into the existing
beta-orbit crossed-product package.

## Local Selected-Tail Value

For each beta translate, keep:

```text
K_2,beta = ker(Top_2|W_axis,beta)
dim_E K_2,beta = 10
```

and let `A_T` be the `E`-linearized annihilator of the normal-basis tail:

```text
T = span_E{nu_10,...,nu_178}
ker(A_T : C -> C) = T.
```

For an `E`-basis `k_0,...,k_9` of `K_2,beta`, define the direct selected-tail
operator determinant:

```text
M_tail(beta) =
  det( A_T(b_28(k_j))^(Q^i) )_{0 <= i,j < 10}.
```

Nonvanishing of `M_tail(beta)` proves:

```text
K_sel,beta = {0}.
```

This is the direct target; it packages both residual rank and avoidance of
the normal-basis tail.

## Denominator Caveat

`M_tail(beta)` depends on a basis of `K_2,beta`.  Its zero/nonzero status is
canonical, but a p-integral certificate must not hide bad denominators in the
chosen kernel basis.

Thus a denominator-safe proof should use one of:

```text
1. the full selected leading Plucker determinant Delta_lead(beta);
2. a Fitting/Schur package:
     prefix determinant p-unit
     + selected-tail operator determinant p-unit;
3. an integral construction of K_2,beta as a locally free kernel plus a
   p-unit determinant of A_T o b_28 on that kernel.
```

The selected-tail object is still the best proof-facing local theorem, because
it isolates the genuine `10 x 10` obstruction.  The final certificate payload
should remain denominator-safe.

## Crossed-Product Orbit Package

Let `B/E` be the degree-`5549` tensor factor and let:

```text
theta = image of zeta_n in B
Q = |E| mod n = p^5460 mod n.
```

Interpolate the beta sequence:

```text
f_tail(theta^(-beta)) = M_tail(beta),
f_tail(Y) in B[Y]/(Y^n - 1).
```

Because every `M_tail(beta)` lies in `E`, the interpolant satisfies the
semilinear fixed relation:

```text
f_tail(Y) = sigma(f_tail)(Y^Q).
```

For a beta orbit:

```text
Omega = { beta, beta*Q, ..., beta*Q^(5548) }
phi_Omega(Y) = product_{gamma in Omega} (Y - theta^(-gamma)) in E[Y],
```

define:

```text
R_tail,Omega =
  det_B(mul_{f_tail} on B[Y]/phi_Omega).
```

Then the finite identity is:

```text
R_tail,Omega = product_{gamma in Omega} M_tail(gamma).
```

Equivalently, `R_tail,Omega` is the reduced norm of the weighted semilinear
cycle with weights `M_tail(gamma)`.

## Theorem To Prove

The selected-tail crossed-product p-unit theorem is:

```text
For the actual p24 CM trace-frame packet:

  M_tail(0) is a p-unit, and
  every nonzero beta-orbit crossed-product norm R_tail,Omega is a p-unit.
```

Equivalently, in a global denominator-safe Fitting package:

```text
Xi_prefix is a p-unit,
Xi_tail,0 is a p-unit,
Xi_tail,Omega is a p-unit for every nonzero Omega,
```

or a single global norm detects all these orbit factors:

```text
Xi_tail,global != 0 mod p
and any zero orbit factor forces Xi_tail,global = 0.
```

For p24:

```text
n = 3107441
ord_n(Q) = 5549
nonzero orbit count = 560 = 8 H-packets * 70 E-tensor factors.
```

So this beats sqrt scaling as a theorem surface: it replaces `n` beta tests
and class-set enumeration by p-unit identities in the `560` crossed-product
orbit factors, or by one global norm that detects those factors.  With the
existing tensor-factor symmetry gates, a degree-8 packet norm is the desired
payload shape.

## Finite Gate

The finite implication is checked in:

```text
p24/lean/TraceFrameSelectedTailCrossedProductGate.lean
```

It proves:

```text
selected-tail bad event at beta
  => orbit product for orbitOf(beta) is zero;
reduced norm equals orbit product;
all reduced norms nonzero
  => no selected-tail bad event for any beta.
```

It also proves the global version:

```text
any zero reduced norm => global norm zero;
global norm p-unit
  => no selected-tail bad event for any beta.
```

The denominator-safe prefix-plus-tail package is checked in:

```text
p24/lean/TraceFramePrefixTailCrossedPackageGate.lean
```

It proves:

```text
Xi_A, Xi_B, Xi_AB are p-units
+ selected-tail crossed-product norms are p-units
=> prefix chart is good and K_sel,beta={0} for every beta
=> every selected trace frame is good.
```

The existing beta-product/crossed-product audits verify the finite orbit
identity on small actual-CM rows:

```text
p24/trace_frame_beta_product_resultant_audit.py
p24/trace_frame_trace_sum_crossed_product_audit.py
```

Those audits rule out ordinary-norm collapse and sparse beta interpolants, so
the p24 proof should target the crossed/Frobenius norm itself.

## Three Algebra Layers

The missing theorem lives across three compatible algebras.

1. Linearized selected-tail algebra:

```text
E{F_Q} acting on C/E, [C:E]=179,
C = H direct_sum T,
H = span_E{nu_0,...,nu_9},
T = span_E{nu_10,...,nu_178}.
```

This is where `A_T o b_28` directly proves `K_sel=0`.

2. Beta/tensor crossed-product algebra:

```text
E = F_p(mu_66254),
[B:E]=5549,
B[Y]/phi_Omega,
semilinear action (sigma, Y -> Y^Q).
```

This is where the orbit product becomes the crossed-product reduced norm
`R_tail,Omega`.

3. Embedded class-field tower:

```text
G = Cl(O_K),
G > <g^2> > <g^314> > <g^66254>,
relative degrees 2, 157, 211,
recovery quotient size 3107441.
```

This is where the producer theorem must identify the actual CM determinant
section and prove its reduced/Fitting norms are p-units.  Abstract class-field
roots or unembedded quotient roots are not enough; the theorem needs the
embedded non-genus phase data that selects the actual CM period and recovery
factor.

## What Would Finish This Route

A proof of the following would be enough:

```text
The p-integral selected-tail Fitting map
  K_2 -> C/T
is an isomorphism after localization at the selected prime over p,
and its beta-orbit determinant line has crossed-product reduced norms that
are p-units.
```

In finite-field terms this is:

```text
det(A_T o b_28 | K_2,beta) != 0 for every beta,
```

with the nonvanishing certified by crossed-product p-units rather than by
enumerating beta translates.

## Negative Controls

The following shortcuts remain false or too weak:

```text
W_axis cap F_27 = {0} as a replacement for K_sel = {0};
U cap T = {0} without full residual-image rank;
f_tail in E[Y];
R_tail,Omega = M_tail(beta_rep)^5549;
sparse beta support;
abstract bnrclassfield roots as embedded CM selectors;
coordinatewise Kummer p-units instead of determinant/Fitting p-units.
```

Small tests supporting these boundaries include:

```text
p24/trace_frame_trace_sum_crossed_product_audit.py
p24/trace_frame_beta_product_resultant_audit.py
p24/tensor_decomposition_accounting.py
p24/relative_tower_character_toy.py
p24/abstract_vs_embedded_quotient_toy.py
p24/embedded_selector_identity_toy.py
```
