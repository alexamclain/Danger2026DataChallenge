# P27 Trace/Norm Dplus A-Coordinate Bridge

Date: 2026-06-22

## Claim

The coordinate part of the `Dplus`-to-A bridge is solved.

On actual p27 `Dplus` rows, the A-line coordinate that carries post-Dplus
`d3/d4` is a rational function of the H90 quotient coordinate:

```text
t = y - 1
a = t - 1/t
A = (t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1)/(4*t^4)
A = a^4/4 - 2
```

Thus the missing bridge is not a low-degree map from H90 coordinates to `A`.
That map exists and is cheap.  The remaining mathematical question is narrower:

```text
compare the A-level d3/d4 Kummer classes with the Dplus H90 second-layer class
A_eta = U_eta + z*W_eta.
```

This does not promote GPU production by itself.  The sampled `d3/d4` signs
remain balanced half-gates after the exact coordinate bridge.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_a_coordinate_bridge_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_a_coordinate_bridge_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_a_coordinate_bridge_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-rows 20000 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_a_coordinate_bridge_probe_20260622.txt
```

## Identities

The probe verifies these formulas on same-stream `Dplus` rows:

```text
t = y - 1
a = t - 1/t
g = w/t
a^2 + g^2 = 4
A = (t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1)/(4*t^4)
A = a^4/4 - 2
A + 2 = ((t^2 - 1)^2/(2*t^2))^2
A - 2 = -(((t^2 + 1)*w)/(2*t^2))^2
```

Since `p27 mod 4 = 3`, the last line makes `chi(A-2)=-1` on the H90 rows,
while `A+2` is visibly square.  This explains the otherwise tautological
low-level A-squareclass signs seen in post-Dplus telemetry.

## Results

The output has no mismatch counters, i.e. all of these were zero in both seed
groups:

```text
conic_relation_mismatch
A_from_conic_a_mismatch
A_Bline_mismatch
Aplus2_Bline_square_mismatch
Aminus2_h90_square_mismatch
candidate_A_formula_mismatch
same_y_multiple_A
Dplus_prefix_failure
```

Group 1:

```text
seeds = 121,122
raw_y_draws = 131072
nonsplit_y = 65766
Dplus_y = 16485
Dplus_candidates = 16398
same_y_single_A = 8199
d3_A_groups = 8199
d3_A_size_2 = 8199
d3_A_mixed_rate = 0
d4_A_after_d3_groups = 4149
d4_A_after_d3_size_2 = 4149
d4_A_after_d3_mixed_rate = 0
d3 plus/minus A groups = 4149 / 4050
d4 plus/minus A groups after d3 = 2031 / 2118
```

Group 2:

```text
seeds = 123,124
raw_y_draws = 131072
nonsplit_y = 65470
Dplus_y = 16454
Dplus_candidates = 16122
same_y_single_A = 8061
d3_A_groups = 8061
d3_A_size_2 = 8061
d3_A_mixed_rate = 0
d4_A_after_d3_groups = 3986
d4_A_after_d3_size_2 = 3986
d4_A_after_d3_mixed_rate = 0
d3 plus/minus A groups = 3986 / 4075
d4 plus/minus A groups after d3 = 1952 / 2034
```

## Interpretation

Positive:

```text
Dplus H90 coordinates have an exact cheap projection to the A-line surface.
A is determined by t alone, equivalently by the conic quotient coordinate a.
Both candidate roots for one y share the same A in the tested rows.
GPU can emit A-level telemetry from y/t without materializing root-dependent A.
```

Negative:

```text
This bridge does not predict d3/d4.
The plus/minus A-group counts remain balanced half-gates.
The H90 payload sign screen is still killed; A_eta signs were tautological or
heldout-flat.
```

## Updated Next Test

Replace the old "find the Dplus-to-A map" task with:

```text
compute the A-level d3 Kummer/divisor class after pulling back through
A = a^4/4 - 2, and compare it with the Dplus H90 second-layer class
A_eta = U_eta + z*W_eta.
```

Promote only if:

```text
the pulled-back d3 class equals, differs by a coboundary from, or shares a
quotient/Prym factor with A_eta;
or the comparison produces a sourceable recurrence controlling later gates.
```

Kill if:

```text
the pulled-back A-level d3 class is independent of the Dplus H90 class and the
successive A-level classes remain fresh half-covers.
```

## Continue / Kill

```text
continue = use A = a^4/4 - 2 as the Dplus/A coordinate bridge
continue = GPU fused-Dplus telemetry should emit A via t if cheap
continue = compare pulled-back A-level d3 class with A_eta
continue = keep A-level Kummer extraction as the mathematical mainline

kill = searching for a new low-degree H90-to-A coordinate map
kill = treating this coordinate bridge as a source-space shrink
kill = more standalone H90 payload sign buckets
```

## Linked Artifacts

- [P27 Sqrt-Beating Test Queue After Coupling Kill](p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md)
- [P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
- [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- [P27 Trace/Norm Dplus H90 Payload Screen](p27_trace_norm_dplus_h90_payload_screen_20260622.md)
- [P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)

```text
p27_trace_norm_dplus_a_coordinate_bridge_rows=1/1
```
