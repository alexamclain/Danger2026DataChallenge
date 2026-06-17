# P25 v2 Q Diagonal Normalization

Updated: 2026-06-16

## Purpose

Record the projection-level selector debt behind the compact conductor-39
`Q` route.

The quotient

```text
Q = prod_{h in <2>} E_{7h}/E_h
```

has useful Hilbert-90 boundary data after powering, but its quotient-`C4`
row-antisymmetric projection does not select one legal edge. It is the diagonal
aggregate projection:

```text
Q_projection = m1 + m4 = m2 + m8
```

So a `Q` theorem is still support-only unless it supplies a boundary-zero
split/orientation, the oriented root data after a split, or a direct one-edge
finite theorem.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_diagonal_normalization_gate.py
```

The gate returned `p25_v2_q_diagonal_normalization_rows=1/1`.

## Projection Calculation

Coset order is `(H, 2H, 4H, 7H)` with `H=<3>` in `(Z/13Z)^*`.

```text
<2>  = (1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32)
7<2> = (7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38)

Q row 1 projection = (-3,  3, -3,  3)
Q row 2 projection = ( 3, -3,  3, -3)
Q row-antisym      = (-6,  6, -6,  6)
```

The four legal edge projections are:

```text
m1 = ( 0, 0, -6, 6)
m2 = (-6, 0,  0, 6)
m4 = (-6, 6,  0, 0)
m8 = ( 0, 6, -6, 0)
```

Therefore:

```text
Q_projection = m1 + m4
Q_projection = m2 + m8
```

This is a projection-level diagonal aggregate identity, not a direct statement
that `Q` is one of the support-156 legal products.

## Boundary-Zero Splits

In the edge coefficient basis `(m1,m2,m4,m8)`:

```text
diagonal m1+m4 = (1,0,1,0)
split    m1-m4 = (1,0,-1,0)
boundary sum   = 0

(m1+m4) + (m1-m4) = 2*m1
(m1+m4) - (m1-m4) = 2*m4
```

and similarly:

```text
diagonal m2+m8 = (0,1,0,1)
split    m2-m8 = (0,1,0,-1)
boundary sum   = 0

(m2+m8) + (m2-m8) = 2*m2
(m2+m8) - (m2-m8) = 2*m8
```

So a diagonal aggregate theorem plus the matching boundary-zero split reaches
twice one edge. It still needs halving/root/orientation data before it becomes
a one-edge theorem at value level.

## Routes

```text
q_diagonal_value_only
  decision = support_diagonal_aggregate_selector_missing
  missing  = boundary-zero split/orientation data or direct one-edge theorem

q_plus_m1_m4_or_m2_m8_quotient_value
  decision = repair_oriented_square_root_missing
  missing  = halving/root/orientation data after reaching twice one edge

q_plus_explicit_oriented_diagonal_split
  decision = normalize_to_one_edge_then_apply_source_snippet_intake
  missing  = source-snippet intake and downstream extraction after scalar-fixed
             theorem

q_plus_direct_one_edge_theorem
  decision = source_stage_candidate_if_scalar_fixed_theorem_present
  missing  = DANGER3 framing and extraction after theorem hit

q6_boundary_only
  decision = repair_additive_or_value_normalization_missing
  missing  = scalar-fixed finite value/additive data plus selector, not just
             Hilbert-90 boundary

wrong_same_parity_or_zero_boundary_split
  decision = reject_zero_boundary_wrong_edge
  falsifier = split data must recover one of m1,m2,m4,m8 with the current
              oriented boundary
```

## Counts

```text
evidence_markers_ok = 6/6
diagonal_equalities = 2
boundary_zero_splits = 2
source_candidate_routes = 1
support_routes = 1
normalize_routes = 1
repair_rows = 2
reject_rows = 1
current_source_theorems = 0
p25_v2_q_diagonal_normalization_rows=1/1
```

## Verdict

The `Q` route is stronger than a generic boundary-only answer, but it is still
not a source-stage close. Its quotient-`C4` projection is the diagonal
aggregate `m1+m4=m2+m8`, so a `Q` value theorem needs one more piece:

```text
boundary-zero split + oriented root
or explicit oriented diagonal split normalization
or direct one-edge finite value/divisor theorem
```

This is the cleanest current way to ask about `Q`: it is a compact support
object and a possible normalization route, not a replacement for the one-edge
theorem.
