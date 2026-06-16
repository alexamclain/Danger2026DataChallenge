# P25 Lane B: Robert KSY Kubert-Lang Raw Reflection-Gauge Contract

Updated: 2026-06-13 18:05 PDT

## Purpose

The quotient reflection-center contract accepts:

```text
C = (2,28)
D = (1,3)
primitive K
```

A theorem source may instead emit raw representatives in `C_75 x C_169`.  This
gate records the exact raw representative freedom for the centered
anti-invariant product.

## Accepted Raw Payload

```text
raw C = (47,28) + aK
raw D = +/-(22,3) + bK
K     = primitive multiplier of (57,0)
a,b mod 25
```

All such choices give the same full K-traced center set and the same
anti-invariant theta2 footprint.

## Counts

```text
center kernel gauges                 = 25
forward D kernel gauges              = 25
reversed D kernel gauges             = 25
oriented D gauges                    = 50
combined center/D oriented gauges    = 1250
primitive K multipliers              = 20
equivalent raw parameter presentations = 25000
```

## Controls

```text
target C=(47,28), D=(22,3), K primitive       pass
primitive K multiplier 2                      pass
D reversal D=(53,166)                         pass
nonprimitive K multiplier 5                   fail
collapsed K multiplier 0                      fail
center plus D / C-axis / right-axis shifts    fail
D plus C-axis / right-axis shifts             fail
```

For the target raw center, the fixed raw bridge edge satisfies:

```text
T - (-2C) = K
```

For other kernel-gauge centers, the difference remains a kernel shift and is
absorbed by the full K trace.

## Candidate Intake

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 --k-multiplier 1
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_reflection_gauge_contract_rows=1/1
```

## Interpretation

This is the raw-level theorem landing pad.  If a formula emits raw
representatives, it does not need to hit the displayed representative exactly;
kernel-gauge shifts of `C`, kernel-gauge shifts of `D`, D reversal, and
primitive K generator changes are harmless.  Non-kernel shifts and nonprimitive
K are not.
