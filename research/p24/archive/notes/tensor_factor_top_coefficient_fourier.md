# Tensor Factor Top-Coefficient Fourier Form

This note records the frequency-side form of the top-coefficient theorem.

## Fourier Identity

For quotient fibers `J_r` and K-character resolvents

```text
R_s = sum_r zeta^(s*r) J_r,
```

linearity gives:

```text
Top_k(R_s) = DFT_s( r |-> Top_k(J_r) ).
```

The audit script is:

```text
p24/tensor_factor_top_coefficient_fourier_audit.py
```

It verifies this identity directly in small tensor-factor rows.

## Small Row

Pinned command:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_top_coefficient_fourier_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1
```

reported:

```text
dft_failures=0
full_frequency_support_counts=[12,12,12]
axis_frequency_support_counts=[6,6,6]
```

With two windows:

```text
dft_failures=0
full_frequency_support_counts=[12,12,12,12,12,12]
axis rank=6
```

So the top-coefficient map is exactly the DFT of a quotient sequence, but its
coordinate functions have dense frequency support.  There is no visible
coordinate-isolated Vandermonde or block-diagonal factorization in the toy
row.

## Theorem Form

The p24 theorem can be phrased as a vector-valued Fourier anti-annihilator:

```text
A_k(r) = Top_k(J_r(theta)).
```

Then:

```text
Top_k(R_s) = hat(A_k)(s).
```

The target is that the selected axis frequencies give independent values of
`hat(A_k)` in the appropriate component windows:

```text
Top_1 on constant+2+157,
Top_2 on 211,
Top_3 on full axis.
```

Equivalently, no nonzero axis-spectrum function annihilates the vector-valued
quotient sequence `A_k`.

This is cleaner than a raw determinant, but it remains an arithmetic
anti-annihilator theorem.  The dense-support audit rules out the easiest
DFT/Vandermonde shortcut.

## CRT Marginals

For a component `c | m` and frequency `s=t*m/c`, the DFT factors through the
CRT marginal:

```text
Top_k(R_{t*m/c})
  = sum_{a mod c} zeta_c^(t*a)
      ( sum_{r == a mod c} Top_k(J_r) ).
```

Thus the structured theorem is:

```text
partial DFT on the CRT marginals of A_k has full rank on the selected
component frequency blocks.
```

The DFT part is formal.  More precisely, the nontrivial component block has
rank equal to the affine rank of the marginals

```text
M_a = sum_{r == a mod c} A_k(r),
```

and the constant-plus-component block has rank equal to
`rank{M_0,...,M_{c-1}}`.  This is recorded and tested in:

```text
p24/tensor_factor_crt_marginal_rank_audit.py
p24/tensor_factor_crt_marginal_rank.md
```

The hard arithmetic input is that these CRT-marginal packet vectors have the
required affine ranks and cross-component directness.  Nonzero entries alone
are not enough, because the small-row coefficient profile shows dense mixing
between the H-packet arithmetic and K-residue coordinate.
