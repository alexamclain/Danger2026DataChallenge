# P25 First-Class Run v2 Plan Guard

Updated: 2026-06-17

Marker: `p25_v2_first_class_run_v2_plan_guard_rows=1/1`

## Purpose

Preserve the v2 operating shape as a cheap cockpit invariant. The plan is now
spread across canonical pages, so this guard checks the parts that should not
drift during production-search-first work.

## Pages Read

- `frontier.md`
- `operations/run-status.md`
- `lanes/practical-search.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `concepts/transfer-matrix.md`
- `AGENTS.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_first_class_run_v2_plan_guard_gate.py
```

The gate returned `p25_v2_first_class_run_v2_plan_guard_rows=1/1`.

## Findings

The cockpit now has an executable v2 shape check:

- Practical search remains the only concrete certificate route today.
- The production surface remains `x16halvenonsplit`, 10 workers, detached
  launcher plus heartbeat, no second manual watcher, and next relaunch seed
  base `27094580`.
- The prior production stop remains classified as a partial unexplained
  termination, not a hit or clean exhaustion.
- H0 and mixed conductor 39 remain the only first-pass theorem fronts.
- Their shared finite target remains one support-156 legal row with
  `Norm_156(Y_507)` boundary and a finite value/divisor theorem.
- Exact-P remains second-pass through the fixed 75-atom payload and the
  `75 -> 300 -> 12 -> 312 -> 156` bridge.
- Lane A remains killed as literal p24 CM/Lang transfer; Lane B and Lane C
  remain support microscopes tied to a live theorem idea.
- The private cockpit/public mirror distinction remains documented.

## Verdict

Continue. The plan is implemented in the canonical cockpit, and the new guard
keeps the executive research shape testable without replaying heavy theorem
gates or encoding fresh private heartbeat numbers.
