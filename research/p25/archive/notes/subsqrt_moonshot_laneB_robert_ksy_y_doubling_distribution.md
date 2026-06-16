# P25 Lane B: Robert KSY-y Doubling Distribution

Updated: 2026-06-13 14:06 PDT

## Purpose

The projection gate showed:

```text
normalized-y footprint = double_pushforward(bridge) - 4*bridge
```

This artifact checks whether the doubled layer can disappear by a cheap
ordinary doubling distribution or orbit average.

## Result

Multiplication by `2` is an automorphism on the source group:

```text
source group = C_75 x C_169
ord_75(2) = 20
ord_169(2) = 156
source order of doubling = 780
kernel size = 1
```

Consequences:

```text
doubled bridge support = 150, wrong trace
full doubling orbit union support = 11700
full orbit sum support = 7800, coefficients +/-10, fails bridge
alternating full orbit sum = 0
```

For low-complexity combinations

```text
normalized-y footprint + lambda * doubled bridge, -5 <= lambda <= 5
```

only `lambda=-1` reduces support to `150`, and it gives `-4*bridge`.  Exact
division by `-4` then recovers the bridge.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_doubling_distribution_gate.py
```

Expected marker:

```text
robert_ksy_y_doubling_distribution_rows=1/1
```

## Interpretation

The doubled `g(2Q)` layer is not removed by a free norm/distribution over the
doubling map.  A successful KSY `y` or Kato-Siegel `dlog` route must provide
the exact doubled-layer subtraction, or an equivalent logarithmic-derivative
cancellation, before the sparse bridge payload is emitted.
