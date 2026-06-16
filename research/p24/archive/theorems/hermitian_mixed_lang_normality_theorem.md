# Hermitian Mixed Lang-Normality Theorem Candidate

This note sharpens the mixed Moore-circulant theorem from
`hermitian_mixed_moore_circulant_theorem.md`.

## Semilinear Shift

For one right Frobenius orbit of length `R`, a mixed DFT orbit block has rows

```text
B(a,b) = sigma^a(seed[b-a]),       b mod R.
```

Define the semilinear cyclic shift:

```text
T(s)_b = sigma(s_{b-1}).
```

Then row `a` is `T^a(seed)`.

The fixed vectors of `T` are explicit:

```text
u_alpha(b) = sigma^b(alpha),       alpha in F_{q^R}.
```

Choosing an `F_q`-basis of `F_{q^R}` gives an invertible Moore matrix `U` with

```text
T U = U sigma.
```

Thus if

```text
seed = U*w,
```

then the row-orbit matrix is column-equivalent to an ordinary Moore matrix:

```text
(sigma^a(w_i)).
```

## Rank Criterion

For a left orbit of length `L`, the row-orbit rank is:

```text
min(L, dim_Fq span{transformed seed coordinates w_i}).
```

So full left-orbit rank is equivalent to:

```text
dim_Fq span{w_i} >= L.
```

This is stronger and cleaner than the raw skew-annihilator statement.  The
mixed Schur theorem can now be phrased as a finite-field normality theorem for
the Lang-trivialized mixed CM periods.

## p24 Shape

For the large `157 x 211` p24 mixed block:

```text
L = ord_157(p) = 156
R = ord_211(p) = 35
number of right orbits = 6
transformed coordinates = 6*35 = 210
```

The target becomes:

```text
The 210 Lang-trivialized mixed Hermitian seed coordinates have
F_p-span dimension at least 156.
```

Equivalently, at least one `156 x 156` Moore minor of those transformed seed
coordinates is nonzero modulo `p`.

## Audit

Added:

```text
p24/hermitian_mixed_lang_normality_audit.py
```

Pinned `(4,3)` rows:

```text
D=-10919:
  rows=2
  left_orbit_tests=12
  criterion_mismatches=0
  full_left_orbit_rank_tests=12

D=-8711:
  rows=2
  left_orbit_tests=12
  criterion_mismatches=0
  full_left_orbit_rank_tests=12
```

Bounded summary:

```text
rows=3
left_orbit_tests=18
criterion_mismatches=0
full_left_orbit_rank_tests=18
max_transformed_fq_rank=2
max_left_orbit_len=2
```

The tested rows only reach small left orbit length `2`, so they do not prove
the p24 theorem.  They verify the exact Lang-normality criterion on actual CM
mixed blocks and give the most compact current p24 theorem target.

## Consequence

The best current proof surface for the mixed Schur correction is:

```text
prove F_p-normality rank >= 156 for the 210 Lang-trivialized
mixed Hermitian class-field periods.
```

This is a rank-metric tuple-span theorem.  A successful arithmetic proof could
come from:

```text
1. an explicit class-field identity for the transformed coordinates;
2. a Moore determinant norm formula showing a selected 156-minor is a p-unit;
3. a local lattice/intersection theorem proving the transformed period tuple
   cannot lie in an F_p-subspace of dimension < 156.
```

The probabilistic heuristic is extremely favorable, but the certificate still
requires one of these arithmetic p-unit inputs.

## Left-Subfield Refinement

Because `gcd(156,35)=1` for p24, the transformed coordinates should land in
the left character field `F_p(mu_157)=F_{p^156}`.  This is recorded in:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
p24/hermitian_mixed_left_subfield_identity_toy.py
p24/hermitian_mixed_left_subfield_span_theorem.md
```

The refined target is:

```text
the 210 transformed coordinates span F_{p^156} over F_p.
```

Important correction: a single normal coordinate of `F_{p^156}` is not enough;
the Moore rank is the `F_p`-rank of the tuple of transformed coordinates.
