# P25 v2 Edge Lattice Intake Classifier

Updated: 2026-06-16

## Purpose

Classify integer combinations of the four quotient-`C4` source-graph edges.
The source graph normal form says that the current target is one oriented
`K_{2,2}` edge. This page records the lattice rule that prevents broader
`W`-boundary combinations from being over-counted as source-stage wins.

This is not the missing arithmetic value/divisor theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_edge_lattice_intake_classifier_gate.py
```

The gate returned `p25_v2_edge_lattice_intake_classifier_rows=1/1`.

## Lattice Rule

Use the edge order:

```text
(m1, m2, m4, m8)
```

For an integer edge combination:

```text
c1*m1 + c2*m2 + c4*m4 + c8*m8
```

the Hilbert-90 boundary scale is:

```text
(c1 + c2 + c4 + c8) * W
```

Therefore the current `W = Norm_156(Y_507)` target has coefficient sum `1`.
But coefficient sum `1` is not enough: it closes source stage only when the
vector is exactly one edge.

## Intake Decisions

```text
unit edge vector:
  condition = one coefficient is 1 and the other three are 0
  decision  = source_stage_candidate_if_theorem_present
  missing   = finite value/divisor theorem plus downstream extraction

nonzero zero-sum vector:
  condition = coefficient sum 0, vector nonzero
  decision  = repair_boundary_zero_relation
  missing   = one-edge theorem; quotient/invariant has no W boundary

W-boundary non-edge vector:
  condition = coefficient sum 1, but not a unit edge
  decision  = repair_edge_plus_boundary_zero_lattice
  missing   = finite value for the boundary-zero part or direct one-edge theorem

scaled-boundary vector:
  condition = coefficient sum not equal to 1
  decision  = repair_or_reject_scaled_boundary
  missing   = root/orientation/value normalization or rewrite to one W-boundary
              edge
```

## Meaning

Any non-edge vector with `W` boundary can be written as:

```text
one legal edge + nonzero boundary-zero lattice element
```

So a source theorem for such a vector is still repair unless it also supplies a
finite value for the boundary-zero part, an oriented root/selector, or the
direct theorem for one legal edge. This covers the common cases already seen:
edge quotients, diagonal aggregates, row-square bridges, and scaled power or
boundary statements.

## Bounded Sample Check

As a sanity check, the gate enumerated all coefficient vectors in
`{-1,0,1,2}^4`:

```text
sample_vectors = 256
legal_edge_vectors = 4
zero_boundary_nonzero_vectors = 30
W_boundary_nonedge_vectors = 36
scale_two_vectors = 44
all_W_boundary_nonedge_decompose_as_edge_plus_zero = 1
source_candidate_routes = 1
repair_or_reject_routes = 3
current_source_theorems = 0
submission_ready_rows = 0
p25_v2_edge_lattice_intake_classifier_rows=1/1
```

The bounded count is not a restriction on the rule; it is a quick check that
the intake classifier catches the small combinations most likely to appear in
source snippets or expert replies.

## Verdict

The first-pass theorem target is one edge, not merely any `W`-boundary lattice
combination. A source answer with coefficient sum `1` still needs edge
selection unless it is already a unit edge vector.
