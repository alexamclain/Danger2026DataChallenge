# P25 KSY-y DANGER3 Finite-Identity Framing Router

Updated: 2026-06-14 16:35 PDT

## Purpose

This is the intake form for future source-theorem, Drew-policy, or literature
claims after a p25 finite product/value identity appears.  It keeps three
states separate:

```text
generic CM/class-field production
finite-field identity framed for this p
official vpp.py-verified DANGER3 triple
```

## Candidate Classifier

```text
no_source_no_triple:
  decision = reject_no_source_theorem_or_triple

source_theorem_no_finite_identity:
  decision = source_theorem_value_shape_missing_finite_identity

generic_cm_class_field_generation:
  decision = reject_generic_cm_generation_not_framing

finite_identity_policy_unknown:
  decision = source_theorem_closed_policy_or_framing_missing

finite_identity_explicit_non_cm_no_bridge:
  decision = danger3_unblocked_cross_level_bridge_missing

finite_identity_policy_yes_no_bridge:
  decision = danger3_unblocked_cross_level_bridge_missing

same_j_bridge_no_x16:
  decision = cross_level_target_identified_specialization_missing

x16_surface_no_x0:
  decision = x16_surface_reached_halving_or_vpp_missing

concrete_A_x0_no_vpp:
  decision = extraction_ready_vpp_missing

official_vpp_verified_triple:
  decision = submission_ready
```

## Counts

```text
row_count                       = 10
rejected_rows                   = 2
source_shape_missing_rows       = 1
policy_or_framing_missing_rows  = 1
danger3_unblocked_rows          = 6
cross_level_bridge_rows         = 4
x16_surface_rows                = 3
extraction_ready_rows           = 2
submission_ready_rows           = 1
```

## CLI Examples

Classify a source theorem with finite p25 identity but no policy/framing:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_finite_identity_framing_router_gate.py \
  --candidate --source-theorem --finite-identity
```

Expected:

```text
source_theorem_closed_policy_or_framing_missing
```

Classify the same theorem after policy yes, before the cross-level bridge:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_finite_identity_framing_router_gate.py \
  --candidate --source-theorem --finite-identity --policy-yes
```

Expected:

```text
danger3_unblocked_cross_level_bridge_missing
```

Reject generic CM/class-field provenance as framing:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_finite_identity_framing_router_gate.py \
  --candidate --source-theorem --finite-identity --generic-cm
```

Expected:

```text
reject_generic_cm_generation_not_framing
```

## Interpretation

This gate does not settle DANGER3 policy.  It records the boundary.  A source
theorem can be framed either by explicit non-CM finite-field identity language
or by an external policy yes.  Generic CM/class-field provenance by itself is
not accepted as framing.

Even after framing is unblocked, the route still needs the same-j bridge, an
X_1(16) surface or equivalent `(A,xP16)`, a concrete `x0`, and official
`vpp.py` verification.  Only the verified `(p,A,x0)` state is submission-ready.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_finite_identity_framing_router_gate.py
```

Marker:

```text
ksy_y_danger3_finite_identity_framing_router_rows=1/1
```
