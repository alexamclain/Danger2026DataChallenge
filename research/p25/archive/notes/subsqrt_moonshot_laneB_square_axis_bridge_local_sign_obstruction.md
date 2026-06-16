# p25 Lane B Square-Axis Bridge Local Sign Obstruction

## Question

The twisted-orientation gate leaves one support-preserving degree-`39`
possibility: a quadratic sign local system with

```text
alpha^(p^39) = -alpha.
```

The cheapest version would be that this sign was already present in the
ambient local residue fields above the square-axis source.

## Result

It is not.

The established p25 square-axis source uses:

```text
mod151: F_l^* = C_2 x C_75, source order C_75
mod677: F_l^* = C_4 x C_169, source order C_169
```

The source generator modulo `151` has primitive-root log `98`, so every source
point has even primitive log and Legendre symbol `+1`.  The source generator
modulo `677` has primitive-root log `384`, so every source point has primitive
log `0 mod 4`; both the Legendre and quartic tags are trivial.

For the bridge factors:

```text
base, K, D, T, Y_raw, D^3 all have two-primary tag (0,0)
```

For the full raw bridge:

```text
support = 150
positive support = 75
negative support = 75
all tags = {(0,0): 150}
positive tags = {(0,0): 75}
negative tags = {(0,0): 75}
```

Scanning the `7` nontrivial two-primary tag characters of `C_2 x C_4` finds
zero characters that separate the positive and negative bridge layers.

## Interpretation

This does not kill the twisted-orientation route.  It kills the cheap local
version of it.

A producer cannot say "the missing sign is just the Legendre/quartic sign of
the existing local source residues."  The sign must be introduced as a new
anti-invariant coefficient/local system, or replaced by an equivalent nonsplit
finite-field identity that is not visible in the p24-amortized source
coordinates.

Multiplying by `-1` would move to the nontrivial two-primary cosets:

```text
mod151: -1 tag = 1 in C_2
mod677: -1 tag = 2 in C_4
```

but those cosets are outside the established odd-order source subgroup used by
the raw `Y[e]` harness.

## Gate

```sh
env PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/p25_laneB_square_axis_bridge_local_sign_obstruction_gate.py
```

Expected line:

```text
square_axis_bridge_local_sign_obstruction_rows=1/1
```
