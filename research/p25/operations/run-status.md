---
type: operations
status: archived
updated: 2026-06-19
canonical: true
owner: llm
---

# Run Status

## Purpose

Track the p25 production fleet result and preserve the boundary between the
successful chunk and the earlier unexplained partial stop.

## Current Claim

The p25 production search is closed with a verified hit from the proven
practical surface:

```text
p = 10000000000000000000000013
mode = x16halvenonsplit
workers = 10 launched, 0 currently alive
run_dir = runs/p25_x16hn_20260616_051158_py_seed26047290
marker = HIT
```

Verified triple:

```text
p  = 10000000000000000000000013
A  = 5863342488035851054212447
x0 = 9636258147581954669181726
```

Hit and accounting:

```text
found_at = 2026-06-18 02:32:33 PDT
successful_worker = worker08
successful_worker_elapsed = 163234.41s
successful_worker_local_accepted_trials = 19634415922
reconstructed_successful_run_aggregate_trials = 196343915922
sqrt_floor(p) = 3162277660168
successful_run_fraction_of_sqrt = 0.062089398
successful_run_speedup_vs_sqrt = about 16.11x
```

Final heartbeat state after cleanup:

```text
workers_alive = 0/10
watcher_alive = no
heartbeat_alive = no
marker = HIT
```

Previous production chunk boundary:

```text
run_dir = runs/p25_x16hn_20260612_085118_py
last_heartbeat = 2026-06-14T23:15:39-0700
last_heartbeat_trials = 266467000000
worker_tail_range ~= 26647000000..26656000000
marker = none
verdict = partial unexplained termination, not exhausted and not a hit
```

Full practical campaign accounting, charging that prior partial chunk:

```text
prior_partial_chunk_trials = 266467000000
successful_run_trials = 196343915922
total_practical_campaign_trials = 462810915922
full_campaign_fraction_of_sqrt = 0.146353662
full_campaign_speedup_vs_sqrt = about 6.83x
```

## Decisive Evidence

- `runs/p25_x16hn_20260616_051158_py_seed26047290/HIT.txt` records the hit
  timestamp, worker tail, triple, and `Verified: PASS`.
- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log` ends with
  `workers=0/10`, `watcher=dead`, and `marker=HIT`.
- Official DANGER3 `vpp.py` returned `True` for the triple.
- `scripts/verify_pomerance_triple.py` in the public repo passed independent
  doubling replay, OpenSSL primality, official verifier, and generated
  `results/p25/pomerance_10000000000000000000000013.lean`.
- [Strict practical improvement evidence](../evidence/lane_D_strict_practical_improvement.md)
  explains why the successful fleet stayed on `x16halvenonsplit`.
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
  checks that this launcher/heartbeat/relaunch policy remains synchronized
  with the theorem-front ordering and the public/private mirror boundary.

## Open Blockers

- No practical-search blocker remains for the p25 certificate.
- The earlier chunk still died without a clean exhausted marker, so it should
  remain recorded as partial unexplained termination.
- The theorem-side moonshot remains future work and was not needed for the
  submitted triple.

## Next Reads

- [Practical search](../lanes/practical-search.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [Frontier](../frontier.md)

## Linked Artifacts

- `runs/LATEST_P25_RUN.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/HIT.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/COMMAND.txt`
- `runs/p25_x16hn_20260612_085118_py/watch.log`
- `results/p25/triple.txt`
- `results/p25/p25-success-summary.txt`
- `results/p25/p25-verification.txt`
- `results/p25/pomerance_10000000000000000000000013.lean`
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
