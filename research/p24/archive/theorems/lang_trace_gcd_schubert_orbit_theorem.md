# Lang Trace-GCD Schubert-Orbit Theorem

Date: 2026-06-05

This note restates the operator-norm target as a Grassmannian/Schubert
avoidance theorem.  It is equivalent to the trace-GCD resultant, but it gives
the arithmetic producer theorem a local-intersection shape.

## Setup

After origin covariance:

```text
Delta(t) = det(P V_t A),       t mod d.
```

For p24:

```text
d = 211,
k = 16,
R = F_p(mu_211) in one degree-35 right factor,
A: K -> R,       dim_Fp K = 16,
P: R -> F_p^16,  first-16 Lang/trace-dual coordinate projection.
```

Assume `A` is injective and set:

```text
W = A(K) subset R,             dim W = 16,
C = ker(P) subset R,           dim C = 19.
```

Then:

```text
Delta(t) != 0
  <=> P | V_t W is an isomorphism
  <=> V_t W cap C = {0}
  <=> W cap V_t^(-1) C = {0}.
```

Thus the origin-product theorem is:

```text
W avoids the 211 Schubert divisors
  Sigma_t = {U in Gr(16,R) : U cap V_t^(-1)C != 0}.
```

Equivalently:

```text
prod_{t mod 211} Delta(t) != 0.
```

The finite implication interface is Lean-checked in:

```text
p24/lean/TraceGcdSchubertOrbitGate.lean
```

It records that determinant-product nonvanishing plus the determinant/
intersection equivalence gives trivial intersection for every translated
Schubert condition.

The dictionary connecting this Schubert condition to the `35+19=54`
leading-erasure support obstruction and the MSRD support gate is:

```text
p24/trace_gcd_schubert_support_dictionary.md
```

## Operator-Norm Interpretation

The Schubert product is the same quotient-algebra norm from:

```text
p24/lang_trace_gcd_operator_norm_theorem.md
```

If:

```text
Q = F[Y]/(Y^211 - 1),
V_univ = sum_v E_v Y^v,
f_trace = det_Q(P V_univ A),
```

then:

```text
Norm_Q/F(f_trace)
  = prod_t Delta(t).
```

The Schubert-orbit statement says exactly that this norm is a p-unit.

## Arithmetic Producer Shape

The p24 producer theorem can now be stated geometrically:

```text
The p-integral CM 16-plane W_trace = A(K) in the right degree-35 factor
has zero local intersection at p with every translate of the Schubert divisor
defined by the selected 19-plane C=ker(P).
```

Equivalently, the section:

```text
s(W) = prod_{t mod 211} det(P V_t | W)
```

of the determinant-line bundle on `Gr(16,R)` is a p-unit at the CM point
`W_trace`.

This is not weaker than the operator-norm theorem; it is the same p-unit
statement in a geometry-first language.

## What Could Prove It

Possible proof routes now have sharper targets:

```text
1. local-intersection proof:
   construct an integral model of the CM point W_trace and show it does not
   meet any translated Schubert divisor modulo the selected prime;

2. divisor/norm proof:
   identify s(W_trace) as a CM value of a modular or automorphic product and
   compute its p-local valuation as zero;

3. explicit class-field plane proof:
   give a formula for W_trace inside R and prove no nonzero vector lies in
   any V_t^(-1)C;

4. operator proof:
   construct f_trace=det_Q(P V_univ A) directly and prove it is a unit in
   the p-local cyclic algebra.
```

The boundary for importing known Gross-Zagier/Borcherds local-intersection
machinery is recorded in:

```text
p24/trace_gcd_borcherds_literature_boundary.md
```

Generic finite-geometry arguments are insufficient: a random `16`-plane in
`F_p^35` avoids all 211 translates with overwhelming probability, but the
certificate needs the actual CM plane.

## Bounded Checks

The nontrivial small actual-CM row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_trace_gcd_spectral_scan.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --only-left 4 --only-right 7 \
  --include-linear --max-factor-degree 8 --max-extension-degree 8 \
  --min-left-orbit-len 2 --require-square-tail --require-prime-right \
  --min-tail-len 1 --max-rows 8
```

reported:

```text
omitted=0: zeros=0, product=6352, complexity=3
omitted=1: zeros=0, product=6639, complexity=3
```

The p24 exterior-support check:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/lang_trace_gcd_exterior_support.py
```

reported:

```text
right=211, orbit_len=35, tail=16,
k=3 already has distinct_subset_sum_size=211,
k=16 has distinct_subset_sum_size=211.
```

So a degree-35 spectral collapse would require special CM cancellations.  The
safe theorem remains Schubert-orbit avoidance / operator-norm p-unitness.

An attempted broader scan with:

```text
--max-rows 16 --max-cases 12 --q-stop 250000
```

was stopped after 45 seconds with no output.  It had become row discovery
rather than a cheap falsifier, so it should not be part of the proof path.

## Current Gap

The missing theorem is now:

```text
For the actual p24 CM trace-GCD plane W_trace, prove

  W_trace cap V_t^(-1) C = {0}

for all t mod 211, p-integrally at p = 10^24 + 7.
```

Equivalently:

```text
Norm_{F[Y]/(Y^211-1)/F}(det_Q(P V_univ A))
```

is a p-unit.  This is the current sharpest mixed-route theorem statement.
