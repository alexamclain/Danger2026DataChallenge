# P27 Frontier

Updated: 2026-06-22

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

The online Magma component check now confirms the genus warning:
[P27 Label-2 Cyclic-Quartic Component Check](evidence/p27_label2_cyclic_components_magma_20260621.md).
After eliminating `T`, the raw projective cyclic-quartic model must be
reduced and decomposed.  Online Magma now gives the same answer over `q=607`,
`q=1471`, and the p27-signature field `q=1607`: two components, a degree-30
genus-17 main component and a degree-1 genus-0 projection artifact.  This
kills the hope that the eliminated model is itself secretly low genus.  It
keeps exactly one serious H90 route alive:
compute the `alpha` quotient/Prym decomposition of the genus-17 component and
derive a cyclic-quartic character over `E` that recurs or couples to `d3/d4`.

The alpha quotient ask is now executable rather than vague:
[P27 Label-2 Alpha Eliminated-Map Probe](evidence/p27_label2_alpha_eliminated_map_20260621.md).
On the eliminated quartic
`R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*S^2 = 0`, the order-4 lift descends to
`R -> R*mt*(2*pref*m0 - R^2)/(2*S*(R^2 - pref*m0))`.  This rational map was
validated over q1607, q1847, and q2087: it maps the curve to itself, squares
to `R -> -R`, and fourth-powers to identity, with only four expected affine
exceptional points per field.  The next concrete theorem/CAS test is therefore
quotient/Prym decomposition using this explicit alpha map.

That quotient test now has a small Magma smoke:
[P27 Label-2 Alpha Projective Quotient Smoke](evidence/p27_label2_alpha_projective_quotient_magma_20260621.md).
After homogenizing the alpha map, online Magma over tiny `q=7` finds the
degree-30 genus-17 main component, certifies the projection to
`E: W^2Z=X^3-XZ^2` as degree `4`, computes ramification degree `32`,
constructs the projective alpha isomorphism, and builds an automorphism group
of order `4`.  The generic
`CurveQuotient(G)` call times out, but the quotient coordinates are no longer
the unknown: `D/<alpha>` is the residual elliptic curve `E`.  The live task is
now the cyclic-quartic/Kummer class over `E` and its relation to the descended
`d3`/`d4` classes, not a blind quotient computation.

The branch-class follow-up kills the nearest alpha shortcut:
[P27 Alpha Branch-Class Screen](evidence/p27_alpha_branch_class_screen_20260621.md).
For the quartic `R^4-2*a*R^2+b`, with
`a=prefactor*m0` and `b=4*prefactor^2*T2*S^2`, the `R`-discriminant
squareclass is just `T2`.  The probe verifies `T2_chi_1` on all active rows:
p27 train `5000/5000` d3 and `2466/2466` d4, p27 heldout `5000/5000` d3 and
`2522/2522` d4, and q1607/q1847/q2087 also all square.  Branch-atom product
fits have zero exact combos and p27 train-best products collapse to
`0.5044` for d3 and at most `0.5075` for d4 on heldout.  So the alpha branch
divisor is not the missing post-compactD selector; the next serious test is
actual `d3`/`d4` cover extraction on `E'` or `P^1_K`.

The first source attempt from that viewpoint is negative:
[P27 Label-2 E[2] Packet Source Probe](evidence/p27_label2_e2_packet_source_probe_20260621.md).
The rational `E[2]` packet selector is exact and gives the expected `~2x`
per-candidate lift after halving the candidate set, but source survival is
unchanged through depth `24` on a 200k-source p27 run.  So the easy packet
source is killed; the surviving tests are the alpha/cyclic-quartic
decomposition and `d3/d4` recurrence telemetry.

The natural H90 norm-one recurrence screen is also negative:
[P27 Label-2 H90 Norm-One Recurrence Screen](evidence/p27_label2_h90_normone_recurrence_20260621.md).
It tested squareclasses built from
`u=(m0+mt*T)/(2*T*Salpha)` and its closest H90 companions on independent
8,000-row train/heldout p27 samples.  The genuinely `T -> -T` invariant
features are only `u^2+1`, `u-u^-1`, `mplus`, `m0`, `Salpha`, `prefactor`,
and `L`.  Best apparent train lifts collapse on heldout: d3 best
`0.5125 -> 0.4910`, d4 best `0.5268 -> 0.4939`, and invariant-only d4 is
just raw bias.  This kills H90 norm-one squareclass products as `d3/d4`
selectors.  The remaining H90 route is non-visible alpha/Prym decomposition,
not canonical-`T` feature fitting.

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

The GPU search-space narrowing audit is now explicit:
[P27 GPU Search-Space Narrowing Probe](evidence/p27_gpu_search_space_narrowing_20260621.md).
At depth 24, fixed-prefix modes through `d4` and their ecover variants gave the
expected post-prefix survivor lift but only `1.00x` to `1.07x` on the raw
`target/source_draw` denominator, below the `1.25x` promotion bar.  Held-out
bucket telemetry did not promote any restart stratum.  In contrast, the
trace/norm `D_plus` candidate gate captured every observed depth-20 through
depth-30 survivor in a `1B+1B` raw-y GPU A/B, with `204` depth-26 survivors and
an exact-looking `4x` conditional lift among ordinary emitted candidates.  This
promotes trace/norm as a real structural stratum/source target, but not yet as
a production filter: the current implementation still pays to classify the
rejected raw-y draws.

The follow-up interpretation is now sharper:
[P27 Trace/Norm D_plus Prefix Identity](evidence/p27_trace_norm_dplus_prefix_identity_20260621.md).
The C depth histogram shows `D_plus` has no stops before depth `6`; relative
to the ordinary nonsplit stream it is exactly a two-gate prefix.  The GPU `4x`
conditional lift is therefore the expected lift from pre-paying two
half-density gates, not evidence by itself of a hidden late-depth recurrence.
After depth `6`, the Dplus-conditioned stream returns to geometric half-loss.
So trace/norm remains valuable as an algebraic description of early selected
halving gates, but the moonshot must find a new trace/norm class, quotient, or
recurrence that couples to post-Dplus gates.

That immediate post-Dplus screen is now negative:
[P27 Trace/Norm Post-Dplus Screen](evidence/p27_trace_norm_post_dplus_screen_20260621.md).
On `16,398` C-style Dplus candidates there were zero first-two-gate prefix
failures, confirming the reconstruction.  The next gate was flat:
`d3_plus=8298/16398=0.5060`; after conditioning on d3, `d4_plus=4062/8298=0.4895`.
All low-weight products of the named `H`, `VQ`, `X_pref`, root, quotient, and
`T_line` atoms failed, with the best train lifts collapsing to about `0.49` to
`0.50` on heldout.  This kills the cheap post-Dplus trace/norm-character route.
The exact orientation follow-up is also negative:
[P27 Trace/Norm Orientation Phase Screen](evidence/p27_trace_norm_orientation_phase_screen_20260622.md).
It attached the actual `D_plus` cover signs `eps_h=chi(t)` and
`eps_v=chi((t+1)C)` to C-style rows.  Across heldout seed groups, `d3` and
`d4` by `eps_h/eps_v`, `H/VQ`, `eps_h/eps_v/T_line`, and
`hcore_chi/vcore_chi` stayed near half; the apparent high `d4` bucket moved
between groups.  This kills orientation buckets as a GPU/source shortcut.
The GPU ask is now sharply bounded:
[P27 GPU Dplus-Native Source Handoff](evidence/p27_gpu_dplus_native_source_handoff_20260622.md).
Ask for fused/native `D_plus` pricing and same-stream coupling telemetry, with
raw-source denominators.  Promote only if `D_plus` is cheaper than letting the
first two selected gates fail naturally or if a direct source reaches beyond
those first two gates.
The surviving trace/norm/quotient task is now formalized as a narrow test card:
[P27 Trace/Norm Half-Norm Test Card](evidence/p27_trace_norm_halfnorm_test_card_20260622.md).
It accepts only a finite-field squareclass, divisor/theta identity, or direct
source map on `C: b^2=16-a^4` / `E: v^2=u^3-u`, with heldout evaluator checks
and raw-source accounting.  Broad trace/norm feature searches remain killed.

The first exact small-field check of that trace/norm quotient changes the
math ask:
[P27 Trace/Norm Spin Obstruction](evidence/p27_trace_norm_spin_obstruction_20260621.md).
For `t=y-1`, `a=t-1/t`, and
`F=t*(t^2+2t-1)*(t^2+1)`, Magma confirms over `q=607` that
`F(t)/F(-1/t)=t^6`, so the domain bit descends as a character, but the
valuation of `F` at the ramification factor `t^2+1` is odd.  This explains why
small `R(a)` rational-character screens were the wrong target for this bit:
the natural object is a spin/half-divisor class on the trace/norm quotient.
The next credible sqrt-beating trace/norm test is therefore explicit
double-cover/divisor-class extraction for `domain_line` and normalized
`T_line`, looking for a shared quotient, Prym factor, or sourceable Kummer
class that samples `D_plus` directly.

That extraction now has a named `D_plus` cover:
[P27 Trace/Norm D_plus Cover](evidence/p27_trace_norm_dplus_cover_20260621.md).
On a 16,096-row p27 component sample,
`D=-chi(core)` and `D_plus iff -core is square` had zero mismatches.  The
online Magma `q=607` checks validate both the domain spin quartic and the
combined `D_plus` cover: the domain quartic has genus `2`, and the D-plus
enumeration reports `mismatch=0`.  The formula still contains orientation
selectors `eps_h=chi(t)` and `eps_v=chi((t+1)C)`, which explains why the
current classifier pays fresh Legendre costs.  The next sqrt-beating test is a
Magma/Sage quotient/Prym decomposition of the four orientation components, or
a direct GPU source sampler if such a quotient is found.
There is now a positive quotient handle:
[P27 Trace/Norm Dplus Quotient Symmetry](evidence/p27_trace_norm_dplus_quotient_symmetry_20260622.md).
Across `q=607,1607,1847,2087`, `Dplus` is invariant under `z -> -z` and under
`t -> -1/t` paired with `w -> -w/t^2`.  Thus it descends to the conic quotient
`a=t-1/t`, `g=w/t`, `a^2+g^2=4`.  Generic fibers have size four and no
conflicts.  However, low-weight products of the tested `a/g/m` atoms do not
hold out, so the next artifact must be the exact descended Kummer/divisor
class on the conic, not another visible character bucket.
That target has now been corrected symbolically:
[P27 Trace/Norm Dplus Relative Descent](evidence/p27_trace_norm_dplus_relative_descent_20260622.md).
Writing `u=-core=u0+u1*z` with
`F=t(t^2+2t-1)(t^2+1)=z^2`, the verifier proves
`Norm_z(u)=F*S^2`.  Thus the conic quotient constancy is conditional on the
domain-spin root already existing; `Dplus` is not a standalone rational
character on `a^2+g^2=4`.  The next serious CAS object is the relative
Hilbert-90/Kummer class over the domain-spin cover, and the bare conic sampler
is killed.  Online Magma over `q=607` prices this reduced relative cover at
genus `17`, uniformly for the four fixed orientation sign pairs.  That is a
real reduction from the naive genus-69 full orientation-source cover, but still
not a direct production source without a special quotient/Prym or `d3`
coupling.
The H90 quotient is now explicit:
[P27 Trace/Norm Dplus H90 Quotient](evidence/p27_trace_norm_dplus_h90_quotient_20260622.md).
The lift `alpha(t,z,w,s)=(t,-z,w,z*S/s)` has `alpha^2` equal to the `s`-deck
involution and fixes `t,w`.  Magma confirms the quotient base
`w^2=-(t^2+2t-1)(t^2-2t-1)` has genus `1`, while the relative `Dplus` cover is
degree `4` over it and genus `17`.  This turns the lane into a precise
cyclic-quartic/Kummer-class extraction over an elliptic curve; it is still not
a GPU source until that class splits, recurs, or couples to `d3`.
The normalized quartic model is now explicit:
[P27 Trace/Norm Dplus H90 Quartic Model](evidence/p27_trace_norm_dplus_h90_quartic_model_20260622.md).
With `rho=s/((t+1)(t^2+2t-1))`, the cover satisfies
`rho^4 - 2*U_eta*rho^2 + F*Sprime^2=0` over `E_h90`, and the four orientation
components collapse to two cases `eta=eh*ev`.  Magma confirms both `eta`
models are still genus `17`, degree `4` over `E_h90`.  The next test is branch
divisor/Kummer extraction for these two eta classes.
That branch extraction is now explicit:
[P27 Trace/Norm Dplus H90 Branch Class](evidence/p27_trace_norm_dplus_h90_branch_class_20260622.md).
The resolvent satisfies `U_eta^2 - F*Sprime^2 = F*W_eta^2`, so the first
quadratic layer is exactly the already-known domain-spin cover `z^2=F`.
The hard class is the second layer `rho^2=U_eta+z*W_eta` over the genus-5
cover `E_h90(z)`.  Magma reports odd branch divisor degree `16` for this
second layer, giving genus `17`.  This kills a hidden low-genus first-resolvent
shortcut; the next real test is whether this named second-layer class equals,
recurs with, or predicts `d3`.
The cheap finite-field payload screen is now negative:
[P27 Trace/Norm Dplus H90 Payload Screen](evidence/p27_trace_norm_dplus_h90_payload_screen_20260622.md).
On `16,398` train and `16,122` heldout Dplus candidates, all `A_eta`
squareclasses are already `+1`, including opposite-eta variants.  Products of
`eta`, `U`, `W`, `rho`, and root-orientation features have no exact
weight-`<=3` predictor; train skews such as `U_actual` for `d3` and
`-eta*U_other` for `d4` collapse on heldout.  The remaining Dplus-H90 test is
actual d3 Kummer/divisor extraction on `E_h90(z)`, not more sign buckets.
The sharper H90/x6 coboundary screen is negative too:
[P27 Trace/Norm Dplus H90-X6 Coboundary Probe](evidence/p27_trace_norm_dplus_h90_x6_coboundary_20260622.md).
On `8199` train and `8061` heldout Dplus `y` rows, simple H90 atoms and
first-order `rho +/- atom` divisors have no exact weight-`<=3` product for
`chi(x6)`.  The best train skew falls from `0.5229` to `0.4950` on heldout.
This kills the cheap H90-root coboundary bucket; only exact CAS/Prym
comparison remains.
The branch-vs-row question is now resolved:
[P27 Trace/Norm Dplus U6 Row-Bit Resultant](evidence/p27_trace_norm_dplus_u6_rowbit_resultant_20260622.md).
On the same Dplus streams, all four `U6` branches over one row share the same
`chi(U6+2)=chi(x6)` sign: `8199/8199` train rows and `8061/8061` heldout rows
are uniform, with balanced `++++`/`----` counts.  The exact eliminated
resultant has square specializations at `U6=+/-2`, but the Kummer lift
`U6=S^2-2` does not split over `Q`.  The moonshot target is therefore one
descended row bit on the selected Dplus/H90 base, not a branch-choice bucket.
The visible branch-atom follow-up is negative:
[P27 Trace/Norm Dplus U6 Row-Bit Branch-Atom Screen](evidence/p27_trace_norm_dplus_u6_rowbit_branch_atom_20260622.md).
Products through weight `5` in the exact resultant branch factors
`t`, `t+/-1`, `t^2+1`, `t^2+/-2t-1` plus nearby `A` and `X` atoms have no
exact match.  The best heldout-ranked product is only weak `-A` bias and does
not hold train/heldout.  This keeps the Dplus row bit as a non-visible
CAS/Prym/theta target.
The nearest H90 quotient shortcut is negative:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Factor Test](evidence/p27_trace_norm_dplus_u6_rowbit_h90_factor_20260622.md).
Online Magma over `q=607` factors the row-bit lift as one degree-32 factor
over `F_607(t)` and still one degree-32 factor over
`E_h90: w^2=-(t^2+2t-1)(t^2-2t-1)`.  So the named elliptic quotient does not
split or source the row bit; only a non-obvious Prym/theta relation remains.
The next factorization tier is staged but above the online-calculator limit:
[P27 Trace/Norm Dplus U6 Row-Bit Aeta Factor Boundary](evidence/p27_trace_norm_dplus_u6_rowbit_aeta_factor_boundary_20260622.md).
The exact domain-spin and `eta=+1` `A_eta` factor fixtures return `504` over
`q=607`; this is now an offline Magma/Sage ask to decide whether the row-bit
lift drops degree after adjoining `z` or `rho`.
The point-fiber probe adds a positive compatibility signal:
[P27 Trace/Norm Dplus U6 Row-Bit H90 Point-Fiber Probe](evidence/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_20260622.md).
In small fields, the row bit can be mixed over `t` alone, but all mixed `t`
fibers have no rational `E_h90` point; every tested rational `E_h90`,
domain-spin, and `A_eta` fiber is uniform, both with and without the
materialization filters.  So H90 still matters, but not as a simple bare
function-field factor over `E_h90`.
The class comparison now has a routing result:
[P27 Trace/Norm Dplus A-Descent Bridge](evidence/p27_trace_norm_dplus_a_descent_20260622.md).
Across three p27 seed groups, post-Dplus `d3` and `d4` after `d3=+1` have zero
mixed `A` groups.  Thus Dplus post-gate work should feed the A-level Kummer
extraction lane; trace/norm remains useful for exact two-gate prefix pricing
and source questions, not as an independent later-gate bucket family.

