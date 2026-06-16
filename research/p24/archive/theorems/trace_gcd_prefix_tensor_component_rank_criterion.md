# Trace-GCD Prefix Tensor-Component Rank Criterion

Date: 2026-06-06

## Point

The safe Gaussian DFT target lives in a product algebra.  For p24:

```text
L = F_p(mu_157) = F_{p^156},
K = F_p(mu_35)  = F_{p^4},
K subset L,
L tensor_{F_p} K ~= L x L x L x L.
```

The four components correspond to the four embeddings

```text
K -> L,    omega |-> omega^(p^r),    r=0,1,2,3.
```

Thus a vector

```text
v in L tensor K
```

has components

```text
v^(0), v^(1), v^(2), v^(3) in L.
```

For a family `v_t`, a `K`-linear relation

```text
sum_t c_t v_t = 0,        c_t in K,
```

is equivalent to the four component equations

```text
sum_t c_t^(p^r) v_t^(r) = 0,      r=0,1,2,3.
```

Equivalently, after untwisting the coefficient Frobenius, the global kernel is
the intersection of four Frobenius-twisted component kernels.  Therefore:

```text
rank_K{v_t in L tensor K} = 140
```

if and only if those four component kernels intersect trivially.

## p24 Gaussian DFT Components

For the Gaussian DFT family

```text
D_{a,j} = sum_i C_{i,j} tensor omega^(-a*i),
```

the `r`th component is the collapsed DFT at the Frobenius-shifted frequency:

```text
D_{a,j}^{(r)} = sum_i C_{i,j} * omega^(-a*i*p^r).
```

Here

```text
p mod 35 = 22,
ord_35(p) = 4.
```

The multiplication-by-`p` orbits on `Z/35Z` are:

```text
fixed:
  [0], [5], [10], [15], [20], [25], [30]

length 4:
  [1,22,29,8], [2,9,23,16], [3,31,17,24],
  [4,18,11,32], [6,27,34,13], [7,14,28,21],
  [12,19,33,26]
```

So each tensor component sees a Frobenius permutation of the 35 right-cycle
frequencies.

## Necessary And Sufficient Shape

As a `K`-vector space:

```text
dim_K(L tensor K) = 156,
dim_K(each component L) = 39,
source dimension = 4*35 = 140.
```

Each component matrix has rank at most `39`.  Hence component ranks alone
cannot prove the prefix theorem; they only give the necessary bound

```text
rank_0 + rank_1 + rank_2 + rank_3 >= 140.
```

The actual theorem is the kernel-transversality statement:

```text
ker(M_0) cap Frob^{-1}ker(M_1)
       cap Frob^{-2}ker(M_2)
       cap Frob^{-3}ker(M_3)
  = {0},
```

where `M_r` is the `r`th component matrix of the scalar-extended Gaussian DFT
prefix map.

This is now the safest diagonalized theorem surface:

```text
four 39-dimensional component images in L, with transverse twisted kernels.
```

It is equivalent to the original prefix Fitting unit, but it avoids the false
shortcuts:

```text
1. collapsed in-field DFT rank;
2. frequency-by-frequency division by target-algebra units;
3. checking component ranks without kernel alignment.
```

## Cheap Gate

The finite warning is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
p24/trace_gcd_prefix_tensor_component_rank_toy.py
```

It constructs two product-algebra maps with the same component rank profile
`[1,1]`; one has full global rank and the other does not.  The difference is
exactly the intersection of component kernels.

The component Frobenius bookkeeping is recorded in:

```text
p24/trace_gcd_prefix_component_frobenius_bookkeeping.md
p24/trace_gcd_prefix_component_frobenius_toy.py
```

There the `r`th component is written as the first collapsed frequency table
with frequency multiplied by `p^r mod 35`, and the coefficients conjugated by
the same Frobenius power.

The same condition can be repackaged as a semilinear invariant-core theorem
for the first component kernel:

```text
p24/trace_gcd_prefix_semilinear_core_criterion.md
p24/trace_gcd_prefix_semilinear_core_toy.py
```

If `C = ker(M_0)` and

```text
(T x)_{b,j} = x_{p^{-1}b,j}^p,
```

then the prefix theorem is exactly:

```text
{x : T^r x in C for r=0,1,2,3} = {0}.
```

This emphasizes the real obstruction: the first component kernel is large,
but it should contain no nonzero semilinear `T`-stable core.
