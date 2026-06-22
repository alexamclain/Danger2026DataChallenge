# P27 Trace/Norm Dplus X6/U-Class

Date: 2026-06-22

## Claim

After the exact `Dplus -> A` coordinate bridge, the next selected gate has a
smaller concrete class target.

For same-stream `Dplus` rows, write:

```text
t = y - 1
A = (t - 1/t)^4/4 - 2
U = x6 + 1/x6
d3 = chi(x6^2 + A*x6 + 1)
```

Then:

```text
each y has 4 U values and 8 x6 values;
each U fiber is the reciprocal pair x6, 1/x6;
chi(U + A) = +1 on every tested branch;
d3 = chi(x6) on the whole Dplus second-halving sheet;
all 8 x6 branches over one y have the same squareclass.
```

So the post-Dplus `d3` class is not a generic sign attached to every branch of
the halving tree.  It is the squareclass of the `x6` quadratic layer after
`U+A` has already become square.  This is still not a production source, but
it gives a sharper CAS comparison target than the previous generic A-level
statement.

Follow-up visible-formula screen:
[P27 Trace/Norm Dplus Four-U Rational Screen](p27_trace_norm_dplus_ucover_rational_screen_20260622.md)
tests whether the elementary coefficients of the four-`U` quartic are
low-degree rational functions of `t`, `a=t-1/t`, or `A`.  The answer is
negative through degree `(20,20)` on a `100` train / `50` heldout screen.
So the four-`U` object remains a CAS cover/class target, not a cheap visible
base formula.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_x6_uclass_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_x6_uclass_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_x6_uclass_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-y 0 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_x6_uclass_probe_20260622.txt
```

## Identity

For every nonzero `x6`,

```text
x6^2 + A*x6 + 1 = x6*(x6 + 1/x6 + A) = x6*(U + A).
```

Thus:

```text
d3 = chi(x6)*chi(U + A).
```

The probe shows `chi(U + A)=+1` on every tested Dplus branch, hence:

```text
d3 = chi(x6).
```

This turns the post-Dplus next-gate question into a squareclass question for
the `x6` layer over the four-branch `U` cover.

## Results

Group 1:

```text
seeds = 121,122
raw_y_draws = 131072
nonsplit_y = 65766
Dplus_y = 16485
Dplus_candidates = 16398
analyzed_y = 8199
y_x5_count_4 = 8199
y_U_count_4 = 8199
y_x6_count_8 = 8199
U_fiber_size_2 = 32796
chi_UplusA_+1 = 65592
chi_UplusA_-1 = 0
y_UplusA_all_square = 8199
y_d3_constant = 8199
y_d3_constant_+1 = 4149
y_d3_constant_-1 = 4050
y_chix6_constant = 8199
```

Group 2:

```text
seeds = 123,124
raw_y_draws = 131072
nonsplit_y = 65470
Dplus_y = 16454
Dplus_candidates = 16122
analyzed_y = 8061
y_x5_count_4 = 8061
y_U_count_4 = 8061
y_x6_count_8 = 8061
U_fiber_size_2 = 32244
chi_UplusA_+1 = 64488
chi_UplusA_-1 = 0
y_UplusA_all_square = 8061
y_d3_constant = 8061
y_d3_constant_+1 = 3986
y_d3_constant_-1 = 4075
y_chix6_constant = 8061
```

The output contains no mismatch counters for:

```text
d3_factor_mismatch
U_reciprocal_pair_mismatch
candidate_A_formula_mismatch
d1_failure
d2_failure
```

## Interpretation

Positive:

```text
The post-Dplus d3 class has a named geometric location: the x6 squareclass.
The U+A part of the d3 discriminant is already forced square.
The four U values are the right reciprocal-reduced object; the eight x6 values
are just the quadratic x6 + 1/x6 = U layer.
All x6 branches over one y have the same squareclass in the tested rows.
```

Negative:

```text
The y-level d3 plus/minus counts remain balanced.
This is not a source-space shrink unless the x6 squareclass is sourceable,
recurrent, or related to the H90 payload class.
The GPU should not run another x6 sign bucket without a named source law.
```

## Updated CAS Target

Use the solved coordinate bridge:

```text
A = (t - 1/t)^4/4 - 2
```

Then build the post-Dplus second-halving cover:

```text
U = x6 + 1/x6
```

with the four observed `U` branches over one `Dplus` row.  The next class is:

```text
x6 squareclass on x6^2 - U*x6 + 1 = 0.
```

Compare this class with the Dplus H90 second-layer payload:

```text
A_eta = U_eta + z*W_eta.
```

Promote if:

```text
chi(x6) equals, differs by a coboundary from, or shares a quotient/Prym factor
with A_eta;
or the four-U cover admits a low-genus/sourceable recurrence that controls
d3 and later gates.
```

Kill if:

```text
the x6 squareclass is fresh and independent of the H90 payload and successive
A-level classes.
```

## Continue / Kill

```text
continue = derive/eliminate the four-U cover over t or the H90 base
continue = compare the x6 squareclass with A_eta
continue = route A-level d3 extraction through this Dplus pullback model
continue = GPU fused-Dplus telemetry may emit U/x6 only as support for this
           class comparison

kill = searching U+A; it is already square in the tested Dplus domain
kill = low-degree rational formulas for the four-U quartic coefficients in
       t,a,A through degree 20
kill = treating d3 as an arbitrary eight-branch sign
kill = GPU production from x6 buckets before a source/coboundary exists
```

## Linked Artifacts

- [P27 Trace/Norm Dplus A-Coordinate Bridge](p27_trace_norm_dplus_a_coordinate_bridge_20260622.md)
- [P27 Trace/Norm Dplus Four-U Rational Screen](p27_trace_norm_dplus_ucover_rational_screen_20260622.md)
- [P27 Sqrt-Beating Test Queue After Coupling Kill](p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md)
- [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- [P27 Trace/Norm Dplus H90 Payload Screen](p27_trace_norm_dplus_h90_payload_screen_20260622.md)
- [P27 A-Level Kummer Extraction Packet](p27_a_level_kummer_extraction_packet_20260622.md)

```text
p27_trace_norm_dplus_x6_uclass_rows=1/1
```
