# Trace-GCD Schubert / Support Dictionary

Date: 2026-06-05

This note identifies the same finite obstruction in three languages:

```text
1. trace-GCD Schubert-orbit avoidance;
2. leading-erasure support avoidance;
3. scalar distance/MSRD-style support lower bound.
```

The point is to keep the proof target from splitting into apparently
different problems.

## Trace-GCD Language

For a representative row, let:

```text
K = common kernel of four full right trace blocks,
A: K -> R = F_p(mu_211),
P: R -> F_p^16       selected first-16 Lang coordinate projection,
C = ker(P),          dim C = 19,
W = A(K),            dim W = 16.
```

For a right-origin translate:

```text
Delta(t) = det(P V_t A).
```

Then:

```text
Delta(t) = 0
  <=> V_t W cap C != {0}
  <=> exists lambda in K, lambda != 0, with P V_t A(lambda)=0.
```

Thus the trace-GCD theorem is Schubert-orbit avoidance:

```text
V_t W cap C = {0}       for all t mod 211.
```

This is recorded in:

```text
p24/lang_trace_gcd_schubert_orbit_theorem.md
p24/lean/TraceGcdSchubertOrbitGate.lean
```

## Leading-Erasure Language

The full Delsarte/Lang trace-dual map is:

```text
Phi: L = F_p(mu_157) -> R^6 ~= F_p^210,
Phi(lambda) = (a_1(lambda),...,a_6(lambda)).
```

The representative row:

```text
deleted O4,
prefix B={O2,O3,O5,O6},
tail O1 first 16 coordinates
```

fails exactly when some nonzero `lambda` satisfies:

```text
a_j(lambda)=0       for j in {2,3,5,6},
first16(a_1(lambda))=0.
```

Equivalently, the nonzero word `Phi(lambda)` is supported only in:

```text
O4 full block + final 19 coordinates of O1.
```

That support has scalar size:

```text
35 + 19 = 54.
```

So the Schubert bad event is exactly the leading-erasure bad event:

```text
Phi(L) contains a nonzero word in the named 54-coordinate erasure subspace.
```

The six unit-equivariant deletion rows give the six analogous erasure
subspaces.  The unit action reduces these to one representative after the
product-algebra equivariance theorem.

## Distance / MSRD Language

If one could prove the scalar-coordinate distance bound:

```text
every nonzero word in Phi(L) has Hamming support >= 55,
```

then the representative bad event is impossible, because:

```text
54 < 55.
```

The finite implication is already Lean-checked in:

```text
p24/lean/MSRDSupportGate.lean
```

This is the valid meaning of the MSRD/LRS import in the representative
surface.  It is not a theorem about the coarse six-block support: in that
metric every word has support at most `6`, so a distance-55 statement would
force the code to be zero.  The metric caveat is recorded in:

```text
p24/msrd_metric_boundary.md
```

Therefore a coding-theory proof must supply either:

```text
ordinary scalar MDS/full-arc behavior for the 210 Lang coordinates,
```

or:

```text
a genuine sum-rank expansion whose rank weight agrees with the
54-coordinate erasure count.
```

Without that arithmetic equivalence, MSRD language only restates the desired
p-unit nonvanishing.

## Plateau / Cyclic-Code Language

In the centered right-profile formulation, a determinant factor vanishes when
a nonzero dual trace word has a long plateau.  For the p24 centered
`156`-minor:

```text
F(t)=0
  <=> some nonzero dual trace word is constant on 157 cyclic positions.
```

After subtracting the plateau constant, the bad word has time support at most:

```text
211 - 157 = 54.
```

This is the same scalar support number as the leading-erasure bad event.
Plain prime cyclic uncertainty only gives frequency support at least `158`,
while the actual family can use all `210` nonzero frequencies.  Thus
uncertainty alone cannot prove the theorem; the CM trace family must be used.

See:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
```

## Current Exact Theorem

All formulations now point to the same missing arithmetic input:

```text
For the actual p24 CM trace-dual code Phi(L), no nonzero word lies in the
representative 54-coordinate erasure subspace

  O4 + final19(O1),

and, by unit/product-algebra equivariance, no nonzero word lies in any of its
six deletion-row translates.
```

Equivalently:

```text
Norm_{F[Y]/(Y^211-1)/F}(det_Q(P V_univ A))
```

is a p-unit for the actual p-integral CM trace-GCD plane.

## What Would Finish This Route

A proof may choose any of these equivalent languages:

```text
Schubert/local-intersection:
  prove W_trace avoids all translated 19-planes V_t^{-1}C;

operator norm:
  construct f_trace=det_Q(P V_univ A) and prove it is a p-local unit;

support/distance:
  prove scalar distance >=55, or a p-unit block-equivalence to a code with
  that exact scalar support distance;

cyclic plateau:
  prove no nonzero CM left-twist trace word has the corresponding plateau.
```

The strongest current proof-facing form is still the Schubert/operator-norm
version, because it names the actual determinant-line section whose p-unitness
would produce the certificate.
