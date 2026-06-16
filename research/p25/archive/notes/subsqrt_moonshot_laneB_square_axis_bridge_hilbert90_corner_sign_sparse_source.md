# P25 Lane B: Bridge Hilbert-90 Corner Sign-To-Sparse-Source Intake

Updated: 2026-06-13 13:45 PDT

## Purpose

This artifact connects the two-sign Hilbert-90 corner intake to the existing
Robert sparse-source bridge contract.  It lets a theorem/literature hit emit
only `eps,a`, then checks that the forced expansion lands on the exact
`C_75 x C_169` sparse triples already accepted by the raw bridge harness.

## Path

```text
eps,a
  -> row-labeled source triangle
  -> quotient corner chain
  -> Hilbert-90 first boundary
  -> inversion boundary
  -> signed S-layer bridge
  -> 25-point K-trace sparse source triples in C_75 x C_169
  -> existing Robert sparse-source bridge harness
```

## Result

All four valid sign pairs pass.  The quotient support ladder is `3 -> 4 -> 6`,
the raw sparse-source support is `150`, the sparse entries equal the recorded
target sparse entries, and the existing Robert sparse-source harness accepts
the promoted triples.

Positive and negative controls:

```text
--eps 1 --branch -1  -> pass
--eps 0 --branch 1  -> fail
```

This lowers the theorem-hit interface from a full sparse-source table to two
signs, but it does not prove the arithmetic producer.  The remaining bridge
debt is the primitive `C_169` source/trace producer that supplies the signs and
source triangle.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_sign_sparse_source_harness.py
```

Expected rows:

```text
square_axis_bridge_hilbert90_corner_sign_sparse_source_harness_rows=1/1
square_axis_bridge_hilbert90_corner_sign_sparse_source_candidate_rows=1/1
```
