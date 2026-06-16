# Hermitian Component Schur Boundary

This note tests whether the intrinsic Hermitian axis determinant can be
reduced to CRT component determinants plus a simple correction.

## Question

For the Hermitian axis Gram matrix ordered as:

```text
constant block, component blocks U_c
```

a tempting proof split is:

```text
det(H_axis)
  = product_c det(H_c) * correction.
```

If the correction were always `1`, or a tiny predictable unit, then the p24
determinant might reduce to separate `2`, `157`, and `211` component p-unit
theorems.

## Script

Added:

```text
p24/hermitian_component_schur_audit.py
```

It computes:

```text
full Hermitian determinant;
diagonal block ranks and determinants;
product of diagonal block determinants;
correction ratio = det(full) / product(det(blocks));
maximum cross-block rank.
```

## Pinned `(4,3)` Rows

Commands:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_component_schur_audit.py \
  --only-D -10919 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 12000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 80 \
  --q-stop 500000 --max-splitting-primes 5 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_component_schur_audit.py \
  --only-D -8711 --max-rows 20 --max-cases 1 --max-h 200 \
  --max-abs-D 10000 --max-composite-quotients 20 \
  --max-axis-dim 40 --max-m 60 --max-n 60 \
  --q-stop 400000 --max-splitting-primes 5 --include-linear
```

Results:

```text
D=-10919, q=11243:
  full_det=4383
  diag_product=1919
  correction=6652
  blocks: constant det=2022, U4 det=6470, U3 det=630
  max_cross=2

D=-10919, q=14519:
  full_det=8450
  diag_product=7806
  correction=228
  max_cross=2

D=-8711, q=8747:
  full_det=1552
  diag_product=3376
  correction=8250
  max_cross=2

D=-8711, q=10007:
  full_det=4093
  diag_product=9377
  correction=7602
  max_cross=2
```

The diagonal blocks are nonsingular in these rows, but the correction is
nontrivial and varies with the split prime.  Thus diagonal component p-units
alone do not imply the full Hermitian p-unit.

## Broader Bounded Window

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_component_schur_audit.py \
  --max-rows 40 --max-cases 16 --min-h 12 --max-h 220 \
  --max-abs-D 80000 --max-prime-quotients 10 \
  --max-composite-quotients 20 --min-n 3 --max-n 220 \
  --q-stop 600000 --max-splitting-primes 2 \
  --max-axis-dim 75 --max-m 120 --include-linear --summary-only
```

reported:

```text
rows=14
full_nonzero_rows=14
full_nonzero_but_singular_diagonal_block_rows=0
correction_ratio_rows=14
distinct_correction_ratios=14
correction_ratio_one_rows=0
max_cross_rank_seen=1
```

The broad scan did not find a row where a diagonal block is singular while the
full Gram is nonsingular, so component p-unit sublemmas remain plausible.
But every row with an invertible diagonal product has a nontrivial correction
ratio, and the ratio is not visibly constant.

## Consequence

The Hermitian determinant route now has a refined hierarchy:

```text
component block p-units:
  plausible useful sublemmas;

Schur correction p-unit:
  still coupled and essential;

full Hermitian packet norm:
  current complete theorem target.
```

This pushes the p24 proof away from a pure CRT component factorization.  A
successful proof can still use component normality, but it must also control
the cross-component Schur correction as a selected CM p-unit.

The Schur correction now has a more explicit kernel-marginal form in:

```text
p24/hermitian_double_marginal_audit.py
p24/hermitian_double_marginal_formula.md
```

Every component block and cross block is a centered single or double CRT
marginal of the Hermitian autocorrelation kernel

```text
K(r,s)=Tr_packet(F_r(X)F_s(X^-1)).
```

So the coupled correction is not an arbitrary Gram determinant.  It is a
centered double-marginal p-unit target, with the largest p24 mixed table
coming from the `157 x 211` CRT component pair.

The centered marginal has an equivalent nonzero-character Fourier form:

```text
p24/hermitian_double_marginal_fourier_audit.py
p24/hermitian_double_marginal_fourier.md
```

After adjoining `mu_m`, the `U_c x U_d` block has the same rank as the mixed
K-character pairing matrix

```text
sum_{r,s} zeta_c^(u*r) zeta_d^(v*s) K(r,s),
1 <= u < c, 1 <= v < d.
```

This is probably the cleanest algebraic surface for proving the Schur
correction p-unit: diagonal component p-units plus mixed nonzero K-character
pairing p-units, packet by packet.
