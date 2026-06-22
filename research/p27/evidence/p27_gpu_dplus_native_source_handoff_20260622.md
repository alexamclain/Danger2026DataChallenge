# P27 GPU Dplus-Native Source Handoff

Date: 2026-06-22

## Claim

The next useful GPU task is not a large blind p27 production run.  It is a
bounded exchange-rate test for the one trace/norm structure that still looks
real:

```text
Dplus = exact first-two-selected-gate prefix
observed conditional scope shrink = about 4x
current problem = the classifier pays to inspect rejected raw-y draws
```

The GPU agent should test whether this `4x` scope shrink can be accessed
cheaply, and whether any fused/native implementation exposes later-gate
coupling beyond the first two gates.

This is not claimed to be sqrt-beating by itself.  It becomes relevant to the
sqrt-beating goal only if it either:

```text
1. gives a genuinely cheaper direct source into Dplus plus later gates, or
2. reveals a recurrence/class that controls gates after Dplus.
```

## Evidence To Treat As Baseline

Read these first:

```text
research/p27/evidence/p27_gpu_search_space_narrowing_20260621.md
research/p27/evidence/p27_trace_norm_dplus_prefix_identity_20260621.md
research/p27/evidence/p27_trace_norm_post_dplus_screen_20260621.md
research/p27/evidence/p27_trace_norm_orientation_phase_screen_20260622.md
research/p27/evidence/p27_trace_norm_dplus_cover_20260621.md
research/p27/evidence/p27_trace_norm_source_orientation_cover_20260621.md
research/p27/evidence/p27_trace_norm_dplus_quotient_symmetry_20260622.md
research/p27/evidence/p27_trace_norm_dplus_relative_descent_20260622.md
research/p27/evidence/p27_trace_norm_dplus_h90_quotient_20260622.md
research/p27/evidence/p27_trace_norm_dplus_h90_quartic_model_20260622.md
research/p27/evidence/p27_trace_norm_dplus_h90_branch_class_20260622.md
research/p27/evidence/p27_trace_norm_dplus_h90_payload_screen_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_h90_u_cubic_quartic_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_local_magma_factor_split_20260622.md
research/p27/evidence/p27_trace_norm_dplus_u6_rowbit_factor_label_20260622.md
research/p27/evidence/p27_trace_norm_elliptic_line_divisor_screen_20260622.md
```

Do not retest these killed routes:

```text
fixed d2/d3/d4 prefix buckets as raw source shrink
low-weight H/VQ/X/T_line/root character products
eps_h/eps_v, H/VQ, eps_h/eps_v/T_line orientation buckets
low-weight tested a/g/m quotient-character products
bare conic quotient a^2+g^2=4 as a standalone Dplus sampler
H90 elliptic quotient alone as a Dplus sampler
H90 eta/U/W/rho payload sign buckets as production filters
visible E_h90/Z/Aeta row-bit product characters
small H90 elliptic group-coset buckets for the row bit
small elliptic line-divisor buckets u-c or v+m*u+c with |m|,|c| <= 4
q1847 monic cubic/quartic u exact-support scans
full genus-69 orientation-cover sampling as the first production plan
seed-order or compact-bucket fishing without a named invariant
```

## Test A: Fused Dplus Prefix Pricing

Goal:

```text
Can Dplus be imposed at lower cost than the ordinary first two selected gates?
```

Implement a same-stream GPU comparison:

```text
baseline = current fastest vanilla X1(16) p27 path
control = current Dplus classifier/precheck path if available
candidate = fused Dplus path that reuses branch/root/halving intermediates
```

The candidate should avoid a fresh independent Legendre toll whenever possible.
It is acceptable if it is only an engineering prototype, but it must report the
same source denominators as baseline.

Report:

```text
raw_y_draws
nonsplit_y
ordinary candidates emitted
Dplus_y
Dplus candidates emitted
depth-20/24/26/28/30 survivors
accepted roots/sec
target survivors/sec at each depth
target survivors per raw_y_draw
kernel time and total wall time
any mismatch against CPU/Python Dplus on replay rows
```

Promotion:

```text
effective survivor/sec at depth >= 26 improves by >= 2x versus baseline
and target/raw_y_draw is not worse than the expected two-gate denominator
```

Excellent:

```text
close to the theoretical 4x conditional scope shrink with tolerable throughput
```

Kill:

```text
the path is slower than just letting the ordinary halving gates fail naturally
or the improvement is only a conditional lift with worse wall-clock throughput
```

## Test B: Direct Dplus Source Prototype

Goal:

```text
Can GPU generate rows already inside Dplus without classifying rejected raw-y?
```

Acceptable prototypes:

```text
sample a named low-genus quotient that maps to Dplus candidates
sample the conic quotient a=t-1/t, g=w/t only after the descended Kummer class
  or branch divisor is named, and only together with the domain-spin cover
do not treat the genus-17 relative cover as a production source unless a
  further quotient/Prym/source map is supplied
do not treat E_h90 alone as a source; the hard object is the degree-4 cover
use the two eta-normalized quartics if testing H90 branch/Kummer structure
the named second-layer payload is A_eta = U_eta + z*W_eta
do not use A_eta squareclass or low-weight eta/U/W/rho products as filters
sample a partial source that provably covers a fixed Dplus component
sample a fused recurrence source that emits Dplus plus a later selected gate
```

