# Selected-Tail Borcherds Local-Intersection Frontier

Date: 2026-06-06

This note translates the older trace-frame Borcherds p-unit route from the
full leading determinant `Xi_lead` to the corrected selected-tail/Fitting
surface.

## Why Another Frontier

The denominator-safe global payload should still prefer:

```text
Xi_A, Xi_B, Xi_AB, Xi_lead
```

because packetwise bases of:

```text
K_2 = ker(Top_2|W_axis)
```

can hide denominators.  But the proof obstruction exposed by the corrected
finite theorem is more local:

```text
A_T o b_28 : K_2 -> C/T
```

must be an isomorphism after reduction at the selected prime, on the open
prefix chart.  Its determinant is the selected-tail Fitting/Schubert divisor.

Thus a Borcherds/local-intersection proof has to address this divisor, not
the older intrinsic full-top-three replacement:

```text
W_axis cap F_27 = {0}.
```

## Local Criterion

Let `O_p` be the localization of the embedded phase/class-field coefficient
ring at the selected ordinary prime over:

```text
p = 10^24 + 7.
```

For a beta orbit `Omega`, let:

```text
B_tail,Omega : K_2,Omega -> C/T
```

be the p-integral selected-tail Fitting map on a prefix-certified chart, and
write:

```text
R_tail,Omega = det(B_tail,Omega)
```

as a determinant-line section, understood up to p-units from basis choices.
Then:

```text
R_tail,Omega in O_p^*
  <=> coker(B_tail,Omega) has unit zeroth Fitting ideal
  <=> the selected ordinary CM point has zero local intersection with
      the pulled-back selected-tail Schubert divisor D_tail,Omega.
```

The finite implication needed by the trace-frame certificate is the forward
direction:

```text
R_tail,Omega p-unit for all Omega
  => K_sel,beta = {0} for every beta
  => the selected trace frame is good.
```

The prefix chart is part of the statement.  Without `Xi_A`, `Xi_B`, and
`Xi_AB` as p-units, an arbitrary tail determinant built from a kernel basis is
not a descended p-integral section.

## Borcherds/Chow Theorem Candidate

The strongest honest product-formula theorem is:

```text
For every beta orbit Omega, construct a phase-aware p-integral product
Psi_tail,Omega with:

  1. div(Psi_tail,Omega) =
       pulled-back selected-tail Schubert divisor D_tail,Omega
       + vertical/boundary terms away from the selected p24 prime;

  2. Psi_tail,Omega =
       p-unit * Theta_tail,Omega
     near the selected ordinary CM point, where Theta_tail,Omega is a
     phase/Fitting payload detecting R_tail,Omega = 0;

  3. v_p(Psi_tail,Omega(x_p24)) = 0
     for the chosen ordinary orientation sqrt(D_K)=+/-t/2 mod p.
```

Then `Theta_tail,Omega` is a p-unit, hence `R_tail,Omega` is nonzero, hence no
selected-tail bad event occurs on `Omega`.

The finite handoff is Lean-checked in:

```text
p24/lean/TraceFrameSelectedTailBorcherdsGate.lean
```

It composes the local-intersection comparison with the selected-tail
phase-producer gate:

```text
zero local intersection
  => Borcherds/Chow value is a p-unit
  => selected-tail phase payload is a p-unit
  => selected-tail norm zero is impossible
  => no selected-tail bad event.
```

## Exact Missing Lemmas

The theorem has three non-formal inputs.

1. Phase-aware divisor construction.

```text
D_tail,Omega
```

must be realized as the divisor of an explicit class-field/Borcherds/Fitting
product.  Plain `j`, one oriented edge, and ordinary base-field residues are
not enough; existing small-row scans make those look generic.

2. Determinant-line comparison.

The product must compare to the selected-tail Fitting line, not merely to
coordinate Kummers or entrywise relative traces.  Coordinatewise Kummer
p-units do not prevent determinant cancellation.

3. p24 local valuation.

Using the explicit p24 ordinary prime data:

```text
sqrt(D_K) =  t/2 mod p  or  -t/2 mod p,
p is prime to 2,157,211,66254,3107441,h,
```

prove the local intersection contribution at the selected ordinary embedding
is zero.

## What Is Already Ruled Out

The easy divisor recognitions fail in the trace-frame and trace-GCD rows:

