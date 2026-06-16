# Trace-GCD Prefix Gaussian DFT Scalar-Extension Boundary

Date: 2026-06-06

## Point

The type-6 Gaussian normal basis makes the right prefix determinant
convolutional, but the right-cycle DFT must be used in the scalar-extended
tensor product, not by collapsing extension coefficients into `L`.

For p24:

```text
ord_35(p) = 4,
K = F_p(mu_35) = F_{p^4},
K subset L = F_p(mu_157) = F_{p^156}.
```

Let

```text
C_{i,j} = Tr_{E/L}(eta_i * S_j) in L,
S_j = H_{157,211}(1,v_j),
j in {2,3,5,6}.
```

The prefix theorem is:

```text
{C_{i,j}} is F_p-independent in L.
```

Equivalently, after faithful scalar extension:

```text
{C_{i,j} tensor 1} is K-independent in L tensor_{F_p} K.
```

Only here is it safe to apply the length-35 DFT.  For a primitive `35`th
root `omega in K`, define

```text
D_{a,j} = sum_i C_{i,j} tensor omega^(-a*i),
0 <= a < 35.
```

The DFT matrix is invertible over `K`, so:

```text
{C_{i,j} tensor 1} K-independent
  <=>
{D_{a,j}} K-independent in L tensor K.
```

## Tensor Product Formula

Let

```text
G_a = sum_i eta_i tensor omega^(-a*i),
U_{a,j} = sum_h tau_R^h(S_j) tensor omega^(a*h).
```

Then in `E tensor K`:

```text
D_{a,j} = G_a * U_{a,j}.
```

The two factors have opposite `tau_R` eigencharacters, so their product lies
in the fixed algebra:

```text
(E tensor K)^{tau_R} = L tensor K.
```

This is the safe phase-aware DFT form of the prefix determinant.

The Gaussian factor `G_a` is a unit in the scalar-extended target algebra,
but that does not let us divide the full `140`-column rank problem by the
different `G_a` values frequency-by-frequency.  Target-algebra unit scaling
is not base-rank-safe.  This boundary is recorded in:

```text
p24/trace_gcd_prefix_gaussian_unit_factor_boundary.md
p24/trace_gcd_prefix_unit_scaling_pitfall_toy.py
```

## What Is Not Safe

Because `K subset L`, it is tempting to multiply the DFT coefficients inside
`L` and use the field elements

```text
sum_i omega^(-a*i) C_{i,j} in L.
```

That collapse is not a faithful rank-preserving operation from
`L tensor K` to `L`.  It can change the `F_p`-rank of a family.  Therefore a
proof cannot argue:

```text
Gaussian DFT values look independent in L
  => original prefix coefficients are independent over F_p.
```

The correct implication must stay in `L tensor K`, or descend by a proven
norm/Fitting determinant identity.

Because `K subset L`, this tensor product decomposes into four components.
The corresponding global rank condition is an intersection-of-kernels
condition across those four components, not merely a collection of component
rank checks.  This is recorded in:

```text
p24/trace_gcd_prefix_tensor_component_rank_criterion.md
p24/trace_gcd_prefix_tensor_component_rank_toy.py
```

The four components are Frobenius-shifted copies of the first collapsed
frequency table.  The exact coefficient conjugation and frequency
permutation are recorded in:

```text
p24/trace_gcd_prefix_component_frobenius_bookkeeping.md
```

## Missing Arithmetic Theorem

The sharper safe theorem is:

```text
the 140 tensors
  D_{a,j} = G_a * sum_h tau_R^h(H_{157,211}(1,v_j)) tensor omega^(a*h)
are K-independent in L tensor_{F_p} K.
```

Equivalently, the determinant/Fitting ideal of this scalar-extended
Gaussian-DFT matrix is a unit.  Since scalar extension is faithful, this is
exactly the original prefix Fitting theorem, but in a diagonalized right-cycle
coordinate system.

## Cheap Gate

The pitfall and the safe tensor interpretation are checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_prefix_gaussian_dft_boundary_toy.py
```

The toy shows that a DFT over `F_4/F_2` can raise the apparent collapsed
`F_2`-rank from `1` to `2`, while the correct tensor-product rank remains
`1` before and after the DFT.
