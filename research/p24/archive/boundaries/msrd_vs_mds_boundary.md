# MSRD vs MDS Boundary

Date: 2026-06-05

This note separates three coding-theory strengthenings of the representative
p-unit theorem.

## Selected Minor

The actual finite certificate only needs one selected Moore minor:

```text
L_rep != 0.
```

Equivalently, one coordinate set of size `156` is independent:

```text
O2,O3,O5,O6 full blocks + first 16 coordinates of O1.
```

This is the weakest and sharpest theorem target.

## Ordinary MDS / Full Moore Arc

A stronger route is ordinary Hamming-MDS:

```text
every 156-subset of the 210 Lang coordinates is independent over F_p.
```

Then the corresponding `[210,156]` code has Hamming distance:

```text
210 - 156 + 1 = 55,
```

so any bad word supported on only `54` coordinates is impossible.

This is exactly what `p24/lang_arc_strength_audit.py` tests in small rows.
The audit found full-arc behavior in two actual-CM rows, but random baselines
were also full arcs.  Thus ordinary MDS is a plausible strengthening but not a
visible CM identity.

## Ordinary Gabidulin Is Not the p24 Shape

One tempting mistake is to call the 210 Lang coordinates an ordinary Gabidulin
evaluation set in:

```text
L = F_p(mu_157),  [L:F_p] = 156.
```

But ordinary Gabidulin MRD length over `F_{p^156}` is bounded by the extension
degree:

```text
n <= 156.
```

The p24 coordinate count is:

```text
210 > 156.
```

So an ordinary single-shot Gabidulin explanation cannot cover the whole p24
coordinate set.  At most, the actual columns can be viewed as an ordinary
MDS/full-arc set over the base field, or as a support-specific Moore minor.

## Sum-Rank LRS / MSRD

The MSRD route is different: it uses the six right Frobenius packets as
blocks.  A linearized Reed-Solomon or related sum-rank construction can have
multiple shots/blocks, so total coordinate count can exceed the single
extension degree.

For p24 the desired statement is:

```text
the six-block mixed trace-dual code is block-equivalent to an
[210,156] LRS/MSRD code.
```

If true, the sum-rank Singleton distance is `55`, and the representative bad
support has size `35+19=54`.  The finite implication is Lean-checked in:

```text
p24/lean/MSRDSupportGate.lean
```

This support count is a scalar-coordinate count unless an explicit sum-rank
expansion is supplied.  The metric caveat is recorded in:

```text
p24/msrd_metric_boundary.md
```

## Consequence

There are now three theorem targets, ordered by strength:

```text
1. selected p-unit:         prove L_rep != 0;
2. ordinary MDS/full arc:   prove every 156-subset is independent;
3. sum-rank LRS/MSRD:       prove a six-block skew-evaluation equivalence
                             with an explicit rank metric of total length 210.
```

The third is the most conceptually aligned with the block structure, but it
has the strongest arithmetic identification burden.  The first remains the
smallest certificate surface.

I also tested whether the small natural Lang full arc visibly comes from
ordinary Reed-Solomon projective geometry:

```text
p24/lang_projective_relation_audit.py
p24/lang_projective_relation_boundary.md
```

For `D=-13319, q=13463, pair=(7,7)`, the six dimension-3 points have no conic
relation, matching random controls.  So the natural coordinates do not show a
plain GRS/rational-normal-curve explanation.
