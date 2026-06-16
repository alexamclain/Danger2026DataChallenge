# P25 KSY-y Priority-1 Divisor/Additive Intake

Updated: 2026-06-14 22:19 PDT

## Purpose

This is the unified intake for the first source-facing ask selected by the
priority selector: exact divisor/additive identities with legal Hilbert-90
boundary.  It composes the existing conductor-`39`, H0, twisted/H90, and
curved-corner classifiers.

It does not claim a theorem has been found.  It records how a future theorem
snippet, expert answer, or source-search result should be routed.

## Closing Rows

These rows would close the source stage if supplied by a real arithmetic
source theorem:

```text
h0_legal_divisor_boundary_identity:
  lane     = H0/H0_translate
  decision = source_theorem_closed_policy_or_framing_missing
  need     = exact legal H0 product plus Hilbert-90 boundary

conductor39_legal_divisor_identity:
  lane     = conductor39
  decision = source_theorem_closed_policy_or_framing_missing
  need     = legal mixed conductor-39 source, Yang lift, and descent

twisted_h90_divisor_with_period_bridge_context:
  lane     = twisted/H90
  decision = source_theorem_closed_policy_or_framing_missing
  need     = finite divisor/additive theorem plus current period-156 bridge context

curved_corner_divisor_with_period156_context:
  lane     = curved_corner
  decision = source_theorem_closed_policy_or_framing_missing
  need     = unit-triangle curved corner plus current period-156 context
```

All four still stop before DANGER3 framing, same-`j` bridge, `X_1(16)`
extraction, concrete `(A,x0)`, and official `vpp.py`.

## Near Misses

```text
h0_divisor_missing_h90_boundary:
  decision = conditional_divisor_identity_missing_h90_boundary

h0_source_certification_only:
  decision = source_certified_value_or_divisor_missing

conductor39_source_certification_only:
  decision = conductor39_source_identified_value_or_divisor_theorem_missing

conductor39_value_without_period156_control:
  decision = conditional_missing_period_156_context

twisted_h90_divisor_missing_period_bridge_context:
  decision = conditional_value_theorem_missing_period156_context

curved_corner_divisor_missing_period156_context:
  decision = conditional_missing_period156_context

finite_payload_without_source_control:
  decision = conditional_finite_payload_without_source_theorem

prime13_projection_or_axis_control:
  decision = reject_loses_mixed_tensor
```

## Counts

```text
row_count                       = 12
priority1_rows                  = 7
source_closing_rows             = 4
current_source_theorem_rows     = 0
avoids_value_branch_rows        = 7
period156_bridge_context_rows   = 5
helper_only_rows                = 2
conditional_rows                = 5
rejected_rows                   = 1
```

## Dependencies

```text
ksy_y_source_theorem_priority_selector_rows=1/1
ksy_y_conductor39_source_theorem_intake_rows=1/1
ksy_y_h0_source_theorem_candidate_matcher_rows=1/1
ksy_y_conductor39_twisted_descent_candidate_router_rows=1/1
ksy_y_value_payload_reality_check_rows=1/1
ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py
```

Marker:

```text
ksy_y_priority1_divisor_additive_intake_rows=1/1
```

## Packet Intake

Classify one theorem-snippet packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json <packet.json>
```

Stable examples live in:

```text
research/p25/priority1_divisor_additive_packet_fixtures
```

The fixture audit covers:

```text
h0_divisor_close.json
h0_missing_boundary.json
conductor39_divisor_close.json
twisted_divisor_close.json
twisted_missing_period.json
curved_corner_divisor_close.json
curved_missing_period.json
projection_reject.json
```

Audit command:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_packet_fixture_export_gate.py
```

Fixture audit marker:

```text
ksy_y_priority1_divisor_additive_packet_fixture_export_rows=1/1
```

Fixture audit counts:

```text
fixture_count                  = 8
exact_field_rows               = 8
decision_match_rows            = 8
priority1_rows                 = 8
source_stage_closing_rows      = 4
current_source_theorem_rows    = 0
avoids_value_branch_rows       = 8
period156_bridge_context_rows  = 4
rejected_rows                  = 1
conditional_rows               = 3
```

## Interpretation

The strongest next theorem ask is now executable:

```text
Give an exact divisor/additive identity for the legal
H0/conductor-39/twisted-H90/curved-corner source object, including the legal
Hilbert-90/ratio/unit-triangle boundary data.
```

For H0 and conductor-`39`, this avoids the finite-value branch.  For the
twisted/H90 and curved-corner routes, the current router still requires
period-`156` context because that is how the live object is tied back to the
p25 support period.
