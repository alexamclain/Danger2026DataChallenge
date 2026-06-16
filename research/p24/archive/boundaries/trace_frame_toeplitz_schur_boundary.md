# Trace-Frame Toeplitz/Schur Boundary

Date: 2026-06-05

This note rewrites the weighted Fourier minor as a cyclic Toeplitz minor.  It
is a useful standard form, but by itself it does not prove the p24 p-unit.

## Toeplitz Form

Let:

```text
C = F * diag(lambda) * F^{-1}
```

over a field containing `mu_n`, where `F` is the `n x n` Fourier matrix.
Then `C` is a circulant/Toeplitz operator.  If:

```text
c_d = (1/n) * sum_u lambda_u zeta^(d*u),
```

then:

```text
C_{r,s} = c_{r-s}.
```

Thus every weighted Fourier minor:

```text
det(C_{T,S})
```

is a cyclic Toeplitz minor:

```text
det(c_{t_i-s_j})_{i,j}.
```

When the row and column sets are consecutive, this is an ordinary Toeplitz
determinant.  For arbitrary increasing row/column sets, it is the finite
cyclic analogue of the Jacobi-Trudi/skew-Schur Toeplitz minor attached to
those index sets.

## Toy Boundary

I added:

```text
p24/weighted_toeplitz_minor_toy.py
```

It uses the same `F_11`, length-`5` spectral twist as:

```text
p24/twisted_chebotarev_minor_toy.py
p24/weighted_fourier_cauchy_binet_toy.py
p24/trace_frame_translate_minor_form.md
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/weighted_toeplitz_minor_toy.py
```

It reports:

```text
inverse_dft_symbol=[10, 5, 4, 1, 3]
zero_symbol_count=0
operator_equals_cyclic_toeplitz=1
full_circulant_det=2
spectral_product=2
operator_minor=0
toeplitz_minor=0
minor_matches=1
```

So even a cyclic Toeplitz matrix with every symbol coefficient nonzero can
have a selected minor vanish.  In fact, the full circulant determinant is
nonzero in the toy, so full reduced normality does not imply the selected
minor.  In finite characteristic there is no positivity or total-positivity
principle to prevent this cancellation.

## p24 Meaning

The p24 trace-frame determinant can be viewed as a relative/crossed-product
version of:

```text
det(c_{t_i-s_j})
```

where:

```text
T = selected relative-coefficient / Schubert rows,
S = selected smooth-axis character columns,
c = inverse DFT of the singular-moduli class-character weights.
```

This gives another exact theorem formulation:

```text
the selected cyclic Toeplitz/skew-Schur minor for the p24 CM symbol c is a
p-unit.
```

But the toy closes the easy implication:

```text
all CM Fourier weights nonzero
and all symbol coefficients nonzero
  => selected Toeplitz minor nonzero.
```

The implication is false.

## Surviving Uses

The Toeplitz/Schur form can still help if it exposes additional arithmetic:

```text
1. a CM-adapted symbol factorization whose Jacobi-Trudi determinant is a
   known p-unit;
2. a p-unit row/column/block change making the selected minor a Fourier
   Chebotarev minor or MSRD/LRS minor;
3. a divisor or p-adic dominance theorem for this specific skew-Schur value.
```

Without such input, Toeplitz language only repackages the same
full-support noncancellation theorem recorded in:

```text
p24/trace_frame_weighted_fourier_expansion.md
p24/trace_frame_translate_minor_form.md
p24/trace_frame_toeplitz_support_boundary.md
p24/trace_frame_lead_local_unit_criterion.md
p24/subagent_toeplitz_schur_synthesis.md
```
