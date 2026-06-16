# P25 Lane B: theta2 Factor-Period Certificate

Updated: 2026-06-13 15:00 PDT

## Purpose

The telescoping certificate checks `[2]^156 bridge = bridge` by pushing
expanded bridge/theta2 supports.  This note records a smaller factor-level
period certificate for the same KSY bridge:

```text
bridge = base * K_trace * D_segment * (1 - T)
```

with

```text
base = (25, 25)
K    = (57, 0)
D    = (22, 3)
T    = (38, 113)
```

## Result

At period `156`, doubling acts on `C_75 x C_169` by

```text
[2]^156 scale = (61, 1)
```

so the `C_169` coordinate is fixed.  The right-coordinate action is absorbed by
the 25-point `K` trace:

```text
base fixed                         = true
K generator maps to 11*K            = true
gcd(11, 25)                         = 1
K_trace fixed as a subgroup         = true

D maps to D + 10*K                  = true
T maps to T + 15*K                  = true
K_trace absorbs D drift             = true
K_trace absorbs T drift             = true

bridge factor product fixed         = true
theta2 fixed by bridge fixedness    = true
proper divisors of 156 fail         = true
```

Budget comparison for the period/fixedness subcheck:

```text
factor support budget               = 31
expanded telescoping subcheck budget = 900
floor improvement factor             = 29
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_factor_period_certificate_gate.py
```

Expected marker:

```text
robert_ksy_theta2_factor_period_certificate_rows=1/1
```

## Interpretation

The support period `156` is no longer just an observed orbit fact.  It has a
factor-level explanation: `[2]^156` preserves the actual bridge because the
only motion in `D` and `T` lies in the kernel trace already present in the
bridge producer.

This strengthens the compact verifier story.  A theorem-side KSY hit can carry
factor data plus these congruences for the period/fixedness part, then use the
telescoping certificate to recover the bridge.  It still does not supply the
missing arithmetic theta2 producer.
