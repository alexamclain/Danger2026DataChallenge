# P25 KSY-y Unified Expert-Answer Router

Updated: 2026-06-14

## Purpose

This packet connects the ray-local pullback intake, the unit-triangle
curved-corner closing ask, and the conductor-`39` expert-answer workflow.

It deliberately does not identify the two languages as the same object.  It
keeps the routing distinction clear:

```text
ray-local 151 x 677 explanation -> must first reach raw/bridge or unit-triangle curved finite payload
conductor-39 / H0 value theorem  -> may close source stage, then needs DANGER3/extraction
```

## Rows

```text
expert_ray_local_no_payload_yet:
  decision = conditional_no_raw_harness_or_curved_corner_payload
  missing  = raw theta31/bridge vector or curved-corner payload

expert_ray_local_raw_bridge_helper:
  decision = helper_only_raw_bridge_payload_value_theorem_missing
  missing  = finite value/divisor theorem for the raw theta31 or bridge payload

expert_ray_local_curved_corner_helper:
  decision = helper_only_curved_corner_payload_value_theorem_missing
  missing  = finite value/divisor theorem for the curved K-traced corner payload
  note     = accepted only after the unit-triangle row law is present
             and routed through the curved-corner minimal closing ask

smoke_Uchi_divisor_identity:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

smoke_canonical_H0_ratio_identity:
  decision = source_theorem_closed_policy_or_framing_missing
  missing  = DANGER3 finite-identity/non-CM framing

smoke_policy_yes_extraction_missing:
  decision = danger3_unblocked_extraction_missing
  missing  = extraction algorithm for concrete (A, x0)

smoke_x1_8112_surface_halving_missing:
  decision = x16_surface_reached_halving_or_vpp_missing
  missing  = valid halving chain from xP16 to concrete x0

smoke_reject_generator_or_projection_only:
  decision = reject_loses_mixed_tensor
  falsifier = mixed chi_3 tensor chi_13 source on X_1(39)

verified_pomerance_triple_requires_real_values:
  decision = not_smoked_without_concrete_A_x0
  missing  = official vpp.py verification
```

## Counts

```text
row_count                = 9
local_pullback_rows      = 3
source_value_rows        = 2
downstream_rows          = 2
guardrail_rows           = 1
helper_only_rows         = 2
conditional_rows         = 1
rejected_rows            = 1
source_stage_closed_rows = 3
danger3_unblocked_rows   = 2
extraction_ready_rows    = 0
submission_ready_rows    = 0
placeholder_rows         = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_unified_expert_answer_router_gate.py
```

Expected marker:

```text
ksy_y_unified_expert_answer_router_rows=1/1
```

## Practical Use

For expert or literature answers:

```text
If the answer is a local modular-unit / CM-Artin pullback:
  first send it through the ray-local router; curved-corner answers must carry
  the unit-triangle law, then use the curved-corner minimal closing ask.

If the answer is a finite value/divisor theorem for U_chi, W, Y_507, H0, or
an H0 translate:
  send it through the conductor-39 / H90 value-theorem intake.

If the answer is only a ray-class generator, prime-13/C169 projection, or
field-generation statement:
  kill it unless it restores the mixed tensor and ray-local coupling.

If the answer gives policy/framing but not concrete A,x0:
  continue to extraction; it is not a submission.
```

This is also the answer to the "75 atoms" ambiguity: even a unit-triangle
75-atom finite payload is still only a helper unless it comes with a
value/divisor theorem and the downstream DANGER3/extraction chain.
