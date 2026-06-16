# Atkin-Lehner Zero-Window Boundary

This note records a near miss for the finite-field zero-lemma correspondence
route.

## Question

For a class element of order `n` and index `m=h/n`, the zero-lemma route needs
a modular/correspondence function of pole degree

```text
delta < m.
```

The ordinary `X0(N)` degree was too large for every useful p24 split class.
But class invariants often exploit Atkin-Lehner/Fricke quotients, so I tested
the optimistic lower proxy

```text
delta_AL = ceil([SL2(Z):Gamma0(N)] / 2^omega(N)).
```

This gives the full squarefree Atkin-Lehner saving whether or not an actual
function with the desired class stabilizer exists.

## Audit

I added:

```text
p24/atkin_zero_window_search.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/atkin_zero_window_search.py \
  --prime-bound 100000 --norm-bound 200000 --show 8
```

Output summary:

```text
index=314
  hit_count=280
  atkin_zero_window_hits=0
  best: delta_AL=339, index=314, norm=677

index=422
  hit_count=194
  atkin_zero_window_hits=0
  best: delta_AL=690, index=422, norm=1838, terms=(2,919)

index=66254
  hit_count=0
  atkin_zero_window_hits=0
```

The closest case is the index-314 layer:

```text
ell=677
Gamma0 degree = 678
full Atkin-Lehner quotient proxy = 339
needed index = 314
```

So even the most generous Atkin-Lehner quotient misses by a factor

```text
339 / 314 = 1.079617834...
```

## Consequence

Atkin-Lehner and Fricke quotients can improve constants and coefficient
heights, but in the tested p24 split-class window they do not make the
finite-field zero lemma fire.

The order-`3107441` layer remains completely out of range for this method:
there is no norm-`<=66254` representative, and no Atkin-Lehner quotient of a
larger representative can be assumed to have the required pole degree without
a new special invariant.

## Linear Endpoint Correction

The closest `ell=677` miss is even less close for the actual
relative-content implication.  The follow-up note

```text
p24/ell677_linear_pole_boundary.md
```

checks the endpoint-linear functions on `X0(677)`.  Harmful packet collapse
forces vanishing of linear character traces of endpoint `j`-values, not of
arbitrary low-degree functions on `X0(677)^+`.  The best descended symmetric
endpoint-linear function `j(tau)+j(677*tau)` has pole degree `677`, so the
usable comparison is

```text
677 / 314 = 2.156051...
```

rather than the optimistic proxy `339/314`.
