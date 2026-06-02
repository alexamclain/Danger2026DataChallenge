# p23 Ruled-Out / Maybe / Untested Synthesis

Generated from the local research state on 2026-06-01 PDT.

Target:

```text
p = 100000000000000000000117
k = 39
sqrt_floor(p) = 316227766016
completed all-X1 run = runs/p23_x16halve_20260601_110154
active run = runs/p23_x16halvenonsplit_20260601_201436
latest live decision check = keep_waiting during y-filtered nonsplit fallback
```

Purpose: a compact ledger of the mathematical and engineering routes tried so
far, grouped by current decision status:

```text
production / active = use now or staged as the next operational step
ruled out           = not a credible p23 production path under current evidence
maybe               = mathematically alive, but not ready to change production
not yet tested      = genuinely incomplete or not tested decisively
```

This file is a synthesis. Detailed backing notes are listed at the end.

## Current Bottom Line

The only production path that should affect the live p23 search right now is:

```text
1. Keep the active y-filtered nonsplit X1(16) fallback shard running.
2. If a worker prints Verified: PASS, finalize and independently verify.
3. If the nonsplit budget misses cleanly, use the next-action gate and the
   prepared direct-y nonsplit follow-on before launching any extension.
```

No research lane found so far is strong enough to kill or restart the active
run.

The main mathematical insight that survived testing is the split/nonsplit
discriminant class:

```text
split    iff chi(A^2 - 4) =  1
nonsplit iff chi(A^2 - 4) = -1

For the X1(16) y-parameter:
chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2)).
```

For the external short-certificate repo, split is useful inside a low-product
certificate frontier. For this p23 high-depth X1(16) search, the useful
production direction is the opposite sign: nonsplit.

## Production / Active

### Active all-X1(16) first-branch halving

Status:

```text
completed p23 production shard; clean 50B miss
```

Idea:

```text
Sample from Sutherland's X1(16) family so the curve starts with a known point
of order 16. Then repeatedly try rational halving, taking one deterministic
branch when a half exists.
```

Evidence:

```text
The model predicts expected trials about 34.6B / L, where L is the empirical
liftability factor. A hit in the 35B-45B region would be consistent with
L around 0.8-1.0. A 50B miss would be disappointing but not decisive.

Completed run:
  runs/p23_x16halve_20260601_110154
  aggregate_trials = 50.000B
  Verified: PASS = none
```

Decision:

```text
Closed as a miss, not as a falsification. Keep it as conditioning evidence for
the active y-filtered nonsplit fallback.
```

### Active fallback: y-filtered nonsplit X1(16)

Status:

```text
active production fallback
```

Idea:

```text
Pre-filter X1(16) y-values to the nonsplit Montgomery discriminant class:

  chi((y^2 - 2)(y^2 - 4y + 2)) = -1
```

Evidence:

```text
The X1(16) discriminant pullback was symbolically derived and then audited
against actual roots.

Largest transfer audit:
  accepted_y = 512
  roots_checked = 1024
  mismatches = 0
  status = PASS

p23 diagnostics:
  nonsplit depth-16 first-branch lift over all-X1 first branch ~= 1.86x
  effective wall-clock proxy after filter cost ~= 1.5x

active binary:
  pomerance_nonsplit_yfilter
  sha256 = 33c9120f7ab39258b4a5da0b1b1cbd13ebe16d15e43409f7a4fe0c1339b271c1
```

Decision:

```text
Keep waiting. Do not restart or mutate active workers.
```

## Clearly Ruled Out For p23 Production

These results may still be mathematically true or useful elsewhere. They are
ruled out only as immediate p23 discovery paths under current evidence.

### Exact-trace CM construction

Idea:

```text
Construct a curve with exactly one of the two target traces using CM.
```

Evidence:

```text
4p - 321963163766^2
  = 2^4 * 3 * 6173744191203913847869

4p - (-227792650122)^2
  = 2^4 * 19 * 2377 * 481741841427711973

The fundamental discriminants are huge and the conductor is only 4.
```

Verdict:

```text
Ruled out for p23. There is no hidden small-class-discriminant CM shortcut.
```

### Direct low-product short-certificate frontier

Idea:

```text
Search the low A*x0 / small x0 region used by the linked
danger3-short-certificate-experiments repo.
```

Evidence:

```text
Using the repo's sparse-grid model lambda ~= 2.571:

x0 <= 64, A*x0 <= 1.25*p/log(p):
  candidates ~= 8.84e21
  expected hits ~= 0.227

About one expected hit would require p/lambda ~= 3.89e22 checks.
```

Verdict:

```text
Ruled out as a first-hit method for p23. It remains a post-hit minimization
tool only.
```

### Split-first transfer from the short-certificate repo

Idea:

```text
Prefer chi(A^2 - 4) = +1 because the external low-product experiments benefit
from split Montgomery curves.
```

Evidence:

