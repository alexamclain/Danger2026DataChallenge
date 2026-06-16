# Subsqrt Moonshot Lane B Robert/Siegel Translated Odd Quotient Skeleton

Date: 2026-06-13

## Result

The targeted Robert/Siegel literature hit now has a finite skeleton gate.

The exact source shape is:

```text
base * K_trace * D_segment * (1 - T)
```

with:

```text
base = (25,25)
K    = (57,0), length 25
D    = (22,3), length 3
T    = (38,113), quotient edge (2,113)
```

This is the finite shadow expected from a translated odd quotient such as:

```text
Dtheta(P+T) / Dtheta(P-T)
y(P+T) / y(P-T)
```

## Controls

The gate checks the important near misses:

```text
K_trace * (1 - T) only:
  raw support = 50
  quotient support = 2
  killed as too small

K_trace * D_segment * (1 - T):
  raw support = 150
  quotient support = 6
  exact bridge

K_trace * D_segment * (1 - T^-1):
  raw support = 150
  quotient support = 6
  killed as wrong orientation

K_trace * D_segment * (1 - T)(1 - T^-1):
  raw support = 225
  quotient support = 9
  killed as even-pair symmetrization

K_trace * D_segment * (1 - T)^2:
  raw support = 225
  quotient support = 9
  killed as squared-edge symmetrization

D_segment * (1 - T) without K_trace:
  raw support = 6
  all 25 kernel modes
  12 raw-relation mismatches
  killed as missing kernel trace
```

## Consequence

A Robert/Siegel candidate must not be merely a point translated quotient,
x-only even quotient, inverse edge, or pre-symmetrized `12N`-power style edge.

It must emit:

```text
D_segment + K_trace + translated odd edge (1 - T)
```

before it is fed to the source-matrix harness.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_skeleton_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_translated_odd_quotient_skeleton_gate.py
```
