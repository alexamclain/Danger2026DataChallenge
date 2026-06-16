# P25 Lane B: theta2 Support-Period Resolvent

Updated: 2026-06-13 14:48 PDT

## Purpose

The first theta2 resolvent used the ambient doubling order `780` on
`C_75 x C_169`.  The actual bridge/theta2 support has smaller doubling period
`156`, so the active finite filter can be shorter:

```text
(4 - [2])^-1 on the support =
  (4^155 + 4^154[2] + ... + [2]^155) / (4^156 - 1)
```

## Result

```text
ambient doubling order on C_75 x C_169 = 780
bridge doubling orbit period           = 156
theta2 doubling orbit period           = 156

denominator bit length                 = 312
denominator nonzero mod p25            = true
gcd(4^156 - 1, p25 - 1)                = 1
gcd(4^156 - 1, p25 + 1)                = 3
gcd(4^156 - 1, 126751 - 1)             = 2535
gcd(4^156 - 1, 2029 - 1)               = 507

shifted theta2 union support           = 11700
shifted theta2 term budget             = 46800
weighted exponent bit budget           = 7300800
recovered bridge passes contract       = true
```

All proper period-divisor shortcuts fail to recover the bridge.  In fact, for
each proper divisor of `156`, the numerator is not exactly divisible by
`4^m - 1`.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_support_resolvent_gate.py
```

Expected marker:

```text
robert_ksy_theta2_support_resolvent_rows=1/1
```

## Interpretation

The active theta2 filter should use support period `156`, not ambient order
`780`.  This cuts the shifted-term budget by factor `5` and removes the
`F_p^*` value-level root ambiguity because `4^156 - 1` is invertible modulo
`p25 - 1`.
