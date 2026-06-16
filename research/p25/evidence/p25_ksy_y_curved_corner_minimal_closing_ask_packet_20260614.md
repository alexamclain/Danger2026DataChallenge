# P25 KSY-y Curved-Corner Minimal Closing-Ask Packet

Updated: 2026-06-14 19:05 PDT

## Purpose

This packet is the compact closing ask for the unit-triangle curved Hilbert-90
corner route.  It separates three things that are easy to blur:

```text
curved corner without unit triangle     -> reject
unit-triangle curved corner             -> finite helper only
period-156 value/divisor source theorem -> source-stage closer
```

The `75` atoms are fixed payload factors, not 75 tries.

## Minimal Ask

The smallest useful yes is:

```text
finite value/divisor theorem
for the exact unit-triangle curved K-traced corner payload
with period-156 branch/root/telescoping context
emitted by a challenge-legal arithmetic source theorem
```

Equivalent H90/Y507 wording:

```text
finite value/divisor theorem for exact P, Y_507, canonical H0, H0 translate,
or conductor39_U_chi
preserving the 75 -> 300 -> 12 -> 312 -> 156 bridge spine
```

After that, the route still needs DANGER3 finite-identity/non-CM framing,
same-j extraction to the practical X_1(16) chart, concrete `(A,x0)`, and
official `vpp.py`.

## Rows

```text
curved_corner_without_unit_triangle:
  decision = reject_passive_or_wrong_unit_triangle

unit_triangle_corner_helper_only:
  decision = helper_only_curved_triangle_value_theorem_missing

unit_triangle_value_no_period156:
  decision = conditional_missing_period156_context

unit_triangle_period156_no_source:
  decision = conditional_finite_payload_without_source_theorem

unit_triangle_source_no_danger3:
  decision = source_theorem_closed_policy_or_framing_missing

h90_live_target_no_value:
  decision = live_target_identified_value_or_divisor_theorem_missing

h90_period156_value_source_no_danger3:
  decision = source_theorem_closed_policy_or_framing_missing

verified_triple_boundary:
  decision = submission_ready_verified_triple
```

## Counts

```text
row_count                    = 8
rejected_rows                = 1
helper_only_rows             = 1
conditional_rows             = 3
source_theorem_closing_rows  = 3
submission_ready_rows        = 1
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_curved_corner_minimal_closing_ask_packet_gate.py
```

Marker:

```text
ksy_y_curved_corner_minimal_closing_ask_packet_rows=1/1
```
