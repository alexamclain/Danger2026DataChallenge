# P25 Lane B: Robert KSY Kubert-Lang Raw Reflection-Orientation Contract

Updated: 2026-06-13 18:10 PDT

## Purpose

The raw reflection-gauge contract records representative freedom for the
forward anti-invariant product.  This gate records the orientation freedom:
formula sources may emit theta2 or theta2-inverse depending on whether they
use `C` or `-C`, and whether the product is written forward or reversed.

## Branches

```text
C,  y(A)/y(-A)  -> theta2 inverse
C,  y(-A)/y(A)  -> theta2
-C, y(A)/y(-A)  -> theta2
-C, y(-A)/y(A)  -> theta2 inverse
```

Raw centers:

```text
C  = (47,28)
-C = (28,141)
```

Each branch has:

```text
center kernel gauges = 25
oriented D gauges    = 50
primitive K choices  = 20
presentations        = 25000
```

Therefore:

```text
theta2-inverse raw presentations = 50000
theta2 raw presentations         = 50000
total accepted raw presentations = 100000
```

## Controls

```text
wrong center C=(47,29)       fail
wrong D=(22,4)               fail
nonprimitive K multiplier 5  fail
```

## Candidate Intake

Forward orientation:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1
```

Reverse orientation:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate.py \
  --center-right 47 --center-c 28 --d-right 22 --d-c 3 \
  --k-multiplier 1 --reverse
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_rows=1/1
```

## Interpretation

A theorem source may produce either theta2 or theta2-inverse.  The verifier
path already accepts both.  What matters is that the source lands in one of
the four oriented anti-invariant branches with kernel-gauge `C`, oriented
kernel-gauge `D`, and primitive `K`.
