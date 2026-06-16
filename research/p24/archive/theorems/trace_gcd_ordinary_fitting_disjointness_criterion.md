# Trace-GCD Ordinary Fitting Disjointness Criterion

Date: 2026-06-06

This note states the p-local theorem in the form that would finish the
trace-GCD orbit-norm route once the phase-aware determinant section is
constructed.

## Local Setup

Let `O_p` be the localization of the phase/class-field coefficient ring at
one of the two ordinary primes above

```text
p = 10^24 + 7.
```

The p24 local invariant audit proves:

```text
p is prime;
p is split and unramified in K=Q(sqrt(D_K));
sqrt(D_K) = +/- t/2 mod p gives the two explicit orientations;
p is prime to 2, 157, 211, 66254, 3107441, and h;
right Frobenius orbits on Z/211Z are {0} plus six length-35 orbits.
```

Thus all Lang/Fourier/level denominators in the current determinant-line
model are p-units.  The remaining question is not integrality; it is whether
the determinant section vanishes at the selected ordinary reduction.

## Criterion

For a right Frobenius orbit `O`, let

```text
B_O : direct sum transported prefix kernels
      -> direct sum selected tail windows
```

be the p-integral block-cycle/Fitting operator attached to the actual p24
trace-GCD maps.  Let

```text
Xi_O = det(B_O)
```

as a determinant-line section.  Independent p-integral basis choices scale
`Xi_O` by p-units, so the statement

```text
Xi_O in O_p^*
```

is intrinsic.

The ordinary Fitting disjointness criterion is:

```text
Xi_O is a p-unit
  <=> reduction(B_O) is an isomorphism
  <=> coker(B_O) has unit zeroth Fitting ideal
  <=> the selected p24 ordinary CM point has zero local intersection
      with the pulled-back orbit Schubert/Chow divisor D_O.
```

The implication needed by the finite certificate is the forward direction:

```text
Xi_O in O_p^*
  => no translated Schubert bad event on O
  => every Delta(t), t in O, is nonzero mod p.
```

The existing Lean gates consume this as:

```text
p24/lean/TraceGcdBlockCycleGate.lean
p24/lean/TraceGcdChowNormGate.lean
p24/lean/TraceGcdChowBorcherdsPUnitGate.lean
p24/lean/DeterminantLineUnitScaleGate.lean
```

The criterion itself is now isolated in:

```text
p24/lean/TraceGcdOrdinaryFittingCriterionGate.lean
```

This Lean gate records the finite handoff:

```text
zero local intersection
  or reduced block map isomorphism
  or unit zeroth Fitting ideal of the cokernel
=> Fitting determinant p-unit
=> no translated trace-GCD Schubert bad event.
```

The residual/Moore version of the same determinant-line section is isolated
in:

```text
p24/trace_gcd_residual_moore_chow_section.md
```

For the p24 representative it decomposes `Xi_O` into the 140-prefix
Moore-Wronskian and the 16-dimensional quotient-tail Moore-Wronskian obtained
from the prefix annihilator.  This gives a concrete way to instantiate
`B_O` without choosing a row-reduced kernel basis; basis choices still change
the determinant only by p-units.

## What Must Be Proved Arithmetically

The missing theorem is now exactly:

```text
For every one of the seven right Frobenius orbits O, the actual p24
phase-aware block-cycle determinant-line section Xi_O has

  v_p(Xi_O(x_p24)) = 0

at the selected ordinary CM orientation.
```

This is the uncompressed local form of the criterion.  The current best
p24 route does not intend to prove all seven orbit instances independently.
Instead it separates the arithmetic proof into:

```text
1. diamond/right-unit determinant-line equivariance up to p-unit scale;
2. the fixed-orbit p-unit Xi_O0 in O_p^*;
3. one nonzero representative p-unit Xi_O1 in O_p^*.
```

The criterion in this note applies orbit-by-orbit after those hypotheses are
transported.  Thus the local Fitting theorem remains a seven-orbit
zero-detection statement, while the arithmetic producer has only two
independent p-unit nonvanishing targets.

There are two viable ways to prove it.

### Direct Fitting Unit

Construct `B_O` from embedded non-genus `157/211` relative phase data, not
from the class set, and prove its reduction is invertible over the selected
residue field.

This would be a direct local-unit theorem:

```text
coker(B_O) tensor O_p/p = 0.
```

### Phase-Aware Product Formula

Construct a p-integral class-field/Borcherds/Fitting section `Psi_O` with

```text
div(Psi_O) = pulled-back D_O + terms away from the selected p24 prime,
Psi_O = p-unit * Xi_O near x_p24,
v_p(Psi_O(x_p24)) = 0.
```

Then the same criterion gives `Xi_O in O_p^*`.

## Evidence Already Checked

The criterion is consistent with all current bounded checks:

```text
p24/trace_gcd_p24_local_invariants.py
  verifies split ordinary p-local data and prime-to-level denominators.

p24/fourier_head_minor_unit_audit.py
  verifies fixed Lang-head Fourier minors are p-units.

p24/block_cycle_determinant_line_invariance_toy.py
  verifies block-cycle determinant-line zero status is basis-independent.

p24/trace_gcd_actual_cm_norm_triangle_audit.py
  verifies on a pinned actual-CM row that scalar orbit products,
  block-cycle determinants, and split-interpolant norms are the same object.

p24/trace_gcd_actual_cm_orbit_norm_miner.py
  verifies on the same pinned actual-CM row that all six positive-size orbit
  Fitting norms are nonzero.

p24/trace_gcd_phase_unit_dictionary_boundary.md
  records that the obvious right-binomial and low-Heegner phase-unit
  dictionary does not explain those small-row determinant values except by
  full-rank interpolation.

p24/trace_gcd_principal_cyclotomic_split_audit.py
  verifies that Hilbert/ring-class Frobenius at p is trivial while
  cyclotomic Frobenius has orders 156 and 35 on the phase coordinates.
```

The pinned actual-CM triangle also reports:

```text
naive_base_polynomial_possible=0.
```

So the criterion must remain in the crossed-product/Fitting determinant-line
language.  Ordinary base-polynomial interpolation is not an honest p24
producer theorem.

## Boundary

This criterion does not itself prove the certificate.  It identifies exactly
what remains:

```text
prove zero local intersection of the actual p24 ordinary CM point with the
phase-aware trace-GCD orbit Schubert/Fitting divisor.
```

Without diamond/right-unit determinant-line equivariance, the finite payload
is:

```text
seven Xi_O values plus seven inverses = 14 F_p elements,
```

or the global operator norm plus inverse if the proof constructs a single
honest full norm.

With the current diamond/Fitting compression target, the finite payload is:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

namely `4` base-field elements.  This compressed route is recorded in:

```text
p24/trace_gcd_diamond_fitting_equivariance_target.md
p24/trace_gcd_two_linearized_resultant_target.md
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

The `1092` scalar equations from the fixed-frequency H-coset route are a
different verifier interface: `156` left rows times `7` right H-cosets after
a tower-native construction supplies compressed coset sums.  They should not
be counted as Fitting orbit payload elements.
