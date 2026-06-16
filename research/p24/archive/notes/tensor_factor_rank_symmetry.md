# Tensor Factor Rank Symmetry

This note records why the one-factor tensor rank target is independent of
which tensor factor is chosen.

## Setup

For one H-character packet:

```text
A = F_p[X]/(f_a),      [A:F_p]=d=ord_n(p),
E = F_p(mu_m),         [E:F_p]=e=ord_m(p),
g = gcd(d,e).
```

Then:

```text
A tensor_{F_p} E ~= product_{i=0}^{g-1} B_i,
```

with each `B_i/E` of degree `d/g`.

For p24:

```text
d = 388430
e = 5460
g = 70
d/g = 5549
```

## Semilinear Symmetry

The absolute Frobenius `x -> x^p` is not `E`-linear, but it is semilinear
over the automorphism `E -> E`, `alpha -> alpha^p`.  It cyclically permutes
the `g` tensor factors.

For a K-character resolvent

```text
R_s(eta) = sum_{r,k} zeta_m^(s*r) j_{n*r+m*k} eta^k,
```

Frobenius gives

```text
R_s(eta)^p = R_{p*s}(eta^p).
```

The selected axis frequency set is stable under `s -> p*s mod m`, because it
is the union of the nonzero character sets of the factors `2`, `157`, and
`211`, plus the constant frequency.  Therefore Frobenius sends the whole
axis-resolvent family in one tensor factor to the same family in the next
tensor factor, up to a semilinear coefficient automorphism and a permutation
of the rows.

Semilinear field isomorphisms preserve linear rank.  Hence:

```text
axis rank in B_i is independent of i.
```

Thus the one-factor theorem can be stated as either:

```text
some B_i has full axis rank,
```

or equivalently:

```text
every B_i has full axis rank.
```

The second formulation is cleaner for a p-unit norm statement; the first is
cleaner for a compact finite certificate.

## Data Check

I updated:

```text
p24/k_character_tensor_factor_rank_scan.py
```

to report equal/unequal factor ranks.

Pinned row:

```text
D=-10919
rows=1
one_factor_full_axis_rows=1
equal_factor_rank_rows=1
unequal_factor_rank_rows=0
```

Broader small window:

```text
rows=20
tensor_factor_count_histogram={2: 20}
full_tensor_axis_possible_rows=3
full_tensor_axis_failure_rows=0
one_factor_full_axis_rows=2
equal_factor_rank_rows=20
unequal_factor_rank_rows=0
one_factor_dimension_possible_rows=2
one_factor_dimension_possible_no_full_factor_rows=0
```

This matches the semilinear argument.

## p24 Certificate Surface

For p24, it is enough to prove the `368 x 368` determinant of any coordinate
minor of the 368 axis resolvents is nonzero in one degree-`5549` tensor
factor over `E=F_p(mu_m)`.

By the symmetry above, nonzero in one factor implies nonzero rank in all
conjugate tensor factors, and by scalar-extension descent it implies the
original packet axis injectivity over `F_p`.
