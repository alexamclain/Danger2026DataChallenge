# P25 KSY-y Priority-1 Source-Query Packet

Updated: 2026-06-14 22:19 PDT

## Purpose

This is the cross-lane query surface for the priority-1 divisor/additive
moonshot.  It turns the packet intake into exact questions for source search,
subagents, or expert conversations.

## Closing Questions

```text
ask_h0_divisor_boundary_identity:
  question = Does the source prove an exact divisor/additive identity for one
             of the four legal 78-over-78 H0 products, with the Hilbert-90
             boundary to Norm_156(Y_507)?
  packet   = priority1_divisor_additive_packet_fixtures/h0_divisor_close.json
  decision = source_theorem_closed_policy_or_framing_missing

ask_conductor39_divisor_identity:
  question = Does the source prove an exact divisor/additive identity for the
             legal mixed conductor-39 source U_chi/W, preserving the chi_3
             tensor chi_13 object, Yang lift, and descent?
  packet   = priority1_divisor_additive_packet_fixtures/conductor39_divisor_close.json
  decision = source_theorem_closed_policy_or_framing_missing

ask_twisted_h90_divisor_identity:
  question = Does the source prove a finite divisor/additive theorem for the
             twisted ratio/Hilbert-90 object, with the period-156 bridge
             context currently required by the router?
  packet   = priority1_divisor_additive_packet_fixtures/twisted_divisor_close.json
  decision = source_theorem_closed_policy_or_framing_missing

ask_curved_corner_divisor_identity:
  question = Does the source prove a finite divisor/additive theorem for the
             exact unit-triangle curved K-traced corner, with the period-156
             context required by the current curved-corner router?
  packet   = priority1_divisor_additive_packet_fixtures/curved_corner_divisor_close.json
  decision = source_theorem_closed_policy_or_framing_missing
```

All four close only source stage.  They still need DANGER3 framing, same-`j`
bridge, `X_1(16)` extraction, concrete `(A,x0)`, and official `vpp.py`.

## Falsifier Questions

```text
falsify_h0_boundary_missing:
  packet   = priority1_divisor_additive_packet_fixtures/h0_missing_boundary.json
  decision = conditional_divisor_identity_missing_h90_boundary

falsify_projection_or_axis_only:
  packet   = priority1_divisor_additive_packet_fixtures/projection_reject.json
  decision = reject_loses_mixed_tensor

falsify_twisted_missing_period_bridge:
  packet   = priority1_divisor_additive_packet_fixtures/twisted_missing_period.json
  decision = conditional_value_theorem_missing_period156_context

falsify_curved_missing_period_context:
  packet   = priority1_divisor_additive_packet_fixtures/curved_missing_period.json
  decision = conditional_missing_period156_context
```

## Counts

```text
query_count                  = 8
closing_query_rows           = 4
falsifier_rows               = 4
current_source_theorem_rows  = 0
priority1_rows               = 7
fixture_rows_present         = 8
```

## Local Commands

Run the query packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_source_query_packet_gate.py
```

Classify any packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_divisor_additive_intake_gate.py \
  --packet-json <packet.json>
```

Marker:

```text
ksy_y_priority1_source_query_packet_rows=1/1
```

## Interpretation

The first serious source pass should not ask whether H0, conductor-`39`,
twisted/H90, or curved-corner language is broadly relevant.  It should ask for
the four exact divisor/additive identities above, and route every answer through the packet
fixtures before spending more context.
