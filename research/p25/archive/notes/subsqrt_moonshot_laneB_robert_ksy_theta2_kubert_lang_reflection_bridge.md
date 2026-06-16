# P25 Lane B: Robert KSY Kubert-Lang Reflection Bridge

Updated: 2026-06-13 16:56 PDT

## Purpose

The KL inversion-pair gate says the elementary Siegel congruence screen sees
anti-invariant atoms `z^a-z^-a`, while the KSY normalized-y product is written
as three parallel `T` edges.

This gate proves the bridge between those descriptions.

## Geometry

Let:

```text
base = (1,25)
D    = (1,3)
T    = (2,113)
C    = base + D = (2,28)
```

Then:

```text
T = -2C
T/2 = -C = (1,141)
```

The positive segment is symmetric around `C`:

```text
C-D = (1,25)
C   = (2,28)
C+D = (0,31)
```

The KSY `T` denominators are:

```text
C-D+T = -C-D = (0,138)
C+T   = -C   = (1,141)
C+D+T = -C+D = (2,144)
```

The inversion-pair denominators are:

```text
-(C-D) = -C+D = (2,144)
-C     = -C   = (1,141)
-(C+D) = -C-D = (0,138)
```

So the two denominator sets are identical; the outer factors are swapped.

## Consequence

As signed divisors:

```text
prod_{j=-1,0,1} [C+jD] / [C+jD+T]
  =
prod_{j=-1,0,1} [C+jD] / [-C-jD]
```

The left side is the KSY `T`-edge normalized-y packet.  The right side is the
anti-invariant inversion-pair packet preferred by the KL/Siegel congruence
screen.

Controls reject the shortcuts:

```text
truncated length-two segment
wrong T
shifted center
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_bridge_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_reflection_bridge_rows=1/1
```

## Interpretation

This is a positive bridge for theorem search.  A Kubert-Lang/Sprang/Robert
source can target anti-invariant pair quotients over the symmetric segment
`C-D,C,C+D`, then use `T=-2C` to identify the product with the KSY
normalized-y/theta2 payload.

The remaining debt is still arithmetic legality: prove such anti-invariant
pairs exist in a challenge-legal finite-field/modular-unit identity, and keep
the forced `K` trace plus period-156 theta2 certificate.
