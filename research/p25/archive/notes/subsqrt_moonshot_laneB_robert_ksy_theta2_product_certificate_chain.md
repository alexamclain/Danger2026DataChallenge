# P25 Lane B: Robert KSY Product-to-Certificate Chain

Updated: 2026-06-13 16:03 PDT

## Purpose

The normalized-y product source law is a concrete finite KSY target. This gate
records how that product payload becomes the accepted bridge certificate once a
challenge-legal arithmetic proof of the product is available.

It is a certificate-chain audit, not the missing arithmetic proof.

## Product Orientation

```text
forward product:
  prod_A y(A)/y(A+T) = theta2^-1
  finite resolvent recovers -bridge

reversed product:
  prod_A y(A+T)/y(A) = theta2
  finite resolvent recovers bridge
```

The sign is harmless for the existing finite payload contract, but a final
certificate should record the orientation explicitly.

## Budgets

```text
source parameter budget       = 31
theta2 payload support        = 300
bridge support                = 150
support-resolvent term budget = 46800
support-resolvent union       = 11700
compact telescoping budget    = 975
compact improvement factor    = 48
```

## Controls

The chain inherits the normalized-y product controls:

```text
missing K      rejected
collapsed K    rejected
truncated D    rejected
wrong D        rejected
wrong T        rejected
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_product_certificate_chain_gate.py
```

Expected marker:

```text
robert_ksy_theta2_product_certificate_chain_rows=1/1
```

## Interpretation

The theory target is now sharply connected to the verifier:

```text
prove product identity -> theta2 payload -> existing theta2 certificate path -> bridge
```

The remaining moonshot proof debt is exactly the arithmetic legality of the
normalized-y product as a challenge-legal object.
