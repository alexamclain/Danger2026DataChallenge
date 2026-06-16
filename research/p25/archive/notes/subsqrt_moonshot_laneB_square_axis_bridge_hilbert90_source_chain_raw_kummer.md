# Subsqrt Moonshot Lane B Square-Axis Bridge Hilbert-90 Source Chain Raw/Kummer

Date: 2026-06-12

## Result

The pinned support-three Hilbert-90 source chains lift cleanly into the raw
`C_12675` producer harness.

For each of the four active source chains:

```text
chain:
  quotient support = 3
  raw support      = 75
  raw degree       = +/-75
  kernel modes     = {0}

first boundary:
  quotient support = 4
  raw support      = 100
  raw degree       = 0
  kernel modes     = {0}

bridge image:
  quotient support = 6
  raw support      = 150
  raw degree       = 0
  kernel modes     = {0}
```

All three stages are block-constant on the invisible `C_25` kernel, recover
their quotient trace under normalized raw trace, and satisfy the raw
`D^3 = Y` relation after the kernel trace.

## Kernel Gauge Scan

The six sparse source-chain pair directions are:

```text
25, 172, 197, 310, 335, 482
```

Each has `25` raw kernel-gauge lifts, obtained by adding invisible multiples
of the quotient order `507`.

For every one of these directions:

```text
right-source order histogram = {3: 1, 15: 4, 75: 20}
minimum combined source order = 507
C-source order values         = {169}
C_169 Kummer degree           = 169
C_13 shadow Kummer degree     = 13
```

So the invisible right kernel can make the right-side motion cheap: one gauge
representative has right-source order `3`.  But the `C` side stays primitive
in every gauge.

## Interpretation

This sharpens the producer contract.

The source-chain ladder is not blocked by raw trace compatibility:

```text
support-3 chain
  -> support-4 degree-zero first boundary
  -> support-6 signed bridge
```

already lives as a kernel-trivial raw object.  The obstruction is not the
`C_25` right kernel.  A successful finite-field identity, CM-Artin producer, or
modular-unit pullback still has to realize primitive `C_169` motion with full
`C_169` Kummer degree on the active source-chain directions.

This rules out a producer story that explains only a cheap right-kernel gauge
or a low-order `C_13` shadow.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_raw_kummer_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p25 python3 research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_raw_kummer_gate.py
```

Standalone marker:

```text
square_axis_bridge_hilbert90_source_chain_raw_kummer_rows=1/1
```
