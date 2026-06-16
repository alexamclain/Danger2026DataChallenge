# Subsqrt Moonshot Lane B Square-Axis Bridge Source-Affine Rigidity

Date: 2026-06-12

## Result

In actual local source-log coordinates, the bridge is rigid.

The six quotient bridge classes lift to a signed mask on `C_3 x C_169`:

```text
+ at (1,25), (2,28), (0,31)
- at (0,138), (1,141), (2,144)
```

Equivalently, on the six active C-source columns:

```text
columns = 25, 28, 31, 138, 141, 144
rank over F_2    = 3
rank over F_2029 = 3
```

The full product-affine action

```text
right -> alpha*right + beta       on C_3
c     -> u*c + v                  on C_169
```

has:

```text
sign-preserving stabilizer = identity only
sign-reversing symmetry    = inversion only: right -> -right, c -> -c
```

The only affine maps carrying the positive layer to the negative layer are:

```text
bridge translation: right -> right + 2, c -> c + 113
inversion:          right -> -right,    c -> -c
```

## Consequence

A source-side producer cannot hide the bridge by a product-affine coordinate
change, diamond action, or lower-rank source mask.  The same top-to-bottom edge
must be explained in source logs:

```text
(right,c) -> (right + 2, c + 113)
```

which is the source-log form of the multiplier `(45 mod151, 667 mod677)`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_source_affine_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_source_affine_rigidity_gate.py
```
