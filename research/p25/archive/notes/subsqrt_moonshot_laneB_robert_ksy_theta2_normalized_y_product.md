# P25 Lane B: Robert KSY Normalized-y Product Source Law

Updated: 2026-06-13 16:00 PDT

## Purpose

The D=2 theorem obligation says a proof should emit theta2 data. This gate
spells out the most concrete KSY finite source-law target:

```text
prod_{A in base*K_trace*D_segment} y(A) / y(A+T)
```

with

```text
y(Q) = -g(2Q) / g(Q)^4
```

At the divisor-footprint level this product is exactly theta2 inverse. The
reversed quotient emits theta2.

## Source Data

```text
base = (25,25)
K    = (57,0), length 25
D    = (22,3), length 3
T    = (38,113)
```

Equivalent compact KSY data recovered by the gate:

```text
center_base = (44,166)
half_shift  = (56,28)
```

## Result

```text
prod y(A)/y(A+T)        -> theta2^-1
prod y(A+T)/y(A)        -> theta2
footprint support       = 300
source parameter budget = 31
```

The finite theta2 resolvent then recovers the bridge through the existing
accepted theta2 path.

## Controls

All fail:

```text
missing K trace
collapsed K
truncated D segment
wrong D
wrong T
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_normalized_y_product_gate.py
```

Expected marker:

```text
robert_ksy_theta2_normalized_y_product_rows=1/1
```

## Interpretation

This is the finite source-law target for a KSY `D=2` proof. The missing theorem
is now sharper:

```text
prove that this normalized-y product is a challenge-legal arithmetic object
```

The gate does not prove that arithmetic legality; it verifies the finite
payload and kills the closest structural mistakes.
