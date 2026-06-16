# Subsqrt Moonshot Lane B Square-Axis Bridge Character-Coset Obstruction

Date: 2026-06-12

## Result

The bridge graph is not a single character level set or a proper subgroup
coset.

After the `25`-point kernel trace, the visible positive bridge is:

```text
C_3 x C_169
base = (1,25)
D    = (1,3)
support = base + {0,D,2D}
```

The step `D=(1,3)` has full order `507` in `C_3 x C_169`.  Therefore any
subgroup coset containing even two adjacent `D`-points is the whole group.

Every single-character level set of size `3` in `C_3 x C_169` is instead a
horizontal fixed-`c` coset:

```text
C_3 x {c}
```

The bridge graph has three different `C_169` values, so it is none of these.

The same obstruction holds before quotienting the kernel:

```text
C_75 x C_169
base   = (25,25)
kernel = (57,0)
D      = (22,3)
support = base + <kernel>_25 + {0,D,2D}
```

Here `D=(22,3)` has full order `12675`.  Every character level set of size
`75` is a fixed-`c` horizontal `C_75` coset, while the bridge trace rectangle
uses three `C_169` values.

## Consequence

A simple local character selector cannot produce the bridge graph.  It can
select a fixed `C_169` value, or it can select the axis-product hull after a
union of three such cosets, but it cannot select the `D`-aligned graph.

So a candidate finite-field/Jacobi/modular-unit producer must realize a short
`D` segment, or an equivalent mixed identity.  A single character equation,
proper quotient, subgroup coset, or fixed-`c` selector is not enough.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_character_coset_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_character_coset_obstruction_gate.py
```
