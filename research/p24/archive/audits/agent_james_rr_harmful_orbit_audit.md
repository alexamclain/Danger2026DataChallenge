# Riemann-Roch audit for harmful H-character packets

## Setup

Third p24 trace:

```text
h = 205880396014 = m*n
m = 66254
n = 3107441 prime
H = <g^m>, |H| = n
ord_n(p) = 388430, so there are 8 nontrivial Frobenius packets
```

For a nontrivial relative character `a mod n`,

```text
P_u(a) = sum_{k=0}^{n-1} zeta_n^(a*k) j_{u+m*k},  0 <= u < m.
```

The harmful event for the Frobenius packet of `a` is:

```text
P_u(a) = 0 for every u, equivalently J_u(X) == 0 mod f_a(X) for every u.
```

## Conditional divisor theorem

Let `C/F_p` be a smooth projective curve, let

```text
S = {Q_u : 0 <= u < m} subset C(F_p)
```

be distinct quotient CM points, and let `F_a in F_p(zeta_n)(C)` be regular at
all `Q_u` with

```text
F_a(Q_u) = P_u(a).
```

If `F_a` is not the zero function and

```text
deg poles(F_a) < m,
```

then the harmful event for `a` is impossible.

The same statement holds packetwise over `F_p[X]/(f_a)`: if a vector-valued or
coefficient-valued modular function represents the residues `J_u mod f_a`,
is not identically zero, is regular at the quotient CM points, and has pole
degree `< m`, then the Frobenius packet cannot vanish on every fiber.

Proof: a nonzero rational function on a smooth projective curve has zero
divisor degree equal to pole divisor degree.  If it vanished at all `m`
distinct `Q_u`, its zero divisor would have degree at least `m`.

## Why this does not currently prove p24

The theorem is useful only after one constructs the representing modular
function `F_a` with pole degree below `66254`.  The natural realization of
`F_a` is the relative character trace along the `H`-fiber.  It requires the
degree-`n` data

```text
j_u, j_{u+m}, ..., j_{u+m*(n-1)}
```

with nontrivial `zeta_n` weights.  On a tautological `H`-cycle cover, this is
an `H`-eigenfunction on the fiber side, not a quotient function.  Its natural
degree scale is the recovery/fiber degree `n = 3107441`, or the much larger
degree of a modular-correspondence path realizing the same class action.

Thus the available divisor count would compare

```text
zeros wanted:  m = 66254
natural poles: >= n = 3107441
```

and gives no contradiction.

## No formal pole-degree miracle

Riemann-Roch alone cannot rule out a hypothetical small-pole eigenfunction:
cyclic Kummer covers show that nontrivial character eigenfunctions can have
small pole divisors when a genuine global cyclic cover with the right
automorphism is already present.

The missing object would therefore have to be genuinely new: a modular or
correspondence curve carrying the unramified class subgroup `H` as a global
character symmetry, together with an `H`-eigenfunction whose CM values are the
embedded sums `P_u(a)` and whose pole degree is `< m`.

Existing CM/class-field constructions do not supply such a curve.  They either
enumerate the `H`-orbit, compute a trace/norm over `H`, or use a recovery
object of degree `n`.

## Bottom line

The divisor/Riemann-Roch route is conditionally sound but not presently
viable for the third p24 target.  It would prove the harmful theorem from a
low-pole modular representative of the relative packet, but producing that
representative is equivalent to the missing non-genus relative-period
primitive.  The sharp obstruction is the degree mismatch:

```text
needed for divisor contradiction: pole degree < 66254
natural relative H-character degree: 3107441
```

