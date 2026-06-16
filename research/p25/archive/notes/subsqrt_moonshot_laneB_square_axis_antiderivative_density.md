# Subsqrt Moonshot Lane B Square-Axis Antiderivative Density

Date: 2026-06-12

## Result

The signed-`D` boundary clue has a sharp quotient-linear obstruction.

Let

```text
A = (1 + D + D^2) * X^3 * Y = {138,310,482}.
```

Then

```text
(1 - D)A = X^3Y - X^3Y^2.
```

Because `D=172` generates the full `C_507` quotient cycle, every solution to
this first-difference equation is `A + c`.  The sparse local solution `A` has
support `3`, but degree `3`.

Forcing degree zero fixes the scalar:

```text
c = -3/507.
```

That scalar is nonzero, so the degree-zero antiderivative is dense on all
`507` quotient classes.

For the correction `-A`, the degree-zero representative is exactly:

```text
-A + (3/507) * 1_{C_507}.
```

This is the scalar-balance escape already seen by the selected-defect gate.
Its block lift has full raw support `12675/12675`.

## Producer Consequence

The antiderivative clue is real, but a quotient-linear modular-unit repair does
not give a local degree-zero correction.  It collapses back to dense scalar
balancing, and the scalar disappears under selected-defect.

So the next positive path cannot merely say "take the `D` antiderivative."
It needs a non-quotient-linear or genuinely raw source mechanism that supplies
the local `D`-antiderivative behavior without reducing to dense scalar balance.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_antiderivative_density_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_antiderivative_density_gate.py
```
