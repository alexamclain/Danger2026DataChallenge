# P25 v2 Source Theorem Acceptance Automaton

Updated: 2026-06-17

Marker: `p25_v2_source_theorem_acceptance_automaton_rows=1/1`

## Purpose

Make the current theorem kernel executable as an intake decision table. If an
expert answer, source snippet, or proof attempt arrives with row product,
power, divisor, value, Q/Yang, projector, aggregate, or exact-P language, this
automaton classifies the minimum missing clause before H0 or conductor 39 lane
status changes.

This is not a source theorem. It is a stricter front-door classifier for
theorem-shaped replies.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_priority1_clause_necessity_matrix_20260617.md`
- `evidence/p25_v2_conductor39_row_binding_overlay_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_self_contained_theorem_statement_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_distribution_relation_closure_screen_20260617.md`
- `evidence/p25_v2_matched_quotient_closure_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_source_theorem_acceptance_automaton_gate.py
```

The gate returned `p25_v2_source_theorem_acceptance_automaton_rows=1/1`.

## Accept Rows

```text
direct_m1_divisor_additive
  decision = accept_direct_row_divisor_additive
  clauses  = legal row, arithmetic source theorem, finite payload,
             Norm_156(Y_507) boundary, scalar/additive normalization

m2_unique_power_e
  decision = accept_via_row_labeled_unique_power
  clauses  = row label, exact finite source theorem for R_m^e with
             e in {3,5,13,39,75,169,507}, gcd(e, p-1)=1, boundary,
             scalar normalization

m4_period156_value
  decision = accept_via_support_period156_value
  clauses  = support-period-156 row value, arithmetic source theorem,
             branch/root/telescoping or additive normalization, boundary
```

## Normalize Or Route Rows

```text
q_yang_selector_paid_to_m8
  decision = normalize_q_yang_support_then_accept
  reason   = Q/Yang support is acceptable only after selector debt is paid and
             it lands on one stable legal row with finite theorem data

matched_quotient_unit_power_to_m1
  decision = normalize_matched_quotient_then_accept
  reason   = aggregate theorem plus exact matched zero-lattice quotient theorem
             with invertible coefficient sum recovers one row power

exactp_theta2_packet
  decision = route_exactp_theta2_heavy_upstream
  reason   = accepted exact-P/theta2 packets remain the heavy upstream route,
             not a first-pass shortcut
```

## Repair Or Reject Rows

```text
conductor39_rowless_mixed_packet  -> repair_row_binding_missing
aggregate_without_matched_quotient -> repair_zero_lattice_value_missing
matched_quotient_nonunit_sum      -> repair_root_debt_remaining
boundary_only_h90_statement       -> repair_finite_payload_missing
finite_payload_without_source     -> repair_arithmetic_source_theorem_missing
ambient_period780_value           -> repair_period156_branch_missing
q_diagonal_without_split           -> repair_selector_debt_unpaid
projector_without_fourth_root      -> repair_selector_debt_unpaid
all_four_orbit_aggregate           -> repair_row_selection_missing
distribution_norm_closure_even_boundary -> repair_even_boundary_distribution_closure
row_power_23                       -> repair_nonunique_power_root
prime_axis_projection              -> reject_lost_mixed_tensor
reciprocal_positive_boundary       -> reject_wrong_boundary_sign
```

## Counts

```text
evidence_markers_ok = 10/10
legal_row_hashes_bound = 4/4
candidate_rows = 25
accepted_source_stage_rows = 9
normalize_then_accept_rows = 2
heavy_upstream_rows = 1
repair_rows = 11
reject_rows = 2
invertible_power_rows = 7
noninvertible_power_rows = 1
matched_quotient_rows = 3
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_source_theorem_acceptance_automaton_rows=1/1
```

## Verdict

The live theorem gap is now one of three accepted first-pass forms:

```text
1. scalar-fixed finite divisor/additive theorem for one stable row;
2. row-labeled uniquely invertible power theorem for one stable row and
   `e in {3,5,13,39,75,169,507}`;
3. support-period-156 value theorem with row bridge and branch normalization.
```

Q/Yang data can help only after it normalizes to one row. Aggregate row-product
data can help only in the matched-quotient packet form: exact `R^v`, exact
`R^(v - (sum v)e_m)`, and `gcd(sum v,p-1)=1`. Exact-P/theta2 data stays the
heavy upstream route. Everything else is a named repair or reject state until
it supplies the missing row, source theorem, finite payload, boundary,
scalar/branch normalization, selector/root data, or direct-edge escape from
the even-boundary distribution/norm closure.
