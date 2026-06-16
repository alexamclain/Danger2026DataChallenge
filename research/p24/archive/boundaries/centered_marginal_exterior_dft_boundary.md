# Centered Marginal Exterior-DFT Boundary

Date: 2026-06-05

This note records the exact character-module expansion of the live
right-translation determinant and why it does not currently give a compressed
certificate by itself.

## Exterior Formula

Let

```text
P_b in F_q^d,      b mod r,
```

be centered marginal point columns, with the right-window determinant

```text
F(t) = det(P_{t+1}-P_t, ..., P_{t+d}-P_t).
```

After adjoining a primitive `r`th root of unity `zeta`, write

```text
P_b = sum_s Q_s zeta^(s*b).
```

The constant term cancels in the differences, and Cauchy-Binet gives

```text
F(t) =
  sum_{S subset {1,...,r-1}, |S|=d}
    det(Q_s)_{s in S}
    det(zeta^(s*i)-1)_{s in S, 1<=i<=d}
    zeta^(t * sum_{s in S} s).
```

Thus the cyclic resultant and the seven p24 orbit products can be lifted into
an exterior right-character polynomial.  Since `F(t)` is base-valued, the
Fourier coefficients satisfy the expected covariance:

```text
A_{q*k} = A_k^q.
```

This is the precise algebraic place where CS/exterior-algebra and
character-module language attaches to the centered affine-arc theorem.

## Audit

Added:

```text
p24/centered_marginal_exterior_dft_audit.py
```

Pinned small actual-CM rows:

```text
D=-6719, q=6863, pair=(3,7):
  subset_count=15
  nonzero_term_count=15
  coefficient_support_size=7/7
  coefficient_frobenius_failures=0
  reconstruction_failures=0
  window_zero_count=0.

D=-13319, q=13463, pair=(4,7):
  subset_count=20
  nonzero_term_count=20
  coefficient_support_size=7/7
  coefficient_frobenius_failures=0
  reconstruction_failures=0
  window_zero_count=0.

D=-10919, q=11243, pair=(3,13):
  subset_count=66
  nonzero_term_count=66
  coefficient_support_size=13/13
  coefficient_frobenius_failures=0
  reconstruction_failures=0
  window_zero_count=0.
```

So the formula is verified exactly, but the tested CM rows are fully dense:
every subset term was nonzero, and every right frequency occurred.

## p24 Consequence

For p24,

```text
d = 156,   r = 211,
```

so the exterior sum has

```text
binom(210,156) = binom(210,54)
               = 613595546695465706377614485483210517178279541807280
               ~= 10^50.79
```

terms before using additional arithmetic structure.

Therefore the right-character exterior expansion is not itself an
asymptotic speedup.  It gives a rigorous theorem language:

```text
prove the exterior character polynomial's seven right Frobenius orbit
products are p-units.
```

But the small-CM audits rule out the easy sparse-support explanation:

```text
the component-character-module expansion is visibly sparse or low-orbit.
```

The remaining live route must add genuine CM/class-field input, such as an
embedded odd class-character trace identity, a Moore/subspace-polynomial
p-unit norm, or a divisor/local p-unit formula for the orbit products.
