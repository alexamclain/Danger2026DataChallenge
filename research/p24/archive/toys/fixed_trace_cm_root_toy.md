# Fixed-Trace CM Root Toy

This records the small correction to the Waterhouse/Mestre fixed-trace
escape hatch.

## Toy

For

```text
p = 103
t = 8
D_K = -87
t^2 - 4p = -348 = 4D_K
```

the ordinary fixed-trace isogeny class is the small conductor-2 analogue of
the p24 strict traces.  Enumerating all nonsingular short Weierstrass curves
over `F_103` gives:

```text
H_{-87} roots mod p:
  [5, 29, 32, 43, 60, 70]

H_{-348} roots mod p:
  [4, 44, 62, 63, 85, 86]

fixed |t|=8 j-values:
  [4, 5, 29, 32, 43, 44, 60, 62, 63, 70, 85, 86]
```

So:

```text
fixed_trace_j_set = roots(H_{D_K}) union roots(H_{4D_K}) mod p.
```

The script is:

```text
p24/fixed_trace_cm_root_toy.py
```

## Interpretation

Waterhouse/Rueck/Voloch-style theorems and Mestre-style point-counting tricks
describe or use fixed isogeny classes.  Over a fixed prime, constructing one
curve in that isogeny class still means choosing an embedded CM root from the
allowed endomorphism orders on the volcano.

For p24 the strict traces satisfy

```text
t^2 - 4p = 4D_K
```

with `|D_K|` comparable to `p`.  Thus fixed trace does not supply a separate
sub-sqrt selector; it restates the target as conductor-2 large-discriminant CM
root selection.
