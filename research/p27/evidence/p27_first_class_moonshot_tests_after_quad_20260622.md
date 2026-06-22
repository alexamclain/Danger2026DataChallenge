# P27 First-Class Moonshot Tests After Quadratic Probe

Date: 2026-06-22

## Claim

After the GPU quadratic-gate result and the q1847 B/K quartic closures, the
p27 moonshot should not spend a large GPU run on another fixed one-bit filter.
The remaining tests that could beat `sqrt(p)` are source or class tests:

```text
1. Coordinated A/B/K/Sroot Kummer sequence extraction.
2. BSM staged legal-pullback normalization.
3. trace/norm half-norm phase identity.
4. bounded GPU telemetry only when it feeds one of the above.
```

The shared promotion bar is strict:

```text
promote = a direct sampler, low-genus/sourceable quotient, or recurrence
          coupling multiple selected gates without paying a fresh half-loss
kill    = one more conditional 2x lift whose source denominator costs 2x
```

## Current Boundary

Closed practical/GPU shortcuts:

```text
fixed quadratic precheck:
  validated formula, but target/source_draw is flat or slightly lower

B/K/lambda visible quartics:
  q1847 B d3 exact_quartics = 0
  q1847 K d3 exact_quartics = 0
  q1847 B gate4-prefix exact_quartics = 0
  q1847 lambda d3 exact_quartics = 0

visible branch dynamics:
  A/B/K/lambda S3, PGL2, Chebyshev, monomial, and hidden-X power maps
  do not give stable d3/d4 recurrence
```

These results do not kill the A/B/K/Sroot Kummer route.  They kill the nearby
coefficient buckets and map-family shortcuts, and the fixture bridges collapse
the surviving coordinates to one class-extraction problem.

## Test 1: Coordinated A/B/K/Sroot Kummer Sequence

Use:

```text
research/p27/evidence/p27_b_line_kummer_extraction_packet_20260622.md
research/p27/archive/gates/p27_b_line_kummer_extraction_packet.py
research/p27/archive/probe_outputs/p27_b_line_kummer_extraction_packet_20260622.txt
```

Known structure:

```text
B = 8X^2/(X^2 - 1)^2
A + 2 = B^2
d3, d4, ... descend to original Bplus in all tested active rows
deep p27 B-prefix counts still thin like independent half-losses
extension-field all-plus plateaus are field-local and stop at moving gates
```

Latest count-only falsifier:
[P27 B-Line Prefix Extension Ladder](p27_b_line_prefix_extension_ladder_20260622.md).
It keeps B-line extraction live, but kills B-prefix counts alone as a direct
below-sqrt sampler.

Follow-up:
[P27 B-Line Frobenius Plateau Audit](p27_b_line_frobenius_plateau_audit_20260622.md).
The local plateaus are not proper-subfield or short-Frobenius-orbit samplers;
all tested plateau sets have full extension degree.  Use them as Kummer-class
regression fixtures, not as production buckets.

Second follow-up:
[P27 B-Line Trace/Norm Plateau Audit](p27_b_line_trace_norm_plateau_audit_20260622.md).
Relative trace+norm is exact only for quadratic extension quotients; prime
degree fields are mixed.  This kills trace/norm bucket sampling as a p27 lane.

Compact CAS input:
[P27 B-Line Kummer Fixture Packet](p27_b_line_kummer_fixture_packet_20260622.md).
It freezes the conditional rows for `f3(B), f4(B), f5(B), f6(B)` over
q1607/q1847/q2087.  The actionable comparison is now `f3` and `f4/f3`; the
later `f5/f6` guard-field rows are one-sided field tails unless a larger
heldout run supplies a named class and raw-source denominator.

Coordinate bridge:
[P27 B/K/Sroot Fixture Bridge](p27_b_ksroot_fixture_bridge_20260622.md).
It proves the frozen B-line and K/Sroot fixtures are exact coordinate views of
the same conditional classes.  Treat B-line and K/Sroot as one coordinated
class-extraction problem, not independent moonshot lanes.

Second coordinate bridge:
[P27 B/A Fixture Bridge](p27_b_a_fixture_bridge_20260622.md).
It proves the frozen A-level `d3,d4` rows are also exact B-line coordinate
views under `A=B^2-2`: `267/267` row-level sign matches and no collisions
across q1607/q1847/q2087.  Treat A as a quotient/check coordinate for the same
problem, not a separate GPU bucket or CAS lane.

