# Principal-Fiber p-Unit Boundary

This note separates three related statements that were easy to conflate:
exact content, all-coordinate relative normality, and the principal-fiber
coordinate.

## Principal Fiber

Choose the complex CM class coordinate so that `j_0` is the principal singular
modulus.  For the p24 third trace, write

```text
h = m*n
m = 66254
n = 3107441.
```

For a nontrivial relative character `a`, the principal fiber is

```text
P_0(a) = sum_k zeta_n^(a*k) j_{m*k}.
```

This is the coordinate that contains the unique principal singular modulus.
The dominance theorem

```text
p24/hermitian_principal_dominance_theorem.md
```

proves

```text
P_0(a) != 0
```

in characteristic zero for every nontrivial `a`.

## Finite-Field Forms

There are three finite-field nonvanishing statements:

```text
exact content:
  for every packet f_a, not all J_u mod f_a vanish;

principal-fiber p-unit at a chosen prime P:
  J_0 mod f_a is nonzero for the coordinate in which the selected reduction
  of j_0 is the origin;

all-prime principal-fiber p-unit:
  J_0 mod f_a is nonzero for every prime P above p.
```

The all-prime version is equivalent to all-coordinate relative normality in
one finite-field root set.  Indeed, changing the prime above `p` translates
the CM torsor, and the origin-shift formula

```text
p24/relative_origin_shift_invariance.md
```

shows that the distinguished `u=0` fiber runs through the quotient coordinates
up to multiplication by powers of `X`.

Thus:

```text
all selected primes have principal-fiber nonzero
  <=>  Res(Phi_n, J_u) != 0 for every u.
```

## Why The Single-Fiber Theorem Is Not Enough By Itself

For an existence proof, it would be enough to prove that there exists at least
one prime above `p` where the principal fiber is nonzero.  But a DANGER
certificate must output an explicit finite-field root or Montgomery parameter.
Without an embedded selector for that prime/root, an existential good prime is
not a construction.

This is why the stronger all-coordinate theorem remains attractive: it avoids
choosing among split primes.  Any selected CM root would have the principal
fiber nonzero after relabeling.

## Toy Calibration

The selected-prime resultant scan now tracks `distinguished_zero`, meaning
whether the `u=0` fiber vanishes:

```text
p24/relative_resultant_selected_prime_scan.py
p24/relative_resultant_selected_prime_scan.md
```

For the pinned composite failure:

```text
D=-1336, q=1777, h=12, m=2, n=6
```

the unique coordinate-zero packet appears on every origin, but
`distinguished_zero` occurs only on half the origins:

```text
coord_zero_packets=12
unique_coord_zero_packets_ignoring_origin=1
distinguished_zero_packets=6
content_zero_packets=0
```

This is exactly the origin-shift permutation behavior.  It also shows why
composite coordinate normality is too strong in general, even though exact
content remains true.

In the bounded prime-`n` multi-splitting window, no distinguished or
all-coordinate failures appeared:

```text
packet_rows=361
prime_packet_rows=204
coord_zero_packets=0
distinguished_zero_packets=0
```

A later wider selected-prime scan found a prime-`n` coordinate failure:

```text
p24/prime_relative_normality_counterexample.md

D=-956 q=3307 h=15 m=5 n=3 deg=1
coord_zero=1 content_zero=0 hermitian_zero=0
```

By origin-shift symmetry, this means the broad all-coordinate/product theorem
is not a general prime-`n` CM theorem.  The p24 all-coordinate statement may
still be true, but it would need p24-specific selected-prime arithmetic.

## Current Best Form

The cleanest sufficient p24 theorem is still:

```text
Res(Phi_3107441, J_u) != 0 mod p for every 0 <= u < 66254.
```

The more conceptually motivated version is:

```text
the principal relative fiber P_0(a) is a p-unit at every split prime above p.
```

This version has the strongest characteristic-zero dominance input, but it
still needs a selected-prime p-adic unit theorem.  Dominance alone only proves
nonzero algebraic numbers, not p-units.
