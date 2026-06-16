# Tensor Factor CRT Marginal Rank

This note extracts the exact linear algebra hidden inside the Fourier form of
the top-coefficient theorem.

## Setup

Let `E` be a field whose characteristic does not divide `c`, and suppose
`E` contains a primitive `c`-th root `zeta_c`.  Let `V` be an `E`-vector
space and let

```text
A : Z/mZ -> V
```

be any vector-valued quotient sequence.  For a CRT component `c | m`, define
the marginals

```text
M_a = sum_{r == a mod c} A(r),     a in Z/cZ.
```

The component DFT values are

```text
D_t = sum_{a mod c} zeta_c^(t*a) M_a,     0 <= t < c.
```

For the original length-`m` transform this is exactly

```text
D_t = hat A(t*m/c).
```

## Rank Lemma

The full `c x c` DFT matrix over `E` is invertible, so:

```text
rank_E {D_0, ..., D_{c-1}}
  = rank_E {M_0, ..., M_{c-1}}.
```

The nontrivial DFT coefficient rows `t=1,...,c-1` form a basis of the
hyperplane

```text
sum_a lambda_a = 0.
```

Therefore:

```text
rank_E {D_1, ..., D_{c-1}}
  = rank_E {M_a - M_0 : 1 <= a < c}.
```

So component-normality is equivalent to affine independence of the CRT
marginals.  Including the constant frequency asks for their ordinary linear
span:

```text
rank_E {D_0, D_1, ..., D_{c-1}}
  = rank_E {M_0, ..., M_{c-1}}.
```

Equivalently, if `a_rank` is the affine rank of the marginals, then:

```text
rank_E {D_0, D_1, ..., D_{c-1}} = a_rank + epsilon,
```

where `epsilon=1` exactly when `0` is not in the affine hull of
`{M_0,...,M_{c-1}}`.

This is a formal statement; no CM input appears until one tries to prove the
required marginal ranks.

## p24 Specialization

For the p24 tensor factor, take

```text
E = F_p(mu_m),       m = 2*157*211,
C = F_{E^179},
V_k = C^k,
A_k(r) = Top_k(J_r(theta)) in V_k.
```

For each component `c in {2,157,211}`, write

```text
M_{c,a}^{(k)} = sum_{r == a mod c} A_k(r),
U_c^{(k)} = span_E {M_{c,a}^{(k)} - M_{c,0}^{(k)} : 1 <= a < c}.
```

Then the split top-coefficient target becomes:

```text
Top_1 on constant+2+157:
  dim_E span( D_0^(1), U_2^(1), U_157^(1) ) = 158.

Top_2 on 211:
  dim_E U_211^(2) = 210.

Top_3 on the full axis:
  dim_E span( D_0^(3), U_2^(3), U_157^(3), U_211^(3) ) = 368.
```

The second line says the 211 marginals in `C^2` are affinely independent.
The first and third lines are directness statements among the total vector
and the affine-difference spaces of the indicated CRT components.

This removes the DFT roots of unity from the hard theorem.  The missing
arithmetic input is now a marginal-affine-rank/directness theorem for the
top-coefficient packet sequence.

## Small Audit

The audit script is:

```text
p24/tensor_factor_crt_marginal_rank_audit.py
```

Pinned command:

```text
PYTHONPATH=p24 python3 p24/tensor_factor_crt_marginal_rank_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 1 --max-rows 8
```

reported:

```text
c=4: marg_span=3/3, marg_affine=3/3,
     dft_nontriv=3, dft_const_plus=3, matches=(1,1)
c=3: marg_span=3/3, marg_affine=2/2,
     dft_nontriv=2, dft_const_plus=3, matches=(1,1)
rank_identity_mismatches=0
```

With two windows:

```text
c=4: marg_span=4/4, marg_affine=3/3,
     dft_nontriv=3, dft_const_plus=4, matches=(1,1)
c=3: marg_span=3/3, marg_affine=2/2,
     dft_nontriv=2, dft_const_plus=3, matches=(1,1)
rank_identity_mismatches=0
```

The capacity transition for the `c=4` constant-plus block is exactly the
marginal-span transition.

The same audit now reports combined marginal-difference targets.  With one
window:

```text
combined=4                    size=3 rank=3/3
combined=constantplus4        size=4 rank=3/3
combined=3                    size=2 rank=2/2
combined=constantplus3        size=3 rank=3/3
combined=constantplus4plus3   size=6 rank=3/3
```

With two windows:

```text
combined=4                    size=3 rank=3/3
combined=constantplus4        size=4 rank=4/4
combined=3                    size=2 rank=2/2
combined=constantplus3        size=3 rank=3/3
combined=constantplus4plus3   size=6 rank=6/6
```

Thus the full toy axis target fills exactly when the top-window coordinate
capacity reaches the combined marginal dimension.
