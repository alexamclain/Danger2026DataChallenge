# p23 Pomerance Experiment and Result

Date: 2026-06-02 PDT

Target:

```text
p = 100000000000000000000117 = 10^23 + 117
sqrt_floor(p) = 316227766016
k = 39
```

This note is the full local write-up of the p23 campaign: what mathematical
idea was tested, how the operational test was run, what failed, what passed,
and how strong the final result is.

## Executive Result

Final Pomerance triple:

```text
100000000000000000000117 24163028207499560363686 64911014007772963770218
```

Equivalently:

```text
p  = 100000000000000000000117
A  = 24163028207499560363686
x0 = 64911014007772963770218
```

Successful route:

```text
Sutherland X1(16) prescribed 2-power torsion
+ y-level nonsplit Montgomery discriminant filtering
+ first-branch halving in the cyclic nonsplit rational 2-Sylow case
```

Hit source:

```text
run_dir = runs/p23_x16halvenonsplit_20260601_201436
worker  = worker03.log
mode    = x16halvenonsplit
binary  = pomerance_nonsplit_yfilter
```

Worker hit line:

```text
Found after 28878.93s (~3104658850 X1(16) curves)
Verified: PASS  (28878.93s)
```

Performance against the sqrt-scale accepted-trial yardstick:

```text
final-shard aggregate-at-hit trials = 31.046588500B
sqrt_floor(p)                       = 316.227766016B
fraction of sqrt_floor(p)           = 0.098177933
speedup versus sqrt-floor trials     = 10.1856x
```

If the earlier 50B all-X1 miss is charged as part of the discovery campaign:

```text
first all-X1 shard trials            = 50.000000000B
final nonsplit shard at hit          = 31.046588500B
total campaign accepted trials       = 81.046588500B
fraction of sqrt_floor(p)            = 0.256291816
speedup versus sqrt-floor trials     = 3.9018x
```

So the final technique itself landed at about 9.82 percent of `sqrt(p)`, and
the whole bounded p23 discovery campaign still landed at about 25.63 percent
of `sqrt(p)`.

## Problem And Success Criterion

The DANGER3/Pomerance task is to find a triple `(p, A, x0)` that passes the
challenge verifier for the target prime `p`. Operationally, the verifier treats
`A` as a Montgomery curve parameter and checks a deterministic Montgomery
doubling trajectory from `x0`. For this target, the relevant depth is `k = 39`.

The practical baseline was the generic `sqrt(p)` search scale:

```text
sqrt(p) ~= 316.228B accepted candidates
```

The requested standard was not merely "find any certificate", but find one
substantially faster than the local sqrt-scale state-of-the-art yardstick.

The pass condition for the campaign was:

```text
1. A worker emits a candidate triple and built-in `Verified: PASS`.
2. The triple passes an independent Python Montgomery replay.
3. The target p passes an independent primality check.
4. Andrew Sutherland's DANGER3 `vpp.py` returns True.
5. The hit is finalized into persistent local artifacts.
6. A Lean certificate artifact is generated if practical.
```

All of those checks passed.

## Literature Inputs

The production idea combines three pieces.

First, use prescribed torsion. Sutherland's construction of elliptic curves
over finite fields with prescribed torsion gives explicit `X1(N)` families.
We used the optimized `X1(16)` model, then mapped samples into Montgomery form.
Starting with a known order-16 point shifts the search from generic 2-Sylow
projection toward curves already carrying meaningful 2-power structure.

Second, use successive halving. The Miret-Moreno-Rio-Valls style 2-Sylow
algorithmic perspective says that once a rational 2-power point is known, one
can test deeper 2-adic divisibility by trying rational halvings.

Third, transfer the split/nonsplit discriminant feature from the sibling
`danger3-short-certificate-experiments` repo. On a Montgomery curve,

```text
split    iff chi(A^2 - 4) =  1
nonsplit iff chi(A^2 - 4) = -1
```

For the local `X1(16)` sampler this was pulled back to the y-line:

```text
chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2)).
```

That identity allowed the production binary to reject the split side before
constructing `A`.

The sign choice is important. The external short-certificate experiments used
the split side for low-product short certificates. The p23 high-depth halving
search used the nonsplit side instead, because nonsplit Montgomery curves have
cyclic rational 2-Sylow subgroup. In that cyclic setting, the marked
order-16 point's halving depth tracks the curve's rational 2-adic depth cleanly.

## Experiment Design

The campaign tested the following concrete hypothesis:

```text
Conditioning on X1(16), then restricting to the nonsplit Montgomery
discriminant class, increases p23 high-depth hit hazard enough to overcome
the added sampler/filter cost and beat sqrt(p)-scale search by a large
constant factor.
```

