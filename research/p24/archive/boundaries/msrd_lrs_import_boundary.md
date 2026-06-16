# MSRD / Linearized Reed-Solomon Import Boundary

Date: 2026-06-05

This note records the strongest CS-theory import found for the current
representative p-unit theorem.

## Live Representative Target

The p24 representative theorem is:

```text
L_rep != 0 mod p,
```

where `L_rep` is the Moore determinant for:

```text
O2,O3,O5,O6 full right packets + first 16 Lang coordinates of O1.
```

In dual support language, a bad nonzero vector would be supported only in:

```text
O4 full block + the unused 19 coordinates of O1,
```

so the bad support has size:

```text
35 + 19 = 54.
```

## Candidate Import

If the full mixed trace-dual code

```text
Phi(L) subset F_p^210
```

were block-equivalent to a linearized Reed-Solomon / MSRD sum-rank code of
dimension `156`, then its Singleton distance would be:

```text
210 - 156 + 1 = 55.
```

A nonzero codeword with support at most `54` would be impossible.  Therefore a
proved LRS/MSRD equivalence would imply the representative tail injectivity and
the whole unit-equivariant delete-one certificate.

This is the cleanest CS import because it matches the p24 erasure count
exactly.

The finite support implication is checked in:

```text
p24/lean/MSRDSupportGate.lean
```

In particular, Lean verifies the numerical gate:

```text
35 + 19 < 210 - 156 + 1.
```

Metric caveat:

```text
p24/msrd_metric_boundary.md
```

The `35+19=54` count is scalar-coordinate Hamming support unless a genuine
sum-rank expansion is supplied whose rank weight agrees with that count.  It
is not the coarse six-block right-orbit support.

## Missing Arithmetic Input

The import does not by itself prove p24.  It needs an arithmetic theorem:

```text
the actual CM/Lang trace-dual coordinate map is block-equivalent, with
p-unit coordinate changes, to the parity/check side of an LRS/MSRD code.
```

Equivalently, the named mixed CM periods must be identified as skew-polynomial
evaluation points with the required sum-rank independence.  Without that
identification, "MSRD" is only a restatement of the desired nonvanishing.

## Small Actual-CM Arc Audit

I added:

```text
p24/lang_arc_strength_audit.py
```

It tests a stronger ordinary Moore-arc proxy: whether every left-degree subset
of the actual Lang-transformed coordinates is independent.

Pinned actual-CM rows:

```text
D=-13319, q=13463, m=28, pair=(7,7):
  left_orbit_len=3, coordinate_count=6,
  subset_full=20/20,
  delete_one_leading_full=[1,1],
  random_full_arc_count=199/200.

D=-5444, q=2657, m=12, pair=(3,4):
  left_orbit_len=2, coordinate_count=3,
  subset_full=3/3,
  delete_one_leading_full=[1,1,1],
  random_full_arc_count=200/200.
```

Thus the full-arc strengthening is consistent with the small actual-CM rows,
but it is also random-generic at these field sizes.  This is evidence for a
useful theorem target, not a proof.

## Consequence

The live CS-shaped theorem is now sharper:

```text
prove a block-equivalence between the p24 mixed CM trace-dual code and an
LRS/MSRD code, or prove the exact selected support minor by a p-unit
skew-polynomial determinant identity.
```

The distinction between this sum-rank route and the ordinary full-arc/MDS
route is recorded in:

```text
p24/msrd_vs_mds_boundary.md
p24/msrd_metric_boundary.md
p24/lang_projective_relation_boundary.md
```

Everything weaker still leaves the same selected-prime p-unit problem:

```text
L_rep = B_rep*T_rep != 0 mod p.
```

The exact dictionary between this `35+19=54` support event, the trace-GCD
Schubert-orbit condition, and the operator-norm p-unit is recorded in:

```text
p24/trace_gcd_schubert_support_dictionary.md
```
