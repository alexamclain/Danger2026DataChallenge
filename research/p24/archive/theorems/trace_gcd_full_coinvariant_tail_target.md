# Trace-GCD Full Coinvariant Tail Target

Date: 2026-06-06

## Point

The fixed two-resultant input can be stated without choosing a prefix kernel
basis.  The prefix Hilbert-90 formulation already gives the intrinsic map

```text
R^4 -> E/(tau_R - 1)E,
(y_j) -> [sum_{j in {2,3,5,6}} y_j*S_j].
```

The tail determinant can be folded into the same coinvariant target.  Let
`C_tail` be the selected `16`-dimensional tail-coordinate subspace of `R`
dual to the first `16` Lang coordinates of the tail orbit `O1`.  Define

```text
Phi_full : R^4 + C_tail -> E/(tau_R - 1)E

Phi_full((y_j), z)
  = [sum_{j in {2,3,5,6}} y_j*S_j + z*S_1].
```

For p24 this is square:

```text
dim_Fp(R^4 + C_tail) = 4*35 + 16 = 156
dim_Fp(E/(tau_R - 1)E) = dim_Fp L = 156.
```

The fixed-resultant theorem is therefore equivalent to:

```text
det(Phi_full) is a p-unit
```

up to the usual p-unit determinant-line changes.

## Relation To Prefix Plus Tail

The trace map induces a p-local isomorphism

```text
E/(tau_R - 1)E  ~=  L
```

because `[E:L]=35` is a p-unit.  Under this isomorphism, `Phi_full` becomes
the trace-adjoint of the full leading trace-GCD map

```text
L -> R^4 + C_tail^vee,
lambda -> (
  Tr_{E/R}(lambda*S_j) for j in {2,3,5,6},
  first16 Tr_{E/R}(lambda*S_1)
).
```

Thus the following fixed-orbit statements are equivalent:

```text
1. Phi_full is an isomorphism modulo p;
2. the full `140+16` trace-GCD map on L is injective;
3. the four-prefix map has rank 140 and the selected tail is injective on
   its 16-dimensional kernel;
4. Res_p-lin(P_K0,T_0) is a p-unit.
```

The advantage is proof-facing rather than verifier-facing: `Phi_full` is a
single class-field coinvariant determinant.  A producer theorem may try to
construct this determinant directly from the mixed periods, instead of first
constructing a kernel basis and then a quotient-tail determinant.

## Actual-CM Determinant-Line Bridge

The bounded actual-CM audit

```text
p24/trace_gcd_actual_cm_square_coinvariant_audit.py
```

checks the finite determinant line after Lang trivialization.  If the selected
leading coordinates are `c_i in L` and `lambda_j` is the chosen `F_q`-basis of
`L`, then the trace-GCD matrix is

```text
B_ij = Tr_{L/F_q}(lambda_j*c_i).
```

The square coinvariant quotient map is represented by `e_i -> c_i`.  The audit
verifies on small actual-CM rows that

```text
det(B) = det(Phi_full) * det(Tr(lambda_i*lambda_j))
```

and that `det(Phi_full)`, `det(B)`, and the residual prefix/tail product have
the same zero event.  It includes six full-rank positive rows and four actual
nontrivial-prefix singular controls with shape `4=3+1`.

## Gaussian DFT / RS-Tail Form

The same fixed determinant can also be written after scalar extension to
`K=F_p(mu_35)`.  In the type-6 Gaussian normal basis of `R/F_p`, the four
full prefix right blocks diagonalize by a length-35 DFT.  The selected
16-dimensional tail does not diagonalize as a full group-ring summand; it
becomes the Reed-Solomon subspace of degree-`<16` polynomials evaluated on
the 35 frequency points.

The resulting theorem target is:

```text
no nonzero prefix frequency vector plus degree-<16 tail polynomial vanishes
in L tensor_{F_p} K.
```

This is recorded in:

```text
p24/trace_gcd_full_gaussian_rs_tail_target.md
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
```

## Nonzero Orbit Version

For a nonzero right Frobenius orbit `O`, transport the same construction:

```text
Phi_t : R^4 + C_t -> E/(tau_R - 1)E,       t in O.
```

The nonzero p-unit theorem is the crossed norm

```text
Nrd_O(det Phi_t) in O_p^*.
```

Together with unit-2 determinant-line transport, this is the same conditional
four-field payload:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

This target is still crossed-product/semilinear.  It does not imply ordinary
base-polynomial descent, and the existing holdout audit says that descent is
false on the small actual-CM rows.

## Current Missing Theorem

For the actual p24 mixed periods

```text
S_j = H_{157,211}(1,v_j),
```

prove that the square p-integral coinvariant determinant

```text
det Phi_full
```

is a p-unit at the selected ordinary prime above `p=10^24+7`, and prove the
analogous degree-35 crossed norm for one nonzero right orbit.

In explicit coboundary form, the fixed theorem says:

```text
sum_{j in {2,3,5,6}} y_j*S_j + z*S_1 = tau_R(W) - W
with y_j in R and z in C_tail
  =>
y_j = 0 for all j and z = 0.
```

This is the strongest current finite-field identity form of the fixed
trace-GCD p-unit.  It combines the prefix additive-Hilbert-90 obstruction and
the quotient-tail resultant into one selected class-field nonintersection.

## Toy And Gate

The finite duality and the bad controls are checked by:

```text
p24/trace_gcd_full_coinvariant_tail_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_audit.py
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
p24/lean/TraceGcdFullCoinvariantTailGate.lean
```

The toy verifies, in tiny coprime finite extensions, that the full
trace-GCD map on `L` is injective exactly when the square coinvariant map has
full rank.  It also includes a forced control where the tail contribution
lies inside the prefix span.  The actual-CM audit checks the determinant-line
identification with the trace-pairing and residual-product representatives on
small CM rows.  The Gaussian/RS-tail toy and audit check the equivalent
scalar-extended frequency form where the selected tail is a truncated
Reed-Solomon subspace rather than a stable group-ring block.

The nonzero-orbit crossed norm of these transported square maps is recorded
in:

```text
p24/trace_gcd_crossed_coinvariant_norm_target.md
p24/trace_gcd_crossed_coinvariant_norm_toy.py
p24/lean/TraceGcdCrossedCoinvariantNormGate.lean
```
