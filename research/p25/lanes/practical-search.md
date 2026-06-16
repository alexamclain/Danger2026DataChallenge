---
type: lane
status: active
updated: 2026-06-16
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

As of `2026-06-16 05:44 PDT`, the current chunk reported:

```text
run_dir = runs/p25_x16hn_20260616_051158_py_seed26047290
workers_alive = 10/10
watcher_alive = yes
accepted_candidates ~= 2320500000
aggregate_rate ~= 1.210 M/s
marker = none
```

The immediately prior production chunk stopped partway through and is treated
as a partial unexplained termination, not exhaustion and not a hit.

## Decisive Evidence

- [Run status](../operations/run-status.md) captures the active chunk and the
  prior partial stop boundary.
- [Lane D strict practical improvement note](../evidence/lane_D_strict_practical_improvement.md)
  keeps `x16halvenonsplit` ahead of dgate, dgateskip, full-branch, Atkin, and
  X1 tower variants on present evidence.
- [P24 prior art](../sources/p24-prior-art.md) remains the authority on why the
  strict X1(16) practical route survived earlier audits.

## Open Blockers

- A certificate still requires an actual hit.
- The prior chunk died without a clean exhausted marker, so operational
  monitoring still matters.
- No alternate production mode has yet cleared the "better hits per CPU-hour"
  bar.

## Next Reads

- [Run status](../operations/run-status.md)
- [Transfer matrix](../concepts/transfer-matrix.md)
- [P24 prior art](../sources/p24-prior-art.md)

## Linked Artifacts

- Operational watcher artifacts lived in the separate `pomerance-p25-run`
  workspace and are summarized in the canonical run-status page and archived
  run ledger.
- [Legacy run ledger](../archive/notes/run_status_legacy_20260616.md)
- [Lane D evidence](../evidence/lane_D_strict_practical_improvement.md)
