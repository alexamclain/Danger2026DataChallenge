# MSRD Metric Boundary

Date: 2026-06-05

This note corrects the metric accounting in the MSRD/LRS import.

## The Finite Gate Is Metric-Agnostic

The checked gate in:

```text
p24/lean/MSRDSupportGate.lean
```

says:

```text
distance >= 55 and bad support <= 54
  => no bad nonzero word.
```

This is correct for any support weight satisfying those two hypotheses.

## What The `35+19=54` Count Means

The representative bad event has nonzero scalar coordinates only in:

```text
O4 full block + unused 19 coordinates of O1.
```

Therefore:

```text
scalar-coordinate Hamming support <= 35 + 19 = 54.
```

So the distance-55 argument is immediately valid for an ordinary scalar MDS
theorem:

```text
every 156-subset of the 210 scalar Lang coordinates is independent.
```

This is the full-arc theorem tested by:

```text
p24/lang_arc_strength_audit.py
```

## What It Does Not Mean

If the "support" is only the number of nonzero right orbit blocks, then a bad
word has support at most:

```text
2 blocks,
```

and every word has support at most:

```text
6 blocks.
```

A distance-55 theorem in that metric would force every word to be zero, since
`6 < 55`.  Lean now checks this counter-gate too:

```text
no_nonzero_word_from_distance_55_and_six_block_support
```

Thus the raw six-block support metric cannot be the MSRD metric behind the
`35+19 < 55` argument.

## Sum-Rank Route Requirement

A genuine LRS/MSRD proof remains possible only after specifying a sum-rank
model whose rank weight on the representative bad event is bounded by `54`,
not merely by two nonzero right orbits.

Concretely, the arithmetic theorem must provide:

```text
1. a blockwise expansion of the mixed trace-dual code into a sum-rank ambient
   space with total rank length 210;
2. p-unit block transformations preserving the selected erasure pattern;
3. an MSRD distance theorem in that exact metric.
```

Without those data, the only currently well-defined distance-55 strengthening
is ordinary scalar MDS/full-arc behavior.

## Consequence

The proof targets are now:

```text
selected p-unit L_rep != 0                         weakest, exact;
ordinary scalar MDS/full arc                       distance-55 works directly;
sum-rank LRS/MSRD with explicit rank expansion     possible but not yet defined.
```

This pushes the LRS/MSRD route back toward an arithmetic equivalence theorem,
not a free coding-theory citation.
