# P27 GPU Agent Initial Handoff

Date: 2026-06-21

## Target

```text
p = 1000000000000000000000000103 = 10^27 + 103
sqrt_floor(p) = 31622776601683
k = 45
p mod 8 = 7
p mod 4 = 3
```

No p27 hit is known yet.

## Current Ask

Do not start with a giant production run unless explicitly requested. The first
useful GPU task is now a bounded structure test for the conic-chain recurrence:
[P27 GPU Conic-Chain Test Handoff](p27_gpu_conic_chain_test_handoff_20260621.md).
Older line/trace telemetry remains useful as controls, but the conic-chain
test is the first one that is plausibly source-shaped rather than just another
fixed-prefix filter.

CPU gate result:
[P27 Trace/Norm Transfer Gate](p27_trace_norm_transfer_gate_20260621.md).
The EK quotient, b-flip cocycle, domain-line descent, and target-line descent
all passed on p27.

CPU practical result:
[P27 Practical Trace/Norm Prefilter Smoke](p27_practical_trace_norm_prefilter_smoke_20260621.md).
The C trace/norm prefilter ran cleanly and showed a bounded CPU net of about
`1.10x` to `1.19x` survivors per second at stable depths 16-19.
[P27 Trace/Norm Variant Benchmark](p27_trace_norm_variant_benchmark_20260621.md)
then found `tracechar` effectively tied with `traced`, while `tracesqrt` was
slower on CPU.

Updated CPU practical result:
[P27 Practical Domain-Line Filter](p27_practical_domain_filter_20260621.md).
The cheaper domain-only filter is now the first GPU A/B candidate.  On measured
CPU streams, `domain_line=-1` had zero depth-16+ survivors, and the
domain-only filter netted about `1.29x` to `1.39x` survivor-per-second at
stable depths on seeds `121`/`122`.

Important correction:
[P27 Domain Line Equals First-Halving Gate](p27_domain_first_halving_gate_20260621.md).
The domain filter is exactly the first-halving square-root gate
`F=(y-1)(y^2-2)(y^2-2y+2)`.  Treat it as a practical constant-factor prefilter,
not as a sqrt-beating theorem.  The math telemetry we most want is whether
`T_line` or another quotient/Hilbert-90 bit predicts a later post-domain
halving gate.

Best current practical source:
[P27 First-Lift Elliptic-Cover Port](p27_first_lift_ecover_port_20260621.md).
The p25 residual elliptic-cover sampler ports to p27:

```text
w^2 = y(y - 1)(y - 2), equivalently E: w^2 = x^3 - x with x = y - 1.
```

It sources the first-halving/domain gate directly.  CPU p27 A/B on two 1M
seeds shows `ecover` beating raw nonsplit survivor-per-second at depth 16 by
about `1.31x` to `1.35x` and at depth 18 by about `1.27x` to `1.67x`.
Domain/dgate remains a useful control, but `ecover` is now the first practical
GPU A/B candidate.  The same note records that residual elliptic 2-descent
classes are flat, so this is not yet the second-gate/tower law.

Latest CPU telemetry:
[P27 Post-Domain Next-Gate Telemetry](p27_post_domain_next_gate_telemetry_20260621.md).
On seeds `124` and `125`, `T_line` is flat at early post-domain gates.  It
should be reported as a control bit, not promoted as the expected winning
filter.

Newest structure:
[P27 Second-D Gate Frontier](p27_second_d_gate_frontier_20260621.md).
After `domain_line=+1`, the next gate is the Montgomery discriminant
`d2=x5^2+A*x5+1`.  In a 1M CPU run, every depth-6 failure was `d2`
nonsquare; there were no `d2` square / `w` failures.  `T_line` is flat against
`d2`.

Tower update:
[P27 Selected Halving Tower Profile](p27_halving_tower_profile_20260621.md).
Through eight selected halving gates in a 1M CPU profile, every obstruction was
the next `d_j` squareclass.  There were zero `d_j` square / `w_j` failures and
zero two-`w_j` branches.

