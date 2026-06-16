# Trace-GCD Full Gaussian DFT / RS-Tail Target

Date: 2026-06-06

## Point

The square fixed-orbit coinvariant determinant

```text
Phi_full : R^4 + C_tail -> E/(tau_R - 1)E
```

can be stated in a more explicit phase basis.  This does not create a new
payload; it gives a sharper producer theorem for the same `Xi_O0` p-unit.

For p24:

```text
R = F_p(mu_211),       [R:F_p] = 35
L = F_p(mu_157),       [L:F_p] = 156
K = F_p(mu_35),        [K:F_p] = 4
K subset L
```

Choose the type-6 Gaussian normal basis

```text
eta_i = tau_R^i(eta_0),        0 <= i < 35,
```

of `R/F_p`.  For the representative row, define coefficient sequences

```text
C_{i,j} = Tr_{E/L}(eta_i * S_j),        j in {2,3,5,6,1}.
```

The fixed `140+16` determinant is the rank of the `156` elements

```text
C_{i,j},     j in {2,3,5,6}, 0 <= i < 35,
C_{i,1},     0 <= i < 16.
```

## DFT Plus RS-Tail Form

After faithful scalar extension to `K`, the four full right blocks can be
diagonalized by the length-35 DFT.  For `omega in K` primitive of order `35`,
set

```text
D_{a,j} = sum_{i=0}^{34} C_{i,j} tensor omega^(-a*i),
0 <= a < 35,       j in {2,3,5,6,1}.
```

The prefix source becomes the independent frequency variables

```text
x_{a,j},       a in Z/35Z, j in {2,3,5,6}.
```

The tail source is not a full frequency block.  A tail vector

```text
z_0,...,z_15
```

contributes, in frequency variables, the degree-`<16` Reed-Solomon constraint

```text
Z(a) = sum_{s=0}^{15} z_s * omega^(a*s).
```

Equivalently, up to the p-unit scalar `35`, the full bad relation becomes

```text
sum_{a,j in prefix} x_{a,j} D_{a,j}
  + sum_a Z(a) D_{a,1} = 0
```

in `L tensor_{F_p} K`, with `Z` restricted to degree `<16`.

Thus the fixed p-unit theorem is equivalently:

```text
the only solution is x_{a,j}=0 and Z=0.
```

This is the honest group-ring boundary: the prefix is a free
`K[Z/35Z]`-diagonalized module, but the selected tail is a 16-dimensional
Reed-Solomon subspace, not a `K[Z/35Z]`-stable summand.

## Component Form

Since `K subset L`,

```text
L tensor_{F_p} K ~= L x L x L x L.
```

The four components correspond to `omega -> omega^(p^r)`,
`r=0,1,2,3`.  The fixed theorem is therefore a semilinear
kernel-transversality statement across four component equations:

```text
sum_a (sum_j x_{a,j}^{(r)} D_{a,j}^{(r)}
       + Z^{(r)}(omega^(p^r a)) D_{a,1}^{(r)}) = 0,
r=0,1,2,3.
```

This imports a precise CS object: the tail coefficients form an
`[35,16]` Reed-Solomon code across right frequencies.  What remains
arithmetic is proving that this RS-constrained subspace has trivial
intersection with the semilinear prefix kernel for the actual CM periods.

## Checks

The finite linear algebra is checked by:

```text
p24/trace_gcd_full_gaussian_rs_tail_toy.py
p24/trace_gcd_actual_cm_gaussian_rs_tail_audit.py
```

The toy checks faithful `K`-scalar extension, DFT rank preservation, and the
inverse-DFT reconstruction of truncated tail columns from the full tail
spectrum.  The actual-CM audit checks the same identity on the small rows used
for the square coinvariant bridge, including the real nontrivial-prefix
singular control:

```text
D=-15791, q=40127, m=65, pair=(5,13), shape 4 = 3 + 1.
```

Current audit signature:

```text
rank_mismatches=0
tail_reconstruction_failures=0
full_rank_rows=6/10
singular_control_rows=4/10
actual_prefix_plus_tail_rows=4/10
```

## Boundary

This target does not prove p24 by itself.  It rules out an overly clean
`F_p[C_35]` Smith-normal-form shortcut for the full determinant: the tail
truncation is essential.  The next arithmetic theorem can now be stated as a
phase-aware RS-tail nonintersection:

```text
No nonzero prefix frequency vector plus degree-<16 tail polynomial vanishes
in L tensor K for the p24 mixed CM coefficient sequences C_{i,j}.
```

The same theorem can now be descended by Hilbert 90 to the fixed semilinear
relation map

```text
Psi_RS : F_p^28 + K^28 + F_p^16 -> L,
28 + 4*28 + 16 = 156.
```

The proof-facing statement is:

```text
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
p24/trace_gcd_actual_cm_rs_tail_semilinear_core_audit.py
```

For the nonzero orbit, the matching object remains the skew-cyclic reduced
norm/block-cycle determinant from:

```text
p24/trace_gcd_crossed_coinvariant_norm_target.md
```
