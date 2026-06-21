# P27 Label-2 E[2] Packet Source Probe

Date: 2026-06-21

## Claim

The residual elliptic `E[2]` packet selector is exact but does not create
source-level lift on p27. It halves the candidate set and therefore doubles
per-candidate survival, but the best survivor per residual elliptic source is
unchanged through the measured depths.

This kills the easiest way the new cyclic-quartic/order-4 structure could have
become sqrt-beating: a small `E[2]` packet source that forces `d1+d2` and
improves the chance of later `d_j` gates.

## Context

The order-4 lift shows that `compactD=-1` is a cyclic quartic cover over the
residual elliptic curve:

```text
E: W^2 = X^3 - X
```

The natural next packet test is whether the rational `E[2]` orbit can choose a
better label-2 representative at the source level, rather than merely filtering
half the candidates.

The C mode still prints `P26` in its banner, but the prime and arithmetic in
these runs are p27:

```text
p = 1000000000000000000000000103
k = 45
```

## Commands

```bash
./src/pomerance 1000000000000000000000000103 \
  141 50000 x16label2packet3stats 24 \
  > research/p27/archive/probe_outputs/p27_label2_packet3_seed141_50k_depth24_20260621.txt 2>&1

./src/pomerance 1000000000000000000000000103 \
  142 200000 x16label2packet3stats 24 \
  > research/p27/archive/probe_outputs/p27_label2_packet3_seed142_200k_depth24_20260621.txt 2>&1
```

## Exactness Checks

Both runs had zero algebra failures:

```text
diagonal_product_mismatches = 0
arf_formula_fail = 0
arf_one_diagonal_mismatches = 0
arf_first_target_mismatches = 0
selected_queried_branch_missing = 0
selected_candidate_fail = 0
```

The predicted good-packet rate is exactly the expected half:

```text
seed 141: good_packet_rate = 0.499340000
seed 142: good_packet_rate = 0.500175000
```

## Survivor Result

On the larger 200k-source run:

```text
selector_candidates_per_plain_candidate = 0.500175000
```

Stable-depth summary:

```text
depth  plain_source  selector_source  source_lift  candidate_lift
12     0.007585000   0.007585000      1.000000     1.999300
13     0.003605000   0.003605000      1.000000     1.999300
14     0.001835000   0.001835000      1.000000     1.999300
15     0.000945000   0.000945000      1.000000     1.999300
16     0.000535000   0.000535000      1.000000     1.999300
17     0.000210000   0.000210000      1.000000     1.999300
18     0.000110000   0.000110000      1.000000     1.999300
19     0.000040000   0.000040000      1.000000     1.999300
20     0.000010000   0.000010000      1.000000     1.999300
21     0.000010000   0.000010000      1.000000     1.999300
22     0.000010000   0.000010000      1.000000     1.999300
23     0.000005000   0.000005000      1.000000     1.999300
24     0.000005000   0.000005000      1.000000     1.999300
```

The smaller 50k run showed the same pattern through its nonzero depths:

```text
source_lift = 1.000000
candidate_lift ~= 2.002643
```

## Interpretation

Positive:

```text
The E[2] packet algebra is internally exact.
The selector really identifies the intended half of candidates.
```

Negative:

```text
The packet selector does not improve the best survivor per elliptic source.
It is a filter, not a source-level lift.
It gives no evidence of a d3/d4 recurrence or sqrt-beating packet law.
```

This is the same distinction that keeps `compactD=-1` from being enough by
itself: one more forced gate is a constant-factor improvement unless it recurs
or can be sourced without paying the random half-loss.

## Continue / Kill

```text
continue = cyclic-quartic/order-4 quotient as a Sage/Magma decomposition target
continue = GPU compactD=-1 telemetry with d3/d4 inside the stratum
continue = search for recurrence across later d_j, not another E[2] packet

kill = E[2] packet selector as a sqrt-beating source
kill = claiming 2x candidate lift as source lift
kill = rerunning packet3 at larger scale unless a new invariant changes the expected source metric
```

## Linked Artifacts

- Output: `research/p27/archive/probe_outputs/p27_label2_packet3_seed141_50k_depth24_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_packet3_seed142_200k_depth24_20260621.txt`
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Related: [P27 Label-2 Second-Gate Cover](p27_label2_second_gate_cover_20260621.md)

```text
p27_label2_e2_packet_source_probe_rows=1/1
```
