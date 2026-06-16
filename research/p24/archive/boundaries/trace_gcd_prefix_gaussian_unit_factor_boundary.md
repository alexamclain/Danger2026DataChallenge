# Trace-GCD Prefix Gaussian Unit-Factor Boundary

Date: 2026-06-06

## Point

The Gaussian DFT factorization

```text
D_{a,j} = G_a * U_{a,j}
```

has a useful positive part and a dangerous false simplification.

The positive part is that `G_a` is a unit after the safe scalar extension.
Let

```text
K = F_p(mu_35),
R = F_p(mu_211),
```

with `[R:F_p]=35` and `[K:F_p]=4`.  Since `gcd(35,4)=1`,

```text
R tensor_{F_p} K
```

is the field `F_{p^140}`.  The Gaussian periods `eta_i` form an
`F_p`-normal basis of `R`, hence after tensoring with `K`, their DFT values

```text
G_a = sum_i eta_i tensor omega^(-a*i)
```

form a `K`-basis of `R tensor K`.  Therefore every `G_a` is nonzero in that
field, hence a unit.  Its image in the product algebra

```text
E tensor_{F_p} K
```

is also a unit: every `K/F_p` conjugate component is nonzero.

## What The Unit Fact Allows

For a fixed frequency `a`, multiplication by `G_a` is a `K`-linear
automorphism, so:

```text
rank_K{D_{a,j} : j in B}
  =
rank_K{U_{a,j} : j in B}.
```

This is a good local check.  If a fixed-frequency four-tuple of `U_{a,j}` is
dependent, the corresponding four-tuple of `D_{a,j}` is dependent.

## What It Does Not Allow

It does **not** allow the full `140`-column theorem to divide each frequency
block by its own `G_a` and then test the union of the `U_{a,j}`.  The reason
is simple: `G_a` is a unit of the target algebra `L tensor K`, not a scalar in
the base field `K`.

Columnwise multiplication by target-algebra units can change linear
independence.  The full theorem remains:

```text
rank_K{G_a * U_{a,j} : 0 <= a < 35, j in {2,3,5,6}} = 140
```

inside `L tensor K`.

It is not equivalent to:

```text
rank_K{U_{a,j} : 0 <= a < 35, j in {2,3,5,6}} = 140.
```

The latter can be useful as a heuristic or a stronger sufficient condition
only if one proves an additional common target automorphism or direct-sum
structure.  The current product-algebra setup does not give that for free.

## Correct Current Theorem

The safe diagonalized prefix theorem is the twisted Schubert condition:

```text
the 140 vectors G_a * U_{a,j} in L tensor_{F_p} K are K-independent.
```

Equivalently, the maximal-minor/Fitting ideal of the scalar-extended
Gaussian-DFT matrix is a unit.  This is just the prefix coinvariant Fitting
theorem in diagonalized right-cycle coordinates.

## Cheap Gate

The pitfall is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_unit_scaling_pitfall_toy.py
```

The toy shows over `F_4/F_2` that two independent vectors can become
dependent after multiplying one by a non-base-field unit.
