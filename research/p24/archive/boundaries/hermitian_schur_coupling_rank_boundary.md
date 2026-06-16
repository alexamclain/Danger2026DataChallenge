# Hermitian Schur Coupling Rank Boundary

This note tests whether the Hermitian Schur correction is a small low-rank
perturbation of the diagonal component blocks.

## Question

Write the Hermitian axis Gram matrix as:

```text
G = D + E,
```

where `D` is block diagonal with the constant and CRT component blocks, and
`E` contains only off-diagonal cross-block pairings.  If `E` had small rank,
then

```text
det(G) / det(D)
```

would be a small low-rank determinant.  That would be a much easier p-unit
target than the full mixed character-pairing matrix.

## Script

Added:

```text
p24/hermitian_schur_coupling_rank_audit.py
```

It reports:

```text
rank(E);
det(G);
det(G)/prod diagonal block determinants;
maximum individual cross-block rank.
```

## Pinned `(4,3)` Rows

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_schur_coupling_rank_audit.py \
  --only-D -10919 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 12000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_schur_coupling_rank_audit.py \
  --only-D -8711 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 10000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 60 \
  --q-stop 400000 --max-splitting-primes 5 \
  --max-factor-degree 20 --include-linear
```

Results:

```text
D=-10919, q=11243:
  axis_dim=6
  offdiag_rank=6/6
  correction=6652
  max_cross=2

D=-10919, q=14519:
  axis_dim=6
  offdiag_rank=6/6
  correction=228
  max_cross=2

D=-8711, q=8747:
  axis_dim=6
  offdiag_rank=6/6
  correction=8250
  max_cross=2

D=-8711, q=10007:
  axis_dim=6
  offdiag_rank=6/6
  correction=7602
  max_cross=2
```

The total off-diagonal coupling has full rank even in the smallest nontrivial
`(4,3)` rows.

## Bounded Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_schur_coupling_rank_audit.py \
  --max-rows 30 --max-cases 12 --min-h 12 --max-h 220 \
  --max-abs-D 80000 --max-prime-quotients 10 \
  --max-composite-quotients 20 --min-n 3 --max-n 220 \
  --q-stop 600000 --max-splitting-primes 2 \
  --max-axis-dim 75 --max-m 120 --max-factor-degree 80 \
  --include-linear --summary-only
```

reported:

```text
rows=9
full_nonzero_rows=9
high_offdiag_rank_rows=9
max_offdiag_rank_ratio=1.000000
```

## Consequence

The Schur correction is not a tiny low-rank perturbation determinant in the
natural CRT block decomposition.  The remaining p24 theorem should be treated
as a genuinely coupled mixed-character p-unit:

```text
diagonal component p-units
  + full mixed nonzero K-character Hermitian pairing p-unit.
```

The Fourier form in:

```text
p24/hermitian_double_marginal_fourier.md
```

is therefore not just cosmetic; it is the clean algebraic formulation of the
full-rank coupled correction.
