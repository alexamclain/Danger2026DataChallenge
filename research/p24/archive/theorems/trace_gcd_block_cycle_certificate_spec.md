# Trace-GCD Block-Cycle Certificate Spec

Date: 2026-06-05

This is the verifier-side contract for the current p24 trace-GCD
block-cycle route.  It answers a practical question: what computation is still
useful?

Short answer:

```text
use computation for exact finite manifests, small-CM falsification, and
arithmetic-honesty tests;

do not use computation to enumerate the p24 class set or to search at
sqrt(p) scale.
```

The mathematical target remains a producer theorem.  Computation is useful
only when it sharpens or falsifies that theorem without becoming the proof.

## Fixed p24 Constants

```text
p = 10^24 + 7
sqrt(p) = 10^12 + tiny
right factor ell = 211
q = p mod 211 = 114
ord_211(q) = 35
block size k = 16
```

The Frobenius orbits on `Z/211Z` are:

```text
O0 length 1:
  [0]

O1 length 35:
  [1, 114, 125, 113, 11, 199, 109, 188, 121, 79, 144, 169,
   65, 25, 107, 171, 82, 64, 122, 193, 58, 71, 76, 13, 5,
   148, 203, 143, 55, 151, 123, 96, 183, 184, 87]

O2 length 35:
  [2, 17, 39, 15, 22, 187, 7, 165, 31, 158, 77, 127, 130,
   50, 3, 131, 164, 128, 33, 175, 116, 142, 152, 26, 10, 85,
   195, 75, 110, 91, 35, 192, 155, 157, 174]

O3 length 35:
  [4, 34, 78, 30, 44, 163, 14, 119, 62, 105, 154, 43, 49,
   100, 6, 51, 117, 45, 66, 139, 21, 73, 93, 52, 20, 170,
   179, 150, 9, 182, 70, 173, 99, 103, 137]

O4 length 35:
  [8, 68, 156, 60, 88, 115, 28, 27, 124, 210, 97, 86, 98,
   200, 12, 102, 23, 90, 132, 67, 42, 146, 186, 104, 40,
   129, 147, 89, 18, 153, 140, 135, 198, 206, 63]

O5 length 35:
  [16, 136, 101, 120, 176, 19, 56, 54, 37, 209, 194, 172,
   196, 189, 24, 204, 46, 180, 53, 134, 84, 81, 161, 208,
   80, 47, 83, 178, 36, 95, 69, 59, 185, 201, 126]

O6 length 35:
  [29, 141, 38, 112, 108, 74, 207, 177, 133, 181, 167, 48,
   197, 92, 149, 106, 57, 168, 162, 111, 205, 160, 94, 166,
   145, 72, 190, 138, 118, 159, 191, 41, 32, 61, 202]
```

For each nonzero orbit:

```text
r = 35
k*r = 560
(-1)^(k*(r-1)) = +1
```

So the block-cycle determinant equals the orbit product with no sign change.

## Determinant Target

The finite sequence is:

```text
Delta(t) = det(P V_t A),      t mod 211.
```

The verifier target is:

```text
Delta(t) != 0 for every t mod 211.
```

For an orbit

```text
O = {t0, q*t0, ..., q^(r-1)*t0},
```

the matrix-level crossed-product object is:

```text
B_O e_i = M_{q^i t0} e_{i+1},
Delta(q^i t0) = det(M_{q^i t0}).
```

For p24 nonzero orbits, `B_O` is a `560 x 560` operator and:

```text
det(B_O) = prod_{t in O} Delta(t).
```

The orbit `O0 = {0}` is the fixed one-step case.

Multiplication by `2 mod 211` fixes `O0` and cycles the six nonzero right
orbits:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

This finite bookkeeping is checked by:

```text
p24/trace_gcd_unit2_orbit_compression_audit.py
p24/lean/UnitOrbitGate.lean
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

With a producer theorem proving determinant-line equivariance up to p-unit
transition factors, the seven orbit products compress to:

```text
Pi_O0 plus inverse
+ one nonzero representative Pi_O plus inverse
= 4 F_p elements.
```

The small actual-CM warning audit is:

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

It shows that right-unit symmetry should not be upgraded to literal equality
of printed orbit norms; the invariant claim is p-unit-scale propagation.

The determinant-line proof target is isolated in:

```text
p24/trace_gcd_diamond_fitting_equivariance_target.md
```

Its finite linear-algebra shadow is:

```text
p24/trace_gcd_diamond_equivariance_toy.py
```

which checks that invertible transports scale determinants by p-units and
therefore preserve p-unitness and zero status.

The conditional compressed verifier schema is:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```

