# Energy Gram-Isotropy Boundary

This note records a linear-algebra boundary for the scalar energy route.

## Gram Identity

For

```text
J_u(X) = sum_k j_{u+m*k} X^k,
```

the relative energy polynomial is

```text
C(X) = sum_d C_d X^d,
C_d = sum_i j_{i+m*d} j_i.
```

Equivalently, in `F_p[X]/(X^n-1)`,

```text
C(X) = sum_u J_u(X) J_u(X^-1).
```

So after reducing modulo a Frobenius packet factor `f_a`, the scalar energy is
the Hermitian/reciprocal Gram norm of the relative-content vector

```text
(J_0 mod f_a, ..., J_{m-1} mod f_a).
```

This explains why energy is a natural sufficient certificate:

```text
all J_u == 0 mod f_a  =>  C == 0 mod f_a.
```

## Isotropy Obstruction

The converse is false even in the exact packet algebra.  The toy script

```text
p24/energy_isotropy_obstruction_toy.py
```

uses the same quadratic packet shape as the calibrated `D=-5000` example:

```text
q = 1259,
f(X) = X^2 + 36X + 1,
conjugation X -> X^-1.
```

It finds

```text
y = 3 + 647X,
Norm(y) = -1 mod 1259.
```

Thus the nonzero vector

```text
(1, y)
```

has content nonzero but Hermitian energy

```text
Norm(1) + Norm(y) = 0.
```

The run reports:

```text
content_certificate_nonzero=1
maximal_base_field_span=1
energy_zero=1
```

So even maximal base-field span in the packet algebra does not rule out
Hermitian isotropy.

## Consequence For p24

The p24 energy packet has

```text
m = 66254
```

coordinates over a large real-cyclotomic packet field.  Nonzero vectors with
zero Hermitian energy are abundant by finite-field linear algebra.  Therefore:

```text
relative content nonzero does not imply energy nonzero;
energy nonzero requires extra arithmetic from the CM/autocorrelation origin.
```

This keeps the certificate hierarchy honest:

```text
content/Bezout: exact vector certificate;
energy: independent scalar sufficient certificate;
packet norm: degree-8 packaging of the energy certificates, not a consequence
             of content alone.
```

The positive energy route must prove that the specific p24 autocorrelation
Gram scalar avoids the isotropic cone at the selected prime.  A pure
linear-algebra or generic packet theorem cannot do it.
