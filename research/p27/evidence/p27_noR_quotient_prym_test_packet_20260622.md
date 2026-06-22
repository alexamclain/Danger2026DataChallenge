# P27 No-R Quotient/Prym Test Packet

Date: 2026-06-22

## Claim

The next plausible sqrt-beating B-line test is not another visible bucket or a
large GPU run.  It is a normalization and quotient/Prym extraction for the
localized no-R reduced cover.

The reason is now sharp:

```text
compactD_R is redundant after reduced_U,
the no-R cover is not an obvious genus-0/1 source,
visible B-fiber classifiers have already failed.
```

So the only first-pass win left on this surface is a low-genus quotient,
component, Prym factor, or repeated Kummer relation that still carries the
selected `gamma^2 = Unext + 2` / next-gate class.

## Durable Inputs

Use these as the exact starting artifacts:

```text
research/p27/evidence/p27_b_line_reduced_cover_symbolic_packet_20260622.md
research/p27/archive/probe_outputs/p27_b_line_reduced_cover_symbolic_packet_20260622.txt
research/p27/archive/fixtures/p27_b_line_reduced_cover_noR_invX_q7_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_cover_localized_reduced_q7_magma.m
research/p27/archive/fixtures/p27_b_line_compact_beta_dnext_square_q7_q23_magma.m
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
research/p27/archive/fixtures/p27_b_line_second_reduced_fiber_fixture_20260622.json
```

Supporting verdicts:

```text
compactD_R/beta/d_next squareclass smoke = pass over q7/q23
no-R genus pressure = genus <= 1 violated in 5/7 fields if one component
no-R closed-point pressure = degree 2 and 3 closed points both nonzero
no-R Frobenius fiber profile = degree-3 B orbits plus quadratic fiber splitting
no-R coordinate degree profile = cubic B-orbit, quadratic fixed-B/fiber split
no-R B-orbit invariant screen = square Norm(B) support, no visible trace/norm gamma selector
no-R quadratic subcover classifier = W/T-only killed; beta_U and hidden_mixed remain
no-R fixed-B character screen = beta_U support chi(B)=+1; no stable gamma law
no-R beta_U norm descent = gamma is Norm(Unext+2), half-size/full-size fiber split
no-R beta_U norm relation = no stable low-bidegree (B,Norm) plane curve
no-R beta_U next-gate = gamma+ materializes cleanly but f4 is mixed inside every active B
no-R beta_U f4 pair = x7-pair norm -4*(A*x6+1) exact, but no pair-level sampler
no-R beta_U same-sign selector = x6 atom products through weight 3 fail on same-plus/same-minus
no-R fixed-B norm comparison = hidden_mixed descends too, but its visible 32/64 split is chi(B), not gamma
no-R hidden_mixed next-gate = nonsquare-B gamma+ does not materialize; square-B materializes but f4 is mixed
reduced lift visible classifier = killed
gamma visible square triviality = killed
oriented alpha/beta word = tautological, not a source
```

## Exact CAS Object

First object, with `eta = +1`, no `compactD_R`:

```text
variables = X, iX, W, T, beta, Bline, Unext
eq_chart = X*iX - 1
eq_E = W^2 - (X^3 - X)
eq_T = T^2 - X*(X^2 + 1)*(X^2 + 2*X - 1)
eq_Bline = Bline*(X^2 - 1)^2 - 8*X^2
eq_first_half = beta^2*U_den^2 - (U_num^2 - 4*U_den^2)
eq_reduced_Unext =
  A_den*(Unext*U_den - x5_num)^2
  - (A_den*x5_num^2 + 2*A_num*x5_num*U_den + 4*A_den*U_den^2)
```

Localize/invert:

```text
X
X - 1
X + 1
X^2 + 1
T - 2*X^2
U_den
A_den
```

Attach only after the no-R base is understood:

```text
materialize_x6 = x6^2 - Unext*x6 + 1
gamma = gamma^2 - (Unext + 2)
compactD_R = redundant/twinned layer after beta and d_next
```

## Test Sequence

1. Normalize the no-R localized curve over at least one promotion guard field
   such as `q1607`, `q1847`, or `q2087`.  q7/q23 are syntax and squareclass
   smoke fields, not decisive promotion fields.

2. Report for every component:

```text
field
component count
degree over P1_Bline
genus
point count sanity against existing layer-count probes
field of definition
singular/boundary points added by completion
```

3. Compare degree-2 and degree-3 base changes:

```text
normalize over GF(7^2) and GF(7^3)
normalize over GF(23^2) and GF(23^3), or give a reason one base is enough
compute component count after each base change
compute Frobenius permutation of components
track whether gamma descends to components or permutes between them
separate B-orbit degree from extension splitting inside a fixed B fiber
```

This comparison is required because the closed-point transform has no degree-1
points but has nonzero coprime degree-2 and degree-3 closed points in both
base-field families.  The finite-field Frobenius-fiber screen further shows
that degree-3 activity sits over degree-3 `B` orbits, while quadratic activity
can also occur above base-field `B` values.  The coordinate-degree screen
splits the next CAS work into a cubic `B`-orbit subtest and a quadratic
fixed-`B` fiber subtest, with the latter separated into `W/T` and
`beta/x5/U` extension layers.

Required subtests:

```text
cubic B-orbit quotient/component test
degree-2 B-orbit quotient/component comparison
quadratic fixed-B beta_U_fixedB subcover test
quadratic fixed-B hidden_mixed_fixedB subcover test
```

Do not spend CAS/GPU effort on the `W/T`-only fixed-`B` subcover as a selected
gamma source: the quadratic classifier finds it is always an 8-point
zero-selector branch in the tested guard fields.

