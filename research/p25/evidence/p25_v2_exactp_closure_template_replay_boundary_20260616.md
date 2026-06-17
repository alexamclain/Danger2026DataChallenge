# P25 v2 Exact-P Closure-Template Replay Boundary

Updated: 2026-06-16

## Purpose

Record the replay boundary for the archived exact-P closure-theorem template.
The old gate is useful provenance for the exact-P moonshot, but it is not a
lightweight probe during an active production fleet. The v2 cockpit should use
the promoted exact-P interface contract, exact-P minimal hook, and theta2
period-156 support contract for normal source/expert intake.

This page is not a theorem result. It is a compute/context hygiene boundary
for the exact-P heavy route.

## Attempted Replay

First, running with only archived gates on `PYTHONPATH` fails before the real
replay because archived harness modules are not on `sys.path`.

```bash
PYTHONPATH=research/p25/archive/gates PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py
```

The correct archived replay surface is:

```bash
PYTHONPATH=research/p25/archive/gates:research/p25/archive/harness \
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py
```

That replay entered the support-resolvent / half-edge footprint stack and was
interrupted after more than 60 seconds while the 10-worker production fleet was
active. The stack was inside the raw-source kernel-mode support calculation,
not a quick source/intake classifier.

## Pages Read

- `evidence/p25_v2_exactp_theorem_interface_contract_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`
- `evidence/p25_v2_source_action_registry_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_exactp_closure_template_replay_boundary_gate.py
```

The gate returned `p25_v2_exactp_closure_template_replay_boundary_rows=1/1`.

## Boundary Rows

```text
archived_closure_template_gate
  status   = heavy_replay_boundary
  decision = do_not_use_as_default_short_probe
  observed = entered support-resolvent / half-edge footprint stack

missing_harness_path
  status   = replay_hygiene_boundary
  decision = use_archive_harness_path_if_explicit_heavy_replay_is_needed
  observed = gates-only PYTHONPATH fails before replay

v2_exactp_theorem_interface_contract
  status   = lightweight_successor
  decision = use_for_normal_exactp_intake

v2_exactp_minimal_hook
  status   = lightweight_successor
  decision = use_for_source_or_expert_answers

v2_theta2_period156_support_contract
  status   = lightweight_successor
  decision = use_for_theta2_payload_intake
```

## Counts

```text
heavy_replay_rows = 1
lightweight_successor_rows = 3
exactp_source_theorems = 0
submission_ready_rows = 0
```

## Verdict

```text
positive_artifact = exact-P heavy replay boundary
continue_exactp = yes, through v2 lightweight contracts by default
heavy_replay_condition = only rerun the archived closure template when an
                         exact-P theorem-shaped snippet needs that full
                         provenance check and the production fleet can spare it
discard_condition = spending active-run CPU/context on the old closure template
                    as a routine source-search probe
```

Exact-P remains live. This pass only says the old closure-template gate should
not be the default way to inspect it during sustained search.
