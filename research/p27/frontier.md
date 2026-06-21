# P27 Frontier

Updated: 2026-06-21

## Target

```text
p = 1000000000000000000000000103 = 10^27 + 103
prime = true
sqrt_floor(p) = 31622776601683
k = ceil(log2(sqrt_floor(p))) = 45
bit_length(p) = 90
p mod 8 = 7
p mod 4 = 3
```

The target is prime. No p27 certificate is known in this workspace yet.

## Current State

The p26 practical target is closed with a verified certificate, so p26 now
serves as prior art rather than an active production target. The p27 folder is
the new live cockpit for math-structure work and bounded practical probes.

The first p27 trace/norm transfer gate is positive as structure:
[P27 Trace/Norm Transfer Gate](evidence/p27_trace_norm_transfer_gate_20260621.md).
The p26 EK quotient, b-flip cocycle, domain-line descent, and target-line
descent all survived on p27 with zero inconsistencies in a `65,536` raw-draw
diagnostic.

The practical C path also smoke-tested on p27:
[P27 Practical Trace/Norm Prefilter Smoke](evidence/p27_practical_trace_norm_prefilter_smoke_20260621.md).
Baseline `x16halvestatsnonsplit` and trace/norm `x16halvestatsnonsplittraced`
both run cleanly.  On a bounded 1M-vs-1M CPU comparison, the trace/norm
prefilter is slower per emitted candidate but shows a stable-depth net of about
`1.10x` to `1.19x` survivors per second at depths 16-19.
[P27 Trace/Norm Variant Benchmark](evidence/p27_trace_norm_variant_benchmark_20260621.md)
then shows that `tracechar` is effectively tied with `traced`, while
`tracesqrt` is slower in this CPU implementation.

The better practical candidate is now the cheaper domain-only filter:
[P27 Practical Domain-Line Filter](evidence/p27_practical_domain_filter_20260621.md).
On three measured streams, `domain_line=-1` had zero depth-16+ first-branch
survivors, including a 5M held-out run.  The domain-only C stats mode gives
about `1.29x` to `1.39x` net survivor-per-second at stable depths on seeds
`121`/`122`, beating the full `D` prefilter on CPU.  `T_line` is not stable
enough to promote as a filter.

The follow-up audit is important:
[P27 Domain Line Equals First-Halving Gate](evidence/p27_domain_first_halving_gate_20260621.md).
`domain_line=+1` is exactly the first-halving square-root gate
`F=(y-1)(y^2-2)(y^2-2y+2)`.  That makes it a real practical constant-factor
filter and a good GPU A/B target, but not the moonshot by itself.  The next
sqrt-beating test is whether the quotient/Hilbert-90 structure predicts a
post-domain halving gate cheaply.

The p25 first-lift sampler now ports to p27:
[P27 First-Lift Elliptic-Cover Port](evidence/p27_first_lift_ecover_port_20260621.md).
The residual cover
`w^2=y(y-1)(y-2)`, equivalently `w^2=x^3-x` with `x=y-1`, sources the first
halving/domain gate directly.  On two 1M p27 CPU A/B seeds it beats raw
nonsplit at depth-16 survivor-per-second by about `1.31x` to `1.35x` and at
depth 18 by about `1.27x` to `1.67x`.  This promotes `ecover` ahead of the
raw domain/dgate filter as the first practical GPU A/B candidate.  The same
note also records a negative residual 2-descent split, so it does not yet give
the second-gate/tower law needed for sqrt beating.

The first post-domain telemetry is negative for the existing `T_line`:
[P27 Post-Domain Next-Gate Telemetry](evidence/p27_post_domain_next_gate_telemetry_20260621.md).
After conditioning on `domain_line=+1`, `T_line` is essentially flat at depths
`6`, `8`, and `10` on two fresh million-row streams, and deeper counts flip
direction.  So the next mathematical target is a new named post-domain
discriminant bit, not another production run with `T_line` as the filter.