Sub-hypotheses:

```text
H1. X1(16) prescribed torsion materially improves the target trace density.
H2. The y-level nonsplit predicate is exactly concordant with chi(A^2 - 4).
H3. Nonsplit cyclic rational 2-Sylow makes first-branch halving complete:
    full branch search cannot find a deeper path missed by first branch.
H4. The nonsplit tail has enough p23 liftability that a 50B bounded shard is
    a credible production test.
```

Operational structure:

```text
workers                 = 10 independent single-thread processes
budget per worker       = 5,000,000,000 accepted trials
aggregate shard budget  = 50,000,000,000 accepted trials
stopping rule           = first Verified: PASS, or clean exhaustion
finalization            = scripts/finalize_pomerance_hit.sh
audit gate              = scripts/p23_next_action.sh
```

The first production shard tested plain all-X1(16) first-branch halving. It
missed cleanly at 50B accepted trials. The second production shard tested the
y-filtered nonsplit version. It hit before reaching 50B.

## Controls And Calibration

The mathematical transfer and branch simplification were not assumed blindly.
They were checked before and during production.

Discriminant pullback:

```text
note   = notes/x16_split_nonsplit_pullback_proof.md
result = chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2))
```

Numeric concordance audit:

```text
command          = ./scripts/audit_short_certificate_transfer.py --samples 512
accepted_y       = 512
roots_checked    = 1024
mismatches       = 0
status           = PASS
```

Final operational audit repeated a smaller concordance check:

```text
samples_requested = 64
accepted_y        = 64
roots_checked     = 128
mismatches        = 0
status            = PASS
```

Nonsplit branch-collapse proof:

```text
note   = notes/x16_nonsplit_branch_collapse_proof_20260601.md
claim  = in the nonsplit family, first-branch survival equals all-branch survival
reason = rational 2-Sylow is cyclic
```

This justified using cheap first-branch halving in the nonsplit production
run rather than paying for full all-branch backtracking.

## Production Runs

### Run 1: all-X1(16) first-branch halving

```text
run_dir        = runs/p23_x16halve_20260601_110154
mode           = x16halve
workers        = 10
budget         = 5B trials per worker, 50B aggregate
result         = clean miss
latest trials  = 50.000B aggregate
worker rate    = ~0.151M trials/s
aggregate rate = ~1.51M trials/s
elapsed        = ~9.19h
```

Each worker ended with:

```text
Not found in ~33070-33085s. Re-run or increase budget.
```

Interpretation:

```text
The all-X1(16) route was not falsified as a mathematical idea, but its 50B miss
made the conditioned nonsplit shard the better next production test.
```

### Run 2: y-filtered nonsplit X1(16) first-branch halving

```text
run_dir        = runs/p23_x16halvenonsplit_20260601_201436
mode           = x16halvenonsplit
workers        = 10
budget         = 5B trials per worker, 50B aggregate
result         = verified hit
worker         = worker03.log
worker trials  = 3,104,658,850
elapsed        = 28,878.93s = 8.0219h
worker rate    = ~0.108M accepted trials/s
aggregate rate = ~1.079M accepted trials/s
```

Run metadata:

```text
seed_base = 7000000
seed_step = 104729
binary_source = pomerance_nonsplit_yfilter
binary_sha256 = 33c9120f7ab39258b4a5da0b1b1cbd13ebe16d15e43409f7a4fe0c1339b271c1
```

The final worker-local hit count was:

```text
worker03 local accepted curves = 3,104,658,850
```

The reconstructed aggregate-at-hit count uses the fact that all ten workers
were running in lockstep at essentially the same rate:

```text
10 * 3,104,658,850 = 31,046,588,500 accepted trials
```

After finalization and process shutdown latency, the latest tail lines summed
to:

```text
aggregate_latest_trials = 31.110B
```

The smaller reconstructed number is the better estimate of the first PASS
wall-clock budget; the later tail sum is the conservative "logs after shutdown"
budget.

## Verification Artifacts

Final artifact directory:

```text
runs/p23_x16halvenonsplit_20260601_201436/hit-100000000000000000000117-worker03
```

Files:

```text
triple.txt
verification.txt
worker.log
worker-tail.txt
pomerance_100000000000000000000117.lean
README.md
```

Finalizer command:

```bash
./scripts/p23_next_action.sh --execute
```

The next-action gate chose:

```text
decision=verify_hit
next_command=scripts/finalize_pomerance_hit.sh --log runs/p23_x16halvenonsplit_20260601_201436/worker03.log
```

Independent replay transcript:

