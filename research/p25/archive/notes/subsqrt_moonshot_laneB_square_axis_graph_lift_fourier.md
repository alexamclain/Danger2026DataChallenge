# Subsqrt Moonshot Lane B Square-Axis Graph-Lift Fourier Gate

Date: 2026-06-12

## Result

The `C_169` boundary residual is exactly a skew graph lift of the `C_13`
trace-shadow mask.

Write:

```text
j = a + 13*b
h = right - a mod 3
```

Then:

```text
residual(right, a + 13*b) = C_13 trace bit at (right,a)
                             if b = 9 - 3*h
                             0 otherwise
```

The graph Fourier formula matches the full `C_3 x C_169` DFT coefficient by
coefficient:

```text
graph_formula_hits = 507 / 507
residual_support = 18 / 18
residual_fourier_nonzero = 505 / 505
```

The residual splits into three boundary slices:

```text
h = 0, b = 9, support = 3, row_sums = [1, 1, 1]
h = 1, b = 6, support = 6, row_sums = [2, 2, 2]
h = 2, b = 3, support = 9, row_sums = [3, 3, 3]
```

Each single slice is already Fourier-dense.  For every `h = 0,1,2`:

```text
fourier_nonzero = 505
by_right_frequency = [169, 168, 168]
pure_lift = 12
pure_nonlift = 156
mixed_lift = 24
mixed_nonlift = 312
right_only = 0
```

The slice support points are:

```text
h=0: [(0,12,129), (1,10,127), (2,11,128)]
h=1: [(0,8,86), (0,11,89), (1,9,87), (1,12,90), (2,7,85), (2,10,88)]
h=2: [(0,4,43), (0,7,46), (0,10,49),
      (1,5,44), (1,8,47), (1,11,50),
      (2,6,45), (2,9,48), (2,12,51)]
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_graph_lift_fourier_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_graph_lift_fourier_gate.py
```

Observed:

```text
square_axis_graph_lift_fourier_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_graph_lift_fourier_gate
```

## Consequence

The residual target is now a graph-lift problem:

```text
C_13 trace-shadow mask
embedded into C_169 along b = 9 - 3*(right - a mod 3)
```

This is a positive compression of the geometry, but not of the frequency
support.  Even one boundary slice, including the 3-point `h=0` slice, already
looks Fourier-dense on `C_3 x C_169`.  A proposed producer cannot be accepted
merely because it has full non-right character support; it has to recover the
skew graph placement itself.

The next producer-facing falsifier should therefore ask:

```text
does the arithmetic object produce the C_13 trace mask?
does it embed that mask on the three graph fibers b = 9,6,3?
does it place the h=0,1,2 slices with support counts 3,6,9?
```

This reframes the square-axis moonshot as a graph-lifted trace-shadow producer,
not as an unexplained 18-point residual.

The actual local-source exponent/residue footprint of the graph lift is
recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_local_graph_residue.md
```
