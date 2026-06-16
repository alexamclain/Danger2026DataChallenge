# Trace-GCD Prefix Semilinear Descent Fixed Relation

Date: 2026-06-06

## Point

The semilinear-core theorem has a useful descent form.  Let

```text
K = F_p(mu_35) = F_{p^4},
M_0 : K^{35*4} -> L,
C = ker(M_0),
(T x)_{b,j} = x_{p^{-1}b,j}^p.
```

The previous criterion was:

```text
core_T(C) = {x : T^r x in C for r=0,1,2,3} = {0}.
```

Since `C` is `K`-linear and `T` is semilinear, the core is also `K`-linear
and `T`-stable.  Semilinear Hilbert 90 / Galois descent says:

```text
dim_{F_p}(core_T(C)^T) = dim_K(core_T(C)).
```

Therefore:

```text
core_T(C) = {0}
  <=>
C cap Fix(T) = {0}.
```

So the prefix theorem is equivalent to injectivity of the first-component map
on the explicit fixed-coordinate source.

## Explicit Fixed Coordinates

The fixed frequencies are:

```text
0, 5, 10, 15, 20, 25, 30.
```

On these frequencies, `T x = x` means:

```text
x_{a,j} in F_p.
```

For a length-4 orbit

```text
O = [a, p*a, p^2*a, p^3*a],
```

a `T`-fixed vector is determined by one element

```text
z_{O,j} in K,
```

with coordinates

```text
x_{p^r a,j} = z_{O,j}^{p^r},      r=0,1,2,3.
```

Hence the fixed source has:

```text
7 fixed frequencies * 4 blocks      = 28 F_p variables,
7 length-4 orbits * 4 blocks        = 28 K variables,
total F_p dimension                 = 28 + 28*4 = 140.
```

This is exactly the original prefix source dimension, but now written in
frequency-orbit descent coordinates.

## Fixed-Relation Theorem

Let `B={2,3,5,6}`.  The prefix theorem is equivalent to:

```text
sum_{a fixed, j in B} c_{a,j} V_{a,j}
+
sum_{O=[a,pa,p^2a,p^3a], j in B}
  sum_{r=0}^3 z_{O,j}^{p^r} V_{p^r a,j}
= 0

with c_{a,j} in F_p, z_{O,j} in K

=> all c_{a,j}=0 and all z_{O,j}=0.
```

This is the scalar-extended Gaussian DFT theorem descended back to an
ordinary `F_p`-linear injectivity statement.  Its advantage is not a smaller
dimension; its advantage is structural:

```text
the only possible K-linear semilinear core would already show up as a
T-fixed linearized-polynomial relation.
```

## Proof Direction

The length-4 orbit part is a degree-4 linearized expression:

```text
z V_{a,j} + z^p V_{pa,j} + z^{p^2} V_{p^2a,j} + z^{p^3} V_{p^3a,j}.
```

So a proof can target a skew-PIT / Moore-normality statement for the `28`
linearized packets, plus the `28` base-field fixed-frequency packets.

This is the current best formal bridge from the tensor-component theorem to
CS/rank-metric language:

```text
zero T-core
  <=>
no fixed semilinear relation
  <=>
injective F_p-linearized packet map of shape F_p^28 + K^28 -> L.
```

The missing arithmetic theorem remains that this fixed-relation map is
p-unit injective for the actual CM Gaussian frequency table `V_{a,j}`.

The trace-adjoint of this fixed-relation map gives a dual syndrome theorem:

```text
L -> F_p^28 + K^28.
```

For a length-4 orbit `O=[a,pa,p^2a,p^3a]`, the `K`-valued syndrome
coordinate is

```text
sum_{r=0}^3 Tr_{L/K}(lambda V_{p^r a,j})^{p^{4-r}}.
```

The fixed-relation map is injective if and only if this adjoint syndrome map
is surjective.  This is recorded in:

```text
p24/trace_gcd_prefix_semilinear_fixed_adjoint.md
p24/trace_gcd_prefix_semilinear_fixed_adjoint_toy.py
```

## Cheap Gate

The descent equivalence is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_semilinear_descent_toy.py
```

The toy reuses the small `K=F_4` semilinear core model and verifies:

```text
dim_K core_T(C) = dim_{F_p}(C cap Fix(T)),
zero core iff no nonzero fixed relation.
```