The naive orientation-source cover is now priced:
[P27 Trace/Norm Source-Orientation Cover](evidence/p27_trace_norm_source_orientation_cover_20260621.md).
Adjoining roots for `eps_h` and `eps_v`, then the trace/domain roots, produces
a degree-16 genus-21 source base.  Riemann-Hurwitz over `q=607` predicts genus
`69` after adjoining the final `D_plus` square root, uniformly for all four
sign components.  This kills "sample the full orientation cover" as the first
production idea.  The live trace/norm moonshot is narrower: find a low-genus
quotient/Prym factor of that genus-69 cover, or show by GPU telemetry that
`D_plus` recurs/couples to later selected x-square gates.

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

The exact single-section follow-up now kills that cheap irreducible-conic-sized
gap too:
[P27 E-Quotient L(4O) Exact Section Screen](evidence/p27_equotient_l4_section_exact_screen_20260622.md).
It exhaustively tested projective sections `a+bX+cX^2+dW` on
`E: W^2=X^3-X`.  For d3, p27-compatible fields
`q=487,599,727,919,1607` all have zero exact `L(4O)` sections.  For d4, the
smaller p27-compatible fields are one-sided after conditioning on d3, but the
non-degenerate `q=1607` check has `112` rows split `76/36` and also zero exact
sections.  This closes the nearest low-pole E-section route.  The live E
route is now actual double-cover/Kummer-class extraction, a higher named
divisor class, or a recurrence arising from the normalized cover.

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

The first low-pole random screen on the 2-isogenous quotient is also negative:
[P27 E-Prime Low-Pole Random Screen](evidence/p27_eprime_lowpole_random_screen_20260621.md).
It tested small-integer sections of `L(nO)` on `E': V^2=U^3+4U` and products
of two sections, at pole bounds `5,7,9`.  On p27 train/heldout splits there
were no exact candidates; best heldout scores were only `0.5225` for d3 and
`0.5295` for d4.  Guard fields `q=1471` and `q=1607` also produced no exact
candidate.  This kills the random low-pole `E'` pilot as a source.  The
remaining quotient lead is exact function-field or divisor-class extraction,
with online Magma suitable for small-field validation of named formulas.

The first affine-walk recurrence screen directly on `E'` is negative too:
[P27 E-Prime Affine-Walk Recurrence](evidence/p27_eprime_affine_walk_recurrence_20260621.md).
It tested every map `P -> [m]P + Q` for `m=+/-1,...,+/-8` and every
`Q in E'(F_q)` over `q=1471,1607,1847`.  The only full-coverage maps are
identity/negation, and they score like raw d4 bias: `28/56`, `38/56`, and
`52/90`.  Nontrivial exact overlaps cover at most about `21%` of the d4 rows.
This kills the small `E'` walk recurrence as a sqrt-beating source.

The p26 visible branch/H90 packet also fails to transfer:
[P27 E-Prime Branch-Factor Span](evidence/p27_eprime_branch_factor_span_20260621.md).
It tested all sparse products of size `1..4` from the p26 branch-degree-6
packet, vertical factors, tangent factors, and nearby lines on `E'`.  There are
no exact p27 or `q=1471,1607,1847` products.  The best 2k d4 branch product
looked mildly promising, but fresh 20k p27 validation flattened it to
`0.5039` and `0.5048`; the p26 branch packet itself is exactly `0.500` on the
fresh d3 samples.  This kills the visible branch-factor transfer.  The live
`E'` route is now explicitly cover/divisor-class extraction, not a sparse
visible factor product.

The reason plain `E'` screens may be missing the real object is now explicit:
[P27 E-Prime T-Cover Twist Obstruction](evidence/p27_eprime_tcover_twist_obstruction_20260621.md).
For the `(0,0)` quotient involution
`sigma(X,W)=(-1/X,W/X^2)`, the label-2 cover
`T^2=X(X^2+1)(X^2+2X-1)` satisfies `sigma(S)/S=X^-6`, so
`sigma(T)=+/-T/X^3`.  A rational `T`-linear invariant over `E'` would require
`sigma(f)/f=+/-X^3`, but `Norm(+/-X^3)=-1`; over the p27-compatible guard
fields `q=607,1471,1607,1847`, `chi(-1)=-1`, so the obstruction is not killed
by a base-field constant.  This reframes the next quotient test: work on the
twisted `T`-cover/Prym/Hilbert-90 class, possibly after adjoining `j^2=-1`,
using the concrete eigenfunction `Z=T*(1-j/X^3)` with `sigma(Z)=jZ`, then
descend a named class back to the p27 sign regime.  Do not repeat plain `E'`
low-pole or sparse-factor scans.  The online Magma `q=1471` check reports
`RESULT p27_eprime_tcover_twist_q1471 ok -1 1660 0 0 0 0 0`.

The first visible order-4 eigenspace packet is negative:
[P27 E-Prime Twisted Eigenspace Screen](evidence/p27_eprime_twisted_eigenspace_screen_20260621.md).
Using `j^2=-1` and `Z=T*(1-j/X^3)`, it tested `Z`, `Z^2`, `Z^4`,
branch-factor shifts, products, and base-field components over
`q=1471,1607,1847`.  There were no exact `d3` or `d4` packets.  The best
scores were field-dependent or raw-majority artifacts, so no GPU sampler
follows from this visible Hilbert-90 layer.  The remaining `E'` route is
actual twisted-cover divisor/Kummer/Prym extraction for the `d3` and `d4`
double covers, not more visible `Z/Z^2/Z^4` packet scans.

The quotient route now has a new positive reduction:
[P27 E-Prime Signed-Doubling Kummer Screen](evidence/p27_eprime_signed_doubling_kummer_screen_20260621.md).
Across twelve non-degenerate guard fields, both `d3` and `d4` are constant on
signed `[2]` projection classes on `E': V^2=U^3+4U`.  Thus the active
function-field target descends to the Kummer-line coordinate
`K=x([2]P)=(U^2-4)^2/(4U(U^2+4))`.  Exhaustive degree-1 and degree-2
polynomial-character screens in `K` are negative over `q=1471,1607,1847`, so
there is no rational source yet.  The next concrete sqrt-beating test is exact
degree `3/4` extraction on the K-line; a surviving cubic or quartic would give
an elliptic source candidate for the next all-plus gate.

The first compact K-line formula screen is negative:
[P27 Kummer Small-Integer Polynomial Screen](evidence/p27_kummer_small_integer_poly_screen_20260621.md).
It tested shared primitive integer cubic/quartic polynomials in `K` with
coefficients in `[-8,8]` across `q=1471,1607,1847`, allowing field-dependent
overall polarity.  No `d3` or `d4` polynomial was exact in all fields.  Best
minimum guard-field rates were only about `0.667` for `d3` degree 4 and
`0.714` for `d4` degree 4.  This keeps the K-line as the best reduced target,
but the next step should be branch-divisor/Kummer-class extraction on
`P^1_K`, not blind coefficient-bound widening.

The first exact K-line branch-divisor screen is also negative:
[P27 Kummer Branch-Divisor Screen](evidence/p27_kummer_branch_divisor_screen_20260621.md).
It tested all squarefree products of rational linear factors and irreducible
quadratic factors in `K` with total degree `<=4`.  For the decisive `d3`
source bit, there were no exact divisors over `q=1471,1607,1847`.  The d4
screen produced degree-3 fits in q1471/q1607 but none in q1847, so those are
small-row local interpolation artifacts.  This kills the first elliptic-source
subcase `z^2=f(K)` with split branch divisor of degree `<=4`; the live K-line
task is now irreducible cubic/quartic branch extraction or a Magma/Sage
divisor/genus computation.

The branch-divisor conclusion survives the corrected guard-field rule:
[P27 Signature-Field Branch-Divisor Replay](evidence/p27_signature_field_branch_divisor_replay_20260621.md).
Using only p27-signature fields `q = 7 mod 16`, `d3` has no exact K-line split
branch divisor of degree `<=4` in q1607, q1847, q2039, or q2087, and no exact
S-root split branch divisor of degree `<=4` in the same fields.  K-line `d4`
has degree-3 local fits in q1607 and q2087, but not q1847; q2039 has constant
`d4` and is not promotion evidence.  Thus the corrected replay keeps `d3`
negative and demotes `d4` fits to local interpolation artifacts.

The nearest monic cubic K-line subcase is negative on a small guard field:
[P27 K-Line Cubic Exhaustive Pilot](evidence/p27_kline_cubic_exhaustive_20260621.md).
Over the p27-compatible field `q=607`, the selected `d3` K rows are balanced
`16/16`.  An exhaustive check of all `223,648,543` monic cubics
`K^3+aK^2+bK+c`, allowing global polarity, found no exact character match and
no exact irreducible cubic.  The best miss was `31/32`.  This is only a local
falsifier, not a p27 proof, but it reinforces the current rule: do actual
K/S branch-class and genus extraction rather than widening blind cubic scans.

The visible K-polynomial source shape has now had its decisive q1847 d3
screen:
[P27 K-Line Quartic GPU Test Card](evidence/p27_kline_quartic_gpu_test_card_20260622.md).
The full monic quartic q1847 test for `d3_on_K` found zero exact quartics:
[P27 Full Quartic q1847 D3 Screen](evidence/p27_full_quartic_q1847_d3_screen_20260622.md).
A q1847 d3 hit would have been highly non-random
(`expected_exact ~= 2.52e-6`), so this kills the decisive K-line visible
degree-4 polynomial source shape.  q1471/q1607 closure is now bookkeeping
rather than a promotion path unless a new named class changes the target.
The B/K coordinate bridge is now explicit:
[P27 B-Line / K-Line Bridge](evidence/p27_b_kline_bridge_20260622.md).
For q1471/q1607/q1847/q2087, the relation
`K^2=(B-2)^4/(8B(B+2)^2)` maps every legal B d3/d4 row to a present signed K
class with the same target sign.  The B-line and K-line quartic GPU screens
are therefore coordinate alternatives for the same descended class, not
independent confirmations.
The signed-root selector over that bridge is not a shortcut:
[P27 B/K Signed-Root Relation Screen](evidence/p27_b_kline_signed_root_relation_20260622.md).
The selected K sheet has no positive extra low-degree plane relation beyond
the inherited bridge cover in q1471/q1607/q1847/q2087.
The descended even-quartic subcase is also dead:
[P27 K-Line Even-Quartic Screen](evidence/p27_kline_even_quartic_screen_20260622.md).
Over q1471/q1607/q1847, `chi(K^4+a*K^2+b)` has zero exact hits for both
`d3_on_K` and `d4_on_K_after_d3`.  So the completed q1847 screen correctly
tested full quartics with odd K terms and the signed K sheet, not a
`K^2`-only proxy.
The visible Belyi reciprocal subcase is dead too:
[P27 K-Line Belyi-Reciprocal Quartic Screen](evidence/p27_kline_reciprocal_quartic_screen_20260622.md).
The two shapes preserved by `K -> 4/K`,
`K^4+aK^3+bK^2+4aK+16` and `K^4+aK^3-4aK-16`, have zero exact hits over
q1471/q1607/q1847.  Thus the full q1847 coefficient-triple screen was the
right decisive test.
The full B/K quartic handoff is now partly executed and locally checkable:
[P27 Full Quartic GPU Suite Handoff](evidence/p27_full_quartic_gpu_suite_handoff_20260622.md)
and
`research/p27/archive/fixtures/p27_full_quartic_gpu_suite_20260622.json`
give the run order, verifier commands, exact packets, and promotion/kill
rules for the B-line/K-line monic-quartic test.  The q1847 `d3` screens in
both B and K coordinates are complete and negative, using a new fast local C
oracle.  This closes the visible q1847 monic-quartic `d3` promotion route.
Remaining quartic work is optional closure bookkeeping, gate4-prefix closure,
or hit verification if another agent produces a candidate; it is no longer
the front-door sqrt-beating lane.
If a hit appears, the promotion-side verifier is also ready:
[P27 Quartic Hit Geometry Promotion Tool](evidence/p27_quartic_hit_geometry_promotion_tool_20260622.md)
checks the frozen target rows and classifies `z^2=f(B)` or `z^2=f(K)` by
squarefree degree, factor degrees, finite-field point count, and normalization
genus.

The fallback branch-extraction ask remains packaged as a separate concrete
handoff:
[P27 Kummer Branch-Extraction Handoff](evidence/p27_kummer_branch_extraction_handoff_20260621.md).
That fallback is now organized as an ordered CAS suite:
[P27 Post-Quartic CAS Suite Handoff](evidence/p27_post_quartic_cas_suite_handoff_20260622.md)
with manifest
`research/p27/archive/fixtures/p27_post_quartic_cas_suite_20260622.json`.
The cheap K/S guard-field sanity layer is complete:
[P27 K/S Guard-Field Sanity](evidence/p27_ks_guard_field_sanity_20260622.md)
checks q1607/q1847/q2087 with zero mismatches for the K/S map and H90
identities.
It records the map from the residual `E: W^2=X^3-X` through
`E': V^2=U^3+4U` to
`K=x([2]P)=((X^2-2X-1)^2*(X^2+2X-1)^2)/(4X(X-1)(X+1)(X^2+1)^2)`,
together with the reverse-source equations for the `d3` all-plus extraction.
The next serious test is to normalize this cover over `P^1_K` in Magma/Sage
and compute the actual branch divisor degree, support field degrees, and genus
over p27-signature guard fields such as `q=1607,1847,2087`.  This is the
current best "could beat sqrt" theorem checkpoint: genus `<=1` or a named
recurrence/sourceable walk promotes; high/generic branch degree with unrelated
`d4` kills the K-line source route.

The first actual Magma normalization smoke is strongly cautionary:
[P27 K/S First-Half Cover Magma Smoke](evidence/p27_ks_first_half_cover_magma_20260621.md).
The full q7 reverse-source fixture and eta-component fixture both hit the
online calculator memory limit.  Staging the equations shows why saturation is
necessary: the raw first-half layer is dimension `2` with `77` affine points,
so cleared-denominator artifacts remain.  After saturating by
`X*(X-1)*(X+1)*(T-2X^2)`, the eta=`+1` first-half layer becomes a curve:
`SAT_SCHEME_OK 1 42 3` and `SAT_CURVE_OK 37 3`.  This is not a promotion-field
theorem, but it is a real obstruction to a direct low-genus K/S source: genus
`37` appears before adding the final reverse-square variables.  The K/S route
now needs an offline promotion-field normalization plus a non-obvious quotient
or recurrence; online full-source normalization and coefficient widening are
not the right next moves.

The most obvious quotient shortcut is now obstructed over the p27 base field:
[P27 K/S First-Half Alpha-Lift Obstruction](evidence/p27_ks_first_half_alpha_lift_obstruction_20260621.md).
The first-half `B` branch class factors as
`32*T*X*(eta*T*W + X*(X-1)*(X+1)^2)*(2*eta*W*X + X^3 + X^2 - X - 1)`.
For `eta=+1`, the same-eta alpha lift ratio is exactly `-1` times a square on
the intermediate curve; since p27 is `3 mod 4`, the lift is not `F_p`-rational.
The eta-swapped ratio is mixed on q1607/q1847/q2087.  Thus the generic
"quotient the genus-37 layer by alpha" test is demoted: it is useful only if an
`F_{p^2}` geometric quotient comes with an explicit `F_p` descent, or if the
actual d3/d4 double covers produce a separate low-genus source.

