# P25 Lane B: Robert KSY Kubert-Lang Raw Orientation Value Route

Updated: 2026-06-13 18:16 PDT

## Purpose

The raw orientation certificate router handles divisor/additive payloads.  This
gate records what is required if a theorem source emits finite-field unit
values instead.

## Result

For the accepted theta2 support period:

```text
support period                         = 156
bit length of 4^156 - 1                = 312
gcd(4^156 - 1, p - 1)                  = 1
gcd(4^156 - 1, p + 1)                  = 3
gcd(4^156 - 1, 126751 - 1)             = 2535
gcd(4^156 - 1, 2029 - 1)               = 507
proper period shortcuts                = all fail
```

For the old ambient period:

```text
ambient period                         = 780
gcd(4^780 - 1, p - 1)                  = 11
F_p value branches                     = 11
```

Thus a value-level theorem hit is viable over `F_p` only if it supplies the
period-156 theta2 context, fixedness, or telescoping.  Then the `F_p^*` root is
unique.  Without that period-156 context, the ambient route still has the
`mu_11` branch ambiguity.

## Branches

```text
C forward        emits theta2 inverse, sign -1
C reverse        emits theta2,         sign +1
-C forward       emits theta2,         sign +1
-C reverse       emits theta2 inverse, sign -1
```

All four divisor/additive routes remain valid through the existing certificate
router.  The value-level branch adds the period-156 obligation.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_orientation_value_route_rows=1/1
```

## Interpretation

This separates two theorem-output types:

```text
divisor/additive theta2 data -> current certificate router is enough
finite-field unit values     -> must include period-156 theta2 fixedness
```

The missing theorem may be a value identity, but it must land on the support
period, not the ambient period.
