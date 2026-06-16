# Subsqrt Moonshot Lane B Robert X-Difference Evenness Obstruction

Date: 2026-06-13

## Result

The literal `x(Q)-x(P)` Robert table is the wrong finite object for the p25
bridge unless it is augmented by an oriented quotient, `y`/differential data,
a unit phase, or another sign-breaking mechanism.

Reason:

```text
x(-P) = x(P)
x(-Q) = x(Q)
```

so any scalar function of an x-only table is even under simultaneous source
inversion:

```text
(right, c) -> (-right, -c).
```

The p25 bridge is anti-invariant under that same involution.

## Finite Control

The gate builds a cyclotomic x-coordinate degeneration over `F_126751`:

```text
x_75(r)  = zeta_75^r  + zeta_75^-r
x_169(c) = zeta_169^c + zeta_169^-c
```

and checks the table:

```text
x_169(c) - x_75(r)
```

This control is inversion-even.  Its zero mask has only one point `(0,0)`,
and its quadratic-character mask is dense:

```text
quadratic distribution = {-1: 6274, 0: 1, 1: 6400}
```

Both fail the bridge harness.

## Producer Consequence

Do not spend the next Robert attempt producing a symmetric x-only table.  A
serious Robert/Siegel candidate must emit a signed or oriented source matrix
whose anti-invariant part survives and then pass:

```text
research/p25/p25_laneB_robert_source_matrix_harness_gate.py --source-matrix PATH
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_robert_x_difference_even_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_x_difference_even_obstruction_gate.py
```
