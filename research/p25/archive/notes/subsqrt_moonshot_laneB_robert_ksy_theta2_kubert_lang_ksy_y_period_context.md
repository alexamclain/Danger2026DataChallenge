# P25 Lane B: KSY-y Period Context

Updated: 2026-06-13 18:48 PDT

## Purpose

The KSY-y Siegel formula gate gives the exact four-layer payload.  This adapter
checks that the formula itself has the period-156 theta2 context required by
the value route.

## Result

For the exact KSY-y footprint:

```text
support period                    = 156
[2]^156 fixes the formula payload  = true
proper divisors of 156 fail        = true
gcd(4^156 - 1, p - 1)              = 1
ambient F_p value branches         = 11
```

Compact witnesses:

```text
telescoping budget = 975 cells
factor-period budget = 31 factor cells
```

Thus a value theorem for the KSY-y formula has a precise period-context witness
to supply.  With that context, the `F_p^*` root is unique.  Without it, the
ambient 780-period value route still has the `mu_11` ambiguity.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_ksy_y_period_context_rows=1/1
```

## Interpretation

This is not the arithmetic value theorem.  It says exactly what extra context a
value theorem must carry once it emits the KSY-y product.
