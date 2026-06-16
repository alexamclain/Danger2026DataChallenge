# Lang Block-Subspace Design Boundary

Date: 2026-06-05

This note records a CS-theory refinement of the representative p24 p-unit
surface.

## Candidate Import

The p24 representative row can be viewed as an array-code/subspace-design
statement.  The six right Frobenius orbits give six blocks

```text
W_1,...,W_6 subset L = F_p(mu_157),
dim W_j <= 35.
```

The representative certificate keeps

```text
O2,O3,O5,O6 full blocks + first 16 coordinates of O1.
```

So a support-specific CS theorem would be:

```text
span(O2,O3,O5,O6) has dimension 140,
and O1 contributes 16 dimensions modulo that prefix.
```

This is weaker than ordinary scalar MDS/full-arc behavior and weaker than a
global LRS/MSRD equivalence.  It is exactly the `B_rep*T_rep` theorem in
block-subspace language.

The finite p24 implication is now explicit in:

```text
p24/lean/MixedSubspacePolynomialGate.lean
```

Lean checks the numerical representative gate:

```text
prefixRank = 4*35, tailAug = 16
=> FullSpan leadingRank 156.
```

## Tool

Added:

```text
p24/lang_block_subspace_design_audit.py
```

It reuses the actual CM/Lang construction and measures:

```text
rank of every right-block subset;
whether block-subset ranks equal min(left_len, total block length);
canonical delete-one full-block prefix rank;
canonical tail rank gain;
random block controls with the same block lengths.
```

This is intentionally narrower than full scalar subset enumeration.  It tests
the array-code theorem shape directly.

## Pinned Actual-CM Runs

For the known `D=-13319` row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_block_subspace_design_audit.py \
  --only-D -13319 --only-q 13463 --q-start 13463 --q-stop 13464 \
  --only-m 28 --include-linear --max-factor-degree 8 \
  --max-extension-degree 8 --min-left-orbit-len 3 \
  --random-trials 200 --max-rows 8
```

reported four rows.  The two `(7,7)` rows have:

```text
right_lengths=[3,3]
rank=3/3
block_generic=3/3
delete tails are length 0
random_block_generic=200/200
random_delete_tail=200/200.
```

The two `(7,4)` rows have:

```text
right_lengths=[2,1]
rank=3/3
block_generic=3/3
no delete-one kept capacity reaches left_len
random_block_generic=200/200.
```

For the known `D=-5444` row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/lang_block_subspace_design_audit.py \
  --only-D -5444 --only-q 2657 --q-start 2657 --q-stop 2658 \
  --only-m 12 --include-linear --max-factor-degree 8 \
  --max-extension-degree 8 --min-left-orbit-len 2 \
  --random-trials 200 --max-rows 12
```

reported:

```text
right_lengths=[1,1,1]
rank=2/2
block_generic=7/7
delete-one leading full for all omissions
random_block_generic=200/200
random_delete_tail=200/200.
```

These are positive sanity checks for the block theorem, but they are not
special: the random controls succeed at the same rate.

## Shape Candidate Check

A cheap shape-only search again found the known `D=-26519` family:

```text
D=-26519 h=240 q in {293,373,...} m=48 n=5
left=16:L4
right=16:orbits[4,2,4,1,2,1,1]
tails=1/7
tail_range=0..2.
```

But the actual-CM block audit on pinned `q=293` and `q=373` reported:

```text
rows=0.
```

So this family remains a shape-only false positive; it does not currently give
a genuine full-block-plus-tail CM analogue.

## Consequence

The block-subspace design import is a good theorem language:

```text
prove the actual six CM right-block subspaces are in the required
support-specific general position.
```

But the small data does not expose a special finite-geometric identity beyond
generic rank behavior.  The p24 proof still needs one of:

```text
1. a selected support subspace-polynomial p-unit identity;
2. a metric-preserving LRS/MSRD equivalence with the correct scalar support;
3. an arithmetic intersection theorem for L cap span_R{S_j}^perp = {0}.
```

In other words, CS theory has sharpened the exact theorem to prove; it has
not removed the arithmetic nonvanishing step.
