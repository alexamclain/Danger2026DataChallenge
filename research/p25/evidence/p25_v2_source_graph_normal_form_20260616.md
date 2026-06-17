# P25 v2 Source Graph Normal Form

Updated: 2026-06-16

## Purpose

Compress the H0/conductor-39 source side into one graph normal form. The
self-contained theorem statement fixes the finite product rows; this page
states the source-side shape those rows have to preserve.

This is not the missing arithmetic value/divisor theorem. It is an intake
surface for source snippets and expert answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_quotient_h90_idempotent_mechanism_20260616.md`
- `evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_source_graph_normal_form_gate.py
```

The gate returned `p25_v2_source_graph_normal_form_rows=1/1`.

## Graph

Let:

```text
H = (1,3,9)
odd quotient-C4 vertices  = 2H=(2,5,6), 7H=(7,8,11)
even quotient-C4 vertices = H=(1,3,9), 4H=(4,10,12)
```

The four legal source rows are exactly the four edges of the complete bipartite
graph `K_{2,2}` from odd vertices to even vertices:

```text
m=1: 7H -> 4H
m=2: 7H -> H
m=4: 2H -> H
m=8: 2H -> 4H
```

Each edge is a signed `C_3 x C_13` column matching, lifts to one support-156
level-507 product row, and has Hilbert-90 boundary `W = Norm_156(Y_507)`.

## Verified Edge Payloads

```text
m=1
edge = 7H -> 4H
sha256 = eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e

m=2
edge = 7H -> H
sha256 = 97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9

m=4
edge = 2H -> H
sha256 = 28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6

m=8
edge = 2H -> 4H
sha256 = ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

## Source-Theorem Routing

The source-stage candidate is:

```text
one oriented K_{2,2} edge
+ finite divisor/additive theorem with scalar normalization
  or support-period-156 value theorem
+ boundary W = Norm_156(Y_507)
```

The following are useful context but not source-stage wins:

```text
opposite-edge diagonal aggregate:
  m1*m4 = m2*m8
  boundary = 2W
  missing = selector/factorization down to one W-boundary edge

edge quotient only:
  boundary = 0
  missing = one-edge value/divisor theorem

aggregate plus quotient:
  reaches a row square
  missing = oriented root or direct one-edge theorem

vertex projection or one-coset statement:
  loses the mixed signed-column fingerprint
  decision = reject for current target
```

## Why This Helps

The literature/expert ask can now be phrased without the artifact forest:

```text
Is there a finite arithmetic theorem for one oriented edge of this quotient-C4
K_{2,2} graph, with Hilbert-90 boundary Norm_156(Y_507)?
```

This avoids three common drifts:

```text
asking for a broad quadratic-character aggregate,
accepting a boundary-zero quotient as if it were the row,
or accepting a projection / one-coset theorem that loses the mixed tensor.
```

## Verified Counts

```text
evidence_markers_ok = 5/5
legal_edges_ok = 4/4
edge_graph_is_k22 = 1
opposite_edge_pairs = ((1,4),(2,8))
adjacent_edge_pairs = ((1,2),(1,8),(2,4),(4,8))
diagonal_aggregates_ok = 1/1
quotient_bridges_ok = 1/1
source_candidate_routes = 1
repair_or_reject_routes = 4
current_source_theorems = 0
submission_ready_rows = 0
p25_v2_source_graph_normal_form_rows=1/1
```

## Verdict

The first-pass source object is best viewed as one oriented edge of a
quotient-`C4` `K_{2,2}` graph. A theorem for an edge can close source stage; a
theorem for a vertex, projection, quotient, diagonal, row square, or all-four
aggregate still needs repair data before it becomes a p25 certificate route.
