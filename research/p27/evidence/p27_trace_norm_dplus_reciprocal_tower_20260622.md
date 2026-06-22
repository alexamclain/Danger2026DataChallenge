# P27 Trace/Norm Dplus Reciprocal Tower

Date: 2026-06-22

## Claim

The post-Dplus `x6` class now has an explicit reciprocal-coordinate tower.

For same-stream `Dplus` rows:

```text
t = y - 1
A = (t - 1/t)^4/4 - 2
X = xp + 1/xp = t^3 + 2*t^2 - 1/t
```

The two candidate `xp` roots are reciprocal, so `X` is a function of `t`
alone.  The subsequent selected reciprocal coordinates satisfy:

```text
F_A(X,U5) = 0
F_A(U5,U6) = 0
```

where:

```text
U5 = x5 + 1/x5
U6 = x6 + 1/x6
F_A(U,V) =
  (V^2 - 4)^2
  - 4*U*(V^2 - 4)*(V + A)
  + 16*(V + A)^2.
```

The next selected class remains:

```text
d3 = chi(x6)
```

on:

```text
x6^2 - U6*x6 + 1 = 0.
```

This is a positive structural object.  It replaces generic A-level language
with a concrete tower:

```text
t -> X -> U5 -> U6 -> x6 squareclass.
```

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-y 0 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_probe_20260622.txt
```

## CAS Fixture

Magma fixture:

```text
research/p27/archive/fixtures/p27_trace_norm_dplus_reciprocal_tower_q7_magma.m
```

It includes:

```text
t*it = 1
4*A*t^4 = t^8 - 4*t^6 - 2*t^4 - 4*t^2 + 1
X*t = t^4 + 2*t^3 - 1
F_A(X,U5) = 0
F_A(U5,U6) = 0
R5^2 = U5^2 - 4
H5^2 = U5 + A
R6^2 = U6^2 - 4
H6^2 = U6 + A
x6^2 - U6*x6 + 1 = 0
```

The fixture does not impose `x6` square.  That squareclass is the class to
compare with H90 `A_eta`.

## Results

Group 1:

```text
seeds = 121,122
raw_y_draws = 131072
nonsplit_y = 65766
Dplus_y = 16485
analyzed_y = 8199
xp_reciprocal_pair = 8199
U5_count_2 = 8199
U6_count_4 = 8199
U5_fiber_size_2 = 16398
U6_fiber_size_2 = 32796
U5_disc_+1 = 32796
U5_plusA_+1 = 32796
U6_disc_+1 = 65592
U6_plusA_+1 = 65592
```

Group 2:

```text
seeds = 123,124
raw_y_draws = 131072
nonsplit_y = 65470
Dplus_y = 16454
analyzed_y = 8061
xp_reciprocal_pair = 8061
U5_count_2 = 8061
U6_count_4 = 8061
U5_fiber_size_2 = 16122
U6_fiber_size_2 = 32244
U5_disc_+1 = 32244
U5_plusA_+1 = 32244
U6_disc_+1 = 64488
U6_plusA_+1 = 64488
```

The output contains no mismatch/failure counters for:

```text
X_formula_mismatch
F_X_U5_mismatch
F_U5_U6_mismatch
d3_chix6_mismatch
candidate_A_formula_mismatch
xp_reciprocal_pair_failure
U5_reciprocal_pair_mismatch
U6_reciprocal_pair_mismatch
d1_failure
d2_failure
```

Small-field descent follow-up:
[P27 Trace/Norm Dplus Reciprocal Tower Small-Field Descent](p27_trace_norm_dplus_reciprocal_tower_smallfield_descent_20260622.md)
shows that this tower should not be promoted as a standalone source sampler.
In exact enumerations over q607/q1607/q1847, the next class
`d3=chi(x6)=chi(U6+2)` has mixed `A`/`B` fibers on the naked tower, even after
the materialization filters.  Therefore the selected legal/core source cut is
essential before comparing this class with H90 `A_eta` or the A/B/K Kummer
sequence.

Row-bit/resultant follow-up:
[P27 Trace/Norm Dplus U6 Row-Bit Resultant](p27_trace_norm_dplus_u6_rowbit_resultant_20260622.md)
adds the sharper p27 fact: inside the actual Dplus stream, the four `U6`
branches over one row all have the same `chi(U6+2)`.  The class is a balanced
descended row bit.  Symbolically, the eliminated `R(t,U6)` has square
specializations at `U6=+/-2`, while `R(t,S^2-2)` does not factor over `Q`.
Thus the next task is sourcing the row bit, not choosing among branches.

## Interpretation

Positive:

```text
The root-dependent candidate stage collapses to one rational X(t).
The post-Dplus branch structure is an iterated F_A reciprocal tower.
U5 has two reciprocal fibers; U6 has four reciprocal fibers.
U5^2-4, U5+A, U6^2-4, and U6+A are all square in the tested rows.
The only remaining next-gate squareclass is the descended U6/x6 row bit.
```

Negative:

```text
This does not itself source chi(x6).
The four-U coefficients still have no low-degree rational formula in t,a,A
through degree (20,20).
GPU production is not justified until the x6 class is sourced or related to
H90 A_eta.
```

## Updated Next Test

Normalize or decompose the tower:

```text
F_A(X(t),U5) = 0
F_A(U5,U6) = 0
x6^2 - U6*x6 + 1 = 0
```

with the side square variables:

```text
U5^2 - 4, U5 + A, U6^2 - 4, U6 + A.
```

Then compare the `x6` squareclass with:

```text
A_eta = U_eta + z*W_eta.
```

Promote if:

```text
the tower has a low-genus/sourceable quotient,
or chi(x6) is a coboundary/pullback/Prym companion of A_eta,
or the tower yields a recurrence controlling d3 and later gates.
```

Kill if:

```text
the normalized tower is generic/high-genus and chi(x6) is independent of A_eta.
```

## Continue / Kill

```text
continue = run offline Magma/Sage normalization on the q7 fixture
continue = extract the x6 Kummer class over the reciprocal tower
continue = compare the descended U6 row bit with H90 A_eta
continue = compare that class with H90 A_eta

kill = generic A-level d3 language without the reciprocal tower
kill = visible t/a/A coefficient fitting for the four-U cover
kill = U6 branch-choice buckets after Dplus
kill = GPU x6 bucket production before a source/coboundary exists
kill = naked reciprocal-tower source sampling without the selected legal/core cut
```

## Linked Artifacts

- [P27 Trace/Norm Dplus X6/U-Class](p27_trace_norm_dplus_x6_uclass_20260622.md)
- [P27 Trace/Norm Dplus U6 Row-Bit Resultant](p27_trace_norm_dplus_u6_rowbit_resultant_20260622.md)
- [P27 Trace/Norm Dplus Four-U Rational Screen](p27_trace_norm_dplus_ucover_rational_screen_20260622.md)
- [P27 Trace/Norm Dplus Reciprocal Tower Small-Field Descent](p27_trace_norm_dplus_reciprocal_tower_smallfield_descent_20260622.md)
- [P27 Trace/Norm Dplus A-Coordinate Bridge](p27_trace_norm_dplus_a_coordinate_bridge_20260622.md)
- [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- [P27 Sqrt-Beating Test Queue After Coupling Kill](p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md)

```text
p27_trace_norm_dplus_reciprocal_tower_rows=1/1
```
