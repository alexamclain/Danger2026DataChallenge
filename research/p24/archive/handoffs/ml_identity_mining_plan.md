# ML / Probability Identity-Mining Plan

Date: 2026-06-05

This note records how CS/ML/probability can still help the p24 proof search
without becoming a heuristic substitute for a certificate.

## Rule

Use learning only to rank exact algebraic objects.  A successful output must
graduate to one of:

```text
finite-field identity;
Moore determinant p-unit;
cyclic/exterior resultant formula;
class-field norm/product theorem;
explicit anti-annihilator incidence lemma.
```

Prediction accuracy, random-model failure probability, or low empirical loss
is not a certificate for `p = 10^24 + 7`.

## Experiments Worth Running

1. Seven-orbit product relation miner.

Target the seven factors:

```text
F(0),  prod_{t in O_j} F(t), j=1..6.
```

Build an exact invariant dictionary on small actual-CM rows:

```text
unit-2 symmetric products;
inversion-paired products;
cyclic resultant pieces;
exterior Plucker norms;
trace and centered-marginal scalars.
```

Then use modular nullspaces or integer-relation reconstruction to search for
polynomial or multiplicative relations that verify on held-out CM rows.
Success means a relation of the form:

```text
G(seven orbit products) = Norm(explicit CM/resolvent expression),
```

not merely a predictor.

2. CM-adapted basis search.

The natural exterior DFT is dense; see:

```text
p24/centered_marginal_exterior_dft_boundary.md
```

So the useful search is for a better arithmetic coordinate system, restricted
to rule-defined bases:

```text
Frobenius-normal bases;
trace-dual bases;
unit-2 equivariant bases;
inversion-compatible Lang bases;
small CM-derived basis changes.
```

Rank basis families by exact outcomes: subfield degree, norm factorization,
equivariant equality up to units, or reduction to known nonzero Moore pieces.

3. Lang tuple subspace-polynomial pivot miner.

For the 210 Lang-trivialized mixed coordinates, mine pivot orders and residual
norm products in the incremental linearized-polynomial update.  The most
important target is the `140 + 16` prefix/tail split:

```text
four full right blocks leave a 16-dimensional residual kernel;
the first 16 coordinates of the fifth block must be injective on it.
```

Success means an explicit representative Moore p-unit:

```text
L_rep = B_rep * T_rep,
```

or a stable delete-one subspace-polynomial identity.

First implementation:

```text
p24/lang_pivot_order_miner.py
p24/lang_pivot_order_mining_boundary.md
p24/lang_tail_shape_index.py
p24/lang_tail_shape_index_boundary.md
```

It confirms the exact leading/residual product behavior on pinned small
actual-CM rows and compares right-orbit orderings.  The shape index should be
used to find hand-picked candidate rows before running the heavier miner; the
bounded shape searches so far found no small genuine tail analogue.

4. Trace-intersection failure-mode miner.

Generate exact small controls with planted low-degree linearized annihilators,
then compare them with actual-CM rows.  Use clustering only to propose
structured failure divisors.  Keep only exact algebraic statements such as:

```text
any failure forces one of these Frobenius-stable incidence divisors.
```

The p24 proof would then be a p-unit/nonmembership check for the actual six
mixed periods.

## Ideas To Avoid

The upstream `DANGER3` data under:

```text
p24/upstream_DANGER3/
```

contains Montgomery Pomerance triples and prefixes.  It is useful for
calibrating the original search problem, but it does not expose the CM fibers
or class-character periods used in the current centered marginal theorem.
Training directly on those triples is therefore unlikely to prove the p24 CM
rank certificate.

Also avoid:

```text
low Fourier support / low recurrence for the right determinant sequence;
random-subspace probability as a proof;
generic neural prediction of successful minors.
```

The local audits already found full DFT support, full Berlekamp-Massey
complexity, and random-looking arc behavior in the natural coordinates.  The
remaining learning-assisted route is exact identity discovery.