```text
plain selected-j divisor:
  generic rational degree, no stable small-Heegner support;

single oriented-edge relation:
  no bounded low-bidegree formula;

coordinate Kummer nonvanishing:
  determinant can vanish with every coordinate Kummer nonzero;

ordinary base-polynomial descent:
  crossed-product orbit norms survive, ordinary norm collapse fails.
```

So a successful proof must construct the pulled-back selected-tail divisor
itself, or bypass divisors with a direct Fitting p-unit theorem.

## Useful Small Falsifier

The next computation should test divisor identity, not probability:

```text
on a small complete CM tower row with a genuine residual tail:
  1. compute the selected-tail determinant-line sequence;
  2. compute phase coordinates for the same embedded row;
  3. test whether the zero divisor of the determinant-line sequence lies in
     a proposed phase-aware divisor span before that span becomes the full
     ambient interpolation space.
```

A pass means an exact low-complexity divisor identity, not just all values
being nonzero.  A fail means the Borcherds route must be even more specific,
or the proof must return to a direct local Fitting-unit argument.

The holdout crossed-product audit already supports the finite norm identity:

```text
rows=16
block_det_match=1
weighted_shift_match=1
ordinary_power_match=0 on nonconstant orbits
```

It does not test the Borcherds divisor construction.  It only says the
selected-tail norm object being handed to the product formula is the right
crossed-product/Fitting object.

## Phase-Divisor Identity Holdout

The combined holdout:

```text
p24/trace_gcd_phase_divisor_identity_holdout.py
```

tests the sidecar's proposed distinction on the pinned actual-CM
`D=-13319, q=13463, m=28, pair=(4,7)` row.  It asks whether the bounded
right-binomial plus small-Heegner unit dictionary recognizes the Chow/Fitting
phase vector before full log-rank interpolation, and it adds a determinant
zero control with all entries and coordinate powers nonzero.

Default output:

```text
unit_dictionary_size=78
nonrandom_span_hits=0
full_rank_interpolation_hits=4
target_misses=2
coordinate_payload_zero_detection_failure=1
```

Interpretation:

```text
1. the bounded dictionary produces no non-random product formula;
2. the odd log components contain the target only after rank 7/7, where
   random controls also always fit;
3. coordinate/Kummer-style nonzero payloads do not detect a forced determinant
   zero.
```

This does not rule out a bespoke phase-aware Borcherds/Fitting section, but
it rules out the currently visible bounded unit dictionary and reinforces that
the payload must live on the determinant line itself.

## Simple-Root/Different Boundary

The local ordinary setup is friendly, but friendliness is not the theorem.
The pinned check:

```text
p24/cm_simple_root_different_boundary.py
```

reports:

```text
class_polynomial_degree=140
root_count_mod_q=140
class_polynomial_split_squarefree=1
zero_derivative_count=0
control_det_zero=1
```

Thus the CM algebra is split etale at the small ordinary prime, but an
unrelated section can still vanish at a simple CM root, and a determinant-line
control can be singular with all coordinate entries nonzero.  The p24 proof
cannot be replaced by a simple-root/Hensel/different unit statement; it must
prove the selected-tail determinant-line section is a p-unit.

## Current Assessment

An independent arithmetic sidecar reached the same boundary: the missing lemma
is not local p-adic friendliness, because the p24 prime is split, unramified,
and prime to all certificate levels.  The missing lemma is divisor
realization:

```text
the pulled-back selected-tail Schubert/Fitting divisor must be the divisor of
an explicit embedded 2-157-211 class-field/Borcherds/Fitting section, with
only boundary/vertical correction away from the selected p24 prime, and this
section must compare to the actual selected-tail crossed-product norm by a
p-unit.
```

The sidecar's proposed falsifier agrees with the one above: a real product
formula must recognize the determinant-line phase vector before the candidate
unit/divisor dictionary reaches full interpolation rank, and it must vanish
on a forced determinant-zero control.  Coordinate Kummers fail this control;
plain divisor dictionaries currently fit only at random/full-rank scale.

This is now the cleanest divisor-form statement of the missing theorem:

```text
prove zero local intersection of the selected p24 ordinary CM point with the
phase-aware selected-tail Schubert/Fitting divisor on the prefix-good chart.
```

If this theorem is proved, the certificate surface remains sub-sqrt through
the existing selected-tail crossed-product and prefix-tail Lean gates.  If it
fails, the remaining route is a direct p-adic noncancellation proof for the
same Fitting determinant line.
