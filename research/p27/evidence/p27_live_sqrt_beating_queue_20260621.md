# P27 Live Sqrt-Beating Queue

Date: 2026-06-21

## Claim

After the alpha branch and K/S first-half cover screens, the p27 moonshot has
three live test surfaces.  They should be treated differently:

```text
1. K/S saturated first-half cover: live only as quotient/decomposition work.
2. Trace/norm half-norm phase coupling: live theorem/expert front.
3. GPU practical A/B: useful only as telemetry or once a source/quotient exists.
```

Do not restart broad visible-character scans.  Do not promote a fixed prefix
filter as sqrt-beating unless it gives a source, recurrence, or scope shrink
that compounds beyond constant factors.

## Current K/S Status

The K/S route is no longer a low-genus direct source candidate.

Latest evidence:
[P27 K/S First-Half Cover Magma Smoke](p27_ks_first_half_cover_magma_20260621.md).

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
```

Concrete next K/S test:

```text
offline Magma/Sage over q=1607, q=1847, q=2087
load saturated first-half ideal
compute decomposition under Sroot -> -Sroot and alpha
ask whether a low-genus quotient still remembers the d3 all-plus class
```

Promotion bar:

```text
genus <= 1 quotient, named recurrence/sourceable walk, or cheap sampler
surviving p27-signature guard fields
```

Kill condition:

```text
no low-genus quotient of the genus-37 layer, or d4 is a fresh unrelated cover
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

GPU is valuable for telemetry and practical search, but current math does not
yet justify a new large p27 production run as a moonshot.

Concrete GPU test if used:

```text
same-stream p27 A/B:
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
on heldout streams, or direct sampler into a named source stratum
```

Kill condition:

```text
fixed-prefix filters give only constant factors and no recurrence/source
```

## Current Recommendation

Ranked next moves:

```text
1. Theory/CAS: quotient decomposition of the saturated genus-37 K/S layer.
2. Theory/lit/expert: trace/norm half-norm phase identity for pref vs h*vq.
3. GPU: bounded same-stream telemetry only; no moonshot-scale run without
   a quotient/source or measured heldout efficiency gain.
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
