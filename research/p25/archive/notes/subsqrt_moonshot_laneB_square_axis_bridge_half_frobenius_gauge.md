# p25 Lane B Square-Axis Bridge Half-Frobenius Gauge

## Question

The twisted-orientation gate says a degree-`39` bridge producer needs a
quadratic sign local system.  This note asks what that half-Frobenius action
looks like on the actual raw source coordinates, not only on collapsed
`C_507`.

## Result

On the raw source group `C_75 x C_169`, the half-Frobenius acts as:

```text
p^39: (right, c) -> (2 * right, -c)
```

The full-degree action is:

```text
p^78: (right, c) -> (4 * right, c)
```

so `p^78` is the identity on the visible `C_3 x C_169` quotient, but still a
nontrivial `C_25` kernel gauge.

The bridge positive layer is parameterized as:

```text
base + K^j + D^i,       j = 0..24, i = 0,1,2
```

and the negative layer is:

```text
base + T + K^j + D^i.
```

For `p^39`, the exact transition law is:

```text
positive (j,i) -> negative (2*j + offset_i, 2-i)
offset_i = 24,12,0 for i = 0,1,2

negative (j,i) -> positive (2*j + offset_i, 2-i)
offset_i = 1,14,2 for i = 0,1,2
```

For `p^78`, signs are preserved, but the kernel trace is still gauged:

```text
positive (j,i) -> positive (4*j + offset_i, i)
offset_i = 0,13,1

negative (j,i) -> negative (4*j + offset_i, i)
offset_i = 2,15,3
```

## Interpretation

The half-orbit orientation is not a plain raw bridge translation.  It works
because the bridge contains the full `C_25` kernel trace and the three-term
`D` segment with the right orientation.  A sparse kernel section is not stable:
the `j=0` positive section maps to kernel indices `{0,12,24}`.

So the quadratic sign local system must be compatible with this raw gauge.  It
cannot merely orient the collapsed `C_507` support while ignoring the source
kernel trace.

This is a producer-facing contract:

- keep the full `K` trace, or explain an equivalent kernel-invariant
  replacement;
- handle the `D`-segment reversal `i -> 2-i`;
- account for the fact that `p^78` is still a raw kernel gauge even after the
  quotient orientation closes.

## Gate

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/p25_laneB_square_axis_bridge_half_frobenius_gauge_gate.py
```

Expected line:

```text
square_axis_bridge_half_frobenius_gauge_rows=1/1
```
