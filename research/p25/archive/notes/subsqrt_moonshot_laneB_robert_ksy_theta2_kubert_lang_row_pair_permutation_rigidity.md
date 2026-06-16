# P25 Lane B: Robert KSY Kubert-Lang Row-Pair Permutation Rigidity

Updated: 2026-06-13 17:48 PDT

## Purpose

The row-labeled pair contract says a theorem source must emit:

```text
row 0: c31 - c138
row 1: c25 - c141
row 2: c28 - c144
```

This gate scans every packet with the same visible `C_169` projection and one
positive/negative C-cell per row.

## Scan

```text
positive cells = 25,28,31
negative cells = 138,141,144
row permutations scanned = 3! * 3! = 36
```

Results:

```text
C-axis projection hits = 36
KL congruence hits     = 36
balanced hits          = 36
D-segment/T-edge hits  = 9
fixed-T hits           = 3
exact base/D/T hits    = 1
source-contract hits   = 1
trace-correct hits     = 1
```

The fixed-`T` survivors are the three cyclic row translates:

```text
positive_by_row=(25,28,31), negative_by_row=(141,144,138) -> fail
positive_by_row=(28,31,25), negative_by_row=(144,138,141) -> fail
positive_by_row=(31,25,28), negative_by_row=(138,141,144) -> pass
```

## Interpretation

The elementary Kubert-Lang screen is saturated on this family: it cannot
distinguish any of the `36` pair permutations.  Fixed `T` recovers only the
three cyclic translates.  The primitive-K source contract selects the single
target translate.

A theorem hit must therefore explain the exact row translate selected by the
source contract.  It is not enough to explain the `C_169` projection, one
signed pair per row, exponent balance, or elementary KL congruences.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_gate.py
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_row_pair_permutation_rigidity_rows=1/1
```