```text
sqrt_floor = 316227766016
sqrt_sqrt_floor = 562341
bound = 316228890699
k = 39
zero_steps = [39]
final_X = 44839297471447980302367
final_Z = 0
gcd_Zprev_p = 1
independent_replay_pass = True
```

Additional verifier checks:

```text
openssl_prime returncode = 0
openssl output = 100000000000000000000117 is prime

danger3_vpp returncode = 0
danger3_vpp output = True

verification_status = PASS
```

Lean artifact:

```text
runs/p23_x16halvenonsplit_20260601_201436/hit-100000000000000000000117-worker03/pomerance_100000000000000000000117.lean
```

The generated Lean theorem is:

```text
theorem pomerance_100000000000000000000117 :
  IsPomeranceTriple 100000000000000000000117 24163028207499560363686 64911014007772963770218
```

## What Was Ruled Out

These are ruled out as immediate p23 production routes under the evidence
collected here. Some remain useful as diagnostics or post-hit minimization.

```text
CM exact-trace construction:
  no hidden small-class shortcut; target discriminants have huge fundamental
  parts and conductor 4.

direct low-product short-certificate frontier:
  useful for post-hit compression, not a p23 first-hit method; expected
  checks are far beyond sqrt(p) for one first hit.

split-first transfer from the short-certificate repo:
  the discriminant axis transfers, but the sign reverses for p23 high-depth
  halving; nonsplit is the useful production class.

generic higher X1(2^n), especially X1(32):
  generic rootfinding/fiber cost grows too fast; local p23 rootbench was
  roughly 58x slower than the active nonsplit worker before full conversion.

generic exact odd trace-residue filters / SEA-style filters:
  mathematically attractive, but measured exact ell=3 filtering was more than
  an order of magnitude above the break-even cost.

full all-branch halving inside nonsplit:
  cyclic rational 2-Sylow makes first branch complete; all-branch search adds
  cost without improving nonsplit survival.

simple residue-class and quartic y-feature gates:
  tested variants did not retain enough deep-survival signal per unit cost.
```

## What Remains Maybe

The result is a strong fixed-p win, but it is not an asymptotic sub-sqrt proof.
Fixed `X1(16)` plus a fixed nonsplit predicate improves the constant, not the
exponent.

Plausible next mathematical directions:

```text
special 2-power tower section:
  grow beyond X1(16) without paying generic X1(N) degree/gonality cost.

cheaper trace-residue information:
  odd-prime trace filters would be valuable if implemented below the measured
  break-even cost.

faster nonsplit sampling kernel:
  the final shard paid a raw throughput cost versus all-X1(16), but the
  hazard improvement won. A direct-y or lower-overhead nonsplit kernel could
  improve the same mathematical route.

post-hit certificate minimization:
  the sibling short-certificate repo is better suited after a valid triple is
  known, when the task becomes shortening or ranking certificates rather than
  finding the first p23 hit.

replication on nearby targets:
  needed to estimate whether the observed 10.2x final-shard improvement is
  typical for this conditioning or partly favorable fixed-target variance.
```

## Interpretation

The mathematical truth that mattered operationally was not a single exotic
black-box theorem. It was a clean combination:

```text
1. X1(16) cheaply prescribes a rational order-16 point.
2. The Montgomery split/nonsplit class pulls back to a cheap y-character.
3. The p23 high-depth target is better aligned with the nonsplit/cyclic
   rational 2-Sylow case.
4. In that cyclic nonsplit case, first-branch halving is complete for survival.
```

That combination converted the search from generic sqrt-scale behavior into a
much smaller fixed-p hazard search. The final p23 certificate was found at
about `31.05B` aggregate accepted trials in the successful shard, versus
`316.23B` for the sqrt-floor yardstick.

The honest conclusion:

```text
This is a substantial fixed-prime win over sqrt(p)-scale search.
It is not, by itself, a proof of asymptotically sub-sqrt scaling.
```

## Reproducibility Commands

Audit the current final state:

```bash
./scripts/p23_operational_audit.sh --no-probability --transfer-samples 64
```

Inspect the next-action decision:

```bash
./scripts/p23_next_action.sh
```

Re-run independent verification from the successful worker log:

```bash
./scripts/verify_pomerance_triple.py \
  --log runs/p23_x16halvenonsplit_20260601_201436/worker03.log
```

Inspect the finalized verification transcript:

```bash
sed -n '1,120p' \
  runs/p23_x16halvenonsplit_20260601_201436/hit-100000000000000000000117-worker03/verification.txt
```

This public ledger preserves the curated result and research artifacts. Full
raw worker logs and transient local scratch files remain outside the commit.