Reason:
[P27 Nonsplit W-Obstruction Identity](p27_nonsplit_w_obstruction_identity_20260621.md).
For a nonsplit Montgomery row, `w_+*w_-=16*x^2*(A^2-4)`, so when `d_j` is
square exactly one `w_j` branch should be square.  The GPU does not need a
separate `w_j` filter beyond mismatch/degenerate telemetry.

Cleaner 2-descent phrasing:
[P27 X-Square / 2-Descent Gate](p27_xsquare_2descent_gate_20260621.md).
For nondegenerate `F_p` points on `E_A`, `chi(d_j)=chi(x_j)`.  GPU prefix
tests can therefore report `x_4`, `x_5`, `x_6` squareclasses directly.

New exact second-gate selector:
[P27 Label-2 Second-Gate Cover](p27_label2_second_gate_cover_20260621.md).
In label-2 residual coordinates

```text
W^2 = X^3 - X
y = 2X/(X - 1)
T^2 = X(X^2 + 1)(X^2 + 2X - 1)
```

the p27 second gate is exactly `compactD=-1`.  The older `compactD=+1`
selector is the wrong p27 sign and produced no depth-16 survivors in a 500k
CPU stats probe.  The corrected-sign CPU mode `compactdneg` starts at depth 6
and gives the expected 2x conditional lift, but is too slow on CPU.  GPU should
test whether this compact criterion is cheap enough natively.

Genus/recurrence warning:
[P27 Label-2 Cover Genus And Recurrence Probe](p27_label2_cover_genus_recurrence_20260621.md).
The first finite-local probe prices the mixed `R` cover at genus `17`, and two
`compactD=-1` streams show the next gate survives at about `1/2`.  Treat
`compactD=-1` as telemetry or a practical fixed-prefix test, not as a known
sqrt-beating source.

Follow-up trace counting:
[P27 Label-2 Cover Trace Decomposition Probe](p27_label2_cover_trace_decomposition_20260621.md).
The intermediate `V4` cover decomposes after a common-branch correction, but
the new Prym trace is not a small visible combination of the `W/T/WT` quotient
traces.  If GPU reports a fixed-prefix gain, still ask for `d3/d4`; if GPU is
flat, the remaining math test is Sage/Magma Prym/Jacobian decomposition.

Positive symmetry follow-up:
[P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md).
The `T -> -T` deck involution lifts to the full second-gate cover with order
`4`, and the quotient has genus `1`, so `compactD=-1` is a cyclic quartic
cover over the residual elliptic curve.  This makes `compactD=-1` more than a
blind filter, but it still needs `d3/d4` telemetry or a cheap cyclic-quartic
source before it becomes a sqrt-beating path.

Alpha/branch recurrence warning:
[P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md).
On 5,000 paired compactD rows, `compactD=-1` matched d2 with zero failures.
But d3 was invariant across both paired `T` roots and both second-half
x-branches, with random-looking `0.4932` plus rate.  Conditioned on d3, d4
had the same invariant-branch shape with `0.5174` plus rate.  Do not spend GPU
time looking for a branch-choice or T-deck-choice selector for d3/d4.  Report
the prefix rates and effective survivor/sec; branch enumeration is only a
consistency check if essentially free.

U+2 prefix-gate formula:
[P27 Halving U+2 X-Square Gate](p27_halving_usquare_gate_20260621.md).
For a successful halving step with `x_next + 1/x_next = u`,
`chi(x_next)=chi(u+2)=chi(u-2)`.  On the p27 compactD sample, this had zero
mismatches for d2-to-d3 and d3-to-d4.  It rejected `50.68%` of d3 attempts and
`48.26%` of d4 attempts before materializing the next branch root.  GPU should
test this only as a cost optimization: report whether the `u+2` precheck wins
effective survivors per GPU-second after Legendre/sqrt cost.

U+2 sequence warning:
[P27 U+2 Sequence Recurrence Screen](p27_usquare_sequence_recurrence_20260621.md).
On 30,000 compactD/d2 rows, gates 3 through 6 had plus rates `0.5001`,
`0.4975`, `0.4965`, and `0.5003`, with later deviations explained by smaller
tail counts.  Do not treat compactD or the u+2 precheck as a sqrt-beating
structure by itself.  It is a fixed-prefix cost optimization unless a
multi-gate recurrence is supplied.

