# P25 KSY-y Post-Policy X1(8112) Work Order

Updated: 2026-06-14 22:34 PDT

## Purpose

This work order starts only after the DANGER3 finite-identity framing boundary
is cleared by explicit non-CM finite-field language or a Drew policy yes.  It
turns the next step into concrete bridge asks instead of a broad extraction
search.

The bridge target is:

```text
odd side:  exact_P, U_507, Y_507, canonical_H0, H0_translate, conductor39_U_chi, or curved_corner
2-side:    production X_1(16) y/x/A/xP16 surface
gluing:    same j-invariant, equivalently an X_1(8112) bridge
```

## Work Rows

```text
odd_theorem_only_control:
  decision = upstream_odd_value_no_cross_level_bridge
  work     = Do not confuse the source theorem with extraction.
  accepted = exact odd-level value/divisor theorem with no cross-level bridge
  falsifier = no X_1(16) relation or X_1(8112) fiber-product theorem

unglued_level16_level507_falsifier:
  decision = reject_unvalidated_fiber_product_gluing
  work     = Reject independent level-16 and level-507 facts.
  accepted = fiber product or modular correspondence over the same j-invariant
  falsifier = independent level data without same-j gluing

same_curve_P16_Q507_bridge:
  decision = cross_level_target_identified_specialization_missing
  work     = Find same-curve exact P16 and Q507 tied to the p25 odd target.
  accepted = same elliptic curve with exact 16- and 507-torsion components over the same j
  falsifier = same-j proof missing or odd target not one of the recorded KSY/Yang/H90 objects

order8112_generator_bridge:
  decision = cross_level_target_identified_specialization_missing
  work     = Find an exact order-8112 generator whose projections are the active P16 and odd target.
  accepted = R of order 8112 with [1521]R=P16 and [6592]R=Q507 on the same curve
  falsifier = R not exact order 8112 or projections not normalized to the p25 odd target

curved_corner_bridge_control:
  decision = cross_level_target_identified_specialization_missing
  work     = Keep the curved-corner source path on the same post-policy bridge ladder.
  accepted = same-j bridge for the unit-triangle curved K-traced corner source path
  falsifier = curved-corner path not tied to an accepted odd target over the same j

bridge_plus_x16_surface_no_halving:
  decision = x16_surface_reached_halving_or_vpp_missing
  work     = Specialize the bridge to the production X_1(16) Montgomery payload.
  accepted = same-j bridge emits y and model root x, or directly emits A,xP16
  falsifier = abstract P16 torsion without practical y/x/A/xP16 data

x0_payload_vpp_missing:
  decision = extraction_ready_vpp_missing
  work     = Finish extraction only after the concrete halving payload is present.
  accepted = bridge emits concrete A,x0 or a checkable halving chain from xP16
  falsifier = no official DANGER3 vpp.py verification

official_vpp_verified_boundary:
  decision = submission_ready_verified_triple
  work     = Submission boundary.
  accepted = official DANGER3 vpp.py verifies concrete p25 A,x0
  falsifier = official vpp.py rejects or has not been run
```

The official-vpp row is a boundary shape only, not current evidence.

## Candidate Commands

Classify a same-curve `P16/Q507` or order-`8112` bridge before `X_1(16)`
specialization:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name same_curve_bridge \
  --odd-payload-object canonical_H0 \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --danger3-framing
```

Expected:

```text
cross_level_target_identified_specialization_missing
```

Classify a bridge that reaches the practical `X_1(16)` surface but lacks
halving:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name bridge_surface \
  --odd-payload-object canonical_H0 \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --x16-relation \
  --emit-y --emit-model-root-xp16 --danger3-framing
```

Expected:

```text
x16_surface_reached_halving_or_vpp_missing
```

Reject independent level data:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name unglued_components \
  --odd-payload-object canonical_H0 \
  --theorem-body --exact-p25 --odd-value-or-divisor \
  --fiber-product --danger3-framing
```

Expected:

```text
reject_unvalidated_fiber_product_gluing
```

Classify the curved-corner bridge-control row:

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

## Counts

```text
row_count             = 8
current_evidence_rows = 0
work_order_rows       = 7
bridge_target_rows    = 6
x16_surface_rows      = 3
extraction_ready_rows = 2
boundary_rows         = 1
continue_rows         = 5
kill_rows             = 1
```

## Dependencies

```text
ksy_y_drew_policy_answer_router_rows=1/1
ksy_y_x1_8112_bridge_theorem_intake_rows=1/1
ksy_y_x1_8112_torsion_gluing_contract_rows=1/1
ksy_y_x1_16_montgomery_chart_contract_rows=1/1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_policy_x18112_work_order_gate.py
```

Marker:

```text
ksy_y_post_policy_x18112_work_order_rows=1/1
```

## Interpretation

After a policy/framing yes, the next theorem target is not "extract `A,x0`"
directly.  It is first one of:

```text
same-curve exact P16 and Q507 tied to the p25 odd target
exact order-8112 generator R with normalized projections to P16 and Q507
```

Only after that bridge is established should effort shift to the practical
`X_1(16)` `y/x/A/xP16` surface, then the halving chain, then official
`vpp.py`.
