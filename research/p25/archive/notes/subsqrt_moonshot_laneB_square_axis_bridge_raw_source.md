# Subsqrt Moonshot Lane B Square-Axis Bridge Raw Source

Date: 2026-06-12

## Result

The unique bridge

```text
S * X * Y^-2 * (1 - X^2Y^3)
```

has a concrete raw local-source lift in the square-axis lab.  Its
kernel-trivial lift has:

```text
quotient support = 6
raw support = 150 = 6 * 25
kernel mode support = {0}
```

Each bridge quotient class lifts to exactly `25` raw exponents.  As with the
residual classes, each class is one `mod677` C-source singleton times one
`25`-element `mod151` right-source coset.

## Source Edge

The bridge step is:

```text
X^2Y^3 = 113
```

On the actual local sources, this is a fixed multiplier on every one of the
`25` trace-kernel layers:

```text
mod151 right source multiplier = 45
mod677 C source multiplier     = 667
```

Equivalently, the step has source-log increments:

```text
right source log mod 75 = 38
C source log mod 169    = 113
```

The three partner-to-anomaly edges all use this same multiplier on all `25`
kernel layers.

## Consequence

The producer target is now fully local on the raw source cycle: it must realize
a block-constant `150`-point signed edge, not a sparse trace-correct section or
a hidden `C_25` kernel phase.  A useful candidate should explain the fixed
source multiplier `(45,667)` carrying the top trace-zero partner slice to the
bottom trace-one anomaly slice.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_raw_source_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_raw_source_gate.py
```
