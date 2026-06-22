# P27 Live Sqrt-Beating Queue

Date: 2026-06-21

## Claim

After the alpha branch and K/S first-half cover screens, the p27 moonshot has
three live test surfaces.  They should be treated differently:

```text
1. K/S saturated first-half cover: live only as quotient/decomposition work.
2. Trace/norm half-norm phase coupling: live theorem/expert front.
3. GPU conic-chain telemetry: useful for exact recurrence checks and legal
   pullback sources, but raw random `(R,L)` is killed as production.
```

Do not restart broad visible-character scans.  Do not promote a fixed prefix
filter as sqrt-beating unless it gives a source, recurrence, or scope shrink
that compounds beyond constant factors.

## Current K/S Status

The K/S route is no longer a low-genus direct source candidate.

Latest evidence:
[P27 K/S First-Half Cover Magma Smoke](p27_ks_first_half_cover_magma_20260621.md).
[P27 K/S First-Half Alpha-Lift Obstruction](p27_ks_first_half_alpha_lift_obstruction_20260621.md).
[P27 K/S First-Half E-Prime Descent](p27_ks_first_half_eprime_descent_20260621.md).
[P27 E-Prime First-Half Pullback Magma Smoke](p27_eprime_first_half_pullback_magma_20260621.md).
[P27 E-Prime D3 Z-Source Magma Smoke](p27_eprime_d3_zsource_magma_20260621.md).
[P27 E-Prime L(4O) Exact Section Screen](p27_eprime_l4_section_exact_screen_20260621.md).
[P27 E-Prime U-Cubic Exact Screen](p27_eprime_ucubic_exact_screen_20260621.md).
[P27 E-Prime Reciprocal R-Quotient Branch Screen](p27_eprime_rquotient_branch_screen_20260621.md).
[P27 S-Map Quartic Recurrence Probe](p27_smap_quartic_recurrence_20260621.md).
[P27 Quadratic Gate Recurrence](p27_quadratic_gate_recurrence_20260621.md).
[P27 Conic-Chain Source Screen](p27_conic_chain_source_screen_20260621.md).

Key result over tiny p27-signature field `q=7`:

```text
raw first-half scheme:
  SCHEME_OK 2 4
  AFFINE_POINTS 77

saturated eta=+1 first-half layer:
  SAT_SCHEME_OK 1 42 3
  SAT_CURVE_OK 37 3
```

Interpretation:

