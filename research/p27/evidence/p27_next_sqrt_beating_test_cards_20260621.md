# P27 Next Sqrt-Beating Test Cards

Date: 2026-06-21

## Current Best Structure

The first p27 structural gate found an exact transfer of the p26 trace/norm
quotient:

```text
a = t - 1/t, t = y - 1
b = w(t^2 + 1)/t^2
b^2 = 16 - a^4
```

The remaining p27 problem has been compressed to two balanced bits on the same
`a`-line:

```text
domain_line(a) = chi((y - 1)(y^2 - 2)(y^2 - 2y + 2))
T_line(a) = normalized D * chi(y), with b-flip removed by chi(a), chi(b)
```

Follow-up audit shows that `domain_line=+1` is exactly the sampler's first
halving gate.  This is still worth pursuing as a practical GPU prefilter, but
not as the moonshot itself.  The sqrt-beating question is whether this same
quotient/Hilbert-90 structure exposes a cheap predictor for a later
post-domain halving gate.

The first post-domain telemetry is negative for `T_line`: at depths `6`, `8`,
and `10`, the `T_line` split is essentially flat after conditioning on
`domain_line=+1`.  So the next cards should look for a new named
post-domain discriminant bit rather than reusing `T_line` as the filter.

The named bit is now `chi(d2)`:

```text
x5 = selected first half after domain_line=+1
d2 = x5^2 + A*x5 + 1
```

On p27, depth-6 failure is `d2` nonsquare; the observed `w` obstruction after
`d2` is absent in the current samples.  `T_line`, old p24 label2 visible
features, H90 orientation, and tiny quotient lines do not predict `chi(d2)`.

The p25 first-lift elliptic-cover sampler has now been ported to p27:
[P27 First-Lift Elliptic-Cover Port](p27_first_lift_ecover_port_20260621.md).
This makes the practical first GPU candidate:

```text
baseline vs ecover source vs domain/dgate control
```

where `ecover` samples `E: w^2=x^3-x` and maps `y=x+1`.  It is the best
current constant-factor practical source.  The residual elliptic 2-descent
split is flat, so the sqrt-beating card remains the later `d_j` tower law.

The second gate now has a sharper label-2 mixed-cover formulation:
[P27 Label-2 Second-Gate Cover](p27_label2_second_gate_cover_20260621.md).
For p27, the exact selector is `compactD=-1`, not the old `compactD=+1` sign.
The corrected CPU filter is too slow, but the cover equations are explicit
enough for GPU and Sage/Magma tests.

## Card 1: P27 Line-Telemetry GPU Smoke

Ask the GPU agent to emit, for a small same-stream p27 run:

```text
raw_y
nonsplit flag
K-square flag
a
domain_line(a)
T_line(a) when domain_line(a)=+1
accepted candidate depth / survivor depth already tracked by GPU code
```

Report:

```text
raw candidates per second
K-cover rows per second
domain_line +1/-1
T_line +1/-1 inside domain
depth/survivor distribution for each of the four line-bit strata
```

Promotion bar:

```text
The domain-only filter beats baseline per GPU-second, and any deeper
post-domain stratum has a measured survivor lift that beats its throughput loss
per GPU-second on the same seed stream.
```

Kill condition:

```text
All four strata are flat after same-stream normalization.
```

Current CPU-side candidates:

```text
baseline mode: x16halvestatsnonsplit
first source mode: x16halvestatsnonsplitecover
first prefilter control: x16halvestatsnonsplittracedomain
secondary prefilter mode: x16halvestatsnonsplittraced
equivalent full-D instrumentation mode: x16halvestatsnonsplittracechar
domain_line meaning: first-halving square-root gate
ecover CPU net at depth 16 on two 1M seeds: about 1.31x to 1.35x
ecover CPU net at depth 18 on two 1M seeds: about 1.27x to 1.67x
domain-filter 1M CPU net at stable depths 16-19: about 1.29x to 1.39x
full-D 1M CPU net at stable depths 16-19: about 1.10x to 1.19x
```

This is enough to justify GPU A/B telemetry.  The ecover source is now the
first practical GPU test; domain-only/dgate is the control; full-D is
secondary.  For moonshot purposes, the same run should also report the next
one or two post-domain halving gates if the GPU implementation can expose them
cheaply.

Current CPU warning:

```text
T_line is flat at early post-domain depths on seeds 124 and 125.
Do not promote T_line unless GPU same-stream telemetry contradicts this with
much larger samples and a clear per-second gain.
```

Second-d update:

```text
Ask GPU for domain-only and domain+second-d A/B telemetry.
Ask GPU for label-2 `compactD=-1` as the named p27 second-gate selector.
Ask math/lit/expert lanes for a source or decomposition of the mixed
`R^2=criterion(X,W,T)` cover.
Do not continue tiny V+aU+b scans without a named theorem; the bound-3 sweep
was flat.
```

Tower update:

```text
Through eight selected halving gates, the obstruction is always chi(d_j);
no w_j obstruction or two-w branch appeared in the 1M p27 tower profile.
Practical GPU tests should measure fixed prefixes d1, d1+d2, d1+d2+d3.
The moonshot is a Kummer/2-cover/theta law enforcing many d_j=+1 conditions,
not another one-bit filter.
```

Label-2 cover update:

```text
Test compactD=-1 as the named p27 second-gate selector.
Do not use compactD=+1 except as a negative control.
Ask Sage/Magma for the genus and Jacobian decomposition of:
  W^2 = X^3-X
  T^2 = X(X^2+1)(X^2+2X-1)
  R^2 = W(X^2+1)(m0+mt_coeff*T)/X
The possible sqrt-beating bridge is a repeatable low-genus/source tower, not
the fixed d1+d2 filter by itself.
```

Genus/recurrence update:

```text
The first local probe prices the compactD cover at genus 17, and two
compactD=-1 streams show the next gate survives at ~1/2.
The small-prime trace probe explains the intermediate cover via W/T/WT after a
common-branch correction, but finds no small visible-factor combination for the
new Prym trace aD-aC.
The T-deck involution does have an exact order-4 lift to the full second-gate
cover; Riemann-Hurwitz gives D/<alpha> genus 1, so the second-gate object is a
cyclic quartic cover over E: W^2=X^3-X.
Next tests must look for special Prym/Jacobian decomposition, low-degree
quotients, or a genuine recurrence.  A fixed d1+d2 prefix is not a
sqrt-beating path.
```

Alpha/branch recurrence update:

```text
On 5,000 paired compactD=-1 rows, d2 had zero failures.
d3 was invariant across both paired T roots and both second-half x-branches,
but the plus rate was random-looking: 9864/20000 = 0.4932.
Conditioned on d3, d4 had the same invariant-branch shape:
10208/19728 = 0.5174.

Reason: the two half x-coordinates from a successful w branch multiply to 1,
so they have the same squareclass; since chi(d_next)=chi(x_next), branch
choice cannot change the next gate.

The d3 visible residual-E factor screen also found no exact GF(2) character;
the best screened combo was only 2548/5000 = 0.5096.
```

Updated kill rule:

```text
Do not spend a lane on branch-choice, T-deck-choice, or alpha-pair-choice
selectors for d3/d4.  The remaining possible win is a source or recurrence for
the descended x-square bit sequence itself.
```

U+2 prefix-gate update:

```text
For a successful halving step with x_next + 1/x_next = u,
  chi(x_next) = chi(u+2) = chi(u-2).

On the same 5,000-pair compactD sample, this formula had zero mismatches for
d2-to-d3 and d3-to-d4.

Potential GPU use:
  after the successful w branch is identified, test chi(u+2) before computing
  sqrt(w) and materializing x_next.

Measured reject shares:
  d3: 5068/10000 = 0.5068
  d4: 4760/9864 = 0.4826
```

Promotion bar:

