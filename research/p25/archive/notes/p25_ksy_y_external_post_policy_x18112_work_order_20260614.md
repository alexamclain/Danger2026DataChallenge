# P25 KSY-y External Post-Policy X1(8112) Work Order

Updated: 2026-06-14 22:30 PDT

## Purpose

This work order starts after an external Drew policy yes, including policy yes
answers for the exact 75-atom product and the curved-corner source path.  It
makes the next missing item explicit: accepted odd targets such as `exact_P`,
`canonical_H0`, and `curved_corner` must be glued to the production `X_1(16)`
surface over the same j-invariant, equivalently through an `X_1(8112)` bridge.

## Exact-P Work Rows

```text
exactP_odd_theorem_only_control:
  decision  = upstream_odd_value_no_cross_level_bridge
  work      = Do not confuse an exact P source theorem with extraction.
  accepted  = exact 75-atom P value/divisor theorem with no cross-level bridge
  falsifier = no X_1(16) relation or X_1(8112) fiber-product theorem

exactP_unglued_level16_level507_falsifier:
  decision  = reject_unvalidated_fiber_product_gluing
  work      = Reject independent level-16 and exact-P facts.
  accepted  = fiber product or modular correspondence over the same j-invariant
  falsifier = independent level data without same-j gluing

exactP_same_curve_P16_odd_bridge:
  decision  = cross_level_target_identified_specialization_missing
  work      = Find same-curve exact P16 and exact-P odd target data.
  accepted  = same elliptic curve with exact 16-torsion and exact_P odd payload over the same j
  falsifier = same-j proof missing or odd target not exact_P/Yang/H90 compatible

exactP_order8112_generator_bridge:
  decision  = cross_level_target_identified_specialization_missing
  work      = Find an exact order-8112 generator whose projections are P16 and exact_P.
  accepted  = R of order 8112 with normalized projections to P16 and the exact_P odd target
  falsifier = R not exact order 8112 or projections not normalized to exact_P

exactP_bridge_plus_x16_surface_no_halving:
  decision  = x16_surface_reached_halving_or_vpp_missing
  work      = Specialize the exact-P bridge to the production X_1(16) Montgomery payload.
  accepted  = same-j exact_P bridge emits y and model root x, or directly emits A,xP16
  falsifier = abstract P16 torsion without practical y/x/A/xP16 data

exactP_x0_payload_vpp_missing:
  decision  = extraction_ready_vpp_missing
  work      = Finish extraction only after the exact-P halving payload is present.
  accepted  = exact-P bridge emits concrete A,x0 or a checkable halving chain from xP16
  falsifier = no official DANGER3 vpp.py verification
```

## Control Rows

```text
canonical_H0_bridge_control:
  decision = cross_level_target_identified_specialization_missing
  purpose  = keep non-exact-P front doors on the same post-policy bridge ladder

curved_corner_bridge_control:
  decision = cross_level_target_identified_specialization_missing
  purpose  = keep the unit-triangle curved-corner front door on the same post-policy bridge ladder

official_vpp_verified_boundary:
  decision = submission_ready_verified_triple
  purpose  = official vpp.py boundary only; not current evidence
```

## Counts

```text
row_count             = 9
current_evidence_rows = 0
work_order_rows       = 8
exact_p_payload_rows  = 6
bridge_target_rows    = 7
x16_surface_rows      = 3
extraction_ready_rows = 2
boundary_rows         = 1
continue_rows         = 6
kill_rows             = 1
```

## Dependencies

```text
ksy_y_external_drew_policy_answer_router_rows=1/1
ksy_y_external_post_source_danger3_handoff_rows=1/1
ksy_y_x1_8112_bridge_theorem_intake_rows=1/1
ksy_y_x1_8112_torsion_gluing_contract_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
```

## Candidate Commands

Classify an exact-P same-j bridge before `X_1(16)` specialization:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name exactP_same_curve_bridge \
  --odd-payload-object exact_P \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --danger3-framing
```

Expected:

```text
cross_level_target_identified_specialization_missing
```

Classify an exact-P bridge that reaches the practical `X_1(16)` surface but
lacks halving:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name exactP_bridge_surface \
  --odd-payload-object exact_P \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --x16-relation \
  --emit-y --emit-model-root-xp16 --danger3-framing
```

Expected:

```text
x16_surface_reached_halving_or_vpp_missing
```

Reject unglued exact-P/level-16 data:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name exactP_unglued_components \
  --odd-payload-object exact_P \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --danger3-framing
```

Expected:

```text
reject_unvalidated_fiber_product_gluing
```

Classify the curved-corner bridge-control row after source and policy closure:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name curved_corner_bridge_control \
  --odd-payload-object curved_corner \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --danger3-framing
```

Expected:

```text
cross_level_target_identified_specialization_missing
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_external_post_policy_x18112_work_order_gate.py

python3 -m py_compile \
  research/p25/p25_ksy_y_external_post_policy_x18112_work_order_gate.py
```

Marker:

```text
ksy_y_external_post_policy_x18112_work_order_rows=1/1
```

## Interpretation

After exact75 or curved-corner policy yes, the next theorem target is not
direct extraction.  It is first a same-j bridge tying the accepted odd target
to the production `X_1(16)` surface, or an exact order-`8112` generator with
normalized projections.  Only then does effort move to `X_1(16)`
`y/x/A/xP16`, the halving chain, and official `vpp.py`.
