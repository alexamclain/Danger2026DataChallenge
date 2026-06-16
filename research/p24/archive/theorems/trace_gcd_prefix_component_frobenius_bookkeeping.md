# Trace-GCD Prefix Component Frobenius Bookkeeping

Date: 2026-06-06

## Point

The four tensor components in

```text
L tensor_{F_p} K,       K = F_p(mu_35),
```

are not unrelated.  They are Frobenius-shifted copies of the same collapsed
Gaussian DFT frequency table.

Let

```text
omega in K
```

be a primitive `35`th root.  For the scalar-extended Gaussian DFT columns

```text
D_{a,j} = sum_i C_{i,j} tensor omega^(-a*i),
```

write the first component as

```text
V_{a,j} = sum_i C_{i,j} * omega^(-a*i) in L.
```

The `r`th component, corresponding to the embedding

```text
omega |-> omega^(p^r),      r = 0,1,2,3,
```

is:

```text
D_{a,j}^{(r)} = V_{p^r a,j}.
```

Thus a `K`-linear relation with coefficients `x_{a,j} in K` is equivalent to
the four equations in `L`:

```text
sum_{a,j} x_{a,j}^{p^r} V_{p^r a,j} = 0,
r = 0,1,2,3.
```

After reindexing:

```text
sum_{b,j} x_{p^{-r} b,j}^{p^r} V_{b,j} = 0.
```

This is the exact twisted-kernel intersection condition.

Equivalently, define

```text
(T x)_{b,j} = x_{p^{-1} b,j}^p.
```

Then the `r`th component equation is

```text
M_0(T^r x) = 0,
```

where `M_0` is the first collapsed component map
`x |-> sum_{a,j} x_{a,j} V_{a,j}`.  Thus the global relation space is the
largest `T`-stable core contained in `ker(M_0)`.

## p24 Frequency Orbits

For p24:

```text
p mod 35 = 22,
ord_35(p) = 4.
```

The fixed frequencies are:

```text
0, 5, 10, 15, 20, 25, 30.
```

The seven length-4 frequency orbits are:

```text
[1,22,29,8],
[2,9,23,16],
[3,31,17,24],
[4,18,11,32],
[6,27,34,13],
[7,14,28,21],
[12,19,33,26].
```

The length-4 orbits explain how the four tensor components rotate the
Gaussian frequencies.  They do **not** by themselves make the prefix matrix
block diagonal by frequency orbit, because all component equations still land
in the same `L` component and may mix all `V_{a,j}`.

## Current Safe Theorem

The prefix theorem is:

```text
for x_{a,j} in K,
if
  sum_{a,j} x_{a,j}^{p^r} V_{p^r a,j} = 0 for r=0,1,2,3,
then
  x_{a,j}=0 for every a,j.
```

Equivalently, the four Frobenius-rotated component kernels intersect
trivially.

This is still exactly the coinvariant Fitting theorem, but it is now stated
in terms of the first collapsed frequency table plus semilinear coefficient
rotation.

## Cheap Gate

The bookkeeping identity is checked by:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
p24/trace_gcd_prefix_component_frobenius_toy.py
```

The equivalent semilinear-core criterion is recorded in:

```text
p24/trace_gcd_prefix_semilinear_core_criterion.md
p24/trace_gcd_prefix_semilinear_core_toy.py
```

The toy uses a length-3 DFT over `F_16` with `K=F_4` and verifies:

```text
D_a^(r) = V_{q^r a},
component relation = reindexed conjugate-coefficient relation.
```
