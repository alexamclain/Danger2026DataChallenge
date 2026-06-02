# p23 X1(16) Halving Experiment

Date: 2026-06-01

Target:

```text
p = 100000000000000000000117 = 10^23 + 117
sqrt(p) floor = 316227766016
k = 39
2^k = 549755813888
```

Hasse-compatible group orders with the required 2-adic divisibility:

```text
N =  99999999999678036836352, trace =  321963163766, v2(N) = 40, odd_part =  90949470177
N = 100000000000227792650240, trace = -227792650122, v2(N) = 39, odd_part = 181898940355
```

## Question

Can prescribed 2-power torsion shrink the effective search space for a Pomerance triple, compared with the generic 2-Sylow projection search?

The current test is not a proof of sub-sqrt asymptotics. It tests whether a fixed prescribed-torsion construction gives a meaningful constant-factor improvement at p23 scale.

## Mathematical Inputs

1. Sutherland's modular-curve construction gives explicit equations for curves with prescribed torsion over finite fields. We use the optimized X1(16) equation and map into a Tate normal form, then into a Montgomery model.

2. Miret-Moreno-Rio-Valls style 2-Sylow computation uses successive halving to climb from a known 2-power torsion point toward maximal 2-power order.

3. The DANGER3 verifier remains the acceptance oracle: any candidate must satisfy exactly the k-th Montgomery doubling condition for p.

References:

- Andrew V. Sutherland, "Constructing elliptic curves over finite fields with prescribed torsion", Math. Comp. 81 (2012), 1131-1147: https://arxiv.org/abs/0811.0296
- Sutherland X1(N) equation tables: https://math.mit.edu/~drew/X1_altcurves.html
- J. Miret, R. Moreno, A. Rio, M. Valls, "Determining the 2-Sylow subgroup of an elliptic curve over a finite field", Math. Comp. 74 (2005), 411-427: https://doi.org/10.1090/S0025-5718-04-01640-0
- DANGER3 challenge/verifier: https://github.com/AndrewVSutherland/DANGER3

## Current Implementation

Mode:

```text
x16halve
```

Pipeline per trial:

1. Sample an Fp-point on Sutherland's X1(16) model.
2. Map it to raw X1(16) coordinates `(r,s)`.
3. Build the Tate normal form with a point of order 16.
4. Convert to a Montgomery model with the known order-16 point as input.
5. Try successive halving from order 16 to order 2^39 using a fast first rational branch.
6. If a candidate x-coordinate survives to depth 39, verify with the built-in Montgomery doubling verifier.

The source also contains an `x16halvefull` mode for full rational-half backtracking. It is cleaner mathematically but much slower in the current implementation, so it is not used for the production run.

## Active Run

Run directory:

```text
runs/p23_x16halve_20260601_110154
```

Workers:

```text
10 independent single-thread processes
5,000,000,000 trials per worker
50,000,000,000 aggregate trial budget
```

Observed steady-state rate:

```text
~0.153M trials/sec per worker
~1.53M trials/sec aggregate
```

Important monitoring note: the supervisor's `observed_progress_trials` field is inflated because it sums every progress line ever printed. The reliable progress number is the latest `trials=` value in each worker log, summed across workers.

Use:

```bash
./scripts/p23_status.sh
```

As of 2026-06-01, the status helper also prints:

```text
aggregate_rate_Mps
eta_to_35B_hours
eta_to_45B_hours
eta_to_50B_hours
model_no_hit_prob_L1.00
model_no_hit_prob_L0.80
model_no_hit_prob_L0.67
```

The model probabilities use the local heuristic `E[trials] ~= 34.6B / L`, so they are interpretation aids rather than stopping rules.

or:

```bash
RUN=$(cat /tmp/p23_run_dir.txt)
while true; do
  clear
  date
  grep -H "Verified: PASS" "$RUN"/worker*.log 2>/dev/null
  for f in "$RUN"/worker*.log; do
    printf "%s: " "$(basename "$f")"
    tail -n 1 "$f"
  done
  sleep 10
done
```

Optional verification watcher:

```bash
scripts/p23_watch_and_verify.sh --run-dir runs/p23_x16halve_20260601_110154
```

It waits for the first worker `Verified: PASS` line, runs `scripts/verify_pomerance_triple.py --log ...`, and writes a verification transcript into the run directory. It was validated on `results/p22/p22-worker07-tail.txt`.

## Probability Model

Local research note added during the active run on 2026-06-01.

Using the discrete Sato-Tate trace mass

```text
Pr(trace = t) ~= sqrt(1 - t^2/(4p)) / (pi * sqrt(p)),
```

the two admissible traces have approximate unconditioned masses:

