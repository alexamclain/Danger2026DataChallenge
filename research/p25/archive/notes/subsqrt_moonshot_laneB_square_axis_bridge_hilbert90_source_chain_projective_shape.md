# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Projective Shape

Date: 2026-06-12

## Result

The curved Hilbert-90 source chain has a specific projective triangle shape in
`C_3 x C_169`.

For the canonical chain:

```text
A = -[0] - [172] - [482]
source row values c(0),c(1),c(2) = 0,3,144
cyclic first differences = 3,141,25
```

Under product-affine source changes, meaning row affine changes in `C_3` and
unit/translation changes in `C_169`, the projective difference shape has normal
form:

```text
C_169 projective shape = (1,18,150)
C_13 projective shadow = (1,2,10)
```

All four bridge-compatible source chains have this same `C_169` and `C_13`
projective shape.  The projective orbit sizes are maximal:

```text
C_169 orbit size = 6 * phi(169) = 936
C_13 orbit size  = 6 * phi(13)  = 72
```

So the shape has no hidden product-affine projective stabilizer.

## Lift Warning

The `C_13` shadow is not enough.  Enumerating all primitive-curvature
projective difference shapes over `C_169` gives:

```text
primitive C_169 projective shape orbits = 32
```

Their `C_13` shadows collapse to four projective shapes:

```text
(0,1,12): 7 lifts
(1,1,11): 7 lifts
(1,2,10): 13 lifts
(1,3,9):  5 lifts
```

The bridge chain's `C_13` shadow `(1,2,10)` has thirteen primitive `C_169`
lifts:

```text
(1,2,166)
(1,4,164)
(1,5,163)
(1,7,161)
(1,8,160)
(1,10,158)
(1,15,153)
(1,18,150)   <- bridge chain
(1,30,138)
(1,31,137)
(1,43,125)
(1,49,119)
(1,57,111)
```

## Interpretation

The producer target is now more specific:

```text
specific C_169 projective triangle shape (1,18,150)
specific first-boundary orientation 197/310
inversion / Hilbert-90 boundary to the signed bridge
```

Matching the `C_13` curvature or projective shape is only a shadow.  It leaves
thirteen primitive `C_169` projective lifts, so a candidate still has to
realize the nonsplit lift selected by the actual p25 source coordinates.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_projective_shape_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_projective_shape_rows=1/1
```
