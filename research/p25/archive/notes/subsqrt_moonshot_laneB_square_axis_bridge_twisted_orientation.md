# p25 Lane B Square-Axis Bridge Twisted Orientation

Updated: 2026-06-12

## Result

The degree-`39` half-orbit escape is now explicit: it is not ordinary descent,
but exactly a quadratic sign-twist problem.

On the collapsed primitive `C_507` coordinate:

```text
p^39 = -1 mod 507
positive bridge cells = 121, 122, 123
negative bridge cells = 384, 385, 386
p^39 pairs = (121,386), (122,385), (123,384)
```

Base/invariant coefficients on these pairs must be even:

```text
c(-q) = c(q)
```

That gives the unsigned hull, not the signed bridge.  The signed bridge is the
odd line:

```text
c(-q) = -c(q)
```

So the only support-preserving degree-`39` mechanism is to introduce an
anti-invariant coefficient `alpha` with:

```text
alpha^(p^39) = -alpha
```

Then `alpha * bridge` is semilinearly fixed by `p^39`, while the ordinary
trace of the literal signed bridge is zero.  Equal weights across the three
`S`-layer pairs impose two additional constraints, cutting the odd three-pair
space down to the single bridge line.

On the raw source cycle, `p^39 mod 12675 = 2027` swaps the positive and
negative raw bridge layers, while `p^78 mod 12675 = 2029` is invisible on the
collapsed quotient because it is `1 mod 507`; it only reindexes the full
`C_25` trace fibers.

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_twisted_orientation_gate.py
```

Expected row:

```text
square_axis_bridge_twisted_orientation_rows=1/1
```

## Continue / Kill

Continue the bridge route, but sharpen the target: a degree-`39` explanation
must be a quadratic sign local system plus the equal-weight `S`-layer bridge.
Kill ordinary invariant-coefficient half-orbit explanations; they produce the
unsigned hull or zero, not the signed six-cell bridge.  Literal `+/-1`
normalization still lives at degree `78` unless a producer supplies an
equivalent nonsplit identity.
