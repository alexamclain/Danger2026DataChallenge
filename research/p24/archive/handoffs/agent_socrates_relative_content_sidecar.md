# Agent Socrates: Relative Content Sidecar

Task: audit whether the third p24 target can rule out a harmful nontrivial
`H`-character Frobenius packet without enumerating the CM class set.

Target data:

```text
h = 205880396014 = m*n
m = 66254
n = 3107441 prime
ord_n(p) = 388430
(n-1)/ord_n(p) = 8
```

For a nonzero relative character orbit represented by `a`, the exact finite
field condition is:

```text
J_u(X) = sum_k j_{u+m*k} X^k
harmful packet vanishes <=> J_u(X) == 0 mod f_a(X) for every u,
```

where `f_a` is the minimal polynomial of `zeta_n^a` over `F_p`.

## Experimentally Testable Invariants

The most useful exact invariant is the **relative content gcd**

```text
C_a(X) = gcd(f_a(X), J_0(X), J_1(X), ..., J_{m-1}(X)).
```

Then:

```text
deg C_a = deg f_a      <=> harmful Frobenius packet
deg C_a = 0            => exact Bezout certificate exists
0 < deg C_a < deg f_a  => partial Frobenius-subpacket collapse
```

This is better than product tests.  The product certificate
`prod_u (J_u mod f_a) != 0` is sufficient but too strong, because it fails
when one fiber vanishes; the harmful event needs every fiber to vanish.

A secondary invariant is the **normal determinant/gcd**

```text
J(T) = sum_i j_i T^i
gcd(J(T), T^h - 1).
```

If this gcd is `1`, all class-character resolvents are nonzero in the selected
finite-field embedding, so no harmful packet can occur.  This is strong but
not generic enough to be an easy theorem: small CM counterexamples already
exist at low order.

Small local checks run here:

```text
natural_relative_resolvent_scan:
  rows=3, quotient_rows=7
  relative_characters_tested=31
  relative_fibers_tested=117
  harmful_a_total=0
  individual_zero_fiber_total=0
  expected_random_zero_fibers=0.024508

normal_basis_support_toy:
  first 4 CM rows had gcd_degree=0

reduced_resolvent_vanishing_scan:
  rows=4, normal_rows=4, nonnormal_rows=0
```

Random-vector baseline over `q=31, h=30`:

```text
m=5,n=6:  harmful=0/10000, zero_fibers=1620, expected=1612.90
m=6,n=5:  harmful=0/8000,  zero_fibers=1505, expected=1548.39
m=3,n=10: harmful=1/18000, zero_fibers=1761, expected=1741.94
```

Also, an artificial vector can force `J_u(zeta_n^a)=0` for all `u` by one
linear constraint per fiber.  So the desired theorem cannot be pure linear
algebra; it must use the arithmetic of the selected CM vector.

The only invariant that cleanly distinguishes true CM cycles from random
vectors is the low-degree modular-correspondence residual, e.g.
`Phi_ell(j_i,j_{i+1})=0` along a split-prime cycle.  That is a sanity marker,
not a selector: turning it into a relative-content nonvanishing theorem still
requires high-order class-character information.

## Possible Theorem Statement

Exact content theorem:

```text
Let O be the conductor-2 CM order for the third p24 trace, let G=Cl(O) be
cyclic of order h=m*n, and let H=<m> have order n.  Fix the selected ordinary
prime P above p and the embedded singular-modulus cycle (j_g) in F_p.

For each of the eight Frobenius orbits of primitive nontrivial H-characters,
represented by a in (Z/nZ)^*, let f_a be the minimal polynomial of zeta_n^a
over F_p and define J_u as above.  Then

    gcd(f_a, J_0, ..., J_{m-1}) = 1

in F_p[X].
```

Equivalent ideal form:

```text
The relative content ideal (P_u(a) : 0 <= u < m) is not contained in the
selected prime P above p.
```

Stronger normality theorem:

```text
The normal determinant
    prod_chi sum_g chi(g) j_g
is a P-adic unit.
```

This stronger theorem implies the content theorem.  The existing dominance
check proves the corresponding characteristic-zero resolvents are nonzero for
the three p24 targets, with enormous margins, but it does not prove they are
units at the selected prime.

## Why This Might Lift To p24

The random model is violently favorable.  For one p24 relative packet the
ambient field has size `p^388430`, and the all-zero vector imposes

```text
m * deg(f_a) = 66254 * 388430
```

linear-looking conditions.  A random vector predicts probability
`p^(-66254*388430)`.  The small CM scans also show no primitive high-order
packet collapse, and normality holds in the tested `h >= 12` rows.

There is also a plausible structural reason: p24's relevant packets are
primitive high-order non-genus packets, while known small CM failures are
low-order accidents.  A theorem excluding primitive packets under conductor-2,
large-discriminant, selected-split-prime hypotheses would be exactly enough.

## Why This Might Not Lift

The core obstruction is embedded p-adic unit control.  Archimedean dominance
proves `P_u(a)` or `T_chi` is nonzero as an algebraic number, but p24 needs
nonzero after reduction at one specific prime above `p`.  Norms of these
periods are enormous, so `p`-divisibility is not ruled out by height.

Known no-go boundaries still apply:

```text
Gross-Zagier style norms control pairwise j-differences, not relative periods.
Genus/trivial trace formulas do not cover order-157/211/non-genus characters.
Local normal-basis theorems provide some normal element, not this j element.
Pure cyclic-code minimum-weight statements are false without CM input.
```

Bottom line: the exact finite-field invariant to test is `deg gcd(f_a,J_0,...,J_{m-1})`.
The promising theorem is a p-adic unit/noncontainment statement for the
relative content ideal.  The route is certificate-shaped, but it does not
currently give a sub-sqrt constructive selector for p24 unless one can prove
that unit statement without computing the high-order CM periods.