```text
Only promote the u+2 precheck if it improves effective prefix survivors per
GPU-second after Legendre/sqrt cost.  As math, independent u+2 checks are still
constant-factor filters unless a recurrence couples many chi(u_j+2) bits.
```

GPU cost result:

```text
x16uprecheckprobe compiled cleanly, but lost per GPU-second.
depth 8:  baseline 36.89M accepted roots/sec, u+2 29.96M
depth 10: baseline 33.85M accepted roots/sec, u+2 27.84M
decision: do not promote independent u+2 precheck as a production filter
```

See [P27 GPU U+2 Precheck Probe](p27_gpu_uprecheck_probe_20260621.md).

U+2 sequence recurrence screen:

```text
Starting from 30,000 compactD/d2 rows, the selected u+2 sequence stayed at
half-loss through the stable-count range:
  gate 3: 0.5001
  gate 4: 0.4975
  gate 5: 0.4965
  gate 6: 0.5003

The prefix-success histogram is geometric-looking and no anomalies appeared.
```

Updated kill rule:

```text
Do not treat compactD as a gateway to biased later u+2 bits.  The remaining
sqrt-beating test must be multi-gate and non-local: a Kummer/theta/H90
relation or a source for the all-plus iterated 2-cover.
```

E-prime reciprocal quotient update:
[P27 E-Prime Reciprocal R-Quotient Branch Screen](p27_eprime_rquotient_branch_screen_20260621.md).

```text
The staged z-source equation is reciprocal in s=z^2.  With r=s+1/s, online
Magma reaches a dimension-1 r-quotient curve:
  D3_RQUOT_AFTER_FIRSTHALF_SCHEME 1 62 0

But the quotient itself is not the d3 selector.  On p27 train/heldout and
q1607/q1847/q2087:
  single_r_value = all usable rows
  r_discriminant_square = all usable rows
  d3 = chi(r+2) = chi(r-2), zero mismatches
```

Updated test card:

```text
Do not spend the next pass trying to make r itself selective.  The concrete
CAS target is the divisor/Kummer class of r+2 on the normalized r quotient,
or a recurrence/source for the sequence of r_j+2 classes.
```

Updated kill rule:

```text
Kill reciprocal-r quotient as a standalone d3 source; it quotients away the
squareclass.  Continue only if r+2 has a sourceable divisor class, low-genus
quotient, or multi-gate recurrence.
```

S-map quartic recurrence update:
[P27 S-Map Quartic Recurrence Probe](p27_smap_quartic_recurrence_20260621.md).

```text
With r=S^2-2, the all-plus reverse-doubling map is:
  x_prev = S^2*(S^2-4)/(4*(S^2+A-2)).

One more all-plus step gives a quartic F(Y) in Y=S_next^2.  Its discriminant is
a square times known degenerate divisors, and its nearest quadratic split has
discriminant 16*S^2*(S^2+A-6).

Guard fields q1607/q1847/q2087:
  every d3-plus row has four Y roots
  either all four Y roots are squares or none are
  this common root squareclass matches d4 with zero mismatches

p27 train/heldout:
  chi(S^2+A-6) is flat
  named quartic-factor GF(2) span has no exact train combo
  best train 0.5198 collapses to heldout 0.4898
```

Updated test card:

```text
The next serious beat-sqrt test is a resolvent/theta/Kummer formula for the
common squareclass of the four roots of F(Y), plus a recurrence comparison at
the next gate.  Do not continue named-factor products from the quartic.
```

Quadratic gate recurrence update:
[P27 Quadratic Gate Recurrence](p27_quadratic_gate_recurrence_20260621.md).

```text
The pair resolvent simplifies in the natural square-root coordinate:
  A = 2 - c^2
  x = r^2
  next_gate = chi(r^2 + c*r + 1)

Equivalently, each next all-plus gate is the conic condition:
  h^2 = r^2 + c*r + 1.
```

Validation:

```text
p27 train:
  gates 3-8 all matched, zero mismatches
p27 heldout:
  gates 3-8 all matched, zero mismatches
q1607/q1847/q2087:
  gates 3-4 all matched, zero mismatches
```

Updated test card:

```text
Build the conic-chain source/pullback:
  A = 2 - c^2
  x_j = r_j^2
  h_j^2 = r_j^2 + c*r_j + 1

Then decide whether this can be pulled back to the legal X1(16)/compactD
starting surface with low genus or a sourceable walk.  This is the current
best candidate for a real sqrt-beating structure.
```

D6 A-descent update:
[P27 Conic Tower D6 A-Descent](p27_conic_tower_d6_a_descent_20260622.md).

```text
After d4-plus/d5-plus, d6 has zero mixed A-groups on p27 1000/1000
train/heldout.  This promotes the conic test from generic pullback
normalization to a sharper A-level Kummer sequence problem:
extract and compare the d4, d5, and d6 quadratic classes on the normalized
A-cover.
```

Deeper A-prefix update:
[P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md).

```text
On 12000/12000 p27 train/heldout, gates d3..d14 have zero mixed A groups.
The robust range through about d10 remains near geometric half-loss, so the
next test is A-line Kummer class extraction or a low-degree A-character
falsifier, not GPU A-bucket production.
```

Updated kill rule:

```text
The recurrence is not by itself a win.  Kill only if the conic-chain pullback
is high/genus-generic or if deriving r_next still requires a fresh independent
cover at every step.
```

Conic-chain source update:
[P27 Conic-Chain Source Screen](p27_conic_chain_source_screen_20260621.md).

```text
Legal halving needs both conjugate conics:
  h_j^2 = r_j^2 + c*r_j + 1
  g_j^2 = r_j^2 - c*r_j + 1
  r_{j+1}^2 - (h_j+g_j)*r_{j+1} + 1 = 0

q7 Magma:
  depth 1 dimension = 2
  depth 2 dimension = 2
  depth 3 hits web memory

finite-field counts:
  q103/q263/q607 through depth 4: zero xDBL mismatches
  q1607 through depth 2: zero xDBL mismatches
  output projection stays near 0.5*q^2 rather than halving each depth

legal-source counts:
  q1607/q1847/q2087 depth 1 conic lift iff d3=+1
  q1607/q1847/q2087 depth 2 conic lift iff d4=+1 after d3
  full q7 E-prime pullback fixture hits web Magma memory before dimension
```

Updated test card:

```text
Do staged elimination for the label-2/compactD legal source equations:
  A = 2 - c^2
  x5 = r0^2
  h0^2 = r0^2 + c*r0 + 1
  g0^2 = r0^2 - c*r0 + 1
  r1^2 - (h0+g0)*r1 + 1 = 0

Avoid the all-at-once web-Magma pullback; it is too heavy.  The next decisive
test is whether staged elimination/normalization yields low-genus or
sourceable legal components.
```

U+2 norm/coboundary screen:

```text
The local norms through s -> -s are exact:
  Norm_s(u+2) = 4*x*(2-A)
  Norm_s(u-2) = -4*x*(A+2)
  Norm_s(u^2-4) = 16*x^2*(A^2-4)

But the selected w-square branch's u+2 bit is not in the local norm/branch
span:
  d3 best = 15054/30000 = 0.5018
  d4 best = 7540/15004 = 0.5025
```

Updated positive target:

```text
The local norm route is killed.  The first selected-orientation product route
has now also been screened below.  Continue only with a non-visible H90/theta
quotient or a source construction on the iterated cover.
```

Selected-orientation cocycle span screen:
[P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md).

```text
Two 30,000-row seeds allowed local characters plus selected s-branch
orientation characters from the successful prefix through gates 3-6.
No exact GF(2) product formula was found for the next selected u+2 bit.
Best low-weight products were small in-sample lifts and did not replicate as
the same named products across seeds.
```

Updated kill rule:

```text
Do not run more small selected-s orientation product scans at the same feature
depth.  The remaining H90 route must be a source/quotient on the iterated
cover, not a visible finite product of prefix characters.
```