```text
The unsaturated handoff has denominator/projection artifacts.
After saturating by X*(X-1)*(X+1)*(T-2X^2), the layer is a genus-37 curve.
This occurs before adding the final reverse-square variables z,Y.
The first-half B-branch factors cleanly, but the same-eta alpha lift ratio is
exactly -1 times a square. Since p27 is 3 mod 4, the natural alpha quotient is
not F_p-rational; the eta-swapped ratio is mixed on q=1607,1847,2087.
In contrast, translation by (0,0) descends the T-cover by T -> +/-T/X^3 and
preserves compactD plus the first-half B-branch squareclass on q=1607,1847,2087.
But the explicit E' first-half pullback still has genus 37 over q7 after
saturation, so E' is a quotient/extraction surface, not a direct source yet.
The actual d3 z-source can be staged as `J = Iclean + <reverse_z>` after
first-half saturation; q7 online Magma reports a dimension-1 scheme with
62 basis polynomials, but genus/normalization exceeds the web memory limit.
Exact single-section tests in `L(4O)=<1,U,U^2,V>` are killed on q599/q727/q919;
q487 exact quadratic-U fits are local artifacts.
The same exact single-section test on the original residual
`E: W^2=X^3-X`, with basis `L(4O)=<1,X,X^2,W>`, is also killed:
q487/q599/q727/q919/q1607 have zero d3 sections, and q1607 has zero
non-degenerate d4 sections.  This closes the cheap low-pole E-section gap.
Exact U-cubic tests also fail on q919/q967/q1063, despite local q487/q599/q727
artifacts, so widening univariate U-polynomials is no longer a live source path.
The reciprocal quotient `r=z^2+z^-2` is real, but it is not the selector:
on p27 train/heldout and q1607/q1847/q2087, the r-quadratic discriminant is
always square and the remaining bit is exactly `d3=chi(r+2)=chi(r-2)`.
The first recurrence model for `r+2` is explicit: with `r=S^2-2`, one more
all-plus step gives a quartic `F(Y)` in `Y=S_next^2`.  Guard fields show four
`Y` roots on every d3-plus row, and either all four are squares or none are;
this common root squareclass is exactly d4.  The nearby split class
`chi(S^2+A-6)` and named quartic-factor span are flat on p27 heldout.
The pair resolvent then collapses the tower to a repeated conic gate.  In
coordinates `A=2-c^2`, `x=r^2`, the next gate is exactly
`chi(r^2+c*r+1)`.  This matched p27 train/heldout through gates 3-8 and
q1607/q1847/q2087 through gates 3-4, all with zero mismatches.
The lifted legal conic-chain object is also dimension-stable in first probes:
with both conjugate conics and the transition
`r_next^2-(h+g)r_next+1=0`, q7 Magma gives dimension 2 at depths 1 and 2,
and finite-field counts through depth 4 keep output projections near `0.5q^2`
with zero xDBL mismatches.
On legal label-2 / compactD rows over q1607/q1847/q2087, depth-1 conic lifts
match exactly the d3-plus rows, and depth-2 lifts match exactly d4-plus after
d3.  The full q7 E-prime pullback still exceeds web Magma memory.
The direct rational conic-pair sampler now has a legal-incidence screen:
it covers every legal d3-plus `(A,x5)` class tested and no d3-minus classes,
but random `(R,L)` hits legal rows at only about `constant/q` per draw.  This
kills the naive free two-dimensional GPU sampler while strengthening the legal
pullback/quotient target.
The d4 selector is now exact in conic-pair coordinates:
with `a=R-1/R` and `L=h-g-2r`,
`d4 = chi(-(L+a)(L-a)cR)`.  The quotient from the tautological conic
`R^2+cR+1` is `2` times a square, so this is valid in the p27 `chi(2)=+1`
regime.  The selected next coordinate does not re-enter the original legal
source in q1607/q1847/q2087, so the live route is the legal pullback plus this
new Kummer divisor, not direct iteration.
The d5 screen confirms this is a repeated tower identity: after adjoining the
d4 selector root, the same product law gives d5 with zero mismatches on
q1607/q1847/q2087 and p27 train/heldout samples.  The source-side obstruction
remains unchanged: selected two-step coordinates also do not re-enter the
original legal source.
The legal depth screen confirms the other half: conic-chain lift existence
matches selected-prefix bits through depth 4, but p27 train/heldout prefix
rates still thin roughly like successive half-gates.  So the tower is exact,
not yet sqrt-beating without a quotient/source for the tower itself.
The raw `(R,L)` quotient screen is negative through total degree 20 on
q1607/q1847/q2087.  The legal d3-plus preimages are not a small plane curve in
the free sampler parameters, so the live quotient search must use tower/Kummer
variables rather than raw `(R,L)` alone.
The follow-up invariant-coordinate screen is also negative through degree 20
in the obvious pair systems: `(A,x)`, `(c,r)`, `(r,d)`,
`(R+1/R,L+a^2/L)`, `((R-1/R)^2,L+a^2/L)`,
`(R+1/R,(L+a)(L-a))`, and related pairs.  q1847/q2087 have no extra nullity;
the only q1607 degree-20 artifact does not repeat.  This kills the cheap
"maybe the quotient is a plane curve after symmetrizing" path.
The first Kummer-root layer is now screened as well.  After adjoining
`Z^2=-(L+a)(L-a)cR`, all obvious pairs involving `Z` are full-rank through
degree 20 except `(A,Z)`.  The `(A,Z)` relation extracts to a univariate
polynomial in `A`, plus its product with `Z`; it is the finite A-projection of
the selected small-field rows, not a Kummer-root quotient.  The A-projection
count grows at constant-density small-field scale, so this is not a p27 source.
The direct A-projection prefix profile confirms the demotion.  On 3,000-row
p27 train/heldout samples through depth 8, unique `A` and unique `(A,x)` shrink
in exact lockstep, with scaled half-loss near `1` and `avg_x_per_A=2` at every
depth.  There is no A-bucket source hiding behind the selected prefixes.
The K-line cubic pilot now has a reusable solver:
[P27 K-Line Cubic Stdin Probe](p27_kline_cubic_stdin_probe_20260622.md).
It reproduces the q607 negative hardcoded pilot, finds many exact q863 cubics,
and then finds no q991 cubic.  This field-to-field instability kills q863
exact cubics as source candidates and reinforces the rule that K-line
promotion needs branch-cover/genus extraction in q1471/q1607/q1847, not
small-field interpolation fits.
The fit-significance calibration makes this quantitative:
[P27 K-Line Fit Significance](p27_kline_fit_significance_20260622.md).
q863 d3 monic cubics have `expected_exact ~= 76.6`, while q1471/q1607/q1847
d3 monic cubics have expected exact counts `5.65e-6`, `1.47e-5`, and
`1.37e-9`.  Thus a stable d3 low-degree fit in the promotion fields would be
meaningful; q863 fits and q1471/q1607 d4 fits are not enough.
The first promotion-field cubic test is now complete:
[P27 K-Line q1471 Cubic Promotion Screen](p27_kline_q1471_cubic_promotion_screen_20260622.md).
It exhausts all `3,183,010,111` monic cubics over q1471 and finds no exact d3
cubic.  Since degree <=2 was already killed, this removes `z^2=cubic(K)` as a
K-line source candidate.  Continue with quartic/branch-cover/genus extraction.
The extension-field source count now gives a staged-geometry substitute for the
memory-heavy online Magma pullback.  Over `GF(7^n)` and `GF(23^n)`, the legal
label-2/compactD source is curve-sized, but selected prefixes still reduce
unique `A` and `(A,x)` together.  Local Frobenius tails occur, but they do not
look like p27 source laws.
The reverse-root extension count now sharpens the K/S projection itself.
Across q607, q1607, q1847, q2087, and nonempty `GF(7^n)`/`GF(23^n)` guard
fields, the actual d3 all-plus cover has constant fibers
`z_rows/unique_K=64`, `z_rows/unique_S=32`, and `unique_Ax/unique_A=4`.
This makes K/S a real branch-extraction target, but `unique_K` and `unique_S`
still grow at field-size scale, so K/Sroot enumeration is not a below-sqrt
source and should not become a GPU bucket search.
The fiber-profile follow-up is completely flat in q1607/q1847/q2087: every K
fiber has 64 rows and one selected A, while every Sroot fiber has 32 rows and
one selected A; all tracked fiber histograms have zero anomalous fibers.  This
promotes Sroot as the cleaner CAS coordinate and kills rational-fiber anomaly
search as a source of sqrt beating.
The K/A graph is now explicit.  With `L=K^2`, all d2-plus rows satisfy
`64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0`, with
discriminant `256(A+2)(A+6)^2(A^2+60A+132)^2`.  This is the first-half source
identity, not the d3 selector: p27 train/heldout and q607/q1607/q1847/q2087
show formula-zero on both d3-plus and d3-minus rows.
The GPU quadratic-gate pass then validated the recurrence formula
`chi(r_j^2+c*r_j+1)` at scale, with `7,874,715` checked gates and zero
mismatches across gates 3-8.  It still did not improve source-normalized
target rate, because the recurrence-coordinate domain costs about the same
factor that it recovers conditionally.
The CPU sign-word follow-up is also negative as a promotion signal:
[P27 Conic Sign-Word Coupling Probe](p27_conic_signword_coupling_20260622.md).
On `4000 + 4000` p27 train/heldout unique `(A,x5)` rows, all-plus conic
prefixes have scaled half-loss near `1` through meaningful counts; the late
heldout depth-14 survivor tail has only two rows.  q1607/q1847/q2087 show
local plateaus, but their kill gates disagree.  This kills GPU sign-word
bucket hunting from short conic words alone; use GPU only for much larger
bounded confirmation or for a direct legal-pullback sampler.
The A-line named-transform follow-up is also negative:
[P27 A-Line Named-Transform Recurrence Screen](p27_a_line_named_transform_recurrence_20260622.md).
The visible S3 transforms preserving `A in {-2,2,infinity}` do not preserve
the selected A-domain or relate successive selected gates.  q1847 has zero
non-identity d3 coverage, while p27 train/heldout have zero non-identity
d3..d8 coverage.  This kills visible A-orbit and branch-S3 recurrence
shortcuts; continue only with normalized-cover/Kummer-class extraction.
The broader affine A-line recurrence screen is negative too:
[P27 A-Line Affine Recurrence Screen](p27_a_line_affine_recurrence_screen_20260622.md).
No full-coverage affine map `A -> m*A+b` carries `d3` to `d4` in
q1607/q1847/q2087; best full-coverage maps are identity and only score the raw
d4 bias.  Later exact identity maps occur only in one-sided small-field tails
with field-dependent signs.  Thus an A-line source law must be a normalized
Kummer-class relation, non-affine correspondence, or coboundary, not a
degree-one recurrence.
The full PGL2 version is negative too:
[P27 A-Line PGL2 Recurrence Screen](p27_a_line_pgl2_recurrence_screen_20260622.md).
Every full-coverage degree-one rational map
`A -> (aA+b)/(cA+d)` is tested for `d3 -> d4`; q1607/q1847/q2087 all have zero
exact recurrences.  The next A-line correspondence test should be higher
degree or theorem-specified, not another rational line map.
The B/K-enhanced legal-pullback screen gives one positive staging coordinate:
[P27 Conic-Pair B/K-Enhanced Pullback Screen](p27_conic_pair_b_enhanced_pullback_20260622.md).
It finds the expected `B^2+c^2=4` and the stable surface
`m^2*(B^2+s^2-4)=4*s^2*(s^2-4)`, where `s=R+1/R` and `m=L+a^2/L`.
All direct `(B,R)`, `(B,L)`, `(K,R)`, `(K,L)`, and `(B,R,L)` shortcuts remain
full-rank.  This is a CAS staging win, not a source sampler: the legal B-domain
still has to be imposed.
The incidence follow-up confirms the denominator:
[P27 BSM Surface Incidence Probe](p27_bsm_surface_incidence_20260622.md).
The BSM surface is about `q^2`-sized in q1607/q1847/q2087 and hits canonical
d3-plus `(B,A,x)` rows at `constant/q` density.  It captures the d3-plus side
when a canonical legal row is already present, but does not source the sparse
legal B-domain.
The legal-B-restricted relation follow-up closes the nearest loophole:
[P27 BSM Legal-Restricted Relation Screen](p27_bsm_legal_restricted_relations_20260622.md).
After restricting the BSM surface to legal B values, q1607/q1847/q2087 show no
extra target relation in `(B,s)`, `(B,m)`, or `(s,m)` through degree `12`, and
the only degree-4 relation in `(B,s,m)` is the inherited BSM equation shared by
the legal surface and target subset.  So legal-B BSM is still CAS staging, not
a GPU source or bucket law.
The base-curve sampler test is negative.  In q1607/q1847/q2087 the base curve
has exactly `q` affine `(K,A)` points and contains every realized legal d2
point, but only `49/1607`, `63/1847`, and `57/2087` base points are realized
by the legal source.  Natural K/A squareclass atoms up to weight 4 do not pick
out the legal subset.  So the base curve is a CAS coordinate, not a direct GPU
sampler.
The online Magma q607 validation now confirms the base model itself:
[P27 K/A Base-Curve Magma Validation](p27_ka_base_curve_magma_validation_20260622.md).
It checks `base_KA=607`, nondegenerate B-chart coverage `604`, exactly three
expected B-degenerate missing points, no spurious B-chart points, and zero
equation/discriminant mismatches.  This pushes the live question entirely onto
the additional legal/d3 cover over the base.
The B-parameter follow-up is a real but only constant-factor improvement.
After adjoining `B` with `A=B^2-2`, all realized d2 and d3plus rows in
q1607/q1847/q2087 lie in a stable bucket for `K`, `B+2`, `B-2`, and `L=K^2`;
the bucket has about `8.04x` all-recall lift in each promotion field.  This is
worth bounded GPU telemetry if the four bits are cheap to emit, but it is not
a production source because the surviving bucket is still field-sized and the
sharper partial buckets vary by field.
The direct next-gate B-atom follow-up is negative.  On actual legal d2 rows,
the core B bucket remains exact, but B/K/A atom products do not stably predict
`d3` or `d4`: p27 train fits weaken or reverse on heldout, and guard-field
winners disagree.  This kills B-bucket GPU scoring as a moonshot route and
reframes the live B test as function-field/CAS extraction of the legal cover
over the rationalized base.
The B quotient itself is now explicit and positive: on the residual source,
`A+2=(8X^2/(X^2-1)^2)^2`, and `d3` descends to
`B=8X^2/(X^2-1)^2` on legal d2 rows in p27 train/heldout and
q1607/q1847/q2087.  `d4` after d3 also descends to B in the tested samples.
The nearest branch-support screens are negative: no degree-<=4 rational-linear
support for d2 or d3 on the B-line, no d3 support of the form one irreducible
quadratic times <=2 rational linears, and no two-irreducible-quadratic support
for d3 or the legal B-domain in the promotion fields.  The exact monic cubic
screen is now negative too: q1607/q1847/q2087 have zero cubics for both the
legal B-domain and `d3(B)`, while d4 local cubics fail at q1847.  So the live
B test is now exact Kummer-class/divisor extraction on `P1_B`, not another
visible low-degree support scan.
The combined-prefix cubic loophole is also closed: no monic cubic on `P1_B`
selects the gate4 all-plus prefix in q1607/q1847/q2087, and the q1607/q2087
gate5 plateau subsets also have zero exact cubics.  This kills the direct
genus-1 "one source for multiple B gates" shortcut in the visible cubic family.
The B-line degree-one rational recurrence loophole is now closed too:
[P27 B-Line PGL2 Recurrence Screen](p27_b_line_pgl2_recurrence_screen_20260622.md).
Every full-coverage PGL2 map `B -> (aB+b)/(cB+d)` was tested for
`d4(B)=+/-d3(phi(B))` in q1607/q1847/q2087; exact recurrences are zero, and
the best full-coverage maps are identity/raw d4-bias baselines.  This keeps
the live B-line target on extracted Kummer classes `f3,f4,f5,...`, not
degree-one B-map fitting.
The B-line result is now multi-gate: extension counts over `GF(7^n)` and
`GF(23^n)` keep legal B inside the core bucket with no d3/d4 mixed groups,
while p27 train/heldout deep-descent probes show no mixed B groups through
`d12`.  Counts remain field-sized, so this is not a sampler by itself.  The
moonshot target is the sequence of B-line Kummer classes
`f3(B), f4(B), f5(B), ...`; a recurrence or coupling among those classes is
the first credible way for this lane to beat independent sqrt-scale half-loss.
The larger p27 scaling follow-up strengthens and limits that claim:
[P27 B-Line 60K Prefix Scaling](p27_b_line_prefix_scaling_60k_20260622.md)
has zero mixed B groups through `d18` on `60000 + 60000` rows, but the
source-normalized all-plus prefix rates stay near geometric half-loss through
the meaningful `d3..d12` range.  Any apparent later lift is a tiny tail and
does not transfer cleanly.  This pushes B-line work toward Kummer/divisor class
extraction, not GPU B-bucket production.
The first B-line Magma staging smoke says how to pursue that extraction:
q7 legal-cover saturation over `P1_B` succeeds as a dimension-1 scheme with
93 basis polynomials, but online point/curve/component extraction and the full
legal+d3 fixture both return `504 Gateway Timeout`.  So use offline
Magma/Sage or targeted elimination for B-line class extraction; online Magma is
only a syntax/saturation sanity check here.
The bounded visible quartic family has now been tested in the decisive q1847
d3 case:
[P27 B-Line Quartic GPU Test Card](p27_b_line_quartic_gpu_test_card_20260622.md).
[P27 Full Quartic q1847 D3 Screen](p27_full_quartic_q1847_d3_screen_20260622.md).
Exact monic quartic support on `P1_B` would have given a genus-1 double-cover
source candidate for `d3_on_legalB`; the full q1847 screen found zero exact
quartics across `6,300,872,423` coefficient triples.
The parallel K-line quotient test is negative in the same decisive field:
[P27 K-Line Quartic GPU Test Card](p27_kline_quartic_gpu_test_card_20260622.md).
Exact monic quartic support on `K=x([2]P)` for `d3_on_K` over q1847 also found
zero exact quartics across `6,300,872,423` coefficient triples.  Since q1847
has expected random exact count about `2.52e-6`, this kills the visible
monic-quartic d3 promotion route in both B and K coordinates.
The bridge between the two line coordinates is exact:
[P27 B-Line / K-Line Bridge](p27_b_kline_bridge_20260622.md).
Under `K^2=(B-2)^4/(8B(B+2)^2)`, every B d3/d4 row maps to a present signed K
class with matching target sign in q1471/q1607/q1847/q2087.  So B-line and
K-line quartics were coordinated coordinate tests for one descended class, not
independent moonshot lanes.
The signed-root shortcut over this bridge is negative:
[P27 B/K Signed-Root Relation Screen](p27_b_kline_signed_root_relation_20260622.md).
The selected K sheet has no positive extra low-degree relation in `(B,K)`
beyond the bridge cover, so the root choice itself is not a simple plane-curve
sampler.
The first targeted B-line elimination proxy is negative:
[P27 B-Line Reverse-Z Relation Screen](p27_b_line_reverse_z_relation_20260622.md).
It keeps the actual d3 all-plus reverse-source root `z` with `x6=z^2` and
tests `(B,z)`, `(B,x6)`, `(B,r)`, `z+/-1/z`, Belyi-normalized B coordinates,
and branch-normalized `z` coordinates.  The main systems are full-rank through
degree 20 in q1607/q1847/q2087; a 1,000-row p27 sample is full-rank through
degree 12.  The only extra-nullity rows are q1607-only degree-20 artifacts in
compressed `z+/-1/z` projections and do not repeat.  This kills the obvious
B-line reverse-root plane-model sampler and leaves actual normalization /
branch-divisor / genus extraction over `P1_B`.
The B-line prefix profile now gives the next verdict:
[P27 B-Line Prefix Profile](p27_b_line_prefix_profile_20260622.md).  Exact
small fields show late all-plus plateaus, but the plateau/kill gate changes
with the field.  On p27 itself, a `4000 + 4000` B-group train/heldout run
through `d16` thins essentially by independent half-gates through the useful
range.  This keeps B as a Kummer-class extraction surface but kills Bplus
bucket counts as a direct scope-shrink or production GPU reason.
The two-step Kummer quotient screen is now negative too.  After adjoining the
first root `Z0`, the next selector `S1`, and when available the second root
`Z1`, all obvious selector/root pair systems are full-rank through degree 12 on
q1607/q1847/q2087.  This kills simple `(Z0,S1)`, `(Z0,Z1)`, normalized-root,
ratio, and product quotients as the next shortcut.
The trivariate follow-up is also negative through degree 6 for the obvious
`A/R/L/S1/Z0/Z1` triples.  This kills the next cheap GPU-bucket idea after
pair relations; further progress needs staged components or a named theorem
coordinate.
```

