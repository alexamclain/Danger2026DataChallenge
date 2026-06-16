# Trace-GCD Nonvacuous Rowspace Search Status

Date: 2026-06-06

## Question

The lambda-plateau bridge audit currently passes vacuously on p24-shaped
small actual-CM rows:

```text
B_leading has full rank, so there is no bad lambda.
```

The most useful next falsifier would be a small actual-CM row where:

```text
1. left/right Frobenius orbit lengths are coprime, as in p24;
2. after deleting one right orbit, at least left_degree leading coordinates remain;
3. B_leading has a genuine kernel;
4. rowspace(C_plateau) subset rowspace(B_leading) can be tested nonvacuously.
```

This would decide whether the plateau bridge has independent content beyond
the leading p-unit theorem.

## Bounded Search

I ran:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/hermitian_mixed_left_subfield_normality_audit.py \
  --summary-only --max-rows 8 --max-cases 20 --max-h 180 \
  --max-abs-D 60000 --q-stop 120000 --max-splitting-primes 1 \
  --max-axis-dim 40 --max-m 84 --min-factor-degree 2 \
  --max-factor-degree 12 --max-extension-degree 12 --include-linear \
  --min-left-orbit-len 3 --require-coprime-lens \
  --max-lambda-enumeration 50000
```

The scan finished in about 30 seconds and reported:

```text
rows=8
tests=52
coprime_left_right_tests=36
left_subfield_failures=0
annihilator_degree_mismatches=0
centered_profile_rank_mismatches=0
full_left_span_tests=28
delete_one_leading_full_tests=16
max_left_orbit_len=4
max_delete_one_leading_min_rank=2
centered_trace_one_support_tests=8
min_centered_trace_right_orbit_support=1
```

The verbose four-row version exposed the boundary:

```text
D=-3351, -3639, -3951:
  (5,3) has left_degree=4 and coprime right orbit lengths,
  but deleting one right orbit leaves only one coordinate.

D=-4319:
  (7,4) has left_degree=3 and coprime right orbit lengths,
  but deleting one right orbit leaves only one or two coordinates.

D=-4319:
  (7,7) has enough coordinates after deletion and leading rank 2 < 3,
  but the left/right orbit degrees are both 3, not coprime.
```

So this bounded pass found genuine low-rank actual-CM controls, but not a
clean p24-shaped nonvacuous rowspace-containment test.

## Consequence

This strengthens the current interpretation:

```text
small p24-shaped actual-CM rows support the leading p-unit route;
nearby nonvacuous failures are explained by dimension or noncoprime-degree
boundaries;
the plateau bridge remains unproved, not falsified.
```

The next nonvacuous search should be two-stage:

```text
1. shortlist discriminants by qfbclassno/divisor/orbit geometry only;
2. only then run polclass and the rowspace/plateau audit.
```

The geometry filter should require:

```text
left_degree >= 3,
gcd(left_degree, right_orbit_len)=1 for every right orbit,
total_right_coordinates_after_one_deletion >= left_degree,
packet_degree >= left_degree,
at least two right Frobenius orbits after deletion.
```

The first-stage filter is now:

```text
p24/trace_gcd_nonvacuous_geometry_filter.py
```

A bounded geometry-only run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_nonvacuous_geometry_filter.py \
  --max-h 220 --max-abs-D 60000 --q-stop 20000 \
  --max-extension-degree 16 --max-hits 12
```

found dimension-possible shapes immediately, led by:

```text
D=-15791, h=195, m=65, n=3, pair=(5,13),
left_len=4, right_lens=[3,3,3,3],
prefix_lengths=[3,3,3,3], tail_lengths=[1,1,1,1].
```

Those `q` values were only orbit-geometry candidates; direct actual-rowspace
checks showed they were not full split-cycle rows.  The filter now has an
optional:

```text
--require-full-cycle
```

gate, but a bounded run with that option was stopped after about a minute
without output.  Therefore the split-cycle gate is useful for deliberate
calibration hunting, not for the default fast theorem microscope.

Without those filters the scan mostly rediscovers expected dimension
obstructions instead of testing the p24 theorem shape.