That target is now sharper:
[P27 Second-D Gate Frontier](evidence/p27_second_d_gate_frontier_20260621.md).
The next obstruction after `domain_line=+1` is exactly another Montgomery
discriminant squareclass `d2=x5^2+A*x5+1`.  On a 1M p27 same-stream run,
`T_line` split this gate at `0.498654` vs `0.501927`, i.e. flat.  Reused p24
label2/H90/residual features and a tiny `chi(V+aU+b)` quotient-line sweep are
also negative.  The current moonshot is therefore a formula or source sampler
for `chi(d2)`, and ultimately a tower law for `chi(d_j)`.

The tower profile now supports that formulation:
[P27 Selected Halving Tower Profile](evidence/p27_halving_tower_profile_20260621.md).
Through the first eight selected halving gates in a 1M p27 run, every gate is
controlled by the next `d_j` squareclass; there were zero `d_j` square / `w`
failures and zero two-`w` branches.  Fixed-prefix `d_j` filtering is a
practical constant-factor GPU test.  The real moonshot is a Kummer/2-cover or
theta/duplication law that enforces many `d_j=+1` conditions at once.

The absence of a separate `w_j` obstruction is now explained:
[P27 Nonsplit W-Obstruction Identity](evidence/p27_nonsplit_w_obstruction_identity_20260621.md).
For the two `w` candidates in a Montgomery halving step,
`w_+*w_-=16*x^2*(A^2-4)`.  On nonsplit rows this has nonsquare squareclass, so
once `d_j` is square exactly one `w` branch is available.  The only real
random-looking obstruction in this path is the sequence `chi(d_j)`.

The `d_j` character is also the ordinary x-square 2-descent character:
[P27 X-Square / 2-Descent Gate](evidence/p27_xsquare_2descent_gate_20260621.md).
Since `E_A` has `y^2=x(x^2+A*x+1)`, every nondegenerate `F_p` point has
`chi(d_j)=chi(x_j)`.  The current moonshot is therefore: can the X1(16) source
be lifted into an iterated 2-cover source where many selected x-coordinates
are squares without paying a random factor `2` per layer?

The second gate now has an explicit label-2 mixed-cover formulation:
[P27 Label-2 Second-Gate Cover](evidence/p27_label2_second_gate_cover_20260621.md).
With residual first-lift coordinates `W^2=X^3-X`, label `y=2X/(X-1)`, and
`T^2=X(X^2+1)(X^2+2X-1)`, the p27 second gate is exactly
`compactD=-1`.  The old `compactD=+1` sign is wrong for p27.  A corrected
`compactdneg` CPU mode starts at depth 6 but loses on survivor-per-second, so
this is a GPU/Sage/Magma source-cover test rather than a CPU production
promotion.  The next moonshot checkpoint is concrete: compute the genus and
Jacobian decomposition of `R^2=criterion(X,W,T)` and test whether the same
compact criterion recurs for `d3`.

First answer to that checkpoint:
[P27 Label-2 Cover Genus And Recurrence Probe](evidence/p27_label2_cover_genus_recurrence_20260621.md).
A finite-local probe over split prime `17` gives intermediate genus `5`,
`16` ramification points for the `R` cover, and genus `17` if smooth.  Two
corrected-sign `compactD=-1` streams then show the next gate is again
`~1/2`.  So the current second-cover route is not a cheap source by itself;
it needs a special Prym/Jacobian decomposition or a new recurrence to become
sqrt-beating.

A small-prime trace-count follow-up sharpens the same read:
[P27 Label-2 Cover Trace Decomposition Probe](evidence/p27_label2_cover_trace_decomposition_20260621.md).
After a `+1` common-branch correction at `X=0`, the intermediate `V4` cover
trace decomposes into the expected `W/T/WT` quotient traces.  The new Prym
trace `aD-aC` is not any small integer combination of those obvious factors
with coefficients in `[-8,8]`.  This is not a proof of genericity, but it
raises the bar: the next credible sqrt-beating route needs an actual
Sage/Magma Prym/Jacobian decomposition, a non-obvious low-degree quotient, or
a recurrence that survives `d3/d4` telemetry.