Concrete next K/S test:

```text
offline Magma/Sage should now target the explicit base curve:
  64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0
  with L=K^2 and K=Sroot^2
then add the d3 reverse-root cover and compute branch/genus data over P1_Sroot
```

Promotion bar:

```text
genus <= 1 quotient, named recurrence/sourceable walk, or cheap sampler
surviving p27-signature guard fields
```

Kill condition:

```text
no low-genus quotient of the genus-37 layer, or d4 is a fresh unrelated cover
no F_p descent of the sqrt(-1)-twisted alpha quotient
no useful low-genus/function-field structure for the conic-chain pullback
another low-degree plane-curve screen in raw or obvious invariant coordinates
another simple first-Z-layer pair scan without a new theorem-specified coordinate
another simple two-step Kummer pair scan in `Z0,S1,Z1` coordinates
another ad hoc two-step Kummer trivariate bucket scan without a new coordinate
K-line affine or reciprocal-affine recurrence scans
K/Sroot reverse-root plane relation scans in `z`, `x6`, `r`, or `z +/- 1/z`
K/Sroot bucket searches based only on the constant-fiber extension counts
rational K/Sroot fiber-anomaly searches
direct GPU sampling of the K/A base curve
an A-projection or A-bucket search based only on selected-prefix filters
raw selected-prefix source enumeration based on extension-field tail artifacts
```

