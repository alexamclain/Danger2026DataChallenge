# P25 KSY-y Yang Quotient Normalized-y Descent

Updated: 2026-06-14 08:58 PDT

## Purpose

The previous Yang checkpoints proved that the raw `150`-term K trace descends
to the six-cell modular unit

```text
U_507 = E_25 E_197 E_369 / (E_138 E_310 E_482).
```

This checkpoint applies the KSY formula

```text
y(Q) = -g(2Q) / g(Q)^4
```

after the same Yang descent.

## Result

The raw KSY-y footprint has `300` terms with coefficient counts:

```text
(-4, 75), (-1, 75), (1, 75), (4, 75)
```

Those `300` terms are exactly `12` constant Yang orbits of length `25`.  The
quotient-level footprint is:

```text
25  -> -4
50  ->  1
113 -> -1
138 ->  4
197 -> -4
231 ->  1
276 -> -1
310 ->  4
369 -> -4
394 ->  1
457 -> -1
482 ->  4
```

Equivalently:

```text
Y_507 = [2]^* U_507 / U_507^4
```

where `[2]^*` sends `E_a` to `E_{2a}`.

## Verdict

Positive payload:

```text
the KSY-y 300-term footprint descends to the quotient modular unit
Y_507=[2]^*U_507/U_507^4
```

First missing clause:

```text
no source theorem yet proves the finite-field value or divisor identity for
Y_507 with period-156 context and DANGER3 extraction
```

Practical effect:

```text
future source/theorem hits can target Y_507 directly instead of the raw
300-term KSY-y footprint
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_quotient_normalized_y_descent_gate.py
```

Marker:

```text
ksy_y_yang_quotient_normalized_y_descent_rows=1/1
```
