# p25 Lane B Square-Axis Bridge Frobenius-Orbit Obstruction

Updated: 2026-06-12

## Result

The primitive bridge is not obtained cheaply by Frobenius or diamond averaging.

On the collapsed `C_507` coordinate:

```text
p mod 507 = 218
ord_507(p) = 78
p^39 = -1
p^2 mod 507 = 373
ord_507(p^2) = 39
```

The signed bridge has:

```text
++: 121, 122, 123
---: 384, 385, 386
```

The first Frobenius images are disjoint from this support:

```text
p image:
  +: 14, 232, 450
  -: 57, 275, 493

p^2 image:
  +: 10, 249, 383
  -: 124, 258, 497
```

The only `p`-power support returns are:

```text
p^0  = identity
p^39 = bridge reversal
```

Thus the full signed `p`-orbit cancels pairwise.  Over `p^2`, the `39`
support images are pairwise disjoint, so the nonzero orbit closure has:

```text
quotient support = 39 * 6 = 234
raw block support = 234 * 25 = 5850
```

## Command

```sh
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_frobenius_orbit_obstruction_gate.py
```

Expected row:

```text
square_axis_bridge_frobenius_orbit_obstruction_rows=1/1
```

## Continue / Kill

Continue searching for an oriented arithmetic producer for the bridge.  Kill
plain Frobenius-average explanations: the full `p`-orbit cancels, while the
`p^2`-stable nonzero orbit closure is a much larger `234`-quotient /
`5850`-raw object, not the `6`-quotient / `150`-raw bridge.
