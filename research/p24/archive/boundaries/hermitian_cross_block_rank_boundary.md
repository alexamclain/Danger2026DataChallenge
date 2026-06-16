# Hermitian CRT Cross-Block Rank Boundary

This note closes a tempting refinement of the Hermitian axis determinant route.

The earlier structure scan reported:

```text
max_cross_block_rank_seen=1
```

in small composite-`m` rows.  That initially suggested a possible
Schur-complement shortcut: perhaps the CRT trace-zero blocks are not
orthogonal, but their pairwise couplings are always rank one.  If true, the
`2*157*211` p24 axis determinant might reduce to component block determinants
plus a tiny coupling matrix.

That hope was an artifact of the first examples.  Most early rows have a
component `2`, so one side of a cross block has dimension `1` and rank one is
automatic.

## Focused Audit

I added:

```text
p24/hermitian_cross_block_rank_audit.py
```

It filters for component pairs `c,d > 2`, so a rank-one cross block is a real
structural constraint rather than a dimension artifact.

Targeted class-number prefiltering found rows such as:

```text
D=-8711,  h=132,  m=12=4*3,  n=11,  axis_dim=6
D=-10919, h=156,  m=12=4*3,  n=13,  axis_dim=6
```

Both have a nontrivial `(4,3)` CRT trace-zero cross block.

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_cross_block_rank_audit.py \
  --only-D -8711 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 10000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 60 \
  --q-stop 400000 --max-splitting-primes 5 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_cross_block_rank_audit.py \
  --only-D -10919 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 12000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 --include-linear
```

Both reported full Hermitian Gram rank and nontrivial cross-block rank `2`:

```text
D=-8711  q=8747   h=132 m=12 n=11 deg=10 comps=[4,3]
axis_dim=6 gram_rank=6 pair_ranks=(4,3,2)

D=-8711  q=10007  h=132 m=12 n=11 deg=10 comps=[4,3]
axis_dim=6 gram_rank=6 pair_ranks=(4,3,2)

D=-10919 q=11243  h=156 m=12 n=13 deg=12 comps=[4,3]
axis_dim=6 gram_rank=6 pair_ranks=(4,3,2)

D=-10919 q=14519  h=156 m=12 n=13 deg=12 comps=[4,3]
axis_dim=6 gram_rank=6 pair_ranks=(4,3,2)
```

## Consequence

The p24 Hermitian determinant is not presently reducible to:

```text
component determinants + rank-one CRT couplings.
```

The surviving theorem is still the full coupled local-lattice statement:

```text
p does not divide Norm_{M^+/Q}(Delta_axis).
```

Any proof has to control the actual axis autocorrelation determinant, not just
independent `2`, `157`, and `211` blocks or a tiny Schur-complement correction.