Reverse-doubling all-plus source card:
[P27 Reverse-Doubling Source Screen](p27_reverse_doubling_source_screen_20260621.md).

```text
For a Montgomery halving step:
  x = (x_next^2 - 1)^2 / (4*x_next*(x_next^2 + A*x_next + 1)).

To source the next all-plus gate, set x_next=z^2:
  x = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1)).

For a legal rational half, also include:
  Y^2 = z^4 + A*z^2 + 1.
```

First screen:

```text
The equations are exact, but p27 density remains random-half:
  seed 20260621: d3_plus_rate = 0.4932
  seed 20260622: d3_plus_rate = 0.5044

Reverse source multiplicity matches the generic expectation:
  z-points per oriented compactD candidate ~= 2
  (z,Y)-points per oriented compactD candidate ~= 4
```

Updated concrete test:

```text
Intersect this reverse-doubled square source with the label-2 compactD=-1
source.  Ask Sage/Magma for components, genus, low-degree quotients, and
whether any component is dominated by an elliptic/rational walk or factors
through D/<alpha>.
```

First quotient update:
[P27 Reverse Source Quotient Screen](p27_reverse_source_quotient_screen_20260621.md).

```text
The d3/reverse-source bit descends perfectly to the residual elliptic quotient
E: W^2=X^3-X on 5,000 p27 fibers.

But the cheap degree-1 line-character source is killed:
  p27 small-coeff lines: exact_lines = 0, best = 0.5128
  GF(607) all projective lines: exact_lines = 0 over 369,057 lines
```

Updated remaining test:

```text
Identify the actual E-level divisor/theta/Kummer class for the descended bit,
or compute the E-level source-cover genus/quotients and show it is generic.
Then test whether d4 reuses the same character after a named transformation.
```

D4 recurrence update:
[P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md).

```text
d4 also descends to E after d3:
  p27 d3-positive E fibers = 2466
  d4 plus/minus = 1276/1190
  d4_not_descended_to_E = 0

But:
  p27 small degree-1 line screen: exact_lines = 0, best = 0.5312
  q=607,863,991 make d4 constant, so simple-transform exactness there is
  degenerate and not promotion evidence.
```

Sharper remaining test:

```text
Derive explicit E-level functions/classes f3(X,W), f4(X,W), compare divisors
or Kummer classes, and ask whether f4 is a translate/pullback of f3 on a
non-degenerate validation field.
```

Named E-basis update:
[P27 E-Quotient Kummer Basis Screen](p27_equotient_kummer_basis_screen_20260621.md).

```text
Visible torsion / 2-descent / order-4 H90 products are killed:
  p27 d3 exact_combos = 0
  p27 d4 exact_combos = 0
  d3 train-best on heldout = 0.5044
  d4 train-best on heldout = 0.5075
  q=1087,1471,1607 exact_combos = 0 for d3 and d4
```

Updated remaining test:

```text
Use Magma/Sage function fields to extract the actual E-level double covers for
d3 and d4, then compare their divisor/Kummer classes.  Do not spend more on
visible product scans unless a new theorem supplies a named function.
```

Low-pole pilot update:
[P27 E-Quotient Low-Pole Random Screen](p27_equotient_lowpole_random_screen_20260621.md).

```text
Small random L(nO) sections/products did not find f3/f4:
  exact_candidates = 0 for p27 d3/d4 at pole bounds 5 and 7
  best heldout d3 = 0.5275
  best heldout d4 = 0.5390
```

This is a bounded negative, not a proof of absence.  It reinforces that the
next serious extraction should be symbolic/function-field based, using the
online Magma calculator for small-field validation when convenient, or use a
faster finite-field solver on non-degenerate small fields before p27
validation.

Exact two-line follow-up:
[P27 E-Quotient Line-Product Screen](p27_equotient_line_product_screen_20260621.md).

```text
Products of two projective lines on E do not explain the quotient bits:
  d3 exact pairs = 0 over q=607, q=1087, q=1471
  d4 exact pairs = 0 over q=1471
  q1087 d4 has 9 exact pairs on only 40 rows, killed by q1471
```

This kills the reducible-conic source subclass.  If the finite-field route
continues, test irreducible conics or extract the divisor class directly.

Affine-walk recurrence update:
[P27 E-Quotient Affine-Walk Recurrence](p27_equotient_affine_walk_recurrence_20260621.md).

```text
All maps P -> [m]P + Q were tested for m=+/-1,...,+/-8 and all Q in E(F_q):
  q=1087: best full coverage = 20/40 = 0.500000000
  q=1471: best full coverage = 56/112 = 0.500000000
  q=1607: best full coverage = 76/112 = raw d4 bias
  nontrivial walks reaching 0.75 coverage = 0
```

This kills the small elliptic-walk recurrence as a sqrt-beating source.  The
remaining quotient work is cover/divisor-class extraction, not a translated
low-multiple walk on `E`.

Kernel-8 / 2-isogeny update:
[P27 E-Quotient Kernel-8 / 2-Isogeny Screen](p27_equotient_kernel8_2isogeny_screen_20260621.md).

```text
Positive:
  p27 d3/d4 are invariant under the rational (0,0) translation in-domain
  quotient coordinates: U=X-1/X, V=W(X^2+1)/X^2
  quotient curve: V^2 = U^3 + 4U

Negative:
  q1471/q1607 exact lines on E' = 0
  q1471/q1607 exact two-line products on E' = 0
```

This is the current best quotient-theory lead.  It does not beat sqrt by
itself, but it moves the function-field extraction from `E` to the smaller
2-isogenous quotient `E'`.

E-prime low-pole update:
[P27 E-Prime Low-Pole Random Screen](p27_eprime_lowpole_random_screen_20260621.md).

```text
P27 exact candidates on E' low-pole sections/products = 0
best p27 heldout d3 lift = 1045/2000 = 0.522500000
best p27 heldout d4 lift = 557/1052 = 0.529467681
q1471/q1607 exact candidates = 0
```

This kills the random low-pole `E'` pilot as a sqrt-beating source.  The
quotient remains valuable because it gives the right smaller curve for exact
function-field extraction and divisor/Kummer class comparison.

E-prime affine-walk update:
[P27 E-Prime Affine-Walk Recurrence](p27_eprime_affine_walk_recurrence_20260621.md).

```text
tested maps: P -> [m]P + Q on E', |m| <= 8, every Q in E'(F_q)
fields: q=1471,1607,1847
full-coverage maps: only m=+/-1, Q=O
best full-coverage rates: 28/56, 38/56, 52/90
nontrivial exact overlaps: low coverage only, at most about 21%
```

This kills the small `E'` affine-walk recurrence as a sqrt-beating source.
The remaining quotient route is cover/divisor-class extraction, not a
translated low-multiple walk.

E-prime branch-factor update:
[P27 E-Prime Branch-Factor Span](p27_eprime_branch_factor_span_20260621.md).

```text
tested: sparse products of size 1..4 from p26 visible branch/H90 factors on E'
p27 exact products = 0
q1471/q1607/q1847 exact products = 0
best 2k p27 d4 lift = 592/1052 heldout
fresh 20k validation of that product = 5100/10122 and 5076/10056
p26 branch packet on fresh p27 d3 = exactly 10000/20000 and 10000/20000
```

This kills the visible p26 branch-factor transfer as a sqrt-beating source.
The remaining quotient route is actual cover/divisor-class extraction on `E'`.

E-prime twist-obstruction update:
[P27 E-Prime T-Cover Twist Obstruction](p27_eprime_tcover_twist_obstruction_20260621.md).

```text
sigma(X,W)=(-1/X,W/X^2)
T^2 = S = X*(X^2+1)*(X^2+2X-1)
sigma(S)/S = X^-6
sigma(T)=+/-T/X^3

A rational T-linear invariant T*f over E' would need:
  sigma(f)/f = +/-X^3

But:
  Norm(+X^3) = -1
  Norm(-X^3) = -1
```