## Current Alpha Status

The alpha/order-4 geometry is understood but not a selector.

Latest evidence:

```text
P27 Label-2 Alpha Projective Quotient Smoke
P27 Alpha Branch-Class Screen
```

Key results:

```text
D/<alpha> is the residual elliptic curve E
degree(C -> E) = 4
ramification degree = 32
alpha group order = 4
visible branch squareclass = T2
T2 is already square on all active d3/d4 rows tested
```

Concrete next alpha test:

```text
only continue alpha inside the K/S or trace/norm quotient/decomposition work
```

Kill condition:

```text
more alpha branch-atom products or T/T-deck/branch-choice selectors
```

## Current Trace/Norm Status

Trace/norm remains structurally live because it describes the early selected
gates exactly, but the visible products are killed.

Known facts:

```text
Dplus = exact two-gate prefix
post-Dplus d3/d4 rates are random-looking
full orientation source cover prices at genus 69
low-weight post-Dplus H/VQ/X/T_line/root products failed
```

Concrete next trace/norm test:

```text
derive or ask for a non-visible half-norm / theta / additive identity on
E: v^2 = u^3-u that couples the two same-boundary Hilbert-90 sign objects
pref and h*vq
```

A useful expert ask is:

```text
On C: b^2=16-a^4, or E: v^2=u^3-u, is there a theta/additive/Kummer identity
for the descended quotient of pref and h*vq whose boundary under
sigma(t)=-1/t is -chi(a), and whose product gives the normalized T_line
selector?
```