There is now one positive quotient-shaped handle:
[P27 Label-2 H90 / Order-4 Lift](evidence/p27_label2_h90_order4_lift_20260621.md).
The mixed second-gate term satisfies
`S^2=X*L` and `m0^2-mt^2*T^2=4*T^2*S^2`, so the `T -> -T` deck involution
lifts to the full cover `R^2=h`; the lift squares to the `R`-deck involution
and has order `4`.  Riemann-Hurwitz gives quotient genus `1`, identifying the
second-gate cover as a cyclic quartic cover over the residual elliptic curve
`E: W^2=X^3-X`.  This does not explain `d3` yet, but it changes the next math
test from "is genus 17 generic?" to "can the cyclic quartic character over E
be sourced cheaply or shown to recur for d3/d4?"

The first source attempt from that viewpoint is negative:
[P27 Label-2 E[2] Packet Source Probe](evidence/p27_label2_e2_packet_source_probe_20260621.md).
The rational `E[2]` packet selector is exact and gives the expected `~2x`
per-candidate lift after halving the candidate set, but source survival is
unchanged through depth `24` on a 200k-source p27 run.  So the easy packet
source is killed; the surviving tests are the alpha/cyclic-quartic
decomposition and `d3/d4` recurrence telemetry.

A residual `[3]` coset source screen is also negative:
[P27 Label-2 Residual E[3] Coset Screen](evidence/p27_label2_residual_e3_coset_screen_20260621.md).
Coset `0` briefly showed a tail lift, but an independent 2M replication did
not confirm it.  Combined over 4M baseline/coset0 samples, the lift is only
about `1.02x` at depth `16`, `1.12x` at depths `18-20`, and unstable deeper.
This is not an active moonshot lane, though it can remain a low-priority GPU
telemetry column if essentially free.

The visible residual-E character route is also negative:
[P27 Label-2 Visible Residual-E Character Screen](evidence/p27_label2_visible_e_character_screen_20260621.md).
Across `1904` small-field rows, no GF(2) combination of the natural H90
factors on `E` matches compactD; the best combinations hit only about `55%`.
So compactD is T-sign invariant but not a cheap visible quadratic character on
the residual elliptic curve from the screened factors.

The newest recurrence/branch check is also narrowing:
[P27 Label-2 Alpha/Branch Recurrence Probe](evidence/p27_label2_alpha_branch_recurrence_20260621.md).
On 5,000 paired compactD rows, `compactD=-1` had zero d2 failures.  But d3
was invariant across both paired `T` roots and both second-half x-branches, at
a random-looking `0.4932` plus rate; conditioned on d3, d4 had the same shape
at `0.5174`.  The reason is structural: the two half x-branches have product
`1`, so they have the same squareclass, and `chi(d_next)=chi(x_next)`.  This
kills branch-choice and alpha/T-pair choice as sqrt-beating routes.  The
moonshot must find a source or recurrence for the descended x-square bit
sequence itself.

That sequence now has a cleaner local formula:
[P27 Halving U+2 X-Square Gate](evidence/p27_halving_usquare_gate_20260621.md).
For a successful halving step with `x' + 1/x' = u`, the next x-square gate is
`chi(x') = chi(u+2) = chi(u-2)`.  On the 5,000-pair compactD sample, this had
zero mismatches for d2-to-d3 and d3-to-d4; it would reject about `50.68%` of
d3 attempts and `48.26%` of d4 attempts before materializing the next branch
root.  This is a concrete GPU prefix-cost test, not a sqrt-beating theorem by
itself.  The moonshot is now even sharper: couple the selected `chi(u_j+2)`
characters across many gates.

The first direct recurrence screen for those characters is negative:
[P27 U+2 Sequence Recurrence Screen](evidence/p27_usquare_sequence_recurrence_20260621.md).
Starting from 30,000 compactD/d2 rows, gates 3 through 6 have plus rates
`0.5001`, `0.4975`, `0.4965`, and `0.5003`; later gates are tail-count noise.
The prefix-success histogram is consistent with geometric half-loss, and no
anomalies were observed.  This kills the simplest hope that compactD enters a
biased later `u+2` stratum.  The remaining moonshot needs a non-local
Kummer/theta/Hilbert-90 relation coupling many `chi(u_j+2)` characters at once,
or a source for the all-plus iterated 2-cover.

