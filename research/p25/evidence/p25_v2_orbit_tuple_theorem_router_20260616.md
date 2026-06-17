# P25 v2 Orbit Tuple Theorem Router

Updated: 2026-06-16

## Purpose

Distinguish a theorem for the whole four-row doubling orbit from a symmetric
orbit aggregate. The first-pass target is one oriented edge. A row-labeled
theorem for all four legal rows contains a one-edge theorem and should be
promoted; an unordered set, product, trace, norm, diagonal pair, or quotient
still lacks the selector/root/scalar data needed for one edge.

This is not the missing arithmetic theorem. It is an intake rule for expert
answers that naturally state a theorem for an orbit rather than for one row.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_partial_projector_selector_20260616.md`
- `evidence/p25_v2_positive_theorem_clause_matcher_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_orbit_tuple_theorem_router_gate.py
```

The gate returned `p25_v2_orbit_tuple_theorem_router_rows=1/1`.

## Exact Orbit Rows

The legal orbit is row-labeled by multiplier, quotient-`C4` edge, and stable
row hash:

```text
m=1  edge=7H -> 4H  sha256=eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e
m=2  edge=7H -> H   sha256=97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9
m=4  edge=2H -> H   sha256=28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6
m=8  edge=2H -> 4H  sha256=ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

Each row has boundary `Norm_156(Y_507)`. One labeled row is enough for source
stage if it comes with the scalar-fixed finite value/divisor theorem or a
support-period-156 value theorem.

## Accepted Orbit Outputs

These are source-stage candidates if the arithmetic theorem and scalar/value
normalization clauses are present:

```text
single_labeled_edge_divisor_additive
  output   = one row m with hash or edge label
  decision = source_stage_candidate_if_arithmetic_source_theorem

row_labeled_four_edge_divisor_additive_tuple
  output   = four scalar-fixed divisor/additive identities labeled by m
  decision = choose any labeled row, then route to extraction contract

row_labeled_four_edge_period156_value_tuple
  output   = four period-156 values labeled by row, with branch/root context
  decision = choose any labeled row, then route to extraction contract

parametric_doubling_orbit_theorem
  output   = uniform theorem for m in {1,2,4,8}
  decision = normalize m, then apply the positive clause matcher
```

This is the useful correction to the "one row is enough" rule: do not
over-demand all four rows, but also do not reject a theorem merely because it
states all four labeled rows.

## Repair Or Reject Orbit Outputs

These are not source-stage wins without extra data:

```text
unordered_four_values_no_row_labels
  decision = repair_row_labeling_missing
  missing  = assignment to one exact oriented edge R_m

symmetric_all_four_product_or_norm
  decision = repair_oriented_edge_selection_missing
  missing  = selected fourth root/scalar data or direct row-labeled theorem

diagonal_or_pair_tuple_only
  decision = repair_square_root_or_pair_selector_missing
  missing  = oriented square root or direct one-edge theorem

row_quotient_or_boundary_zero_tuple
  decision = repair_one_edge_value_missing
  missing  = finite value/divisor theorem for one W-boundary edge

orbit_source_legality_only
  decision = repair_finite_theorem_missing
  missing  = scalar-fixed finite value/divisor theorem

orbit_values_up_to_scalar
  decision = repair_scalar_normalization_missing
  missing  = finite additive/value/basepoint/branch/telescoping normalization

outside_doubling_orbit_tuple
  decision = reject_not_current_legal_four_row_target
  falsifier = row orbit normalization fixes the legal representatives
```

## Counts

```text
evidence_markers_ok = 6/6
row_payloads_ok = 4/4
accepted_routes = 4
repair_rows = 6
reject_rows = 1
current_source_theorems = 0
current_submission_ready = 0
p25_v2_orbit_tuple_theorem_router_rows=1/1
```

## Verdict

A row-labeled orbit theorem is a positive theorem shape because it contains
one exact oriented edge theorem. A symmetric orbit theorem is a repair row
because it lands on an aggregate and still needs row labeling, root/scalar
selection, or a direct one-edge theorem.

Continue H0/conductor-39 first-pass work through this route only when the
output is row-labeled and theorem-shaped. Kill orbit aggregate leads that do
not select one legal edge.
