# P25 KSY-y Yang Y507 Modular-Period Certificate

Updated: 2026-06-14 09:02 PDT

## Purpose

The quotient normalized-y descent reduced the raw KSY-y footprint to:

```text
Y_507 = [2]^*U_507 / U_507^4
```

This checkpoint certifies `Y_507` itself as the compact theorem target: a
Yang/Yu modular unit on `X_1(507)` with exact doubling period `156`.

## Modular-Unit Certificate

`Y_507` has quotient exponents:

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

Yang odd-level congruences:

```text
sum e_g mod 12    = 0
sum g^2 e_g mod 507 = 0
```

Yang/Yu signed orbit condition:

```text
signed orbit bad counts:
  3  -> 0
  13 -> 0
```

Controls:

```text
unsigned orbit bad counts:
  3  -> 12
  13 -> 12

general even-level controls fail:
  sum g e_g mod 2     = 1
  sum g^2 e_g mod 2N  = 507
```

## Period Certificate

```text
minimum doubling period of Y_507 = 156
[2]^156 fixes Y_507              = true
proper divisors of 156 fail      = true
gcd(4^156 - 1, p - 1)            = 1
gcd(4^780 - 1, p - 1)            = 11
```

So the compact quotient target carries the same support-period root uniqueness
needed by the value route.

## Verdict

Positive payload:

```text
Y_507 is a Yang/Yu modular unit on X_1(507) with exact doubling period 156 and
unique F_p^* root at the support period
```

First missing clause:

```text
no source theorem yet gives the finite-field value/divisor identity for Y_507
or extracts a DANGER3 triple
```

Practical effect:

```text
future theorem hits should prove the value/divisor identity for Y_507, not
merely its modular-unit admissibility
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_modular_period_certificate_gate.py
```

Marker:

```text
ksy_y_yang_y507_modular_period_certificate_rows=1/1
```