The GPU cost test for the independent `u+2` precheck is now negative:
[P27 GPU U+2 Precheck Probe](evidence/p27_gpu_uprecheck_probe_20260621.md).
The CUDA `x16uprecheckprobe` mode compiled cleanly with no spills and did
confirm the exact continuation-scope shrink.  The implementation also avoided
many `sqrt(w)` calls, but the extra Legendre tests cost more than they saved.
At depth 8, the ordinary prefix probe ran at `36.89M` accepted
roots/sec versus `29.96M` for `u+2`; at depth 10, `33.85M` versus `27.84M`.
Do not promote independent `u+2` prechecking as the production implementation;
look for a direct source or recurrence that exploits the smaller stratum.

The local norm/coboundary screen is also negative but clarifying:
[P27 U+2 Norm/Coboundary Screen](evidence/p27_usquare_norm_coboundary_20260621.md).
The identities `Norm_s(u+2)=4*x*(2-A)`, `Norm_s(u-2)=-4*x*(A+2)`, and
`Norm_s(u^2-4)=16*x^2*(A^2-4)` held with no mismatches on 30,000 compactD
rows.  But the selected `w`-square branch's `u+2` bit was not in the small
local norm/branch span: best scores were `0.5018` for d3 and `0.5025` for d4.
So the open math object is a selected-branch orientation/Hilbert-90 class, not
a visible `A,x` norm factor.

The first selected-orientation cocycle span screen is also negative:
[P27 Selected Orientation/Cocycle Span Screen](evidence/p27_selected_orientation_cocycle_span_20260621.md).
It allowed local characters plus selected `s`-branch orientation characters
from the whole successful prefix through gates 3-6.  Two 30,000-row seeds found
no exact GF(2) product for the next `u+2` bit.  The best weight-3 in-sample
scores were small (`0.513`, `0.523`, `0.528`, `0.545` by gate on the first
seed) and did not replicate as the same named products.  This kills the cheap
"selected orientation character product" version of the H90 idea.  The next
test should be a real source-cover construction.

The concrete source-cover target is now reverse doubling.  If `x_next` is the
next half x-coordinate, then:

```text
x = (x_next^2 - 1)^2 / (4*x_next*(x_next^2 + A*x_next + 1)).
```

Thus the next all-plus gate can be sourced by substituting `x_next=z^2`:

```text
x = (z^4 - 1)^2 / (4*z^2*(z^4 + A*z^2 + 1)).
```

This gives a concrete reverse-source equation to intersect with the
label-2/compactD source.  By itself it is only an equation; it needs
Sage/Magma components, genus, low-degree quotients, or a cheap walk before it
can beat random half-loss per gate.

First reverse-source screen:
[P27 Reverse-Doubling Source Screen](evidence/p27_reverse_doubling_source_screen_20260621.md).
The equations are exact and had zero reverse-doubling or rational-point
mismatches, but p27 density remains random-half: `0.4932` on seed `20260621`
and `0.5044` on seed `20260622`.  The z-source multiplicity also matches the
generic expectation: about `2` z-points and `4` `(z,Y)` points per oriented
compactD candidate.  A follow-up handoff artifact made the required
`eta^2=1` first-half branch sign explicit and passed both p27 point
verification and an online Magma `q=607` validation:
`RESULT p27_reverse_q607 ok 512 256 0 0 1024 2048`.  So reverse doubling is a
precise source-cover equation, not yet a cheap source.  The next meaningful
test is Sage/Magma component, genus, quotient, and factor-through-`D/<alpha>`
analysis.

