# P27 B-Line No-R Closed-Point Pressure

Date: 2026-06-22

## Claim

The no-R reduced B-line cover does not look like a single simple extension
unlock.  Its affine closed points appear in coprime degrees over the small
base fields.

This is not normalization.  It applies the standard Mobius transform to the
existing extension-field point counts:

```text
closed_n = (1/n) * sum_{d|n} mu(d) * #X(F_{q^(n/d)})
```

The purpose is to route the component/quotient/Prym CAS pass: if components
or selected classes only appear after extension, degree `2` and degree `3`
are both mandatory tests.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_closed_point_pressure_probe.py
```

New low-degree count logs:

```text
research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_7_7n2_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_localized_cover_layer_count_probe_23_20260622.txt
```

Closed-point output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_closed_point_pressure_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_noR_closed_point_pressure_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_closed_point_pressure_probe_20260622.txt
```

## Result

Over base `GF(7)`:

```text
degree  noR_points  gamma_points  closed_noR  closed_gamma
1       0           0             0           0
2       8           8             4           4
3       288         144           96          48
4       1688        1680          420         418
5       18880       19520         3776        3904
6       124808      126728        20752       21096
```

Over base `GF(23)`:

```text
degree  noR_points  gamma_points  closed_noR  closed_gamma
1       0           0             0           0
2       648         520           324         260
3       12768       13296         4256        4432
```

In both bases:

```text
closed degree 1 = 0
closed degrees 2 and 3 are both nonzero
degree 2 and degree 3 are coprime
```

## Interpretation

Positive:

```text
The no-R cover still has structured extension behavior worth sending to CAS.
Degree-2 and degree-3 base changes are concrete component-splitting tests.
The gamma class has its own closed-point profile and should be tracked with no-R.
```

Negative:

```text
There is no evidence for a single extension degree that exposes a source.
The closed-point counts do not produce a sampler or GPU mode.
The result strengthens component/Frobenius pressure, not low-genus optimism.
```

## CAS Consequence

The no-R quotient/Prym pass should add this required comparison:

```text
normalize over GF(7^2) and GF(7^3)
normalize over GF(23^2) and GF(23^3), or explain why one base suffices
compute component count and Frobenius permutation on each base change
track whether gamma^2=Unext+2 descends or permutes between components
compare f4/f3 only after the degree-2/degree-3 behavior is understood
```

Promote only if a component, quotient, or Prym factor carrying the selected
class becomes sourceable.  Kill the simple extension-unlock story if degree-2
and degree-3 normalizations both show generic fresh Kummer behavior.

## Continue / Kill

```text
continue = include GF(q^2)/GF(q^3) component comparison in the no-R CAS packet
continue = compute Frobenius component permutation and gamma descent data
continue = use closed-point counts as sanity checks for normalized components

kill = one-extension-degree source story
kill = GPU production from extension-count behavior alone
kill = interpreting no degree-1 points as a sqrt-beating obstruction or win
```

```text
p27_b_line_noR_closed_point_pressure_rows=1/1
```