Not acceptable:

```text
enumerating the full genus-69 orientation cover as the first production path
choosing eps_h/eps_v buckets and calling that a source
reporting only conditional survivor rates without raw source accounting
```

Report:

```text
source parameter draws
valid source rows
mapped X1(16) candidates
dedup/collision rate
failure reasons
depth histogram through at least 30
target/source_draw
target/GPU-second
validation replay against ordinary X1(16) verifier path
```

Promotion:

```text
target/source_draw and target/GPU-second both beat baseline with margin
and the source reaches beyond the first two selected gates
```

Kill:

```text
the source pays the same random half-losses as ordinary search
or only implements the known two-gate prefix at higher cost
```

## Test C: Coupling Telemetry While Fused

If Test A is already instrumented, emit cheap later-gate telemetry on the
Dplus-conditioned stream:

```text
d3,d4,d5,... as far as cheap
A coordinate / A hash for each emitted candidate
pairwise and lagged correlations
short sign-word bucket counts
depth-conditioned transition rates
```

Bridge baseline:
[P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
shows zero mixed `A` groups for post-Dplus `d3` and `d4` after `d3=+1` across
three p27 seed groups.  So any fused Dplus telemetry should report whether the
same A-descent persists at GPU scale, and should route later-gate class work
to the A-level Kummer extraction packet unless it finds a genuine trace/norm
class not visible on A.

Coordinate bridge update:
[P27 Trace/Norm Dplus A-Coordinate Bridge](p27_trace_norm_dplus_a_coordinate_bridge_20260622.md)
shows that the A coordinate is already cheap from the H90/base coordinate:

```text
t = y - 1
A = (t - 1/t)^4/4 - 2
```

So a fused-Dplus GPU telemetry mode can emit A-level columns from `y/t`
without first materializing root-dependent candidate A.  This is only a
telemetry/source-accounting convenience; it does not by itself predict `d3/d4`.

Second-layer update:
[P27 Trace/Norm Dplus X6/U-Class](p27_trace_norm_dplus_x6_uclass_20260622.md)
shows that on same-stream `Dplus` rows:

```text
U = x6 + 1/x6
chi(U + A) = +1
d3 = chi(x6)
```

Each analyzed y has four `U` values and eight `x6` values, with all eight
`x6` branches sharing one squareclass.  A GPU telemetry mode should emit
`x6`/`U` only if it is supporting the class comparison with H90 `A_eta`;
this is not yet a production bucket.
Follow-up [P27 Trace/Norm Dplus Four-U Rational Screen](p27_trace_norm_dplus_ucover_rational_screen_20260622.md)
kills low-degree rational formulas for the four-`U` quartic coefficients in
`t`, `a=t-1/t`, and `A` through degree `(20,20)`, so do not treat the four-`U`
cover as a simple visible GPU source formula.
Follow-up [P27 Trace/Norm Dplus Reciprocal Tower](p27_trace_norm_dplus_reciprocal_tower_20260622.md)
names the CAS object: `X=t^3+2*t^2-1/t`, `F_A(X,U5)=0`, `F_A(U5,U6)=0`,
and `x6^2-U6*x6+1=0`.  GPU telemetry should support this tower/class
comparison; it is still not a standalone production mode.
Follow-up [P27 Trace/Norm Dplus Reciprocal Tower Small-Field Descent](p27_trace_norm_dplus_reciprocal_tower_smallfield_descent_20260622.md)
makes that boundary explicit: q607/q1607/q1847 exact enumerations have mixed
`A`/`B` fibers for `chi(x6)` on the naked tower.  Do not build a GPU source
that samples only `F_A(X,U5),F_A(U5,U6)`.  A useful GPU mode must either stay
same-stream from legal `Dplus` rows or enforce the selected legal/core source
cut and report the raw denominator.
Follow-up [P27 Trace/Norm Dplus H90-X6 Coboundary Probe](p27_trace_norm_dplus_h90_x6_coboundary_20260622.md)
kills the cheap H90/root bridge: simple H90 atoms and first-order
`rho +/- atom` branch divisors have no exact weight-`<=3` product for
post-Dplus `chi(x6)`, and train skews do not hold out.  Do not add GPU
production modes for H90/rho/x6 sign buckets unless CAS supplies a named
quotient or source map.
Latest row-bit boundary:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Solubility Boundary](p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_20260622.md)
finds zero failures of:

```text
Ktrace square or zero  => row-bit t-fiber uniform;
Ktrace nonsquare       => row-bit t-fiber mixed, always 4 plus / 4 minus.
```

This is worth validating at GPU scale as telemetry, because it is a precise
class boundary.  It is not a production source until the plus/minus class on
the H90-soluble side is named.