For the B-orbit tests, carry forward the visible invariant screen:

```text
active degree-2/3 B-orbits have chi(Norm(B))=+1
degree-2 orbit discriminant has chi=-1
degree-3 orbit discriminant has chi=+1
gamma is Frobenius-stable at the B-row signature level
```

This is only support/component data.  The trace/norm/discriminant character
screen does not select `gamma`: degree-2 orbits are mostly or exactly
half/half, and the exact `GF(7^3)` linear character fails in `GF(23^3)`.
Promote the B-orbit subtest only if normalization finds a quotient/Prym factor
carrying `gamma` or coupling f3/f4; do not promote square `Norm(B)` support as
a sampler.

For the `beta_U_fixedB` test, impose `chi(B)=+1` as a support gate.  Do not
promote that support gate as a sampler unless the gamma/f4 class descends on
the resulting quotient.  For `hidden_mixed_fixedB`, ignore the small-field
`B +/- 2` atom shortcut unless a divisor proof resurrects it.

For beta_U specifically, the class to extract is now named:

```text
N_B = Norm_GF(q^2)/GF(q)(Unext + 2)
```

The finite-field signature to explain is:

```text
gamma = chi_base(N_B)
gamma+ rows have 16 beta_U points over B
gamma- rows have 32 beta_U points over B
```

Do not ask for a small visible `(B, N_B)` plane equation as the main route:
the relation screen is negative through bidegree `B12_N16` in the stable guard
fields.  The task is divisor/Kummer extraction of `N_B`, not another blind
low-degree scan.

Also do not treat beta_U gamma-positive rows as a two-gate source.  The
next-gate probe finds:

```text
gamma=+1 beta_U row => 2 x6 roots
each x6 => 2 x7 roots
chi(v+2)=chi(x7) with zero mismatches
every active gamma-positive B row has both f4 signs
```

So beta_U is a clean f3/materialization class, but f4 must be compared after
normalization as a possible quotient/Prym relation or fresh half-cover.  It is
not a direct GPU sampler.

At the x6-pair level, carry the exact ordinary halving norm as orientation
data:

```text
x7_plus * x7_minus = -4*(A*x6 + 1)
```

The pair probe verifies this with zero formula/squareclass mismatches.  It
only distinguishes mixed-sign x7 pairs from same-sign pairs; it does not
decide same-plus versus same-minus, and reciprocal x6 pair products are not
stable.  Do not promote x6-pair buckets without a new normalized quotient or
class relation.

The remaining same-sign choice has also been screened against the natural
x6-level atoms and products through weight `3`.  No exact or stable selector
appears; the `359^2` heldout best reaches only `276/456`.  Treat further
visible x6 product scans as killed unless a theorem names a new coordinate.

For `hidden_mixed_fixedB`, the same norm-descent comparison has zero
finite-field mismatches and zero per-`B` sign conflicts, but it does not
reproduce beta_U's selected `gamma`/fiber-size handle.  Its visible split is:

```text
chi(B)=+1 => 32 hidden_mixed points over B
chi(B)=-1 => 64 hidden_mixed points over B
```

So run hidden_mixed only after beta_U unless the CAS engine can extract both
classes at essentially the same cost.  The hidden_mixed promotion criterion is
stricter: it must find a quotient/Prym/divisor class carrying `gamma`, not
merely the `chi(B)` fiber-size split.

The hidden_mixed next-gate test adds a materialization boundary:

```text
chi(B)=-1 and gamma=+1 => no x6 materialization
chi(B)=+1 and gamma=+1 => x6 materializes, but every active B has mixed f4
```

Thus hidden_mixed is not a continuation sampler.  If normalized CAS keeps it
alive, separate the nonsquare-B non-materialized boundary from the square-B
materialized class and carry the ordinary x7-pair norm
`x7_plus*x7_minus=-4*(A*x6+1)` only as orientation data.

4. Compute quotient/Prym structure under the available symmetries:

```text
W -> -W
T -> -T
beta -> -beta
X -> 1/X, if the reciprocal B involution lifts on the normalized model
any component permutation induced by these maps
```

5. For every genus `0` or `1` quotient, test whether the selected class
descends nontrivially:

```text
div(Unext + 2) modulo squares
gamma^2 = Unext + 2 as a Kummer class
materialization class x6^2 - Unext*x6 + 1
f4/f3 class from the second reduced-fiber fixture
```

6. Compare the f3 and f4 classes:

```text
pullback
translate
coboundary
iterate/recurrence
fresh unrelated half-cover
```

## Promote / Kill

Promote only if one of these happens:

```text
a genus 0/1 quotient carries the selected class and gives a direct source map
a quotient/Prym factor couples f3 to f4 without adding a fresh half-cover
a recurrence/walk samples the selected class without raw X1(16) rejection
a GPU implementation can sample the named quotient directly, not prefilter it
```

Kill this first-pass B-line route if:

```text
all components and quotients carrying gamma are high-genus/generic
gamma and f4/f3 are fresh unrelated Kummer classes
the surviving beta_U/hidden_mixed fixed-B subcovers are fresh unrelated half-covers
the only benefit is a constant-factor continuation filter
the proposed GPU mode pays a new Legendre/classification toll
```

## GPU Boundary

GPU work should wait for a named map from the CAS pass.  The useful GPU test is
then:

```text
sample the named quotient/source directly,
verify exact agreement with ordinary x16halvenonsplit on heldout seeds,
report target survivors per raw source draw and per second.
```

Do not run a large p27 GPU production search from no-R, `Bplus`, `compactD_R`,
`alpha`, `beta`, or `gamma` alone.

```text
p27_noR_quotient_prym_test_packet_rows=1/1
```
