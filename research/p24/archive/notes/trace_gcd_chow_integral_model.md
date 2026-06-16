# Trace-GCD Chow Integral Model

Date: 2026-06-06

This note isolates the p-integrality sublemma for the orbit Chow norm.  It is
not the p-unit theorem; it says the Chow section is a well-defined p-integral
determinant-line object and that all compatible coordinate choices change it
only by p-units.

## Local Order

Let `O_p` be the localization at the selected prime above

```text
p = 10^24 + 7
```

of the ring-class/cyclotomic compositum needed for the mixed trace-GCD
construction.  The relevant roots of unity have orders:

```text
2, 157, 211.
```

All are p-adic units because `p` is prime to `2*157*211`.

For one nonzero right Frobenius orbit, let:

```text
B_O
```

be the corresponding p-integral finite etale orbit algebra.  After reduction,
this is the 35-dimensional right factor used in the trace-GCD determinant.

## Integral Lattices

The trace-GCD construction supplies:

```text
Lambda_W  subset B_O,        rank 16,
Lambda_C  subset B_O,        rank 19,
```

where:

```text
Lambda_W = integral image of the transported prefix kernel,
Lambda_C = integral lift of ker(P), the selected tail-complement lattice.
```

The selected Lang/head coordinates and the prefix-kernel transport are chosen
so that their reductions have the finite ranks already required by the
trace-GCD local-unit theorem.  Consequently any matrices inverted in these
choices have p-unit determinants.

## Chow Section

Choose p-integral bases:

```text
w_1,...,w_16 of Lambda_W,
c_1,...,c_19 of Lambda_C,
e_1,...,e_35 of B_O.
```

For a right translate `t`, define the integral Chow value by:

```text
Chow_t(W,C)
  = det( w_1,...,w_16, V_t^{-1}c_1,...,V_t^{-1}c_19 )
    / det(e_1,...,e_35),
```

or, equivalently, as the determinant-line pairing:

```text
det(Lambda_W) tensor det(V_t^{-1}Lambda_C) -> det(B_O).
```

Since `V_t` is multiplication by a root of unity, it preserves the p-integral
orbit algebra and has p-unit determinant.  Thus `Chow_t(W,C)` is p-integral.

Changing any of the chosen bases multiplies `Chow_t` by:

```text
det(GL_16(O_p)) * det(GL_19(O_p)) * det(GL_35(O_p))^{-1},
```

hence by a p-unit.  Therefore:

```text
Chow_t is a p-unit
```

is independent of all compatible p-integral basis and volume-form choices.

## Relation To Delta(t)

The row-determinant value

```text
Delta(t) = det(P V_t | W)
```

is the same determinant-line pairing after identifying:

```text
B_O / V_t^{-1}C  ~=  selected head coordinates.
```

Therefore:

```text
Delta(t) = u_t * Chow_t(W,C),
u_t in O_p^*.
```

The orbit product satisfies:

```text
Pi_O = prod_t Delta(t)
     = u_O * prod_t Chow_t(W,C),
u_O in O_p^*.
```

So the seven-orbit trace-GCD payload is equivalently a seven-orbit Chow-norm
p-unit payload.

## What Remains

This integral model removes denominator ambiguity.  It does not prove that
the Chow values are p-units.  The missing theorem is still:

```text
prod_{t in O} Chow_t(W_CM,C) is a p-unit
```

for each right Frobenius orbit `O`.

Equivalently:

```text
the reduced CM 16-plane is transverse to every translated 19-plane C_t.
```

The finite cancellation toy:

```text
p24/orbit_exterior_schubert_toy.py
```

shows that p-integrality and nonzero individual Plucker pieces do not imply
this p-unitness.  The remaining input must be a true p-adic
noncancellation/Fitting/class-field theorem.

The finite basis-scaling hygiene is exercised by:

```text
p24/chow_basis_unit_invariance_toy.py
```

It verifies in small finite-field models that changing bases in `W` and `C`
scales the Chow determinant by the corresponding determinant units and
preserves zero/nonzero status.
