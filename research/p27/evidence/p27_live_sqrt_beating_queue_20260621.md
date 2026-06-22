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
```

Concrete next K/S test:

```text
offline Magma/Sage should now target E': V^2=U^3+4U:
  do staged elimination for the legal pullback:
    first A=2-c^2 and x5=r0^2,
    then both conjugate conics and the r_next transition
  compute whether the resulting legal source has low genus/sourceable
    components, or remains a high-complexity cover
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
1. Theory/CAS: staged legal pullback / quotient decomposition of the
   conic-chain/K/S layer, now including Z^2=-(L+a)(L-a)cR.
2. GPU/structure: recurrence telemetry and legal-pullback sampler only, not
   raw random `(R,L)`.
3. Theory/lit/expert: trace/norm half-norm phase identity for pref vs h*vq.
4. Production GPU: no moonshot-scale run without a quotient/source or measured
   heldout efficiency gain.
```

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
