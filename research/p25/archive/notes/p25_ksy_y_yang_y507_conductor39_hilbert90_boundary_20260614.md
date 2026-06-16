# P25 KSY-y Yang Y507 Conductor-39 Hilbert-90 Boundary

Updated: 2026-06-14 09:24 PDT

## Purpose

The conductor-`39` Frobenius orbit gate showed that `Frob_p` sends the pure
period-norm character word `W` to `-W`.  This checkpoint records the explicit
Hilbert-90 boundary shape:

```text
W = (1 - Frob_p) V
```

## Balanced Potential

The balanced potential is:

```text
V_bal = W / 2 = -3 * chi_39
```

It has:

```text
support                 = 24
coefficient counts      = (-3,12), (3,12)
Frob_p(V_bal)           = -V_bal
(1 - Frob_p)V_bal       = W
```

On every length-`6` Frobenius orbit, this is the unique gauge minimizing
`L_infinity`; the values are always:

```text
-3, 3, -3, 3, -3, 3
```

## Sparse Potentials

The same boundary has one-coset support-`12` gauges:

```text
V_pos =  6 * 1_{chi_39 = -1}
V_neg = -6 * 1_{chi_39 =  1}
```

Both satisfy:

```text
(1 - Frob_p)V = W
```

The positive sparse support is:

```text
7, 14, 17, 19, 23, 28, 29, 31, 34, 35, 37, 38
```

The negative sparse support is:

```text
1, 2, 4, 5, 8, 10, 11, 16, 20, 22, 25, 32
```

On each Frobenius orbit, support `3` is minimal among integral orbit-constant
gauges; total minimal support is therefore `12`.

## Verdict

Positive payload:

```text
the conductor-39 character word is an integral Hilbert-90 boundary, with a
balanced anti-invariant half-character gauge and sparse one-coset support-12
gauges
```

First missing clause:

```text
the boundary shape is a value-side routing target, not the finite-field
value/divisor theorem or DANGER3 extraction
```

Practical effect:

```text
ask value-side sources for a Hilbert-90 ratio, twisted trace, or sparse
one-coset potential whose (1-Frob_p) boundary is the conductor-39 word; reject
ordinary norm-only claims
```

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_gate.py
```

Marker:

```text
ksy_y_yang_y507_conductor39_hilbert90_boundary_rows=1/1
```