The right quotient for that separate source is now reinforced:
[P27 K/S First-Half E-Prime Descent](evidence/p27_ks_first_half_eprime_descent_20260621.md).
Translation by `(0,0)` sends `X -> -1/X`, `W -> W/X^2`, and
`T -> +/-T/X^3`; symbolically `T2(-1/X)=T2(X)/X^6`, and over
q1607/q1847/q2087 both T-lifts preserve compactD and the first-half
`B`-branch squareclass on every compactD point tested.  This turns the next
K/S extraction into a concrete E-prime task:
extract the actual d3/d4 double covers on `E': V^2=U^3+4U`, compute their
branch divisors/Kummer classes/genera, and decide whether d4 is a fresh cover
or a recurrence/sourceable transform of d3.

The first E-prime pullback smoke keeps the genus warning in force:
[P27 E-Prime First-Half Pullback Magma Smoke](evidence/p27_eprime_first_half_pullback_magma_20260621.md).
After substituting `W=V*X^2/(X^2+1)` and saturating by the known denominator
divisors, online Magma over q7 reports `EPRIME_PULLBACK_SAT_SCHEME 1 61 0`
and `EPRIME_PULLBACK_SAT_CURVE 37 0`.  Thus E-prime is the right extraction
coordinate, but not a direct low-genus source; the win must be a lower-genus
factor, Kummer-class relation, or recurrence inside/under the genus-37 staged
cover.

The actual d3 z-source is now staged but still needs offline CAS:
[P27 E-Prime D3 Z-Source Magma Smoke](evidence/p27_eprime_d3_zsource_magma_20260621.md).
All-at-once saturation of the z-source ideal hits the online memory limit after
showing raw dimension `3`.  Sequential saturation also exceeds the limit.  The
successful staging is to first compute the saturated first-half ideal
`Iclean`, then add the reverse-source equation `reverse_z`, producing
`D3_Z_AFTER_FIRSTHALF_SCHEME 1 62 0` over q7.  Online Magma cannot compute
genus/normalization for this curve, so the concrete next test is offline
normalization of `J = Iclean + <reverse_z>` over q7 and p27-signature guard
fields, then branch/Kummer-class comparison against d4.

The nearest exact low-pole section family on E' is now killed:
[P27 E-Prime L(4O) Exact Section Screen](evidence/p27_eprime_l4_section_exact_screen_20260621.md).
The probe exhaustively tested projective sections
`a+bU+cU^2+dV` on p27-signature fields.  q487 has local exact quadratic-U
artifacts, but q599, q727, and q919 all have non-degenerate d3 splits and zero
exact L(4O) sections.  So the E' source, if it exists, is not a single
irreducible-conic-sized section; it must come from the actual normalized
z-source curve, a higher divisor/Kummer class, or a recurrence visible only
after the d3 class is named.

The next rational U-line loophole is also closed:
[P27 E-Prime U-Cubic Exact Screen](evidence/p27_eprime_ucubic_exact_screen_20260621.md).
Exact U-cubic polynomials `a+bU+cU^2+dU^3` occur locally in q487, q599, and
q727, but disappear on q919, q967, and q1063.  This demotes univariate U-line
coefficient widening as another interpolation trap.  The surviving E' task is
not "try degree 4"; it is normalize `J = Iclean + <reverse_z>` and recover the
actual branch/Kummer class.

That branch class is now partially named:
[P27 E-Prime Reciprocal R-Quotient Branch Screen](evidence/p27_eprime_rquotient_branch_screen_20260621.md).
The reverse-source equation is reciprocal in `s=z^2`; setting
`r=s+1/s` gives a real quotient curve, and online Magma reaches
`D3_RQUOT_AFTER_FIRSTHALF_SCHEME 1 62 0` before the same memory limit.  On two
20,000-candidate p27 samples and guard fields q1607/q1847/q2087, every usable
row has a single `r`, the r-quadratic discriminant is always square, and
`d3 = chi(r+2) = chi(r-2)` with zero mismatches.  Thus the r quotient itself is
not a d3 source; it quotients away the squareclass.  The sharper live CAS target
is the divisor/Kummer class of `r+2` on the normalized r-quotient, or a
recurrence/source for many `chi(r_j+2)` bits at once.

The first recurrence model for that class is now explicit:
[P27 S-Map Quartic Recurrence Probe](evidence/p27_smap_quartic_recurrence_20260621.md).
With `r=S^2-2`, the all-plus reverse-doubling map is
`x_prev=S^2*(S^2-4)/(4*(S^2+A-2))`.  One more all-plus step gives a quartic
`F(Y)` in `Y=S_next^2` whose discriminant is a square times known degenerate
divisors.  Over q1607/q1847/q2087, every d3-plus row has four `Y` roots, and
either all four are squares or none are; this common root squareclass equals
`d4` with zero mismatches.  But the nearest split class `chi(S^2+A-6)` is flat
on p27 heldout, and the named quartic-factor GF(2) span has no exact train
combo.  The next live test is therefore a resolvent/theta/Kummer formula for
the common root squareclass of `F(Y)`, not another coefficient/factor screen.

That resolvent now simplifies to a repeated conic gate:
[P27 Quadratic Gate Recurrence](evidence/p27_quadratic_gate_recurrence_20260621.md).
In the square-root coordinate, write `A=2-c^2` and `x=r^2`.  Then the next
selected x-square gate is exactly `chi(r^2+c*r+1)`, independent of the signs
of `c` and `r` in the tested tower.  This matched p27 train and heldout through
gates 3-8 with zero mismatches, and q1607/q1847/q2087 at gates 3-4 with zero
mismatches.  This is the first genuinely source-shaped p27 recurrence: the
next beat-sqrt test is to parametrize or pull back chains of conics
`h_j^2=r_j^2+c*r_j+1` to the legal X1(16)/compactD starting surface, or prove
that each step still introduces a fresh independent cover.

The first source-screen for that chain is positive but incomplete:
[P27 Conic-Chain Source Screen](evidence/p27_conic_chain_source_screen_20260621.md).
Legal halving requires both conjugate conics
`h_j^2=r_j^2+c*r_j+1` and `g_j^2=r_j^2-c*r_j+1`, with
`r_{j+1}^2-(h_j+g_j)r_{j+1}+1=0`.  Online Magma over q7 reports dimension `2`
for depth 1 and depth 2 chain ideals, while finite-field counts through depth
4 over q103/q263/q607 and depth 2 over q1607 show zero xDBL mismatches and
output projections staying near `0.5*q^2`.  This supports a genuine lifted
two-dimensional chain object.  On actual label-2 / compactD rows in
q1607/q1847/q2087, depth-1 conic-chain lifts are exactly the d3-plus rows and
depth-2 lifts are exactly the d4-plus-after-d3 rows.  The full q7 E-prime
legal pullback fixture still hits the web Magma memory limit, so the remaining
decisive test is a staged elimination/normalization of the legal pullback,
not another count check.

That source test now has a GPU-ready handoff:
[P27 GPU Conic-Chain Test Handoff](evidence/p27_gpu_conic_chain_test_handoff_20260621.md).
The one-step legal pair can be sampled directly from two nonzero parameters
`R,L` by setting `a=R-1/R`, `s=R+1/R`, `d=(L-a^2/L)/2`,
`r=-(L+a^2/L)/4`, `h=(s+d)/2`, `g=(s-d)/2`, and `c=s*d/(2*r)`.  This
identically satisfies the two conjugate conics and the transition to `R`; it
validated on q1607/q1847/q2087 and p27 random trials.  So the answer to
"should GPU test this?" is yes, but only as a bounded conic-chain source and
telemetry test.  A large production hunt should wait until the direct sampler
either pulls back to legal rows at useful rate or controls more than one
selected gate without paying a fresh half-loss.

The direct sampler incidence is now measured:
[P27 Conic-Pair Sampler Legal Incidence](evidence/p27_conic_pair_sampler_legal_incidence_20260621.md).
Across q263/q607/q1607/q1847/q2087 it covers every legal d3-plus `(A,x5)`
class tested and zero d3-minus classes, so the structure is real.  But random
free `(R,L)` hits legal rows at only about `constant/q` per draw, so the raw
two-dimensional sampler is killed as a production GPU source.  The live target
is sharper: find the legal pullback/quotient or a d4 recurrence on the
intersection.

The d4 recurrence now has an exact selector:
[P27 Conic-Pair D4 Recurrence](evidence/p27_conic_pair_d4_recurrence_20260621.md).
With `a=R-1/R` and `L=h-g-2r`, the next gate satisfies
`chi(R^2+cR+1)=chi(-(L+a)(L-a)cR)` because the quotient is `2` times a square
and p27 has `chi(2)=+1`.  This held on q1607/q1847/q2087 and on 1,000-row p27
train/heldout samples.  The selected next coordinate still does not re-enter
the original legal label-2/compactD source in the guard fields, so the live
test is now the legal pullback with `Z^2=-(L+a)(L-a)cR`, not blind iteration of
the same sampler.

The repeated-tower check is positive:
[P27 Conic-Pair D5 Tower](evidence/p27_conic_pair_d5_tower_20260621.md).
After adjoining the d4 selector root, the same product law gives d5 with zero
mismatches on q1607/q1847/q2087 and p27 train/heldout samples, including a
larger `1500 + 1500` p27 confirmation.  This promotes the conic-chain lead
from a one-off d4 identity to a recursive Kummer selector tower.  The
obstruction remains source-side: the selected one-step and two-step
coordinates do not re-enter the original legal label-2/compactD source in the
guard fields.

