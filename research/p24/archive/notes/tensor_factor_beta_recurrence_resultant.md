# Tensor Factor Beta Recurrence Resultant

This note records the recurrence/resultant form of the marginal beta-product
certificate.

## Formal Surface

For a chosen Plucker coordinate `P` of one marginal exterior product, define:

```text
a_beta = P(Omega_beta),       beta in Z/nZ.
```

If the sequence has a connection polynomial

```text
a_j + c_1 a_{j-1} + ... + c_L a_{j-L} = 0,
```

then its characteristic polynomial is:

```text
chi(T) = T^L + c_1 T^(L-1) + ... + c_L.
```

Because `a_beta` is periodic of period `n`, a useful certificate surface is:

```text
chi(T) | T^n - 1.
```

Then the beta sequence lives in the `L`-dimensional cyclic module

```text
E[T] / (chi),
```

and the origin-stable product

```text
Pi_{P,Omega} = prod_{beta mod n} a_beta
```

is a norm/resultant-type polynomial in the initial state of that module.  If
`L << n`, this would compress the beta product into a much smaller finite
certificate surface.

Equivalently, after adjoining the `n`-th roots of unity, `a_beta` is an
exponential polynomial supported on the roots of `chi`.  The product is:

```text
prod_{z^n=1} A(z) = Res_Z(Z^n - 1, A(Z)),
```

where `A` is the spectral interpolation polynomial of the chosen Plucker
coordinate.  The hard p24 question is whether `A` has support in few
`E`-Frobenius orbits.

## Audit

The audit script is:

```text
p24/tensor_factor_beta_recurrence_audit.py
```

Pinned projected component row:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_beta_recurrence_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1 \
  --target 4 --without-constant
```

reported:

```text
distinct_values=13
zero_count=0
product=(5606, 6427)

order=7
order_over_n=0.538462
characteristic_divides_T^n_minus_1=1
quotient_degree_if_divides=6
recurrence_failures_on_doubled_sequence=0
generation_mismatches_on_doubled_sequence=0
periodic_closure_failures=0
```

The `constant+3` determinant has the same order-7 characteristic polynomial.
The full two-window determinant has order `1`, but that is a full-space
artifact: its coordinate count equals the whole tensor-factor degree.

The CM-vs-random support audit is recorded in:

```text
p24/tensor_factor_marginal_random_support_audit.py
p24/tensor_factor_marginal_random_support.md
```

On the projected `D=-10919` component determinants, random tensor-factor data
has the same recurrence order:

```text
random_order_hist={7: 40}.
```

Thus the toy order-7 recurrence is generic for the determinant shape, not a
visible CM support-collapse phenomenon.

## p24 Consequence

For p24, `E`-Frobenius on the `n`-th root coordinate has orbit size:

```text
5549.
```

So a recurrence/resultant compression is meaningful only if a chosen Plucker
coordinate uses a small number of these degree-5549 spectral orbits.  The
support audit:

```text
p24/tensor_factor_plucker_spectral_support.md
p24/tensor_factor_beta_support_boundary.md
```

is negative for generic large exterior coordinates:

```text
O+O covers 557 of 560 nonzero degree-5549 orbit factors,
O+O+O = Z/nZ.
```

Thus recurrence/resultant packaging is a valid finite certificate surface, but
not an automatic asymptotic speedup.  The proof would need a CM-specific
support collapse or a p-unit theorem for the full-support resultant.
