# Selected-Tail Phase/Fitting Producer Frontier

Date: 2026-06-06

This note isolates the current missing theorem after the selected-tail
correction and the embedded tower/Kummer normal form.  The finite certificate
surface is now clean; the open part is an arithmetic producer for a
phase-aware determinant-line p-unit.

## Finite Object

For each beta translate, the direct selected-tail determinant is:

```text
M_tail(beta) =
  det( A_T(b_28(k_j))^(Q^i) )_{0 <= i,j < 10},
```

where `k_j` is an `E`-basis of:

```text
K_2,beta = ker(Top_2|W_axis,beta).
```

The denominator-safe package uses prefix p-units to put this determinant on a
fixed Fitting line.  Then:

```text
M_tail(beta) != 0  =>  K_sel,beta = {0}.
```

Orbitwise, with:

```text
Omega = {beta, beta*Q, ..., beta*Q^5548},
R_tail,Omega = product_{gamma in Omega} M_tail(gamma),
```

the crossed-product gate already proves:

```text
R_tail,Omega p-unit for all Omega
  => no selected-tail bad event for any beta.
```

## Phase Producer Interface

The embedded class-field tower might not naturally construct `M_tail(beta)`
itself.  It may instead construct a Kummer or relative-phase payload attached
to the same determinant line:

```text
Theta_Omega.
```

The finite requirement is only zero-detection:

```text
R_tail,Omega = 0  =>  Theta_Omega = 0,
Theta_Omega is a p-unit for every Omega.
```

or, locally:

```text
M_tail(beta) = 0  =>  Theta_{orbit(beta)} = 0.
```

This implication is now Lean-checked in:

```text
p24/lean/TraceFrameSelectedTailPhaseProducerGate.lean
```

It does not prove any CM arithmetic.  It records the exact handoff a
phase/Kummer producer must satisfy before it can replace the raw selected-tail
crossed-product norm.

## Strongest Theorem Candidate

The live arithmetic theorem is:

```text
For the p24 conductor-2 CM packet and the selected prime above p,
construct phase payloads Theta_Omega in the embedded class-field tower such
that:

  1. Theta_Omega lies on the Fitting/determinant line of
     A_T o b_28 : K_2,beta -> C/T over the beta orbit algebra;
  2. R_tail,Omega = 0 implies Theta_Omega = 0;
  3. every Theta_Omega is a p-unit, or one global phase norm detects every
     zero Theta_Omega and is a p-unit.
```

The most class-field-shaped specialization is a Plucker-Kummer theorem:

```text
Theta_Omega = unit_Omega * product_{gamma in Omega} M_tail(gamma)^r
```

for a relative Kummer exponent `r` coming from one of the `157` or `211`
tower layers, or an equivalent reduced norm in the crossed algebra.  The
point is that `Theta_Omega` must be attached to the selected-tail Plucker
coordinate itself, not merely to the primitive relative traces or matrix
entries from which that coordinate is built.

## Why Coordinate Kummers Are Not Enough

The Kummer normal form gives exact phase payload for selected child
polynomials:

```text
157 layer: one Frobenius orbit of 156 primitive Kummer powers
211 layer: six Frobenius orbits of 35 primitive Kummer powers.
```

Those values are equivalent to the selected child-polynomial phase, but
coordinatewise nonvanishing does not imply determinant nonvanishing.  A
determinant can vanish by row dependence while every visible relative trace
and every coordinate Kummer power is nonzero.

The finite boundary is tested by:

```text
p24/kummer_coordinate_nonzero_det_boundary_toy.py
p24/plucker_kummer_payload_toy.py
```

The first script gives the rank-one control:

```text
all_kummers_nonzero=1
determinant_zero_with_nonzero_kummers=1
```

The second script shows the correct determinant-level replacement:

```text
plucker_kummer = det^r
plucker_kummer_detects_zero=1.
```

Thus a usable producer must construct a Plucker/Fitting Kummer payload, or an
orbit norm of such a payload.  Plain relative character traces remain
coordinates, not the certificate.

## Embedded Tower Obligations

The tower data are:

```text
G = Cl(O_K) = <g>
G > <g^2> > <g^314> > <g^66254>
relative degrees: 2, 157, 211
recovery quotient size: 3107441
```

The theorem must supply three pieces that abstract class-field roots do not:

```text
1. embedded phase: relative class-character or Kummer data paired with the
   actual conductor-2 singular-modulus torsor over F_p;
2. determinant-line descent: proof that the selected-tail Fitting/Plucker
   coordinate is semi-invariant, or that its whole orbit norm is the produced
   phase payload;
3. local unit proof: p-adic/unit argument at the selected prime showing the
   phase payload is a unit.
```

Without item 1, `bnrclassfield` roots are unpaired with the CM `j` roots.
Without item 2, coordinate Kummers do not see determinant cancellation.
Without item 3, the identity is only a repackaging, not a certificate.

## Computation That Helps

Computation should now be used only as a theorem debugger:

```text
pass:
  a small actual-CM row shows an exact Plucker/Fitting zero-detection identity
  between the determinant line and relative Kummer/phase data;

fail:
  the proposed payload is only a coordinate Kummer, only an orbit norm of
  child phase, only abstract quotient roots, or appears first at a generic
  interpolation threshold.
```

The next useful small test is:

```text
for a complete small CM tower row, compute:
  1. the selected determinant sequence Delta;
  2. the relative Kummer/phase coordinates for the same embedded row;
  3. whether Delta=0 is detected by a Plucker/Fitting Kummer payload,
     not by coordinatewise nonzero values.
```

This test is intentionally small.  If it takes p24-scale enumeration to see
the pattern, it is not the asymptotic speedup requested by the challenge.

## Holdout Crossed-Product Check

I also ran the sidecar-suggested crossed-product holdout on a small composite
CM row, using valid component targets for the encountered `m=6` case:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_trace_sum_crossed_product_audit.py \
  --include-linear --require-composite-m \
  --min-h 40 --max-h 260 --max-abs-D 80000 \
  --max-n 260 --max-m 60 --max-factor-degree 18 \
  --max-extension-degree 8 --max-tensor-factor-degree 12 \
  --max-top-count 4 --max-cases 12 \
  --target axis --target constant_plus_3
```

It produced:

```text
rows=16
block_det_match=1 on every row
weighted_shift_match=1 on every row
block_det_zero=0 on every row
ordinary_power_match=0 on nonconstant orbits
```

This does not prove the p24 p-unit theorem.  It does keep the crossed-product
selected-tail norm surface alive on proper small tail rows with
`residual_dim` up to `3`, and it again rejects ordinary norm collapse as the
certificate object.

## Current Status

The finite gates are complete enough for this route:

```text
selected-tail determinant p-unit
  => selected trace frame good;

selected-tail crossed-product norm p-unit
  => selected-tail determinant nonzero on every beta orbit;

phase payload detects selected-tail norm zero
  + phase payload p-unit
  => selected-tail crossed-product norm nonzero.
```

The missing theorem is arithmetic:

```text
produce and prove p-unitness of a phase-aware selected-tail Fitting payload
from the embedded 2-157-211 class-field tower, without enumerating the full
CM class set.
```

This is narrower than "construct the whole tower" and stronger than
"coordinate Kummers are nonzero."  It is the current best theorem candidate
for a genuine sub-sqrt certificate.