For the p27-compatible guard fields `q=607,1471,1607,1847`, `chi(-1)=-1`,
so this obstruction is real over the base field.  This explains why plain
`E'` searches can fail even if the quotient route is still alive.  The online
Magma `q=1471` validation reports:

```text
RESULT p27_eprime_tcover_twist_q1471 ok -1 1660 0 0 0 0 0
```

Updated quotient test:

```text
Stop repeating plain E' low-pole or sparse branch-factor screens.
Build the twisted T-cover quotient/Prym/Hilbert-90 class, allowing j^2=-1 over
F_{q^2}.  The concrete first model is:
  h = 1 - j/X^3
  Z = T*h
  sigma(Z) = jZ
Then ask whether the d3/d4 double covers become named order-4 eigenspace
classes that descend back to the p27 sign regime.
```

Visible eigenspace update:
[P27 E-Prime Twisted Eigenspace Screen](p27_eprime_twisted_eigenspace_screen_20260621.md).

```text
Using j^2=-1 and Z=T*(1-j/X^3), the first packet screen tested:
  Z, Z^2, Z^4
  Z +/- branch_factor
  Z^2 +/- branch_factor
  Z^4 +/- branch_factor
  Z * branch_factor
  base-field components of Z^4

Guard fields:
  q=1471,1607,1847

Result:
  d3 exact packets = 0 in all three fields
  d4 exact packets = 0 in all three fields

The best scores were field-dependent or raw-majority artifacts, e.g. q1471
d4 had 160/224 for Z4+U-1, while q1607/q1847 winners were often Z2/Z4/base
components tracking raw target bias.
```

Updated kill rule:

```text
Stop visible Z/Z2/Z4 branch-factor packet scans.  The next meaningful test is
the actual divisor/Kummer/Prym class of the d3 and d4 double covers on the
twisted T-cover/eigenspace model, followed by a guard-field exactness check.
```

Signed-doubling Kummer update:
[P27 E-Prime Signed-Doubling Kummer Screen](p27_eprime_signed_doubling_kummer_screen_20260621.md).

```text
On E': V^2=U^3+4U, both d3 and d4 descend to signed [2] projection classes in
all 12 tested non-degenerate guard fields.

The quotient coordinate is:
  K = x([2]P) = (U^2-4)^2/(4*U*(U^2+4)).

Main guard fields:
  q=1471: d3 100 -> 50 K rows; d4 56 -> 28 K rows
  q=1607: d3 98  -> 49 K rows; d4 56 -> 28 K rows
  q=1847: d3 126 -> 63 K rows; d4 90 -> 45 K rows

Exhaustive K-polynomial screens:
  degree 1 exact = 0 for d3/d4 over q=1471,1607,1847
  degree 2 exact = 0 for d3/d4 over q=1471,1607,1847
```

Updated concrete test:

```text
Search exact degree 3/4 K-polynomial characters for d3 and d4.
An exact cubic or quartic gives z^2=f(K), a genus-1 source candidate.
If degree 3/4 fails on q=1471 and q=1607, move to divisor/Kummer extraction on
the K-line rather than returning to plain E' visible scans.
```

Small-integer K-polynomial update:
[P27 Kummer Small-Integer Polynomial Screen](p27_kummer_small_integer_poly_screen_20260621.md).

```text
Tested one shared primitive integer polynomial shape across q=1471,1607,1847,
with coefficients in [-8,8] and field-dependent polarity allowed.

Exact all-field formulas:
  d3 degree 3 = 0
  d3 degree 4 = 0
  d4 degree 3 = 0
  d4 degree 4 = 0

Best minimum guard-field rates:
  d3 degree 4: about 0.667
  d4 degree 4: about 0.714
```

Updated next test:

```text
Do not simply widen small coefficient bounds.  Recover the actual K-line
branch divisor/Kummer class for d3, determine its minimal degree, then compare
the d4 branch divisor after d3.  Promote only an exact branch polynomial/class
or a recurrence/source relation that survives q=1471 and q=1607.
```

Branch-divisor update:
[P27 Kummer Branch-Divisor Screen](p27_kummer_branch_divisor_screen_20260621.md).

```text
Tested exact squarefree products of:
  rational linear factors in K
  irreducible quadratic factors in K over F_q
with total degree <=4.

d3:
  q1471 exact divisors = none
  q1607 exact divisors = none
  q1847 exact divisors = none

d4:
  q1471/q1607 have degree-3 local fits
  q1847 exact divisors = none
```

Updated kill rule:

```text
Kill the split degree <=4 K-line branch-divisor source.  The remaining K-line
route is irreducible cubic/quartic extraction or Magma/Sage recovery of the
actual branch divisor/genus, not more visible split-factor screens.
```

K-line degree-one recurrence update:
[P27 K-Line Affine Recurrence Screen](p27_kline_affine_recurrence_20260621.md).

```text
Tested all K -> a*K+b and K -> a/K+b maps.

q1607:
  affine full coverage = identity only, 19/28 raw d4 majority
  reciprocal full coverage = 0, best coverage = 6/28

q1847:
  affine full coverage = identity only, 26/45 raw d4 majority
  reciprocal full coverage = 0, best coverage = 7/45

q2087:
  affine full coverage = identity only, 18/25 raw d4 majority
  reciprocal full coverage = 0, best coverage = 6/25

q2039:
  identity exact only because d4 is constant
```

Updated kill rule:

```text
Kill degree-one rational K-line recurrences as a d4-from-d3 source.  The next
K-line work must be actual branch-class/genus extraction, not affine or
reciprocal-affine bucket searches.
```

Reverse-root relation update:
[P27 K-Line Reverse-Z Relation Screen](p27_kline_reverse_z_relation_20260621.md).

```text
Kept the actual d3 source root x6=z^2 and tested:
  (K,z), (Sroot,z), (K,x6), (Sroot,x6),
  (K,r), (Sroot,r), r=x6+1/x6,
  (K,z+1/z), (Sroot,z+1/z),
  (K,z-1/z), (Sroot,z-1/z).

q1607/q1847/q2087:
  main systems full-rank through degree 20
  q1607 has non-repeating degree-20 artifacts in lower projections only

p27 1000-row sample:
  7744 z rows
  all systems full-rank through degree 12
```

Updated kill rule:

```text
Kill obvious plane-model shortcuts for the K/Sroot branch cover.  The next
K-line work must be normalization / branch divisor / genus extraction.
```

Reverse-root extension-count update:
[P27 K-Line Reverse-Z Extension Counts](p27_kline_reverse_z_extension_count_20260621.md).

```text
Validated against q607 and repeated on q1607/q1847/q2087 plus GF(7^n),
GF(23^n).  Every nonempty guard field has:
  z_rows/unique_K = 64
  z_rows/unique_S = 32
  unique_Ax/unique_A = 4

This confirms that K/S is a structured constant-degree projection of the
actual reverse-root cover, but unique_K and unique_S still grow at field-size
scale.  K/Sroot enumeration is therefore not a below-sqrt sampler.
```

Updated action:

```text
Do actual branch/genus/CAS extraction for the constant-degree K/S cover.
Do not spend GPU time on K/S bucket searches unless a new quotient or
recurrence is named first.
```

Reverse-root fiber-profile update:
[P27 K-Line Reverse-Z Fiber Profile](p27_kline_reverse_z_fiber_profile_20260621.md).

```text
q1607/q1847/q2087:
  every K fiber has 64 rows, one selected A, four (A,x), eight x6,
    sixteen z, and four r values
  every Sroot fiber has 32 rows, one selected A, four (A,x), eight x6,
    sixteen z, and four r values
  anomalous_fibers = 0 for all tracked histograms

Sroot is the cleaner extraction coordinate; K can merge A-values in small even
extensions, while Sroot separates them.
```

