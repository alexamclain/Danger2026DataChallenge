# Hermitian Mixed Trace-Intersection Theorem

This note restates the dual-trace target as a local intersection theorem.

## Setup

Let

```text
L = F_p(mu_157),        [L:F_p]=156,
R = F_p(mu_211),        [R:F_p]=35,
E = L R.
```

For the six right-orbit representatives `v_j`, set:

```text
S_j = H_{157,211}(1,v_j) in E,
W = span_R{S_1,...,S_6} subset E.
```

Use the perfect trace pairing for `E/R`:

```text
<x,y>_R = Tr_{E/R}(x*y).
```

The dual-trace map is:

```text
L -> R^6,
lambda |-> (<lambda,S_j>_R)_j.
```

Therefore the mixed Schur theorem is equivalent to:

```text
L ∩ W^perp = {0}.
```

Here `W^perp` is the `R`-orthogonal complement inside the 156-dimensional
`R`-space `E`.

## Why This Matters

The six periods cannot span `E` over `R`:

```text
dim_R W <= 6 << 156 = dim_R E.
```

So the proof cannot be "`S_j` span `E` over `R`."  The required theorem is a
transversality statement between:

```text
L, viewed as a 156-dimensional F_p-subspace of E,
and
W^perp, a huge R-subspace of codimension at most 6.
```

In scalar dimensions:

```text
dim_Fp L = 156,
codim_Fp W^perp <= 6*35 = 210.
```

So injectivity is dimensionally possible even though `W^perp` is enormous over
`R`.  In the random-linear model, a map

```text
F_p^156 -> F_p^210
```

is injective with overwhelming probability; a failure for p24 would require a
structured class-field reason.

## Existing Checks

The duality and trace-coordinate formulas are tested by:

```text
p24/hermitian_mixed_trace_dual_formula_toy.py
p24/hermitian_mixed_dual_trace_injectivity_toy.py
p24/hermitian_mixed_resolvent_pairing_audit.py
p24/hermitian_mixed_resolvent_pairing_formula.md
p24/lean/MixedTraceIntersectionGate.lean
```

The six-right-orbit finite-field toy:

```text
q=2, left=7, right=31
ord_7(2)=3
ord_31(2)=5
(31-1)/5=6
```

reported:

```text
dual_tests=80
rank_mismatches=0
full_span_tests=80
dual_injective_tests=80
```

A larger toy with `left_degree > 6` was intentionally stopped after it became
slower than its value for theorem-shaping.  The useful output here is the
exact intersection formulation, not another random-rank sample.

The finite equivalence between separation and trivial intersection is
Lean-checked in:

```text
p24/lean/MixedTraceIntersectionGate.lean
```

The six periods themselves are mixed K-character resolvent pairings:

```text
S_j = H_{157,211}(1,v_j) = <A_1,B_{v_j}>.
```

This is recorded and audited in:

```text
p24/hermitian_mixed_resolvent_pairing_formula.md
p24/hermitian_mixed_resolvent_pairing_audit.py
```

## Current Proof Surface

The p24 arithmetic theorem can now be stated as:

```text
For the six mixed Hermitian periods S_j, the R-orthogonal complement of
span_R{S_j} contains no nonzero element of L.
```

This is a local lattice/intersection p-unit theorem.  It is equivalent to the
210-coordinate Moore-minor p-unit, but it may be the better class-field
formulation because it speaks directly about relative trace pairings.

## Linearized Trace-GCD Form

The same theorem can be packaged as a linearized common-gcd identity:

```text
gcd_p-lin(X^(p^156)-X, T_1, ..., T_6) = X,
T_j(lambda)=Tr_{E/R}(lambda*S_j).
```

For the representative `140+16` certificate this becomes:

```text
K = common kernel of four full trace blocks,
dim_Fp K = 16,
the selected 16 tail coordinates have rank 16 on K.
```

Equivalently:

```text
gcd_p-lin(P_K, tail_16) = X.
```

This formulation and the small actual-CM audit are recorded in:

```text
p24/linearized_trace_gcd_certificate_boundary.md
p24/lang_trace_gcd_kernel_audit.py
p24/lean/TraceGcdGate.lean
```
