# Dual-Coset Annihilator Lemma

This note explains the structured artificial counterexamples in the cyclic-code
minimum-weight scans.

## Setup

Let

```text
G = Z/hZ,       h = m n,
H = <m>,        |H| = n,
Q_H = {0,n,2n,...,(m-1)n}
```

where `Q_H` is the dual subgroup of characters trivial on `H`.

The subgroup projector is

```text
e_H = sum_{k=0}^{n-1} T^{m k}.
```

Its Fourier transform is supported exactly on `Q_H`.

## Lemma

Suppose the annihilator of the reduced CM vector contains all characters in a
nontrivial dual coset

```text
a + Q_H,       a not == 0 mod n.
```

Equivalently, all resolvents in this coset vanish modulo the selected prime.
Then `Ann(J)` contains a codeword supported on `H`, whose values on `H` are a
nontrivial character of `H`.

Consequently the affine coset

```text
e_H + Ann(J)
```

has a representative of support at most

```text
n - gcd(a,n).
```

If `n` is prime, as in the third p24 target with

```text
n = 3107441,
```

a single nontrivial dual-coset vanishing can reduce support by only one.
Large support reduction would require many such cosets or a more structured
annihilator.

## Proof

Let `zeta` be a primitive `h`-th root.  The inverse Fourier transform of the
indicator of `a+Q_H` has coefficient at position `i` proportional to

```text
sum_{r=0}^{m-1} zeta^{-(a+r n)i}
  = zeta^{-a i} * sum_{r=0}^{m-1} (zeta^{-n i})^r.
```

The geometric sum vanishes unless `m | i`.  Thus the codeword is supported on
the subgroup positions `i=m k`.  On those positions it is proportional to

```text
zeta^{-a m k},
```

a character of the order-`n` subgroup `H`.  This character has kernel size
`gcd(a,n)`.  Adding a scalar multiple of this codeword to `e_H` can cancel one
fiber of equal character value, i.e. `gcd(a,n)` of the `n` nonzero projector
positions.

## Relative-Resolvent Form

The same harmful event has a sharper arithmetic interpretation.  Write
`i=u+m k` and define

```text
P_u(a) = sum_{k=0}^{n-1} zeta_n^(a k) j_{u+m k}.
```

Then all full resolvents in the dual coset `a+Q_H` vanish if and only if

```text
P_u(a) = 0       for every quotient fiber u.
```

This is proved in:

```text
p24/harmful_dual_coset_relative_resolvent_lemma.md
```

So a harmful coset is not merely an abstract coding event; it is a fiberwise
relative class-character collapse.

## Toy Evidence

The scan

```text
p24/cyclic_code_min_weight_scan.py
```

found exactly this pattern in the first reductions:

```text
h=4,  m=2, vanished=[1,3],     best 2 -> 1
h=6,  m=2, vanished=[1,4],     best 3 -> 2
h=8,  m=2, vanished=[1,5],     best 4 -> 3
h=10, m=2, vanished=[1,6],     best 5 -> 4
h=12, m=3, vanished=[1,5,9],   best 4 -> 3
```

Each vanished set is a translate `a+Q_H`.

The actual small CM reduced-normality failures

```text
D=-216
D=-300
```

do not contain such a harmful coset for their tested quotients, and their
projector support remains exact.

## p24 Consequence

For the third trace, the exact additive support theorem can be weakened again:
it is enough to rule out enough harmful dual-coset vanishings in the CM
annihilator.  Full reduced normality rules them all out, but is stronger than
needed.

This still does not give a certificate.  It says any p-specific sparse
additive selector would need a highly structured annihilator, not just an
isolated Frobenius packet vanishing.
