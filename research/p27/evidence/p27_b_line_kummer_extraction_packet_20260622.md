# P27 B-Line Kummer Extraction Packet

Date: 2026-06-22

## Claim

The B-line route has advanced from a bucket/telemetry idea to a precise
function-field extraction target:

```text
extract the Kummer/divisor class d3(B) on P1_B
then compare f3(B), f4(B), f5(B), ... for recurrence or coupling
```

This is the next concrete B-line test that could beat `sqrt(p)`: not by
filtering one more half-gate, but by finding a source, low-genus quotient, or
multi-gate class relation on `P1_B`.

## Artifacts

Packet generator:

```text
research/p27/archive/gates/p27_b_line_kummer_extraction_packet.py
```

Generated packet:

```text
research/p27/archive/probe_outputs/p27_b_line_kummer_extraction_packet_20260622.txt
```

Magma sanity fixture:

```text
research/p27/archive/fixtures/p27_b_line_sanity_q1607_magma.m
```

Local sanity equivalent:

```text
q1607 rows/degenerate/mismatches = 1604 / 3 / 0 / 0 / 0 / 0
```

This checks the B quotient, `A+2=B^2`, and the K/A branch equations over
`q=1607`.  The Magma fixture is an algebraic sanity check only; the full
normalization/genus extraction is still the open CAS task.

## Exact B-Line Quotient

On the residual source coordinate `X`:

```text
B = 8X^2/(X^2 - 1)^2
A + 2 = B^2
```

The packet records:

```text
B_relation = B*X^4 - 2B*X^2 + B - 8X^2
B_branch_resultant = 16384*B^3*(B + 2)^2
```

The K/A branch relation with `L=K^2` is:

```text
L = (B - 2)^4/(8B(B + 2)^2)         for Bplus
L = -(B + 2)^4/(8B(B - 2)^2)        for Bminus
```

This is why the B-line is a natural genus-0 quotient for the legal selected
tower.

## Source Cover To Normalize

The packet gives the d3 all-plus cover over `P1_Bline` with variables:

```text
X, W, T, beta, R, z, Y, eta, Bline
```

where `beta` is the first-half branch root and `Bline` is the quotient
coordinate.  The defining equations are:

```text
eta^2 = 1
W^2 = X^3 - X
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
X*R^2 = criterion_num
Bline*(X^2 - 1)^2 = 8X^2
beta^2*U_den^2 = U_num^2 - 4U_den^2
4*z^2*H_num*(U_num + beta*U_den)
  = 2*U_den*A_den*(z^4 - 1)^2
Y^2*A_den = H_num
```

The auxiliary rational functions are emitted in the generated packet so the
CAS user does not need to reconstruct them from prose.

## Prior Kills

Already killed on the B line:

```text
B-atom products as d3/d4 predictors
rational-linear branch support of weight <=4 for d3(B)
one irreducible quadratic times <=2 rational linears for d3(B)
two irreducible quadratic branch factors for d3(B)
two irreducible quadratic branch factors for the legal B-domain
visible Belyi S3 orbit sampler on B
Belyi-conjugated hidden-X power maps X -> X^m, m=2..6, as d3/d4 recurrence
S3-conjugated monomial Belyi maps u -> u^m, u=-B/2, m=2..12
B-line prefix counts alone as a below-sqrt sampler
large GPU search from B buckets without an extracted class
```

So the B-line task is no longer "find a good bucket."  It is:

```text
compute the actual Kummer class, branch support, and genus
```

## CAS Task

Run over the p27-signature fields first:

```text
q = 1607, 1847, 2087
```

Required outputs:

```text
branch divisor degree for d3(B)
support field degrees
normalization genus over P1_B
visible involutions or quotients over B
comparison of f4/f3 and f5/f4 if d3 is tractable
```

Promotion bar:

```text
genus <= 1
or explicit sourceable walk
or recurrence/coupling among f3(B), f4(B), f5(B), ...
or a direct sampler that improves target/source_draw without fresh half-losses
```

Kill condition:

```text
high/generic branch degree
only previously killed split low-degree supports appear
f4/f5 are unrelated fresh Kummer classes
normalization is too high-genus to source or quotient
```

Update: the legal-domain split degree-4 screen is also negative:
[P27 B-Line Legal-Domain Two-Quadratic Support Screen](p27_b_line_legal_two_quadratic_support_20260622.md).
The core-to-legal B cut is not a product of two irreducible quadratic branch
factors in q1607/q1847/q2087.

Update: the visible Belyi orbit shortcut is negative:
[P27 B-Line Belyi-Orbit Screen](p27_b_line_belyi_orbit_20260622.md).
Every non-identity automorphism of the branch set `{0,-2,infinity}` sends core
B values outside the core bucket in q1607/q1847/q2087.

