# P25 KSY-y Ray-Local / Conductor-39 Bridge-Theorem Intake

Updated: 2026-06-14 17:27 PDT

## Purpose

The alignment check proves:

```text
U_chi=-chi_3*chi_13 is not the ray-local theta31 payload.
```

This packet classifies future claims that try to cross that gap.  A claim may
be useful in two different ways:

```text
conductor-39 value route:
  finite value/divisor theorem for U_chi, W, Y_507, H0, or H0 translate

ray-local bridge route:
  explicit theorem mapping/evaluating the conductor-39 source into a raw
  theta31/bridge payload or the curved-corner payload
```

It rejects the bad middle ground:

```text
U_chi is theta31
```

unless the claim supplies an actual bridge/evaluation theorem resolving the
support/rank/orthogonality mismatch.

## Alignment Facts

The required obstruction to resolve is:

```text
theta31 support          = 18
U_chi support            = 24
raw signed dot           = 0
theta31 mixed rank       = 2
U_chi rank               = 1
combined mixed rank      = 3
```

## First Falsifier

The intake now depends on the simple-transform falsifier:

```text
simple_transform_falsifier_ok = 1
exact support matches         = 0
row/column solvable rows      = 0
separated rank ceiling        = 1
```

So a claim that tries to bridge `U_chi` to `theta31` must beat more than the
raw alignment mismatch.  It must also get past the finite check that kills:

```text
scalar/sign multiple
product-affine relabel on C_3 x C_13
product-affine relabel plus scalar
row-plus-column additive normalization
separated row/C-axis multiplicative gauge
```

## Regression Rows

```text
no_theorem_body:
  decision = reject_no_theorem_body

missing_conductor39_source:
  decision = reject_missing_conductor39_source

projection_generator_only:
  decision = reject_loses_mixed_tensor

bare_uchi_theta31_rename:
  decision = reject_uchi_theta31_renaming

source_only_no_bridge:
  decision = conditional_conductor39_source_only_no_ray_bridge

conductor39_value_no_ray_bridge:
  decision = source_theorem_closed_not_ray_payload_policy_or_framing_missing

bridge_unresolved_alignment:
  decision = reject_alignment_obstruction_unresolved

bridge_target_unspecified:
  decision = conditional_bridge_target_payload_unspecified

bridge_no_finite_acceptor:
  decision = conditional_bridge_no_finite_acceptor

raw_theta31_helper:
  decision = helper_only_raw_theta31_bridge_value_theorem_missing

curved_corner_helper:
  decision = helper_only_curved_corner_bridge_value_theorem_missing

value_no_period156:
  decision = conditional_missing_period156_context

period156_value_no_source:
  decision = conditional_finite_payload_without_source_theorem

source_no_framing:
  decision = source_theorem_closed_policy_or_framing_missing

danger3_no_same_j:
  decision = danger3_unblocked_cross_level_bridge_missing

same_j_no_x16:
  decision = cross_level_target_identified_specialization_missing

x16_no_x0:
  decision = x16_surface_reached_halving_or_vpp_missing

x0_no_vpp:
  decision = extraction_ready_vpp_missing

official_vpp_verified:
  decision = submission_ready
```

## Counts

```text
row_count                 = 19
rejected_rows             = 5
helper_only_rows          = 2
conditional_rows          = 5
source_stage_closed_rows  = 7
ray_payload_rows          = 10
finite_value_rows         = 9
danger3_unblocked_rows    = 5
cross_level_bridge_rows   = 4
x16_surface_rows          = 3
extraction_ready_rows     = 2
submission_ready_rows     = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ray_local_conductor39_bridge_theorem_intake_gate.py
```

Expected marker:

```text
ksy_y_ray_local_conductor39_bridge_theorem_intake_rows=1/1
```

## Practical Routing

```text
If a theorem evaluates U_chi/W/H0 but has no ray-local bridge:
  continue as conductor-39/H0 value route.

If a theorem claims U_chi is theta31:
  reject unless it resolves the finite mismatch beyond the simple-transform
  falsifier.

If a theorem gives a raw/curved ray-local payload:
  run the finite acceptor, then demand a value/divisor theorem.

If a theorem closes source stage:
  route to DANGER3 framing, same-j X_1(8112), X_1(16), concrete A/x0, and
  official vpp.py.
```