The legal source-side depth screen is now explicit:
[P27 Legal Conic Tower Depth](evidence/p27_legal_conic_tower_depth_20260621.md).
In q1607/q1847/q2087, legal conic-chain lift existence matches selected-prefix
bits through depth 5 with zero mismatches.  On the larger p27 train/heldout
samples, prefix rates through depths 1-5 are about
`0.481/0.245/0.104/0.057/0.028` and
`0.519/0.240/0.111/0.061/0.028`.  Thus the tower is exact, but not
density-beating on the original legal source without a quotient or direct
tower sampler.
The remaining conic moonshot is now packaged as:
[P27 Conic Tower Quotient CAS Handoff](evidence/p27_conic_tower_quotient_cas_handoff_20260622.md)
with manifest
`research/p27/archive/fixtures/p27_conic_tower_quotient_cas_suite_20260622.json`.
It asks for depth-1/depth-2 legal-pullback quotients, genus/components, and a
direct legal tower sampler if a quotient appears.
The first quotient sanity screen is now in:
[P27 Conic Tower Sign-Quotient Probe](evidence/p27_conic_tower_sign_quotient_20260622.md).
The obvious sign quotients preserve d5 and even descend to `A`/`(A,x)` on p27
samples, but they collapse only finite multiplicities.  A-space still thins
like random half-loss, so this is CAS staging, not a GPU sign-bucket source.
The d6 continuation is now positive too:
[P27 Conic Tower D6 A-Descent](evidence/p27_conic_tower_d6_a_descent_20260622.md).
On `1000 + 1000` p27 train/heldout rows, d6 has zero mixed `A` groups after
d4-plus/d5-plus (`49` and `54` base-A groups respectively).  This promotes an
A-level Kummer-class extraction for d4/d5/d6, but still not a GPU A-bucket run:
the older A-prefix profile shows ordinary half-loss on A-space.
The cheap deeper follow-up is stronger:
[P27 A-Level Prefix Descent](evidence/p27_a_level_prefix_descent_20260622.md).
On `12000 + 12000` p27 train/heldout samples, selected gates d3..d14 all have
zero mixed A groups.  Robust counts through about d10 stay near the geometric
half-loss baseline, so the moonshot target is a normalized A-line Kummer
sequence/class extraction, not a prefix-count source.
The first visible A-character falsifier is now negative:
[P27 A-Line Character Support Screen](evidence/p27_a_line_character_support_20260622.md).
Complete degree `<= 4` branch-support families on `P1_A` are killed for d3 in
q1607/q1847/q2087, q1847 also kills d4, and nearby `7 mod 8` fields reject
split degree `<= 4` d3 support.  Do not widen blind A-polynomial scans; the
next real test is divisor/Kummer class extraction on the normalized A-cover.
The combined-prefix version is negative too:
[P27 A-Line Combined Prefix Support Screen](evidence/p27_a_line_prefix_support_20260622.md).
The all-plus `d3&d4` prefix has no visible degree `<= 4` A-line character in
q1607/q1847/q2087.  Three- and four-gate prefixes are either one-sided
finite-field tails or repeat the same negative pattern.  This kills GPU
A-prefix bucket production unless a named Kummer/source law is found.
That extraction now has a concrete packet:
[P27 A-Level Kummer Extraction Packet](evidence/p27_a_level_kummer_extraction_packet_20260622.md).
It emits a JSON fixture of A-labeled d3/d4 rows over q1607/q1847/q2087 and
asks CAS to recover the normalized A-cover, branch divisor data, genus, and
successive Kummer-class relations.  This is the next first-class conic/A-line
test that could still beat sqrt if it finds recurrence rather than fresh
half-covers.
The A/B row-level bridge is exact:
[P27 B/A Fixture Bridge](evidence/p27_b_a_fixture_bridge_20260622.md).
Across q1607/q1847/q2087 and gates d3/d4, `A=B^2-2` gives `267/267`
row-level sign matches with no missing rows, uncovered A rows, or collisions.
This folds A into the coordinated A/B/K/Sroot class-extraction problem; it is
not a separate GPU A-bucket lane.
The trace/norm bridge now points here too:
[P27 Trace/Norm Dplus A-Descent Bridge](evidence/p27_trace_norm_dplus_a_descent_20260622.md).
On three Dplus-conditioned p27 seed groups, `d3` and `d4` after `d3=+1`
descend to whole `A` fibers with zero mixed groups.  This collapses the
post-Dplus later-gate question into the same A-level Kummer class sequence,
while leaving fused/native Dplus pricing as a separate engineering test.
The cheap visible-transform recurrence is now closed:
[P27 A-Line Named-Transform Recurrence Screen](evidence/p27_a_line_named_transform_recurrence_20260622.md).
The S3 group preserving the visible A-branch set `{-2,2,infinity}` almost
never maps the legal A-domain back to itself.  In q1847 it has zero
non-identity d3 coverage, and in p27 `4000 + 4000` train/heldout samples every
non-identity transform has zero d3..d8 coverage.  So the A-line route cannot
be promoted through a visible orbit or `d_{j+1}(A)=d_j(T(A))` shortcut; it
still needs actual normalized-cover/Kummer-class extraction.
The broader affine A-line recurrence is now killed too:
[P27 A-Line Affine Recurrence Screen](evidence/p27_a_line_affine_recurrence_screen_20260622.md).
It tests every full-coverage map `A -> m*A+b` for the meaningful
`d3 -> d4` transition in q1607/q1847/q2087.  All three promotion fields have
zero exact affine recurrences; the best full-coverage maps are identity and
score only the raw d4 bias (`19/28`, `26/45`, `18/25`).  Later exact identity
maps occur only in small-field one-sided tails with field-dependent signs and
stop gates.  Thus an A-line win must be a normalized Kummer class,
non-affine correspondence, coboundary, or higher structure, not a cheap
degree-one A recurrence.
The full degree-one rational A-line recurrence is killed as well:
[P27 A-Line PGL2 Recurrence Screen](evidence/p27_a_line_pgl2_recurrence_screen_20260622.md).
It enumerates every full-coverage PGL2 map
`A -> (aA+b)/(cA+d)` for the same `d3 -> d4` transition.  q1607, q1847, and
q2087 all have zero exact PGL2 recurrences; again the best maps are identity
with raw d4-bias scores.  Do not spend more agent or GPU time on degree-one
A-line recurrence scans unless a theorem supplies a different object.
The first theorem-shaped higher A-correspondence is negative too:
[P27 A-Level Power-Correspondence Screen](evidence/p27_a_level_power_correspondence_screen_20260622.md).
It projects the hidden-`X` power maps from the B-line through `A=B^2-2`,
allowing both B roots and all Belyi conjugations for `X -> X^m`, `m=2..6`.
There are no exact forward or reverse `d3/d4` recurrences in
q1607/q1847/q2087.  The best forward coverage is only `9/28`, `17/45`, and
`11/25`, so forgetting B sign does not recover a sourceable hidden-`X`
recurrence.
The canonical Chebyshev/Dickson self-maps of the A branch set are now negative:
[P27 A-Line Chebyshev Recurrence Screen](evidence/p27_a_line_chebyshev_recurrence_screen_20260622.md).
It tests `D_m(A)=2*T_m(A/2)` for `m=2..12`, conjugated by the six branch-S3
symmetries.  No full-domain recurrence appears in q1607/q1847/q2087; the
main `d3 -> d4` best coverages are only `10/28`, `17/45`, and `9/25`.  Later
perfect-looking rows are low-coverage small-field one-sided tails.  This
leaves normalized A-cover Kummer extraction, not A-line dynamics, as the live
route.
The K/lambda normalized branch line has the same negative outcome:
[P27 Lambda Monomial Recurrence Screen](evidence/p27_lambda_monomial_recurrence_screen_20260622.md).
It tests S3-conjugated `lambda -> lambda^m` maps for `m=2..12` on
`lambda=-K^2/4`.  There is no exact forward or reverse `d3/d4` recurrence in
q1471/q1607/q1847, with best forward coverages only `4/28`, `5/28`, and
`9/45`.  Thus lambda remains useful for branch-class normalization, not as a
standalone recurrence/source.
The lambda low-genus subcase is sharpened:
[P27 Lambda Low-Genus Screen](evidence/p27_lambda_lowgenus_screen_20260622.md).
It freezes lambda targets and exhausts all monic cubic support for
`d3_on_lambda` in q1471/q1607/q1847, finding zero exact cubics.  The decisive
q1847 exact monic quartic screen is now closed too:
[P27 Lambda Quartic q1847 D3 Screen](evidence/p27_lambda_quartic_q1847_d3_screen_20260622.md).
It scans `6,300,872,423` coefficient triples and finds zero exact quartics.
Thus lambda is no longer a GPU quartic target; it remains a normalization
coordinate for actual K-level branch-class extraction with the K-square stratum
preserved.
The compact synthesis after these closures is:
[P27 Post-Branch-Dynamics Test Frontier](evidence/p27_post_branch_dynamics_test_frontier_20260622.md).
It lists the closed branch-map families and the remaining first-class tests:
coordinated A/B/K/Sroot Kummer extraction with the rational K-square stratum
preserved and the trace/norm half-norm phase identity.  BSM is now demoted to
a coordinate view of the one-step halving cover unless a non-inherited selector
is added.  GPU is demoted to bounded telemetry or
direct-sampler testing until one of those produces a named class or source.
The K/Sroot density shortcut is now priced too:
[P27 K/Sroot Prefix Profile](evidence/p27_sroot_prefix_profile_20260622.md).
It shows that selected prefix bits descend cleanly to both K and Sroot, but
Sroot is only a doubled K grouping with identical all-plus prefix ratios.  This
strengthens Sroot as the normalization coordinate for CAS and kills Sroot
prefix buckets as a GPU/source shortcut.
The compact K/Sroot class fixture is now frozen:
[P27 K/Sroot Kummer Fixture Packet](evidence/p27_ksroot_kummer_fixture_packet_20260622.md).
It records conditional `f3/f4/f5/f6` rows over q1607/q1847/q2087 for both K
and signed Sroot, with `Sroot^2=K` included row-by-row.  Every K row has two
Sroot rows and the signs double, so the live test is normalized `f3` branch
class extraction preserving K-square rationality, then `f4/f3` comparison.
The row-level coordinate bridge is exact:
[P27 B/K/Sroot Fixture Bridge](evidence/p27_b_ksroot_fixture_bridge_20260622.md).
Through every nonempty recorded gate, B rows map to exactly one signed K row
and two Sroot rows with matching signs.  This collapses B-line and K/Sroot to
one coordinated class-extraction lane rather than independent evidence.
The A quotient view has now been bridged too:
[P27 B/A Fixture Bridge](evidence/p27_b_a_fixture_bridge_20260622.md).
For the frozen d3/d4 fixtures, A is exactly the quotient coordinate
`A=B^2-2` with signs preserved.  The live CAS ask is therefore one
A/B/K/Sroot normalized-class extraction, choosing whichever coordinate makes
the branch divisor easiest.
The first local fiber-invariant extraction is now done:
[P27 B-Line Fiber Invariant Probe](evidence/p27_b_line_fiber_invariant_probe_20260622.md).
For every legal B in q1607/q1847/q2087, the d3 next-root fiber has `32`
occurrences but only `8` distinct x-roots, closed under `x -> 1/x`, hence
`4` values of `u=x+1/x`; all satisfy `f3=chi(u+2)`.  The full product/norm is
always square, power sums through exponent `64` have no exact or near
selector, and the four-u coefficients are maximal-degree on the legal-B set.
So the next CAS object is the reduced 4-u/8-x cover, not a GPU symmetric
invariant sampler.  The exact row-level fixture is
`research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json`.
The reduced-cover plane relation screen is now negative too:
[P27 B-Line Reduced-Fiber Relation Screen](evidence/p27_b_line_reduced_fiber_relation_20260622.md).
Across q1607/q1847/q2087, `(B,u)`, `(B,u^2)`, `(B,u+2)`, `(A,u)`,
`(lambda,u)`, `(mu,u)`, and the f3 plus/minus subcovers all have
`extra_nullity=0` through total degree `20`.  This kills the cheap plane-model
route; the remaining test is actual normalization/genus/quotient extraction
of the reduced cover.
The reduced-cover symbolic handoff is now explicit:
[P27 B-Line Reduced-Cover Symbolic Packet](evidence/p27_b_line_reduced_cover_symbolic_packet_20260622.md).
It rewrites the d3 cover using `Unext=x6+1/x6` and
`(Unext-2*x5)^2=4*(x5^2+A*x5+1)`, then emits that equation in the B-line
source variables.  Validation over q1607/q1847/q2087 has zero reduced-equation
or selector mismatches.  This is the first CAS normalization target before the
full reverse `z,Y` cover.
The first online Magma smoke for this reduced cover is cautionary:
[P27 B-Line Reduced-Cover Magma Smoke](evidence/p27_b_line_reduced_cover_magma_smoke_20260622.md).
Even over q7, the saturation-only fixture exceeds the online calculator memory
limit during `Saturation(I,bad)`.  The reduced cover remains the right first
offline CAS/expert object, but this is not a GPU-production green light.
A direct finite-field point-count probe then clarifies the offline object:
[P27 B-Line Reduced-Cover Point Count](evidence/p27_b_line_reduced_cover_pointcount_20260622.md).
In q1607/q1847/q2087, every legal chart point has two `U_next` roots, but the
materialized `x6` layer and selector cover `gamma^2=U+2` split by B-fiber into
0/middle/full lift profiles.  So the next CAS pass should attach those layers
and extract their branch/Kummer classes; the bare U double cover is not a
source and does not justify GPU production.
The nearest visible classifier for those lift profiles is now negative:
[P27 B-Line Reduced-Lift Classifier Screen](evidence/p27_b_line_reduced_lift_classifier_20260622.md).
Across q1607/q1847/q2087, no pair of named atoms, rational-linear factors, or
monic irreducible quadratic factors classifies the 0/mixed/full B-fiber lift
profile.  This closes the obvious two-character sampler shortcut and keeps the
lane pointed at actual branch/Kummer extraction.
That result is now reconciled with the frozen legal B fixture:
[P27 B-Line Reduced-Domain Reconciliation](evidence/p27_b_line_reduced_domain_reconcile_20260622.md).
The legal fixture equals `legal_b_maps`, is contained in the point-count chart,
and has no mixed fibers: `lift_units=2` is exactly `d3 plus`, while
`lift_units=0` is exactly `d3 minus`.  The mixed point-count fibers are outside
the selected-source legal domain, so the next CAS pass must impose that
legal/core cut before extracting branch/Kummer classes.
The first second-fiber artifact is now frozen:
[P27 B-Line Second Reduced-Fiber Fixture](evidence/p27_b_line_second_reduced_fiber_20260622.md).
On the legal `f3=+1` B-domain, each active row has `64` x7 occurrences,
`16` distinct x7 roots, and `8` values of `v=x7+1/x7`, with
`f4=chi(v+2)` throughout q1607/q1847/q2087.  Stable plane relations in
`(B,v)` and `(B,v+2)` are absent through degree `20`, so the B-line ask is now
a true f3-vs-f4 Kummer/divisor class comparison, not another GPU bucket.
The transition/orientation layer is now explicit too:
[P27 B-Line Transition Closure And Orientation](evidence/p27_b_line_transition_closure_orientation_20260622.md).
The generic quotient transition
`(v^2-4)^2 - 4*u*(v^2-4)*(v+A) + 16*(v+A)^2 = 0` has `4` v-roots per u-root,
while the actual selected source keeps exactly the `2` roots with
`chi(v^2-4)=chi(v+A)=+1`.  That half is just the visible lift from quotient
`v` to actual `x7`; `chi(v+2)=f4(B)` is already constant on the larger generic
transition.  The live CAS object is therefore the staged cover
`F_A(u,v)=0`, `rho^2=v^2-4`, `gamma^2=v+2`, and the live question is whether
`gamma` is a sourceable Kummer class rather than a fresh half-cover.
The first gamma norm/coboundary screen is now bounded:
[P27 B-Line Gamma Norm/Coboundary Boundary](evidence/p27_b_line_gamma_norm_coboundary_20260622.md).
`Norm_4(v+2)=16*(A-2)^2`, and the actual/missing two-root gamma norms are
always square in q1607/q1847/q2087.  But the naive parent-`x6` norm formula is
false, and no visible pair-invariant product through weight `4` predicts
`f4`.  This keeps a real H90/coboundary CAS question alive while killing
gamma norm-triviality as a direct GPU/source rule.
The explicit H90 quotient is now computed:
[P27 B-Line Gamma H90 Quotient](evidence/p27_b_line_gamma_h90_quotient_20260622.md).
For `r=(v1+2)/(v2+2)` and `h^2=r`, the identities `r+1/r=u` and
`(h+1/h)^2=u+2` hold with zero failures.  Thus the quotient collapses to the
already-imposed first reduced `f3` layer and does not predict `f4`; the live
object is now `gamma` as a class over that f3/H90 layer.
The visible f3/H90-layer screen is also negative:
[P27 B-Line Gamma Over F3/H90 Layer Relation Screen](evidence/p27_b_line_gamma_f3_layer_relation_20260622.md).
After adjoining both sheets `H=+/-(h+1/h)`, stable pair-coordinate screens in
`(B,H)`, `(B,tau)`, `(B,H^2)`, and `(B,tau_sym)` do not expose `f4`.  The live
B-line task is now actual divisor/Kummer-class extraction for `gamma` over the
normalized f3/H90 layer, not another visible coordinate bucket.
That extraction now has a compact handoff:
[P27 B-Line Gamma Class Handoff](evidence/p27_b_line_gamma_class_handoff_20260622.md).
It freezes q1607/q1847/q2087 rows for the staged object
`A=B^2-2`, `H^2=u+2`, `F_A(u,v)=0`, and `gamma^2=v+2`.  Every active parent
has four generic transition roots, two materialized roots, two discarded roots,
constant `chi(v+2)` on the generic roots, and zero failures in the norm/H90
identities.  The next accepted B-line result must classify this `gamma` class
as pullback/coboundary/quotient/recurrent, or kill it as a fresh half-cover.
The class now has an explicit V4 factorization:
[P27 B-Line Gamma V4 Factorization](evidence/p27_b_line_gamma_v4_factorization_20260622.md).
Writing `Y=v+2`, the quartic `P(Y)` has square discriminant and split cubic
resolvent; after adjoining `R^2=H^2-4` and `S^2=B^2+H^2-4`, its roots are
`(H +/- R)*(H +/- S)`.  Thus `f4=chi(v+2)=alpha*beta`, where
`alpha=chi(H+R)` and `beta=chi(H+S)`.  Both factors flip under `H -> -H`,
while the product is invariant and constant on active B.  This gives the next
bounded GPU/CAS target: test the successive `alpha_j,beta_j` phase sequence
for recurrence or telescoping; do not promote either factor as a standalone
bucket.
The visible gamma-square shortcut is now killed:
[P27 B-Line Gamma Specialized Square Smoke](evidence/p27_b_line_gamma_specialized_square_smoke_20260622.md).
In irreducible `GF(7)` and `GF(23)` one-parameter specializations of the
`B/H/Y` transition, `Y=v+2` is not square while `Norm(Y)` remains the expected
square.  So the V4 norm-square pattern does not trivialize gamma on the
visible B/H layer; the remaining task is still normalized divisor/Kummer
class extraction or a recurrence/telescoping relation.
The first phase-sequence screen is negative:
[P27 B-Line Alpha/Beta Phase Sequence Screen](evidence/p27_b_line_alpha_beta_phase_sequence_20260622.md).
On `3000+3000` p27 train/heldout starts, the main next-product rates stay near
random half-loss, and link products such as `alpha_j*alpha_{j+1}` remain near
`1/2`.  The small gate4-to-gate5 phase-state skew is only about `1.1x`
conditional and costs a half split, below the source-normalized promotion bar.
Guard-field all-plus/all-minus plateaus stop at different gates, so they are
field-tail artifacts.  Keep alpha/beta as optional telemetry columns, not a
production mode.
The natural sheet-orientation loophole is also closed:
[P27 B-Line Oriented Phase-Word Screen](evidence/p27_b_line_oriented_phase_word_screen_20260622.md).
With `H=(x+1)/sqrt(x)`, `alpha=+1` and `beta` equals the actual selected gate
bit through gate 9 on `6000+6000` p27 starts.  The apparent conditional lifts
keep the same target/source denominator as baseline, so this orientation is a
tautological gate filter rather than a recurrence.
The pre-registered phase-word source screen is negative too:
[P27 B-Line Phase-Word Source Screen](evidence/p27_b_line_phase_word_source_screen_20260622.md).
On `6000+6000` p27 train/heldout starts, natural V4 words
(`alpha_j`, `beta_j`, adjacent products, and cumulative products) fail the
`1.25x` conditional lift bar and all lose absolute target/source after the
phase split.  This kills natural short phase words as production filters; GPU
phase work is now only a scale/diagnostic test unless it finds a new named
recurrence or sourceable sheet choice.
The GPU-scale version is now pre-registered:
[P27 B-Line Phase GPU Telemetry Handoff](evidence/p27_b_line_phase_gpu_telemetry_handoff_20260622.md)
with manifest
`research/p27/archive/fixtures/p27_b_line_phase_gpu_telemetry_suite_20260622.json`.
It asks for bounded `x16blinephaseprobe` telemetry emitting
`alpha_j,beta_j,alpha_j*beta_j` against actual selected bits with raw-source
denominators.  Promotion requires heldout source-normalized recurrence or a
named Kummer/divisor hypothesis; matching the small CPU half-loss screen is a
kill.
The extension-field denominator audit is also negative:
[P27 B-Line Gamma Extension Count](evidence/p27_b_line_gamma_extension_count_20260622.md).
The new finite-field engine replays `q=607` exactly against the earlier
prime-field point-count probe, then counts `GF(7^3)`, `GF(7^4)`, `GF(7^5)`,
`GF(23^2)`, and `GF(23^3)`.  In every tested field,
`selector_gamma_points = materialized_x6_points`, and the larger odd
extensions have near-half selector rates (`0.5169` for `GF(7^5)`, `0.5207`
for `GF(23^3)`).  This says `gamma^2=U+2` is coupled to the ordinary
materialized `x6` denominator, not a cheaper source stratum.  Continue with
offline Kummer/divisor extraction only; do not run gamma bucket production.
The reduced-cover CAS staging now has a better attack order:
[P27 B-Line Reduced-Cover Charted Magma Staging](evidence/p27_b_line_reduced_cover_charted_magma_20260622.md).
Online q7 product saturation fails first at `Saturation(J,X)`.  Adding an
explicit chart variable `X*iX=1` makes the no-R reduced cover saturate as a
dimension-1 scheme with 6 basis equations; the full compactD_R model is
dimension 1 before remaining saturation; and the fully localized full model is
dimension 1 with 12 equations and no saturation stage.  This is now the
concrete offline Magma/Sage object for the B-line moonshot: normalize the
localized complete intersection, then compute compactD/gamma branch classes.
Follow-up invariant probes show the web endpoint cannot compute even
degree/reducedness/irreducibility on that localized chart, so these invariants
must also be part of the offline CAS ask.
The layer-count follow-up gives a sharper simplification:
[P27 B-Line Localized Cover Layer Count](evidence/p27_b_line_localized_cover_layer_count_20260622.md).
Across `607`, `7^3`, `7^4`, `7^5`, `7^6`, `23^2`, and `23^3`, the probe finds
zero mismatches for `chi(compactD_R_rhs / beta_rhs)=chi(d_next)`.  Since the
reduced `U_next` equation makes `d_next` square, compactD_R is a twinned beta
layer on the reduced cover, not a fresh first CAS layer.
[P27 B-Line CompactD/Beta/Dnext Squareclass](evidence/p27_b_line_compact_beta_dnext_squareclass_20260622.md)
then verifies the corresponding Magma function-field `IsSquare` check over
`GF(7)` and `GF(23)`: `compactD_R_rhs/(beta^2*d_next)` is square with
`root^2` checked in both fields.  The B-line normalization target is now the
no-R reduced cover; the remaining squareclass task is lifting this witness
beyond the q7/q23 smoke if CAS resources permit.
The no-R reduced cover is also no longer a naive low-genus hope:
[P27 B-Line No-R Genus Pressure](evidence/p27_b_line_noR_genus_pressure_20260622.md).
A one-component Hasse-Weil pressure read of the same layer counts violates
genus `<= 1` in `5/7` tested fields and reaches `g >= 11` under that reading.
If the cover is reducible or field-of-definition sensitive, that is the next
structure to compute.  The live CAS ask is components, quotients, and Prym
decomposition of the no-R chart before compactD_R/gamma are added.
That ask is now packaged as an executable packet:
[P27 No-R Quotient/Prym Test Packet](evidence/p27_noR_quotient_prym_test_packet_20260622.md).
Promote only a direct source map, a low-genus quotient carrying the selected
class, or an f3/f4 coupling; kill constant-factor filters and GPU prechecks
that pay a fresh classification toll.
The extension behavior now has a sharper routing test:
[P27 B-Line No-R Closed-Point Pressure](evidence/p27_b_line_noR_closed_point_pressure_20260622.md).
Over both base `7` and base `23`, there are no degree-1 affine closed points
but there are nonzero closed points in coprime degrees `2` and `3`.  This
requires the CAS pass to compare degree-2 and degree-3 base changes and compute
Frobenius component permutation/gamma descent, not just one small-field genus.
The fiber-level localization is now recorded too:
[P27 B-Line No-R Frobenius Fiber Profile](evidence/p27_b_line_noR_frobenius_fiber_20260622.md).
Degree-3 activity sits over degree-3 `B` orbits in both base families, while
quadratic activity can occur by fiber splitting over base-field `B` values.
So the CAS pass must separate B-orbit degree from fiber-extension degree.
The coordinate-degree microscope sharpens this split:
[P27 B-Line No-R Coordinate Degree Profile](evidence/p27_b_line_noR_coordinate_degree_20260622.md).
Cubic activity is a `B`-orbit phenomenon; quadratic activity includes fixed-`B`
fiber extensions, with a clean `GF(7^2)` case where only `W` or `T` leaves the
base field.  The next no-R CAS run should split into cubic B-orbit and
quadratic fixed-B fiber subtests.
The B-orbit invariant screen now closes the visible shortcut:
[P27 B-Line No-R B-Orbit Invariant Screen](evidence/p27_b_line_noR_borbit_invariant_screen_20260622.md).
Active degree-2 and degree-3 B-orbits have square `Norm(B)` and stable
Frobenius signatures, so this is real component/support structure.  But
`Norm(B)` is not a gamma selector: degree-2 orbits are mostly or exactly
half/half, and the one exact cubic linear law in `GF(7^3)` fails at
`GF(23^3)`.  Keep B-orbit as a quotient/Prym extraction target, not as a GPU
bucket or trace/norm character sampler.
The quadratic split has already killed one tempting branch:
[P27 B-Line No-R Quadratic Subcover Classifier](evidence/p27_b_line_noR_quadratic_subcover_classifier_20260622.md).
Across `q = 7, 23, 71, 103, 167`, the `W/T`-only fixed-`B` class is always an
8-point `gamma=0` branch.  Keep only `beta_U_fixedB`, `hidden_mixed_fixedB`,
and B-orbit quotient/component tests as active no-R CAS targets.
The fixed-`B` character screen gives one support law:
[P27 B-Line No-R Fixed-B Character Screen](evidence/p27_b_line_noR_fixedB_character_screen_20260622.md).
`beta_U_fixedB` support is exactly `chi(B)=+1` on the tested fixed-`B` domain,
but its gamma polarity is not stable; `hidden_mixed` small-field `B +/- 2`
patterns fail at `q=167`.  This is a CAS support gate, not a GPU sampler.
The beta_U class now has a named norm target:
[P27 B-Line No-R Beta_U Norm Descent](evidence/p27_b_line_noR_betaU_norm_descent_20260622.md).
Across `q = 23, 71, 103, 167, 199, 263`, gamma descends as
`chi_base(Norm(Unext+2))`, is uniform per active base `B`, and matches the
`16` versus `32` beta_U fiber-size split.  The next beta_U CAS test is divisor
extraction for this norm class on the `chi(B)=+1` support.
The norm map profile is sharper:
[P27 B-Line No-R Beta_U Norm-Fiber Profile](evidence/p27_b_line_noR_betaU_norm_fiber_profile_20260622.md).
In `23^2,71^2,103^2,167^2,199^2,263^2,311^2`, `gamma=+1` is exactly the
low-support side of the norm map: each active `B` has `1` or `8` distinct
`Norm(Unext+2)` values.  `gamma=-1` has `9`, `12`, `14`, or `16`.  This is a
real branch/ramification target for CAS, but not a production sampler because
the support count is obtained only after enumerating the beta_U fiber.
The cheap visible precursor is now replayed and killed:
[P27 B-Line No-R Beta_U B-Character Replay](evidence/p27_b_line_noR_betaU_b_character_replay_20260622.md).
In q199/q263/q311, beta_U support is still exactly `chi(B)=+1`, but the
`gamma=+1` / low-norm-support side is not any named atom, linear factor, or
irreducible quadratic `B` character.  So the norm profile is CAS
branch/ramification data, not a GPU B-bucket.
The two-gate quotient is now killed too:
[P27 B-Line No-R Beta_U Norm/F4 Descent](evidence/p27_b_line_noR_betaU_norm_f4_descent_20260622.md).
After beta_U `gamma=+1`, `f4` remains mixed on `B`, on
`N=Norm(Unext+2)`, and on the joint quotient `(B,N)` in
`71^2,167^2,199^2,263^2,311^2`.  Thus beta_U is a clean f3/materialization
class and norm-map branch target, but not a two-gate sampler.
The obvious plane-curve shortcut is now screened:
[P27 B-Line No-R Beta_U Norm Relation Screen](evidence/p27_b_line_noR_betaU_norm_relation_20260622.md).
`(B, Norm(Unext+2))` has no stable extra bidegree relation through `B12_N16`;
the lone `q=199` signal dies at `q=263` and `q=311`.  Keep beta_U as a
divisor/Kummer extraction target, not a low-degree plane-curve sampler.
The beta_U next-gate check draws the first hard boundary:
[P27 B-Line No-R Beta_U Next-Gate Probe](evidence/p27_b_line_noR_betaU_next_gate_20260622.md).
On gamma-positive beta_U rows, `Unext=x6+1/x6` materializes cleanly and
`chi(v+2)=chi(x7)` for the next roots, but every active gamma-positive `B`
row has both f4 signs.  Thus beta_U is a clean f3/materialization Kummer
class, not a direct two-gate sampler.  Compare f4 only after normalization;
do not send beta_U gamma-positive rows to GPU production.
The pair-level f4 check sharpens that boundary:
[P27 B-Line No-R Beta_U F4 Pair Probe](evidence/p27_b_line_noR_betaU_f4_pair_20260622.md).
For each x6, the ordinary halving norm
`x7_plus*x7_minus=-4*(A*x6+1)` holds exactly, explaining same-sign versus
mixed x7 pairs.  But same-plus versus same-minus is still not selected, and
reciprocal x6 pair products are not stable.  Carry `A*x6+1` into CAS as
orientation data; do not promote x6-pair buckets.
The visible same-sign selector screen is also negative:
[P27 B-Line No-R Beta_U Same-Sign Selector Screen](evidence/p27_b_line_noR_betaU_same_sign_selector_20260622.md).
After restricting to same-sign x7 pairs, natural x6-level atoms and products
through weight `3` do not select same-plus versus same-minus.  Best labels are
weak and field-dependent; `359^2` only reaches `276/456`.  This closes the
visible beta_U f4-product route absent a named new coordinate.
The fixed-`B` comparison now explains why beta_U remains first in that queue:
[P27 B-Line No-R Fixed-B Norm Comparison](evidence/p27_b_line_noR_fixedB_norm_comparison_20260622.md).
Across `q = 23, 71, 103, 167, 199, 263, 311`, both beta_U and hidden_mixed
have zero norm-descent mismatches and zero per-`B` sign conflicts.  But
hidden_mixed's visible fiber split is `chi(B)` (`32` points for square `B`,
`64` for nonsquare `B`), while beta_U's `16/32` split is controlled by
`gamma` itself.  So hidden_mixed stays as a second-pass Kummer comparison; the
first CAS extraction target is still beta_U `Norm(Unext+2)` on
`chi(B)=+1` support.
The square-`B` relation is now explicit:
[P27 B-Line No-R Fixed-B Norm Relation](evidence/p27_b_line_noR_fixedB_norm_relation_20260622.md).
On the common square-`B` support, `gamma_hidden = gamma_beta` in every tested
quadratic field.  This demotes hidden_mixed as an independent first-sign
source; keep it as related component/Prym data for the beta_U class.
The hidden_mixed next-gate check is also negative:
[P27 B-Line No-R Hidden_Mixed Next-Gate Probe](evidence/p27_b_line_noR_hidden_mixed_next_gate_20260622.md).
Gamma-positive nonsquare-`B` hidden_mixed rows do not materialize to x6.
Gamma-positive square-`B` rows materialize, but every active `B` row has mixed
f4.  This kills hidden_mixed gamma=+1 as a continuation sampler; keep it only
as second-pass normalized Kummer/Prym comparison data.
The B-line visible two-gate quartic shortcut is closed as well:
[P27 B-Line Gate4-Prefix Quartic q1847 Screen](evidence/p27_b_line_gate4_prefix_quartic_q1847_screen_20260622.md).
It scans `6,300,872,423` q1847 coefficient triples for
`gate4_prefix_on_legalB` and finds zero exact quartics.  Together with the
q1847 B/K d3 quartic kills, this pushes the B-line lane fully back to
normalized Kummer/divisor class extraction.
The direct sign-word coupling telemetry now agrees:
[P27 Conic Sign-Word Coupling Probe](evidence/p27_conic_signword_coupling_20260622.md).
On `4000 + 4000` p27 train/heldout unique `(A,x5)` rows, the all-plus conic
prefix thins like independent half-gates through the meaningful range; scaled
half-loss stays near `1` until tiny tails dominate.  Exact q1607/q1847/q2087
again show local all-plus plateaus, but their stopping gates disagree.  This
kills GPU sign-word bucket hunting from short conic words alone; GPU
recurrence telemetry is now only a larger-scale confirmation unless a
legal-pullback sampler or quotient appears.
The first B-enhanced legal-pullback relation screen gives a useful staging
surface:
[P27 Conic-Pair B/K-Enhanced Pullback Screen](evidence/p27_conic_pair_b_enhanced_pullback_20260622.md).
Raw `(B,R)`, `(B,L)`, `(K,R)`, `(K,L)`, and `(B,R,L)` systems remain
full-rank, but `(B,s,m)` has the stable equation
`m^2*(B^2+s^2-4)=4*s^2*(s^2-4)`, with `s=R+1/R` and `m=L+a^2/L`.
Together with the tautology `B^2+c^2=4`, this is a cleaner CAS staging
coordinate for the legal pullback.  It still does not select the sparse legal
B-domain, so it is not a GPU sampler by itself.
The source-sheet follow-up is negative:
[P27 Conic-Pair Source-Sheet Relation Screen](evidence/p27_conic_pair_source_sheet_relation_20260622.md).
Joining the staged conic preimages to actual residual source sheets `X,W,T`
does not reveal a cheap second relation.  `(X,R,L)`, `(W,s,m)`, and `(T,s,m)`
are full-rank through degree `12`, pair projections such as `(X,s)` and
`(X,R)` are full-rank through degree `16`, and `(X,s,m)` has no relation
through degree `8`.  The low-degree relations that do appear are inherited
source/staging equations (`W^2=X^3-X`, the T-cover, `B(X)`, and `(B,s,m)`).
So the conic route remains an offline normalization/Kummer-class problem, not
a direct source-sheet GPU sampler.
The incidence follow-up prices that surface:
[P27 BSM Surface Incidence Probe](evidence/p27_bsm_surface_incidence_20260622.md).
Over q1607/q1847/q2087 the BSM surface has about `q^2` points and hits
canonical d3-plus `(B,A,x)` rows at `constant/q` density
(`rate*q` about `0.38..0.78`).  It captures all canonical d3-plus target rows
and no canonical d3-minus rows, so it is a good staged model, but it does not
solve the legal B-domain denominator.
The legal-B-restricted relation follow-up is also negative:
[P27 BSM Legal-Restricted Relation Screen](evidence/p27_bsm_legal_restricted_relations_20260622.md).
In q1607/q1847/q2087, the target rows have no extra low-degree relation beyond
the legal-B-restricted BSM surface in `(B,s)`, `(B,m)`, or `(s,m)` through
degree `12`.  In `(B,s,m)`, degree `4` gives exactly the inherited BSM
equation on both the full legal surface and the target subset
(`target_minus_legal_extra=0`).  This kills the legal-B BSM surface as a
GPU-promotable bucket/source until a true legal-B cover or next Kummer selector
is added.
The next-selector version is now negative too:
[P27 BSM Next-Selector Relation Screen](evidence/p27_bsm_next_selector_relation_20260622.md).
It asks whether `d4+` after `d3+` gets a new low-degree relation on the same
staged surface.  Across q1607/q1847/q2087, `(B,s)`, `(B,m)`, and `(s,m)` have
no `d4+` extra relation through degree `12`, and `(B,s,m)` degree `4` is again
only the inherited BSM equation shared by legal, `d3+`, `d4+`, and `d4-`.
So BSM remains CAS staging, not a visible two-gate coupling.
The BSM surface is now identified with the ordinary halving cover:
[P27 BSM Halving-Cover Identity](evidence/p27_bsm_halving_cover_identity_20260622.md).
With `A=B^2-2`, `x=m^2/16`, and `z=s^2`, the BSM equation becomes
`z^2 - 4*(x+1)*z - 4*x*(B^2-4)=0`, whose discriminant is
`16*(x^2+A*x+1)`.  Every nondegenerate BSM point has `x` square and
halving-discriminant square; canonical d3-plus rows have exactly eight BSM
lifts, while d3-minus rows have none.  This demotes BSM from a peer moonshot
lane to a coordinate view of the known one-step selected halving cover.

