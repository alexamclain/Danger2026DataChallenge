# Subsqrt Moonshot Lane B Ray-Local Modular-Unit Pullback Router

Date: 2026-06-14

## Purpose

This checkpoint is the front door for future CM-Artin, modular-unit,
Robert/Siegel/Kubert-Lang, or related theorem claims that purport to explain
the p25 Lane B local pullback.

It does not construct the missing arithmetic producer.  It decides whether a
claim deserves to enter one of the finite acceptors that already exist:

```text
raw theta31 / bridge vector -> ray-local theta31 pullback falsifier or bridge harness
curved Hilbert-90 corner    -> unit-triangle 75-atom curved-corner producer intake
```

## Local Target

The claim must be about the actual p25 negative-trace source:

```text
right source: inert/ray-local prime 151
C-axis source: split prime 677
quotient: C_3 x C_13 for the first lab
raw order: 12675
quotient rectangles: 39
residue rectangle size: 25 * 13 = 325
carrying rectangles: 18
raw carry-one positions: 5850
```

For the square-axis/bridge route, the same source discipline has to preserve
the mixed right/C payload:

```text
bridge mixed right/C characters: 336
compact curved-corner support: 75 atoms
required translated quotient edge: T=(2,113)
curved-corner unit triangle: primitive unit sign + branch coefficient
```

## Gate

File:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_ray_local_modular_unit_pullback_router_gate.py
```

Default command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_modular_unit_pullback_router_gate.py
```

Candidate command template:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_modular_unit_pullback_router_gate.py \
  --candidate --name proposed_pullback \
  --theorem-body --ray-local --split-c --coupled --rectangles \
  --rank2 --avoid-degenerate --not-x-only --c-odd --not-c-character \
  --d-segment --k-trace --t-edge --kernel-gauge --raw-bridge
```

For a curved-corner proposal, replace `--raw-bridge` with
`--curved-corner --unit-triangle`.  A curved-corner proposal without
`--unit-triangle` is rejected before finite-shape credit.  A proposal with an
accepted finite shape but no finite value/divisor theorem is deliberately
classified as helper-only.

## Regression Matrix

The router checks 24 synthetic rows:

```text
row_count              = 24
rejected_rows          = 13
helper_only_rows       = 2
conditional_rows       = 3
finite_shape_rows      = 10
finite_value_rows      = 8
source_closing_rows    = 6
danger3_unblocked_rows = 5
cross_level_bridge_rows= 4
x16_surface_rows       = 3
extraction_ready_rows  = 2
submission_ready_rows  = 1
```

Expected marker:

```text
ray_local_modular_unit_pullback_router_rows=1/1
```

## First Falsifiers

Reject a proposed producer if it is any of the following:

```text
no verified theorem body
split-prime-only or plain class quotient source
separated right selector times C selector
not constant on the 25 x 13 residue rectangles
rank-1-only mixed module or dependence on u+2v=0
x-only or inversion-even table
missing active C-side odd orientation
plain C-character/sign tag instead of coupled orientation
point quotient with no D segment
missing, collapsed, or nonprimitive K trace
translated edge other than T=(2,113)
raw representative shifted outside kernel gauge
curved-corner payload missing the unit-triangle row law
```

## Positive Artifact

A useful positive artifact must provide one of:

```text
explicit raw vector accepted by the ray-local theta31 pullback falsifier;
explicit raw bridge vector accepted by the square-axis bridge harness;
unit-triangle 75-atom curved-corner finite shape accepted by the curved-corner intake.
```

Even after such a finite shape, the route remains helper-only until it comes
with:

```text
finite value/divisor theorem;
period-156 branch/root/telescoping context;
challenge-legal arithmetic source theorem;
DANGER3 finite-identity or non-CM framing;
same-j X_1(8112) bridge;
X_1(16) specialization;
concrete (A,x0);
official vpp.py verification.
```

## Interpretation

This is the intake for literature hits and expert suggestions.  It amortizes
the existing p24/p25 local-source work by making the first falsifier explicit:
a candidate has to explain the inert-151 by split-677 coupling and the
rank-2 mixed payload before we spend energy on global certificate packaging.
