# Hermitian Origin-Invariance Theorem

This note records a structural win for the Hermitian axis determinant.

## Statement

Fix a packet factor

```text
f_a | Phi_n,      A_a = F_p[X]/(f_a),
```

with `d=deg(f_a)` even and

```text
p^(d/2) == -1 mod n.
```

For a chosen CM origin, write

```text
F_r(X) = sum_k j_{n*r + m*k} X^k.
```

For an origin shift `s`, choose CRT coordinates

```text
s == n*alpha + m*beta mod h.
```

Then the shifted fibers are

```text
F'_r(X) = X^(-beta) * F_{r+alpha}(X) in A_a.
```

The axis coefficient space

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}
```

is stable under `r -> r+alpha`.  This translation is an integral unimodular
change of the standard axis basis.

For the Hermitian trace pairing

```text
<x,y> = Tr_{A_a/F_p}(x * y^(p^(d/2))),
```

the scalar monomial cancels:

```text
<X^(-beta)x, X^(-beta)y>
 = Tr(X^(-beta)x * X^(-beta*p^(d/2)) y^(p^(d/2)))
 = Tr(X^(-beta)x * X^(beta) y^(p^(d/2)))
 = <x,y>.
```

Therefore the Hermitian axis Gram determinant is independent of the embedded
CM origin, up to the square of a unimodular axis-basis determinant, hence
exactly unchanged modulo sign conventions and certainly unchanged as a
p-unit/non-p-unit condition.

## Consequence

The p24 Hermitian axis theorem no longer has to prove a separate statement for
each chosen embedded origin.  For each H-packet, origin shifts give congruent
Hermitian Gram matrices.  The selected-prime theorem is still packetwise, but
not originwise.

This is specific to the Hermitian pairing.  The ordinary trace pairing uses

```text
Tr(X^(-beta)x * X^(-beta)y)
```

and the monomial factor does not cancel.  This explains why ordinary
trace-Gram failures can move with the origin while Hermitian failures do not.

## Data Check

I added:

```text
p24/hermitian_gram_determinant_distribution.py
```

Pinned ordinary trace-Gram failure:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_gram_determinant_distribution.py \
  --only-D -524 --min-h 12 --max-h 20 \
  --max-prime-quotients 10 --max-composite-quotients 10 \
  --min-n 3 --max-n 20 --q-start 167 --q-stop 168 \
  --max-splitting-primes 1 --max-axis-dim 20 --include-linear
```

reported:

```text
origins=15
zeros=0
distinct_values=1
squareclasses={'nonsquare': 15}
```

Composite all-origin window:

```text
determinant_origin_rows=30
determinant_packets=1
packets_with_zero_determinant_origin=0
origin_invariant_packets=1
squareclass_invariant_packets=1
distinct_value_count_histogram={1: 1}
```

Broader all-origin window:

```text
determinant_origin_rows=195
determinant_packets=9
packets_with_zero_determinant_origin=0
origin_invariant_packets=9
squareclass_invariant_packets=9
distinct_value_count_histogram={1: 9}
```

The data matches the theorem: Hermitian determinant values are origin
invariant in every tested packet.

## New Target

The local-lattice theorem should be stated packetwise:

```text
For each of the eight p24 H-character packets, the Hermitian axis Gram
determinant is a p-unit.
```

The embedded origin can be chosen for convenience; it is not an additional
arithmetic variable.