The first raw quotient screen is negative:
[P27 Conic-Pair Low-Degree Relation Screen](evidence/p27_conic_pair_lowdegree_relation_20260621.md).
For q1607/q1847/q2087, the legal d3-plus sampler preimages in `(R,L)` have no
nonzero total-degree relation through degree `20`.  This kills the easiest
"low-degree plane curve in raw `(R,L)`" source, and pushes the quotient search
to the repeated Kummer tower variables instead.

The obvious invariant-coordinate quotient screen is also negative:
[P27 Conic-Pair Invariant Relation Screen](evidence/p27_conic_pair_invariant_relation_20260621.md).
The same legal d3-plus preimages were tested in target coordinates `(A,x)`,
signed conic coordinates `(c,r)`, and symmetric pairs such as
`(R+1/R,L+a^2/L)`, `((R-1/R)^2,L+a^2/L)`, and
`(R+1/R,(L+a)(L-a))`.  Through degree `20`, q1847/q2087 have no extra nullity
in any tested pair system, and the only q1607 degree-20 artifact does not
repeat.  This spends the cheap invariant plane-curve idea; the remaining live
route must retain selector roots `Z_j` or use staged pullback/normalization.

The first selector-root layer has now been screened too:
[P27 Conic-Pair Kummer-Z Relation Screen](evidence/p27_conic_pair_kummer_z_relation_20260621.md).
After adjoining `Z^2=-(L+a)(L-a)cR`, all tested simple pairs involving `Z` are
full-rank through degree `20` except `(A,Z)`.  Extracting `(A,Z)` shows the
exception is only a univariate `A`-projection polynomial, with the next
relation equal to that polynomial times `Z`; the A-projection grows at
constant-density small-field scale.  This kills the first-Z-layer simple
pair-quotient hope and pushes the live route to staged normalization/components
or a named Kummer/Hilbert-90 theorem.