Reduced fiber check:
[P27 B-Line Fiber Invariant Probe](p27_b_line_fiber_invariant_probe_20260622.md).
For every legal B in q1607/q1847/q2087, the d3 next-root fiber compresses
from `32` occurrences to `8` distinct x-roots and then `4` values of
`u=x+1/x`, with `f3=chi(u+2)` on the whole fiber.  But the full norm/product
is always square, power sums through exponent `64` have no exact or near
selector, and the four-u polynomial coefficients are maximal-degree on the
legal-B set.  This makes the reduced 4-u/8-x cover the next CAS object, not a
GPU symmetric-invariant sampler.
The corresponding row-level CAS fixture is
`research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json`.

Plane-relation follow-up:
[P27 B-Line Reduced-Fiber Relation Screen](p27_b_line_reduced_fiber_relation_20260622.md).
The all-cover and f3 plus/minus subcovers have zero extra low-degree relation
through total degree `20` in `(B,u)`, `(B,u^2)`, `(B,u+2)`, `(A,u)`,
`(lambda,u)`, and `(mu,u)`.  Do not widen this as another search lane; the
remaining test is actual normalization/genus/quotient extraction of the
reduced cover.

Symbolic handoff:
[P27 B-Line Reduced-Cover Symbolic Packet](p27_b_line_reduced_cover_symbolic_packet_20260622.md).
It gives the reduced equation
`(Unext - 2*x5)^2 = 4*(x5^2 + A*x5 + 1)` in the B-line source variables and
validates `f3=chi(Unext+2)` with zero mismatches across q1607/q1847/q2087.
This is the first CAS model to try before the full reverse `z,Y` cover.

Online Magma smoke:
[P27 B-Line Reduced-Cover Magma Smoke](p27_b_line_reduced_cover_magma_smoke_20260622.md).
The q7 saturation-only fixture hits the online calculator memory limit during
`Saturation(I,bad)`.  This keeps the reduced cover as the right first offline
CAS object, but it means web Magma cannot answer genus/component/sourceability
for this lane.

Finite-field point-count smoke:
[P27 B-Line Reduced-Cover Point Count](p27_b_line_reduced_cover_pointcount_20260622.md).
The `U_next` layer is exactly two-valued over each legal chart point in the
promotion fields, but the materialized `x6` and selector `gamma^2=U+2` layers
split into B-fibers with `0`, middle, or full lift.  The next offline object is
therefore the reduced cover with those layers attached, not the bare U-cover
and not a GPU bucket.

Visible lift-classifier follow-up:
[P27 B-Line Reduced-Lift Classifier Screen](p27_b_line_reduced_lift_classifier_20260622.md).
The `0/mixed/full` profile is not the sum of two named atoms, two rational
linears, or two monic irreducible quadratic characters on `P1_B` in the
promotion fields.  This kills the nearest low-degree sampler interpretation
of the point-count profile.

Domain reconciliation:
[P27 B-Line Reduced-Domain Reconciliation](p27_b_line_reduced_domain_reconcile_20260622.md).
The frozen legal B fixture equals `legal_b_maps` and sits inside the
point-count chart.  On those legal rows, the selector lift is exactly `0/full`
and matches `d3(B)` with zero mismatches; the mixed point-count fibers are
outside the selected-source legal domain.  CAS must impose that legal/core cut
before interpreting the reduced-cover branch classes.

Second reduced-fiber handoff:
[P27 B-Line Second Reduced-Fiber Fixture](p27_b_line_second_reduced_fiber_20260622.md).
Restricting to legal `f3=+1` B rows, the next selected fiber has `64` x7
occurrences, `16` distinct x7 roots, and `8` values of `v=x7+1/x7` per B,
with `f4=chi(v+2)` in every q1607/q1847/q2087 row.  Stable low-degree
relations in `(B,v)` and `(B,v+2)` are absent through degree `20`, so this is
a concrete f4/f3 CAS class-comparison artifact, not a GPU bucket.

