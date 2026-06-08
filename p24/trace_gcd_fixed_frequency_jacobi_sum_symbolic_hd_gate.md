# Symbolic Hasse-Davenport Gate

Date: 2026-06-07

## Point

The finite-field Jacobi anchor correction is not only an empirical finite
field pattern.  The product-formula identities follow from symbolic
character/Gauss-sum accounting.

This gate checks the residue conditions for the reduced packet:

```text
Jdagger(1,1)=1
Jdagger(A,B)=J(A,B) otherwise.
```

## Symbolic Row-Ratio Cancellation

For fixed right row `r`, write:

```text
A_k = chi^(u*t(r,k))
B_k = chi^(v*t(r,k)).
```

Since `u` is right-trivial, `B_k` and `A_kB_k` have the same right component.
Since `v` and `u+v` have nonzero C-components, each runs through the same
size-`c` C-coset as `k` varies.

At `k=0`, `A_0=1`, so:

```text
B_0 = A_0 B_0.
```

Removing the common `k=0` element leaves identical punctured C-cosets.  Thus
in:

```text
prod_{k != 0} G(A_k)G(B_k)/G(A_kB_k)
```

the `B_k` and `A_kB_k` Gauss factors cancel, leaving:

```text
prod_{k != 0} G(A_k),
```

which is independent of the right row `r` and of the right-mixed partner `v`.

## Symbolic Pair-Product Constants

For `k != 0`, admissibility makes `A`, `B`, and `AB` all nontrivial, so:

```text
J(A,B)J(A^-1,B^-1)=q.
```

On the C-zero fiber, `A=1`.  For `r != 0`, `B` is nontrivial and
`J(1,B)=-1`, giving pair-product `1`.  At `r=0`, the reduced anchor
`Jdagger(1,1)=1` also gives pair-product `1`.

## Coverage

The gate checks all admissible right-mixed pairs for:

```text
c = 5, 11, 13, 17, 19, 179.
```

For p24, `c=179`, and the pair count is:

```text
6*(179-1)*(179-2) = 189036.
```

Observed:

```text
symbolic_pair_count_rows=6/6
symbolic_pair_product_rows=6/6
symbolic_row_ratio_rows=6/6
symbolic_reduced_anchor_rows=6/6
symbolic_producer_rows=6/6
p24_symbolic_right_mixed_pairs=189036
```

No finite-field sums and no p24 class-set enumeration are used.

## Consequence

The p24 missing theorem is not the finite Jacobi/Hasse-Davenport algebra
anymore.  That algebra is isolated.

The remaining arithmetic input is:

```text
construct the selected trace-GCD packet after Tr_{B/C} as the p-integral
specialization/log/divisor of the reduced Jacobi/CM-Lang packet.
```

Equivalently, find the CM/Lang unit whose single degenerate anchor is the
p24 analogue of `J(1,1)/(q-2)`.