U+2 norm/coboundary warning:
[P27 U+2 Norm/Coboundary Screen](p27_usquare_norm_coboundary_20260621.md).
The local norms through the two `s^2=d` branches are exact:
`Norm_s(u+2)=4*x*(2-A)`, `Norm_s(u-2)=-4*x*(A+2)`, and
`Norm_s(u^2-4)=16*x^2*(A^2-4)`.  But the selected `w`-square branch's `u+2`
bit is not visible in the local `A,x` norm/branch character span.  The best
30k-row d3 score was `0.5018`; the best d4 score was `0.5025`.  Do not
implement a local norm-factor selector unless a new theorem names a new
orientation/cocycle object.  The live mathematical target is selected-branch
H90/cocycle coupling, not another visible norm scan.

Selected-orientation span warning:
[P27 Selected Orientation/Cocycle Span Screen](p27_selected_orientation_cocycle_span_20260621.md).
Two 30,000-row CPU seeds allowed local characters plus selected `s`-branch
orientation characters from the successful prefix through gates 3-6.  No exact
GF(2) product predicted the next `u+2` bit, and the weak low-weight in-sample
lifts did not replicate as the same named products.  Do not implement these
orientation products as GPU filters.  If orientation columns are already
available, log them only as diagnostics.  The next real source target is the
reverse-doubled square-source construction, not another prefix-product scan.

Reverse-doubling source warning:
[P27 Reverse-Doubling Source Screen](p27_reverse_doubling_source_screen_20260621.md).
The reverse equations are exact, but p27 density remains random-half on two
5,000-pair CPU seeds (`0.4932` and `0.5044`).  The source multiplicity also
matches the generic expectation of about `2` z-points and `4` `(z,Y)` points
per oriented compactD candidate.  Do not implement a reverse-doubling GPU
sampler until a quotient/source map is named by Sage/Magma or an expert.  GPU
can log reverse-source columns only as diagnostics.

GPU U+2 cost result:
[P27 GPU U+2 Precheck Probe](p27_gpu_uprecheck_probe_20260621.md).
CUDA `x16uprecheckprobe` confirmed the identity as a real continuation-scope
shrink, but this independent Legendre implementation lost per second.  At
depth 8, baseline was `36.89M` accepted roots/sec versus `29.96M` for the
precheck; at depth 10, baseline was `33.85M` versus `27.84M`.  Keep the
telemetry, but do not promote independent `u+2` Legendre prechecks as the
production implementation.  The useful next question is whether there is a
direct source or recurrence into the smaller `u+2` stratum.

Conic-chain update:
[P27 Quadratic Gate Recurrence](p27_quadratic_gate_recurrence_20260621.md)
and [P27 Conic-Chain Source Screen](p27_conic_chain_source_screen_20260621.md)
give the current best source-shaped GPU target.  In coordinates
`A=2-c^2`, `x_j=r_j^2`, the next selected gate is exactly
`chi(r_j^2+c*r_j+1)` in all tested p27 rows.  The legal one-step pair is:

```text
h_j^2 = r_j^2 + c*r_j + 1
g_j^2 = r_j^2 - c*r_j + 1
r_{j+1}^2 - (h_j + g_j)*r_{j+1} + 1 = 0
```

The one-step pair has a direct rational sampler.  For nonzero `R,L`, set:

```text
a = R - 1/R
s = R + 1/R
d = (L - a^2/L)/2
r = -(L + a^2/L)/4
h = (s + d)/2
g = (s - d)/2
c = s*d/(2*r)
```

Then `h^2=r^2+c*r+1`, `g^2=r^2-c*r+1`, and
`R^2-(h+g)R+1=0`.  The legal incidence screen now shows the important split:
[P27 Conic-Pair Sampler Legal Incidence](p27_conic_pair_sampler_legal_incidence_20260621.md).
The sampler image covers every legal d3-plus `(A,x5)` class tested and no
d3-minus classes, but random free `(R,L)` hits legal rows at only about
`constant/q`.  So instrument the formula and test any implemented legal
pullback source; do not promote raw random `(R,L)` as a production sampler.