Updated action:

```text
Prioritize offline normalization over P1_Sroot with K as a quotient check.
Do not run rational K/Sroot fiber-anomaly searches or GPU K/S buckets.
```

K/A base-curve and GPU quadratic-gate update:
[P27 K/A Map And GPU Quadratic-Gate Update](p27_kline_a_map_and_gpu_quad_20260622.md).

```text
With L=K^2, the d2/base source satisfies:
  64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0

discriminant_L:
  256(A+2)(A+6)^2(A^2+60A+132)^2

This explains the flat K/Sroot fibers but is not the d3 selector.  The formula
vanishes on both d3-plus and d3-minus rows in p27 train/heldout and
q607/q1607/q1847/q2087.
```

GPU result:

```text
branch: codex/add-cuda-p26-search
commit: e153fd1 Add p27 quadratic gate GPU probe
checked gates: 7,874,715
gates: 3..8
mismatches: 0
source-normalized target rate: flat/slightly lower
```

Updated action:

```text
Do not run a larger production GPU search from this formula alone.
Next GPU use requires either a direct legal-pullback sampler into the
recurrence-coordinate domain or a measured multi-gate coupling law.
```

Base-curve sampler update:
[P27 K/A Base-Curve Sampler Probe](p27_kline_base_curve_sampler_20260622.md).

```text
q1607/q1847/q2087:
  base_KA = q
  realized legal d2 K/A = 49, 63, 57
  all realized legal K/A points lie on the base curve
  natural K/A squareclass atoms up to weight 4 do not select the legal subset
```

Updated action:

```text
Use the K/A equation as a normalization coordinate.
Do not ask GPU to sample the base curve directly; it mostly produces non-legal
points and does not avoid the legal-cover toll.
```

B-parameter follow-up:
[P27 B-Parameter Base-Curve Sampler Probe](p27_kline_base_param_sampler_20260622.md).

```text
A = B^2 - 2
branch0: L = -(B + 2)^4 / (8 B (B - 2)^2)
branch1: L =  (B - 2)^4 / (8 B (B + 2)^2)

stable all-recall bucket:
  atoms = K, B+2, B-2, L
  bits  = 0, 0,   1,   0

q1607/q1847/q2087:
  d2 all-recall lift ~= 8.04x
  d3plus all-recall lift ~= 8.04x
```

Updated GPU action:

```text
Yes to a bounded same-stream GPU telemetry probe of the B bucket if it is cheap
to emit the four squareclass bits along the existing p27 path.
No to a larger production GPU run from this alone: the win is constant-factor,
not below-sqrt, and the sharper partial buckets are field-sensitive.
```

B-next-gate update:
[P27 B-Parameter Next-Gate Probe](p27_kline_base_param_nextgate_20260622.md).

```text
p27 train/heldout:
  legal rows all stay in the core B bucket
  d3 train-best combo does not hold out
  d4 train-best combo weakens to about 1.015x majority-lift on heldout

q1607/q1847/q2087:
  small-field winners disagree
```

Updated action:

```text
Do not ask GPU to score B-atom next-gate buckets.
The next beat-sqrt test is CAS/function-field extraction of the legal cover
over the B-rationalized base curve, looking for genus <= 1 quotient,
sourceable walk, or repeated multi-gate coupling.
```

B-source descent update:
[P27 B-Source Descent And Branch Support](p27_b_source_descent_and_branch_20260622.md).

```text
B = 8X^2/(X^2 - 1)^2
A + 2 = B^2
d3 descends to Bplus on legal d2 rows
d4 after d3 also descends to Bplus in tested samples
```

Negative branch support:

```text
d2 legal on core B:
  no product of <=4 rational linear factors over q1607/q1847/q2087

d3 on legal B:
  no product of <=4 rational linear factors over q1607/q1847/q2087
  no one irreducible quadratic times <=2 rational linear factors over
  q1607/q1847/q2087
```

Updated action:

```text
Promote B-line Kummer-class extraction as the next theorem/CAS card.
Do not continue visible B-factor bucket scans unless they are part of a
structured divisor extraction.
```

B-line deep descent update:
[P27 B-Line Extension Counts And Deep Descent](p27_b_line_extension_and_deep_descent_20260622.md).

```text
extension counts:
  legal_B_missing_core = 0 in all nonempty GF(7^n), GF(23^n) tests
  B_d3_mixed = 0
  B_d4_mixed = 0
  legal_B is still field-sized, roughly 0.03N in informative odd extensions

p27 deep descent:
  original Bplus determines active selected gate bits through d12
  no mixed B groups in p27 train/heldout
```

Updated action:

```text
Promote B-line Kummer sequence extraction:
  f3(B), f4(B), f5(B), ...
Compare these classes for recurrence/coupling.
Only use GPU for bounded Bplus + deep-bit telemetry until exact classes exist.
```

K/S first-half cover update:
[P27 K/S First-Half Cover Magma Smoke](p27_ks_first_half_cover_magma_20260621.md).
[P27 K/S First-Half Alpha-Lift Obstruction](p27_ks_first_half_alpha_lift_obstruction_20260621.md).
[P27 K/S First-Half E-Prime Descent](p27_ks_first_half_eprime_descent_20260621.md).
[P27 E-Prime First-Half Pullback Magma Smoke](p27_eprime_first_half_pullback_magma_20260621.md).
[P27 E-Prime D3 Z-Source Magma Smoke](p27_eprime_d3_zsource_magma_20260621.md).
[P27 E-Prime L(4O) Exact Section Screen](p27_eprime_l4_section_exact_screen_20260621.md).
[P27 E-Prime U-Cubic Exact Screen](p27_eprime_ucubic_exact_screen_20260621.md).

```text
Full q7 reverse-source fixture: online Magma memory limit.
Eta=+1 component fixture: online Magma memory limit.
Raw first-half layer: SCHEME_OK 2 4, AFFINE_POINTS 77.
Saturated first-half layer:
  SAT_SCHEME_OK 1 42 3
  SAT_CURVE_OK 37 3
```

Updated K/S interpretation:

```text
The unsaturated handoff equations contain denominator/projection artifacts.
After saturating by X*(X-1)*(X+1)*(T-2X^2), the first post-alpha layer is a
genus-37 curve over tiny p27-signature q=7, before adding final reverse-square
variables z,Y.  This is not a promotion-field theorem, but it is strong
negative pressure on a direct low-genus K/S source.

The first-half B-cover branch class also factors exactly:
  32*T*X*(eta*T*W + X*(X-1)*(X+1)^2)
          *(2*eta*W*X + X^3 + X^2 - X - 1).
For eta=+1, the same-eta alpha lift ratio is -1 times a square on the
intermediate curve.  Since p27 is 3 mod 4, this lift is not F_p-rational.
The eta-swapped ratio is mixed on q=1607, q=1847, and q=2087.

Positive quotient update: translation by `(0,0)` sends
`X -> -1/X`, `W -> W/X^2`, and `T -> +/-T/X^3`.  It preserves compactD and
the first-half B-branch squareclass on every compactD point over
q=1607/q1847/q2087 tested.  Online Magma q1607 reports:
`BRANCH_FACTOR_DIFF_ZERO true`, `T2_TRANSFORM_ZERO true`, and
`COUNTS 800 800 1600 0 0 0`.

However, the explicit E' pullback of the eta=+1 first-half layer still reports
`EPRIME_PULLBACK_SAT_SCHEME 1 61 0` and `EPRIME_PULLBACK_SAT_CURVE 37 0`
over q7 after saturation.

The actual d3 z-source is now staged:
  all-at-once saturation: memory limit after raw dimension 3
  sequential saturation: memory limit
  first-half-saturation then reverse_z: `D3_Z_AFTER_FIRSTHALF_SCHEME 1 62 0`
Genus/normalization of this curve is the concrete offline CAS ask.

The nearest exact low-pole source family on E' is killed: sections
`a+bU+cU^2+dV` in `L(4O)` have zero exact d3 formulas on q599/q727/q919.
The q487 exact quadratic-U sections do not survive and are local artifacts.

The next rational U-line loophole is also killed.  Exact U-cubics appear in
some small fields, including one q599 formula and many q487/q727 formulas, but
there are zero exact U-cubics on q919, q967, and q1063.
```