```text
t =  321963163766: 8.66e-13
t = -227792650122: 9.39e-13
combined:          1.805e-12
```

X1(16) samples curves with a rational point of order 16. The working heuristic is therefore:

```text
hazard_X1 ~= 16 * 1.805e-12 * L
           ~= 2.889e-11 * L
```

where `L` is the liftability or branch-survival factor from the known order-16 point up to the required `2^39` or `2^40` 2-Sylow level.

This gives the following expected aggregate trial counts:

```text
L = 1.00 -> 34.6B
L = 0.90 -> 38.5B
L = 0.80 -> 43.3B
L = 0.75 -> 46.2B
L = 0.67 -> 51.7B
L = 0.50 -> 69.2B
```

Interpretation: a hit in the 35-45B range is exactly what this model predicts if `L` is about 0.8-1.0. A miss at 50B is not enough to falsify the technique, but a miss at 100B would be strong evidence that `L` is much lower than hoped or that the X1 family is biased away from these traces.

Compared with the generic Montgomery projection loop, the relevant gain is not the full factor 16 because generic Montgomery curves are already conditioned on rational 2-torsion. A rough per-trial density gain is:

```text
gain ~= 8 * L / F_generic
```

with `F_generic ~= 0.62` for this p23 projection setup, giving about `12.9 * L`, or roughly 9.7x to 12.9x for `L = 0.75-1.0`. Wall-clock gain is lower because X1 sampling and halving cost more per trial.

Halving-survival diagnostics were added locally in:

```text
notes/x16_halving_survival_stats.md
```

The first 1M-sample diagnostic reached depth 20 but not the target depth 39. This is expected at diagnostic scale and confirms that the high-depth tail is very thin; it does not by itself estimate the final p23 hit probability without the trace-conditioning model.

## Pass Criteria

The run passes if a candidate `(p,A,x0)` is found and then survives:

1. Built-in verifier in `pomerance.c`.
2. Andrew Sutherland's `vpp.py`.
3. Independent Python Montgomery doubling replay.
4. Lean certificate generation if practical, matching the p22 artifact style.

## Interpretation

If a hit lands inside roughly 35-45B aggregate trials:

- The result supports a real constant-factor search-space shrink from X1(16) prescribed torsion plus halving.
- Combined with the observed throughput, it is operationally far below `sqrt(p) ~= 316B`.
- It is still not formal sub-sqrt scaling, because fixed X1(16) only changes constants.

If a hit lands below about 5B aggregate trials:

- Treat it as exciting but ambiguous.
- It may be luck, or it may indicate a stronger distributional bias than expected.
- Replicate on nearby targets and controlled smaller targets.

If the 50B budget misses:

- Do not discard the idea immediately.
- Either extend to 100-120B aggregate with fresh seeds, or switch to calibration and cleaner higher-torsion variants.

## Next Actions By Outcome

Hit:

1. Stop all workers.
2. Extract the triple and preserve the successful worker log.
3. Run the local verification helper, which performs independent replay, `openssl prime`, and DANGER3 `vpp.py`:

   ```bash
   scripts/verify_pomerance_triple.py --log runs/p23_x16halve_20260601_110154/workerNN.log
   ```

   This helper was validated on the known p22 triple and on `results/p22/p22-worker07-tail.txt`.

4. Or run the one-command finalizer, which verifies, copies the worker log, writes a transcript, and generates the Lean certificate artifact:

   ```bash
   scripts/finalize_pomerance_hit.sh --log runs/p23_x16halve_20260601_110154/workerNN.log
   ```

   This finalizer was validated on the p22 worker artifact into `/tmp/p22-finalize-test`.

5. Record total latest-worker-tail trials, not supervisor cumulative progress.
6. Compare against p22 handoff and generic p23 projected estimates.

Miss at 50B:

1. Launch a second 50B shard set with fresh seeds if operationally convenient.
   The local helper for this is:

   ```bash
   scripts/p23_launch_x16halve_shard.sh --seed-base 5000000
   ```

   It refuses to launch while `pomerance_halve` processes are already running unless `--force` is supplied.

2. Run controlled smaller-p A/B tests: generic projection vs X1(16)-halving.
3. The SEA `ell=3` filter and naive full backtracking diagnostics have been demoted as next-production options:
   - naive `ell=3` filtering is too slow versus `x16halve`;
   - bounded all-branch halving only gave about a 1.35x survival lift through depth 12 while frontier size grew rapidly.
4. Prototype X1(32) sampling and measure overhead only as a calibration/research path, not as the next production shard.

Miss at 100-120B:

1. Downgrade X1(16)-first-branch as a standalone p23 production strategy.
2. Prioritize X1(32), full halving, or a CM/prescribed-order construction.
3. Preserve negative result as useful calibration.
