# P25 Lane B: Robert KSY Kubert-Lang Graph Row Law

Updated: 2026-06-13 17:35 PDT

## Purpose

The exact Kubert-Lang matrix route survives only if it preserves the mixed
`C_3 x C_169` row graph.  The prime-power `C_169` projection is not enough.

This gate scans the natural sign-affine row lifts of the six `C_169` cells.

## C-Axis Projection

```text
positive C cells = 25,28,31
negative C cells = 138,141,144
```

Sign-affine row law:

```text
positive row = positive_base + slope*j
negative row = negative_base + slope*j
j = 0,1,2
```

## Result

```text
sign-affine laws scanned = 27
KL congruence laws       = 27
balanced laws            = 21
D-segment/T-edge laws    = 9
fixed-T laws             = 3
exact base/D/T laws      = 1
```

The unique exact law is:

```text
slope = 1
positive_base = 1
negative_base = 0
```

The fixed-`T` edge leaves three row translates:

```text
slope=1, positive_base=0, negative_base=2 -> rejected
slope=1, positive_base=1, negative_base=0 -> accepted
slope=1, positive_base=2, negative_base=1 -> rejected
```

The two wrong row translates lift to support-`150` packets but fail the source
packet contract.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_graph_row_law_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_graph_row_law_rows=1/1
```

## Interpretation

An exact Kubert-Lang/Siegel theorem must supply both:

```text
the sign-affine row graph
the base-row anchor
```

The `C_169` projection plus KL congruences does not select the p25 packet.