That quotient question now has its first answer:
[P27 Reverse Source Quotient Screen](evidence/p27_reverse_source_quotient_screen_20260621.md).
On 5,000 p27 residual-elliptic quotient fibers, the d3/reverse-source bit
descends perfectly to `E: W^2=X^3-X`: all `5,000` fibers had orbit size `4`,
with zero non-descended fibers, and split `2466/2534` plus/minus.  That is
positive structure: the next bit is quotient-level, not hidden in full
compactD fiber data.  But it is not a cheap degree-1 line character on `E`:
the p27 small-coefficient line screen had no exact line and best rate
`0.5128`, while an exhaustive `GF(607)` projective line screen tested
`369,057` lines and found `0` exact lines.  The next ask is therefore an
E-level divisor/theta/Kummer class or recurrence, not another branch/T-choice
or line scan.

The d4 recurrence follow-up keeps the quotient lead alive but does not close
it:
[P27 Reverse Source D4 Recurrence Screen](evidence/p27_reverse_source_d4_recurrence_20260621.md).
After conditioning on d3, d4 also descends perfectly to the same residual
elliptic quotient: on the 5,000-fiber p27 sample, `2466` d3-positive fibers
produced `1276/1190` d4 plus/minus with zero non-descended or missing fibers.
The p27 small-coefficient d4 line screen found no exact line and best rate
`0.5312`.  Tiny fields `q=607,863,991` make d4 constant on the d3-positive
locus, so their exact simple-transform recurrences are degeneracies, not a
p27 theorem.  The active moonshot is now very specific: derive E-level
functions/classes `f3(X,W)` and `f4(X,W)`, compare their divisors or Kummer
classes, and look for a recurrence or sourceable walk there.

The first named E-basis attempt is negative:
[P27 E-Quotient Kummer Basis Screen](evidence/p27_equotient_kummer_basis_screen_20260621.md).
The screened basis was the existing structural one:
`X`, `W`, torsion factors `X±1`, 2-descent factors, and the order-4/H90
functions `S`, `S_conj`, `m0`, `mt_coeff`, `prefactor`, and `L`.  No exact
product explains d3 or d4 on p27.  Train-best products do not replicate:
d3 train-best falls to `0.5044` on heldout, and d4 train-best to `0.5075`.
Non-degenerate fields `q=1087,1471,1607` also have zero exact products.  This
kills the visible named-basis route.  The remaining quotient moonshot now
requires symbolic/function-field extraction of the actual E-level double
covers, not more visible product scans.

A broader low-pole pilot also failed to produce a source:
[P27 E-Quotient Low-Pole Random Screen](evidence/p27_equotient_lowpole_random_screen_20260621.md).
It tested small-integer sections of `L(nO)` on `E` and products of two
sections, modeling low-pole rational-function squareclasses.  On a p27
train/heldout split there were no exact candidates; best heldout scores were
only `0.5275` for d3 and `0.5390` for d4 in a 200-trial pilot.  This is not a
proof of absence, but it kills the nearest cheap random low-pole route.  The
next useful artifact should be a Magma/Sage function-field extraction of the
actual E-level double covers, with online Magma acceptable for small-field
validation in the p24 style, or a faster finite-field solver on
non-degenerate small fields before p27 validation.

The first exact small-field follow-up kills the reducible-conic subclass:
[P27 E-Quotient Line-Product Screen](evidence/p27_equotient_line_product_screen_20260621.md).
It exhaustively tested products of two projective-line characters on `E`.
There are no exact d3 two-line products over `q=607`, `q=1087`, or `q=1471`,
and no exact d4 two-line product over the decisive non-degenerate `q=1471`
field.  The `q=1087` d4 exact pairs occur on only `40` rows and disappear at
`q=1471`, so they are treated as a small-row coincidence.  This kills the
visible reducible-conic source; the next cheap algebraic step is irreducible
conics or direct function-field extraction.

The first broader recurrence screen is also negative:
[P27 E-Quotient Affine-Walk Recurrence](evidence/p27_equotient_affine_walk_recurrence_20260621.md).
It tested every map `P -> [m]P + Q` over `q=1087,1471,1607`, for
`m = +/-1, ..., +/-8` and every `Q in E(F_q)`.  Only identity/negation plus
the `(0,0)` torsion shift had full coverage, and they scored exactly like the
raw d4 distribution (`20/40`, `56/112`, `76/112`).  No nontrivial walk reached
the `0.75` coverage threshold.  This kills the small elliptic-walk recurrence
as a GPU/sqrt-beating source.

