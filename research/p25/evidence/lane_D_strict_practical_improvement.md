# Lane D: Strict Practical Improvement for p25

Date: 2026-06-12 PDT

## Files inspected

- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/strict_danger3_frontier.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/p23_transfer_to_p24_scaling_audit.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/x1_tower_mitm_cost_audit.py`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/notes/x16_first_d_y_gate_20260601.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/notes/x16_inverse_gate_branch_stats.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/notes/p23_operational_runbook.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/src/pomerance.c`
- `/Users/agent/Documents/Codex/pomerance-p25-run/README.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/RESULT.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/LATEST_P25_RUN.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_085118_py/COMMAND.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_085118_py/worker00.log`

## p25 facts

Active run target is:

```text
p = 10000000000000000000000013 = 10^25 + 13
mode = x16halvenonsplit
workers = 10
trials_per_worker = 50000000000
```

Arithmetic:

```text
p mod 8 = 5
p mod 3 = 2
p mod 5 = 3
p mod 7 = 2
k = 42
odd parts = 2273736754433, 8881784197, 2273736754431
```

Worker00 startup rate was about `0.109-0.116 M` accepted nonsplit X1(16)
curves/s, matching the p23/p24 production baseline scale.

## Immediate mode

`x16halvenonsplit` remains the best immediate mode.

Reasons:

- p25 is `5 mod 8`, the native residue class for the original Jane/Alexa
  X1(16) square-root path; no p24 `3 mod 4` patch risk is involved.
- p24 transfer notes say fixed X1(16) plus nonsplit branch collapse is still
  the practical constant-factor route; growing X1/X0 tower ideas remain
  rejection-cost neutral without a new subdensity sampler.
- In the nonsplit family the rational 2-Sylow is cyclic, so first-branch
  halving is complete. The inverse-gate branch selector showed no p23 lift:
  nonsplit depth-12 first/gate/all were all `410/100000`.
- The current source verifies any found `(A,x0)` with `verify128`, and the
  active p25 command is exactly the proven p24 production surface.

## Other modes

Safe to leave off for production now:

- `x16halvenonsplitdgate` and `x16halvenonsplitdgateskip`: correctness-safe
  search modes, but p23 production timing demoted them. Baseline nonsplit was
  about `0.1165 M/s`; dgate was `0.0665 M/s`; dgateskip was `0.0653 M/s`.
  The gate would need a full-depth survivor lift above about `1.75x`, and the
  measured depth-16 survivor/sec was not robustly positive.
- `x16halvefull`: full branch recursion is not a practical production mode;
  branch growth eats the small bounded survival gain.
- `x16`, `x16halve`: dominated by nonsplit halving for the strict run.
- `x16ell3bench`, `x16ell3directybench`, `x16cubic3stats`: p25 has
  `p mod 3 = 2`, so the nontrivial cubic/ell=3 path is unavailable.
- `x16atkin5bench`: p25 has `p mod 5 = 3`; the code itself warns the p23
  target-residue interpretation assumes `p mod 5 = 2`, and p23 timing made
  X0(5) too slow anyway.
- `x16atkin7bench`: diagnostic only, not wired as a target-safe production
  filter; p23 runbook says small Atkin status filters were too slow.
- `x1_32rootbench`: useful diagnostic only. The X1 tower cost audit says
  the degree-10 fiber/root work is likely more expensive than the 2x density
  gain unless a new sampler appears.
- `x16quarticstats*`, `x16labelstats`, `x16split*`, `x16torsionstats`: stats
  surfaces, not production search modes; prior cheap-character scans plateaued
  at constant lifts.

## Safe small mode to benchmark later

If the fleet is idle, the only existing production-mode retest worth doing is
a tiny paired timing of:

```text
x16halvenonsplit
x16halvenonsplitdgate
x16halvenonsplitdgateskip
```

This is a wall-clock check only. Promote nothing unless dgate/dgateskip is
unexpectedly close to baseline throughput on p25 and a paired survivor/sec
stats run beats the `1.75x` break-even threshold with margin.

## First falsifier / positive next command

Run only when the fleet is idle:

```bash
cd /Users/agent/Documents/Codex/pomerance-p25-run
for mode in x16halvenonsplit x16halvenonsplitdgate x16halvenonsplitdgateskip; do
  /usr/bin/time -p ./src/pomerance 10000000000000000000000013 26012345 500000 "$mode" > "/tmp/p25_laneD_${mode}.log" 2>&1
done
rg "curve_mode|rate_Mps|Not found|Found|Verified" /tmp/p25_laneD_x16*.log
```

Falsifier: dgate/dgateskip still run near the p23 ratio, around `0.56-0.58x`
of baseline accepted-candidate throughput. Keep them killed.

Positive: dgate or dgateskip reaches at least `0.85x` baseline throughput;
then run a small paired `x16branchstatsnonsplit` vs
`x16branchstatsnonsplitdgate` depth-14/16 survivor/sec check before any fleet
switch.

## Recommendation

Continue the current p25 `x16halvenonsplit` fleet. Do not kill or switch it
for first-d, dgateskip, X1(32), Atkin, cubic, quartic, or full-branch modes
on present evidence. Reassess only after a hit, after the current budget is
exhausted, or after the idle-machine micro-timing above produces a clear
positive.
