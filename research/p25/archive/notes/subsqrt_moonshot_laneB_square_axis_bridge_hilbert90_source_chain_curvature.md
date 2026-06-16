# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Curvature

Date: 2026-06-12

## Result

The support-`3` Hilbert-90 antiderivative chains are now classified as source
graphs.  The four best witnesses from masks `1` and `6` form one
product-affine source orbit, but they are not source lines, arithmetic
progressions, or affine disguises of the known `D` segment.

Canonical witness:

```text
A = -[0] - [172] - [482]
source coordinates:
  0   -> (0,0)
  172 -> (1,3)
  482 -> (2,144)
row graph over C_169:
  c(0),c(1),c(2) = 0,3,144
cyclic first differences:
  3,141,25
curvature:
  144 - 2*3 + 0 = 138 mod 169
```

The curvature is primitive:

```text
gcd(138,169) = 1
```

The `C_13` shadow already sees curvature:

```text
(0,3,144) mod 13 = (0,3,1)
1 - 2*3 + 0 = 8 mod 13
```

So this is not a uniform `C_13` shadow hiding a linear `C_169` lift.

The four witnesses are source-affine equivalent:

```text
mask 1, direction 197:  -[0]   -[172] -[482]
mask 1, direction 310:   [172] +[197] +[369]
mask 6, direction 197:  -[138] -[310] -[335]
mask 6, direction 310:   [0]   +[25]  +[335]
```

Each has unit `C_169` curvature, nonzero `C_13` curvature, zero arithmetic
progression presentations in `C_507`, and zero product-affine maps to the
standard `D` segment `{0,172,344}`.

## Interpretation

The positive target is smaller than before, but not easier in the naive way.
The producer should not look for a line segment or ordinary source AP.  It
must realize a curved three-point source graph, then take the primitive
first-boundary direction `197/310`, then the nonsplit Hilbert-90/inversion
boundary.

Current target shape:

```text
curved 3-point graph A
F = (1 - T_197) A
bridge = (1 - inversion) F
```

This preserves the moonshot while narrowing the falsifier: kill any candidate
that linearizes this chain into a source line, AP, or affine `D` segment.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_curvature_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_curvature_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_curvature_rows=1/1
```