The quotient route now has one positive descent:
[P27 E-Quotient Kernel-8 / 2-Isogeny Screen](evidence/p27_equotient_kernel8_2isogeny_screen_20260621.md).
Small-field projection screens pointed at `[8]P`; the p27 forced-collision
test showed the actual invariant is the `(0,0)` rational 2-torsion orbit.
On 1,000 p27 rows, each compactD orbit had exactly two in-domain kernel
translates, `O` and `(0,0)`, with `mixed_d3_orbits=0` and
`mixed_d4_orbits=0`.  Thus d3/d4 descend to the 2-isogenous quotient
`V^2=U^3+4U`, where `U=X-1/X` and `V=W(X^2+1)/X^2`.  Exact line and two-line
screens on this quotient are still negative over `q=1471` and `q=1607`, so the
win is a sharper function-field target, not yet a sampler.

The newest p26 GPU trace/norm result is positive structure but negative as a
production prefilter:
[P27 GPU Filter-Cost Lesson From P26](evidence/p27_gpu_filter_cost_lesson_from_p26_20260621.md).
On p26, `D_trace=+1` captured all observed depth-20 through depth-28 survivors
in three 100M raw-`y` streams, giving essentially exact `4x` enrichment.  But
the current trace/norm classifier path ran at only about `4.47M` candidate
roots/sec versus `31.87M` accepted roots/sec for the no-trace baseline.  The
lesson for p27 is decisive: compactD/order-4 and any later stratum must be
judged by effective deep survivors per GPU-second.  The desired next win is a
direct sampler, a cheaper algebraic test, or a recurrence into `d3/d4`, not an
expensive rejector with beautiful conditional lift.

The latest p26 GPU seed-order/compact-bucket probe is negative: the replay
telemetry works, but identity/splitmix/mixed seed order and the hit's compact
bucket did not produce a held-out-promoted stratum.  This keeps the p27 focus
on mathematical 2-descent invariants, not seed law.

The quotient line also has a cleaner elliptic interpretation now:
[P27 Trace/Norm Elliptic Line / Coset Audit](evidence/p27_trace_norm_elliptic_line_coset_20260621.md).
The map to `E: v^2 = u^3 - u` verifies the expected supersingular order
behavior on p27 samples.  Small torsion/coset projections and visible
branch-coordinate rational functions are negative as explanations for
`domain_line` or `T_line`.

The large-factor elliptic quotient route is also negative:
[P27 Elliptic Large-Factor Collision Audit](evidence/p27_elliptic_large_factor_collision_20260621.md).
For the p27-specific factor `345451` and small multiples through
`12*345451`, repeated projection classes are mixed at roughly random rates.
Projected-point characters such as `chi(x_m)`, `chi(y_m)`, and
`chi(x_m^2+1)` are not exact and do not show stable held-out lift.

The first 2-isogeny visible-divisor layer is also negative:
[P27 Line 2-Isogeny Character Span](evidence/p27_line_2isogeny_character_span_20260621.md).
The full `65,536`-product GF(2) span of branch and first 2-isogeny characters
had no exact survivors for either line bit.

The domain bit now has an algebraic half-norm explanation:
[P27 Line Half-Norm And Joint Stratum](evidence/p27_line_half_norm_joint_stratum_20260621.md).
With `t=y-1` and `a=t-1/t`, `domain_line` is the squareclass of
`(a+2)(t^2+1)`, and `sigma(t^2+1)/(t^2+1)` is a square.  This explains why
the bit descends to the `a`-line but does not appear as a visible rational
`chi(R(a,u))`.

The quotient automorphism audit adds one more domain-side explanation:
[P27 Quotient Automorphism Orbit Audit](evidence/p27_quotient_automorphism_orbit_20260621.md).
The easy `F_p` automorphisms preserve `domain_line`, including the maps sending
`a -> -a`.  They do not close `T_line`: under `a -> -a`, `T_line` remains
balanced and no exact degree-2 branch-sign ratio was found.