Promotion bar:

```text
named formula with zero mismatches on p27 rows
plus a source/enumeration method for the selected stratum cheaper than sqrt(p)
```

Kill condition:

```text
identity only rederives visible norm/branch squareclasses already screened
```

## Current GPU Status

GPU is valuable now for a bounded structure test, but current math does not
yet justify a new large p27 production run as a moonshot.

Concrete GPU tests if used:

```text
1. conic-chain recurrence telemetry:
  next_gate = chi(r_j^2 + c*r_j + 1)
  expected mismatch count = 0

2. direct one-step pair sampler:
  a = R - 1/R
  s = R + 1/R
  d = (L - a^2/L)/2
  r = -(L + a^2/L)/4
  h = (s + d)/2
  g = (s - d)/2
  c = s*d/(2*r)
  killed as free random (R,L) production by legal-incidence rate ~constant/q
  continue only as a legal-pullback sampler

3. same-stream practical controls:
  baseline raw X1(16)
  ecover first-lift source
  domain/dgate control
  optional Dplus telemetry

report:
  raw source draws/sec
  accepted roots/sec
  depth-20/24/26 survivor rates per source draw
  d3/d4 rates inside Dplus, ecover, and domain strata
```

Promotion bar:

```text
at least 1.25x target/source_draw or effective deep-survivor/sec improvement
on heldout streams, direct sampler into a named source stratum, or two-step
chain evidence that avoids a fresh independent half-loss
```

