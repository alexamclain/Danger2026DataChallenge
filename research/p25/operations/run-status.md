---
type: operations
status: active
updated: 2026-06-17
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

Latest public-safe status from the private cockpit (`2026-06-17`):

```text
workers_alive = 10/10
watcher_alive = yes
heartbeat_alive = yes
trials = redacted in public mirror
rate_Mps = 1.200
marker = none
```

Standard launch/relaunch path:

```bash
cc -O3 -o src/pomerance src/pomerance.c
python3 src/launch_fleet_detached.py \
  10000000000000000000000013 \
  x16halvenonsplit \
  10 \
  50000000000 \
  <seed_base> \
  104729 \
  runs/p25_x16hn_<timestamp>
python3 src/launch_status_heartbeat.py runs/p25_x16hn_<timestamp> --interval 60
```

For this lineage, the next 10-worker relaunch seed base is:

```text
next_seed_base = 27094580
```

Do not start a separate manual watcher for a launcher-managed run; the detached
launcher already starts `watch_hit.sh`.

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

- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log` shows the live
  worker count, rate, and marker state in the private cockpit.
- `runs/LATEST_P25_RUN.txt` pins the active run directory in the private
  cockpit.
- A fresh private live-run smoke check on `2026-06-17` found ten
  `src/pomerance` workers plus watcher and status-heartbeat processes alive;
  fresh heartbeat and trial-count telemetry is intentionally not mirrored.
- [Strict practical improvement evidence](../evidence/lane_D_strict_practical_improvement.md)
  explains why the fleet is still on `x16halvenonsplit`.
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
  checks that this launcher/heartbeat/relaunch policy remains synchronized
  with the theorem-front ordering and the public/private mirror boundary.

## Open Blockers

- No hit has been found yet.
- The earlier chunk died without a clean exhausted marker, so operational
  continuity is still worth watching.
- No alternate mode has yet produced better expected hits per CPU-hour.
- If this run dies, classify it as `HIT`, `EXHAUSTED`, or partial unexplained
  termination before launching the next chunk.

## Next Reads

- [Practical search](../lanes/practical-search.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [Frontier](../frontier.md)

## Linked Artifacts

- `runs/LATEST_P25_RUN.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/COMMAND.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/status_heartbeat.pid`
- `runs/p25_x16hn_20260612_085118_py/watch.log`
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
