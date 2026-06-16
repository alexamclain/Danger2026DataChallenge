# Subsqrt Moonshot Lane B Square-Axis Bridge Primitivity

Date: 2026-06-12

## Result

The bridge source multiplier is primitive, even though the bridge support is
small.

The bridge step is:

```text
X^2Y^3 = 113
```

It is coprime to both the quotient order and raw order:

```text
gcd(113, 507) = 1
gcd(113, 12675) = 1
```

On the local source factors the multiplier is:

```text
45  mod 151, order 75
667 mod 677, order 169
```

So the product source multiplier has order:

```text
lcm(75,169) = 12675
```

## No Proper Quotient

The signed bridge descends through the trace kernel to `C_507`, but no farther.
It is not a pullback from any proper divisor quotient:

```text
1, 3, 13, 39, 169
```

Each attempted quotient has conflicting fibers.

## Raw Fourier Profile

For the kernel-trivial raw bridge lift on `C_12675`, the nonzero Fourier support
is exactly the quotient-side support lifted to kernel mode zero:

```text
nonzero raw frequencies = 504
zero raw frequencies    = 12171
```

All nonzero raw frequencies are multiples of `25`, and the only quotient-zero
frequencies are:

```text
0, 169, 338
```

Thus the raw bridge is kernel-trivial but quotient-frequency-full.

## Consequence

A useful producer cannot explain this bridge with a lower-order local motion,
a proper quotient, a hidden kernel phase, or a low-frequency filter.  It must
realize a primitive raw source edge whose support is nevertheless constrained
to the six bridge quotient classes.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_primitivity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_bridge_primitivity_gate.py
```
