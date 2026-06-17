# P25 v2 Edge Projector Denominator

Updated: 2026-06-16

## Purpose

Record the projector decomposition of the quotient-`C4` `K_{2,2}` edge space.
This screen explains why many character-component or aggregate source
statements naturally land on `4 * edge` or boundary-zero pieces, not on one
selected edge. For p25, recovering one edge from projector data requires
explicit fourth-root/scalar selection.

This is not the missing value/divisor theorem. It is a routing screen for
source or expert answers stated in character/projector language.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_edge_projector_denominator_gate.py
```

The gate returned `p25_v2_edge_projector_denominator_rows=1/1`.

## Edge Basis

Use the edge order:

```text
(m1, m2, m4, m8)
```

with the quotient-`C4` source graph:

```text
m1: 7H -> 4H
m2: 7H -> H
m4: 2H -> H
m8: 2H -> 4H
```

## Projector Basis

```text
constant     = ( 1,  1,  1,  1)   boundary = 4W
odd_row      = ( 1,  1, -1, -1)   boundary = 0
even_column  = ( 1, -1, -1,  1)   boundary = 0
checkerboard = ( 1, -1,  1, -1)   boundary = 0
```

The four exact identities are:

```text
4*m1 = constant + odd_row + even_column + checkerboard
4*m2 = constant + odd_row - even_column - checkerboard
4*m4 = constant - odd_row - even_column + checkerboard
4*m8 = constant - odd_row + even_column - checkerboard
```

So a theorem for projector components is naturally a theorem for `4 * edge`,
plus boundary-zero selector components, not automatically a theorem for one
edge.

## P25 Root Data

```text
p mod 4 = 1
gcd(4, p - 1) = 4
```

Thus the fourth-power map on `F_p^*` has a four-element kernel. If an answer
proves a fourth-power value, or reconstructs an edge only after dividing the
projector identity by `4`, it still needs an explicit root/scalar/orientation
selector before source-snippet intake can promote it.

## Accepted Routes

```text
direct_one_edge_theorem
  decision = source_stage_candidate_if_theorem_present

projector_theorem_with_explicit_fourth_root
  decision = normalize_selected_root_then_intake
```

## Repair Routes

```text
constant_component_only
  decision = repair_all_four_or_4W_boundary_not_one_edge

row_or_column_component_only
  decision = repair_boundary_zero_selector_missing

checkerboard_component_only
  decision = repair_boundary_zero_selector_missing

all_projector_values_without_root
  decision = repair_mu4_root_or_scalar_missing

fourth_power_value_only
  decision = repair_mu4_root_selection_missing
```

## Counts

```text
evidence_markers_ok = 4/4
projector_identities_ok = 4/4
accepted_routes = 2
repair_routes = 5
current_source_theorems = 0
current_submission_ready = 0
p25_v2_edge_projector_denominator_rows=1/1
```

## Verdict

Character/projector language can be useful only if it comes with an explicit
selected fourth root or a direct theorem for one oriented edge. Otherwise it is
a repair route: the constant component has boundary `4W`, while the other
projector components have boundary zero, and p25 has real `mu_4` ambiguity when
recovering an edge from `4 * edge`.
