# P27 Trace/Norm Dplus Reciprocal Tower Small-Field Descent

Date: 2026-06-22

## Claim

The reciprocal tower isolated after `Dplus` is a good CAS comparison object,
but it is not a standalone source sampler.

Exact enumeration over small fields shows that the bare tower has mixed
`A`/`B` fibers for the next class:

```text
d3 = chi(x6) = chi(U6 + 2)
```

after:

```text
A = (t - 1/t)^4/4 - 2
B = (t^2 - 1)^2 / (2*t^2)
X = t^3 + 2*t^2 - 1/t
F_A(X,U5) = 0
F_A(U5,U6) = 0.
```

Thus the earlier p27 same-stream fact that post-`Dplus` `d3/d4` descend to
whole `A` fibers depends on the selected legal/core source cut.  It should not
be generalized to the naked reciprocal tower.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe.py \
  --fields 607 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe.py \
  --fields 1607,1847 \
  | tee -a research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe.py \
  --fields 607 \
  --no-materialization-filters \
  | tee -a research/p27/archive/probe_outputs/p27_trace_norm_dplus_reciprocal_tower_smallfield_probe_20260622.txt
```

The default run keeps the materialization filters:

```text
chi(U5^2 - 4) = +1
chi(U5 + A) = +1
chi(U6^2 - 4) = +1
chi(U6 + A) = +1
```

## Result

With materialization filters:

```text
field  active A/B groups  mixed A/B groups  mixed rate  d3 plus/minus
607    48                 16                0.333333    256/256
1607   78                 28                0.358974    448/400
1847   109                45                0.412844    720/512
```

Over q607 without materialization filters:

```text
active A/B groups = 66
mixed A/B groups  = 32
mixed rate         = 0.484848
d3 plus/minus/zero = 514/520/8
```

In all tested fields, the exact `A`, `B`, and joint `A,B` group summaries have
the same mixed counts.  The p27-signature fields `q=1607` and `q=1847` both
show substantial mixed fibers.

## Interpretation

Positive:

```text
The reciprocal tower is exact and small enough for deterministic small-field
descent checks.
The materialization filters reduce the mixed rate but do not make d3 a bare
tower-level A/B class.
This gives a clean falsifier for a standalone reciprocal-tower source sampler.
```

Negative:

```text
The naked tower does not carry a base A/B Kummer class for d3.
The selected legal/core source equations are essential.
GPU should not sample F_A(X,U5), F_A(U5,U6) as a production source without
also enforcing the selected source cut.
```

## Consequence

Keep the cross-lane comparison, but narrow it:

```text
compare the pulled-back selected-source d3 class with H90 A_eta;
do not compare the naked reciprocal tower to A_eta as if it were the source;
do not launch a GPU tower sampler unless it includes the legal/core cut and
reports raw source denominators.
```

For CAS, this strengthens the current A/B/K instruction:

```text
normalize the selected legal/core cover first;
then attach the reciprocal tower or gamma layer;
then compare Kummer classes.
```

## Continue / Kill

```text
continue = selected-source A/B/K Kummer extraction
continue = Dplus same-stream telemetry that carries A, x6, and A_eta columns
continue = reciprocal tower as a local class-comparison object after source cut

kill = naked reciprocal-tower source sampler
kill = interpreting tower-level A/B descent from p27 same-stream Dplus data
kill = GPU production from F_A tower roots without legal/core denominator accounting
```

## Linked Artifacts

- [P27 Trace/Norm Dplus Reciprocal Tower](p27_trace_norm_dplus_reciprocal_tower_20260622.md)
- [P27 Trace/Norm Dplus X6/U-Class](p27_trace_norm_dplus_x6_uclass_20260622.md)
- [P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
- [P27 A/B/K Symbolic Kummer CAS Brief](p27_abk_symbolic_kummer_cas_brief_20260622.md)
- [P27 Sqrt-Beating Test Queue After Coupling Kill](p27_sqrt_beating_test_queue_after_coupling_kill_20260622.md)

```text
p27_trace_norm_dplus_reciprocal_tower_smallfield_descent_rows=1/1
```
