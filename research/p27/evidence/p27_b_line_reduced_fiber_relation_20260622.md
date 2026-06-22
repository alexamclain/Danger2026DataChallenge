# P27 B-Line Reduced-Fiber Relation Screen

Date: 2026-06-22

## Claim

The reduced 4-u / 8-x d3 fiber over legal B does not have a low-degree plane
relation in the screened coordinates through total degree `20`.

This is a negative result for the nearest "maybe the reduced cover is a small
plane curve" route.  It does not kill normalization of the reduced cover, but
it says the next step needs real function-field/CAS work rather than another
visible relation scan.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_b_line_reduced_fiber_relation_probe.py
```

Input fixture:

```text
research/p27/archive/fixtures/p27_b_line_reduced_fiber_fixture_20260622.json
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_reduced_fiber_relation_probe_20260622.txt
```

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_reduced_fiber_relation_probe.py \
  | tee research/p27/archive/probe_outputs/p27_b_line_reduced_fiber_relation_probe_20260622.txt
```

## Systems Screened

The probe tests all-cover rows and sign subcovers in these coordinates:

```text
(B, u)
(B, u^2)
(B, u+2)
(A, u), where A=B^2-2
(lambda, u), where lambda=B/(B+2)
(mu, u), where mu=(B-2)/(B+2)
(B, u) restricted to f3=plus
(B, u) restricted to f3=minus
```

For each system it computes rank/nullity for total degrees:

```text
2,4,6,8,10,12,14,16,18,20
```

and reports only extra nullity beyond interpolation forced by the number of
points.

## Results

Every screened system in q1607, q1847, and q2087 has:

```text
extra_nullity = 0
```

through total degree `20`.

Representative all-cover rows:

```text
q1607 (B,u):
  unique = 196
  degree 18: monomials 190, rank 190, nullity 0, extra 0
  degree 20: monomials 231, rank 196, forced 35, extra 0

q1847 (B,u):
  unique = 252
  degree 20: monomials 231, rank 231, nullity 0, extra 0

q2087 (B,u):
  unique = 228
  degree 18: monomials 190, rank 190, nullity 0, extra 0
  degree 20: monomials 231, rank 228, forced 3, extra 0
```

The plus/minus sign subcovers are also full-rank until forced interpolation.
For example:

```text
q1847 f3=plus:
  unique = 180
  degree 16: monomials 153, rank 153, extra 0
  degree 18: monomials 190, rank 180, forced 10, extra 0

q2087 f3=minus:
  unique = 128
  degree 14: monomials 120, rank 120, extra 0
  degree 16: monomials 153, rank 128, forced 25, extra 0
```

## Interpretation

Positive:

```text
The reduced 4-u fixture remains the right compact CAS input.
The screen rules out a large class of cheap visible plane models.
The plus/minus subcover check directly tests the selector, not only the
all-cover.
```

Negative:

```text
No low-degree relation in (B,u) or the screened B/A/lambda/mu normalizations.
No separate low-degree relation for f3=plus or f3=minus subcovers.
No GPU source follows from a plane-curve model of the reduced fiber.
```

## Continue / Kill

```text
continue = actual normalization/function-field extraction of the reduced 4-u cover
continue = compute genus/components/quotients, not more degree widening
continue = compare f4/f3 only after the reduced f3 cover is understood

kill = low-degree plane relation route for the reduced B-line d3 fiber
kill = plus/minus subcover low-degree relation through degree 20
kill = GPU production from reduced-fiber coordinate buckets
```

```text
p27_b_line_reduced_fiber_relation_rows=1/1
```
