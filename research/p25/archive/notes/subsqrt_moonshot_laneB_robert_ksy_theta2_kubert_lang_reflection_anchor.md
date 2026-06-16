# P25 Lane B: Robert KSY Kubert-Lang Reflection Anchor

Updated: 2026-06-13 17:51 PDT

## Purpose

The row-pair permutation scan leaves three fixed-`T` cyclic row translates.
This gate asks which one is compatible with the anti-invariant reflection
identity:

```text
T = -2C
```

where `C` is the center of the positive `D` segment.

## Result

All three fixed-`T` translates share the same C-axis midpoint `c=28`, but only
one has the correct row coordinate for the center.

```text
positive_by_row=(25,28,31), negative_by_row=(141,144,138)
  base=(0,25), center=(1,28), -2C=(1,113), source fail

positive_by_row=(28,31,25), negative_by_row=(144,138,141)
  base=(2,25), center=(0,28), -2C=(0,113), source fail

positive_by_row=(31,25,28), negative_by_row=(138,141,144)
  base=(1,25), center=(2,28), -2C=(2,113), source pass
```

For the survivor:

```text
T       = (2,113)
C       = (2,28)
T/2     = (1,141)
-C      = (1,141)
base    = C-D = (1,25)
```

## Interpretation

The C-axis midpoint alone is insufficient: every fixed-`T` cyclic translate has
midpoint `c=28`.  The theorem source must recover the row of the
anti-invariant center `C=-T/2`, equivalently the identity `T=-2C` in
`C_3 x C_169`.

This is a theorem-facing anchor for the row-labeled pair contract.  A formula
that explains only the C-axis midpoint, the fixed `T` edge, or the elementary
Kubert-Lang congruences still misses the source-selected packet.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_anchor_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_reflection_anchor_rows=1/1
```
