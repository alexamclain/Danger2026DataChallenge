# P25 KSY-y H0 X1(8112) Bridge Payload Contract

Updated: 2026-06-14 16:00 PDT

## Purpose

After an H0 source-closing theorem, the missing constructive bridge is not a
generic mention of level `16`.  It must glue the H0 odd component to the
practical `X_1(16)` component on the same curve, or equivalently produce an
order-`8112` point whose normalized projections recover both sides.

## Projection Arithmetic

```text
8112 = 16 * 507
gcd(16,507) = 1

507^-1 mod 16 = 3
16^-1 mod 507 = 412

P16  = [3*507]R  = [1521]R
Q507 = [412*16]R = [6592]R

1521 + 6592 = 1 mod 8112
ord([1521]R) = 16
ord([6592]R) = 507
```

Thus an acceptable bridge payload can be either:

```text
same-curve exact P16 and H0-tied Q507
exact order-8112 generator R tied to H0
```

## Rows

```text
source-closed H0 with no same-curve bridge:
  decision = upstream_odd_value_no_cross_level_bridge

independent P16 and Q507 data:
  decision = reject_unglued_components

same-curve P16/Q507 pair:
  decision = construct_order_8112_generator_then_specialize_x16

order-8112 R without X_1(16) specialization:
  decision = cross_level_target_identified_specialization_missing

order-8112 bridge with abstract X_1(16) relation:
  decision = conditional_x16_relation_without_y

order-8112 bridge with y but no model root/A/xP16:
  decision = conditional_y_without_montgomery_surface

order-8112 bridge with practical X_1(16) surface:
  decision = cross_level_surface_policy_or_framing_missing

DANGER3-framed X_1(16) surface without x0:
  decision = x16_surface_reached_halving_or_vpp_missing

concrete A/x0 without official verifier:
  decision = extraction_ready_vpp_missing

officially verified triple:
  decision = submission_ready_verified_triple
```

## Counts

```text
row_count                    = 10
projection_rows_ok           = 4
x1_classifier_rows           = 8
rejected_rows                = 1
same_j_bridge_rows           = 8
order8112_constructible_rows = 8
x16_surface_rows             = 4
extraction_ready_rows        = 2
submission_ready_rows        = 1
```

## Interpretation

The bridge theorem ask is now exact: give same-`j`/same-curve torsion data,
not independent level-`16` and level-`507` statements.  Even a correct
order-`8112` bridge still has to specialize to the practical `X_1(16)` chart
and then to a `vpp.py`-verified `(p,A,x0)` triple.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x18112_bridge_payload_contract_gate.py
```

Marker:

```text
ksy_y_h0_x18112_bridge_payload_contract_rows=1/1
```