```text
The discriminant axis transfers, but the sign does not. Exact small-prime
trace enumeration shows split is curve-level trace-enriched, but p23 marked
point halving diagnostics favor nonsplit.

Follow-up p23 audit:
  notes/x16_split_trace_vs_halving_audit_20260602.md

First-branch splitstats, 500k p23 samples to depth 16:
  depth 12 split first    = 3/249888
  depth 12 nonsplit first = 972/250112
  depth 16 split first    = 0/249888
  depth 16 nonsplit first = 40/250112

Split-class first-vs-all branchstats, 200k p23 samples to depth 16:
  depth 14 split all      = 34/99968
  depth 14 nonsplit all   = 112/100032
  depth 16 split all      = 14/99968
  depth 16 nonsplit all   = 20/100032

Split all-branch recovers some survival only by carrying a much larger
frontier; it does not beat nonsplit on the useful p23 calibration depths.

Split 2-torsion translation follow-up:
  notes/x16_split_torsion_translate_audit_20260602.md

For a split Montgomery curve, adding rational 2-torsion to the marked X1(16)
point gives four same-curve starts: P, P+T0, P+Talpha, P+Tbeta. A 200k p23
holdout showed this really recovers split component mass:

  depth 10 original split first = 45/200000
  depth 10 best-of-four         = 160/200000
  depth 12 original split first = 4/200000
  depth 12 best-of-four         = 16/200000

But the same best-of-four split path is still far below active nonsplit:

  depth 12 split best-of-four = 0.000080
  depth 12 nonsplit first     = 0.003886
  depth 14 split best-of-four = 0.000010
  depth 14 nonsplit first     = 0.000840

The measured split translated rate was only 0.048391M split samples/s
or 0.096788M all-X1 attempts/s.
```

Verdict:

```text
Ruled out as a p23 production ordering under current first-branch or all-branch
machinery. Split can only revive with a cheap section/orientation label that
places the marked point in the useful component without carrying the frontier.
The 2-torsion translation test validates the component idea but is also ruled
out as a production shard under current depth rates.
```

### Fixed-A inverse tree / MITM as a search replacement

Idea:

```text
Invert the Montgomery doubling map for a fixed A and use meet-in-the-middle
or inverse-tree enumeration.
```

Evidence:

```text
The identity is correct and useful:

f_A(x) = (x^2 - 1)^2 / (4*x*(x^2 + A*x + 1))
y = x + 1/x
f_A(x) = (y^2 - 4) / (4*(y + A))

But it solves x0 after A is chosen. It does not select an A whose curve has
one of the rare p23 target traces.
```

Verdict:

```text
Ruled out as a first-hit replacement. Keep as a diagnostic identity.
```

### Full all-branch halving

Idea:

```text
Carry every rational half instead of one deterministic branch.
```

Evidence:

```text
p23 depth-12 diagnostics:
  first-branch survival ~= 0.0021-0.0023
  all-branch survival   ~= 0.0029-0.0030

The lift is real, but the branch frontier can grow to hundreds or thousands
of x-coordinates.
```

Verdict:

```text
Ruled out as direct production. It spends too much state/cost for the lift.
```

### Bounded recursive lookahead

Idea:

```text
Use shallow recursive lookahead to choose the halving child with more
descendants.
```

Evidence:

```text
p23 target depth 12:
  first survival    = 0.002310
  lookahead depth 2 = 0.002860
  all-branch upper  = 0.003020
  half-call cost    = 2.14x

p23 target depth 14:
  first survival    = 0.000480
  lookahead depth 2 = 0.000660
  all-branch upper  = 0.000720
  half-call cost    = 2.14x
```

Verdict:

```text
Ruled out as-is. It proves better branches exist, but the observed selector
cost exceeds the survival gain.
```

### Static sign-label branch ordering

Idea:

```text
Prefer a fixed sign pattern in the square-root choices used by halving.
```

Evidence:

```text
200k p23 samples to depth 14:
  natural_0123 = 0.000460
  prefer_1     = 0.000460
  prefer_2     = 0.000465
  prefer_3     = 0.000460
```

Verdict:

```text
Ruled out. The better branch is not encoded by a fixed sign label.
```

### Inverse-gate branch score

Idea:

```text
Use a Legendre gate derived from the inverse-doubling identity to choose a
child likely to have another rational half.
```

Evidence:

```text
p23 depth-12:
  all X1(16): first = 0.002310, gate = 0.002310, all = 0.003020
  nonsplit:   first = 0.004100, gate = 0.004100, all = 0.004100
```

Verdict:

```text
Ruled out as production. No survival lift and extra Legendre work.
```

### Quartic / sqrt-flag filters

Idea:

```text
Use p = 5 mod 8 square-root flags, quartic characters, or +/- sqrt(-1)
cosets to filter the nonsplit stream.
```

Evidence:

```text
Deep-survival flags were balanced or too weak. The best half-density features
did not retain enough deep survivors to compensate for discarding half the
stream.

1M p23 nonsplit depth-16 holdout:
  earlier chi(y+1) and chi(y-1) tilts did not persist
  strongest genuine pre-halving half-density rows captured only about 54.8%
  of depth-16 survivors, roughly 1.10x over the nonsplit base
```

Verdict:

```text
Ruled out for the next shard.
```

### Cubic character / ell=3 native y filter

Idea:

```text
Use a cubic character of an X1(16) y-polynomial as a cheap trace-mod-3 proxy.
```

Evidence:

```text
100k p23 nonsplit samples to depth 20:
  cube coverage ~= 0.335
  depth-16 cube survival    = 0.000119
  depth-16 noncube survival = 0.000301
  depth-20 cube/noncube essentially tied
```

Verdict:

```text
Ruled out for production filtering.
```

### Naive SEA / Atkin trace-mod-3 filter

Idea:

```text
Reject curves whose trace modulo 3 cannot match the target traces.
```

Evidence:

```text
exact ell=3 C benchmark:
  filter cost ~= 79.2 us/curve
  specialized quartic pow-only cost ~= 65.4 us/curve
  current x16halve path ~= 9.2 us/trial
  rejection rate ~= 37.5%
```