Transition/orientation follow-up:
[P27 B-Line Transition Closure And Orientation](p27_b_line_transition_closure_orientation_20260622.md).
The generic quotient transition from `u` to `v` has `4` v-roots per u-root,
while the actual selected source keeps exactly the `2` with
`chi(v^2-4)=chi(v+A)=+1`.  This visible half is only the lift/materialization
of quotient `v` to actual `x7`; `chi(v+2)=f4(B)` is already constant on the
larger generic transition.  The CAS target should therefore be the staged
cover `F_A(u,v)=0`, `rho^2=v^2-4`, `gamma^2=v+2`, with the question whether
`gamma` is a pullback/coboundary/iterate/low-genus quotient.

Gamma norm/coboundary follow-up:
[P27 B-Line Gamma Norm/Coboundary Boundary](p27_b_line_gamma_norm_coboundary_20260622.md).
The full norm `Norm_4(v+2)=16*(A-2)^2` is square, and the actual/missing
two-root gamma norms are square across q1607/q1847/q2087.  However, the naive
`Norm_2(v+2)=4*x6*(2-A)` formula is false, and screened visible pair
invariants have no exact `f4` predictor through weight `4`.  The remaining
test is therefore an explicit H90 quotient/coboundary computation for
`gamma`, not another norm or pair-invariant scan.

Explicit H90 follow-up:
[P27 B-Line Gamma H90 Quotient](p27_b_line_gamma_h90_quotient_20260622.md).
The quotient is real but collapses: for `r=(v1+2)/(v2+2)`,
`r+1/r=u`, and if `h^2=r`, then `(h+1/h)^2=u+2`.  No visible H90 quotient
product through weight `4` predicts `f4`.  So the next CAS object is `gamma`
as a class over the known f3/H90 layer, not the H90 quotient itself.

F3/H90 layer relation follow-up:
[P27 B-Line Gamma Over F3/H90 Layer Relation Screen](p27_b_line_gamma_f3_layer_relation_20260622.md).
After adjoining both sheets `H=+/-(h+1/h)`, stable pair-coordinate screens do
not expose the `f4` split in `(B,H)`, `(B,tau)`, `(B,H^2)`, or `(B,tau_sym)`.
The triple relations are the tautologies `H^2=u+2` and the Cayley relation
between `H` and `tau`, not gamma source laws.

Required computation:

```text
normalize the reduced 4-u / 8-x legal+d3 cover over P1_B/P1_A/P1_Sroot
include x6^2-U*x6+1 and gamma^2=U+2 in the offline branch/class extraction
impose the selected-source legal/core cut before using all-chart lift buckets
extract branch divisor degree, support field degrees, components, genus
if d3 is tractable, normalize F_A(u,v)=0 plus rho^2=v^2-4 and compare gamma^2=v+2 in the Kummer group
compute the H90 quotient/coboundary for gamma and ask whether it telescopes or recurs
after the quotient collapses to f3, compute gamma over the f3/H90 layer
extract the gamma divisor/Kummer class over the normalized f3/H90 layer
use f5/f6 only as regression checks until larger data supports them
```

Promote if:

```text
genus <= 1
or an explicit sourceable walk/direct sampler appears
or f3,f4,f5 share a pullback/translate/coboundary/iterate relation
```

Kill if:

```text
d3 is high-genus/generic after normalization
and f4/f5 are fresh unrelated half-covers
or online Magma is the only available extraction engine
or the only proposed sampler is the killed visible two-character lift profile
```

This is the top CAS/expert ask because the same active selected bits are now
proven in A, B, K, and Sroot coordinates, not merely fitted buckets.

## Test 2: BSM Staged Legal Pullback

Use:

```text
research/p27/evidence/p27_conic_pair_b_enhanced_pullback_20260622.md
research/p27/evidence/p27_bsm_surface_incidence_20260622.md
research/p27/evidence/p27_bsm_legal_restricted_relations_20260622.md
research/p27/evidence/p27_bsm_next_selector_relation_20260622.md
```

Staging equation:

```text
m^2*(B^2 + s^2 - 4) = 4*s^2*(s^2 - 4)
```

Current pricing:

```text
surface size ~= q^2
canonical d3-plus incidence remains constant/q
legal-B-restricted relation screen finds no extra low-degree selector
d4-plus next-selector screen finds no extra low-degree relation
```

Required computation:

```text
add the legal B-cover/function field to the BSM surface
compute quotient/components/genus after imposing legal B
then add the next Kummer selector and compare with the B-line f_j sequence
```

Promote if:

```text
the staged surface plus legal cover exposes a low-genus quotient
or a direct legal-pullback sampler with better target/source_draw
```

Kill if:

