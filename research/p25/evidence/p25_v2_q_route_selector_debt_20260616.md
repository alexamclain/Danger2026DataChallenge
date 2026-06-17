# P25 v2 Q Route Selector Debt

Updated: 2026-06-16

## Purpose

Classify what the compact conductor-39 `Q` route does and does not buy us.
The quotient

```text
Q = prod_{h in <2>} E_{7h}/E_h
```

is a useful norm-one value object because `Frob_p(Q)=Q^-1` and
`Q^6=(1-Frob_p)(Q^3)` has the current `W` boundary. But `Q` boundary data is
still downstream of the quotient-`C4` edge selector. This page records the
remaining selector debt.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md`
- `evidence/p25_v2_frobenius_tensor_eigenboundary_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_route_selector_debt_gate.py
```

The gate returned `p25_v2_q_route_selector_debt_rows=1/1`.

## Invariants

```text
q_boundary_is_current_w
  Q^6=(1-Frob_p)(Q^3) has the current W boundary, but Q route source theorems
  are still zero.

frobenius_erases_edge_phase
  The Hilbert-90 boundary map kills the order-4 C4 selector phases for all
  four legal rows.

one_edge_is_the_intake_target
  The edge lattice has exactly one source-candidate intake route: a unit edge
  vector.

expert_ask_has_q_near_misses
  The minimal expert ask now includes Q support rows and Q repair/reject rows.
```

## Routes

```text
q_value_period156_context_only
  decision = support_route_selector_debt_remains
  missing  = edge-selecting order-4 C4 phase, boundary-zero value, or direct
             one-edge theorem

q3_h90_preimage_finite_theorem_only
  decision = support_route_selector_debt_remains
  missing  = theorem data that recovers one oriented quotient-C4 edge before
             source-stage promotion

q_with_order4_selector_and_finite_edge_theorem
  decision = source_stage_candidate_if_scalar_fixed_theorem_present
  missing  = DANGER3 framing and extraction after theorem hit

q_plus_boundary_zero_value_or_selector
  decision = normalize_to_one_edge_then_apply_source_snippet_intake
  missing  = same theorem data after subtracting the boundary-zero lattice
             content or selecting one edge

q_source_or_coset_selector_only
  decision = repair_finite_value_divisor_theorem_missing
  missing  = finite value/divisor theorem for Q, Q^3, Q^6, or the selected
             Yang lift

q6_boundary_only
  decision = repair_additive_or_value_normalization_missing
  missing  = scalar-fixed finite value/additive data plus edge selector, not
             just Hilbert-90 boundary

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels
  falsifier = Frobenius alternation makes the degree-6 norm zero
```

## Counts

```text
evidence_markers_ok = 5/5
invariants_ok = 4/4
source_candidate_routes = 1
support_routes = 2
normalize_routes = 1
repair_rows = 2
reject_rows = 1
current_source_theorems = 0
p25_v2_q_route_selector_debt_rows=1/1
```

## Verdict

The compact `Q` route is a good support route, not a free source-stage close.
A `Q` value theorem with period-156 context or a finite theorem for `Q^3`
still owes selector data unless it also recovers one oriented quotient-`C4`
edge, supplies the boundary-zero value needed to normalize to one edge, or
directly proves the one-edge finite value/divisor theorem.

This is the expert-facing caution: ask for `Q`/`Q^3` theorem data, but do not
count boundary-visible `Q` data as a p25 source theorem until the order-4
selector debt has been paid.