Verdict:

```text
Ruled out unless a qualitatively cheaper closed form is found. Optimizing the
known degree-4 Euler powmod/gcd path cannot meet the p23 cost gate because the
powmod alone is already about 21x above ell=3 break-even.
```

### Ell=3 quartic-pattern shortcut

Idea:

```text
Replace the slow exact ell=3 polynomial-Frobenius classifier by the
factorization pattern of the Montgomery 3-division quartic

  psi_3(x) = 3*x^4 + 4*A*x^3 + 6*x^2 - 1

or by an obvious one-symbol character in A.
```

Evidence:

```text
Three 1000-sample calibration-prime probes showed:

  trace == 0 mod 3  => psi_3 pattern ((2,1),(2,1))

but both trace == 1 mod 3 and trace == 2 mod 3 appear in the common
((1,1),(3,1)) pattern and in the fully split pattern.

Simple A-character features such as A, A +/- 2, A^2 - 4, A^2 - 3, and
A^2 +/- A + 1 gave only weak, unstable reject-class lifts around 1.1-1.15.
```

Verdict:

```text
Ruled out as a production shortcut. Factorization type alone sees rational
3-torsion x-coordinates, but distinguishing the rejected trace == 1 class from
the accepted trace == 2 class still requires the curve-versus-twist square
test at rational roots.
```

### Low-degree ell=3 y-cubic pullback

Idea:

```text
Search cubic characters of low-degree X1(16) y-polynomial features for a cheap
parameter-level proxy for trace mod 3.
```

Evidence:

```text
Three calibration primes, 1500 X1(16) samples each, and 1538 cubic-character
expressions were tested.

The best stable feature was C3_resolvent:
  min majority accuracy ~= 0.5883
  avg majority accuracy ~= 0.5939
  best bucket mostly trace == 0 mod 3

But C3_resolvent still mixed rejected trace == 1 with accepted trace == 2,
and product expressions fell back to roughly baseline purity.
```

Verdict:

```text
Ruled out as the current low-degree y-character version of the ell=3 pullback.
The direct symbolic pullback also does not collapse into a low-degree
y-character:

  notes/ell3_x1_16_square_root_pullback_audit_20260602.md

The remaining squareclass bit is now identified more precisely:

  notes/ell3_frobenius_eigenvalue_squareclass_closure_20260602.md

For p == 1 mod 3, rational 3-torsion x-roots have uniform squareclass, and
that squareclass is exactly the Frobenius eigenvalue on the rational
3-torsion line. A 6000-sample p23-residue holdout had zero mixed-squareclass
cases and zero classifier mismatches. Thus there is no root-local shortcut
left; only a genuinely new formula for this 3-isogeny eigenvalue character on
the X1(16) parameter could revive the lane. A faster generic quartic-root or
powmod routine is no longer enough, because the specialized pow-only benchmark
is already far above the microsecond cost gate.
```

### Ad hoc native X1(16) trace-residue y features

Idea:

```text
Find Legendre features of the X1(16) parameter y that enrich target trace
residues modulo small odd primes.
```

Evidence:

```text
Feature winners were unstable across calibration primes. Larger heldout scans
with primes matching p23 modulo 9240 still showed shifting winners and no
predeclared production-grade filter.
```

Verdict:

```text
Ruled out as an ad hoc production filter. A symbolic exact pullback remains a
separate maybe.
```

### Generic X-Only Odd Division-Polynomial Factorization

Idea:

```text
Factor psi_ell(x) over Fp and use the x-coordinate factorization pattern as a
cheap trace-residue proxy.
```

Evidence:

```text
notes/x_division_factor_sign_obstruction_20260602.md
notes/ell5_division_factor_pattern_probe_20260602.md
notes/ell7_division_factor_pattern_probe_20260602.md

The roots of psi_ell(x) are (E[ell] - {0}) / {+/-1}. Replacing Frobenius M by
-M changes t to -t but induces the same action on x-coordinates, so x-only
factorization patterns are invariant under t -> -t mod ell.

p23 sign-closure ceilings:
  ell=3 target residues {0,2} -> all residues, max lift 1.00x
  ell=5 target residues {1,3} -> {1,2,3,4}, max lift 1.25x
  ell=7 target residues {5,6} -> {1,2,5,6}, max lift 1.75x

The empirical psi_5 and psi_7 probes reached exactly these coarse closures,
not exact two-residue filters.
```

Verdict:

```text
Ruled out as a generic production lane. Exact odd trace residues remain alive
only if the predicate cheaply breaks the t -> -t ambiguity, for example by
including a curve-vs-twist/root-squareclass bit.
```

### Direct X1(32) with generic degree-10 fiber root finding

Idea:

```text
Sample Sutherland's X1(32) model directly, then start the halving chain one
level higher.
```

Evidence:

```text
The generic Tate-to-Montgomery map now validates order-32 samples.

Largest holdout:
  X1(32) depth-12 first = 3/952 = 0.003151
  X1(16) depth-12 first = 170/100000 = 0.001700

The density lift is real, but the sampler requires degree-10 finite-field
root finding. The lift is roughly a constant-factor rung, not enough to pay
for an obviously slower generic sampler.

C root-existence cost-floor benchmark:
  notes/x1_32_c_rootbench_20260602.md

p23, 5000 random x-fibers:
  root-existence only = 1854.779 fibers/s = 0.001855 M fibers/s
  root_gcd_seconds_per_fiber = 5.368290e-04
  root_fibers = 3111/5000 = 0.6222

One active nonsplit worker runs around 0.108 M accepted trials/s, so root
existence alone is roughly 58x slower per single process before root
extraction, Tate/Montgomery conversion, filtering, and halving.
```