The remaining `T_line` selector is now split into components:
[P27 T-Line Component Descent](evidence/p27_tline_component_descent_20260621.md).
The `vq` factor is the unique observed carrier of the `chi(a)` b-flip cocycle;
`h`, `x_pref`, `chi(y)`, and `pref=chi(y-2)` are b-invariant.  No single
component explains `T_line`; the theorem ask is a coupling identity for
`chi(y-2)*h*vq` after the line normalization.

The next component norm audit is negative but clarifying:
[P27 Component Norm / Half-Norm Audit](evidence/p27_component_norm_halfnorm_audit_20260621.md).
The visible norm factors inside the `h` and `vq` square-root arguments collapse
to already-known branch classes such as `chi(t^2-1)`.  A `13`-atom named
product span has no exact `T_line` selector, and its best in-sample lift
collapses to about `1.00x` on held-out seed streams.  The remaining math target
is therefore a non-visible theta/additive/Hilbert-90 phase-coupling identity,
not another visible branch-divisor product screen.

The best current theorem-shaped handle is the quotient involution boundary:
[P27 Component Involution Boundary](evidence/p27_component_involution_boundary_20260621.md).
Under `sigma(t)=-1/t`, both `pref=chi(y-2)` and `h*vq` pick up the same
boundary `-chi(a)`, so `T=pref*h*vq` descends.  This gives a narrow expert ask:
identify or exploit the descended quotient of two same-boundary Hilbert-90 sign
objects on `C: b^2=16-a^4` / `E: v^2=u^3-u`.

A direct trace/anti-trace follow-up is negative:
[P27 H/V Trace Coupling Audit](evidence/p27_hv_trace_coupling_audit_20260621.md).
The tautological `T_arg=(t-1)BCHV` check is exact, but simple
`Tr`, anti-`Tr`, and `Norm` squareclasses of `H`, `V`, `HV`, `pref_HV`, and
`BC_HV` give no non-tautological exact selector.  Percent-level lifts are too
small and unstable to promote without GPU same-stream survivor telemetry.

No long p27 production run should be launched until the practical sampler has
GPU baseline telemetry and any transferred p26/p25 filter/source candidate has
a same-stream per-second lift measurement.

## Baseline Arithmetic

See [P27 Arithmetic Baseline](evidence/p27_arithmetic_baseline_20260621.md).

Important immediate implication:

```text
p26: p mod 8 = 3, chi(2) = -1
p27: p mod 8 = 7, chi(2) = +1
```

The p26 trace/norm quotient story does transfer at the level of the first p27
gate, but it has not yet produced a cheap source sampler.

## First-Class Plan

1. Smoke-test the official practical path on p27 with a tiny bounded run.
2. Use the transferred trace/norm line structure as the first theorem front.
3. Prefer concrete sqrt-beating test cards over broad literature wandering.
4. Use GPU only for high-throughput telemetry or production once the exactness
   contract is clear.

## P26 Transfer Hypothesis

The most promising recent p26 structural artifact was not the certificate
itself, but the trace/norm descent:

```text
F-square gate -> E_K: w^2 = -(y^2 - 2)(y^2 - 4y + 2)
t = y - 1
E_K: w^2 = -t^4 + 6t^2 - 1
g(t,w) = (-1/t, w/t^2)
a = t - 1/t
b = w(t^2 + 1)/t^2
b^2 = 16 - a^4
```

For p27, the same structure now passes the first medium gate:

```text
neg_inv_cocycle_exact = 1
quotient_relation_exact = 1
b_flip_cocycle_exact = 1
domain_line_consistent = 1
target_line_p26_Tline_consistent = 1
degree-1/2 tiny line exact found = 0
```

See [P27 Transfer Plan](evidence/p27_p26_trace_norm_transfer_plan_20260621.md)
and [P27 Trace/Norm Transfer Gate](evidence/p27_trace_norm_transfer_gate_20260621.md).

