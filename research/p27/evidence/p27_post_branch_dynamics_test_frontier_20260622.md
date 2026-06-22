# P27 Post-Branch-Dynamics Test Frontier

Date: 2026-06-22

## Claim

The obvious branch-dynamics routes have been closed.  The remaining
sqrt-beating tests are no longer map-family screens; they are class-extraction
or direct-sampler tests.

This note is a compact handoff after the latest A/B/K/lambda recurrence
screens.

## Closed Map Families

The following fixed correspondence families have no exact `d3/d4` recurrence
in the p27-signature guard fields:

```text
A-line:
  visible S3 branch transforms on {-2,2,infinity}
  affine maps A -> mA+b
  full PGL2 maps A -> (aA+b)/(cA+d)
  hidden-X power correspondences projected through A=B^2-2, X -> X^m, m=2..6
  Chebyshev/Dickson maps D_m(A)=2*T_m(A/2), m=2..12

B-line:
  visible S3 branch transforms on {0,-2,infinity}
  full PGL2 maps B -> (aB+b)/(cB+d)
  hidden-X power maps from B=8X^2/(X^2-1)^2, X -> X^m, m=2..6
  monomial Belyi maps u=-B/2 -> u^m, m=2..12
  q1847 monic quartic support for d3 and d3+d4 all-plus

K/lambda:
  split degree <=4 lambda branch divisors for d3
  lambda monomial Belyi maps lambda -> lambda^m, m=2..12
  monic cubic lambda support for d3
  q1847 monic quartic lambda support for d3
```

The common pattern is important:

```text
no full-domain recurrence
only small partial overlaps or field-local one-sided tails
no source-normalized shrink
no GPU production reason
```

## Remaining First-Class Tests

### Test 1: Coordinated A/B/K/Sroot Kummer Class Extraction

Use:

```text
research/p27/archive/fixtures/p27_a_level_kummer_extraction_packet_20260622.json
research/p27/archive/fixtures/p27_b_line_kummer_fixture_packet_20260622.json
research/p27/archive/fixtures/p27_ksroot_kummer_fixture_packet_20260622.json
```

The coordinate bridges are now exact on the frozen fixtures:

```text
A = B^2 - 2
K^2 = (B - 2)^4 / (8*B*(B + 2)^2)
Sroot^2 = K
```

So A-level, B-line, K-line, and Sroot are coordinate views of the same
selected-gate class problem, not independent lanes.

Compute:

```text
normalized cover carrying d3 over P1_A/P1_B/P1_Sroot
branch divisor degree and support field degrees
genus/component count
f4/f3 and later classes on selected prefixes
```

Promote only if:

```text
d3 is low-genus/sourceable
or d4,d5,d6 are pullbacks/translates/coboundaries/iterates of one class
```

Kill if:

```text
d3 is high/generic and d4,d5,d6 are fresh independent half-covers
```

#### B-Line Coordinate

Use:

```text
research/p27/evidence/p27_b_line_kummer_extraction_packet_20260622.md
```

The visible quartic shortcut is now closed in q1847 for both d3 and the direct
two-gate prefix:
[P27 Full Quartic q1847 D3 Screen](p27_full_quartic_q1847_d3_screen_20260622.md)
and [P27 B-Line Gate4-Prefix Quartic q1847 Screen](p27_b_line_gate4_prefix_quartic_q1847_screen_20260622.md).
So this lane now means actual class extraction, not another B-line quartic
bucket.

Compute:

```text
normalized d3 cover over P1_B
branch divisor degree/support fields/genus
f4/f3 and f5/f4 class comparison if d3 is tractable
```

Promote only if:

```text
genus <= 1
or an explicit sourceable walk / class recurrence appears
```

Kill if:

```text
the normalized B-line cover is high genus and successive classes are unrelated
```

#### K/Lambda Coordinate With K-Square Stratum

Use lambda only as a normalization coordinate:

```text
lambda = -K^2/4
```

but keep the p27 rational constraint:

```text
K is a square on the doubled image
K ~ -K is not a rational source quotient
```

Compute:

```text
actual K-level branch class for d3
genus/support field degrees
whether lambda-level structure lifts back to the K-square stratum
```

The K/Sroot prefix-density shortcut is now closed:
[P27 K/Sroot Prefix Profile](p27_sroot_prefix_profile_20260622.md).
Sroot is still the cleaner normalization coordinate, but in every tested field
it is just a doubled K grouping with identical selected-prefix ratios.  Use it
for branch extraction, not GPU bucket production.

First bounded subtest, now closed in the decisive field:

```text
exact monic quartic support on lambda for d3_on_lambda
```

The cubic subfamily is already closed in q1471/q1607/q1847:
[P27 Lambda Low-Genus Screen](p27_lambda_lowgenus_screen_20260622.md).
The quartic q1847 promotion-field screen is also closed and negative:
[P27 Lambda Quartic q1847 D3 Screen](p27_lambda_quartic_q1847_d3_screen_20260622.md).

Promote only if:

```text
there is a K-level source or recurrence inside the rational doubled image
```

Kill if:

```text
lambda gives only an algebraic-closure quotient with no rational K-square lift
```

### Test 2: BSM Staged Legal Pullback

The staged BSM surface remains a CAS coordinate only.  It should be compared
against the same A/B/K/Sroot class sequence after the legal B-cover is imposed,
not treated as a raw GPU sampling surface.

### Test 3: Trace/Norm Half-Norm Phase Identity

The exact `Dplus` predicate is still useful as a two-gate model, but not as a
late recurrence.  The remaining trace/norm test is theoretical:

```text
find a theta/additive/Hilbert-90 identity controlling the joint phase of the
h and vq half-norm sections
```

Promote only if:

```text
the identity predicts a post-Dplus gate or gives a direct sampler
```

Kill if:

```text
it reduces to already-killed visible branch/norm squareclasses
```

## GPU Boundary

Do not run a large p27 GPU production search from any branch-map family above.

The post-quad first-class queue is consolidated in
[P27 First-Class Moonshot Tests After Quadratic Probe](p27_first_class_moonshot_tests_after_quad_20260622.md).
It keeps the surviving tests scoped to coordinated A/B/K/Sroot Kummer sequence
extraction, BSM staged legal-pullback normalization, and the trace/norm
half-norm phase identity.

GPU becomes first-class again only for:

```text
bounded telemetry that feeds class extraction
or a direct sampler/source map from one of the tests above
```

Promotion bar:

```text
>=1.25x held-out source-normalized lift
or target/GPU-second improvement with the same denominator
or an exact direct sampler into a named source stratum
```

## Continue / Kill

```text
continue = A/B/K/Sroot normalized Kummer/divisor class extraction
continue = trace/norm half-norm phase theorem ask
continue = GPU only after a class/sampler is named

kill = more branch-S3/PGL2/Chebyshev/monomial map screens without a new theorem
kill = bucket production from A, B, K, lambda, or Bplus alone
kill = treating partial low-coverage overlaps as recurrences
```

```text
p27_post_branch_dynamics_test_frontier_rows=1/1
```
