# Representative Leading P-Unit Certificate

This note records the smallest current finite certificate surface after the
opposite-pair, inversion, and right-unit equivariance reductions.

## Representative Row

Use the representative equivariant deletion row:

```text
deleted O4,
B_prefix={O2,O3,O5,O6},
T_tail=O1,
tail_window=first 16 Lang coordinates of O1.
```

The leading coordinate set has size

```text
4*35 + 16 = 156.
```

Let `L_rep` be the Moore residual product / leading Moore determinant for
these `156` coordinates:

```text
L_rep = B_rep * T_rep.
```

Here:

```text
B_rep != 0  <=>  the four full prefix blocks have rank 140,
T_rep != 0  <=>  the tail adds the missing 16 dimensions.
```

But for the finite certificate itself, the single condition is:

```text
L_rep != 0 mod p.
```

The sharpest CS-theory strengthening currently on the table is recorded in:

```text
p24/msrd_lrs_import_boundary.md
```

If the full 210-coordinate mixed trace-dual code is block-equivalent to an
`[210,156]` LRS/MSRD sum-rank code, its minimum distance would be `55`, while
the bad representative support has size `35+19=54`.  This would imply
`L_rep != 0`.  The missing input is precisely the arithmetic block-equivalence
or an equivalent skew-polynomial p-unit determinant identity.

The finite support-count implication is Lean-checked in:

```text
p24/lean/MSRDSupportGate.lean
```

The weaker support-specific block-subspace design formulation is recorded in:

```text
p24/lang_block_subspace_design_boundary.md
p24/lang_block_subspace_design_audit.py
```

It states exactly the representative `140+16` theorem:

```text
four full right blocks span 4*35 dimensions,
and the selected 16-coordinate tail injects into the quotient.
```

The corresponding finite numerical gate is Lean-checked in:

```text
p24/lean/MixedSubspacePolynomialGate.lean
```

This directly proves the representative leading erasure avoidance.  The
factorization into `B_rep` and `T_rep` remains useful as a proof strategy and
as a verifier implementation detail, but it is not a separate logical
requirement if the verifier is supplied with the leading determinant.

## Residual Product Formula

For an ordered tuple

```text
x_0,...,x_155 in L,
```

let `P_i` be the monic `p`-linearized annihilator of the span of

```text
x_0,...,x_{i-1}.
```

Then the Moore determinant satisfies

```text
det(x_j^(p^i))_{0<=i,j<156}
  = product_{i=0}^{155} P_i(x_i),
```

with the convention that a dependent coordinate contributes the zero residual
`P_i(x_i)=0`.  Therefore nonvanishing of `L_rep` is exactly the statement
that every residual in this ordered update is nonzero.

For the p24 representative row, the ordered tuple splits as:

```text
140 prefix coordinates from O2,O3,O5,O6,
16 tail coordinates from O1.
```

So:

```text
B_rep = product of the first 140 residuals,
T_rep = product of the next 16 residuals,
L_rep = B_rep*T_rep.
```

The finite-field identity and split factorization are checked by:

```text
p24/moore_residual_product_toy.py
```

The small-CM pivot-order miner for this exact leading-window shape is:

```text
p24/lang_pivot_order_miner.py
p24/lang_pivot_order_mining_boundary.md
```

It compares right-orbit orderings and records whether the leading product,
full-block prefix, and tail residual products are nonzero/base-field-valued in
actual-CM rows.

Example outputs:

```text
q=3, degree=8, count=6, prefix_count=4:
  determinant_mismatches=0
  split_mismatches=0
  nonzero_mismatches=0

q=2, degree=7, count=5, prefix_count=3:
  determinant_mismatches=0
  split_mismatches=0
  nonzero_mismatches=0
```

## Equivariant Propagation

The unit `2 mod 211` cycles the six right orbit labels:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

Therefore the unit orbit of the representative row covers all six deletion
rows:

```text
delete O4, tail O1
delete O5, tail O2
delete O6, tail O3
delete O1, tail O4
delete O2, tail O5
delete O3, tail O6.
```

With the full-product-algebra and compatible Lang-coordinate conventions from

```text
p24/right_unit_equivariance_theorem.md
p24/opposite_conjugation_tail_theorem.md
```

nonvanishing of `L_rep` propagates to the leading p-units for all six
deletion rows.

The finite orbit logic is Lean-checked in:

```text
p24/lean/RepresentativeOnePUnitGate.lean
p24/lean/UnitOrbitGate.lean
```

The first file packages the combined one-representative handoff:

```text
representative p-unit
  => all six deletion rows by unit equivariance
  => delete-one separation
  => right support >= 2
  => mixed rank certificate.
```

The downstream finite implications are also checked in:

```text
p24/lean/RepresentativeDualObstructionGate.lean
p24/lean/MixedSubspacePolynomialGate.lean
p24/lean/MixedRightOrbitSupportGate.lean
```

The dual bad-lambda formulation is recorded in:

```text
p24/representative_dual_obstruction_theorem.md
p24/representative_dual_obstruction_toy.py
```

## Current Sharpest Arithmetic Theorem

The p24 certificate is reduced to the selected-prime p-unit theorem:

```text
L_rep is nonzero modulo p = 10^24 + 7.
```

Equivalently:

```text
the representative leading 156-coordinate Moore determinant for the actual
embedded p24 mixed Hermitian periods is a p-unit.
```

This is now the smallest named finite-field object in the current route.  A
proof of this single p-unit theorem, together with the finite equivariance
data, gives the desired mixed Schur rank theorem and hence the sub-sqrt
decomposed certificate surface.

## Boundary

This does not make the arithmetic theorem easier by itself.  It packages the
same selected-prime nonvanishing as one determinant rather than two residual
factors.  The split

```text
L_rep = B_rep*T_rep
```

is still the best visible route for a proof, because it exposes the
`140+16` structure of the determinant.

A separate symmetry boundary is recorded in:

```text
p24/unit_orbit_transversality_boundary.md
```

The right-unit orbit compresses the six deletion-row tests to one
representative p-unit, but cyclic symmetry alone does not prove
transversality.  The remaining arithmetic theorem is still exactly:

```text
L_rep != 0 mod p.
```

The sharper trace-GCD comparison is recorded in:

```text
p24/punit_route_comparison_frontier.md
```

There the representative Moore determinant is further unpacked as a rank-140
prefix theorem plus a selected `16 x 16` tail-on-kernel p-unit.  This is the
current preferred proof-facing form of the same arithmetic input.

The most compressed trace-GCD packaging is now:

```text
p24/lean/TraceGcdOperatorRepresentativeGate.lean
```

It shows that a p-unit for the honest global operator norm

```text
Norm_trace = det(m_f on F[Y]/(Y^211 - 1))
```

together with zero-detection for the actual determinant sequence `Delta(t)`,
implies the selected representative row, then the unit-equivariant six-row
handoff, and finally the mixed rank certificate.  This does not prove the
operator norm is honest or a p-unit; it gives the smallest finite handoff once
that arithmetic theorem is supplied.
