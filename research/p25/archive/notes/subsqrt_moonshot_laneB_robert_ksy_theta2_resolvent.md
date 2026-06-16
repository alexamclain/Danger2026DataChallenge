# P25 Lane B: Robert KSY / Kato-Siegel theta2 Resolvent Gate

Updated: 2026-06-13 14:28 PDT

## Purpose

The even-`D` gate showed that the Kato-Siegel-looking object has the finite
shape

```text
theta2 = 4*bridge - [2]bridge
```

where `[2]` is the doubling automorphism on `C_75 x C_169`.  Since `[2]` has
order `780`, the finite operator `(4 - [2])` is invertible by a geometric
resolvent.

## Result

The resolvent exactly recovers the bridge:

```text
(4 - [2])^-1 =
  (4^779 + 4^778[2] + ... + [2]^779) / (4^780 - 1)

theta2 = (4 - [2]) * bridge
resolvent(theta2) = bridge
resolvent(theta2_inverse) = -bridge
```

Cost profile:

```text
doubling order                 = 780
theta2 support                 = 300
shifted theta2 term budget     = 234000
shifted theta2 union support   = 11700
weighted numerator support     = 150
denominator bit length         = 1560
denominator nonzero mod p25    = true
term budget below sqrt(p)      = true
union support below sqrt(p)    = true
```

The recovered bridge passes the full existing bridge contract.

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_resolvent_gate.py
```

Expected marker:

```text
robert_ksy_theta2_resolvent_rows=1/1
```

## Interpretation

This upgrades the KSY/theta2 route from "needs unexplained doubled-layer
cancellation" to a finite constructive target:

1. emit the arithmetic `theta2` object;
2. apply the doubling resolvent below `sqrt(p)`;
3. justify division by `4^780 - 1` or scalar inversion modulo p25;
4. feed the recovered bridge into the existing certificate harness.

The remaining debt is arithmetic production and normalization, not source
geometry.
