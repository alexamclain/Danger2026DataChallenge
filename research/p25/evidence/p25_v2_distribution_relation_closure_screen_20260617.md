# P25 v2 Distribution Relation Closure Screen

Updated: 2026-06-17

Marker: `p25_v2_distribution_relation_closure_screen_rows=1/1`

## Purpose

Test a tempting source-stage shortcut: maybe the standard distribution, norm,
or aggregate relations in the nearby Siegel/Kubert-Lang/Koo-Shin/Sprang
language already generate one legal p25 row.

They do not. In the edge basis `(m1, m2, m4, m8)`, the usual aggregate
distribution rows all have even `W`-boundary scale, while quotient relations
have boundary scale zero. Their integer closure therefore cannot produce one
boundary-`W` unit edge. A row can be reconstructed rationally only after
division by `2` or `4`, which is exactly the root/selector/scalar debt already
tracked elsewhere.

This is not a theorem-level impossibility result for all future sources. It is
a finite group-ring routing screen for the common distribution/norm relation
shapes currently in hand.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_external_distribution_relation_scout_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_distribution_relation_closure_screen_gate.py
```

The gate returned `p25_v2_distribution_relation_closure_screen_rows=1/1`.

## Edge Basis

Use the current legal edge order:

```text
(m1, m2, m4, m8)
```

The p25 source-stage target is one unit edge, for example:

```text
m1 = (1,0,0,0)
boundary scale = 1
```

## Distribution / Norm Rows

The common aggregate rows have even boundary scale:

```text
odd vertex 7H sum:      m1 + m2       boundary = 2
odd vertex 2H sum:      m4 + m8       boundary = 2
even vertex H sum:      m2 + m4       boundary = 2
even vertex 4H sum:     m1 + m8       boundary = 2
opposite diagonal:      m1 + m4       boundary = 2
opposite diagonal:      m2 + m8       boundary = 2
all-four norm:          m1+m2+m4+m8   boundary = 4
```

The quotient rows have boundary scale zero:

```text
m2 - m1
m4 - m1
m8 - m1
m1 - m4
m2 - m8
```

Therefore any integer combination of these aggregate and quotient rows has
even boundary scale. It cannot equal a unit p25 row, whose boundary scale is
`1`.

## Rational Reconstruction Debt

The same screen records the useful repair shapes:

```text
((m1 + m2) + (m1 - m2)) / 2 = m1
((m1 + m4) + (m1 - m4)) / 2 = m1
(all_four + row_sign + column_sign + C4_phase) / 4 = m1
```

These are useful normalizations, not source-stage closers by themselves. A
source must still provide an oriented root/sign, scalar-fixing value, direct
one-edge theorem, or equivalent data before the relation can enter the current
theorem kernel.

## Counts

```text
evidence_markers_ok = 5/5
distribution_generators_even_boundary = 1
zero_boundary_generators_ok = 1
integer_closure_can_have_boundary_one = 0
direct_edge_rows = 1
aggregate_or_distribution_rows = 7
zero_boundary_rows = 5
root_or_selector_repair_rows = 3
current_distribution_source_closers = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_distribution_relation_closure_screen_rows=1/1
```

## Verdict

Generic distribution, norm, vertex-sum, diagonal, all-four aggregate, and
boundary-zero quotient relations should remain support or repair rows unless a
source also supplies one of:

```text
direct arithmetic theorem for one oriented legal edge
oriented root/sign for a boundary-2 aggregate plus quotient
projector denominator/root/scalar normalization
scalar-fixed finite value/divisor/additive theorem after normalization
```

This keeps the literature route alive where it is genuinely useful, but it
prevents broad distribution-relation language from being counted as the missing
p25 source-stage theorem.
