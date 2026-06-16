# Subsqrt Moonshot Lane B Robert/Siegel Translated Odd Quotient Rigidity

Date: 2026-06-13

## Result

The visible quotient skeleton:

```text
base * D_segment * (1 - T)
```

is rigid on `C_3 x C_169`.

The positive bridge layer is:

```text
(0,31), (1,25), (2,28)
```

The negative bridge layer is:

```text
(0,138), (1,141), (2,144)
```

Scanning every nonzero `D` direction and translated edge `T` gives exactly
two factorizations:

```text
base=(1,25), D=(1,3),   T=(2,113)
base=(0,31), D=(2,166), T=(2,113)
```

The second is only the reversal of the same recorded `D=(1,3)` segment.

## Consequence

There is no alternate visible AP segment and no alternate translated odd edge.
A Robert/Siegel producer must recover:

```text
D = (1,3) up to reversal
T = (2,113)
```

before the raw `K_trace` lift.

This narrows the Kato-Siegel / `y`-quotient target further: the arithmetic
object cannot use a different local segment and hope to pass after kernel
trace or source-matrix conversion.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_rigidity_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_translated_odd_quotient_rigidity_gate.py
```