```text
the staged model keeps the same legal-B denominator
and the next selector is a fresh independent half-cover
or BSM only contributes the inherited surface equation
```

This is the best conic-chain CAS coordinate, but not a GPU source by itself.

## Coordinate View: K/Sroot Branch Class

Use:

```text
research/p27/evidence/p27_sroot_prefix_profile_20260622.md
research/p27/evidence/p27_kline_a_map_and_gpu_quad_20260622.md
research/p27/evidence/p27_post_branch_dynamics_test_frontier_20260622.md
research/p27/evidence/p27_ksroot_kummer_fixture_packet_20260622.md
```

Known structure:

```text
Sroot is the cleaner normalization coordinate
selected bits descend to K and Sroot with no mixed groups
Sroot is density-equivalent to K, not a stronger bucket
K/Sroot fixture rows preserve Sroot^2=K explicitly
A/B/K/Sroot fixtures are exact coordinate views of the same classes
```

Required computation:

```text
extract the normalized d3 branch class over P1_Sroot or P1_K
preserve the rational K-square stratum
compare d4/d5 only after d3 is explicit
use f5/f6 only as tail/regression checks unless larger heldout data names a class
cross-check against the B-line class through the fixture bridge
```

Promote if:

```text
the K/Sroot d3 class has genus <= 1
or a rational recurrence/source survives the K-square lift
```

Kill if:

```text
lambda/Sroot structure exists only after forgetting the rational K-square
stratum, or successive classes are unrelated
```

## Test 3: Trace/Norm Half-Norm Phase

Use:

```text
research/p27/evidence/p27_tline_component_descent_20260621.md
research/p27/evidence/p27_hv_trace_coupling_audit_20260621.md
research/p27/evidence/p27_trace_norm_elliptic_line_coset_20260621.md
research/p27/evidence/p27_trace_norm_halfnorm_test_card_20260622.md
```

Ask narrowly for:

```text
a theta/additive/Hilbert-90 identity coupling the h and vq half-norm phases
on E: v^2 = u^3 - u
that reduces to a finite-field squareclass, divisor, or source map
```

Promote if:

```text
the identity predicts a post-Dplus selected gate
or gives a direct sampler/source map
or gives >=1.25x heldout target/source_draw lift with raw-source accounting
```

Kill if:

```text
it reduces to already-killed visible branch/norm squareclasses
or only rederives the first fixed half-gate
```

This is the cleanest expert/literature ask, not a broad "anything relevant"
request.

## GPU Boundary

Run GPU now only for bounded telemetry or for a named sampler:

```text
allowed:
  A/B/K/Sroot deep-prefix telemetry with d3..dN emitted same-stream
  recurrence sign-word telemetry with raw source denominator reported
  direct sampler A/B test after CAS names a sampler/source map

not allowed:
  large p27 production run from fixed quadratic precheck
  A/B/K/lambda quartic bucket production
  raw BSM surface sampling
  Bplus/core-B bucket search without a class recurrence
  GPU production before reduced-cover genus/sourceability is known
```

GPU promotion requires:

```text
>=1.25x held-out target/source_draw lift
or target/GPU-second lift with the same denominator
or exact direct sampling into a named source stratum
```

## Continue / Kill

```text
continue = coordinated A/B/K/Sroot normalized Kummer sequence extraction
continue = BSM staged legal-pullback normalization
continue = trace/norm half-norm phase expert ask
continue = GPU only as bounded telemetry or for a named sampler
continue = offline Magma/Sage for the reduced B-line cover
continue = offline Magma/Sage comparison of the second reduced f4/f3 cover

kill = more one-bit filters as moonshots
kill = norm/trace/power-sum selectors for the B-line d3 fiber
kill = low-degree plane relations for the reduced B-line d3 fiber through degree 20
kill = low-degree plane relations for the second reduced B-line f4/f3 fiber through degree 20
kill = treating chi(v^2-4) or chi(v+A) materialization as a GPU/source win
kill = naive gamma norm or visible pair-invariant predictors as source laws
kill = explicit H90 quotient as a standalone f4 source law
kill = visible f3/H90-layer pair-coordinate source laws for gamma
kill = online Magma as the reduced-cover extraction engine
kill = more visible quartic/branch-map bucket searches without a theorem
kill = treating source-conditional 2x lift as sqrt-beating
```

```text
p27_first_class_moonshot_tests_after_quad_rows=1/1
```
