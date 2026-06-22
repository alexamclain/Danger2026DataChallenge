# P27 First-Class Moonshot Tests After Quadratic Probe

Date: 2026-06-22

## Claim

After the GPU quadratic-gate result and the q1847 B/K quartic closures, the
p27 moonshot should not spend a large GPU run on another fixed one-bit filter.
The remaining tests that could beat `sqrt(p)` are source or class tests:

```text
1. B-line Kummer sequence extraction on P1_B.
2. BSM staged legal-pullback normalization.
3. K/Sroot normalized branch-class extraction.
4. trace/norm half-norm phase identity.
5. bounded GPU telemetry only when it feeds one of the above.
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

These results do not kill the B/K/A/Kummer routes.  They kill the nearby
coefficient buckets and map-family shortcuts.

## Test 1: B-Line Kummer Sequence

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

Required computation:

```text
normalize the legal+d3 cover over P1_B in q1607/q1847/q2087
extract branch divisor degree, support field degrees, components, genus
if d3 is tractable, compare f4/f3 in the Kummer group
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
```

This is the top CAS/expert ask because B is already proven to carry the active
selected bits, not merely a fitted bucket.

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

## Test 3: K/Sroot Branch Class

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
B/K/Sroot fixtures are exact coordinate views of the same classes
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

## Test 4: Trace/Norm Half-Norm Phase

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
  B-line deep-prefix telemetry with Bplus and d3..dN emitted same-stream
  recurrence sign-word telemetry with raw source denominator reported
  direct sampler A/B test after CAS names a sampler/source map

not allowed:
  large p27 production run from fixed quadratic precheck
  B/K/lambda quartic bucket production
  raw BSM surface sampling
  Bplus/core-B bucket search without a class recurrence
```

GPU promotion requires:

```text
>=1.25x held-out target/source_draw lift
or target/GPU-second lift with the same denominator
or exact direct sampling into a named source stratum
```

## Continue / Kill

```text
continue = B-line normalized Kummer sequence extraction
continue = BSM staged legal-pullback normalization
continue = K/Sroot branch-class extraction preserving K-square rationality
continue = trace/norm half-norm phase expert ask
continue = GPU only as bounded telemetry or for a named sampler

kill = more one-bit filters as moonshots
kill = more visible quartic/branch-map bucket searches without a theorem
kill = treating source-conditional 2x lift as sqrt-beating
```

```text
p27_first_class_moonshot_tests_after_quad_rows=1/1
```
