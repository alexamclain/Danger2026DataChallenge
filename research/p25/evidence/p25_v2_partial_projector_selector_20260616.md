# P25 v2 Partial Projector Selector

Updated: 2026-06-16

## Purpose

Classify two-edge and half-projector source answers. This is the intermediate
case between a one-edge theorem and the full projector-denominator screen:
row-pair, column-pair, or diagonal-pair data can narrow the target, but it
still does not select one oriented edge.

This is not the missing value/divisor theorem. It is an intake screen for
source snippets that prove a pair aggregate, a pair difference, or a doubled
edge.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_edge_projector_denominator_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_partial_projector_selector_gate.py
```

The gate returned `p25_v2_partial_projector_selector_rows=1/1`.

## Edge Basis

Use the edge order:

```text
(m1, m2, m4, m8)
```

The six two-edge selectors are:

```text
odd_row_pair      = m1 + m2    boundary = 2W
even_row_pair     = m4 + m8    boundary = 2W
right_column_pair = m1 + m8    boundary = 2W
left_column_pair  = m2 + m4    boundary = 2W
diagonal_pair_a   = m1 + m4    boundary = 2W
diagonal_pair_b   = m2 + m8    boundary = 2W
```

Every pair difference has boundary zero:

```text
m_i - m_j    boundary = 0
```

For each pair `{a,b}`, pair aggregate plus pair difference reaches a doubled
edge:

```text
(a + b) + (a - b) = 2a
(a + b) - (a - b) = 2b
```

So pair data plus quotient/difference data can at best reach `2*edge` before
additional root/orientation information is supplied.

## P25 Root Data

```text
p mod 2 = 1
gcd(2, p - 1) = 2
```

Thus a doubled-edge or square-value theorem still has a sign/root ambiguity in
`F_p^*`. It must name the oriented root or prove the one-edge theorem directly.

## Accepted Routes

```text
direct_one_edge_theorem
  decision = source_stage_candidate_if_theorem_present

pair_plus_difference_with_oriented_square_root
  decision = normalize_oriented_root_then_intake
```

## Repair Routes

```text
two_edge_pair_aggregate_only
  decision = repair_2W_boundary_not_one_edge

pair_difference_only
  decision = repair_zero_boundary_selector_missing

pair_plus_difference_without_square_root
  decision = repair_sign_or_root_missing

complement_pair_choice_only
  decision = repair_pair_selector_not_edge_selector
```

## Counts

```text
evidence_markers_ok = 5/5
two_edge_pairs = 6
pair_boundary_scales_ok = 6/6
difference_boundary_scales_ok = 6/6
doubled_edge_identities_ok = 6/6
accepted_routes = 2
repair_routes = 4
current_source_theorems = 0
current_submission_ready = 0
p25_v2_partial_projector_selector_rows=1/1
```

## Verdict

A two-edge theorem is still a repair row. It either has boundary `2W`, has
zero boundary as a selector/difference, or reaches a doubled edge that needs an
oriented square root. The source-stage close remains a theorem for one
oriented edge, or an explicitly normalized route that selects that edge.
