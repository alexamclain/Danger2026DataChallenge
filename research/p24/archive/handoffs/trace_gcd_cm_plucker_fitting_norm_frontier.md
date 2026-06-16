# Trace-GCD CM Plucker/Fitting Norm Frontier

Date: 2026-06-06

This note records the proof surface after the fixed Fourier-head minors have
been removed from the list of possible obstructions.

## Exterior Norm Object

Fix one nonzero right Frobenius orbit

```text
O subset (Z/211Z)^*,        |O| = 35,
k = 16.
```

Over the 211st-root splitting field, let

```text
B_O = direct sum_{u in O} E e_u,
V_t e_u = zeta_211^(t u) e_u.
```

The trace-GCD tail gives a p-integral decomposable vector

```text
a_trace = wedge^16 A(K_0) in wedge^16 B_O,
```

and the selected Lang head gives a fixed exterior functional

```text
ell_head in (wedge^16 B_O)^vee.
```

Then

```text
Delta_O(t) = ell_head((wedge^16 V_t) a_trace).
```

In coordinates:

```text
Delta_O(t)
  = sum_{U subset O, |U|=16}
      det(P_U) det(A_U) zeta_211^(t * sum_U u).
```

The fixed coefficients `det(P_U)` are p-units by
`p24/trace_gcd_fourier_minor_unit_theorem.md`.  Thus the remaining theorem is
entirely about the actual CM determinant line `a_trace`.

## Sharp Plausible Theorem

The producer theorem should now be stated as:

```text
For the conductor-2 p24 CM phase torsor, the determinant line
a_trace = wedge^16 A(K_0) is p-integral in the right-orbit exterior lattice,
and for each of the seven right Frobenius orbits O the scalar

  Pi_O = prod_{t in O} ell_head((wedge^16 V_t) a_trace)

is a p-unit at the selected ordinary prime over p=10^24+7.
```

Equivalently, the p-integral Fitting element

```text
f_O(Y) =
  sum_{U subset O, |U|=16}
    det(P_U) det(A_U) Y^(sum_U u)
```

is a unit in the right orbit algebra after reduction at the selected p24
prime:

```text
f_O mod Phi_O(Y) in O_p[Y]/Phi_O(Y) is a unit.
```

The global two-element payload is the same statement with `Y^211-1` instead
of `Phi_O`.

## Constructive Route

The proof has to construct `a_trace` or `f_O` from embedded non-genus
`157/211` relative phase data.  A useful lemma stack is:

```text
1. p-integral exterior line:
   A(K_0) defines a p-integral rank-16 determinant line in B_O.

2. phase descent:
   that determinant line is a function of the embedded class-field phase
   torsor, not of an enumerated class set.

3. Fitting/Chow comparison:
   ell_head((wedge^16 V_t) a_trace)=0 cuts out exactly the translated
   Schubert/Chow divisor W_trace cap V_t^{-1}ker(P) != {0}.

4. local p-unit theorem:
   the pulled-back orbit divisor has zero local intersection with the
   selected p24 ordinary CM point, or is the divisor of a phase-aware
   Borcherds/Fitting product whose CM value has p-adic valuation zero.
```

This is stronger and more specific than proving coordinatewise Kummer
nonvanishing.  It is weaker than producing the entire p24 class set.

## Concrete Small-Scale Identity To Test

On small actual-CM rows, the next bounded audit should check determinant-line
descent rather than raw determinant-value descent:

```text
input:
  one small trace-GCD row with right orbit O;
  the transported kernel map A;
  the selected Lang-head projection P.

check:
  1. compute the exterior Plucker vector a_trace in the split right orbit;
  2. compute f_O(Y) from the Cauchy-Binet formula;
  3. verify f_O(zeta^t)=det(P V_t A) for every t;
  4. test whether the projective line [a_trace] is equivariant under the
     embedded right-phase action, up to p-unit scalars;
  5. compare the crossed-product norm of f_O with the block-cycle/Fitting
     determinant already used by the finite gate.
```

The exact finite triangle to enforce, including signs and p-unit
normalizations, is:

```text
prod_{t in O} det(P V_t A)
  = det(block-cycle(M_t : t in O))
  = Norm_O(sum_U det(P_U) det(A_U) Y^(sum_U u)).
```

