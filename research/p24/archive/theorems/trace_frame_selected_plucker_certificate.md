# Trace-Frame Selected Plucker Certificate

Date: 2026-06-05

This note isolates the smallest current `L1` trace-frame certificate surface.

## Coordinate-Free Object

For one p24 H-packet and one tensor factor:

```text
E = F_p(mu_m)
B/E has degree 5549
C/E has degree 179
B/C has degree 31
```

Let:

```text
S_axis = {0} union nonzero 2-, 157-, and 211-axis K-characters.
```

For each `s in S_axis`, let `R_s in B` be the corresponding K-character
resolvent in the chosen tensor factor.  The selected trace-frame map is:

```text
Top_3 : B -> C^3,
```

the top three relative `C`-coefficients of `g'(theta)*x`.

The canonical exterior object is:

```text
Omega_top3 = wedge_{s in S_axis} Top_3(R_s)
             in Exterior_E^368(C^3).
```

The p24 theorem for this packet/factor is simply:

```text
Omega_top3 != 0.
```

This is coordinate-free and exactly equivalent to axis injectivity in the
chosen trace-frame.

## Finite Certificate

A finite verifier can choose an `E`-basis of `C` and a `368`-subset `I` of
the `537=3*179` trace-frame coordinates.  This gives a Plucker coordinate:

```text
delta_I = det( coordinate_I(Top_3(R_s)) )_{s in S_axis}.
```

The certificate condition is:

```text
delta_I != 0 in E.
```

The coordinate count is large:

```text
binom(537,368) ~= 10^143.820126.
```

So a certificate has to name `I`, or the proof has to produce a
coordinate-free norm identity for `Omega_top3`.  There is no canonical
single determinant without a coordinate choice.

The accounting script is:

```text
p24/trace_frame_selected_plucker_accounting.py
```

It reports:

```text
axis_dimension=368
top_target_dimension=537
h_packet_count=8
tensor_factor_count_over_E=70
```

Tensor-factor rank symmetry means a proof/certificate for one tensor factor
propagates across the `70` factors once the factor choice is fixed; the eight
H-packets still need coverage or a degree-8 decomposition-field product.

## Best Current p24 Certificate Shape

The smallest explicit certificate route is:

```text
for each of the eight H-packets:
  name one tensor factor B_i over E;
  name one Plucker coordinate I;
  prove delta_{a,i,I} is a p-unit/nonzero.
```

Equivalently, package the eight selected coordinates into a
decomposition-field product:

```text
Delta_selected = product_a delta_{a,i(a),I(a)}
```

and prove:

```text
Delta_selected != 0.
```

This is stronger than the intrinsic statement only because it chooses
coordinates, but it is verifier-friendly.

## Leading-Prefix Candidate

The current best named-coordinate candidate is no longer arbitrary after the
trace-frame basis/order is fixed.  In the normal `E`-basis of `C` used by the
trace-frame construction, order the coordinates blockwise in `C^3`.  Then
take:

```text
I_lead = first 368 coordinates
       = 179 + 179 + 10.
```

Equivalently, keep the first two full top-coefficient blocks and the first
ten normal coordinates of the third block.  The sharpened finite target is:

```text
delta_lead != 0 in E
```

in each H-packet, or the degree-8 product of these `delta_lead` values.

Equivalently, over the base field this can be checked as:

```text
Norm_{E/F_p}(delta_lead) != 0
```

for the selected embedded origin in each packet.  A beta-product over
H-translates would be an origin-stable strengthening, not a free consequence
of the selected-coordinate theorem.

The small actual-CM pivot audit is recorded in:

```text
p24/trace_frame_leading_plucker_pivot_theorem.md
p24/trace_frame_plucker_pivot_audit.py
```

On the pinned `D=-10919, m=12` tensor analogue, the deterministic row-reduction
pivots are the leading prefix across the tested origins for the full axis and
for both component-plus-constant targets.  This is not a proof, and it is not
intrinsic Grassmannian structure.  It turns the previous "some Plucker
coordinate" surface into a specific verifier-facing Schubert-tail p-unit
candidate.

## Relation To Stronger Routes

The all-three-block erasure theorem in:

```text
p24/trace_frame_sum_rank_erasure_theorem.md
```

would prove many Plucker coordinates nonzero, but it asks for all
`binom(31,3)=4495` block projections.  That is better as a proof import than
as certificate data.

The visible LRS/MSRD route in:

```text
p24/trace_frame_lrs_signature_boundary.md
```

did not find simple low-displacement structure in the natural relative
coefficient matrix.  Therefore the selected Plucker p-unit remains the
smallest honest finite certificate surface.

The kernel-shape audit in:

```text
p24/trace_frame_annihilator_kernel_boundary.md
```

explains why this has to be a Plucker/direct-sum theorem rather than a list of
component p-units.  In compact trace-frame rows, dimension-forced kernels can
remain after every individual smooth-axis block is injective; the residual
kernel is cross-block.  Therefore the p24 theorem must prove the leading
Schubert coordinate itself is a p-unit, or prove an equivalent cross-block
transversality statement.

The factorized Schubert version is recorded in:

```text
p24/trace_frame_factorized_schubert_punit.md
```

It splits the leading coordinate into a prefix rank p-unit and a residual-tail
p-unit on the 10-dimensional kernel after the first two trace-frame blocks.
This is the smallest currently named proof surface for the cross-block
obstruction.

## Open Arithmetic Input

The missing theorem is now:

```text
For the actual p24 CM axis resolvents, at the selected prime p,
the leading-prefix Plucker coordinate delta_lead of Omega_top3 is a p-unit
for the selected embedded origin in every H-packet.
```

This is a selected-prime class-field p-unit theorem.  It is not implied by
generic rank, random-subspace heuristics, or the finite Lean gates.
