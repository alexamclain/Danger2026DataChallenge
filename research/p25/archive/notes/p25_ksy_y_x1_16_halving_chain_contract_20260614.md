# P25 KSY-y X1(16) Halving-Chain Contract

Updated: 2026-06-14 12:07 PDT

## Purpose

The Montgomery-chart contract stops at the active production surface:

```text
A, xP16
```

This note records the remaining extraction burden.

For p25:

```text
p = 10^25 + 13
sqrt_floor = 3162277660168
k = 42
active mode = x16halvenonsplit
active start depth = 4
active halving steps = 42 - 4 = 38
```

The optional d-gate route starts from a certified first half:

```text
optional mode = x16halvenonsplitdgate
optional start depth = 5
optional halving steps = 42 - 5 = 37
```

## One Halving Step

Given a Montgomery surface point with x-coordinate `x`, the production code
uses:

```text
d = x^2 + A*x + 1
sqrt(d) required

u = 2*x + 2*sqrt(d)
or
u = 2*x - 2*sqrt(d)

w = u^2 - 4
sqrt(w) required

candidate halves:
  (u + sqrt(w))/2
  (u - sqrt(w))/2
```

The active `x16halvenonsplit` route takes the first nonzero candidate in the
C loop order.  The `x16halvefull` control explores all distinct halves.

## Route Classifier

```text
A,xP16 surface only:
  decision = surface_reached_halving_chain_missing
  missing  = 38 active first-branch halvings or direct x0

active first-branch chain to x0:
  decision = x0_extracted_official_vpp_missing
  missing  = official vpp.py verification

any valid halving chain to x0:
  decision = x0_extracted_not_active_path_vpp_missing
  missing  = official vpp.py verification; active-path provenance optional

direct A,x0 without chain:
  decision = direct_x0_official_vpp_missing
  missing  = official vpp.py verification

internal verify128 only:
  decision = internal_verify_not_submission
  missing  = official vpp.py verification and archive

official vpp.py verified triple:
  decision = submission_ready
```

## Consequence

A moonshot theorem that reaches `A,xP16` has not yet closed extraction.  It
must either:

```text
1. provide the 38-step active halving chain from xP16 to x0;
2. provide some valid x0 that official vpp.py accepts; or
3. directly output a vpp.py-verified (p,A,x0) triple.
```

The active first-branch chain is useful provenance, but official `vpp.py`
verification is the final submission boundary.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_16_halving_chain_contract_gate.py
```

Marker:

```text
ksy_y_x1_16_halving_chain_contract_rows=1/1
```
