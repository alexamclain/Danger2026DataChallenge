# Centered Profile Payload Frontier

Date: 2026-06-06

This note compares the finite verifier surfaces for the centered-profile
mixed-rank route.

## Centered Profile Target

The theorem target is:

```text
rank_Fp C = 156,
```

where `C` is the base-field doubly-centered Hermitian marginal:

```text
C(r,s) = M(r,s) - M(r,0) - M(0,s) + M(0,0),
1 <= r < 157,
1 <= s < 211.
```

Equivalently, the centered right-profile values

```text
G_s^0 in F_p(mu_157)
```

span the full `156`-dimensional left field.

## Payload Surfaces

The base matrix has:

```text
156 * 210 = 32760
```

entries.  An explicit matrix-plus-rank-witness certificate can carry the
matrix together with one `156 x 156` inverse/minor witness:

```text
156*210 + 156*156 = 57096
```

field elements.  This is still much smaller than the selected-chain tower
surface:

```text
57096 < 3107811.
```

If an arithmetic theorem directly proves the selected leading minor is a
p-unit, the finite scalar payload is only:

```text
Delta_C_leading and Delta_C_leading^{-1}: 2 field elements.
```

The right-translation product forms are:

```text
pointwise 211 values plus inverses: 422 field elements;
seven orbit norms plus inverses:    14 field elements.
```

Lean checks these counts in:

```text
p24/lean/CenteredProfilePayloadGate.lean
```

The finite implication from orbit products to the selected rank certificate is
checked in:

```text
p24/lean/CenteredArcProductGate.lean
```

## Why This Route Is Interesting

Unlike the selected-chain route, the centered-profile route does not output a
`j` recovery polynomial.  It is a p-unit route: it proves the mixed Schur rank
correction needed by the factorized/trace-GCD certificate stack.

Its advantage is that the theorem can be stated entirely over the base field:

```text
the actual p24 156 x 210 centered Hermitian marginal has full row rank.
```

The cleanest scalar is:

```text
Delta_C_leading =
  det(C(r,s))_{1 <= r <= 156, 1 <= s <= 156}.
```

The manifest is:

```text
p24/p24_centered_profile_manifest.py
```

and the finite implication is checked by:

```text
p24/lean/CenteredProfileGate.lean
```

## Boundary

The centered-profile theorem remains arithmetic.  Small-row checks and random
rank intuition do not prove selected-prime p-unitness.  Existing boundaries
show:

```text
nonzero relative content does not imply centered-profile full span;
a single normal G_s^0 value does not imply the full profile spans;
generic Cauchy-Binet support does not factor into separate easy p-units.
```

So the productive theorem target is:

```text
prove Delta_C_leading is a p-unit,
or prove a right-translation/orbit product of Delta_C is a p-unit,
or identify Delta_C with a phase-aware Borcherds/Fitting divisor whose
selected p-local intersection vanishes.
```

The probability/CS calibration is now:

```text
p24/centered_marginal_transversality_boundary.md
```

It shows that the plateau obstruction is a complementary Schubert-divisor
avoidance problem in the centered hyperplane
(`156 + 54 = 210`), with random failure probability about `211/p`.  This
explains the small-row/random success pattern but is not a certificate unless
lifted to a class-field p-unit/equidistribution theorem.

The ranked theorem-family synthesis is:

```text
p24/centered_profile_theorem_family_synthesis.md
```

The centered-specific phase-aware p-unit target is:

```text
p24/centered_marginal_phase_borcherds_target.md
p24/lean/CenteredBorcherdsPUnitGate.lean
p24/centered_marginal_full_origin_borcherds_gate.md
p24/lean/CenteredFullOriginBorcherdsGate.lean
```

If a closed phase-aware full-origin product is constructed, the finite payload
can shrink to:

```text
full-origin product scalar plus inverse: 2 field elements.
```

This only counts as an asymptotic speedup if the product is produced by a
closed class-field/Borcherds/Fitting formula; enumerating the full class
torsor would be class-number scale.

This is now the smallest base-field p-unit surface still worth pursuing.
