# Subsqrt Moonshot Lane B Square-Axis Relation/Kernel Equivalence

Date: 2026-06-12

## Result

The raw lifted quotient relation is not merely a good filter on examples.  It
is exactly the kernel-trivial condition.

The quotient relation is:

```text
D^3 = Y
```

On raw exponents:

```text
D = +172
Y = +9
3*172 - 9 = 507
raw_order = 12675 = 25 * 507
```

So `D^3 = Y` on raw values is exactly invariance under the `507`-step trace
kernel.  The relation space is the block-constant/kernel-trivial subspace.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_relation_kernel_equivalence_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_relation_kernel_equivalence_gate.py
```

Observed:

```text
case = square_axis_C3xC169
raw_order = 12675
quotient_order = 507
B = 25
modulus = 126751

relation_offset:
  3*S_STEP - Y_STEP = 507
  equals_quotient_order = 1

cycle_structure:
  cycle_count = 507
  length_counts = {25: 507}

linear_dimensions:
  relation_rank = 12168
  relation_nullity = 507
  trace_rank = 507
  trace_kernel_dimension = 12168

residual_unique_block_lift:
  trace_matches = 507 / 507
  raw_support = 450 / 450
  relation_holds = 1

trace_restricted_to_relation_space:
  sample_isomorphism_hits = 507 / 507

square_axis_relation_kernel_equivalence_rows = 1 / 1
```

## Consequence

The producer contract can be stated without ambiguity:

```text
raw D^3 = Y
<=> 507-step kernel invariance
<=> block-constant / kernel-trivial lift
```

On this relation space, normalized `B=25` trace to `C_3 x C_169` is an
isomorphism.  Therefore the quotient residual has a unique raw lift satisfying
the raw quotient relation: the `450`-point block lift.

This upgrades the previous toy-lift falsifier:

```text
trace-correct but sparse lifts fail because they are not in the relation space;
trace-zero kernel contamination fails because it leaves the relation space;
any valid producer must land in the 507-dimensional relation space before trace.
```

The immediately preceding checked examples are:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_raw_quotient_relation.md
```
