# P27 B-Line Reduced-Cover Charted Magma Staging

Date: 2026-06-22

## Claim

The reduced B-line cover is still an offline CAS problem, but the failure mode
is now sharper and the next Magma/Sage attack order is concrete.

The original reduced-cover fixture failed during product saturation.  The new
charted fixtures show:

```text
X*iX = 1 removes the first saturation wall.
The no-R reduced cover then saturates to a dimension-1 scheme online.
The full cover with compactD_R is dimension 1 before saturation, but online
Magma times out during the remaining factors.
A fully localized full model, replacing all denominator saturations by inverse
variables, is immediately dimension 1 with 12 equations.
```

This does not prove low genus or sourceability.  It gives the right offline
CAS formulation: normalize the localized complete intersection or the no-R
base first, then add compactD and the materialization/gamma layers.

## Artifacts

Fixtures:

```text
research/p27/archive/fixtures/p27_b_line_reduced_cover_noR_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_noR_stepwise_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_noR_invX_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_invX_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_invX_stepwise_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_localized_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_localized_invariants_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_localized_reduced_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_stepwise_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_stepwise_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_invX_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_noR_invX_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_invX_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_invX_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_invX_stepwise_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_invX_stepwise_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_invariants_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_invariants_q7_magma_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_reduced_q7_magma_20260622.xml
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_localized_reduced_q7_magma_20260622.txt
```

Submission shape:

```bash
curl -L -s -A 'Mozilla/5.0 Codex p27 research' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode input@research/p27/archive/fixtures/<fixture>.m \
  https://magma.maths.usyd.edu.au/xml/calculator.xml
```

## Results

### No-R Product Saturation

Removing compactD_R is not enough by itself:

```text
BREDUCED_NOR_START 7
memory limit during Saturation(I, bad)
```

### No-R Stepwise Saturation

The first wall is the `X=0` artifact:

```text
BREDUCED_NOR_STEP_START 7 2 5
BREDUCED_NOR_STEP_BEFORE 1 X
memory limit during Saturation(J, X)
```

### No-R With X Inverted

Replacing the first saturation with `X*iX=1` succeeds:

```text
BREDUCED_NOR_INVX_START 7 1 6
BREDUCED_NOR_INVX_SATURATION 1 6
```

The later `Curve(S)` / `Genus(C)` call still hits the online memory limit, so
normalization remains offline work.

### Full Cover With X Inverted

Keeping compactD_R gives a dimension-1 raw chart:

```text
BREDUCED_INVX_START 7 1 7
```

Product saturation then exceeds the 60-second online time limit.

### Full Cover With X Inverted, Stepwise

The first remaining factor is manageable, the next one is not online:

```text
BREDUCED_INVX_STEP_START 7 1 7
BREDUCED_INVX_STEP_BEFORE 1 Xminus1
BREDUCED_INVX_STEP_AFTER 1 Xminus1 1 7
BREDUCED_INVX_STEP_BEFORE 2 Xplus1
time limit
```

### Fully Localized Full Cover

Replacing all denominator saturations by inverse variables gives a direct
dimension-1 complete-intersection chart:

```text
BREDUCED_LOCALIZED_START 7 1 12
```

The online calculator still cannot compute `#Points(S)` or `Curve(S)`, but the
localized model avoids the failing saturation stage entirely.

### Localized Invariant Boundary

The lighter invariant fixtures show the same boundary more sharply:

```text
BREDUCED_LOCALIZED_INV_START 7 1 12
BREDUCED_LOCALIZED_INV_DEG_ERROR
time limit

BREDUCED_LOCALIZED_REDUCED_START 7 1 12
time limit
```

So the web calculator can certify dimension for the localized complete
intersection, but not degree, reducedness, irreducibility, point count, curve
conversion, or genus.

## Interpretation

Positive:

```text
The reduced-cover formula is CAS-staged more cleanly now.
The no-R base can be saturated after charting away X=0.
The full localized model is dimension 1 without saturation.
This gives an offline Magma/Sage agent a concrete attack order.
```

Negative:

```text
Online Magma still cannot extract genus, components, branch divisors, or a
source map.
Online Magma also cannot extract lightweight degree/reduced/irreducible
invariants from the localized full model.
No low-genus quotient has been found.
No GPU production mode follows from this result.
```

## Offline CAS Attack Order

Use this order:

```text
1. Start from p27_b_line_reduced_cover_localized_q7_magma.m.
2. Port the same localized chart to q1607/q1847/q2087 or characteristic 0.
3. Normalize the 13-variable complete intersection directly, without
   Saturation(I,bad).
4. Compute degree/reducedness/irreducibility offline; the online endpoint
   cannot supply even these invariants.
5. If that is too heavy, normalize the no-R X-inverted base first:
   p27_b_line_reduced_cover_noR_invX_q7_magma.m.
6. Add compactD_R as a quadratic cover and compute its branch divisor.
7. Only after the reduced f3 cover is understood, attach
   x6^2 - U*x6 + 1 and gamma^2 = U + 2.
```

Promote only if this yields:

```text
genus <= 1,
a sourceable quotient/walk,
a recurrent/coboundary relation controlling f3 and f4/f5,
or a direct sampler with source-normalized gain.
```

Kill if:

```text
the localized reduced cover is high genus with no quotient,
compactD_R and gamma are fresh unrelated half-covers,
or the only available evidence remains point counts and finite-field buckets.
```

## Continue / Kill

```text
continue = offline normalize the localized reduced cover
continue = use X-inverted no-R base as a fallback decomposition
continue = compute branch divisor degrees for compactD_R and gamma only after normalization

kill = online Magma as the extraction engine
kill = saturation-first reduced-cover strategy on the web calculator
kill = GPU production before a sourceable quotient or recurrence is extracted
```

```text
p27_b_line_reduced_cover_charted_magma_rows=1/1
```