Verdict:

```text
Ruled out as the next p23 production shard. Keep as a calibrated research rung
only if a special sampler avoids generic degree-10 root finding.
```

### Generic growing prescribed torsion via X1(N)

Idea:

```text
Grow the prescribed torsion level N with p, so the X1(N) density gain becomes
an asymptotic improvement rather than a fixed constant factor.
```

Evidence:

```text
Fixed X1(N) buys only a fixed density factor. To improve the exponent, the
level must grow, say N ~= p^epsilon.

For X1(N):
  [SL2(Z) : Gamma1(N)] = N^2 * product_{ell|N}(1 - ell^-2)

For N = 2^a:
  [SL2(Z) : Gamma1(2^a)] = (3/4) * N^2

Abramovich's gonality lower bound is linear in modular-curve index, so
gonality(X1(2^a)) = Omega(N^2). Sutherland's optimized equation table shows
the same shape in the practical degrees:

  X1(16):  deg_y = 3
  X1(32):  deg_y = 10
  X1(64):  deg_y = 40
  X1(128): deg_y = 161

The density gain from forcing a rational point of order N is roughly N, while
generic one-parameter fiber/rootfinding cost grows like N^2.

Local cost gates agree:
  first X1(16)->X1(32) gate = production-negative
  X1(32) root-existence floor = ~58x slower than one active worker
  X1(24)->order48 = mathematically credible but production-negative
```

Backing note:

```text
notes/prescribed_torsion_scaling_barrier_20260602.md
```

Verdict:

```text
Ruled out as a generic asymptotic scaling route. Higher prescribed torsion
only remains alive through a non-generic tower section, trace-v2 selector, or
exact trace-residue/root-squareclass pullback that avoids generic X1(N)
rootfinding.
```

### X0(32) route as currently implemented

Idea:

```text
Use X0(32) as a cheaper cyclic-subgroup route toward order-32 structure.
```

Evidence:

```text
The route can construct validated order-32 x-states, but p23 depth holdouts
were negative:

combined:
  validated X0(32) order-32 states = 3424
  bounded all-branch depth-12 survivors = 0

The later large sampled BSGS curve-v2 scan also tested cheap X0(32)
Legendre/quartic labels as curve-level high-v2 proxies:

  notes/x0_32_bsgs_v2_feature_scan_20260602.md

Across three 3000-row matched-control nonsplit runs near p=260M:

  aggregate v2>=8  = 1108/9000 = 0.123111
  aggregate v2>=10 =  296/9000 = 0.032889

The v2 tail itself looked healthy, but cheap labels were weak. Half-stream
Legendre labels were usually around 1.0x-1.35x, and the best quartic v2>=10
bucket reshuffled across holdouts while capturing only about 45%-52% of
survivors.
```

Verdict:

```text
Demoted below nonsplit. Not a next production shard without a genuinely new
curve-level trace-v2 / volcano-altimeter selector or special tower section.
```

### Engineering micro-optimizations checked

Items:

```text
sqrt-existence classifier for the nonsplit y-character
-march=native build of the current kernel
```

Evidence:

```text
The sqrt-existence classifier was not faster than the pow-based character
test. -march=native gave no material speedup for this kernel.
```

Verdict:

```text
Ruled out as material changes.
```

### Non-number-theory search replacements

Ideas checked:

```text
Pollard/rho-style search inside one curve
fixed-A meet-in-the-middle as a global search
caching/hash reuse of random y values or halving radicands
more parallel shards on the same saturated machine
batch Legendre/sqrt without a real SIMD field kernel
```

Verdict:

```text
Ruled out as scaling improvements. They either attack the wrong bottleneck
or collapse to constant-factor engineering. The hard event remains choosing a
curve with one of the rare p23 target traces and enough 2-adic depth.
```

## Maybe / Research-Only

These are alive as mathematical directions but should not interrupt the current
operational path.

### Cheap tower section for X1(2^(m+1)) -> X1(2^m)

Question:

```text
Can we choose a better halving branch than first-branch without recursive
lookahead?
```

Why it remains alive:

```text
All-branch and lookahead diagnostics prove better branches exist. Static sign
labels and inverse gates failed, but the broader section-selection problem is
still one of the best paths toward a real scaling improvement.
```

Current boundary:

```text
notes/two_power_tower_section_obstruction_20260602.md
notes/x16_first_d_cover_sampler_audit_20260601.md
notes/two_adic_strategy_exploration.md
notes/x16_first_lift_cover_feature_scan_20260602.md
notes/x16_first_lift_cover_automorphism_audit_20260602.md
notes/x16_first_lift_quotient_feature_scan_20260602.md

The first X1(16)->X1(32) lift squareclass is
H(y) = (y - 1)*(y^2 - 2)*(y^2 - 2y + 2).

The witness cover z^2 = H(y) is squarefree of degree 5 with discriminant
-2048, hence genus 2 over p23. So a cheap tower section cannot be just a
rational parametrization of the current X1(16) y-line.

The explicit tower-section obstruction note sharpens this: because H(y) is
squarefree and not a square in Q(y), the first-lift cover has no rational
section over the y-line. A true scaling route would need sampler overhead
N^alpha with alpha < 1 as the prescribed level N=2^a grows. Generic X1(2^a)
sampling has alpha about 2, and the tested first-lift/quotient/norm features
do not supply the missing non-generic section.

The automorphism follow-up found that this genus-2 cover is not generic: its
branch set has the rational Mobius symmetry y -> (y - 2)/(y - 1), which lifts
over p23 using i^2=-1. The visible invariant relation is

  v^4 = u^2 * (u - 2 - 2i) * (u - 2 + 2i)^3.

This refines but does not reverse the production decision. Lifting back to the
original y,z stream still requires a quadratic condition, and the nonsplit
predicate is not absorbed. No cheap sampler or tower section follows from the
visible quotient.

A quotient-feature scan tested the resulting cheap Legendre/quartic buckets in

  u = (y^2 - 2)/(y - 1),
  u - 2 +/- 2i,
  (u - 2)^2 + 4.

Two 20k p23 holdouts showed best aggregate lift only about 1.15x at depth 12,
with about 29% survivor capture. Half-stream quotient features were about
1.05x. This rules out the visible quotient characters as the missing
tower-section label.

The direct first-d gate and skip-to-depth-5 variants were also demoted by
production-mode timing.

The latest first-lift-cover feature scan tested cheap sign-invariant norm
characters:

  chi(Norm(q(y) + z)) = chi(q(y)^2 - H(y))

for small linear and quadratic `q`. On a 50k p23 accepted-cover holdout, the
best depth-12 lift was only about 1.18x with about 59% survivor capture. The
20k holdouts also reshuffled their top features. This rules out low-degree
norm characters on the first-lift cover as the missing tower-section label.
```

Post-fallback caveat:

```text
notes/x16_nonsplit_branch_depth20_holdout_20260601.md
notes/x16_nonsplit_branch_collapse_proof_20260601.md
notes/x16_nonsplit_depth_equals_v2_audit_20260602.md
notes/x16_exact_v2_distribution_calibration_20260602.md
```

For the y-filtered nonsplit family now used by the active fallback, the
rational 2-Sylow subgroup is cyclic. If the X1(16) marked point has exact
order 16 and `v2(#E(Fp)) = m`, then its rational halving depth is exactly `m`.
Equivalently:

```text
nonsplit survival to depth d  <=>  v2(#E(Fp)) >= d
```

This is not just a depth-20 sampled fact. Full exact enumerations at p=3037
and p=10357 had zero nonsplit depth-vs-v2 mismatches. That demotes branch
selection as a production lever for the active nonsplit sampler, although the
broader tower-section question remains mathematically alive for all-X1,
split, or deeper/growing-torsion routes.

Exact p23-residue v2-distribution enumeration now includes `p=30517` and
`p=35317`:

```text
p=30517, rows=30344:
  nonsplit Pr[v2>=5]  = 0.507928
  nonsplit Pr[v2>=6]  = 0.248414
  nonsplit Pr[v2>=7]  = 0.117865
  nonsplit Pr[v2>=8]  = 0.070825
  nonsplit Pr[v2>=9]  = 0.048626
  nonsplit Pr[v2>=10] = 0.033827

p=35317, rows=35144:
  nonsplit Pr[v2>=5]  = 0.495939
  nonsplit Pr[v2>=6]  = 0.243231
  nonsplit Pr[v2>=7]  = 0.113718
  nonsplit Pr[v2>=8]  = 0.060921
  nonsplit Pr[v2>=9]  = 0.027076
  nonsplit Pr[v2>=10] = 0.000000
```

Across `p=3037,10357,21157,30517,35317`, nonsplit is close to the simple
geometric tail at depths 5-7. This mildly supports the active model, but the
visible higher-depth tail is p-specific and does not prove the p23 depth-39
tail. The p=35317 row is a useful caution against overestimating L from shallow
or favorable small-prime calibrations.

Promotion test:

```text
Find a non-generic 2-power model, biased/probabilistic section, or cheap
2-adic orientation label that captures deeper liftability at <=1.2x current
sampler cost, validated on paired p23 survivor/sec holdouts.
```

### Symbolic X1(16) trace-residue pullback

Question:

```text
Can the trace modulo ell classifier be pulled back to a cheap exact condition
in the X1(16) parameter y?
```

Why it remains alive:

```text
The two target traces differ by 2^39, so they are distinct modulo every odd
prime ell. An ideal exact trace-residue filter modulo ell keeps 2/ell classes.
Through ell = 43, the ideal cumulative survival is about 1.25e-12, comparable
to the two-target trace mass.
```

Promotion test:

```text
Find an exact low-degree y-condition for ell = 3, 5, 7, or 11 that includes
the curve-vs-twist/root-squareclass bit, with predictable coverage/capture and
cheaper cost than the halving work it avoids. X-only factorization patterns
are structurally capped by the t -> -t sign obstruction.
```

### C-level X1(32) or special 2-power parametrization

Question:

```text
Can order-32 sampling be made nearly as cheap as the current X1(16) quadratic
sampler?
```

Why it remains alive:

```text
The order-32 map is now validated, and X1(32) shows the expected density lift.
The generic degree-10 root-finding route is now cost-negative, and the generic
growing-X1(N) route has the wrong asymptotic cost shape. The remaining live
version is a special 2-power parametrization or tower section whose sampling
cost is close to the current X1(16) quadratic sampler.
```

Promotion test:

```text
A non-generic sampler avoids the degree-10 root-gcd floor and then beats
y-filtered nonsplit X1(16) on paired p23 survivor/sec, not merely accepted
trial survival.
```

