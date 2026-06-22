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

3. Compute quotient/Prym structure under the available symmetries:

```text
W -> -W
T -> -T
beta -> -beta
X -> 1/X, if the reciprocal B involution lifts on the normalized model
any component permutation induced by these maps
```

4. For every genus `0` or `1` quotient, test whether the selected class
descends nontrivially:

```text
div(Unext + 2) modulo squares
gamma^2 = Unext + 2 as a Kummer class
materialization class x6^2 - Unext*x6 + 1
f4/f3 class from the second reduced-fiber fixture
```

5. Compare the f3 and f4 classes:

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