The A-projection shortcut is now explicitly killed:
[P27 A-Projection Selected-Prefix Profile](evidence/p27_a_projection_prefix_profile_20260621.md).
On 3,000-row p27 train/heldout samples, unique `A` and unique `(A,x)` shrink in
lockstep through depth 8.  The scaled half-loss stays near `1`, and
`avg_x_per_A` remains exactly `2` at every p27 sampled prefix.  Thus the tower
does not reveal a smaller A-bucket source; the univariate small-field
polynomials are finite A-projection artifacts, not p27 laws.

Extension-field counts give the first staged-geometry substitute:
[P27 Extension-Field Selected-Prefix Counts](evidence/p27_extension_prefix_count_20260621.md).
The trusted residual `E/T`, `compactD=-1`, label-2 map, and selected-prefix
equations were counted over `GF(7^n)` and `GF(23^n)`.  The source is
curve-sized over extension fields, but selected prefixes still reduce unique
`A` and unique `(A,x)` together.  Local Frobenius tails appear, but there is no
stable source collapse that extrapolates to p27 or beats sqrt.

The two-step Kummer shortcut is also killed:
[P27 Conic-Pair Two-Step Kummer Screen](evidence/p27_conic_pair_two_step_kummer_20260621.md).
After adjoining `Z0^2=-(L0+a0)(L0-a0)c*r1`, the next selector
`S1=-(L1+a1)(L1-a1)c*r2`, and when available `Z1^2=S1`, all obvious
selector/root pair systems are full-rank through degree `12` on
q1607/q1847/q2087.  This rules out the simple `(Z0,S1)`, `(Z0,Z1)`,
normalized-root, ratio, and product quotients.  The live conic-chain route is
therefore staged normalization/components or a theorem-level repeated
Kummer/Hilbert-90 identity, not a GPU bucket search in simple two-root
coordinates.

The next cheap bucket generalization is also negative:
[P27 Conic-Pair Two-Step Kummer Trivariate Screen](evidence/p27_conic_pair_two_step_kummer_trivar_20260621.md).
Selector/root triples such as `(A,Z0,S1)`, `(A,Z0,Z1)`,
`(A,Z1/Z0,Z0*Z1)`, normalized-root triples, and `(R_j,Z0,Z1)` are full-rank
through degree `6` on q1607/q1847/q2087.  This spends the obvious
three-coordinate surface search; continuing now needs a staged component
calculation or a theorem-specified coordinate, not larger ad hoc bucket scans.

The K-line now has a cleaner coordinate for that extraction:
[P27 Kummer Belyi Structure Probe](evidence/p27_kummer_belyi_structure_probe_20260621.md).
Symbolically,
`K_num=(X^2-2X-1)^2*(X^2+2X-1)^2` and
`K_den=4X(X-1)(X+1)(X^2+1)^2`, with branch resultant
`K^4*(K^2+4)^4`.  Thus `lambda=-K^2/4` has branch values
`0,1,infinity`.  The cheap visible branch atoms `K`, `K^2+4`, and `K^2` are
all already square on the selected guard-field rows, so they do not explain
`d3/d4` and do not give a sampler.  The useful consequence is only the
normalization: the next Magma/Sage pass should mark these Belyi branch values
when recovering the actual `d3` branch class.

The visible Belyi involutions do not give a further quotient:
[P27 K/S Belyi Involution Audit](evidence/p27_k_belyi_involution_audit_20260621.md).
The tempting shortcut was `K -> 4/K`, equivalently
`Sroot -> +/-2/Sroot`.  It is closed in some small fields but not stable:
for `d3`, q607 has `32/32` present with opposite targets and q1471 has
`49/50` present with same targets, while the promotion fields q1607 and q1847
have `0/49` and `0/63` present.  An online Magma q607/q1607 fixture confirms
the contrast.  So Belyi automorphisms remain normalization data, not a
sqrt-beating sampler or quotient shortcut.

The guard-field rule is now sharper:
[P27 Guard-Field Signature Audit](evidence/p27_guard_field_signature_audit_20260621.md).
Because p27 is `7 mod 16` and `v2(p+1)=3`, K/S orbit and recurrence positives
must promote through fields with `q = 7 mod 16`, not merely `q = 7 mod 8`.
In an audit of 144 primes `q = 7 mod 8` from 607 to 5000, every tested
`q = 7 mod 16` field had `K -> 4/K` absent on selected `d3` and `d4` K rows.
All full or partial `K -> 4/K` closures came from `q = 15 mod 16` fields with
an extra 2-adic layer.  Thus q1471 is useful as a stress checksum, but q1471
positives are no longer promotion evidence for 2-adic-sensitive K/S claims;
future promotion fields should look like q1607, q1847, q2039, and other
`7 mod 16` fields.

The K-line recurrence loophole is now closed for small Lattes maps:
[P27 K-Line Lattes Recurrence Screen](evidence/p27_k_lattes_recurrence_20260621.md).
It tested `d4(K) = +/- d3(x([m]Q))` and
`d4(K) = +/- d3(x([m]Q+(0,0)))` for `m=1..24` on the reduced Kummer line.
In the promotion fields, only identity has full coverage, except for the
already-local q1471 `K -> 4/K` artifact; the scores are raw d4 bias
(`14/28`, `19/28`, `26/45`, `18/25` in q2087).  Nontrivial maps cover at most
`13/28` in q1607, `19/45` in q1847, and `10/25` in q2087.  So a
d4-from-d3 Lattes recurrence is not the
sqrt-beating mechanism; compare d4 only after the actual d3 branch class is
named.

The broader degree-one K-line recurrence screen is negative too:
[P27 K-Line Affine Recurrence Screen](evidence/p27_kline_affine_recurrence_20260621.md).
It tested all maps `K -> a*K+b` and `K -> a/K+b` over p27-signature fields
q1607/q1847/q2039/q2087.  In the non-degenerate promotion fields, the only
full-coverage affine map is identity, scoring as raw d4 bias
(`19/28`, `26/45`, `18/25`), and reciprocal-affine maps cover at most
`6/28`, `7/45`, and `6/25`.  q2039 has full exact identity only because d4 is
constant there.  This kills the sourceable degree-one rational recurrence
loophole; the K-line route now really needs branch-divisor/Kummer-class/genus
extraction.

The first actual reverse-root branch proxy is negative:
[P27 K-Line Reverse-Z Relation Screen](evidence/p27_kline_reverse_z_relation_20260621.md).
Instead of using only the sign bit, it keeps the d3 all-plus source root
`x6=z^2` and screens `(K,z)`, `(Sroot,z)`, `(K,x6)`, `(K,r)`, and normalized
`z +/- 1/z` coordinates.  On q1847/q2087 all systems are full-rank through
degree `20`; q1607 has only non-repeating degree-20 artifacts in lower
multiplicity projections, while `(K,z)` and `(Sroot,z)` stay full-rank.  On a
1,000-row p27 sample, all systems are full-rank through degree `12`.  This
kills the obvious plane-model shortcut for the branch cover.  The surviving
K-line work is now literal normalization / branch divisor / genus extraction
over `P1_K` or `P1_Sroot`.

The reverse-root extension count is now in:
[P27 K-Line Reverse-Z Extension Counts](evidence/p27_kline_reverse_z_extension_count_20260621.md).
It validates against q607 and repeats on q1607/q1847/q2087 plus
`GF(7^n)`/`GF(23^n)`: the actual reverse-root cover has exact constant fibers
`z_rows/unique_K = 64`, `z_rows/unique_S = 32`, and `unique_Ax/unique_A = 4`
on every nonempty guard field.  That is strong evidence that K/S is a real
structured projection, but `unique_K` and `unique_S` still grow at field-size
scale.  So K/Sroot enumeration is not a below-sqrt sampler by itself; the
next useful work is the actual branch/genus/CAS extraction of this
constant-degree cover, not a GPU bucket search on K or Sroot.

The rational fiber profile is even cleaner:
[P27 K-Line Reverse-Z Fiber Profile](evidence/p27_kline_reverse_z_fiber_profile_20260621.md).
On q1607/q1847/q2087, every selected K fiber has `64` z-rows, one selected
`A`, four `(A,x)` values, eight `x6` values, sixteen `z` values, and four
`r=x6+1/x6` values.  Every selected Sroot fiber has exactly half the rows
with the same one-`A` structure.  There are zero anomalous rational fibers in
the promotion fields.  This makes Sroot the cleaner branch-extraction
coordinate, but it also kills the hope that rational K/Sroot fiber anomalies
are the sqrt-beating source.

The K/A graph now has an exact equation and a matching GPU interpretation:
[P27 K/A Map And GPU Quadratic-Gate Update](evidence/p27_kline_a_map_and_gpu_quad_20260622.md).
With `L=K^2`, the first-half source satisfies
`64(A-2)^2(A+2)L^2 + 64(A+2)(A+14)(3A+10)L - (A-2)^4 = 0`,
whose discriminant in `L` is
`256(A+2)(A+6)^2(A^2+60A+132)^2`.  This explains the clean K/S fibers and
shows that Sroot is the natural first-half coordinate.  But the formula
vanishes on both d3-plus and d3-minus d2-plus candidates in p27 train/heldout
and q607/q1607/q1847/q2087, so it is not the missing d3 selector.  The new GPU
quadratic-gate run then checked `7,874,715` gates across gates `3..8` with
zero mismatches, but its recurrence-coordinate domain is only a conditional
half-scope: source-normalized target rate remains flat or slightly lower.
The next sqrt-beating test is therefore a direct legal-pullback/quotient
sampler for this recurrence domain, or a coupling law across many
`chi(r_j^2+c*r_j+1)` signs.
The GPU decision memo records the operational boundary:
[P27 GPU Test Decision After Quadratic Probe](evidence/p27_gpu_test_decision_after_quad_20260622.md).
Use GPU next for bounded recurrence-coupling telemetry or for a direct
legal-pullback sampler once one exists; do not launch a large production run
from the fixed quadratic precheck alone.

The direct base-curve sampler test is negative:
[P27 K/A Base-Curve Sampler Probe](evidence/p27_kline_base_curve_sampler_20260622.md).
Over q1607/q1847/q2087, the explicit base curve has exactly `q` affine
`(K,A)` points and contains every realized legal d2 point, but the realized
legal subset is only `49/1607`, `63/1847`, and `57/2087` respectively.
Low-weight squareclass products of the natural K/A atoms do not identify this
subset; their best nontrivial scores are only about `0.53`.  Thus the base
curve is a good normalization coordinate, not a direct GPU source.  The live
object is still the additional legal cover over the base, especially the d3
reverse-root cover over `P1_Sroot`.
Online Magma now independently validates the base equation and B chart:
[P27 K/A Base-Curve Magma Validation](evidence/p27_ka_base_curve_magma_validation_20260622.md).
In q607, `base_KA=607`, the nondegenerate B chart covers `604` of them, the
only missing points are the expected three B-degeneracies, and equation plus
discriminant checks have zero mismatches.  So the remaining obstruction is the
legal/d3 cover, not the K/A base model.

The B-rationalized follow-up is positive as bounded telemetry, but not as a
production source:
[P27 B-Parameter Base-Curve Sampler Probe](evidence/p27_kline_base_param_sampler_20260622.md).
With `A=B^2-2`, the base branches are
`L=-(B+2)^4/(8B(B-2)^2)` and `L=(B-2)^4/(8B(B+2)^2)`.  Across
q1607/q1847/q2087, every realized legal d2 row and every d3plus row lies in
the same core bucket for `K`, `B+2`, `B-2`, and `L`, with about `8.04x`
all-recall lift.  That is a real constant-factor scope shrink and a good
bounded GPU telemetry target.  It is not sqrt-beating by itself: the bucket is
still field-sized, and the higher-lift partial buckets are not stable enough
to promote without a theorem.

The direct next-gate version of that idea is now negative:
[P27 B-Parameter Next-Gate Probe](evidence/p27_kline_base_param_nextgate_20260622.md).
After conditioning on actual legal `d2` rows, the core B bucket still contains
all rows in p27 train/heldout and q1607/q1847/q2087.  But B/K/A atom products
do not stably predict `d3` or `d4`: the p27 train-best `d3` parity combo drops
below majority on heldout, and the train-best `d4` combo falls from `1.087x`
majority-lift to only `1.015x` on heldout.  So the B route is no longer a GPU
bucket-search route; it is a function-field/CAS cover-extraction route over
the B-rationalized base curve.

