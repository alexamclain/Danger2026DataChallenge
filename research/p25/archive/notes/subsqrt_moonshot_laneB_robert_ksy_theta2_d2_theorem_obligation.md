# P25 Lane B: Robert KSY/Kato-Siegel D=2 Theorem Obligation

Updated: 2026-06-13 15:54 PDT

## Purpose

The finite pipeline now accepts theta2 as a producer interface. This gate
states the remaining theorem-side burden for a Koo-Shin-Yoon / Kato-Siegel
`D=2` route.

It is not an arithmetic proof. It is an executable checklist for what such a
proof must supply.

## Accepted Theorem Outputs

```text
divisor_theta2_or_inverse
  accepted finite payload
  must prove a challenge-legal identity emitting exact theta2 or theta2^-1

compact_ksy_center_half_orientation
  accepted finite payload
  must derive center_base=(44,166), half_shift=(56,28), and orientation

source_packet_or_factor_shadow
  accepted finite payload
  must emit the six-cell source packet or quotient factor classes
```

## Rejected Or Conditional Shortcuts

```text
normalized_y_footprint_as_bridge
  rejected: coefficient-blind 300-cell footprint fails

coefficient_abs_4_layer_filter
  not a theorem by itself: the bridge appears only after post-hoc finite
  coefficient filtering

kato_siegel_dlog_chain_rule_alone
  rejected: dlog footprint still has support 300; only lambda=-2 repair works

formal_two_norm_or_transport
  rejected: multiplication by 2 has trivial kernel and transported theta2 fails

square_root_or_half_dlog_escape
  rejected: theta2 has no integral square-root footprint; half-dlog still fails

value_unit_without_branch
  conditional: gcd(4^780-1,p-1)=11, and the finite bridge contract cannot
  select one of the eleven value branches
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_d2_theorem_obligation_gate.py
```

Expected marker:

```text
robert_ksy_theta2_d2_theorem_obligation_rows=1/1
```

## Interpretation

The current sharp theory target is:

```text
find a challenge-legal D=2 theta2 identity emitting an accepted payload
```

The smallest theorem-facing output remains compact KSY data:

```text
center_base=(44,166)
half_shift=(56,28)
orientation/inversion flag
```

The most robust divisor-level output is an exact theta2 or theta2-inverse
payload. If a route produces only multiplicative values, it must also supply
root/branch selection.
