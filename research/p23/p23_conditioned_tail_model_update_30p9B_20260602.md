# p23 Conditioned Tail Model Update At 30.9B

Date: 2026-06-02 PDT

Purpose: update the active p23 probability model using two current facts:

```text
1. larger exact/sampled calibration rows support a geometric nonsplit v2 tail
   through visible depths;
2. the live p23 run has reached about 30.9B accepted nonsplit trials with no
   verified hit, which updates the p23-specific L posterior downward.
```

This is an analysis artifact only. It does not touch the active workers.

## Live State

Latest probability command:

```bash
RUN=$(cat /tmp/p23_run_dir.txt)
python3 scripts/p23_nonsplit_probability_window.py "$RUN" \
  --lifts 1.5 \
  --targets 35000000000 45000000000 50000000000 75000000000 100000000000 \
  --sensitivity \
  | tee "$RUN/probability_update_30p9B_20260602.log"
```

Snapshot:

```text
accepted_nonsplit_trials = 30.957B
fraction_of_sqrt_p = 0.097896
Verified: PASS = none seen
```

Main prior:

```text
L ~ Uniform(0.4, 1.2)
lift = 1.5
posterior mean L = 0.659
posterior q10/q50/q90 = 0.430 / 0.610 / 0.980

conditional hit probability from now:
  by 35B  = 0.1085
  by 45B  = 0.3254
  by 50B  = 0.4115
  by 75B  = 0.6952
  by 100B = 0.8365
```

Pessimistic prior:

```text
L ~ Uniform(0.1, 1.2)
lift = 1.5
posterior mean L = 0.401
posterior q10/q50/q90 = 0.130 / 0.330 / 0.800

conditional hit probability from now:
  by 35B  = 0.0669
  by 45B  = 0.2073
  by 50B  = 0.2664
  by 75B  = 0.4843
  by 100B = 0.6206
```

## Tail Rollup Helper

Added:

```text
scripts/x16_nonsplit_tail_rollup.py
```

It parses exact FFT/brute logs and sampled BSGS logs, then reports:

```text
Pr[v2(#E) >= d] / 2^(4-d)
```

for the nonsplit X1(16) stream. The denominator is the simple geometric
baseline after X1(16) forces `v2 >= 4`.

Compile check:

```bash
python3 -m py_compile scripts/x16_nonsplit_tail_rollup.py
```

Status:

```text
PASS
```

## Exact FFT Rows

Command:

```bash
python3 scripts/x16_nonsplit_tail_rollup.py \
  --min-p 50000 \
  runs/x16_fast_trace_enumeration_20260602/*.log \
  | tee runs/x16_nonsplit_tail_rollup_20260602/exact_fft_minp50000.log
```

Aggregate over five exact rows with `p >= 50000`:

```text
total nonsplit rows = 7,201,024

d=5   ratio = 1.000
d=6   ratio = 1.000
d=7   ratio = 0.997
d=8   ratio = 0.999
d=9   ratio = 1.005
d=10  ratio = 0.964
d=11  ratio = 0.905
d=12  ratio = 0.906
d=13  ratio = 1.025
d=14  ratio = 1.208
d=15  ratio = 0.887
```

Interpretation:

```text
The exact nonsplit v2 tail is essentially geometric through depths 5-9 and
still broadly compatible through the highest visible exact depths. Individual
rows show finite-trace-lattice plateaus/cutoffs, so deeper small-prime rows
should not be overfit.
```

## Larger BSGS Matched Controls

Command:

```bash
python3 scripts/x16_nonsplit_tail_rollup.py \
  runs/x16_fast_trace_stack_20260602/*bsgs_sample30000.log \
  | tee runs/x16_nonsplit_tail_rollup_20260602/bsgs_matched_260M_3x30k.log
```

Aggregate over three 30k-row target-residue-matched controls near `p = 260M`:

```text
total nonsplit rows = 90,000

d=5   ratio = 1.003
d=6   ratio = 0.998
d=7   ratio = 0.994
d=8   ratio = 1.001
d=9   ratio = 0.997
d=10  ratio = 0.961
d=11  ratio = 1.013
d=12  ratio = 1.010
d=13  ratio = 0.933
d=14  ratio = 1.013
d=15  ratio = 1.001
```

This is the cleanest current calibration for the nonsplit curve-v2 tail:

```text
inside large p23-residue-matched controls, nonsplit v2 is nearly geometric
through depth 15.
```

## Interpretation

This improves the basis for the prior:

```text
The prior for L is not based only on p23 shallow branchstats anymore. Exact FFT
rows and larger BSGS rows both support a geometric nonsplit v2 tail through
the visible range.
```

But it does not prove `L = 1` at p23 depth 39:

```text
1. p23 success also needs the target trace lattice, not just high v2.
2. exact target-trace mass on larger FFT rows had nonsplit L_trace range about
   0.70 to 1.16, mean about 0.89.
3. depth 39 is far beyond visible exact/sampled calibration depths.
4. the live no-hit evidence through 30.9B accepted trials is real and updates
   the p23-specific posterior downward.
```

So the right synthesis is:

```text
calibration evidence supports keeping L near order 1;
production no-hit evidence argues against the high end of L;
L remains a sensitivity parameter, not a theorem.
```

## Operational Decision

No production change.

```text
keep active y-filtered nonsplit X1(16) while decision=keep_waiting;
if decision=verify_hit, run ./scripts/p23_next_action.sh --execute;
if the 50B budget cleanly misses, use the guarded direct-y nonsplit follow-on.
```