### Improved X0(32) with curve-level trace-v2 filtering

Question:

```text
Can X0(32) be filtered by a cheap high-2-adic trace/volcano-altimeter predicate
so sampled cyclic subgroups land on curves with enough depth?
```

Why it remains alive:

```text
Trace compatibility is not ruled out, and X0(32) constructs valid order-32
states. The refined relevant-v2 probe shows that, in the nonsplit/cyclic case,
X0(32) state depth equals curve-level v2(#E) on the tested small primes.
```

What is now ruled out:

```text
More cheap nonsplit x-state squareclasses. Beyond chi(A^2-4)=-1, the missing
selector is curve-level trace-v2, not a separate order-32 state orientation
label.

Cheap X0(32) parameter Legendre/quartic labels as curve-v2 proxies were also
tested at larger sampled exact-trace controls:

  notes/x0_32_bsgs_v2_feature_scan_20260602.md

They showed only noisy constant-factor stratification, not a stable selector.

Volcano/pairing literature was audited in:
  notes/volcano_pairing_selector_audit_20260602.md

It explains the observed cyclic/non-cyclic 2-Sylow behavior but does not give
a cheap p23 `v2(#E)` label by itself.

Trace-v2 prefilter cost-floor audit:
  notes/trace_v2_prefilter_cost_floor_20260602.md

On 500k p23 nonsplit samples to depth 16, the existing early-abort halving
test used only:

  per_sample first_d_sqrt_calls = 2.005
  per_sample first_w_sqrt_calls = 1.508

So a trace-v2 prefilter is not racing against 35 halvings on every candidate;
it is racing against a couple of square-root tests on average. This rules out
generic Schoof/SEA trace mod 2^m, generic 2-power division-polynomial
factorization, generic volcano walks, and p-adic/canonical-lift point counting
as production prefilters.
```

Promotion test:

```text
Find a p23-cheap predicate that predicts high v2(p+1-t), costs about one
Legendre/square-root-level operation per candidate, then shows depth-12/14
survivor/sec above y-filtered nonsplit X1(16) on a paired p23 holdout.
```

### 2-isogeny volcano / orientation labels

Question:

```text
Can volcano level or orientation predict halving branch survival cheaply?
```

Why it remains alive:

```text
Volcano theory is structurally relevant to 2-adic depth. It cannot discover
trace by itself because isogenies preserve trace. After the relevant-v2 probe,
its only plausible role is a cheap curve-level altitude/trace-v2 proxy, not a
new nonsplit branch label.

Pairing-the-volcano style orientation can distinguish isogeny directions, but
the p23 split all-branch audit already shows split below nonsplit on the useful
marked-point calibration depths. Orientation would need to change marked-point
survival, not merely reduce all-branch navigation cost.
```

Promotion test:

```text
Exact small-prime volcano labels predict marked-point survival, the winning
labels have a p23-cheap proxy, and a paired p23 survivor/sec benchmark beats
y-filtered nonsplit X1(16).
```

### Conditioned trace model for the X1(16) family

Question:

```text
Is the X1(16) family biased toward or away from the two p23 target traces?
```

Why it remains alive:

```text
This could refine run-length expectations and explain a long miss, even if it
does not directly speed the search.
```

Current evidence:

```text
notes/x16_conditioned_trace_calibration_20260602.md

Small-prime trace-only calibration found all-X1 target trace rates above the
simple 16*trace_mass heuristic. Exact small p23-residue enumerations found
positive nonsplit target-trace mass, but split remains enriched. The p23-residue
exact checks currently give nonsplit L_trace around 0.5-1.3 and split around
1.6-3.8.

The split enrichment is structurally explained by full rational 2-torsion:
X1(16) already forces `v2(#E)>=4`, and split curves have an additional
independent rational order-2 point, so `v2(#E)>=5` automatically.

Operational follow-up:
notes/x16_split_trace_vs_halving_audit_20260602 found that split trace
enrichment does not translate into better marked-point survivor throughput
with first-branch or all-branch halving at p23.

Cheap feature follow-up:
notes/x16_nonsplit_trace_feature_holdout_20260602 tested low-degree y-feature
Legendre filters inside the nonsplit substream. Exact odd trace residues still
look stackable, but the cheap y-feature approximations were weak and unstable
across p23-residue calibration primes. Do not add a trace-feature sidecar to
production.

Pair-label follow-up:
notes/x16_closed_form_pair_scan_20260602 extended the p23 nonsplit diagnostic
to pairwise low-degree X1(16) y/A Legendre labels against actual depth-16
survival. The first 1M seed produced a tempting quarter-density winner,
`chi(A^2 - 3)=-1` and `chi(y^2 - 3y + 1)=+1`, with 1.431x conditional lift,
but the same pair collapsed to 0.688x on an independent 1M holdout. The
two-seed aggregate best genuine pre-halving pair had only 1.293x lift and
captured 32.4% of depth-16 survivors. Since this costs two extra character
tests while the active predicate already early-aborts after only about two
first-branch half attempts per candidate, pairwise fitted labels are closed
for immediate production.

Joint v2/residue follow-up:
notes/x16_exact_v2_trace_residue_stack_20260602 added exact small-prime rows
conditioned simultaneously on split class, v2(#E), and p23 odd target residues.
At shallow depth, odd residues still stack with nonsplit: in the p=61837 row,
nonsplit v2>=5 through ell=7 was 1184/15568 = 0.076053, essentially the
independent ideal 0.076190. At deeper visible depths, the small-prime trace
lattice dominates: nonsplit v2>=9 in that same row had 864/864 through ell=11.
This keeps exact trace-residue pullbacks alive as a stackable selector if the
cost collapses, but it rules out using small-prime joint rows as a tight p23 L
prior.

p23 trace-lattice follow-up:
notes/p23_trace_lattice_model_20260602 exactly enumerated the p23 Hasse trace
lattice under `v2(p+1-t)>=d`. At p23 depths d=16-20, odd residue cuts through
ell=17/19 match the independent ideals nearly exactly. At d=39, there are only
the two final target traces, so every tested odd residue condition is automatic.
This sharply defines the remaining trace-residue opportunity: it must be an
early, exact, cheap filter. Independent odd-prime multiplication at final depth
is ruled out.

Break-even follow-up:
notes/p23_trace_filter_break_even_20260602 turned that lattice result into a
microsecond cost bound. An exact ell=3 sidecar keeps q=2/3, so it must cost
under about 3.09 us on the active kernel and 2.84 us on the direct-y follow-on.
The measured exact ell=3 predicate costs about 72 us per nonsplit candidate.
The specialized quartic pow-only slice costs about 65.4 us per p23 curve, so
the exponentiation itself is the cost floor.
Even a hypothetical combined ell=3,5,7 filter would need to cost below about
8 us, still far below the measured cost of ell=3 alone.

Midpoint probability follow-up:
notes/p23_midpoint_probability_update_20260602 records the active nonsplit
midpoint miss at 25.041B accepted trials. Under the main prior and lift=1.5,
conditional hit probability from now is 0.2483 by 35B, 0.4311 by 45B, and
0.5037 by 50B. Under a wider pessimistic prior L~Uniform(0.1,1.2), the same
quantities are 0.1601, 0.2864, and 0.3396. This updates against optimistic L
without changing the action: keep waiting until hit or clean exhaustion.
```

Promotion test:

```text
A formal conditioned-family trace calculation or robust small-prime model that
predicts the active p23 hazard better than the current equidistribution model.
```

### Post-hit certificate minimization

Question:

```text
After a verified p23 PASS, can the short-certificate repo find a smaller or
cleaner certificate for the same p?
```

Why it remains alive:

```text
It could improve the final artifact. It does not help find the first hit.
```

Promotion test:

```text
Only begin after an independently verified p23 triple exists.
```

### Kernel constant-factor engineering

Question:

```text
Can the current C kernel be made materially faster without changing the search
distribution?
```

Why it remains alive:

```text
A read-only algorithmic audit flagged two plausible hot-path ideas:

1. batch X1 sampler inversions across the two quadratic roots from the same y;
2. keep more X1/halving algebra in Montgomery-domain form with fixed p23
   exponent chains or sliding-window exponentiation.

The direct X1(16) y-map audit found a more concrete simplification:

  A(y) =
    (y^8 - 8y^7 + 24y^6 - 32y^5 + 8y^4
     + 32y^3 - 48y^2 + 32y - 8)
    / (4*(y - 1)^4)

  xP = x / (x - y)

An experimental `pomerance_fastformula` binary preserved paired branchstats
survivor counts and showed rough under-load speedups around 1.09x-1.14x.

Fresh direct-y readiness:
  notes/directy_next_readiness_20260602.md
  old active binary = 2.0M in 19.25s, rate ~= 0.1039 M/s
  direct-y binary   = 2.0M in 17.02s, rate ~= 0.1175 M/s
  aggregate speedup ~= 1.131x

The post-miss next-action path now routes a clean exhausted nonsplit shard to:

  scripts/p23_launch_x16halvenonsplit_directy_next.sh

These are constant-factor engineering bets, not mathematical scaling wins.
```

Promotion test:

```text
Do not hot-swap the active run. If it cleanly misses, use the guarded direct-y
nonsplit follow-on that rebuilds and records the binary hash before launch.
```

## Not Yet Tested Decisively

```text
1. Final outcome of the active y-filtered nonsplit X1(16) fallback shard.

2. Whether the p23 nonsplit X1(16) high-v2 trace tail seen at depth 12-16
   extrapolates to the true target depth 39. The branch mechanism itself is
   now exact: nonsplit marked depth equals `v2(#E)`. Exact small-prime
   p23-residue v2 distributions now include p=35317 and support the nonsplit
   tail at depths 5-8, but depths above that are p-specific and remain too
   shallow to prove depth 39.

3. Symbolic exact elimination/pullback of SEA trace residues to the X1(16)
   y-parameter. Low-degree y-cubic and nonsplit-conditioned y-Legendre feature
   scans are now negative, and the direct `G_y(T)` quotient-ring predicate is
   exact but far too slow. The ell=3 squareclass bit is now identified as the
   Frobenius eigenvalue/sign on a rational 3-torsion line, with no mixed-root
   squareclass shortcut. The only remaining version would need a qualitatively
   new formula for this eigenvalue character on the X1(16) parameter.

4. Exact small-prime 2-isogeny volcano/orientation labels, plus a p23-cheap
   proxy feature. Cheap Legendre/quartic X0(32) parameter characters were
   tested as curve-v2 proxies and were not stable enough for production.
   Generic trace-v2 computation is now cost-ruled-out as a prefilter; only a
   mathematically derived closed-form cheap label remains alive. Fitted
   one- and two-character low-degree labels have now been tested and rejected
   for production.

5. A compressed tower-section, child-mass, or split-component orientation
   feature beyond static sign labels, inverse gates, quartic flags, cubic
   filters, simple y-characters, low-degree first-lift-cover norm characters,
   visible first-lift quotient characters, rational first-lift sections, and
   explicit split 2-torsion translation.

6. Post-hit low-product certificate minimization for this p.

7. X0(32) with an additional liftability/orientation filter and a C-level
   throughput test.

8. A formal conditioned-trace probability model for the active X1(16) family.
    A first trace-only small-prime calibration is recorded, but a robust
    filter-first or verifier-hit model remains open. Exact joint v2/residue
    rows now show the model must treat the trace lattice directly rather than
    multiplying independent odd-prime residue factors at high visible v2.
    A new FFT character-convolution trace helper now gives exact larger
    p23-residue calibration rows through p=10000357, correcting the old
    sampled zero-hit impression for nonsplit while preserving the
    split-enrichment and finite-lattice cautions. The same fast trace method
    now confirms that p23 odd residues stack approximately independently early
    in exact nonsplit X1(16) rows. A sampled Hasse-interval BSGS trace helper
    extends this to three 30k-row nonsplit samples at the first larger matched
    controls near p=260M; aggregate through ell=7 is 7285/90000 = 0.080944
    versus independent ideal 0.076190. The remaining obstacles are exact
    predicate cost and, for exhaustive larger matched controls, a
    memory-frugal exact trace counter.

    The latest conditioned-tail model update is:

      notes/p23_conditioned_tail_model_update_30p9B_20260602.md

    It adds a rollup helper:

      scripts/x16_nonsplit_tail_rollup.py

    and shows that the nonsplit v2 tail is almost exactly geometric through
    visible depths in both five exact FFT rows and three 30k-row BSGS matched
    controls. In the 90k BSGS aggregate near p=260M, ratios to the geometric
    baseline are 1.003, 0.998, 0.994, 1.001, 0.997 at depths 5 through 9 and
    remain near 1 through depth 15. This strengthens the order-1 basis for L,
    while the live no-hit evidence through about 30.9B accepted nonsplit
    trials pushes the p23-specific posterior downward.

9. A true sub-sqrt scaling primitive. Fixed X1(16) plus nonsplit conditioning
   is a strong p23 constant-factor search improvement, but not an asymptotic
   scaling theorem. The remaining scaling candidates are a special 2-power
   tower section, a scalar-time trace-v2 label, or an exact cheap
   trace-residue/root-squareclass pullback.
```

## Operational Rules Going Forward

Use the decision wrapper:

```bash
./scripts/p23_next_action.sh
```

Interpretation:

```text
decision=verify_hit
  run ./scripts/p23_next_action.sh --execute
  then inspect the finalized verification artifact

decision=keep_waiting
  do not touch workers

decision=launch_nonsplit_next_shard
  run ./scripts/p23_next_action.sh --execute
  this would launch the next guarded nonsplit extension after the active
  nonsplit shard has ended cleanly

decision=manual_review
  inspect liveness and latest progress before changing anything
```

## Detailed Backing Notes

```text
notes/p23_research_synthesis_20260601.md
notes/p23_candidate_decision_matrix.md
notes/p23_mathematical_shortlist.md
notes/p23_literature_map_20260601.md
notes/p23_operational_runbook.md
notes/p23_operational_timeline_20260601.md
notes/p23_trace_residue_ceiling.md
notes/x16_split_nonsplit_pullback_proof.md
notes/danger3_short_certificate_transfer_recap_20260601.md
notes/short_certificate_repo_transfer.md
notes/ell3_quartic_shortcut_probe_20260601.md
notes/ell3_y_cubic_pullback_probe_20260601.md
notes/ell3_direct_y_quartic_benchmark_20260602.md
notes/x16_direct_y_map_optimization_20260601.md
notes/x16_direct_y_map_promotion_checklist.md
notes/subagent_findings_20260601.md
notes/x1_32_sampler_design.md
notes/prescribed_torsion_scaling_barrier_20260602.md
notes/x0_32_route_audit.md
notes/x0_32_relevant_v2_probe_20260602.md
notes/x0_32_curve_v2_feature_scan_20260602.md
notes/x16_exact_v2_distribution_calibration_20260602.md
notes/trace_v2_prefilter_cost_floor_20260602.md
notes/sea_small_prime_filter_design.md
notes/cm_exact_trace_audit.md
notes/x16_lookahead_branch_stats.md
notes/x16_branch_feature_stats.md
notes/x16_inverse_gate_branch_stats.md
notes/x16_quartic_sqrt_flag_stats.md
notes/x16_closed_form_pair_scan_20260602.md
notes/x16_split_torsion_translate_audit_20260602.md
notes/x16_exact_v2_trace_residue_stack_20260602.md
notes/p23_trace_lattice_model_20260602.md
notes/p23_trace_filter_break_even_20260602.md
notes/p23_midpoint_probability_update_20260602.md
notes/p23_true_subsqrt_scaling_frontier_20260602.md
notes/p23_probability_update_27B_20260602.md
notes/x16_first_lift_cover_feature_scan_20260602.md
notes/x16_fast_trace_convolution_calibration_20260602.md
notes/x16_fast_trace_residue_stack_20260602.md
notes/x16_order32_lift_feature_scan.md
notes/ell3_quartic_pow_cost_floor_20260602.md
notes/x16_first_lift_cover_automorphism_audit_20260602.md
notes/x16_first_lift_quotient_feature_scan_20260602.md
```
