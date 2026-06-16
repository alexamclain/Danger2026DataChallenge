# P25 KSY-y Koo-Shin / Kubert-Lang Hygiene Bridge

Updated: 2026-06-13 22:05 PDT

## Purpose

The Koo-Shin access probe found a promising snippet for a prime-level
Siegel-function product/distribution theorem, but no theorem body.  This note
records the exact p25 checksum against the open Kubert-Lang-style product
criterion exposed in Koo-Shin II and the existing p25 finite gates.

The useful conclusion is narrow:

```text
The p25 product passes the elementary Siegel-product exponent hygiene.
That does not close the route.  A theorem must still preserve the mixed graph.
```

## Bridge Rows

```text
KSY-y four-layer raw footprint
  evidence = y(Q)=-g(2Q)/g(Q)^4 expanded over the 75 atoms
  level = 12675
  support = 300
  congruence = passes Kubert-Lang quadratic/exponent screen
  mixed graph = preserved
  source theorem = missing
  verdict = necessary_KL_hygiene_passes_not_source_theorem

Six-cell mixed source packet
  evidence = common-level C_3 x C_169 source packet before K-trace expansion
  level = 507
  support = 6
  congruence = passes Kubert-Lang quadratic/exponent screen
  mixed graph = preserved
  source theorem = missing
  verdict = mixed_packet_hygiene_passes_but_needs_producer

C169 prime-power projection
  evidence = prime-power projection of the packet
  level = 169
  congruence = passes the screen
  mixed graph = not preserved
  verdict = prime_power_projection_is_necessary_but_insufficient
  missing = C_3 row labels, base anchor, and T-edge orientation

Odd-prime snippet boundary
  evidence = Koo-Shin 2010 snippet mentions an odd-prime product theorem
  theorem body = not recovered
  verdict = snippet_positive_not_enough_for_mixed_level_p25
  missing = full theorem body plus lift to p25 mixed levels 507 and 12675

Local control falsifiers
  controls = truncated D, wrong D, wrong T, positive-only variants
  result = all fail the exponent screen
  use = first local falsifier for any attempted theorem mapping
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_kl_hygiene_bridge_gate.py
```

```text
target_footprint_rows       = 2
congruence_positive_rows    = 3
mixed_graph_positive_rows   = 2
prime_power_projection_rows = 1
theorem_body_rows           = 0
direct_closing_rows         = 0
control_rejection_rows      = 1
exact_product_intake_decision = conditional_missing_arithmetic_producer
```

Marker:

```text
ksy_y_koo_shin_kl_hygiene_bridge_rows=1/1
```

## Verdict

This improves the moonshot posture slightly.  The Koo-Shin/Kubert-Lang product
lead is not arithmetically incompatible with the p25 footprint: the exact
target survives the standard product congruences.  But any theorem text we
recover must do more than produce an odd-prime or `C_169` product.  The first
acceptance check is whether it emits, lifts to, or canonically preserves the
mixed `C_3 x C_169` row graph at levels `507` and `12675`.