The first equality is finite Fitting linear algebra; the second is the
exterior resultant/operator-norm identity.  In p24 the block-cycle sign is
positive because `16*(35-1)` is even.

The block-cycle determinant should be read as a determinant-line/Fitting
norm.  Independent p-integral source and target basis changes scale it by a
p-unit and preserve zero status; this is checked in:

```text
p24/block_cycle_determinant_line_invariance_toy.py
p24/lean/DeterminantLineUnitScaleGate.lean
```

The p-local ordinary-prime version of this statement is isolated in:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
```

It states the remaining theorem as zero local intersection of the selected
p24 ordinary CM point with the phase-aware orbit Schubert/Fitting divisor.

The split finite-field toy for this triangle is:

```text
p24/trace_gcd_norm_triangle_toy.py
```

The faithful pinned actual-CM audit is:

```text
p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

Default run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_actual_cm_norm_triangle_audit.py
```

On the pinned row

```text
D=-13319, q=13463, h=140, m=28, n=5, right=7,
block_size=2, Frobenius orbits [0], [1,2,4], [3,6,5],
```

it reports for both omitted rows:

```text
right_class_det_mismatches=0
split_eval_mismatches=0
naive_base_polynomial_possible=0
product_equals_signed_block_cycle=1
product_equals_split_norm=1
orbit_norm_nonzero=1
failures=0
```

Thus the scalar determinant sequence, actual block-cycle/Fitting determinant,
and split-interpolant norm are the same object on a faithful small CM row.
The non-base split coefficients keep the crossed-product distinction alive.

The positive-size orbit-norm miner for the same actual row is:

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
```

Default run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_actual_cm_orbit_norm_miner.py
```

It reports six actual orbit norms, all nonzero:

```text
matrix_rows=1
orbit_rows=6
nonzero_orbits=6
zero_or_bad_orbits=0
zero_norm_orbits=0
```

The individual norms are:

```text
omitted=0: 2125, 2515, 603
omitted=1: 11423, 9495, 6085
```

This is stronger evidence than the split toy alone: it tests the actual
tail-on-kernel determinant values before taking the block-cycle/Fitting norm.
It is still evidence, not a p24 proof; the proof must explain these units by a
class-field/Fitting divisor identity rather than by broad empirical scanning.

The first bounded phase-unit dictionary does not explain the same small-row
values:

```text
p24/trace_gcd_phase_unit_dictionary_boundary.md
```

Right-binomial units and low-Heegner fiber units capture the determinant
sequence only after reaching full ambient rank in odd discrete-log factors,
and miss the mod-2 log component.  This demotes the shortcut

```text
trace-GCD phase determinant = product of simple phase units
```

for the pinned row.  A successful proof still needs the actual
phase-aware Fitting/Borcherds section, not a generic small-unit span.

It is also part of the lightweight falsifier harness:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py --skip-spectral --no-danger3-inventory
```

The actual-CM triangle is available in that harness behind:

```text
--include-actual-cm-triangle
```

If step 4 fails in faithful small rows, the phase-aware class-field route must
target only orbit norms or a Borcherds divisor, not an individual descended
Plucker coordinate.

## False Shortcuts To Avoid

```text
fixed Fourier minors:
  already p-units; not the remaining obstruction.

coordinatewise Kummer p-units:
  nonzero entries do not prevent determinant cancellation.

one-orbit spectral support:
  p24 exterior support is all of Z/211Z already by distinct 3-subset sums.

generic/random nonvanishing:
  useful for falsification and probability baselines, but not a certificate
  at the selected p24 prime.

Jacobi complementary minors:
  correct as linear algebra, but only moves the selected Schubert condition
  to a complementary inverse minor unless a new CM theorem controls that
  inverse determinant line.
```

## Current Status

This is not yet the p24 certificate.  It is the narrowed theorem frontier:

```text
prove a p-unit orbit norm for the actual CM exterior determinant line.
```

If this theorem is proved, the existing Lean gates consume either seven orbit
products plus inverses or one global operator norm plus inverse, both
asymptotically below `sqrt(p)`.
