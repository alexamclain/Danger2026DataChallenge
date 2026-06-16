# P25 KSY-y H0 Candidate-Packet Intake

Updated: 2026-06-14 18:05 PDT

## Purpose

This gate accepts one future H0 candidate packet and routes it through the
whole executable downstream ladder in order:

```text
exact H0 product file
  -> H0 source-theorem matcher
  -> DANGER3 finite-identity/non-CM framing
  -> same-j/order-8112 bridge component
  -> X_1(16) chart payload
  -> halving chain or direct x0
  -> official vpp.py boundary
```

It is designed for expert answers, theorem snippets, subagent reports, or
source-derived JSON packets.  The output is a first missing stage or a hard
falsifier, not a vague "promising" label.

## Packet Fields

```text
product_file
theorem_body_verified
arithmetic_source_theorem
output_kind
period156_context
h90_boundary
danger3_framing
same_curve_p16
same_curve_q507
same_j_or_curve
order8112_generator
y
x
A
xP16
z
x32
chain
chain_file
x0
run_vpp
```

`product_file` must match one of the stable H0 product fixtures.  `chain` may
be supplied inline, while `chain_file` may contain either bare field elements
or `depth value` rows.

## Regression Decisions

```text
missing_product_file:
  reject_missing_h0_product_file

source_certification_only:
  source_certified_value_or_divisor_missing

source_value_no_danger3:
  source_theorem_closed_policy_or_framing_missing

danger3_no_bridge:
  upstream_odd_value_no_cross_level_bridge

unglued_p16_q507:
  reject_unglued_components

bridge_no_chart:
  cross_level_target_identified_specialization_missing

chart_no_chain:
  surface_reached_certificate_missing

one_link_chain_prefix:
  partial_x_chain_verified_not_extraction

direct_A_x0_no_vpp:
  direct_x0_vpp_missing

direct_A_x0_vpp_fails:
  reject_vpp_failed
```

## Counts

```text
row_count                = 10
rejected_rows            = 3
source_stage_closed_rows = 8
danger3_framed_rows      = 7
cross_level_bridge_rows  = 5
x16_surface_rows         = 2
partial_chain_rows       = 1
extraction_ready_rows    = 1
vpp_executed_rows        = 1
submission_ready_rows    = 0
```

## CLI

Run the default regression gate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_candidate_packet_intake_gate.py
```

Classify a concrete packet:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_candidate_packet_intake_gate.py \
  --packet-json <packet.json>
```

Marker:

```text
ksy_y_h0_candidate_packet_intake_rows=1/1
```

## Interpretation

The packet gate is the current practical intake boundary for the H0 route.
It ensures that a future source/product answer is credited only for the stages
it actually closes.  A verified source theorem is not yet a DANGER3 answer; a
bridge is not yet an `X_1(16)` surface; and a verified halving prefix is not
yet an extraction-ready certificate.