The next selector is also explicit now:
[P27 Conic-Pair D4 Recurrence](p27_conic_pair_d4_recurrence_20260621.md).
With `a=R-1/R` and `L=h-g-2r`, the d4 gate is:

```text
d4 = chi(-(L+a)(L-a)cR)
```

because the quotient with `R^2+cR+1` is `2` times a square and p27 has
`chi(2)=+1`.  GPU should log this only when legal conic-pair variables are
already available.  This is not a license to run raw random `(R,L)`.

Packet source warning:
[P27 Label-2 E[2] Packet Source Probe](p27_label2_e2_packet_source_probe_20260621.md).
The easy rational `E[2]` packet source has already been tested on p27 and gives
`1.0x` source lift.  Do not spend GPU time on packet3 unless a new invariant
changes the source metric.

Residual `[3]` warning:
[P27 Label-2 Residual E[3] Coset Screen](p27_label2_residual_e3_coset_screen_20260621.md).
Coset `0` did not replicate as a stable lift.  Log it only if residual coset
telemetry is essentially free; do not prioritize it over compactD/d3/d4.

Visible-character warning:
[P27 Label-2 Visible Residual-E Character Screen](p27_label2_visible_e_character_screen_20260621.md).
The natural H90 factor span on `E` did not produce an exact compactD character.
Do not spend GPU time on visible E-factor selectors unless a new theorem names
a different divisor.

P26 trace/norm GPU lesson:
[P27 GPU Filter-Cost Lesson From P26](p27_gpu_filter_cost_lesson_from_p26_20260621.md).
The p26 `D_trace=+1` stratum captured every observed depth-20 through depth-28
survivor in three 100M raw-`y` streams, so the stratum is real.  But the
current classifier path is too expensive: the best filter-only run was about
`4.47M` candidate roots/sec versus `31.87M` accepted roots/sec for the
no-trace baseline.  For p27, report effective deep survivors per GPU-second,
not just enrichment.  Prefer direct samplers, cheaper algebraic tests, or
recurrence telemetry over expensive rejectors.

P26 seed-law caution:
the p26 GPU stratum probe on branch `codex/add-cuda-p26-search` recovered the
p26 hit, but identity/splitmix/mixed seed order and the hit compact bucket did
not produce a held-out-promoted stratum.  Do not spend p27 GPU time on
seed-order assumptions unless a new invariant is supplied.

Do not spend GPU time on the named branch/norm product
`chi_B * chi(y-2) * chi(1-t^2)`.  It had a `1.039x` in-sample lift but dropped
to about `1.00x` on held-out p27 seed streams:
[P27 Component Norm / Half-Norm Audit](p27_component_norm_halfnorm_audit_20260621.md).

Likewise, simple H/V trace-coupling counters are optional telemetry only, not
production filters.  The best non-taut CPU lifts were percent-level and not
exact:
[P27 H/V Trace Coupling Audit](p27_hv_trace_coupling_audit_20260621.md).

## Required Reports

For any p27 GPU run, report:

```text
code commit or source hash
exact command
GPU model
seed base / seed offset / cap
candidate stream definition
raw candidates tested
accepted candidates
candidate rate
accepted candidate rate
hit if any: p, A, x0
verifier result if any hit
full log path
```

For source/filter A/B tests, also report:

```text
same-seed coverage check
baseline candidates and rate
filtered/source candidates and rate
survivor lift
effective lift per GPU-second
classifier/source cost versus baseline
any branch/sign mismatch count
```

## First Suggested GPU Experiments

0. Bounded conic-chain structure test:

```text
baseline = raw p27 X1(16) nonsplit halving path
candidate A = recurrence telemetry:
              next_gate = chi(r_j^2 + c*r_j + 1)
candidate B = legal pullback of the one-step pair sampler, if implemented
candidate C = two-step chain pressure if B maps to legal rows
```

Report mismatch counts, legal pullback rate, d3/d4/d5 rates, and effective
deep survivors/sec.  Do not run free random `(R,L)` as a production source:
CPU guard fields show legal hits are only `~constant/q` per draw.  Promote only
if the legal pullback source gives a real heldout rate lift or controls more
than one selected gate without paying a new independent Legendre/sqrt toll. Use
[P27 GPU Conic-Chain Test Handoff](p27_gpu_conic_chain_test_handoff_20260621.md)
as the exact brief.

