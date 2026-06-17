# P25 v2 K22 Automorphism Quotient Falsifier

Updated: 2026-06-16

Marker: `p25_v2_k22_automorphism_quotient_falsifier_rows=1/1`

## Purpose

Classify what happens when a source theorem is stated only up to a nontrivial
symmetry of the four-edge quotient-`C4` `K_{2,2}` source graph. The first-pass
target is one oriented edge. A row-labeled theorem for all four edges is useful
because it contains a theorem for one row; an automorphism-invariant quotient
or aggregate is not enough.

This is not the missing arithmetic theorem. It is a falsifier for plausible
near-misses in H0/conductor-39 source answers.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_orbit_tuple_theorem_router_20260616.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_k22_automorphism_quotient_falsifier_gate.py
```

The gate returned `p25_v2_k22_automorphism_quotient_falsifier_rows=1/1`.

## Graph Symmetry Model

The legal source graph is:

```text
m=1: 7H -> 4H
m=2: 7H -> H
m=4: 2H -> H
m=8: 2H -> 4H
```

The oriented bipartite graph has the side-preserving symmetry group
`S_2 x S_2`, represented by identity, row swap, column swap, and simultaneous
row/column swap.

## Quotient Rows

```text
identity_singletons
  orbits = {m1} {m2} {m4} {m8}
  product boundary scales = 1,1,1,1
  decision = promote only if one row has the scalar-fixed finite theorem

row_swap_pairs
  orbits = {m1,m8} {m2,m4}
  product boundary scales = 2,2
  decision = repair: two-edge selector or square root missing

column_swap_pairs
  orbits = {m1,m2} {m4,m8}
  product boundary scales = 2,2
  decision = repair: two-edge selector or square root missing

diagonal_pairs
  orbits = {m1,m4} {m2,m8}
  product boundary scales = 2,2
  decision = repair: diagonal selector or oriented root missing

full_k22_symmetry
  orbits = {m1,m2,m4,m8}
  product boundary scale = 4
  decision = repair: fourth root, scalar, or row labeling missing
```

For quotient relations inside any nontrivial orbit, the boundary scale is
zero. That can be useful support data, but it still does not provide a
scalar-fixed `W`-boundary edge value.

## Intake Rule

Accept only:

```text
identity_or_row_labeled_singleton
  shape = one oriented edge, or a row-labeled theorem containing one singleton edge
  decision = source-stage candidate if the arithmetic theorem and scalar data are present
```

Repair:

```text
row_or_column_pair_orbit
  missing = oriented square root, selected edge, or direct one-edge theorem

diagonal_pair_orbit
  missing = factorization/root down to one W-boundary edge

all_four_orbit
  missing = selected fourth root/scalar data or direct row-labeled theorem

unlabeled_four_tuple
  missing = assignment to one exact oriented edge R_m

automorphism_invariant_value_only
  missing = row-antisymmetric C4 phase, mixed tensor sign, and scalar-fixed theorem
```

Reject:

```text
orientation_reversing_or_vertex_projection_symmetry
  falsifier = the oriented mixed signed-column edge is not preserved
```

## Counts

```text
evidence_markers_ok = 6/6
automorphism_group_order = 4
subgroup_rows = 5
nontrivial_subgroups = 4
nontrivial_singleton_orbits = 0
accepted_routes = 1
repair_routes = 5
reject_routes = 1
current_source_theorems = 0
current_submission_ready = 0
p25_v2_k22_automorphism_quotient_falsifier_rows=1/1
```

## Verdict

No nontrivial automorphism quotient of the legal `K_{2,2}` source graph
selects one legal p25 edge. Nontrivial orbit products have `2W` or `4W`
boundary, and orbit quotients have zero boundary. They are support or repair
data, not first-pass closers.

Continue H0/conductor-39 work only when the theorem is row-labeled or directly
selects one oriented edge. Kill symmetry-quotient leads unless they also supply
the missing root/scalar/selector data or a direct one-edge finite theorem.
