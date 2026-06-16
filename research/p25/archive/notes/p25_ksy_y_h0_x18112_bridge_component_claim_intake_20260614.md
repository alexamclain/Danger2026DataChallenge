# P25 KSY-y H0 X1(8112) Bridge-Component Claim Intake

Updated: 2026-06-14 17:42 PDT

## Purpose

This gate is the downstream intake for an expert/subagent answer that claims
to bridge a source-closed H0/Y507 theorem into the practical DANGER3
`X_1(16)` surface.

It answers:

```text
Do the level-16 and level-507 components live on the same curve/same j-line,
or are they merely independent facts?
```

## Projection Arithmetic

```text
8112 = 16 * 507
507^-1 mod 16 = 3
16^-1 mod 507 = 412

P16  = [3*507]R  = [1521]R
Q507 = [412*16]R = [6592]R
1521 + 6592 = 1 mod 8112
```

So a same-curve `P16/Q507` pair can construct an order-`8112` bridge, but
independent level-`16` and level-`507` statements are rejected.

## Regression Rows

```text
snippet_only_no_theorem:
  decision = reject_no_theorem_body

h0_source_only:
  decision = upstream_odd_value_no_cross_level_bridge

generic_x16_no_h0_payload:
  decision = reject_no_h0_source_payload

same_curve_p16_only:
  decision = conditional_incomplete_component_pair

independent_p16_q507:
  decision = reject_unglued_components

same_curve_p16_q507_pair:
  decision = construct_order_8112_generator_then_specialize_x16

order8112_generator_no_x16_specialization:
  decision = cross_level_target_identified_specialization_missing

order8112_x16_relation_without_y:
  decision = conditional_x16_relation_without_y

order8112_x16_y_without_surface:
  decision = conditional_y_without_montgomery_surface

order8112_x16_surface_policy_missing:
  decision = cross_level_surface_policy_or_framing_missing

order8112_x16_surface_halving_missing:
  decision = x16_surface_reached_halving_or_vpp_missing

order8112_x0_payload_vpp_missing:
  decision = extraction_ready_vpp_missing

verified_pomerance_triple:
  decision = submission_ready_verified_triple
```

## Counts

```text
row_count                    = 13
rejected_rows                = 3
upstream_only_rows           = 1
incomplete_component_rows    = 1
order8112_constructible_rows = 7
cross_level_bridge_rows      = 8
x16_surface_rows             = 4
extraction_ready_rows        = 2
submission_ready_rows        = 1
```

## CLI Examples

Independent components are rejected:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x18112_bridge_component_claim_intake_gate.py \
  --candidate --name independent_demo --theorem-body --h0-source-payload \
  --same-curve-p16 --same-curve-q507
```

Same-curve components construct the order-`8112` bridge, but still need
practical `X_1(16)` specialization:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x18112_bridge_component_claim_intake_gate.py \
  --candidate --name same_curve_demo --theorem-body --h0-source-payload \
  --same-curve-p16 --same-curve-q507 --same-j
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x18112_bridge_component_claim_intake_gate.py
```

Marker:

```text
ksy_y_h0_x18112_bridge_component_claim_intake_rows=1/1
```

## Interpretation

This makes the extraction ask sharper.  After a source-closing H0 theorem, the
next useful answer is not generic level-`16` data.  It must provide same-j
gluing to the H0-tied `Q507`, or an order-`8112` generator whose projections
recover both sides, and then specialize to the production `X_1(16)` chart.
