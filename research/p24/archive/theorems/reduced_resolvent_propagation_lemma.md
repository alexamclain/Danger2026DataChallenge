# Reduced Resolvent Propagation Lemma

This note sharpens the reduced-normality gap.  It does not prove p24 reduced
normality, but it shows that any failure is a large Galois-stable spectral
collapse rather than a single unlucky character.

## Setup

Let `L/K` be the p24 ring class field, and assume the ordinary prime
`frak_p | p` of `K` splits completely in `L`.  Let

```text
G = Gal(L/K) = <sigma>,       |G| = h,
j_i = sigma^i(j).
```

Let `E` contain the values of a class character `chi`, and define the
resolvent

```text
R_chi = sum_i chi(sigma)^i sigma^i(j) in L E.
```

Choose a prime `P` of `LE` above `frak_p` and reduce the roots of unity
compatibly.

## Lemma 1: Split-prime propagation

If

```text
R_chi == 0 mod P,
```

then

```text
R_chi == 0 mod tau(P)       for every tau in G.
```

Consequently

```text
Norm_{LE/E}(R_chi)
```

is divisible by the product of the `G`-orbit of primes above `P`; in the
completely split case this is the `h`-fold split-prime contribution in `E`.

### Proof

For `tau=sigma^a`,

```text
tau(R_chi)
  = sum_i chi(sigma)^i sigma^{i+a}(j)
  = chi(sigma)^{-a} R_chi.
```

The scalar `chi(sigma)^{-a}` is a root of unity, hence a unit at primes above
`p` because `p` does not divide `h` in the p24 targets.  If `R_chi` lies in
`P`, then `tau(R_chi)` lies in `tau(P)`, so `R_chi` lies in `tau(P)` as well
after multiplying by the unit scalar.

## Lemma 2: Frobenius orbit propagation

Write the reduced cyclic vector as

```text
J(T) = sum_i j_i T^i in F_p[T]/(T^h-1).
```

If `J(zeta)=0` for an `h`-th root of unity `zeta`, then

```text
J(zeta^{p^r}) = 0        for every r >= 0.
```

### Proof

The coefficients `j_i` lie in `F_p`, so

```text
J(zeta)^p = J(zeta^p).
```

Iterating gives the claim.

## p24 orbit sizes

For the third strict trace quotient,

```text
ord_157(p)   = 156
ord_211(p)   = 35
ord_33127(p) = 5460
ord_66254(p) = 5460
```

Thus a primitive odd quotient-character vanishing would erase an entire
Frobenius orbit of `5460` spectral components.  Separate relative layers
would erase orbits of sizes `156` and `35`.

## Boundary

This propagation is strong structure, but it is not a contradiction.  The
height/norm bounds are far too loose: p24 singular-modulus resolvents are
astronomically larger than `p`, so large split-prime divisibility does not
force the algebraic integer to be zero.

The lemma is still useful because it rules out the mental model of an
isolated one-character accident.  Reduced normality can fail only through a
Galois-stable kernel of the group determinant

```text
det(j_{a+b}) = product_chi R_chi.
```

That is exactly the finite-field group-algebra kernel needed for a sparse
additive selector to beat the subgroup projector.  No such kernel appeared in
the complete toy CM scans, but p24 still needs a genuine p-adic nonvanishing
certificate to close the theorem.
