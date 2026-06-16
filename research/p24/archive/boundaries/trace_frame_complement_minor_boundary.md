# Trace-Frame Complement-Minor Boundary

Date: 2026-06-05

This note records what Jacobi's complementary-minor identity does, and does
not, buy for the selected translate-minor theorem.

## Identity

Let `M` be the cyclic translate matrix:

```text
M_{a,b} = j_{a-b}.
```

If `M` is invertible and `I,J` are `k`-subsets, then Jacobi's identity gives:

```text
det(M_{I,J})
  = +/- det(M) * det((M^{-1})_{J^c,I^c}).
```

For the p24 trace-frame target:

```text
n = 3107441
k = 368
n-k = 3107073.
```

Thus full reduced normality:

```text
det(M) != 0
```

turns the selected `368 x 368` minor p-unit theorem into the p-unit theorem
for a complementary:

```text
3107073 x 3107073
```

minor of `M^{-1}`.

## Toy Check

I added:

```text
p24/translate_minor_complement_toy.py
```

It uses the same invertible length-`5` translate matrix from the Toeplitz
boundary.  It verifies Jacobi's identity on both a vanishing selected minor
and a nonzero selected minor:

```text
full_translate_det=2
selected_minor=0
selected_jacobi_rhs=0
selected_jacobi_matches=1
nonzero_minor=8
nonzero_jacobi_rhs=8
nonzero_jacobi_matches=1
```

So the identity is correct, but it only mirrors selected-minor vanishing into
a complementary inverse-minor vanishing.

## Why This Does Not Finish p24

The inverse translate matrix is also diagonalized by Fourier:

```text
M^{-1} = F * diag(lambda_u^{-1}) * F^{-1}
```

up to p-unit normalization.  So the complementary minor is another weighted
Fourier/Toeplitz/skew-Schur determinant, now of size `n-368`.

This does not shrink the certificate or expose a simpler divisor.  It is
usually worse for p24:

```text
selected minor size:       368
complement inverse size:   3107073
```

The only way Jacobi's identity helps is if one has an independent theorem
about the inverse CM symbol or the huge complementary Schubert coordinate.
No such theorem is currently visible.

## Consequence

The standard full-determinant route is closed as a shortcut:

```text
full reduced normality + Jacobi complement
  does not imply selected translate-minor p-unitness.
```

It restates the local-unit theorem as a different selected Schubert p-unit,
and that version is much larger.  The useful target remains the original
`368 x 368` determinant:

```text
R_lead,Omega is a p-unit.
```