Updated K/S next test:

```text
Do not continue visible K/S coefficient or branch-product scans.
Do offline Magma/Sage quotient/decomposition only with a sharper target:
  normalize the staged d3 z-source J = Iclean + <reverse_z> on E',
  compute branch divisor / Kummer class / genus beyond L(4O),
  and d4 fresh-cover vs recurrence testing.
Do not treat E' descent alone as a low-genus source; the staged first-half
pullback remains genus 37.
Do not widen univariate U coefficient searches without a divisor-class reason.
Promote only if a low-genus quotient, named recurrence, or sourceable walk
survives over F_p on p27-signature fields.
```

Updated K/S kill condition:

```text
No useful quotient of the genus-37 first-half layer, or d4 is a fresh
unrelated cover after the d3 class is named.  A quotient that exists only
after adjoining sqrt(-1) is diagnostic but not a direct p27 sampler unless it
comes with an explicit F_p descent.
```

Promotion bar:

```text
The d3 all-plus source has a cheap walk or low-degree quotient that samples
d1+d2+d3 without paying an independent 1/2 loss for d3.
```

Kill condition:

```text
The reverse-doubled compactD source is a generic high-genus cover with no
useful quotient.  The finite-field density screen alone already matches a
random 1/2 cover, so do not promote reverse doubling without quotient data.
```

Order-4 quotient card:

```text
Ask Sage/Magma for the quotient by:
  alpha(X,W,T,R) =
    (X, W, -T, R*(m0-mt*T)/(2*T*(W(X+1)+2X^2))).

Report fixed points, verify genus(D/<alpha>)=1, identify the quotient with
E=(X,W), and derive the cyclic quartic character/function over E controlling
compactD=-1.  Promote only if that elliptic cyclic-quartic structure gives a
cheap source, a better-than-random character test, or a repeatable recurrence
for more d_j gates.
```

E[2] packet source update:

```text
The obvious rational E[2] packet route is killed on p27.
It gives exact algebra and ~2x candidate lift, but 1.0x source lift through
depth 24 on the 200k-source run.  Do not count this as sqrt-beating.
```

E[3] coset source update:

```text
The residual E[3] coset route is also not promoted.
Coset0 had one positive 2M tail, but the independent 2M replication failed.
Combined lift is small/unstable: about 1.02x at d16 and 1.12x at d18-d20.
Treat it as a low-priority GPU telemetry column only if essentially free.
```

Visible residual-E character update:

```text
The natural H90 factor span on E does not explain compactD.
Across 1904 small-field rows, no exact GF(2) character combo exists; the best
screened combos are only about 55%.
```

P26 GPU trace/norm lesson:

```text
The p26 D_trace=+1 stratum is real: it captured all observed depth-20 through
depth-28 survivors in three 100M raw-y streams and gives essentially 4x
conditional enrichment.

It is not yet a production win: the best filter-only path ran at about
4.47M candidate roots/sec versus 31.87M accepted roots/sec for the no-trace
baseline.

For p27, every ecover/domain/compactD/order-4 test must report effective
survivors per GPU-second.  Prefer a direct sampler, cheaper algebraic test, or
d3/d4 recurrence over an expensive classifier-only rejector.
```

W-obstruction update:

```text
For nonsplit Montgomery rows, w_+*w_-=16*x^2*(A^2-4), so the two w candidates
have opposite squareclass.  Thus d_j square implies exactly one w_j branch
except at degeneracies.  Do not spend a lane searching for an independent
w_j predictor.
On the successful w branch, the two x halves multiply to 1, so they also
cannot be used as a selector for the next x-square bit.
```

X-square update:

```text
Because y^2=x*d on E_A, chi(d_j)=chi(x_j) for nondegenerate F_p points.
The prefix tests should be phrased as x-coordinate square tests:
  x_4 square, x_5 square, x_6 square, ...
The moonshot is an iterated 2-descent source, not an independent d/w filter.
```

P26 GPU seed-law update:

```text
The p26 replay/stratum probe recovered the hit and logged source telemetry, but
identity/splitmix/mixed seed order and the hit compact bucket were negative.
Do not assume p27 has a seed-order shortcut without a mathematical invariant.
```

## Card 2: Named Cover / Spin Candidate Evaluator

The Magma spin check now says `domain_line` is not naturally a plain
low-degree rational character on the `a`-line.  For
`F=t*(t^2+2t-1)*(t^2+1)`, `F(t)/F(-1/t)=t^6`, so the character descends, but
`F` has odd valuation at the ramification factor `t^2+1`.  Treat this as a
half-divisor / spin class on the trace/norm quotient.

The existing p27 evaluator is still useful for named rational functions:

```text
R(a) = numerator(a) / denominator(a)
```

and tests:

```text
chi(R(a)) = domain_line(a)
chi(R(a)) = T_line(a)
chi(R1(a)) = domain_line(a) and chi(R2(a)) = T_line(a)
```

The first basis should not be arbitrary high-degree fitting.  Start with
branch-divisor-shaped functions supported on:

```text
a = 0
a = +/-2
a^2 + 4 = 0
infinity
```

and their theta/divisor descendants on `b^2 = 16 - a^4`.

Status: evaluator added as
`research/p27/archive/gates/p27_line_rational_evaluator.py`.  Default visible
branch functions are negative, and the spin check explains why blind `R(a)`
fitting is likely mis-targeted for `domain_line`.

Updated first-class target:

```text
construct the actual double covers / divisor classes over
  C: b^2=16-a^4
  E: v^2=u^3-u
for domain_line and normalized T_line, then test whether their sum/product
gives a sourceable D_plus stratum.
```

Current named D_plus cover:

```text
t = y - 1
B = t^2 + 1
C = t^2 + 2t - 1
z^2 = t*C*B
eps_h = chi(t)
eps_v = chi((t+1)*C)
hcore = C*B + eps_h*2*t*z
vcore = 2*C*t^2 + eps_v*z*w
core = (1-t^2)*B*C*(t+1)*vcore*hcore
D = -chi(core)
D_plus iff -core is square
```

The p27 probe has zero mismatches on `16,096` rows, and the online Magma
`q=607` validation has `mismatch=0`.  The C depth histogram now identifies
`D_plus` as an exact two-gate prefix: all Dplus-filtered rows survive through
depth `6`, then return to geometric half-loss.  The domain spin quartic
obtained by eliminating `t`,

```text
r^4 - (a+2)(a^2+1)(a^2+4)r^2 + (a+2)^2(a^2+4) = 0,
```

has projective genus `2` in the q=607 check.

Next concrete test:

```text
Split the D_plus cover by eps_h,eps_v in {+1,-1}; ask Magma/Sage for genus,
quotient maps, and Prym/Jacobian decomposition of each orientation component.
```

Status update:

```text
The direct source-orientation cover is not cheap.
Adding u_h^2=eps_h*t and u_v^2=eps_v*(t+1)C gives a degree-16 genus-21 base.
After the final Dplus square root, Riemann-Hurwitz predicts genus 69 for every
sign component.
```

So the next test is not "sample the full cover"; it is:

```text
find a low-genus quotient/Prym factor that still remembers Dplus and couples
to later selected x-square gates.
```

Post-Dplus update:

```text
The immediate named-character version of that test is negative.
On 16,398 C-style Dplus candidates, Dplus had zero first-two-gate failures,
but d3_plus was 8298/16398 = 0.5060 and d4_plus after d3 was
4062/8298 = 0.4895.

All low-weight products of H,VQ,X_pref,T_line/root/quotient atoms failed for
d3 and d4; train lifts collapsed to about 0.49-0.50 on heldout.
```

Updated next concrete test:

```text
Do not run another low-weight post-Dplus sign scan.
Extract the actual d3 and d4 double-cover divisor/Kummer classes on
  E:  W^2 = X^3 - X
or on the 2-isogenous quotient
  E': V^2 = U^3 + 4U, U = X - 1/X.

Use online Magma for small-field validation once there is a named formula or
component map, as in the p24 workflow.
```

Promotion bar:

```text
zero mismatches on prefix and held-out p27 line samples or a small-field Magma
cover validation, plus a cheap way to sample or enumerate the selected stratum
without paying sqrt(p) again.
```

Kill condition:

```text
only post-hoc high-degree interpolation, another blind low-degree R(a) scan,
or a filter whose cost/loss cancels the lift.
```

## Card 3: Branch-Divisor / Theta Ask

Formulate the expert/literature ask as:

```text
On C: b^2 = 16 - a^4, equivalently E: v^2 = u^3 - u with u=4/a^2,
over F_p with p = 10^27 + 103, is there a known divisor/theta/additive
identity whose squareclass gives either domain_line(a), T_line(a), or their
simultaneous +1 stratum?
```

Do not ask for "anything relevant to p27."  The ask is specifically about the
line-level pair produced by the trace/norm quotient.

Promotion bar:

```text
a named identity that can be converted into Card 2 and checked on held-out rows.
```

Kill condition:

```text
a source-only certification that does not produce the finite-field squareclass
or selected stratum.
```

## Card 4: Practical Baseline Before Any Giant GPU Run

Before using GPU for a large hunt, run a tiny p27 baseline and report:

```text
p
seed base / cap
raw X1(16) curves tested
accepted candidates
candidate rate
verifier path if hit
```

Promotion bar:

```text
clean p27 telemetry and no branch/sign mismatch.
```

Kill condition:

```text
do not spend a large run debugging p27 target plumbing.
```

Status: CPU stats plumbing passed.  GPU plumbing remains to be checked.

## Card 5: Small Torsion / Coset Explanation

Test whether either line bit is explained by small torsion projections on
`E(F_p)`.

Status: negative.  `p27_trace_norm_elliptic_coset_gate.py` verifies the
supersingular order behavior but every small class for `m=2,3,4,6,12` is mixed;
class lift is flat.  Do not spend more effort on small torsion unless a named
identity changes the target.

Large-factor follow-up is also negative.  The p27-specific factor `345451` and
small multiples through `12*345451` have mixed repeated projection classes;
see [P27 Elliptic Large-Factor Collision Audit](p27_elliptic_large_factor_collision_20260621.md).

Continue only with a named theta/divisor/additive identity, not another
quotient-class lookup.

## Card 6: First 2-Isogeny Visible-Divisor Span

Test whether either line bit is a product of visible branch and first
2-isogeny characters:

```text
phi0  = u - 1/u
phi1  = u*(u + 1)/(u - 1) - 2
phim1 = u*(u - 1)/(u + 1) + 2
```

Status: negative.  The `65,536`-product span has no exact survivors for either
`domain_line` or `T_line`; best lifts are only about `1.03x`.

Follow-up: the first low-pole random screen on the 2-isogenous quotient `E'`
is also negative.  Pole bounds `5,7,9` produced no exact p27 or guard-field
candidate; best p27 heldout lifts remain below sampler promotion.

Follow-up: the first affine-walk recurrence screen on `E'` is also negative.
All maps `P -> [m]P+Q` with `|m|<=8` and every `Q` over
`q=1471,1607,1847` fail to give a high-coverage d4-from-d3 recurrence.

Follow-up: the p26 visible branch/H90 packet does not transfer to p27.  Sparse
branch products of size `1..4` have no exact p27 or guard-field formula, and
fresh 20k validation flattens the mild 2k d4 lift.

Continue only with a named non-visible theta/divisor/additive identity.

## Card 7: Half-Norm / Descent Torsor

Use the algebraic form:

```text
t = y - 1
a = t - 1/t
domain_line = chi((a + 2)(t^2 + 1))
sigma(t) = -1/t
sigma(t^2 + 1)/(t^2 + 1) = 1/t^2
Norm(t^2 + 1) = a^2 + 4
```

This is the first clean explanation for why the domain bit descends without
being a visible rational character in `a`.

Concrete ask:

```text
Find a half-norm/descent, theta, or additive identity that trivializes this
torsor or couples it to T_line on E: v^2 = u^3 - u.
```

Status: active theorem front.  The visible joint/product character shortcut is
negative; the joint rows are exactly the domain-positive rows, so the remaining
selector is `T_line=+1` inside the domain.

Additional status: the easy quotient automorphisms preserve `domain_line`,
including `a -> -a`, but do not close `T_line`; see
[P27 Quotient Automorphism Orbit Audit](p27_quotient_automorphism_orbit_20260621.md).

Practical status: `domain_line=+1` is now a measured depth-16 gate on p27 CPU
streams and gives the best current practical filter; see
[P27 Practical Domain-Line Filter](p27_practical_domain_filter_20260621.md).

## Card 8: T-Line Component Coupling

Use the component split:

```text
D = -x_pref * vq * h
T = D * chi(y)
pref = -x_pref*chi(y) = chi(y - 2)
T = chi(y - 2) * h * vq
```

Measured descent behavior:

```text
vq(a,-b) / vq(a,b) = chi(a)
h(a,-b) / h(a,b) = 1
pref(a,-b) / pref(a,b) = 1
```

Concrete ask:

```text
Find a half-norm/descent, theta, or additive identity that couples the
b-invariant factor chi(y-2)*h with the vq factor whose b-flip cocycle is chi(a).
```

Status: active theorem front, narrowed by
[P27 Component Norm / Half-Norm Audit](p27_component_norm_halfnorm_audit_20260621.md).
`h`, `vq`, `pref`, and `D` alone are not the missing selector.  Their visible
norm squareclasses and degree `<=4` products of the named branch/norm atoms do
not explain `T_line`.  The positive handle is now the involution boundary in
[P27 Component Involution Boundary](p27_component_involution_boundary_20260621.md).

## Card 9: H/V Phase Coupling Identity

Use the two half-norm arguments:

```text
H = 4 C B + 8 t z
V = 8 y C t^2 + 4 y z w
z^2 = F = t C B
w^2 = K = -C R
```

Their norms reduce to visible branch classes:

```text
Norm_z(H) = 16 C B (t - 1)^3 (t + 1)
Norm(V)  = 16 y^2 C^2 t (t + 1)^3 (t - 1)
```

So the next theorem cannot merely identify a norm squareclass.  It must control
the phase/sign of `H` and `V` together after the `T_line` normalization.
The current exact boundary is:

```text
sigma(t) = -1/t
pref(sigma) / pref = -chi(a)
(h*vq)(sigma) / (h*vq) = -chi(a)
T(sigma) / T = 1
```

Concrete ask:

```text
On C: b^2 = 16 - a^4, or E: v^2 = u^3 - u, identify/exploit the descended
quotient of the two same-boundary Hilbert-90 sign objects pref and h*vq.  A
winning identity must give the coupled selector chi(y-2)*h*vq after b-flip
normalization, not just the norm of H or V.
```

Status:

```text
Simple trace, anti-trace, and norm evaluations of H, V, HV, pref_HV, and
BC_HV are negative; see P27 H/V Trace Coupling Audit.
The remaining ask needs a nontrivial theta/additive/Kummer formula, not just
Tr(U), U-sigma(U), or Norm(U) for these named U.
Easy F_p quotient automorphisms are also not enough: a -> -a leaves T_line
balanced and not exactly predicted by degree-2 branch-sign products.
```