Update: the full degree-one rational B-line recurrence shortcut is negative:
[P27 B-Line PGL2 Recurrence Screen](p27_b_line_pgl2_recurrence_screen_20260622.md).
It tests every full-coverage map `B -> (aB+b)/(cB+d)` for
`d4(B) = +/- d3(phi(B))` in q1607/q1847/q2087 and finds zero exact
recurrences.  The best full-coverage maps are identity/raw d4-bias baselines,
so future B-line correspondence tests should be extracted or theorem-shaped,
not PGL2 restarts.

Update: the first theorem-shaped higher correspondence screen is also
negative:
[P27 B-Line Power-Map Recurrence Screen](p27_b_line_power_recurrence_screen_20260622.md).
It tests the maps induced by `X -> X^m` on
`B=8X^2/(X^2-1)^2`, for `m=2..6`, conjugated by the six visible Belyi
symmetries.  There are no exact forward or reverse `d3/d4` recurrences in
q1607/q1847/q2087, and the best maps cover only a minority of the relevant
domains.  Thus hidden-`X` doubling/tripling is not the missing sourceable
B-line recurrence.

Update: the adjacent monomial Belyi family is also negative:
[P27 B-Line Monomial Belyi Recurrence Screen](p27_b_line_monomial_belyi_recurrence_screen_20260622.md).
After normalizing `u=-B/2`, it tests S3-conjugated maps `u -> u^m` for
`m=2..12`.  There are no exact forward or reverse `d3/d4` recurrences in
q1607/q1847/q2087, and coverage is lower than in the hidden-`X` power screen.

Update: the bounded visible quartic d3 family has now been tested in the
decisive q1847 B/K screens:
[P27 B-Line Quartic GPU Test Card](p27_b_line_quartic_gpu_test_card_20260622.md).
[P27 Full Quartic q1847 D3 Screen](p27_full_quartic_q1847_d3_screen_20260622.md).
Exact monic quartic support for `d3_on_legalB` would have given a genus-1
double-cover source candidate.  Instead, q1847 found zero exact quartics in
both B and K coordinates.  That makes this packet's offline normalization /
Kummer-class route active rather than a fallback behind the visible d3 quartic
screen.

Update: the direct two-gate visible quartic is now negative too:
[P27 B-Line Gate4-Prefix Quartic q1847 Screen](p27_b_line_gate4_prefix_quartic_q1847_screen_20260622.md).
It exhausts `gate4_prefix_on_legalB` over q1847 and finds zero exact quartics,
so the B-line quartic shortcut is closed in the decisive field for both d3 and
the d3+d4 all-plus prefix.

Update: the deep-prefix B-line telemetry lane is now separately packaged:
[P27 B-Line Deep-Prefix GPU Telemetry Handoff](p27_b_line_deep_prefix_gpu_telemetry_handoff_20260622.md).
That run should emit `Bplus` and selected bits `d3..dN` from the same p27
stream to stress-test no-mixed-B descent and feed Kummer-sequence extraction.
It is not a replacement for the completed q1847 quartic screen and not a
production hunt.

Update: the compact guard-field fixture for the actual conditional Kummer
sequence is now available:
[P27 B-Line Kummer Fixture Packet](p27_b_line_kummer_fixture_packet_20260622.md).
It freezes `f3(B), f4(B), f5(B), f6(B)` rows over q1607/q1847/q2087.  The
meaningful first comparison is `f3` then `f4/f3`; the `f5/f6` rows are already
small-field tail dominated and should be treated as regression data, not
promotion evidence.

Update: the first finite-field fiber-invariant extraction is now available:
[P27 B-Line Fiber Invariant Probe](p27_b_line_fiber_invariant_probe_20260622.md).
For every legal B in q1607/q1847/q2087, the d3 next-root fiber has `32`
occurrences, `8` distinct x-roots, and `4` reciprocal-quotient values
`u=x+1/x`; all four satisfy `f3=chi(u+2)`.  This gives a smaller normalization
target than the full source fiber.  But the full product/norm is square, power
sums through exponent `64` do not select f3, and the four-u polynomial
coefficients are maximal-degree on legal B.  So this is not a GPU sampler; it
is a sharper CAS model.

Update: the V4 phase telemetry has a GPU-scale contract:
[P27 B-Line Phase GPU Telemetry Handoff](p27_b_line_phase_gpu_telemetry_handoff_20260622.md).
The class decomposition `f_{j+1}=alpha_j*beta_j` remains useful for Kummer
extraction, but the small p27 phase sequence screen is negative as a sampler.
The GPU run should therefore report phase recurrence/telescoping with
raw-source denominators, and should be killed if it reproduces independent
half-loss at larger scale.

