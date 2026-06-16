# P25 KSY-y H0 X1(16) Halving-Chain Payload Intake

Updated: 2026-06-14 17:56 PDT

## Purpose

This gate checks the final numeric extraction payload below the H0/order-`8112`
and `X_1(16)` chart layers:

```text
x_4 = xP16, x_5, ..., x_42 = x0
```

Each supplied child coordinate must double back to its parent on the same
Montgomery curve.  A verified prefix is useful, but only a full `39`-point
chain or a direct `x0` can become extraction-ready, and official `vpp.py`
remains the submission boundary.

## Shape

```text
p = 10^25 + 13
start_depth = 4
final_depth = 42
halving_links = 38
x_chain_points = 39
```

The link check is:

```text
xDBL_A(x_{i+1}) = x_i, for i = 4..41
```

using the Montgomery x-coordinate doubling formula.

## Regression Rows

```text
surface_only:
  decision = surface_reached_certificate_missing

one_link_verified_prefix:
  decision = partial_x_chain_verified_not_extraction

chain_without_xP16:
  decision = conditional_chain_without_xP16_start

chain_start_mismatch:
  decision = reject_chain_start_mismatch

chain_link_mismatch:
  decision = reject_chain_link_mismatch

chain_x0_tail_mismatch:
  decision = reject_x0_tail_mismatch

direct_A_x0_no_vpp:
  decision = direct_x0_vpp_missing

direct_A_x0_vpp_fails:
  decision = reject_vpp_failed

missing_A:
  decision = reject_missing_A
```

## Positive Prefix Control

The one-link control uses the chart sample from the chart-payload intake:

```text
A     = 5001921875000000000039606
xP16  = 5641277106015054878246206
x32   = 8473620875806245623307779
```

The gate verifies:

```text
xDBL_A(x32) = xP16
```

and classifies it as a verified prefix, not extraction-ready.

## Counts

```text
row_count             = 9
rejected_rows         = 5
surface_missing_rows  = 1
partial_chain_rows    = 1
full_chain_rows       = 0
direct_x0_rows        = 1
extraction_ready_rows = 1
vpp_executed_rows     = 1
submission_ready_rows = 0
```

## CLI Examples

Valid one-link prefix:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_halving_chain_payload_intake_gate.py \
  --candidate --name one_link \
  --A 5001921875000000000039606 \
  --xP16 5641277106015054878246206 \
  --chain 5641277106015054878246206 8473620875806245623307779
```

Corrupted child coordinate:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_halving_chain_payload_intake_gate.py \
  --candidate --name bad_link \
  --A 5001921875000000000039606 \
  --xP16 5641277106015054878246206 \
  --chain 5641277106015054878246206 8473620875806245623307780
```

For real candidate chains, pass either bare values or `depth value` rows in a
file:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_halving_chain_payload_intake_gate.py \
  --candidate --name proposed_chain \
  --A <A> --xP16 <xP16> --chain-file <path>
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_x16_halving_chain_payload_intake_gate.py
```

Marker:

```text
ksy_y_h0_x16_halving_chain_payload_intake_rows=1/1
```

## Interpretation

This is the last executable intake before official submission verification.
A future extraction answer can now be checked as actual finite-field data:
chart payload, then halving-chain payload, then official `vpp.py`.
