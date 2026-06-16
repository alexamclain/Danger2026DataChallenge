# Subsqrt Moonshot Lane B Robert Oriented-Phase Contract

Date: 2026-06-13

## Result

The Robert lane now has a sharper finite target than "add an orientation."

The p25 bridge signs on `C_75 x C_169` are exactly a C-side odd phase on the
three active C-pairs:

```text
positive C-values: 25, 28, 31
negative C-values: 138, 141, 144 = -31, -28, -25 mod 169
```

Multiplying the coupled unsigned bridge hull by this C-odd phase recovers the
signed bridge.  But this phase alone is not a producer: applying it to the
separated right-trace-times-C hull overproduces support `450` and has zero
mixed right/C character payload.

## Consequence

A successful Robert/Siegel producer needs both:

```text
1. coupled unsigned support/magnitude:
   the D-segment/K-trace source graph, not a separated C selector

2. oriented C-side phase:
   a quotient, y/differential datum, or unit phase odd under c -> -c
```

Row-only orientation is impossible because every raw right row contains both a
positive and a negative bridge point.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_oriented_phase_contract_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_oriented_phase_contract_gate.py
```