1. Tiny p27 baseline smoke: confirm the GPU implementation accepts p27 and
   emits the same type of candidate telemetry as p26.
2. Same-stream A/B, first priority:

```text
baseline = raw p27 X1(16) nonsplit halving path
candidate A = p27 first-lift elliptic-cover source:
              E: w^2=x^3-x, y=x+1
candidate B = p27 domain-line/dgate filter:
              F=(y-1)(y^2-2)(y^2-2y+2) is a square
same seeds, same cap, same reporting horizon
```

Report depth/survivor lift and effective lift per GPU-second.
Treat candidate B as the control; candidate A is the preferred practical test.

2b. Same-stream A/B, practical/structure bridge:

```text
baseline = raw p27 X1(16) nonsplit halving path
candidate A = ecover first-lift source
candidate B = ecover label-2 + compactD=-1:
              this is the p27 second-gate selector
```

Report whether `d2` is cheap enough in the GPU implementation to be useful.
This is still constant-factor filtering unless a longer tower rule follows.
Use the p26 trace/norm result as the guardrail: a strong stratum is not a win
if the classifier cost overwhelms the lift.

2c. Prefix-gate telemetry if cheap:

```text
candidate C = require d1,d2,d3 square
candidate D = require d1,d2,d3,d4 square
```

Report per GPU-second rates and whether any `w_j` obstruction or multi-branch
case appears.  The CPU profile saw none through eight gates.
The branch recurrence probe explains why branch choice should not help:
available half x-branches have the same squareclass, so they share the next
`d_j` character.
If implementing fixed prefixes, also A/B the `u+2` precheck before
materializing `x_next`; promote only if it improves effective prefix
survivors/sec.
If the fixed-prefix path loses per second, keep the telemetry but do not
promote it as production.

3. Same-stream A/B, second priority:

```text
baseline = raw p27 X1(16) nonsplit halving path
candidate = p27 trace/norm D prefilter equivalent to x16halvenonsplittraced
            or x16halvenonsplittracechar
same seeds, same cap, same reporting horizon
```

Report depth/survivor lift and effective lift per GPU-second.

4. Same-stream p27 line telemetry:

```text
a = (y - 1) - 1/(y - 1)
b = w((y - 1)^2 + 1)/(y - 1)^2
domain_line = chi((y - 1)(y^2 - 2)(y^2 - 2y + 2))
T = D * chi(y)
T_line = T if chi(a)=+1 else T * chi(b)
```

Report survivor/depth distributions for the four strata:

```text
domain_line=+1, T_line=+1
domain_line=+1, T_line=-1
domain_line=-1
unusable/branch mismatch
```

Treat `T_line` as telemetry only unless the GPU finds a much stronger
same-stream survivor-per-second signal than CPU did.  CPU data now says it is
flat at depths `6`, `8`, and `10` after `domain_line=+1`.

If available, also report the next one or two post-domain halving gate
outcomes inside `domain_line=+1`.  This is now the main structure test:

```text
domain_line=+1, next_halving_gate pass/fail
domain_line=+1, next2_halving_gate pass/fail if cheap
T_line split against those deeper gates
explicitly report d2_chi = chi(x5^2 + A*x5 + 1)
if cheap, also report d3_chi and d4_chi on the selected branch
```

For label-2 compactD specifically, report both signs.  `compactD=-1` should
match the second gate on p27; `compactD=+1` is a negative-control sign.
Also report `d3_chi` and `d4_chi` inside `compactD=-1`; CPU currently says the
next gates are flat and invariant across the obvious branch/T choices.

5. Same-stream p27 baseline vs any candidate source/filter that beats its
   throughput loss in the line telemetry.
6. Only then consider a large production hunt.

## Transfer Warning

p26 was `p mod 8 = 3`; p27 is `p mod 8 = 7`. Any GPU-native implementation of
the p26 trace/norm filter must rederive or import p27-specific signs rather
than copying p26 constants blindly.
