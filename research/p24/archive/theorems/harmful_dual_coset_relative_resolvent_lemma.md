# Harmful Dual-Cosets Are Relative Resolvents

This note sharpens the exact additive-selector obstruction from
`dual_coset_annihilator_lemma.md`.

## Setup

Let

```text
G = Z/hZ,       h = m n,
H = <m>,        |H| = n,
G/H has size m,
Q_H = {0,n,2n,...,(m-1)n}
```

and index the embedded CM cycle by

```text
j_i,       0 <= i < h.
```

Write every index uniquely as

```text
i = u + m k,      0 <= u < m,  0 <= k < n.
```

Work over a splitting field of characteristic prime to `h`.
Let `zeta_h` be a primitive `h`-th root, and set

```text
zeta_m = zeta_h^n,
zeta_n = zeta_h^m.
```

For a character index `s`, define the full class-character resolvent

```text
R_s = sum_{i=0}^{h-1} zeta_h^(s i) j_i.
```

For a residue class `a mod n`, define the relative `H`-character sums on
quotient fibers:

```text
P_u(a) = sum_{k=0}^{n-1} zeta_n^(a k) j_{u+m k},
          0 <= u < m.
```

## Lemma

For any `a mod n`,

```text
R_{a+r n} = 0 for every 0 <= r < m
```

if and only if

```text
P_u(a) = 0 for every 0 <= u < m.
```

Thus a harmful dual-coset vanishing

```text
a + Q_H,       a not == 0 mod n,
```

is exactly the statement that the nontrivial relative `H`-character `a`
vanishes separately on every quotient fiber.

## Proof

Using the decomposition `i=u+m k`,

```text
R_{a+r n}
  = sum_u sum_k zeta_h^((a+r n)(u+m k)) j_{u+m k}
  = sum_u zeta_h^(a u) zeta_m^(r u)
          [sum_k zeta_n^(a k) j_{u+m k}]
  = sum_u zeta_h^(a u) zeta_m^(r u) P_u(a).
```

For fixed `a`, the `m` values `R_{a+r n}` are the length-`m` Fourier
transform of the vector

```text
V_u(a) = zeta_h^(a u) P_u(a).
```

The Fourier matrix over an algebraic closure is invertible, so all
`R_{a+r n}` vanish if and only if every `V_u(a)` vanishes, which is
equivalent to every `P_u(a)` vanishing.

## Edge Cases

If `a == 0 mod n`, this is the quotient-character case: `P_u(0)` is the
ordinary `H`-period sum on the fiber.  This is useful, but it is not a
harmful non-quotient coset.

If `g = gcd(a,n) > 1`, the relative character on `H` is imprimitive and has
kernel size `g`.  The inverse-Fourier codeword from `a+Q_H` is still supported
on `H`, and adding a scalar multiple to the subgroup projector can cancel at
most `g` positions of that projector.  This recovers the cancellation count
in `dual_coset_annihilator_lemma.md`.

The statement is made over an algebraic closure containing `mu_h`.  Over
`F_p`, vanished character sets are Frobenius-stable: if the embedded `j_i` lie
in `F_p` and one full coset `a+Q_H` vanishes, then every coset

```text
p^e a + Q_H
```

in the Frobenius orbit also vanishes.

Equivalently, an `F_p`-rational certificate should packetize the relative
condition: if `f_a` is the minimal polynomial of `zeta_n^a` over `F_p`, then
the Frobenius packet of harmful cosets vanishes exactly when each fiberwise
relative polynomial vanishes modulo `f_a`.  A single algebraic `H`-supported
cancellation word need not descend by itself to an `F_p`-valued sparse
selector.

## p24 Consequence

For the third p24 target,

```text
m = 66254,
n = 3107441,
h = 205880396014,
p mod n = 2509452,
ord_n(p) = 388430,
(n-1)/ord_n(p) = 8.
```

Since `n` is prime, a single algebraic harmful coset cancels only one of the
`n` subgroup-projector positions.  But over `F_p` this event propagates to a
Frobenius orbit of

```text
388430
```

nonzero relative `H`-characters, i.e. to `388430` complete harmful dual
cosets.  In character-count terms that is

```text
66254 * 388430 = 25735041220 = h/8
```

vanished full characters.

So the missing p24 theorem can be stated more explicitly:

```text
No Frobenius orbit of nontrivial relative H-characters has P_u(a)=0 on every
quotient fiber u.
```

This is weaker than full reduced normality, but much stronger than generic
quotient support.  It asks for nonvanishing of fiberwise relative
class-character sums, not just nonvanishing of global quotient periods.

## Current Status

This lemma is a proof reduction, not yet the desired certificate.  It says the
sparse-selector route can only pass through a very structured relative
resolvent collapse.  The remaining arithmetic input is to rule out that
collapse for the selected p24 CM embedding, or to prove the still weaker
minimum-weight condition for the actual CM annihilator.
