---
type: operations
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Run Status

## Purpose

Track the live production fleet and preserve the boundary between the current
chunk and the earlier unexplained partial stop.

## Current Claim

The active production search is healthy and still uses the proven practical
surface:

```text
p = 10000000000000000000000013
mode = x16halvenonsplit
workers = 10
run_dir = runs/p25_x16hn_20260616_051158_py_seed26047290
```

Latest observed watcher snapshot (`2026-06-16 05:44:02 PDT`):

```text
workers_alive = 10/10
watcher_alive = yes
trials = 2320500000
rate_Mps = 1.210
marker = none
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

## Decisive Evidence

- The live watcher snapshots recorded in the original `pomerance-p25-run`
  workspace showed the current worker count, rate, and marker state.
- [Strict practical improvement evidence](../evidence/lane_D_strict_practical_improvement.md)
  explains why the fleet is still on `x16halvenonsplit`.

## Open Blockers

- No hit has been found yet.
- The earlier chunk died without a clean exhausted marker, so operational
  continuity is still worth watching.
- No alternate mode has yet produced better expected hits per CPU-hour.

## Next Reads

- [Practical search](../lanes/practical-search.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [Frontier](../frontier.md)

## Linked Artifacts

- The original run-specific `LATEST_P25_RUN.txt` and `watch.log` files lived in
  the separate run workspace and are summarized here rather than vendored into
  this repository copy.
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
