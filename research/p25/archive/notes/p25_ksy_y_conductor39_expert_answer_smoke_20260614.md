# P25 KSY-y Conductor-39 Expert-Answer Smoke

Updated: 2026-06-14 14:15 PDT

## Purpose

The expert-query packet names ten possible answer shapes.  This smoke packet
runs the nine answer shapes that can be classified now, and explicitly refuses
to smoke-test the verified-triple row without concrete `A,x0` values.

## Executed Rows

```text
smoke_Uchi_divisor_identity:
  actual = source_theorem_closed_policy_or_framing_missing
  missing = DANGER3 finite-identity/non-CM framing

smoke_W_degree6_value_descent:
  actual = source_theorem_closed_policy_or_framing_missing
  missing = DANGER3 finite-identity/non-CM framing

smoke_canonical_H0_ratio_identity:
  actual = source_theorem_closed_policy_or_framing_missing
  missing = DANGER3 finite-identity/non-CM framing

smoke_Y507_period156_value_identity:
  actual = source_theorem_closed_policy_or_framing_missing
  missing = DANGER3 finite-identity/non-CM framing

smoke_policy_yes_extraction_missing:
  actual = danger3_unblocked_extraction_missing
  missing = extraction algorithm for concrete (A, x0)

smoke_x1_8112_surface_halving_missing:
  actual = x16_surface_reached_halving_or_vpp_missing
  missing = valid halving chain from xP16 to concrete x0

smoke_reject_direct_Fp_order39_root:
  actual = reject_direct_Fp_order39_root_shortcut
  falsifier = ord_39(p)=6

smoke_reject_sqrt_minus39_scalar:
  actual = reject_sqrt_minus39_scalar_shortcut
  falsifier = (-39/p)=-1

smoke_reject_generator_or_projection_only:
  actual = reject_loses_mixed_tensor
  falsifier = mixed chi_3 tensor chi_13 source on X_1(39)
```

## Held Boundary

```text
verified_pomerance_triple_requires_real_values:
  actual = not_smoked_without_concrete_A_x0
  missing = official vpp.py verification
```

This is intentional.  The submission row cannot be truthfully tested with
placeholders.

## Counts

```text
smoke_row_count        = 10
executed_rows          = 9
source_closing_rows    = 5
downstream_rows        = 2
guardrail_rows         = 3
placeholder_rows       = 1
submission_ready_rows  = 0
```

The `source_closing_rows=5` count includes the downstream policy row, because a
policy yes presupposes a source theorem that has already closed.  The four
actual source-answer shapes remain the four rows from the expert-query packet.

## Arithmetic

```text
p_order_mod39            = 6
sqrt_minus39_in_fp       = 0
period156_unique_branch  = 1
ambient780_mu11          = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_expert_answer_smoke_gate.py
```

Marker:

```text
ksy_y_conductor39_expert_answer_smoke_rows=1/1
```
