# Symbolic Hasse-Davenport Gate

Date: 2026-06-07

## Point

The finite-field Jacobi anchor correction is not only an empirical finite
field pattern.  The product-formula identities follow from symbolic
character/Gauss-sum accounting.

This gate checks the residue conditions for the reduced packet:

```text
Jdagger(1,1)=1
Jdagger(A,B)=J(A,B) otherwise.
```

## Symbolic Row-Ratio Cancellation

For fixed right row `r`, write:

```text
A_k = chi^(u*t(r,k))
B_k = chi^(v*t(r,k)).
```

Since `u` is right-trivial, `B_k` and `A_kB_k` have the same right component.
Since `v` and `u+v` have nonzero C-components, each runs through the same
size-`c` C-coset as `k` varies.

At `k=0`, `A_0=1`, so:

```text
B_0 = A_0 B_0.
```

Removing the common `k=0` element leaves identical punctured C-cosets.  Thus
in:

```text
prod_{k != 0} G(A_k)G(B_k)/G(A_kB_k)
```

the `B_k` and `A_kB_k` Gauss factors cancel, leaving:

```text
prod_{k != 0} G(A_k),
```

which is independent of the right row `r` and of the right-mixed partner `v`.

## Symbolic Pair-Product Constants

For `k != 0`, admissibility makes `A`, `B`, and `AB` all nontrivial, so:

```text
J(A,B)J(A^-1,B^-1)=q.
```

On the C-zero fiber, `A=1`.  For `r != 0`, `B` is nontrivial and
`J(1,B)=-1`, giving pair-product `1`.  At `r=0`, the reduced anchor
`Jdagger(1,1)=1` also gives pair-product `1`.

## Coverage

The gate checks all admissible right-mixed pairs for:

```text
c = 5, 11, 13, 17, 19, 179.
```

For p24, `c=179`, and the pair count is:

```text
6*(179-1)*(179-2) = 189036.
```

Observed:

```text
symbolic_pair_count_rows=6/6
symbolic_pair_product_rows=6/6
symbolic_row_ratio_rows=6/6
symbolic_reduced_anchor_rows=6/6
symbolic_producer_rows=6/6
p24_symbolic_right_mixed_pairs=189036
```

No finite-field sums and no p24 class-set enumeration are used.

## Consequence

The p24 missing theorem is not the finite Jacobi/Hasse-Davenport algebra
anymore.  That algebra is isolated.

The targeted source refresh gives the right name for this algebra:
Kubert-Lichtenbaum/Weil mixed-level Jacobi-sum Hecke characters and the
Langlands/Hasse-Davenport Gauss-sum identities.  That source validates the
shape of the reduced Jacobi packet, but it does not by itself identify the
p24 class-field orbit.

The imaginary-quadratic refinement of Brattstrom-Lichtenbaum gives the
natural next theorem shape: a mixed-level `theta` packet with integral
infinity type yields a Galois-equivariant Jacobi-sum Hecke character.  For
p24 the non-formal part is to choose such a packet so that, after projection
to the unramified `rho` quotient, it is exactly this reduced `C_7 x C_179`
packet.

The visible packet has the right conductor-lift infinity shadow.  Since the
p24 quadratic conductor is coprime to `7*179`, the conductor units split
evenly between the two CM embeddings.  For every admissible
`theta=[u]+[v]-[u+v]`, the visible unit sum is:

```text
phi(7*179)/2 = 534.
```

The p24 lift therefore has equal integral identity/conjugate coefficients:

```text
174015840695068591393327296
```

on both embeddings.  This makes the conductor lift compatible with the
Jacobi-sum Hecke-character criterion, but it also shows that the infinity type
does not select the rho quotient; selection has to come from the finite Artin
component.

The visible ray/Shimura unit component is not that finite Artin source.  Both
visible primes are inert in the p24 CM field, so the visible ray unit part
over the Hilbert class field has order:

```text
((7^2 - 1)(179^2 - 1))/2 = 768960.
```

This order is not divisible by `7`, by `179`, or by `7*179`.  Therefore the
post-`B/C` quotient is not a visible ray quotient.  It comes from the
unramified `n=3107441` class component, where `rho=p^780` has order
`7*31*179` and the `B/C` trace removes the `31` factor.

The gate records the explicit quotient coordinates:

```text
rho^e = (rho^179)^r * (rho^7)^c,
e = 179*r + 7*c mod 1253.
```

Equivalently, the `179` exponent step is the right `C_7` axis, the `7`
exponent step is the `C_179` axis, and the pairs `(r,c)` cover the full
post-`B/C` quotient.

The plain cyclotomic Frobenius check is deliberately negative:

```text
p mod 7        = 1,  order 1
p mod 179      = 77, order 89
p mod 7*179    = 435, order 89
actual quotient after Tr_{B/C} has order 7*179 = 1253
```

So the reduced packet cannot be realized by simply taking ordinary
cyclotomic Frobenius on `mu_{7*179}`.  It has to be pulled back through the
CM/class-field Artin quotient where `rho=p^780` has the checked
post-`B/C` quotient `C_7 x C_179`.

The remaining arithmetic input is therefore:

```text
construct the selected trace-GCD packet after Tr_{B/C} as the p-integral
specialization/log/divisor of the reduced Jacobi/CM-Lang packet after the
CM-Artin pullback from the actual rho quotient.
```

Equivalently, find the CM/Lang unit whose single degenerate anchor is the
p24 analogue of `J(1,1)/(q-2)`.
