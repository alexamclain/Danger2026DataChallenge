# P25 KSY-y X1(8112) Bridge-Theorem Intake

Updated: 2026-06-14 22:30 PDT

## Purpose

This note turns the cross-level extraction gap into an intake contract for
future theorem or literature hits.

The target is not just:

```text
evaluate Y_507 / H0
```

and not just:

```text
construct some X_1(16) data
```

The target is a p25-specialized bridge between them:

```text
odd side:  exact_P, U_507, Y_507, canonical H0, H0 translate, conductor39_U_chi, or curved_corner
2-primary side: X_1(16) y, model root x, A, xP16, and halving chain
bridge level: lcm(16,507) = 8112
gluing: same j-invariant / real modular correspondence, not independent facts
```

## Accepted Shape

A real `X_1(8112)` bridge-theorem hit must provide all of:

```text
verified theorem/proof body
accepted odd target object
exact p25 specialization
odd-level value or divisor payload
fiber-product/cross-level modular correspondence
same-j gluing between X_1(16) and X_1(507)
specialization to the practical X_1(16) surface
actual y
model root x or marked xP16
DANGER3 finite-identity/non-CM framing
```

Then it still needs either:

```text
valid halving chain to x0 and official vpp.py verification
```

or a direct:

```text
official vpp.py-verified (p,A,x0)
```

## Falsifiers

```text
pure Y_507/H0/conductor-39 value theorem
  -> upstream only, not extraction

generic X_1(16) construction
  -> reject unless tied to the p25 odd target

independent level-16 and level-507 statements
  -> reject unless glued over the same j-invariant

fiber-product existence without p25 specialization
  -> cross-level target identified, extraction still missing

y without x/A/xP16
  -> not yet the practical Montgomery surface
```

The curved-corner route is accepted only after it has been promoted from
helper payload to an exact p25 odd-level value/divisor theorem.  Once promoted,
it joins the same bridge ladder and still needs the same-j `X_1(8112)` bridge
and `X_1(16)` specialization.

## Candidate Classifier

Example for a pure odd-level value theorem:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name pure_y507_value --theorem-body \
  --odd-payload-object Y_507 --exact-p25 --odd-value-or-divisor
```

Expected decision:

```text
upstream_odd_value_no_cross_level_bridge
```

Example for a bridge reaching the practical surface but not the halving chain:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name bridge_surface --theorem-body \
  --odd-payload-object canonical_H0 --exact-p25 --odd-value-or-divisor \
  --fiber-product --j-gluing --x16-relation --emit-y \
  --emit-model-root-xp16 --danger3-framing
```

Expected decision:

```text
x16_surface_reached_halving_or_vpp_missing
```

Example for the curved-corner bridge after source/policy closure but before
`X_1(16)` specialization:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py \
  --candidate --name curved_corner_bridge_control \
  --odd-payload-object curved_corner --theorem-body \
  --exact-p25 --odd-value-or-divisor --fiber-product --j-gluing \
  --danger3-framing
```

Expected decision:

```text
cross_level_target_identified_specialization_missing
```

## Counts

```text
accepted_odd_targets      = H0_translate, U_507, Y_507, canonical_H0, conductor39_U_chi, curved_corner, exact_P
odd_target_rows           = 10
cross_level_bridge_rows   = 8
x16_surface_rows          = 4
extraction_ready_rows     = 2
submission_ready_rows     = 1
upstream_only_rows        = 1
rejected_rows             = 3
conditional_rows          = 8
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_8112_bridge_theorem_intake_gate.py
```

Marker:

```text
ksy_y_x1_8112_bridge_theorem_intake_rows=1/1
```
