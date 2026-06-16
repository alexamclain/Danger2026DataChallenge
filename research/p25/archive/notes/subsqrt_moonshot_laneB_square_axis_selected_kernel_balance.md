# Subsqrt Moonshot Lane B Square-Axis Selected-Kernel Balance

Date: 2026-06-12

## Result

The selected-defect kernel is larger than the global scalar kernel.  It consists
of functions that are constant in the `C_169` direction separately on each of
the three right rows.

This gives a less dense degree-zero representative than global scalar balance.
For the correction `-A`, where

```text
A = (1 + D + D^2) * X^3 * Y = {138,310,482},
```

degree zero only requires

```text
row_constant_0 + row_constant_1 + row_constant_2 = 3/169.
```

The minimum support solution has one dense row plus the two remaining anomaly
points:

```text
support = 169 + 1 + 1 = 171
raw block support = 25 * 171 = 4275.
```

So row-constant balance improves on the fully dense scalar support `507`, but
it is still a whole-row correction, not a local repair.

## Obstruction

A row-constant term is invisible to selected-defect, so the visible diagonal
defect is unchanged.  The selected-defect value identities still fail.

The raw producer contract also fails for every row-constant choice.  A fixed
right-zero inversion witness is enough:

```text
g(0,1) + g(0,-1)      = 2 * row_constant_0
g(0,46) + g(0,-46)    = 2 * row_constant_0 - 1.
```

These cannot be equal in the odd fields used by the quotient or raw split
checks.

## Producer Consequence

The selected-defect kernel does not rescue scalar balance.  It offers a
one-row-dense degree repair, but it leaves the selected-defect anomaly visible
and violates the raw inversion condition.

A viable producer still needs a genuinely mixed correction for the fixed
`h=2,t=1` slice, not a row-constant selected-kernel term.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_selected_kernel_balance_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_selected_kernel_balance_gate.py
```
