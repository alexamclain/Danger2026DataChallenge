# Reduced-Anchor Kernel Generator Invariance Gate

This gate records the search-space correction after replacing an individual
one-point divisor by the whole-subgroup kernel polynomial.

For an odd cyclic subgroup `H=<P>` of order `c`,

```text
K_H(x) = prod_{Q in (H\{O})/{+-1}} (x - x(Q)).
```

Changing the generator from `P` to `uP`, with `u in (Z/cZ)^*`, only permutes
the nonzero subgroup.  Therefore the oriented one-point divisors have `c-1`
diamond conjugates, and their x-coordinates have `(c-1)/2` sign-paired
choices, but the subgroup kernel polynomial has one generator orbit.

For p24:

```text
c = 179
oriented one-point diamond choices = 178
x-coordinate generator pairs = 89
kernel-polynomial generator orbits = 1
forced Kummer exponent choices = 1
independent anchor signs = 2
conditional kernel search cases = 2
```

This does not construct the selected CM/Lang subgroup polynomial.  It says
that once that producer object is available, there are not 178 generator
variants to try; only the two anchor signs remain before the finite verifier.