Kill condition:

```text
fixed-prefix filters give only constant factors and no recurrence/source
conic-pair sampler does not pull back to legal rows at useful rate
raw free (R,L) remains the only conic-pair source
```

## Current Recommendation

Ranked next moves:

```text
1. Theory/CAS: staged legal pullback / quotient decomposition of the repeated
   conic-chain Kummer tower with Z_j^2=-(L_j+a_j)(L_j-a_j)c*r_{j+1}.
2. Theory/CAS: exact E/E' or B-line divisor/Kummer class extraction for
   d3/d4, with class comparison rather than visible-factor scans.
3. Theory/lit/expert: trace/norm half-norm phase identity for pref vs h*vq.
4. GPU/structure: bounded recurrence telemetry and legal-pullback sampler
   only; no raw `(R,L)`, no simple two-step bucket searches, and no Bplus-only
   production run.
```

The conic-chain CAS ask is now packaged as
[P27 Conic Tower Quotient CAS Handoff](p27_conic_tower_quotient_cas_handoff_20260622.md).
Its first sign-quotient sanity screen is
[P27 Conic Tower Sign-Quotient Probe](p27_conic_tower_sign_quotient_20260622.md):
the obvious sign quotient is selector-preserving but only a finite cover, not
a source shrink.
The continuation screen
[P27 Conic Tower D6 A-Descent](p27_conic_tower_d6_a_descent_20260622.md)
adds the current sharpest conic test: d6 also descends to A on p27
train/heldout after d4-plus/d5-plus.  The next concrete sqrt-beating attempt is
not GPU buckets; it is A-level Kummer class extraction for d4/d5/d6, looking
for a repeated low-genus class, coboundary, or recurrence.
The cheap deeper sanity check
[P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md)
extends the positive side: d3..d14 all have zero mixed A groups on `12000 +
12000` p27 train/heldout samples.  The negative side remains decisive for
operations: counts stay near geometric half-loss, so this is class-extraction
evidence, not a source-space shrink.
The first A-character falsifier
[P27 A-Line Character Support Screen](p27_a_line_character_support_20260622.md)
kills visible degree `<= 4` branch support for d3 in q1607/q1847/q2087 and
for d4 in q1847, with nearby-field split-support negatives.  The live conic
task is now normalized A-cover divisor/Kummer class extraction, not wider
low-degree A polynomial scans.
[P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)
is the concrete CAS handoff for that task: it emits q1607/q1847/q2087
A-labeled d3/d4 fixtures and the promote/kill criteria for normalized A-cover
class extraction.  The affine recurrence falsifier means the next A-line
correspondence test should be theorem-shaped, not another degree-one or PGL2
map scan.

The compact actionable version is the "Current Priority After Two-Step Kummer
Screen" section of
[P27 Next Sqrt-Beating Test Cards](p27_next_sqrt_beating_test_cards_20260621.md):
Test A staged legal pullback normalization, Test B direct `E/E'` double-cover
class extraction, Test C bounded GPU legal-pullback telemetry only after a
legal sampler exists, and Test D the trace/norm half-norm phase identity.

The clearest possible sqrt-beating win would now be:

```text
a low-genus quotient or recurrence that controls many selected chi(u_j+2)
or chi(d_j) gates at once
```

The clearest falsifier would be:

```text
K/S genus-37 layer has no useful quotient and trace/norm phase identities
reduce only to already-killed visible branch/norm classes
```

```text
p27_live_sqrt_beating_queue_rows=1/1
```
