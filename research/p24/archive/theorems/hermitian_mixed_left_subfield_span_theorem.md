# Hermitian Mixed Left-Subfield Span Theorem

This note sharpens the Lang-normality target and records a correction.

## Left-Subfield Landing

For p24:

```text
ord_157(p)=156
ord_211(p)=35
gcd(156,35)=1
```

After the right-orbit Lang trivialization from
`hermitian_mixed_lang_normality_theorem.md`, the transformed mixed coordinates
land in the left character field:

```text
F_p(mu_157) = F_{p^156}.
```

Thus the mixed `157 x 211` Schur block is controlled by:

```text
210 transformed coordinates in F_{p^156}.
```

The rank target is:

```text
dim_Fp span{these 210 coordinates} = 156.
```

Equivalently, some `156 x 156` Moore minor of the 210 coordinates is nonzero.

## Important Correction

A single normal element of `F_{p^156}` is **not** enough.

The row-orbit matrix after Lang trivialization is:

```text
M(a,i)=sigma^a(w_i),      0 <= a < 156.
```

Its rank over the scalar-extension field is the `F_p`-linear rank of the
tuple `{w_i}`, not the normal-basis rank of one coordinate's conjugates.  A
single coordinate can be normal as an element of `F_{p^156}`, but one column
still gives matrix rank at most `1`.

So the theorem is a **tuple span** theorem:

```text
at least 156 of the 210 transformed coordinates are F_p-independent.
```

## Audits

Added:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
p24/hermitian_mixed_left_subfield_identity_toy.py
p24/hermitian_mixed_trace_dual_formula_toy.py
p24/hermitian_mixed_dual_trace_injectivity_toy.py
p24/lean/MixedTraceDualGate.lean
p24/hermitian_mixed_trace_intersection_theorem.md
p24/hermitian_mixed_resolvent_pairing_formula.md
p24/lean/MixedTraceIntersectionGate.lean
```

Pinned CM rows:

```text
D=-10919:
  rows=2
  tests=12
  left_subfield_failures=0
  full_left_span_tests=12

D=-8711:
  rows=2
  tests=12
  left_subfield_failures=0
  full_left_span_tests=12
```

These rows have only tiny left orbit length `2`, so they test the machinery
but not p24-scale rank.

The coprime-degree finite-field toy:

```text
q=2, left=7, right=5
ord_7(2)=3, ord_5(2)=4, gcd=1
```

reported:

```text
left_orbit_tests=40
left_subfield_failures=0
full_left_span_tests=29
max_transformed_fq_rank=3
```

The same toy also showed why individual normality is only diagnostic:
individual normal coordinates can occur even when the tuple span rank is too
small.

## Trace-Dual Formula

The Lang coordinates have an intrinsic trace form.  Let

```text
E = F_p(mu_157, mu_211),
L = F_p(mu_157),
R = F_p(mu_211).
```

For each of the six right-orbit representatives `v_j`, let

```text
S_j = H_{157,211}(1, v_j) in E.
```

Choose an `F_p`-basis `alpha_i` of `R`, and let `delta_i` be the trace-dual
basis for `Tr_{R/F_p}`.  Then the 210 transformed coordinates are:

```text
w_{j,i} = Tr_{E/L}(delta_i * S_j),     1 <= j <= 6, 1 <= i <= 35.
```

The toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_trace_dual_formula_toy.py \
  --trials 20 --summary-only
```

reported:

```text
formula_tests=40
trace_dual_mismatches=0
left_subfield_failures=0
full_left_span_tests=29
```

So the current theorem target can be stated without procedural Lang matrices:

```text
dim_Fp span{Tr_{E/L}(delta_i * S_j) : i=1..35, j=1..6} = 156.
```

## Dual Injectivity Form

By trace duality on `L/F_p`, the span statement is equivalent to injectivity
of:

```text
L -> R^6,
lambda |-> (Tr_{E/R}(lambda * S_j))_{j=1..6}.
```

Equivalently:

```text
for every nonzero lambda in F_p(mu_157),
there exists a right orbit representative v_j such that
Tr_{E/F_p(mu_211)}(lambda * H_{157,211}(1,v_j)) != 0.
```

The toy

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_dual_trace_injectivity_toy.py \
  --trials 20 --summary-only
```

reported:

```text
dual_tests=40
rank_mismatches=0
full_span_tests=29
dual_injective_tests=29
```

The same duality was also checked in a small six-right-orbit toy:

```text
q=2, left=7, right=31
ord_7(2)=3, ord_31(2)=5
(31-1)/ord_31(2)=6
```

with output:

```text
dual_tests=80
rank_mismatches=0
full_span_tests=80
dual_injective_tests=80
```

This may be the best class-field-facing statement: six relative traces to the
right character field separate every nonzero left character.

The finite separation gate is Lean-checked in:

```text
p24/lean/MixedTraceDualGate.lean
```

## Intersection Form

Let

```text
W = span_R{S_1,...,S_6} subset E.
```

Under the `E/R` trace pairing, the dual injectivity statement is:

```text
L ∩ W^perp = {0}.
```

This is recorded in:

```text
p24/hermitian_mixed_trace_intersection_theorem.md
p24/lean/MixedTraceIntersectionGate.lean
```

This formulation is important because `dim_R W <= 6 << 156`; the six periods
do not need to span `E` over `R`.  They only need their orthogonal complement
to miss the embedded `F_p`-space `L`.

The six periods have the concrete resolvent-pairing form:

```text
S_j = <A_1,B_{v_j}>.
```

Here `A_1` is the left `157`-character resolvent and `B_{v_j}` are the six
right `211`-orbit resolvents.

## Subspace-Polynomial Form

Equivalently, if

```text
C = {Tr_{E/L}(delta_i*S_j)}
```

and `A_C(X)` is the monic `p`-linearized subspace polynomial of
`span_Fp(C)`, then the p24 target is:

```text
A_C(X) = X^(p^156) - X.
```

This is the same theorem as full `F_p`-span, but it is coordinate-free inside
`L` and identifies the failure mode as a common low-degree `p`-linearized
annihilator.  See:

```text
p24/hermitian_mixed_subspace_polynomial_certificate.md
p24/hermitian_mixed_subspace_polynomial_toy.py
p24/lean/MixedSubspacePolynomialGate.lean
```

## Centered Right-Profile Form

There is an even more intrinsic equivalent target.  Let `M(r,s)` be the
Hermitian double marginal and define:

```text
G_s = sum_r zeta_157^r M(r,s) in L,
G_s^0 = G_s - average_t(G_t).
```

The nonzero right DFT values `S_v` are the Fourier transform of `G_s`, with
the `v=0` component omitted.  Hence they determine exactly the centered
profile `G_s^0`, and the `F_p`-span of the trace-dual coordinates equals:

```text
span_Fp{G_s^0 : s mod 211}.
```

Thus the p24 target is also:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157).
```

This removes the right trace-dual basis from the theorem statement.  See:

```text
p24/hermitian_mixed_centered_right_profile_theorem.md
```

## Current Proof Surface

The mixed Schur correction is now reduced to:

```text
Prove that the 210 explicit Lang-trivialized mixed Hermitian CM periods span
F_{p^156} over F_p.
```

A proof could be:

```text
1. a class-field formula identifying these 210 values with a known spanning
   period family in F_p(mu_157);
2. a Moore-minor norm formula proving one selected 156-subtuple has p-unit
   determinant;
3. a local-lattice theorem ruling out containment in every proper F_p-subspace
   of F_{p^156}.
```

This is the most compact current statement of the mixed-character
nonvanishing theorem.
