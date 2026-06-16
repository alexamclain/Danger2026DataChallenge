# Trace-Frame Translate-Minor Form

Date: 2026-06-05

This note identifies the CM-weighted Fourier determinant with a selected minor
of a cyclic translate matrix.  It is the bridge between the current
local-unit theorem and the reduced-normality notes.

## Fourier-To-Translate Identity

Let `j_r`, `r mod n`, be a cyclic CM torsor sequence over a field containing
`mu_n`, and define its class-character resolvents by:

```text
lambda_u = sum_r j_r zeta^(-u*r).
```

Then:

```text
C = F * diag(lambda) * F^{-1}
```

is, up to the harmless Fourier normalization convention, the cyclic translate
matrix:

```text
C_{a,b} = j_{a-b}.
```

Equivalently, the Toeplitz symbol:

```text
c_d = (1/n) * sum_u lambda_u zeta^(d*u)
```

is exactly the original embedded CM sequence:

```text
c_d = j_d.
```

Since `n=3107441` is prime to `p`, the normalization is a p-unit.  Therefore
the p24 weighted Schubert determinant is p-unit equivalent to a selected
minor of the cyclic translate matrix of the relevant singular-moduli period
sequence.

## Relation To Reduced Normality

The full cyclic translate determinant is:

```text
det(j_{a-b})_{a,b in Z/nZ}
  = product_u lambda_u
```

by Dedekind's group determinant formula.  This is the reduced-normality
determinant.

The current trace-frame theorem needs a selected minor, not the full
determinant:

```text
det(j_{t_i-s_j})_{i,j=1}^{368}.
```

Thus:

```text
full reduced normality
```

is necessary-looking but not sufficient for the selected Schubert p-unit.

## Toy Boundary

The toy:

```text
p24/weighted_toeplitz_minor_toy.py
```

reports:

```text
inverse_dft_symbol=[10, 5, 4, 1, 3]
zero_symbol_count=0
operator_equals_cyclic_toeplitz=1
full_circulant_det=2
spectral_product=2
operator_minor=0
toeplitz_minor=0
```

So the full translate matrix is invertible and every character resolvent is
nonzero, but the selected minor vanishes.

This is the finite-field version of the warning in:

```text
p24/reduced_normality_proof_frontier.md
```

Reduced normality controls the full group determinant.  The trace-frame
certificate needs a selected translate minor / Schubert coordinate.

## p24 Theorem Candidate

The determinant-line local-unit theorem can now be stated as:

```text
For each beta-orbit algebra A_Omega, the selected 368 x 368 translate minor
of the p24 singular-moduli torsor sequence is a p-unit.
```

Equivalently:

```text
R_lead,Omega is a p-unit.
```

This is not easier by itself, but it is more class-field-facing.  It suggests
three possible proof inputs:

```text
1. selected-minor p-adic nonvanishing for singular-moduli translate matrices;
2. a CM-adapted row/column change turning this selected minor into the full
   reduced-normality determinant or an MSRD minor;
3. a divisor formula for the selected translate minor as a Schubert coordinate
   on the embedded class-field torsor.
```

Without one of these, full normality and nonzero resolvents remain too weak.

Two standard determinant shortcuts are now separated in:

```text
p24/trace_frame_complement_minor_boundary.md
p24/trace_frame_translate_minor_dominance_boundary.md
```

Jacobi complementary minors convert the target into a much larger inverse
minor, and archimedean principal dominance can prove only characteristic-zero
nonvanishing.  Neither supplies selected-prime p-unitness on its own.

The verifier-facing selected-origin version is specified in:

```text
p24/trace_frame_selected_minor_certificate_spec.md
```

It records a useful compression from the raw `368 x 368` matrix to the
length-`66254` Toeplitz symbol.  It also records the important boundary that a
literal symbol over every beta-orbit algebra is much larger than `sqrt(p)`;
the beta-orbit statement has to be proved by a reduced norm or class-field
identity, not by table enumeration.