Update: the reduced-fiber low-degree plane relation screen is negative:
[P27 B-Line Reduced-Fiber Relation Screen](p27_b_line_reduced_fiber_relation_20260622.md).
The all-cover and f3 plus/minus subcovers have `extra_nullity=0` through total
degree `20` in the screened B/A/lambda/mu coordinates.  The reduced cover
still matters, but it needs normalization/genus extraction rather than more
visible plane-relation scans.

Update: the reduced cover now has an explicit symbolic packet:
[P27 B-Line Reduced-Cover Symbolic Packet](p27_b_line_reduced_cover_symbolic_packet_20260622.md).
It emits the B-line source equations plus
`(Unext-2*x5)^2=4*(x5^2+A*x5+1)` in denominator-cleared form.  The selector is
`chi(Unext+2)`, and q1607/q1847/q2087 validation has zero reduced-equation or
selector mismatches.  This should be the first CAS normalization model before
the full reverse `z,Y` cover.

Update: the reduced-cover online Magma failure now has a charted workaround:
[P27 B-Line Reduced-Cover Charted Magma Staging](p27_b_line_reduced_cover_charted_magma_20260622.md).
Stepwise q7 saturation fails immediately at `Saturation(J,X)`.  Adding
`X*iX=1` lets the no-R reduced cover saturate as a dimension-1 scheme; the
full compactD_R cover is dimension 1 before remaining saturation; and a fully
localized complete-intersection model with inverse variables for all
denominator factors is dimension 1 with 12 equations.  Offline CAS should use
that localized model or normalize the X-inverted no-R base first.

Update: the compactD_R layer is now demoted after reduced_U:
[P27 B-Line Localized Cover Layer Count](p27_b_line_localized_cover_layer_count_20260622.md).
Over `607, 7^3, 7^4, 7^5, 7^6, 23^2, 23^3`, the finite-field check has zero
mismatches for
`chi(compactD_R_rhs / beta_rhs) = chi(d_next)`.  Thus compactD_R is not a
fresh Kummer layer once the reduced `U_next` cover makes `d_next` square.  The
first normalization target should be the no-R reduced cover; then prove this
square relation and add compactD_R as a redundant/twinned layer.

Update: the compactD_R demotion now has a function-field smoke:
[P27 B-Line CompactD/Beta/Dnext Squareclass](p27_b_line_compact_beta_dnext_squareclass_20260622.md).
Magma verifies over `GF(7)` and `GF(23)` that
`compactD_R_rhs/(beta^2*d_next)` is a square in the staged function field
with `Z=x5`, `beta=Z-1/Z`, and `d_next=Z*(U+A)`.

Update: the no-R reduced cover has a first genus/component pressure test:
[P27 B-Line No-R Genus Pressure](p27_b_line_noR_genus_pressure_20260622.md).
Applying a one-component Hasse-Weil pressure bound to the existing layer
counts gives genus-one violations in `5/7` tested fields and maximum
`g_min = 11` under that reading.  If the cover is not one component, the same
data is component or field-of-definition pressure.  The CAS target is therefore
normalization with components, quotients, and Prym structure, not an obvious
genus-0/1 source.

## Continue / Kill

```text
continue = run Magma/Sage normalization over P1_Bline in q1607/q1847/q2087
continue = normalize the reduced 4-u / 8-x d3 fiber cover if easier than the full source cover
continue = use the reduced_Unext symbolic packet as the first CAS model
continue = use the localized reduced-cover chart to avoid product saturation
continue = normalize no-R reduced cover before compactD_R
continue = compute no-R components/quotients/Prym after genus pressure
continue = lift compactD_R/beta/d_next square relation beyond q7/q23
continue = optional q2087 quartic closure only if useful
continue = use the B-line Kummer fixture rows as the compact CAS/expert input
continue = bounded GPU deep-prefix telemetry if it feeds f3/f4/f5 extraction
continue = if d3 is tractable, compare the B-line Kummer sequence f3,f4,f5
continue = use GPU only after a source/sampler or recurrence is named

kill = more unguided B-bucket scoring
kill = large GPU production from Bplus alone
kill = norm/trace/power-sum selectors for the B-line d3 fiber
kill = low-degree plane relations for the reduced B-line d3 fiber through degree 20
kill = treating one-bit conditional lift as sqrt-beating
kill = visible monic quartic d3 promotion after the q1847 B/K negatives
kill = degree-one rational B-line recurrence
kill = hidden-X power-map B-line recurrence for m=2..6
kill = monomial Belyi B-line recurrence u -> u^m for m=2..12
kill = q1847 visible B-line monic quartic for d3+d4 all-plus
kill = treating one-sided q1607/q1847/q2087 f5/f6 tails as recurrence evidence
kill = saturation-first online Magma extraction of the reduced cover
kill = compactD_R as an independent first-layer normalization target after reduced_U
kill = expecting the no-R reduced cover to be an obvious genus-0/1 source
```

```text
p27_b_line_kummer_extraction_packet_rows=1/1
```
