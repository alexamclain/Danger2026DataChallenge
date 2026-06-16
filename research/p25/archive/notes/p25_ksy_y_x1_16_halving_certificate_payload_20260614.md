# P25 KSY-y X1(16) Halving-Certificate Payload Contract

Updated: 2026-06-14 12:13 PDT

## Purpose

The halving-chain contract records the extraction burden after a theorem reaches
the active surface:

```text
A, xP16
```

This note records what a compact, independently checkable finite payload may
look like.  A theorem or extraction routine does not need to reproduce the C
square-root branch order if it can instead provide an x-coordinate chain whose
links double back on the same Montgomery curve.

## Checkable Chain

For p25:

```text
active mode = x16halvenonsplit
start depth = 4
final depth = 42
halving links = 38
x-coordinate chain points = 39
```

The checkable chain is:

```text
x_4 = xP16, x_5, ..., x_42 = x0
```

For each link, `x_{i+1}` must double back to `x_i` on
`B*y^2 = x^3 + A*x^2 + x`.

In projective Montgomery xDBL form:

```text
C = (A + 2)/4
U = (X + Z)^2
V = (X - Z)^2
W = U - V
X' = U*V
Z' = W*(V + C*W)

require X' - x_i*Z' = 0
require Z' != 0
```

This proves a valid x-coordinate chain without proving that the active C loop
would have chosen each half first.

## Provenance Versus Submission

An active-path provenance payload is stronger.  It must include, for each
halving step:

```text
sqrt(d)
chosen u branch
sqrt(w)
candidate order
first-nonzero choice
```

That is useful for reproducing the exact `x16halvenonsplit` path, but it is not
the final challenge boundary.

Official `vpp.py` verification of `(p,A,x0)` remains the submission boundary.

## Route Classifier

```text
A,xP16 surface only:
  decision = surface_reached_certificate_missing
  missing  = x-chain, sqrt-witness chain, direct x0, or vpp-verified triple

branch word without values:
  decision = reject_branch_word_without_values
  missing  = actual square-root witnesses, x-chain, or x0

sqrt witness chain:
  decision = active_path_provenance_vpp_missing
  missing  = official vpp.py verification

x-coordinate chain:
  decision = checkable_x_chain_vpp_missing
  missing  = official vpp.py verification

direct A,x0:
  decision = direct_x0_vpp_missing
  missing  = official vpp.py verification

vpp-verified triple:
  decision = submission_ready
```

## Consequence

A cross-level theorem that emits `A,xP16` still needs one of three payloads:

```text
1. a 39-point x-coordinate chain from xP16 to x0;
2. an active square-root witness chain proving production-path provenance; or
3. a direct `(p,A,x0)` triple accepted by official vpp.py.
```

A branch word alone is not a certificate.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_x1_16_halving_certificate_payload_gate.py
```

Marker:

```text
ksy_y_x1_16_halving_certificate_payload_rows=1/1
```
