# Axis Sliding-Window Product Theorem

This note packages the coefficient-minor route into an origin-stable p-unit
target.

## Product

For a packet factor `f_a`, let

```text
V_a = T_a(W_axis) in F_p[X]/(f_a)
```

be the axis image subspace, written in the packet power basis, and let `P_0`
project to the first `r = dim(W_axis)` coordinates.  Define

```text
Pi_axis,a = prod_{beta mod n} det(P_0 X^(-beta) V_a).
```

If `Pi_axis,a != 0`, then every beta-shifted leading coordinate minor is
nonzero.  In particular the selected embedded origin's leading minor is
nonzero, so the axis map is injective and the `L1` certificate gate fires.

This is the coefficient-minor analogue of the Hermitian determinant
`Delta_axis`, but it is a coordinate/Pluecker object rather than a trace-form
discriminant.

## Origin Action

An origin shift has CRT coordinates

```text
s == n*alpha + m*beta_0 mod h.
```

The beta part sends

```text
det(P_0 X^(-beta) V_a)
  -> det(P_0 X^(-(beta+beta_0)) V_a),
```

so it permutes the factors of `Pi_axis,a`.

The alpha part changes the standard axis basis by a unimodular matrix `U_alpha`.
Thus

```text
Pi_axis,a -> det(U_alpha)^n Pi_axis,a.
```

For the p24 third trace `n=3107441` is odd, so the value may change by a sign,
but the p-unit status is independent of origin.  Squaring the product removes
this sign ambiguity.

## Data

I added:

```text
p24/axis_sliding_window_product_audit.py
```

Tiny composite row:

```text
D=-671, q=2693, h=30, m=6, n=5
```

reported:

```text
alpha_count=6
distinct_alpha_products=2
zero_alpha_products=0
distinct_squareclasses=1

alpha products: 823 and 1870 = -823 mod 2693
```

First extra-coordinate row:

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
```

reported:

```text
alpha_count=12
distinct_alpha_products=2
zero_alpha_products=0
distinct_squareclasses=2

alpha products: 1465 and 7282 = -1465 mod 8747
```

The product's zero/nonzero status is stable across alpha, as predicted.

## Status

The best coefficient-minor theorem is now:

```text
For every p24 packet a,
Pi_axis,a is nonzero modulo p.
```

or, as an origin-value invariant:

```text
Pi_axis,a^2 is a p-unit.
```

This would beat sqrt scaling if it can be proved or computed from an embedded
class-field/tower identity without enumerating the class set.  At present it
is still not tied to a known class-field norm formula; the random baseline in

```text
p24/cyclic_superregular_random_baseline.md
```

shows that nonvanishing is generic-looking, not proof-like.

The sequence-complexity audit in

```text
p24/axis_sliding_window_sequence_complexity.py
p24/axis_sliding_window_sequence_complexity.md
```

also shows no generic recurrence shortcut.  On the first extra-dimensional row
`D=-8711`, the beta-minor sequence has full Berlekamp-Massey complexity
`11/11`, matching random subspaces.  Thus `Pi_axis,a` is origin-stable but
still high-order in the packet beta phase.

The p24 exterior character-support audit in

```text
p24/exterior_character_support_audit.py
p24/exterior_character_support_boundary.md
```

explains why: for the actual p24 packet orbit `H=<p> mod n`, the sumset `H+H`
already equals all of `Z/nZ`, with at least `48343` ordered representations
of every residue.  The exterior-power packet representation therefore has full
beta-character support available before any CM-specific input is used.

The full Grassmannian support audit in

```text
p24/plucker_full_support_audit.py
p24/plucker_full_support_boundary.md
```

checks whether the axis subspace has all coordinate Pluecker minors nonzero.
On `D=-8711`, the CM axis has `0/210` zero Pluecker coordinates, but so do
`490/500` random subspaces.  Thus even full Pluecker support is generic in
this window, not a visible CM-specific structure.