The B route now has its first real quotient theorem target:
[P27 B-Source Descent And Branch Support](evidence/p27_b_source_descent_and_branch_20260622.md).
Symbolically, on the residual source
`A+2=(8X^2/(X^2-1)^2)^2`, so `B=8X^2/(X^2-1)^2` is a genus-0 quotient of the
source, not merely a fitted square root.  In p27 train/heldout and
q1607/q1847/q2087, `d3` and `d4` after `d3=+1` descend to `Bplus` with no
mixed groups.  This is positive and narrows the moonshot to a Kummer class on
`P1_B`.  The nearest branch supports are negative: `d2` on the B core and `d3`
on legal B have no rational-linear support of weight `<=4`, and `d3` is not
one irreducible quadratic times `<=2` rational linear factors in any promotion
field.  The structured split degree-4 follow-up is also negative:
[P27 B-Line Two-Quadratic Support Screen](evidence/p27_b_line_two_quadratic_support_20260622.md).
It enumerates all monic irreducible quadratic character vectors in
q1607/q1847/q2087 and finds no pair whose product matches `d3(B)`.  The next
serious test is Magma/Sage divisor extraction for the descended `d3(B)` class,
including possible irreducible quartic, cubic-plus-linear, or higher
non-visible support, not another B-bucket scan.
That extraction now has a concrete packet:
[P27 B-Line Kummer Extraction Packet](evidence/p27_b_line_kummer_extraction_packet_20260622.md).
It packages the quotient `B=8X^2/(X^2-1)^2`, the branch resultant
`16384*B^3*(B+2)^2`, the source equations for the d3 all-plus cover over
`P1_B`, and a q1607 Magma sanity fixture.  The next accepted B-line result is
a normalization/genus/branch-divisor computation over q1607/q1847/q2087, not
another visible-factor or bucket screen.
The compact row-level handoff is now also frozen:
[P27 B-Line Kummer Fixture Packet](evidence/p27_b_line_kummer_fixture_packet_20260622.md).
It records the conditional classes `f3(B), f4(B), f5(B), f6(B)` over
q1607/q1847/q2087.  This sharpens the CAS ask to `f3` first, then `f4/f3`.
The later `f5/f6` rows are already small-field tail dominated and should not
be treated as recurrence evidence without larger heldout support.
The legal-domain split degree-4 screen is now negative too:
[P27 B-Line Legal-Domain Two-Quadratic Support Screen](evidence/p27_b_line_legal_two_quadratic_support_20260622.md).
Inside the core B bucket, the legal B subset is not a product of two
irreducible quadratic branch factors in q1607/q1847/q2087.  This kills the
nearest low-degree split-divisor sampler for the `core B -> legal B` step.
The monic cubic genus-1 route is also closed:
[P27 B-Line Cubic Support Screen](evidence/p27_b_line_cubic_support_20260622.md).
The exact bitset solver tests every cubic `B^3+aB^2+bB+c`, with global
polarity allowed.  In q1607/q1847/q2087, both the legal B-domain and the
decisive `d3(B)` selector have `exact_cubics = 0`.  Local d4 cubics appear in
q1607/q2087 on only 28/25 rows, but q1847 has 45 d4 rows and zero exact
cubics, so those are interpolation artifacts.  This kills the visible cubic
genus-1 B-line source; the remaining low-genus B cases must come from actual
class extraction, not coefficient guessing.
The stronger combined-prefix cubic shortcut is now closed as well:
[P27 B-Line Prefix Cubic Support Screen](evidence/p27_b_line_prefix_cubic_support_20260622.md).
This tests whether a single genus-1 cubic on `P1_B` selects the all-plus prefix
directly, even if the individual `d3(B)` and `d4(B)` characters look generic.
For the combined gate4 prefix, q1607/q1847/q2087 all have `exact_cubics = 0`.
For gate5, q1607 and q2087 keep their small-field plateau subsets but still
have zero exact cubics; q1847 is one-sided with no plus tail.  So the B-line
plateaus are not visible cubic source laws.
The visible Belyi orbit shortcut is also negative:
[P27 B-Line Belyi-Orbit Screen](evidence/p27_b_line_belyi_orbit_20260622.md).
The six Möbius transforms preserving `{0,-2,infinity}` send every non-identity
image of a core B value outside the core bucket in q1607/q1847/q2087.  Thus the
B-line branch-set symmetry gives no orbit sampler or GPU reason.
The broader degree-one rational recurrence shortcut is negative too:
[P27 B-Line PGL2 Recurrence Screen](evidence/p27_b_line_pgl2_recurrence_screen_20260622.md).
It tests every full-coverage map `B -> (aB+b)/(cB+d)` for
`d4(B) = +/- d3(phi(B))` in q1607/q1847/q2087.  All three fields have zero
exact recurrences; the best full-coverage maps are identity maps scoring raw
d4 majority bias (`19/28`, `26/45`, `18/25`).  So the B-line coupling target
is extracted Kummer classes or a theorem-shaped higher correspondence, not
degree-one rational B maps.
The nearest theorem-shaped higher correspondence is now negative as well:
[P27 B-Line Power-Map Recurrence Screen](evidence/p27_b_line_power_recurrence_screen_20260622.md).
It tests the hidden-`X` maps induced by `X -> X^m` for `m=2..6`, with all
Belyi branch symmetries on both sides.  No exact `d3 -> d4` or reverse
recurrence appears in q1607/q1847/q2087, and the best maps cover only
`7/28`, `12/45`, and `6/25` of the forward domains.  This closes the natural
hidden-`X` doubling/tripling shortcut and leaves actual B-line
Kummer/divisor-class extraction as the live route.
The adjacent monomial Belyi family is also negative:
[P27 B-Line Monomial Belyi Recurrence Screen](evidence/p27_b_line_monomial_belyi_recurrence_screen_20260622.md).
With `u=-B/2`, it tests `u -> u^m` for `m=2..12`, conjugated by the branch-S3
symmetries.  Again there is no exact forward or reverse `d3/d4` recurrence in
q1607/q1847/q2087; best forward coverages are only `5/28`, `10/45`, and
`4/25`.  This closes the canonical B-line branch dynamics short of actual
Kummer/divisor-class extraction.

The B-line target is now stronger than a one-bit descent:
[P27 B-Line Extension Counts And Deep Descent](evidence/p27_b_line_extension_and_deep_descent_20260622.md).
Extension counts over `GF(7^n)` and `GF(23^n)` show that legal B values stay
inside the core B bucket with no misses, and that `d3`/`d4` remain unmixed on
B.  The legal B-domain is still field-sized, about `0.03N` in the informative
odd extensions, so counts alone do not give a below-sqrt sampler.  But deep
p27 train/heldout tests show no mixed B groups through `d12`: the original
`Bplus` value determines every active selected gate bit tested.  This changes
the live B moonshot from "find d3(B)" to "extract the B-line Kummer sequence
`f3(B), f4(B), ...` and test whether those classes recur or couple."  That is
the first B-lane mechanism that could genuinely amortize multiple half-losses.
The larger p27 source-normalized check is now in:
[P27 B-Line 60K Prefix Scaling](evidence/p27_b_line_prefix_scaling_60k_20260622.md).
On `60000 + 60000` p27 train/heldout rows, there are again zero mixed B groups
through `d18`, but scaled half-loss remains near `1` through meaningful counts
(`d3..d12`).  Train's `d13/d14` bump is only `18/9` rows and does not transfer
to heldout; heldout's larger `d15+` values are single-digit tails.  So B is a
real Kummer-sequence surface, not a count-only sampler or B-bucket GPU reason.
That GPU follow-up is now bounded and pre-registered:
[P27 B-Line Deep-Prefix GPU Telemetry Handoff](evidence/p27_b_line_deep_prefix_gpu_telemetry_handoff_20260622.md)
with manifest
`research/p27/archive/fixtures/p27_b_line_deep_prefix_gpu_telemetry_suite_20260622.json`.
It asks the GPU to emit `Bplus`, selected bits `d3..dN`, mixed-B examples, and
source-normalized prefix counts from the same p27 stream.  Promotion requires
large-scale no-mixed-B persistence plus either a source-normalized recurrence
or a named Kummer/divisor hypothesis.  It is not a B-bucket production hunt.
The B-line prefix-density screen has also been strengthened:
[P27 B-Line Prefix Profile](evidence/p27_b_line_prefix_profile_20260622.md).
Small extension fields show field-dependent late plateaus, but a larger
`6000 + 6000` p27 train/heldout B-group sample has no mixed groups and thins
close to independent half-loss through meaningful depths.  This keeps B as a
Kummer-extraction surface, not as a count-only sampler.
The first Magma staging smoke sets the extraction boundary:
[P27 B-Line Magma Staging Smoke](evidence/p27_b_line_magma_staging_20260622.md).
Over q7, the eta=`+1` legal B-cover saturation succeeds as a dimension-1
scheme with `93` basis polynomials.  But adding point/curve/component calls to
that legal cover returns a web-calculator `504`, and the full legal+d3
reverse-source fixture also returns `504`.  So the B-line CAS target is
concrete, but online Magma is only a syntax/saturation sanity tool here.  The
next real extraction needs offline Magma/Sage or a specialized elimination over
`Bline`.
The first specialized elimination proxy is negative:
[P27 B-Line Reverse-Z Relation Screen](evidence/p27_b_line_reverse_z_relation_20260622.md).
It keeps the actual d3 all-plus root `z` with `x6=z^2` and tests B-line plane
models in `(B,z)`, `(B,x6)`, `(B,r)`, `z+/-1/z`, Belyi-normalized B
coordinates, and branch-normalized `z` coordinates.  The actual `(B,z)` cover
and branch-normalized systems are full-rank through total degree `20` in
q1607/q1847/q2087, and a 1,000-row p27 sample is full-rank through degree
`12`.  Only q1607 has degree-20 artifacts in compressed `z+/-1/z`
projections, and they do not repeat.  This kills the nearest B-line
reverse-root plane-model sampler; the surviving B route remains actual
normalization / branch-divisor / genus extraction over `P1_B`.

The first Belyi-normalized source family is now killed:
[P27 Lambda Branch-Divisor Screen](evidence/p27_lambda_branch_divisor_screen_20260621.md).
It tested `z^2=f(lambda)` with `deg_lambda(f)<=4`, where
`lambda=-K^2/4` and the branch divisor splits over each guard field into
rational linear and irreducible quadratic factors.  For `d3` there are no
exact divisors over `q=1471,1607,1847`; for `d4`, degree-3 fits appear in
q1471/q1607 but disappear at q1847.  This rules out the nearest genus `<=1`
lambda-line sampler for the decisive next bit.  The surviving K/lambda route
is not coefficient-bound widening; it is actual branch-class/genus extraction,
including possible irreducible cubic/quartic support or a higher-degree class.

The remaining visible low-genus B-line d3 family has now had its decisive
q1847 exact screen:
[P27 B-Line Quartic GPU Test Card](evidence/p27_b_line_quartic_gpu_test_card_20260622.md).
The full q1847 monic quartic support test
`chi(B^4+aB^3+bB^2+cB+d)` for `d3_on_legalB` found zero exact quartics:
[P27 Full Quartic q1847 D3 Screen](evidence/p27_full_quartic_q1847_d3_screen_20260622.md).
Since q1847 had expected random exact count about `2.52e-6`, this sharply
downgrades the visible genus-1 B-line support route.  q2087/q1607 closure or
gate4-prefix quartics are now optional closure tests; the live B-line work is
normalization / branch-divisor / Kummer-class extraction, not another visible
d3 quartic hunt.
The visible Belyi-involution subfamilies are now dead:
[P27 B-Line Belyi-Involution Quartic Screen](evidence/p27_b_line_involution_quartic_screen_20260622.md).
The five small families attached to the three order-2 symmetries of
`{0,-2,infinity}` have zero exact hits over q1607/q1847/q2087 for both
`d3_on_legalB` and `gate4_prefix_on_legalB`.  The completed full q1847
B-line screen was therefore the right decisive test, not a branch-symmetry
proxy.

There is also a rational-source obstruction to treating `lambda` as the next
quotient:
[P27 Lambda Rational-Quotient Obstruction](evidence/p27_lambda_rational_quotient_obstruction_20260621.md).
On `E': V^2=U^3+4U`,
`K=x([2]P)=((U^2-4)/(2V))^2`, so every nondegenerate rational doubled `K` is a
square.  In the p27 sign regime `chi(-1)=-1`, hence `-K` is outside the same
rational doubled stratum.  Across fifteen `q=7 mod 8` guard fields, the full
doubled image has no nonzero `K/-K` paired values, and selected `d3/d4` rows
all have `chi(K)=+1` with no `-K` partner.  Therefore `lambda=-K^2/4` is a
Belyi bookkeeping coordinate, not a standalone rational sampler.  Any
sqrt-beating source must lift back to the K-level square stratum.

That rational lift has now been tested:
[P27 S-Root Branch-Divisor Screen](evidence/p27_sroot_branch_divisor_screen_20260621.md).
On `E'`, write `S=(U^2-4)/(2V)`, so `K=S^2`.  This keeps the rational
K-square stratum and restores the `S/-S` orientation that lambda quotients
away.  The guard-field data has paired `S/-S` rows throughout, but there are no
exact split branch divisors `z^2=f(S)` with `deg_S(f)<=4` for `d3` over
`q=1471,1607,1847`; unlike K/lambda, `d4` also has no small-field local fits
in this S family.  This kills the nearest rational square-root line sampler.
The remaining K-square route is branch-class/genus extraction over K or S, not
another low-degree split-divisor scan.

The visible S-ramification is now priced too:
[P27 S-Root Belyi Structure Probe](evidence/p27_sroot_belyi_structure_probe_20260621.md).
The S-map branch resultant is
`S^8*(S^2-2S+2)^4*(S^2+2S+2)^4`.  On selected rows, the quadratic branch atoms
`S^2-2S+2`, `S^2+2S+2`, and `S^2` are already square, while `chi(S)` flips on
every `S/-S` pair and the `d3/d4` target is constant on each pair.  So visible
S branch values and `chi(S)` are killed as selectors.  A future extraction
should use these branch values as marked points, but the source class, if it
exists, is non-visible.

The S parity reduction is now explicit:
[P27 S-Root Parity Reduction](evidence/p27_sroot_parity_reduction_20260621.md).
The `d3/d4` targets are constant on every `S/-S` pair, while `chi(S)` flips
because `chi(-1)=-1`.  Thus global even low-degree S classes are just
K-classes already covered by the K-line screens, and global odd S classes
cannot match the pair-even target.  This kills broad visible S coefficient
scans as a useful next step.  The remaining test is function-field extraction
of the actual non-visible branch class and its decomposition under `S -> -S`.

That extraction is now packaged as a K/S CAS packet:
[P27 K/S Branch-Extraction Packet](evidence/p27_ks_branch_extraction_packet_20260621.md).
It combines the `K=x([2]P)` map, the rational square root
`Sroot=(U^2-4)/(2V)`, the reverse-source equations, and the label-2
order-4/H90 identities in one Magma/Sage-ready handoff.  Its symbolic checks
recover `Sroot^2=K`, the branch resultants
`Sroot^8*(Sroot^2-2Sroot+2)^4*(Sroot^2+2Sroot+2)^4` and
`K^4*(K^2+4)^4`, and the H90 identities with zero remainders.  The attached
online-Magma sanity fixture has now passed over `q=1471`; after the
guard-field signature audit this is only an algebraic checksum, not promotion
evidence.  The real next test is
normalization of the `d3` source over `P^1_K` and
`P^1_Sroot`.  Promote for genus `<=1`, a sourceable recurrence, or a cheap
character/source sampler; kill for high/generic branch degree or an unrelated
fresh `d4` half-cover.

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

The first visible elliptic divisor follow-up is also negative:
[P27 Trace/Norm Elliptic Line-Divisor Screen](evidence/p27_trace_norm_elliptic_line_divisor_screen_20260622.md).
Vertical divisors `u-c` and affine divisors `v+m*u+c` with `|m|,|c| <= 4`
produce no exact selector; the best heldout target lift is only `1.011x`.
So there is no small `L(3O)` line-divisor bucket worth sending to GPU.

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
The visible automorphism quotient follow-up is now negative:
[P27 Trace/Norm Automorphism Quotient Obstruction](evidence/p27_trace_norm_automorphism_quotient_obstruction_20260622.md).
On four heldout seeds, `T_line` is invariant under `t -> -1/t` on `65120`
comparable rows, while `pref` and `h*vq` both have the exact `-chi(a)`
boundary.  But under `t -> 1/t` and `t -> -t`, `T_line` is mixed
`32568/32552` with no exact reference sign.  Thus the remaining identity must
live on the `C/E` quotient; it does not descend to a smaller visible
automorphism quotient.

The first visible divisor family on that quotient is now bounded negative:
[P27 Trace/Norm Elliptic Line-Divisor Screen](evidence/p27_trace_norm_elliptic_line_divisor_screen_20260622.md).
It checked `u-c` and `v+m*u+c` for `|m|,|c| <= 4`; exact counts were zero
for train and heldout, with heldout target lift at only `1.011x`.

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

Status: completed for the first GPU matrix.  Baseline, domain, ecover, fixed
`d2/d3/d4` prefixes, and ecover-prefix variants all ran as same-seed GPU
scope probes.  Fixed prefixes are exact continuation filters but not a raw
source-space cut in the measured depth-24 matrix.  The trace/norm `D_plus`
gate is the only promoted search-space narrowing lead: it captures all
observed depth-20 through depth-30 survivors in the 1B+1B raw-y confirmation,
but still needs a direct sampler or cheaper pretest before it is a production
throughput win.

Equivalent x-square request: report prefix filters as `x_4 square`,
`x_4,x_5 square`, and `x_4,x_5,x_6 square`.  For nonsplit rows this is the same
gate sequence and is the cleaner 2-descent language.

### Card 4b: B-Line Prefix Profile

The B-line quotient is exact structure but not a direct source win:
[P27 B-Line Prefix Profile](evidence/p27_b_line_prefix_profile_20260622.md),
updated by
[P27 B-Line 60K Prefix Scaling](evidence/p27_b_line_prefix_scaling_60k_20260622.md).

The original `Bplus` value still determines the selected gate sequence in
p27 samples, with no mixed B groups through `d18` in the latest
`60000 + 60000` train/heldout check.  But the all-plus population thins close
to one independent half-loss per gate through the meaningful range:

```text
p27 train gate3..gate12 scaled_half_loss:
  0.9978, 0.9980, 1.0027, 0.9899, 1.0176,
  1.0453, 0.9472, 0.9984, 1.0581, 0.9557

p27 heldout gate3..gate12 scaled_half_loss:
  1.0043, 1.0065, 1.0187, 1.0171, 1.0176,
  1.0453, 0.9856, 1.0240, 0.9387, 1.0581
```

Small exact guard fields sometimes show late all-plus plateaus, but the
collapse gate varies by field.  Treat those as finite-field artifacts unless a
named divisor/Kummer relation explains them and survives p27 rows.

Status: B-line remains a clean Kummer-class extraction surface; do not run a
large GPU production search based only on Bplus buckets.

