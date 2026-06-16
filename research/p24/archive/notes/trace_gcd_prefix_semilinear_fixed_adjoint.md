# Trace-GCD Prefix Semilinear Fixed-Adjoint Syndrome

Date: 2026-06-06

## Point

The fixed-relation descent

```text
F_p^28 + K^28 -> L
```

has an explicit trace adjoint.  This turns the zero fixed-relation theorem
into a structured syndrome-surjectivity theorem.

Keep the notation:

```text
K = F_p(mu_35) = F_{p^4},
L = F_p(mu_157) = F_{p^156},
B = {2,3,5,6},
V_{a,j} in L.
```

For a fixed frequency `a`, the source variable is

```text
c_{a,j} in F_p.
```

For a length-4 orbit

```text
O = [a, pa, p^2a, p^3a],
```

the source variable is

```text
z_{O,j} in K
```

and contributes

```text
sum_{r=0}^3 z_{O,j}^{p^r} V_{p^r a,j}.
```

## Adjoint Formula

Use the trace pairings:

```text
<x,y>_L = Tr_{L/F_p}(xy),
<u,v>_K = Tr_{K/F_p}(uv).
```

For `lambda in L`, the adjoint syndrome has:

Fixed-frequency coordinates:

```text
s_{a,j}(lambda) = Tr_{L/F_p}(lambda V_{a,j}) in F_p.
```

Length-4 orbit coordinates:

```text
S_{O,j}(lambda)
  =
  sum_{r=0}^3
    Tr_{L/K}(lambda V_{p^r a,j})^{p^{4-r}}
  in K.
```

Here the exponent `p^{4-r}` is read modulo the order-4 Frobenius on `K`; for
`r=0` it is the identity.

Indeed, for `z in K`,

```text
Tr_{L/F_p}(lambda z^{p^r} V_{p^r a,j})
  = Tr_{K/F_p}(z^{p^r} Tr_{L/K}(lambda V_{p^r a,j}))
  = Tr_{K/F_p}(z Tr_{L/K}(lambda V_{p^r a,j})^{p^{4-r}}).
```

Summing over `r` gives:

```text
<lambda, F(c,z)>_L
 =
sum_{a fixed,j} c_{a,j} s_{a,j}(lambda)
+
sum_{O,j} Tr_{K/F_p}(z_{O,j} S_{O,j}(lambda)).
```

## Syndrome Theorem

The fixed-relation map is injective if and only if the adjoint map

```text
L -> F_p^28 + K^28
```

is surjective.  Since

```text
dim_Fp L = 156,
dim_Fp(F_p^28 + K^28) = 140,
```

the desired p24 prefix theorem is equivalent to:

```text
rank_Fp lambda |-> (s_{a,j}(lambda), S_{O,j}(lambda)) = 140.
```

Equivalently, the adjoint syndrome kernel has dimension `16`.

This is the descended form of the original prefix trace map, but with the
Gaussian frequency orbits separated into:

```text
28 scalar trace tests over F_p,
28 K-valued linearized trace packets.
```

## Why This Helps

The missing arithmetic theorem can now be attacked as a rank-metric /
linearized-polynomial normality statement for the explicit syndrome map.

In particular, a compact certificate could be:

```text
1. a p-unit maximal minor of the 140-coordinate syndrome map;
2. a Moore/subspace-polynomial residual product for the 140 syndrome
   coordinates;
3. a class-field norm/resultant identity proving that residual product is a
   p-unit.
```

This does not solve the p24 arithmetic theorem yet, but it gives the exact
coordinate-free-to-structured handoff:

```text
coinvariant Fitting p-unit
  = zero semilinear T-core
  = no fixed relation
  = surjective fixed-adjoint syndrome.
```

After choosing an `F_p`-basis `theta_t` of `K`, this syndrome is represented
by the `140` coordinate elements:

```text
V_{a,j}                         for fixed frequencies,
sum_r theta_t^{p^r} V_{p^r a,j} for length-4 frequency orbits.
```

Their Moore/subspace-polynomial residual product is the corresponding
p-unit certificate surface:

```text
p24/trace_gcd_prefix_syndrome_moore_certificate.md
p24/trace_gcd_prefix_syndrome_moore_toy.py
```

## Cheap Gate

The formula and rank equivalence are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_semilinear_fixed_adjoint_toy.py
```

The toy verifies, in a small `K=F_4`, `L=F_256` model:

```text
<lambda, F(source)>_L = <source, F^*(lambda)>_fixed,
rank(F) = rank(F^*),
injective fixed relation iff adjoint syndrome is surjective.
```