Small-coset follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Group-Coset Screen](p27_trace_norm_dplus_u6_rowbit_h90_group_coset_20260622.md)
kills the nearest quick source for that plus/minus class.  After mapping to
`E: v^2=u^3-u`, quotient projections with `m <= 24` have:

```text
exact_nontrivial_projection_total = 0
```

So do not add GPU modes for small H90 elliptic coset buckets unless a new
theorem names a projection outside the tested family.

U-line divisor follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit H90 U-Divisor Screen](p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_20260622.md)
finds that the soluble-side sign descends to the even elliptic coordinate
`u=4/(t-1/t)^2`, but has no monic linear or quadratic divisor in the tested
fields.  It writes the exact-support packet:

```text
research/p27/archive/fixtures/p27_dplus_rowbit_u_divisor_targets_20260622.json
```

This packet is the next bounded GPU exact-support ask:

```text
degree 3: u^3 + a*u^2 + b*u + c
degree 4: u^4 + a*u^3 + b*u^2 + c*u + d
accept: chi(P(u)) = polarity * sign on every listed row, with no zero evals
priority: q1847 and q2087, then q1607 for cross-check
```

Promote an exact cubic/quartic hit only if it appears in a promotion field and
verifies on another guard field or yields a named divisor/class.  Do not treat
q607 quartic fits as promotion evidence; random fits are expected there.

Latest exact-support follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit H90 U Cubic/Quartic Screen](p27_trace_norm_dplus_u6_rowbit_h90_u_cubic_quartic_20260622.md)
finds zero exact cubics in q607/q1607/q1847/q2087 and zero exact quartics in
q1847 after a full `6300872423`-triple scan.  Do not spend GPU time on q1847
`u` cubic/quartic exact support.  q2087 quartic is optional closure only if a
GPU is already warm; the main row-bit ask is now non-visible
divisor/theta/Prym extraction or telemetry for a named class supplied by CAS.

Local Magma factor-split update:
[P27 Trace/Norm Dplus U6 Row-Bit Local Magma Factor Split](p27_trace_norm_dplus_u6_rowbit_local_magma_factor_split_20260622.md)
finds stable factor drops in q607/q1607/q1847/q2087:

```text
domain-spin: 32 -> 16 + 16
Aeta eta=+1: 32 -> 8 + 8 + 8 + 8
Aeta eta=-1: 32 -> 8 + 8 + 8 + 8
```

The q607/q1607 action probe shows `z -> -z` swaps the two domain-spin factors,
`rho -> -rho` swaps Aeta degree-8 factors in pairs, and `S -> -S` fixes each
tested factor.  This is not itself a GPU sampler.  It is a CAS-to-GPU bridge:
if CAS extracts a cheap factor label or Kummer class from the degree-8 factors,
GPU should emit that label against d3/d4/d5 in same-stream Dplus telemetry.

Factor-label follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit Factor Label Probe](p27_trace_norm_dplus_u6_rowbit_factor_label_20260622.md)
shows the degree-8 factors are quartics in `Y=S^2=U6+2`, and rho-paired
quartics multiply back to the domain-spin factors.  GPU should not implement
this yet as raw factorization; wait for CAS to provide a cheap quartic-label
formula or resolvent class.  Once supplied, the GPU ask is same-stream telemetry:

```text
domain factor label
Aeta quartic label / resolvent class
d3,d4,d5
source denominator and replay data
```

If cheap, fused telemetry should therefore emit:

```text
Ktrace squareclass
row bit chi(U6+2)=chi(x6)
H90 elliptic coordinates or compact hashes
A coordinate
d3,d4,d5,...
```

Promotion:

```text
a named low-complexity recurrence or state has heldout source-normalized lift
that compounds across gates by >= 1.25x
```

Kill:

```text
post-Dplus signs remain independent half-gates, matching the CPU orientation
and product screens
H90/rho/x6 branch-root products behave like heldout noise
```

## Required Output

Return one compact report with:

```text
commit hash
exact command lines
GPU model and compile flags
run duration and cost
all denominators listed above
PASS/FAIL replay validation
promote/kill recommendation for each test
logs saved under results/p27/
research note saved under research/p27/evidence/
```

## Continue / Kill

```text
continue = Dplus-native/fused implementation if it improves effective deep
           survivor throughput or exposes later-gate coupling
continue = direct source only if it names the source map and denominator
continue = emit A with Dplus later-gate telemetry and compare to A-level classes
continue = emit Ktrace and row-bit telemetry to validate the H90 boundary at scale

kill = large p27 production run based only on the existing Dplus classifier
kill = orientation bucket telemetry as a standalone GPU task
kill = fixed-prefix filtering without source-normalized improvement
kill = visible H90 row-bit products or small H90 elliptic coset buckets
kill = monic degree <= 2 u-divisor support for the row bit
kill = q1847 monic cubic/quartic u exact-support GPU scans
kill = visible monic P^1_u support through degree 4 as a production target
```

```text
p27_gpu_dplus_native_source_handoff_rows=1/1
```