Extension-field update:
[P27 B-Line Prefix Extension Ladder](evidence/p27_b_line_prefix_extension_ladder_20260622.md)
pushes that verdict through `GF(7^n)`, `GF(23^n)`, and `GF(103^n)`.  Legal B
continues to have zero core-bucket misses, but all-plus plateaus stop at
field-dependent gates: `GF(7^6)` dies at `d7`, `GF(23^3)` at `d9`, and
`GF(103^2)` at `d6`.  This kills B-prefix counts alone as a transferable
below-sqrt sampler; the live B-line work is still Kummer-sequence extraction
for `f3(B), f4(B), ...`.

Subfield audit:
[P27 B-Line Frobenius Plateau Audit](evidence/p27_b_line_frobenius_plateau_audit_20260622.md)
then checks the obvious explanation for those plateaus.  In `GF(7^5)`,
`GF(7^6)`, `GF(23^3)`, and `GF(103^2)`, every tested legal, survival, and
first-stop B set has full extension degree and full Frobenius orbit size.
So the local plateaus are not proper-subfield or short-orbit samplers.

Trace/norm audit:
[P27 B-Line Trace/Norm Plateau Audit](evidence/p27_b_line_trace_norm_plateau_audit_20260622.md)
then tests the next named Frobenius-invariant buckets.  Trace+norm is exact in
relative quadratic extensions only, where it records conjugate pairs; prime
degree fields remain mixed.  This is regression data for Kummer/Frobenius
class extraction, not a p27 sampler.

Follow-up: [P27 B-Line Reverse-Z Relation Screen](evidence/p27_b_line_reverse_z_relation_20260622.md)
keeps the actual d3 reverse-source root and kills low-degree B-line plane
models in `(B,z)` and nearby branch-normalized coordinates through degree `20`
in q1607/q1847/q2087.  This reinforces that the B-line path needs real
normalization/genus extraction, not a GPU sampler from obvious B projections.

The post-quad moonshot queue is now consolidated:
[P27 First-Class Moonshot Tests After Quadratic Probe](evidence/p27_first_class_moonshot_tests_after_quad_20260622.md).
After the GPU quadratic-gate validation and the q1847 B/K/lambda quartic
closures, the first-class tests are coordinated A/B/K/Sroot Kummer-sequence
extraction and the trace/norm half-norm phase identity.  BSM is demoted to
halving-cover notation unless a non-inherited selector appears.  GPU is
reserved for bounded telemetry or a named
direct sampler; fixed one-bit filters and visible quartic buckets are not
production moonshots.

The coordinated CAS request is now compact:
[P27 A/B/K Symbolic Kummer CAS Brief](evidence/p27_abk_symbolic_kummer_cas_brief_20260622.md).
It puts the conic transition, reduced B-line first transition, f4/f3
`F_A(U,V)` transition, and V4 gamma factorization into one normalization and
Kummer-class extraction brief.  This is the current offline CAS/expert object
that could still yield a below-sqrt source law; without such a named relation,
GPU remains limited to `Dplus` fused pricing and bounded telemetry.
The first executable q7 chart for that brief is
`archive/fixtures/p27_abk_f3_f4_localized_noR_q7_magma.m`; the online Magma
calculator was temporarily disabled when submitted, so no genus/dimension
answer exists yet.  A later retry, and a second retry on 2026-06-22 after
successful smaller H90 function-field Magma tests, both returned `504 Gateway
Timeout`; this remains an offline Magma/Sage normalization task rather than an
online-calculator task.
Finite-field chart counts are now available:
[P27 A/B/K F3/F4 Chart Count](evidence/p27_abk_f3_f4_chart_count_20260622.md).
They show that the f3-plus-only B fibers reproduce the prior gamma handoff,
while all-chart mixed fibers are staging artifacts.  This keeps the live task
as selected-component Kummer extraction and kills all-chart gamma buckets as a
GPU source.
The next-layer count is positive as structure:
[P27 A/B/K F4/F5 Transition Count](evidence/p27_abk_f4_f5_transition_count_20260622.md).
On the selected `f4=+1` component, `chi(W+2)` is constant across
`F_A(V,W)=0` and matches frozen `f5(B)` in q1607/q1847/q2087.  Because the
guard-field `f5` rows are one-sided tails, this promotes CAS comparison of
repeated gamma classes, not GPU production.
The mixed-guard update removes that specific weakness:
[P27 A/B/K F4/F5 Mixed-Guard Transition](evidence/p27_abk_f4_f5_mixed_guard_20260622.md).
In q4999/q5783/q6007/q6247, `f5(B)` has both signs and the exact transition
still holds on every selected B row.  This strengthens the repeated-Kummer
CAS target, while p27/GPU telemetry still kills gamma bucket production.
The cheap visible-source explanation is negative:
[P27 B-Line F5 Visible Character Screen](evidence/p27_b_line_f5_visible_character_20260622.md).
No named B atom and no split linear support of degree `<=2` explains the mixed
`f5(B)` signs, so the live route remains Kummer/Prym extraction rather than a
base-line character bucket.
The cheap recurrence explanation is negative too:
[P27 B-Line Mixed-F5 Recurrence Screen](evidence/p27_b_line_mixedf5_recurrence_20260622.md).
Across q4999/q5783/q6007/q6247 there is no exact visible PGL2 recurrence
`f5(B)=+/-f4(phi(B))`, and the tested Belyi-conjugated hidden-X power maps
cover only small row fractions.  This keeps repeated gamma as a CAS/Prym
class-comparison target rather than a visible recurrence or GPU bucket.
P27 telemetry now sets the practical boundary:
[P27 Gamma-Chain 20k Telemetry](evidence/p27_gamma_chain_p27_20k_telemetry_20260622.md).
On `20k + 20k` train/heldout samples, gamma products and V4 phase links stay
near ordinary half-gates.  The A/B/K gamma recurrence is therefore a CAS
class-comparison lane, while GPU should stay limited to bounded named
telemetry or `Dplus` fused pricing.
The GPU-scale coupling run confirms the boundary:
[P27 GPU Recurrence-Coupling Telemetry](evidence/p27_gpu_recurrence_coupling_20260622.md).
On an A40, `200M` raw draws through gates `3..12` and `200M` raw draws through
gates `3..16` validated the formulas with zero mismatches, but no sign-word
bucket cleared promotion; max heldout all-plus lift was `1.053x` versus the
`1.25x` bar.  This kills current sign-word/gamma GPU production and leaves
CAS Kummer-class extraction plus separate `Dplus` fused pricing.
The repeated-gamma CAS object is now executable:
[P27 A/B/K Gamma4/Gamma5 CAS Fixture](evidence/p27_abk_gamma4_gamma5_cas_fixture_20260622.md).
It stages `gamma4^2=V+2` and `gamma5^2=Wnext+2` on the localized no-R A/B/K
chart.  Online Magma returned a gateway timeout, so this is an offline
Magma/Sage normalization and Kummer-class comparison task.
The current sqrt-beating queue is consolidated here:
[P27 Sqrt-Beating Test Queue After Coupling Kill](evidence/p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md).
It makes the priority explicit: A-level Kummer extraction is the mathematical
mainline, fused/native `Dplus` is the only immediate GPU engineering ask, and
the new bridge test is reconstructing whether `Dplus` H90 coordinates map
cheaply to the A-level `d3` surface.  More gamma/sign-word GPU buckets stay
killed unless CAS names a quotient or source.
The coordinate bridge part is now solved:
[P27 Trace/Norm Dplus A-Coordinate Bridge](evidence/p27_trace_norm_dplus_a_coordinate_bridge_20260622.md).
On same-stream `Dplus` rows, `A = (t - 1/t)^4/4 - 2` exactly matches the
candidate A, so the next cross-lane question is not finding `A`; it is comparing
the pulled-back A-level `d3` class with the H90 payload
`A_eta = U_eta + z*W_eta`.  The bridge is not a source shrink by itself:
`d3/d4` remain balanced half-gates in the probe.
The pulled-back `d3` class is now sharper:
[P27 Trace/Norm Dplus X6/U-Class](evidence/p27_trace_norm_dplus_x6_uclass_20260622.md).
After `Dplus`, every tested y has four `U=x6+1/x6` values and eight `x6`
values; `chi(U+A)=+1`, so `d3=chi(x6)` across the whole second-halving sheet.
This makes the next CAS comparison `x6` squareclass versus H90 `A_eta`, not an
undifferentiated A-level sign.
The cheap version of that comparison is now killed:
[P27 Trace/Norm Dplus H90-X6 Coboundary Probe](evidence/p27_trace_norm_dplus_h90_x6_coboundary_20260622.md)
finds no stable low-weight H90/rho product for `chi(x6)`.  Keep this as an
exact Kummer/Prym comparison, not a GPU sign-bucket request.
The cheap visible formula for the four-`U` cover is negative:
[P27 Trace/Norm Dplus Four-U Rational Screen](evidence/p27_trace_norm_dplus_ucover_rational_screen_20260622.md).
No elementary coefficient of `prod(Z-U_i)` is a rational function of degree
`(20,20)` in `t`, `a=t-1/t`, or `A` on the train/heldout screen.  Continue with
cover normalization and class comparison, not coefficient fishing.
The positive replacement is the reciprocal tower:
[P27 Trace/Norm Dplus Reciprocal Tower](evidence/p27_trace_norm_dplus_reciprocal_tower_20260622.md).
The candidate `xp` roots are reciprocal with `X=t^3+2*t^2-1/t`, and the tower
is `F_A(X,U5)=0`, `F_A(U5,U6)=0`, then `x6^2-U6*x6+1=0`.  This is now the
CAS object for comparing the descended `chi(x6)=chi(U6+2)` row bit with H90
`A_eta`.
The row-bit/resultant follow-up
[P27 Trace/Norm Dplus U6 Row-Bit Resultant](evidence/p27_trace_norm_dplus_u6_rowbit_resultant_20260622.md)
shows that the four `U6` branches over each Dplus row are all `++++` or all
`----`, never mixed, on `8199 + 8061` analyzed rows.  It also records
`R(t,U6)` as degree `16` in `U6`, with square specializations at `U6=+/-2`
and no visible rational factor of `R(t,S^2-2)`.  Source the row bit; do not
build a branch-choice GPU bucket.
The visible branch-atom source is killed by
[P27 Trace/Norm Dplus U6 Row-Bit Branch-Atom Screen](evidence/p27_trace_norm_dplus_u6_rowbit_branch_atom_20260622.md);
continue only with a non-visible quotient/Prym/source relation.
The H90 factor test
[P27 Trace/Norm Dplus U6 Row-Bit H90 Factor Test](evidence/p27_trace_norm_dplus_u6_rowbit_h90_factor_20260622.md)
then shows the named elliptic quotient still leaves the lift irreducible of
degree `32` over `q=607`.
The staged domain-spin/Aeta factor tests
[P27 Trace/Norm Dplus U6 Row-Bit Aeta Factor Boundary](evidence/p27_trace_norm_dplus_u6_rowbit_aeta_factor_boundary_20260622.md)
are the next offline CAS checkpoint; online Magma times out at that tier.
The point-fiber companion
[P27 Trace/Norm Dplus U6 Row-Bit H90 Point-Fiber Probe](evidence/p27_trace_norm_dplus_u6_rowbit_h90_pointfiber_20260622.md)
keeps this alive by showing uniform rational H90/domain-spin/Aeta fibers in
the tested small fields, even when `t` alone is mixed.
The visible-character follow-up
[P27 Trace/Norm Dplus U6 Row-Bit H90 Visible Character](evidence/p27_trace_norm_dplus_u6_rowbit_h90_visible_character_20260622.md)
then kills the cheap explanation: no product character through weight `4` on
`E_h90`, domain-spin, or `A_eta` coordinates exactly matches the row bit.  So
the row-bit signal is real but currently non-visible; do not hand GPU another
sign-bucket scan from these atoms.
The local-solubility follow-up
[P27 Trace/Norm Dplus U6 Row-Bit H90 Solubility Boundary](evidence/p27_trace_norm_dplus_u6_rowbit_h90_solubility_boundary_20260622.md)
is cleaner and positive: in fields `71,167,199,263,607,1607,1847,2087`, both
with and without materialization filters, `Ktrace` square/zero exactly matches
uniform row-bit `t`-fibers, while `Ktrace` nonsquare gives mixed fibers with
`4` plus and `4` minus branches.  The next theorem target is the H90
local-solubility boundary plus the non-visible soluble-side sign class.
The small group-coset follow-up
[P27 Trace/Norm Dplus U6 Row-Bit H90 Group-Coset Screen](evidence/p27_trace_norm_dplus_u6_rowbit_h90_group_coset_20260622.md)
kills the nearest sourceable shortcut for that sign: after mapping to
`E: v^2=u^3-u`, small quotient projections through `m=24` have no nontrivial
exact separation in the fields with both signs.  Keep the row-bit lane in
divisor/theta/Prym extraction, not GPU coset buckets.
The `u`-divisor follow-up
[P27 Trace/Norm Dplus U6 Row-Bit H90 U-Divisor Screen](evidence/p27_trace_norm_dplus_u6_rowbit_h90_u_divisor_20260622.md)
finds a sharper positive/negative split: the soluble-side sign descends to
`u=4/(t-1/t)^2` with zero mixed `u` groups, but monic degree `<=2` divisors
have no exact hits.  It creates
`archive/fixtures/p27_dplus_rowbit_u_divisor_targets_20260622.json` for exact
monic cubic/quartic support tests in the promotion fields.
That exact-support follow-up now kills the visible q1847 low-degree route:
[P27 Trace/Norm Dplus U6 Row-Bit H90 U Cubic/Quartic Screen](evidence/p27_trace_norm_dplus_u6_rowbit_h90_u_cubic_quartic_20260622.md).
Full monic cubic scans in q607/q1607/q1847/q2087 and a full q1847 monic
quartic scan all find zero exact supports.  Since q1847 quartic random exact
fits are expected only about `6.31e-7` times, visible monic `P^1_u` support
through degree `4` is closed in the decisive field.  The row-bit lane now
needs non-visible divisor/theta/Prym extraction, not a GPU cubic/quartic
bucket run.
The small-field descent audit then sets the boundary:
[P27 Trace/Norm Dplus Reciprocal Tower Small-Field Descent](evidence/p27_trace_norm_dplus_reciprocal_tower_smallfield_descent_20260622.md).
Over q607/q1607/q1847, the naked reciprocal tower has mixed `A`/`B` fibers for
`d3=chi(x6)=chi(U6+2)`, even after materialization filters.  Thus the selected
legal/core source cut is essential: do not hand GPU a naked `F_A` tower
sampler, and do not compare the tower to H90 `A_eta` as if it were already the
source-level A/B Kummer class.

### Card 4c: K-Line Fit Significance

K-line exact fits now have a quantitative promotion rule:
[P27 K-Line Fit Significance](evidence/p27_kline_fit_significance_20260622.md).

The q863 exact cubic burst is expected interpolation, not structure:

```text
q863 d3 monic cubic expected exact fits ~= 76.6
observed exact cubics = 58
```

By contrast, exact d3 cubics in the promotion fields would be highly
non-random:

```text
q1471 expected ~= 5.65e-6
q1607 expected ~= 1.47e-5
q1847 expected ~= 1.37e-9
```

Status: promote only stable promotion-field d3 low-degree formulas or
branch-cover/genus extraction.  Demote q863 cubics and low-row d4 local fits.

Promotion-field update:
[P27 K-Line q1471 Cubic Promotion Screen](evidence/p27_kline_q1471_cubic_promotion_screen_20260622.md)
exhausted all `3,183,010,111` monic cubics over q1471 and found no exact d3
cubic.  Since degree `<=2` was already killed, the K-line source shape
`z^2 = cubic(K)` is now dead in the first promotion field.  The K-line
moonshot is reduced to quartic/non-polynomial branch-cover extraction and
genus/sourceability.

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
Hilbert-90 involution identity under `t -> -1/t`.  The other visible
automorphisms `t -> 1/t` and `t -> -t` mix `T_line`, so there is no smaller
automorphism quotient.  Simple trace/anti-trace/norm evaluations of the H/V
sections are also killed.  The easy quotient automorphism orbit explains
`domain_line` but not `T_line`.

## Active Interpretation

The p24 and p26 early hits keep the seed-ordering/source-stratum question alive,
but the current evidence does not justify treating early hits as proof of a
hidden scheduling shortcut. For p27, the high-value move is to turn p26's
post-hit structure into pre-registered p27 tests and let the telemetry decide.