Promotion bar:

```text
The identity becomes a named formula or gate with zero mismatches on p27 rows
and a way to sample/enumerate the selected stratum cheaper than sqrt(p).
```

Kill condition:

```text
The source only rederives the visible norm or branch squareclasses already
killed by the component norm audit, or the simple trace/anti-trace/norm
squareclasses killed by the H/V trace audit.
```

## Current Recommendation

The current compact queue is:
[P27 Live Sqrt-Beating Queue](p27_live_sqrt_beating_queue_20260621.md).

Ranked next moves:

```text
1. Theory/CAS: quotient decomposition of the saturated genus-37 K/S layer.
2. Theory/lit/expert: trace/norm half-norm phase identity for pref vs h*vq.
3. GPU: bounded same-stream telemetry only; no moonshot-scale run without
   a quotient/source or heldout efficiency gain.
```

The first large GPU use should still be Card 1 rather than a blind production
cap, but the moonshot bottleneck has moved: fixed-prefix and visible-character
screens are no longer the scarce work.  The scarce work is a low-genus
quotient/source or a non-visible theta/Kummer/Hilbert-90 identity that
controls many selected `chi(d_j)` / `chi(u_j+2)` gates at once.

## Current Priority After Two-Step Kummer Screen

The latest conic-pair two-step Kummer screens kill the simple `Z0/S1/Z1`
quotient family: pair systems are flat through degree 12, and the obvious
trivariate systems are flat through degree 6.  The current test queue should
now be this compact list:

Update after B-line prefix profiling:
[P27 B-Line Prefix Profile](p27_b_line_prefix_profile_20260622.md) keeps
`Bplus` as an exact descent coordinate but demotes B-bucket counting.  Small
exact fields have late all-plus plateaus, while p27 `4000 + 4000` B-group
train/heldout samples thin like independent half-gates through the meaningful
range.  B-line work should therefore be divisor/Kummer extraction, not GPU
production or bucket scoring.

### Test A: Staged Legal Pullback Normalization

Build the legal pullback in stages rather than as one web-Magma monolith:

```text
residual E/T compactD source
label-2 map to (A,x)
A = 2-c^2
x = r^2
h^2 = r^2+c*r+1
g^2 = r^2-c*r+1
r_next^2 - (h+g)r_next + 1 = 0
Z_j^2 = -(L_j+a_j)(L_j-a_j)c*r_{j+1}
```

Report component genera, projection degrees to `E`, `E'`, and `K/lambda`,
branch divisors, and whether any quotient controls two or more selected gates.
The first sharpened target is now the A-level class sequence forced by
[P27 Conic Tower D6 A-Descent](p27_conic_tower_d6_a_descent_20260622.md)
and extended by
[P27 A-Level Prefix Descent](p27_a_level_prefix_descent_20260622.md): compute
the normalized A-cover carrying d3..d10 first, then compare successive
quadratic branch divisor classes.

Promotion bar:

```text
genus <= 1 quotient, sourceable low-genus component, or a recurrence that
forces d_{j+1} from the previous Kummer class without a fresh half-loss
```

Kill condition:

```text
all components are high-genus/generic and the d4/d5 classes are independent in
the divisor/Kummer group; after the d6 update, kill only after d6 is included
in that class comparison too.  After the deeper A-prefix update, the sharper
kill is independence of the d3..d10 A-line classes.
```

### Test B: E/E' Double-Cover Class Extraction

Extract the actual double-cover classes for the descended d3 and d4 bits on:

```text
E:  W^2 = X^3 - X
E': V^2 = U^3 + 4U
```

Do not use more visible factor products or random low-pole scans.  Compute the
function-field/divisor classes directly, then compare whether `d4` is a
translate, pullback, norm, or low-degree transform of `d3`.

Promotion bar:

```text
named divisor/Kummer relation with zero mismatches on q1471/q1607/q1847 and
p27 rows, plus a sourceable walk or quotient
```

Kill condition:

```text
d3 and d4 land in unrelated classes and no low-degree quotient/translation
survives the guard fields
```

### Test C: B-Line Kummer-Class Extraction

Use `B = 8X^2/(X^2-1)^2` and `A + 2 = B^2` as the rational line coordinate.
Extract the actual Kummer classes:

```text
f3(B), f4(B), f5(B), ...
```

Do not continue rational-linear or small visible-factor product scans.  The
needed output is branch divisor support, class degree, and a comparison such
as translate, pullback, norm, recurrence, or independence.

Promotion bar:

```text
a named divisor/Kummer relation that predicts at least one later gate from an
earlier class with zero mismatches on q1607/q1847/q2087 and p27 heldout rows,
plus a source/sampler interpretation that avoids a fresh half-loss
```

Kill condition:

```text
the classes remain independent in the divisor/Kummer group, or the only
relations are small-field Frobenius artifacts that do not survive p27 samples
```

### Test D: K-Line Branch-Cover Extraction

Use the signed-doubling Kummer line:

```text
K = x([2]P),  E': V^2 = U^3 + 4U
```

Current finite-field status:

```text
degree <=2 K-polynomial characters are killed
shared small-integer degree 3/4 K-polynomials are killed
split degree <=4 branch divisors from rational linears / irreducible
quadratics are killed
q607 and q991 monic cubics are killed, while q863 exact cubics are unstable
local interpolation artifacts
q1471 promotion-field monic cubics are killed
```

See [P27 K-Line Cubic Stdin Probe](p27_kline_cubic_stdin_probe_20260622.md).
Use [P27 K-Line Fit Significance](p27_kline_fit_significance_20260622.md)
to decide whether an exact finite-field fit is meaningful.  In particular,
q863 exact cubics are expected interpolation, while q1471/q1607/q1847 d3
cubic or quartic fits would be strong evidence if stable.
The q1471 cubic promotion screen is now negative:
[P27 K-Line q1471 Cubic Promotion Screen](p27_kline_q1471_cubic_promotion_screen_20260622.md).

Promotion bar:

```text
Magma/Sage branch-cover normalization in q1471/q1607/q1847 with genus <= 1,
or a named stable branch-class relation that sources d3 without a fresh
half-loss
```

Kill condition:

```text
the recovered d3 cover over P1_K is high-genus/generic, or d4 is an unrelated
fresh cover after d3
```

### Test E: Bounded GPU Legal-Pullback Telemetry

Only run this if the GPU implementation samples legal pullback rows, not free
random `(R,L)`.

Report:

```text
source_draws/sec
legal_pullback_rows/sec
d3/d4/d5 survivor rates per source draw
same-stream baseline raw X1(16) survivor rates
effective deep survivors/sec
identity mismatch counts for the conic-chain formulas
```

Promotion bar:

```text
>= 1.25x effective deep survivors/sec on heldout streams, or evidence that two
successive gates are sourced without independent half-loss
```

Kill condition:

```text
the sampler is just free `(R,L)`, legal hits are still constant/q, or the
pullback pays the same Legendre/square-root toll as ordinary halving
```

### Test F: Trace/Norm Half-Norm Phase Identity

Use this as an expert/theorem ask, not as another product scan.  The target is
the same-boundary Hilbert-90 pair:

```text
pref(sigma)/pref = -chi(a)
(h*vq)(sigma)/(h*vq) = -chi(a)
T(sigma)/T = 1
```

Promotion bar:

```text
non-visible theta/additive/Kummer identity that predicts a post-Dplus or
T_line selector with zero mismatches and gives a cheaper source
```

Kill condition:

```text
the identity reduces to already-killed visible norm, branch, trace, or
anti-trace squareclasses
```

Current decision:

```text
GPU is justified for Test E telemetry only after a legal pullback sampler
exists.  Without that, the next best work is CAS/theory on Test A, Test B,
Test C, or Test D.  Bplus-only GPU telemetry is bounded validation, not a
production moonshot.
```
