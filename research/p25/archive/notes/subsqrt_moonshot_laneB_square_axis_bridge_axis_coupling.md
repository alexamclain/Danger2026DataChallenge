# Subsqrt Moonshot Lane B Square-Axis Bridge Source-Axis Coupling

Date: 2026-06-12

## Result

The positive raw bridge trace rectangle is not an axis product in the actual
split source coordinates `C_75 x C_169`.

It is:

```text
base   = (25,25)
kernel = (57,0)
D      = (22,3)

positive = base + <kernel>_25 + {0,D,2D}
```

In source axes this is the union of three rectangles:

```text
right == 1 mod 3  x  c = 25
right == 2 mod 3  x  c = 28
right == 0 mod 3  x  c = 31
```

So the positive layer is a graph over the full `C_75` right axis: the `C_169`
singleton is determined by the right coordinate modulo `3`.

The negative layer is the bridge translate with the same shape:

```text
right == 0 mod 3  x  c = 138
right == 1 mod 3  x  c = 141
right == 2 mod 3  x  c = 144
```

## Falsifier

The positive right projection has all `75` right-source values, while the
positive `C_169` projection has only three values.  The axis product hull has
`75 * 3 = 225` cells, but the true positive support has only `75` cells.

Thus a producer that supplies only:

```text
right kernel trace
times
three C-axis values
```

overproduces by a factor of `3`.  The missing ingredient is the mixed
alignment by the `D=(22,3)` source-line step.

For the signed bridge, the axis product hull has `450` cells while the true
signed support has `150`.

## Consequence

A finite-field/Jacobi/modular-unit producer must recover the coupled graph:

```text
right mod 3  ->  selected C_169 singleton
```

It is not enough to match the kernel trace, the three C-values, or the spectral
zero pattern separately.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_axis_coupling_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_axis_coupling_gate.py
```
