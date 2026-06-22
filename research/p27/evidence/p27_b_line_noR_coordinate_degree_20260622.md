# P27 B-Line No-R Coordinate Degree Profile

Date: 2026-06-22

## Claim

The no-R extension behavior splits into two different mechanisms:

```text
degree-3 activity is B-orbit activity
degree-2 activity can be hidden fiber activity over fixed B
```

This is a sharper routing result than the closed-point and B-orbit probes
alone.  The coordinate-degree profile says which variables force the extension
degree for each no-R `U_next` point.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_coordinate_degree_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_coordinate_degree_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_coordinate_degree_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_coordinate_degree_probe_20260622.txt
```

## Result

Degree-2 base `7`:

```text
GF(7^2):
  noR_U_points = 8
  B_degree_1 = 8
  point_degree_2 = 8
  source_fiber_over_base_B = 8
  gamma_chi_0 = 8

  dominant vectors:
    (B,X,W,T,beta,x5,U,selector,point,gamma)
    (1,1,2,1,1,1,1,1,2,0) = 4
    (1,1,1,2,1,1,1,1,2,0) = 4
```

So over `GF(7^2)`, the no-R points are above base-field `B`, with base-field
`X`, `beta`, `x5`, `U`, and selector.  The extension is only in `W` or `T`,
and the selector is the zero branch.

Degree-3 bases:

```text
GF(7^3):
  B_degree_3 = 288
  point_degree_3 = 288
  source_B_orbit = 288
  gamma_chi_-1 / +1 = 216 / 72

GF(23^3):
  B_degree_3 = 12768
  point_degree_3 = 12768
  source_B_orbit = 12768
  gamma_chi_-1 / +1 = 6120 / 6648
```

Thus cubic activity is genuinely carried by degree-3 `B` orbits in both base
families.

Degree-2 base `23` is mixed:

```text
GF(23^2):
  noR_U_points = 648
  B_degree_1 = 264
  B_degree_2 = 384
  source_fiber_over_base_B = 264
  source_B_orbit = 384
  gamma_chi_-1 / 0 / +1 = 384 / 8 / 256
```

The base-`B` quadratic points include several layer patterns: some force
extension only at `beta/x5/U/selector`, some already at hidden `X/W/T`, and
the zero selector appears in the same small `W/T`-only pattern seen over
`GF(7^2)`.

## Interpretation

Positive:

```text
The CAS pass now has a layer-by-layer routing target.
Cubic activity should be studied as a B-orbit/component phenomenon.
Quadratic activity should be studied as fiber splitting over fixed B, with
separate W/T and beta/x5/U subcases.
```

Negative:

```text
There is no single coordinate-degree law that selects gamma.
The degree-2 behavior is not just a B-orbit quotient.
The degree-3 behavior is not a hidden fixed-B fiber shortcut.
No GPU sampler follows from coordinate degrees alone.
```

## CAS Consequence

Split the no-R quotient/Prym task into two subtests:

```text
1. Cubic B-orbit subtest:
   normalize/quotient the no-R cover over degree-3 B orbits and test whether
   gamma or f4/f3 descends to a low-genus B-orbit quotient.

2. Quadratic fixed-B fiber subtest:
   for base-field B fibers, separate W/T-only extension from beta/x5/U
   extension, then compute whether either quadratic subcover carries the
   selected gamma class or is only a tower artifact.
```

Promote only if one subtest produces a direct source map, recurrence, or
low-genus quotient/Prym factor carrying the selected class.  Kill the no-R
first-pass route if both subtests are generic fresh Kummer behavior.

## Continue / Kill

```text
continue = cubic B-orbit component/quotient test
continue = quadratic fixed-B fiber subcover test split by W/T vs beta/x5/U
continue = compare gamma and f4/f3 separately in the cubic and quadratic mechanisms

kill = one coordinate-degree selector law
kill = treating degree-2 and degree-3 activity as the same mechanism
kill = GPU production without a named source map from one subtest
```

```text
p27_b_line_noR_coordinate_degree_rows=1/1
```
