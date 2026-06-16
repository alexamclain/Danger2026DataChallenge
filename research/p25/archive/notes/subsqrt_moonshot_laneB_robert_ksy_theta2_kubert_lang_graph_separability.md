# P25 Lane B: Robert KSY Kubert-Lang Graph Separability

Updated: 2026-06-13 17:41 PDT

## Purpose

The graph row-law gate killed the hope that the `C_169` projection plus
Kubert-Lang congruences selects the p25 row graph.  This gate checks the next
tempting shortcut: apply a row-only character, mask, or phase to the `C_169`
projection to recover the base-row anchor.

## Target Matrix

Columns are `25,28,31,138,141,144`.

```text
row 0: 0 0 1 -1 0 0
row 1: 1 0 0 0 -1 0
row 2: 0 1 0 0 0 -1
```

```text
target rank          = 3
target row sums      = 0,0,0
target column sums   = 1,1,1,-1,-1,-1
C_169 projection     = 1,1,1,-1,-1,-1
```

## Row-Only Shortcut Scan

Every nonempty row mask was multiplied by the `C_169` projection vector.

```text
row-only masks scanned = 7
support counts         = support 6: 3, support 12: 3, support 18: 1
rank counts            = rank 1: 7
source contract hits   = 0
```

Thus a separated row factor times the `C_169` projection is always rank `1`
and always fails the source-packet contract.

## Positive Remaining Shape

The target is exactly three row-labeled anti-invariant pairs:

```text
row 0: c31 - c138
row 1: c25 - c141
row 2: c28 - c144
```

This is the next theorem-shaped payload: an exact Kubert-Lang/Siegel/Robert
formula must supply a genuinely mixed row-C graph, or directly produce these
three row-labeled anti-invariant pairs.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_graph_separability_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_graph_separability_rows=1/1
```

## Interpretation

The row anchor is not a standalone row character, row mask, or phase applied
after a prime-power `C_169` selector.  Any surviving theorem route must explain
the mixed graph itself.
