# P27 B-Line Gamma Class Handoff

Date: 2026-06-22

## Claim

The remaining B-line moonshot has been converted into a concrete
CAS/GPU/expert handoff.  The first class to extract is:

```text
gamma^2 = v + 2
```

on the generic transition over the `f3=+1` reduced B-line layer:

```text
A = B^2 - 2
H^2 = u + 2
F_A(u,v) = (v^2 - 4)^2 - 4*u*(v^2 - 4)*(v + A) + 16*(v + A)^2 = 0
```

The materialization layer

```text
rho^2 = v^2 - 4
```

is orientation data, not the first Kummer class to extract.  In the guard
fields, `chi(v+2)` is already constant on all four generic transition roots.

## Artifacts

Generator:

```text
research/p27/archive/gates/p27_b_line_gamma_class_handoff.py
```

Readable packet:

```text
research/p27/archive/probe_outputs/p27_b_line_gamma_class_handoff_20260622.txt
```

JSON fixture:

```text
research/p27/archive/fixtures/p27_b_line_gamma_class_handoff_20260622.json
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_class_handoff.py \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_b_line_gamma_class_handoff_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_gamma_class_handoff.py \
  --small-primes 1607,1847,2087 \
  --json \
  > research/p27/archive/fixtures/p27_b_line_gamma_class_handoff_20260622.json
```

## Guard-Field Shape

The packet freezes every active `(B,u)` parent in the p27-signature fields.

```text
q1607: rows=112, B=28, f4 plus/minus=76/36, generic4=112, actual2=112, missing2=112
q1847: rows=180, B=45, f4 plus/minus=76/104, generic4=180, actual2=180, missing2=180
q2087: rows=100, B=25, f4 plus/minus=72/28, generic4=100, actual2=100, missing2=100
```

The checks have zero failures for:

```text
F_A(u,v)=0 on the generic roots
actual roots subset generic roots
chi(v+2) constant on the generic four-root transition
Norm_generic(v+2) = 16*(A-2)^2
actual/missing two-root gamma norms square
H^2 = u + 2
r=(v0+2)/(v1+2), r+1/r=u
(h+1/h)^2=u+2 when h^2=r
```

## Interpretation

Positive:

```text
The f4/f3 class is now packaged as an exact staged Kummer-class problem.
The class to extract first is gamma^2=v+2 on the generic transition.
The materialization characters chi(v^2-4) and chi(v+A) are separated from the
gamma class so a CAS pass can avoid chasing the wrong half-cover.
```

Negative:

```text
This is not a production GPU sampler yet.
The previous visible norm, H90 quotient, and f3/H90-coordinate screens remain
killed.
The packet does not promote B-line buckets or one-sided small-field tails.
```

Extension-count update:
[P27 B-Line Gamma Extension Count](p27_b_line_gamma_extension_count_20260622.md)
checks the same reduced source chart over `GF(607)`, `GF(7^3)`, `GF(7^4)`,
`GF(7^5)`, `GF(23^2)`, and `GF(23^3)`.  It finds
`selector_gamma_points = materialized_x6_points` in every tested field, with
larger odd extension selector rates near `1/2`.  Thus `gamma^2=v+2` is not a
direct source sampler or GPU bucket; the remaining value of this handoff is
offline Kummer/divisor-class extraction.

Specialized squareclass update:
[P27 B-Line Gamma Specialized Square Smoke](p27_b_line_gamma_specialized_square_smoke_20260622.md)
checks two one-parameter function-field specializations of the visible
`B/H/Y` transition.  In both, the transition quartic is irreducible and
`Y=v+2` is not square, while `Norm(Y)` has the expected square form.  This
kills the visible universal claim that gamma is already square over the `B/H`
layer, but does not replace normalization of the actual no-R reduced base.

## Concrete Tests

First CAS test:

```text
Normalize the f3-plus B-u-H base using the reduced-cover symbolic packet.
Record genus, components, branch support, and involutions/quotients.
```

Second CAS test:

```text
On F_A(u,v)=0 over that base, compute div(v+2) modulo squares.
Classify gamma as pullback, coboundary, translate, quotient class, or fresh
independent half-cover.
```

Third test:

```text
Repeat after f4-plus and compare the f5/f4 class with gamma.
Promote only if one class or recurrence controls multiple selected gates.
```

GPU is useful only after one of those tests names a coordinate/quotient to emit,
or as bounded telemetry that reports the same staged coordinates with a raw
source denominator.

## Continue / Kill

```text
continue = normalize the f3-plus B-u-H base
continue = extract div(v+2) / Kummer class for gamma over that base
continue = use the specialized square smoke as a regression for visible B/H claims
continue = compare gamma with the next f5/f4 class
continue = use GPU only for named-class telemetry or a direct sampler test

kill = treating rho^2=v^2-4 materialization as the moonshot class
kill = visible B/H/tau relation scans without a new named class
kill = B-line GPU buckets without raw-source accounting
kill = one-sided guard-field f5/f6 tails as recurrence evidence
```

```text
p27_b_line_gamma_class_handoff_rows=1/1
```
