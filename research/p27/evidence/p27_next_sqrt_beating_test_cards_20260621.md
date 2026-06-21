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

## Card 2: Named R(a) Candidate Evaluator

Use the p27 evaluator that accepts a named rational function:

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
branch functions are negative; use this only for named theorem/expert
candidates.

Promotion bar:

```text
zero mismatches on prefix and held-out p27 line samples, plus a cheap way to
sample or enumerate the selected line stratum without paying sqrt(p) again.
```

Kill condition:

```text
only post-hoc high-degree interpolation or a filter whose cost/loss cancels the lift.
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

The first large GPU use should be Card 1, not a blind production cap.  If Card
1 shows flat strata, the math effort should move to Card 3/9.  If Card 1 shows
a real same-stream survivor lift, then the GPU agent should run a paired A/B
cost model before any certificate hunt.
