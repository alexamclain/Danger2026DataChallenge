# Trace-GCD Prefix Syndrome Moore Certificate

Date: 2026-06-06

## Point

The fixed-adjoint syndrome map can be represented by an explicit list of
`140` elements of `L`.  Its surjectivity is equivalent to a Moore /
subspace-polynomial residual product being a p-unit.

This gives the current sharpest finite certificate surface for the prefix
theorem.

## Coordinate Elements

Keep:

```text
K = F_p(mu_35) = F_{p^4},
L = F_p(mu_157) = F_{p^156},
B = {2,3,5,6},
V_{a,j} in L.
```

The fixed-adjoint syndrome has target:

```text
F_p^28 + K^28.
```

Choose an `F_p`-basis

```text
theta_0, theta_1, theta_2, theta_3
```

of `K`.  The scalar fixed-frequency syndrome coordinates are represented by
the elements:

```text
V_{a,j},        a in {0,5,10,15,20,25,30},  j in B.
```

For a length-4 frequency orbit

```text
O = [a, pa, p^2a, p^3a],
```

the `K`-valued syndrome coordinate

```text
S_{O,j}(lambda)
  =
  sum_{r=0}^3 Tr_{L/K}(lambda V_{p^r a,j})^{p^{4-r}}
```

has `theta_t`-coordinate represented by the element:

```text
W_{O,j,t}
  =
  sum_{r=0}^3 theta_t^{p^r} V_{p^r a,j}.
```

Indeed:

```text
Tr_{K/F_p}(theta_t S_{O,j}(lambda))
  =
  Tr_{L/F_p}(lambda W_{O,j,t}).
```

Thus the full syndrome map is the trace-pairing map associated to the `140`
elements:

```text
C_prefix =
  {V_{a,j} : a fixed, j in B}
  union
  {W_{O,j,t} : O length-4, j in B, 0<=t<4}.
```

## Moore Certificate

By nondegeneracy of the trace pairing on `L/F_p`,

```text
L -> F_p^28 + K^28
```

is surjective if and only if

```text
span_Fp(C_prefix)
```

has dimension `140`.

Equivalently, for any fixed ordering

```text
c_1,...,c_140
```

of `C_prefix`, let `P_i` be the monic `p`-linearized annihilator of

```text
span_Fp(c_1,...,c_i).
```

Then the prefix theorem is equivalent to:

```text
prod_{i=1}^{140} P_{i-1}(c_i) != 0 in L.
```

Or, as a selected-prime scalar p-unit:

```text
Norm_{L/F_p}(prod_i P_{i-1}(c_i)) in F_p^*.
```

This is the Moore/subspace-polynomial p-unit that a class-field, Kummer,
or resultant proof must produce.  It is not a p24-scale computation: once
the arithmetic formula for this residual product is known, the verifier
checks one field element and its inverse.

## Certificate Shape

A conservative verifier payload could contain:

```text
R_prefix = Norm_{L/F_p}(prod_i P_{i-1}(c_i)),
R_prefix^{-1}.
```

Together with a producer theorem identifying `R_prefix` with the fixed
CM/Fitting section, this proves:

```text
R_prefix != 0
  => syndrome surjective
  => no fixed relation
  => zero semilinear T-core
  => prefix Fitting p-unit.
```

The missing theorem is still arithmetic: prove that this specific p24
residual product is a p-unit without enumerating the class set.

## Cheap Gate

The finite equivalences are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_syndrome_moore_toy.py
```

The toy verifies:

```text
syndrome coordinate elements give the same trace-pairing rank;
Moore residual product is nonzero exactly in the full-rank case;
a forced fixed-frequency relation makes the residual product zero.
```
