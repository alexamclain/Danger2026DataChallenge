# P27 B-Line No-R Frobenius Fiber Profile

Date: 2026-06-22

## Claim

The no-R degree-2/degree-3 extension behavior is not explained by one simple
`B`-field-of-definition story.

The active degree-3 points over `GF(7^3)` and `GF(23^3)` sit over degree-3
`B` orbits.  The quadratic fields also show fiber-level extension behavior
above some base-field `B` values.  Therefore the CAS pass must track both:

```text
Frobenius orbits of B-values
quadratic/cubic splitting inside fibers over fixed B
```

The gamma profile is stable on Frobenius orbits in this finite-field test, so
gamma descent/permutation is a well-posed normalized-cover question rather
than visible orbit noise.

Coordinate-degree follow-up:
[P27 B-Line No-R Coordinate Degree Profile](p27_b_line_noR_coordinate_degree_20260622.md).
The cubic activity is genuinely degree-3 `B`-orbit activity, while quadratic
activity can be hidden fiber activity over base-field `B`: over `GF(7^2)` all
eight no-R points have base-field `B`, `X`, `beta`, `x5`, `U`, and selector,
with extension only in `W` or `T`; over `GF(23^2)` the quadratic behavior is a
mix of degree-2 `B` orbits and fixed-`B` fiber extensions.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_noR_frobenius_fiber_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_noR_frobenius_fiber_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_noR_frobenius_fiber_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_noR_frobenius_fiber_probe_20260622.txt
```

## Result

Summary by field:

```text
GF(7^2):
  active B-orbits = 1
  active degree-1 B fibers = 1
  active degree-2 B fibers = 0
  orbit signature mismatches = 0

GF(7^3):
  active B-orbits = 6
  active degree-1 B fibers = 0
  active degree-3 B fibers = 18
  orbit signature mismatches = 0

GF(23^2):
  active B-orbits = 12
  active degree-1 B fibers = 5
  active degree-2 B fibers = 14
  orbit signature mismatches = 0

GF(23^3):
  active B-orbits = 266
  active degree-1 B fibers = 0
  active degree-3 B fibers = 798
  orbit signature mismatches = 0
```

Degree-3 orbit summaries:

```text
GF(7^3):
  orbit(deg=3, noR=48, gamma=0)  = 3
  orbit(deg=3, noR=48, gamma=48) = 3

GF(23^3):
  orbit(deg=3, noR=48, gamma=48) = 133
  orbit(deg=3, noR=48, gamma=96) = 72
  orbit(deg=3, noR=48, gamma=0)  = 61
```

Quadratic behavior:

```text
GF(7^2):
  the only active orbit is degree-1 in B, but the no-R points do not exist over GF(7)

GF(23^2):
  both base-field B fibers and degree-2 B fibers are active
```

## Interpretation

Positive:

```text
The closed-point pressure is now localized to B-orbit and fiber-splitting data.
Degree-3 activity is genuinely over degree-3 B orbits in both base families.
Gamma counts are Frobenius-stable on B-orbits, making descent/permutation testable.
```

Negative:

```text
There is no single B-degree source law.
There is no visible GPU sampler from the Frobenius profile alone.
Quadratic activity includes fiber-level splitting above base B values, so a
simple B-orbit quotient would miss part of the behavior.
```

## CAS Consequence

The no-R quotient/Prym pass should explicitly report:

```text
component count over base field
component count after degree-2 and degree-3 base change
Frobenius permutation on components
whether active degree-3 B orbits lie on a separate component/quotient
whether quadratic points over base-field B are singular/boundary artifacts or genuine fiber splitting
whether gamma descends on each component or changes only after a fiber extension
```

Promote only if this produces a named low-genus component/quotient/Prym factor
that carries gamma or couples f3/f4.  Kill any proposal that only says
"restrict to degree-3 B" without a direct sampler, because that is an
extension-field diagnostic, not a p27 source.

## Continue / Kill

```text
continue = run normalized no-R component/Frobenius test over q^2 and q^3
continue = distinguish B-orbit degree from fiber-extension degree above fixed B
continue = track gamma descent separately on degree-3 B orbits and quadratic base-B fibers
continue = split quadratic fixed-B fiber tests into W/T-only and beta/x5/U subcovers

kill = single B-degree source law
kill = GPU production from Frobenius B-orbit buckets alone
kill = interpreting Frobenius-stable counts as a descent proof without divisors
kill = treating degree-2 and degree-3 activity as the same mechanism
```

```text
p27_b_line_noR_frobenius_fiber_rows=1/1
```