## Immediate Test Cards

### Card 1: Practical Sampler Smoke

Run a bounded p27 `X1(16)` smoke to confirm the current C path handles this
target and reports sane candidate/marker telemetry.

Promotion bar: verifier-compatible output path, no branch failures, and stable
baseline candidate rate.

Status: passed for bounded stats mode.  Not a production search.

### Card 2: P27 Trace/Norm Sign Smoke

Parameterize or copy the p26 trace/norm gates for p27 and verify whether the
same quotient formulas remain internally consistent after the `chi(2)` flip.

Status: passed on the first medium diagnostic.

### Card 3: Domain-Line Re-test

Re-run the p26 domain-line collapse on p27:

```text
F = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

Promotion bar: the domain descends cleanly to the same quotient coordinate and
produces a non-flat payload class worth GPU scoring.

Status: the domain descends cleanly, but the first tiny degree-1/2 line
families are flat.

### Card 4: GPU Same-Stream A/B

Once CPU exactness passes, ask the GPU agent for same-seed, same-stream
telemetry comparing baseline against any p27 source/filter candidate.

Promotion bar: candidate lift or survivor lift beats baseline per GPU-second,
not merely per raw tested curve.

See [P27 Next Sqrt-Beating Test Cards](evidence/p27_next_sqrt_beating_test_cards_20260621.md).

Current candidate: baseline vs `x16halvenonsplitecover`, with domain/dgate as
the first-bit control.  The older trace-norm `D` prefilter is secondary.
`T_line` is retained as a theorem/control bit but is not a next-gate filter
from current CPU evidence.  `tracechar` is an equivalent full-D instrumentation
variant; `tracesqrt` is not the preferred CPU-side path.

The new GPU telemetry request is `domain_line + second-d`: report whether the
native GPU code can compute `d2=x5^2+A*x5+1` cheaply enough to test baseline vs
domain-only vs domain+second-d.  This remains practical filtering unless it
leads to a reusable tower law for many `d_j` gates.

Extend that request to prefix gates if cheap: `d1`, `d1+d2`, and
`d1+d2+d3` filters, with explicit reporting of whether any `w_j` obstruction
appears.

Equivalent x-square request: report prefix filters as `x_4 square`,
`x_4,x_5 square`, and `x_4,x_5,x_6 square`.  For nonsplit rows this is the same
gate sequence and is the cleaner 2-descent language.

### Card 5: Elliptic Line Identity

Use the model:

```text
C: b^2 = 16 - a^4
E: v^2 = u^3 - u
u = 4/a^2
```

Status: small torsion/coset projections and large-factor quotient-class
explanations are killed.  Continue only with a named divisor/theta/additive
identity or a concrete `R(a,u)` formula that is not merely a quotient-class
lookup.

### Card 6: First 2-Isogeny Character Span

Status: killed.  Products of visible branch characters from `a`, `u`, and the
three first 2-isogeny x-coordinates do not explain either line bit.

### Card 7: Half-Norm / Joint Stratum

Status: active theorem ask.  Explain the descended half-norm class
`t^2+1` or the remaining `T_line` bit by a non-visible theta/divisor/additive
identity.  The joint visible-character shortcut is killed.

### Card 8: T-Line Component Coupling

Status: active theorem ask, narrowed.  Explain or exploit the coupling
`T = chi(y-2)*h*vq`, where `vq` carries the `chi(a)` b-flip cocycle and `h`
is b-invariant.  One-factor explanations and visible norm/branch-product
explanations are killed; the current positive handle is the same-boundary
Hilbert-90 involution identity.  Simple trace/anti-trace/norm evaluations of
the H/V sections are also killed.  The easy quotient automorphism orbit
explains `domain_line` but not `T_line`.

## Active Interpretation

The p24 and p26 early hits keep the seed-ordering/source-stratum question alive,
but the current evidence does not justify treating early hits as proof of a
hidden scheduling shortcut. For p27, the high-value move is to turn p26's
post-hit structure into pre-registered p27 tests and let the telemetry decide.
