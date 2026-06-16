# Subagent Toeplitz/Schur Synthesis

Date: 2026-06-05

The existing subagent was asked whether the Toeplitz/Jacobi-Trudi form of the
weighted Fourier minor imports any known theorem strong enough to prove the
p24 selected-prime p-unit.

## Verdict

The Toeplitz/Jacobi-Trudi rewrite is correct and useful as notation, but by
itself it restates the same noncancellation problem.

Since:

```text
F * diag(lambda) * F^-1
```

is a circulant, the selected trace-frame minor is a cyclic Toeplitz determinant
in the inverse-DFT symbol coefficients.  Equivalently, it can be viewed as a
skew/cylindric Schur-Jacobi-Trudi determinant attached to the row/column index
sets defining `Delta_lead`.

## Non-Fitting Imports

The following known frameworks do not directly prove the selected p-unit:

```text
Toeplitz total positivity / PF_infinity:
  positivity does not survive as a finite-field p-unit theorem without a
  separate p-adic no-cancellation argument.

Skew-Schur positivity / LGV paths:
  gives positive path expansions over ordered fields, but modulo p the same
  expansion can cancel.

Finite-field superregular circulants:
  false for arbitrary invertible spectral twists; the small toy already has
  an invertible circulant with a zero selected minor.

Chebotarev/Tao uncertainty:
  controls untwisted Fourier minors, not the interior CM diagonal twist.
```

The local toy boundary is:

```text
p24/twisted_chebotarev_minor_toy.py
p24/weighted_fourier_cauchy_binet_toy.py
p24/weighted_toeplitz_minor_toy.py
```

It shows that nonzero spectral weights, full Cauchy-Binet support, nonzero
Toeplitz symbol coefficients, and even full circulant invertibility do not
force the selected minor to be nonzero.

## Sharp Theorem Candidate

The useful standard-form theorem is:

```text
CM cyclic skew-Schur p-unit theorem:

For each beta orbit Omega, let c_r be the inverse-DFT symbol coefficients of
Lambda_CM in the orbit algebra A_Omega.  For the cyclic index data (T,S)
defining Delta_lead, the Jacobi-Trudi / Toeplitz determinant

  JT_{T,S}(c) = det(c_{t_i-s_j})

is a unit in A_Omega.
```

Equivalently:

```text
R_lead,Omega is a p-unit.
```

## What Would Make It A Proof

To become more than a restatement, this surface needs an extra arithmetic
mechanism:

```text
1. a unique p-adically minimal tableau/path term in the LGV/Jacobi-Trudi
   expansion;
2. a hidden p-unit equivalence reducing the CM twist to row/column scaling of
   a superregular Fourier/MSRD/LRS matrix;
3. a class-field/divisor theorem saying the actual CM symbol avoids this
   selected skew-Schur divisor.
```

Without one of these, Toeplitz/skew-Schur language is a clean coordinate
system for the determinant-line local-unit theorem, not an independent proof.
