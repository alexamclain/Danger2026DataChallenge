---
type: lane
status: active
updated: 2026-06-17
canonical: true
owner: llm
---

# Practical Search

## Purpose

Track the production search surface, the live run, and the decision boundary
for changing modes.

## Current Claim

`x16halvenonsplit` remains the best practical route for `p = 10^25 + 13`.
The active 10-worker fleet is healthy, `p mod 8 = 5` means no p24 square-root
patch is needed, and there is still no measured alternative with better
expected hits per CPU-hour.

As of the latest private smoke check on `2026-06-17`, the public-safe status is:

```text
run_dir = runs/p25_x16hn_20260616_051158_py_seed26047290
workers_alive = 10/10
watcher_alive = yes
heartbeat_alive = yes
accepted_candidates = redacted in public mirror
aggregate_rate ~= 1.200 M/s
marker = none
```

The immediately prior production chunk stopped partway through and is treated
as a partial unexplained termination, not exhaustion and not a hit.

Canonical relaunch uses `src/launch_fleet_detached.py` plus
`src/launch_status_heartbeat.py`; the detached launcher already starts
`watch_hit.sh`, so a second manual watcher is unnecessary. The next 10-worker
chunk should start at `seed_base=27094580`.

## Decisive Evidence

- [Run status](../operations/run-status.md) captures the active chunk and the
  prior partial stop boundary.
- The private live-run smoke audit verifies the detached launcher layout,
  worker liveness, watcher liveness, heartbeat liveness, and marker state; it
  is not mirrored here because it contains fresh local telemetry.
- [V2 post-theorem extraction router](../evidence/p25_v2_post_theorem_extraction_router_20260616.md)
  records the bridge from a theorem hit to the practical `x16halvenonsplit`
  surface: same-`j` `X_1(8112)`, `A,xP16`, 38 halvings or direct `x0`, and
  official `vpp.py`.
- [V2 extraction payload contract](../evidence/p25_v2_extraction_payload_contract_20260616.md)
  records the constructive downstream payload accepted after a theorem hit:
  same-j bridge, practical `X_1(16)` payload, halving/x-chain/direct `x0`, and
  official `vpp.py`.
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
  is the compact post-theorem acceptance boundary: theorem hits and exact-P
  hooks still need DANGER3 framing, same-`j` `X_1(8112)`, practical
  `X_1(16)` payload, halving/direct `x0`, and official `vpp.py`.
- [V2 end-to-end answer router](../evidence/p25_v2_end_to_end_answer_router_20260616.md)
  classifies future source, theorem, extraction, or practical-search payloads
  from repair/reject through source-stage, framed theorem, extraction-ready,
  and official `vpp.py`-verified submission.
- [Lane D strict practical improvement note](../evidence/lane_D_strict_practical_improvement.md)
  keeps `x16halvenonsplit` ahead of dgate, dgateskip, full-branch, Atkin, and
  X1 tower variants on present evidence.
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
  keeps the production mode, relaunch policy, theorem-front order, exact-P
  demotion, and support-microscope boundary testable from the cockpit.
- [P24 prior art](../sources/p24-prior-art.md) remains the authority on why the
  strict X1(16) practical route survived earlier audits.

## Open Blockers

- A certificate still requires an actual hit.
- The prior chunk died without a clean exhausted marker, so operational
  monitoring still matters.
- No alternate production mode has yet cleared the "better hits per CPU-hour"
  bar.
- A theorem-side bridge is not enough unless it passes the extraction minimal
  hook and emits the practical payload accepted by the extraction contract.
- A mode change is accepted only if paired timing gives at least `0.85x`
  baseline throughput and measured survivor lift clears the `1.75x` break-even
  threshold with margin.

## Next Reads

- [Run status](../operations/run-status.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [P24 prior art](../sources/p24-prior-art.md)

## Linked Artifacts

- `runs/LATEST_P25_RUN.txt`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/watch.log`
- `runs/p25_x16hn_20260616_051158_py_seed26047290/COMMAND.txt`
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
- [Lane D evidence](../evidence/lane_D_strict_practical_improvement.md)
- [V2 extraction payload contract](../evidence/p25_v2_extraction_payload_contract_20260616.md)
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
- [V2 end-to-end answer router](../evidence/p25_v2_end_to_end_answer_router_20260616.md)
- [First-class-run v2 plan guard](../evidence/p25_v2_first_class_run_v2_plan_guard_20260617.md)