## Minimal Payload

The preferred finite certificate supplies:

```text
for each O in {O0,...,O6}:
  Pi_O
  Pi_O_inv
```

and the verifier checks:

```text
Pi_O * Pi_O_inv = 1 mod p.
```

Payload size:

```text
14 F_p elements
14 / sqrt(p) = 1.4e-11.
```

This is sound only with the arithmetic honesty theorem:

```text
Pi_O = det(B_O)
```

where `B_O` is the actual p-integral block-cycle/Fitting operator built from
the p24 trace-GCD tail maps.  The finite gate then gives:

```text
Pi_O nonzero for every O
=> prod_{t in O} Delta(t) nonzero for every O
=> Delta(t) nonzero for every t.
```

The finite zero-detection step, including singular controls, is exercised by:

```text
p24/block_cycle_fitting_zero_detection_toy.py
p24/lean/TraceGcdBlockCycleGate.lean
```

## Optional Expanded Payloads

The conservative pointwise payload is:

```text
Delta_t, Delta_t_inv for all t mod 211
```

with size:

```text
422 F_p elements
422 / sqrt(p) = 4.22e-10.
```

If a producer naturally supplies explicit block matrices, the raw matrix
sizes are still sub-sqrt in field-element count:

```text
O0 block matrix entries: 16^2 = 256
six nonzero block matrices: 6 * 560^2 = 1,881,600
total explicit block matrix entries = 1,881,856
with inverse matrices = 3,763,712
ratio to sqrt(p) = 3.763712e-6.
```

This is not the desired final certificate because it shifts work from a
seven-scalar norm theorem to large linear algebra.  It is nevertheless useful
as a debugging payload if the producer theorem first lands at the matrix
level.

## Useful Computation

Computation is productive in these bounded roles:

```text
1. exact p24 manifest generation:
   orbit lists, dimensions, signs, payload counts;

2. small-CM theorem falsification:
   run the block-cycle audit on right-7/right-19/right-31 style rows and
   check determinant/product/kernel equivalences;

3. randomized algebra models:
   stress the local-intersection theorem shape before spending proof effort;

4. spectral and recurrence audits:
   test whether proposed degree collapses are genuine or only artifacts of
   tiny examples;

5. finite verifier checks:
   Lean gates for the implication from honest norms to nonzero determinant
   values.
```

Computation is not productive in these roles:

```text
1. enumerating the p24 class set;
2. class-set product norms without a closed formula;
3. long searches for raw determinant values;
4. pretending arbitrary nonzero scalars are a certificate.
```

## Current Missing Theorem

The theorem to prove is:

```text
For each Frobenius orbit O on Z/211Z, construct the p-integral
block-cycle/Fitting operator B_O attached to the actual p24 trace-GCD tail
maps and prove det(B_O) is a p-unit.
```

Equivalent local-intersection form:

```text
For each right Frobenius orbit O, there is no nonzero section in the direct
sum of transported prefix kernels whose block-cycle tail image is zero.
```

The finite part is already checked in:

```text
p24/lean/TraceGcdBlockCycleGate.lean
```

The determinant-line basis-change hygiene is checked in:

```text
p24/block_cycle_determinant_line_invariance_toy.py
p24/lean/DeterminantLineUnitScaleGate.lean
```

Changing p-integral bases in the source and target blocks scales
`det(B_O)` by a p-unit, so zero/nonzero and p-unit status are intrinsic to
the Fitting determinant line.

The small actual-CM audit supporting the formula is:

```text
p24/lang_trace_gcd_block_cycle_norm_audit.py
p24/lang_trace_gcd_block_cycle_norm_boundary.md
```

The exact p24 constants in this document are generated by:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_block_cycle_certificate_manifest.py
```

The finite 14-element payload verifier is:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py
```

Run without a certificate to print the JSON schema:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_orbit_norm_certificate_verifier.py --schema
```

Given a payload, it checks:

```text
Pi_O * Pi_O_inv = 1 mod p
```

for all seven right Frobenius orbits, reports:

```text
payload_field_elements=14
payload_over_sqrt_floor=1.4e-11
producer_honesty_required=1
```

The final line is essential: the arithmetic theorem must still prove that the
supplied `Pi_O` values are the actual p24 phase-aware block-cycle/Fitting
orbit norms.
