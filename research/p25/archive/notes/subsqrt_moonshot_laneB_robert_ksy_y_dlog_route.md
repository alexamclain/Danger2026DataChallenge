# P25 Lane B: Robert KSY-y / Kato-Siegel dlog Route Gate

Updated: 2026-06-13 13:54 PDT

## Purpose

This gate turns the latest Robert/Kato-Siegel scout into an executable finite
route policy.  The only live Robert/Siegel branch is a primitive level-`169`
normalized odd `y/wp'` or Kato-Siegel `dlog` translated finite-difference route.

The accepted finite shadow is:

```text
base * K_trace * D_segment * (1 - T)

base = (25,25)
K    = (57,0), length 25
D    = (22,3), length 3
T    = (38,113), quotient edge (2,113)
```

## Controls

The route gate keeps the positive route narrow:

```text
accepted odd y/dlog route       -> pass, support 150
edge-only translated quotient   -> fail, support 50 / quotient support 2
missing K trace                 -> fail, all 25 kernel modes exposed
inverse T                       -> fail, wrong orientation
even/x-like T                   -> fail, wrong signed bridge and scalar leak
D-boundary-only                 -> fail, support 100 / quotient support 4
split C13 shadow of T           -> fail, loses primitive C169 edge
literal subgroup divisor        -> fail, cannot supply D segment
canonical triangle              -> pass
split low/fiber triangle        -> fail
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_y_dlog_route_gate.py
```

Expected marker:

```text
robert_ksy_y_dlog_route_rows=1/1
```

## Interpretation

This is still not an arithmetic proof.  It says exactly what a Koo-Shin-Yoon
normalized `y/wp'` quotient or Kato-Siegel logarithmic derivative must realize
at the finite layer, and it kills the closest lower-effort escapes before they
can absorb more search time.
