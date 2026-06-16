# Relative Product Is Not A Group-Determinant Factor

This note corrects a tempting but false shortcut.

## The True Linear Relation

Let `h=m n`.  For fixed `a`,

```text
R_{a+r n}
  = sum_u zeta_h^(a u) zeta_m^(r u) P_u(a).
```

Thus the vector

```text
(R_{a+r n})_r
```

is an invertible Fourier transform of

```text
(zeta_h^(a u) P_u(a))_u.
```

Consequently:

```text
all R_{a+r n} are zero    <=>    all P_u(a) are zero.
```

This is exactly the harmful-dual-coset lemma.

## The False Product Shortcut

It is tempting to multiply the coordinates and write

```text
prod_r R_{a+r n}  ?=  unit * prod_u P_u(a).
```

This is false.  A determinant controls the top exterior power of the linear
map, not the product of coordinates of one vector.  An invertible Fourier
transform preserves the zero vector, but it does not preserve the union of
coordinate hyperplanes.

Thus the following are different sufficient certificates:

```text
relative product:
  prod_u P_u(a) != 0
  means no relative fiber vanishes;

dual-coset group determinant factor:
  prod_r R_{a+r n} != 0
  means no full resolvent in the dual coset vanishes.
```

Either condition rules out the harmful event, because the harmful event is
the zero vector.  Neither product condition is equivalent to the other.

## p24 Meaning

The exact content certificate remains:

```text
(P_u(a))_u is not the zero vector
```

or, packetized over `F_p`,

```text
(J_u mod f_a)_u is not the zero vector.
```

The relative product certificate is stronger than needed, but it is not the
same as reduced normality on the full dual coset.  It asks for every selected
quotient fiber to have nonzero relative character sum.  The full-resolvent
product asks for every quotient Fourier mode of that vector to be nonzero.

Small natural CM scans have so far supported both stronger conditions, but a
proof of either would still need arithmetic control of high-order non-genus
periods.
