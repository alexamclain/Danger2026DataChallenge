# P25 Lane B: Robert KSY Kubert-Lang Reflection Center Contract

Updated: 2026-06-13 17:55 PDT

## Purpose

This is a compact theorem-output intake for sources that naturally emit the
anti-invariant center and D segment rather than the six quotient cells.

Accepted quotient payload:

```text
C = (2,28)
D = (1,3)
primitive K multiplier mod 25
```

The checker derives:

```text
base = C-D  = (1,25)
T    = -2C  = (2,113)
T/2  = -C   = (1,141)
```

It then reuses the quotient-factor certificate, source-packet contract, and
row-labeled pair contract.

## Result

```text
target C=(2,28), D=(1,3), K primitive -> pass
primitive K multiplier 2              -> pass
nonprimitive K multiplier 5           -> fail

wrong center row C=(0,28) -> derives T=(0,113), fail
wrong center row C=(1,28) -> derives T=(1,113), fail
wrong center c  C=(2,29) -> derives T=(2,111), fail
wrong D         D=(1,4)  -> fail
```

Expected marker:

```text
robert_ksy_theta2_kubert_lang_reflection_center_contract_rows=1/1
```

## Candidate Intake

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_reflection_center_contract_gate.py \
  --center-right-class 2 --center-c 28 --d-right-class 1 --d-c 3 \
  --k-multiplier 1
```

## Interpretation

This is now the smallest quotient-level row-anchor target:

```text
center C, step D, primitive K
```

A theorem source does not need to emit `base` or `T` separately if it proves the
reflection-center data.  But it must recover the row of `C`, not only the
C-axis midpoint, because the wrong center rows derive the wrong reflection
edge and fail all finite contracts.
