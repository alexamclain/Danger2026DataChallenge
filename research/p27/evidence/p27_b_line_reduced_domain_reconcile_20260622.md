# P27 B-Line Reduced-Domain Reconciliation

Date: 2026-06-22

## Claim

The reduced-cover point-count chart is larger than the frozen selected-source
legal B-domain.  On the actual legal B-domain, the selector-lift profile has
no mixed fibers and exactly matches the known `d3(B)` sign:

```text
d3 plus  <=> selector lift_units = 2
d3 minus <=> selector lift_units = 0
```

The mixed fibers from the point-count probe live outside the selected-source
legal B-domain, mostly outside the core B bucket.  They are chart artifacts for
the moonshot, not a new GPU bucket.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_reduced_domain_reconcile_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_domain_reconcile_probe_20260622.txt
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_reduced_domain_reconcile_probe.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_domain_reconcile_probe_20260622.txt
```

## Results

The frozen reduced-fiber fixture equals `legal_b_maps` in every field:

```text
q1607: fixture_B = 49, legal_b_maps_B = 49, equal = true
q1847: fixture_B = 63, legal_b_maps_B = 63, equal = true
q2087: fixture_B = 57, legal_b_maps_B = 57, equal = true
```

The point-count chart strictly contains the fixture:

```text
q1607: pointcount_B = 100, fixture_B = 49, pointcount_minus_fixture = 51
q1847: pointcount_B = 128, fixture_B = 63, pointcount_minus_fixture = 65
q2087: pointcount_B = 114, fixture_B = 57, pointcount_minus_fixture = 57
```

On the frozen legal fixture rows, selector lift and `d3` sign agree with zero
mismatches:

```text
q1607 fixture:
  lift_units_0 = 21 = d3 minus rows
  lift_units_2 = 28 = d3 plus rows

q1847 fixture:
  lift_units_0 = 18 = d3 minus rows
  lift_units_2 = 45 = d3 plus rows

q2087 fixture:
  lift_units_0 = 32 = d3 minus rows
  lift_units_2 = 25 = d3 plus rows
```

The mixed fibers are outside the fixture:

```text
q1607 pointcount_minus_fixture:
  lift_units_0 = 1
  lift_units_1 = 50

q1847 pointcount_minus_fixture:
  lift_units_0 = 1
  lift_units_1 = 64

q2087 pointcount_minus_fixture:
  lift_units_1 = 57
```

The only point-count/core rows outside the fixture are the small artifact
`B=1` in q1607 and q1847:

```text
q1607 pointcount_core_not_fixture_values = [1]
q1847 pointcount_core_not_fixture_values = [1]
q2087 pointcount_core_not_fixture_values = []
```

## Interpretation

Positive:

```text
The point-count model correctly contains the selected-source legal B-domain.
On that legal domain, the selector layer is exactly the known d3 class.
The apparent mixed lift profile is explained by extra chart points outside the
selected source, not by ambiguity in legal d3.
```

Negative:

```text
The all-chart 0/mixed/full lift profile is not itself a source.
The reduced point-count chart must be cut down by the actual legal/core source
conditions before branch/Kummer extraction.
No GPU production bucket follows from the mixed chart fibers.
```

## Continue / Kill

```text
continue = offline normalize the reduced cover after imposing selected-source legal/core constraints
continue = extract the d3 Kummer class on the frozen legal B-domain
continue = compare f4/f3 only after legal-domain class extraction

kill = treating mixed point-count fibers as legal-source ambiguity
kill = all-chart reduced-lift buckets as a GPU sampler
kill = CAS extraction that ignores the legal/core source cut
```

```text
p27_b_line_reduced_domain_reconcile_rows=1/1
```
