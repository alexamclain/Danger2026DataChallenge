# Subsqrt Moonshot Lane B Square-Axis Bridge Axis-Hull Character Gap

Date: 2026-06-12

## Result

The previous checkpoint showed that the positive bridge layer is a graph in
`C_75 x C_169`, not an axis product.  This checkpoint records the dual
character-space obstruction.

Work after the `25`-point right-kernel trace, so the visible source group is
`C_3 x C_169`.

The true positive graph has three points:

```text
(right,c) = (1,25), (2,28), (0,31)
```

The tempting axis-product hull is:

```text
right in C_3
c in {25,28,31}
```

Both have all `168` nontrivial pure `C_169` characters.  But the axis hull has
no mixed right/C characters, while the true graph has all:

```text
2 * 168 = 336
```

mixed characters.

The same gap holds for the signed bridge:

```text
true signed bridge:       336 mixed right/C characters
signed axis-product hull:   0 mixed right/C characters
```

## Consequence

A separated local factor of the form:

```text
right trace
times
C-axis selector
```

can match the pure `C_169` shadow, but it misses the entire mixed right/C
payload.  It also overproduces support: the positive hull has `9` quotient
cells instead of `3`, and the signed hull has `18` cells instead of `6`.

So the producer must realize the `D=(22,3)` aligned graph itself.  Matching the
three C-values, the right trace, or the pure C Fourier payload separately is
not enough.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_axis_hull_character_gap_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_axis_hull_character_gap_gate.py
```
