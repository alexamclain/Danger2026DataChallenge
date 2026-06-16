# Trace-Frame Orbit Zero-Lemma Degree Boundary

Date: 2026-06-06

This note records a small but important boundary for the leading
crossed-product p-unit theorem.

## Orbit Product Vanishing Gives Too Few Zeros

For one beta orbit

```text
Omega = beta <Q>,
|Omega| = d,
R_lead,Omega = product_{gamma in Omega} Delta_lead(gamma),
```

a zero of the orbit product gives zeros only on that orbit:

```text
Delta_lead(gamma) = 0 for at least one gamma in Omega
```

and a proof by divisor counting would need a function whose forced vanishing
propagates to all `d` orbit points while its pole degree is strictly less than
`d`.

Thus a zero-lemma proof of one crossed-product orbit factor requires:

```text
pole_degree < |Omega|.
```

For p24,

```text
|Omega| = ord_n(p^5460) = 5549.
```

So any plain or phase-aware divisor proof for a single orbit must exhibit a
selected function of degree below `5549`, or else use a local-intersection
formula rather than zero counting.

## Toy Evidence

The moving trace-frame divisor scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_lead_divisor_support_scan.py \
  --D -10919 --q 11243 --ell 2 --m 4 \
  --factor-index 0 --subdegree 2 \
  --max-heegner-abs-D 1000 --max-heegner-h 20
```

reports:

```text
h=156
factor_degree=12
origin_value_orbit_size=12
rational_degree=78
zero_norm_values=0
distinct_norm_values=13
```

So the already-constructed plain-`j` rational function is on the wrong side
of the zero-lemma inequality:

```text
78 >= 12.
```

This does not show the determinant is zero; in fact the scan has no zero norm
values.  It shows that the nonvanishing cannot be certified by the simple
divisor-counting mechanism.

## p24 Consequence

The analogous half-class scale for the third p24 trace is:

```text
h/2 = 102940198007
```

which is much larger than the beta-orbit size:

```text
102940198007 >> 5549.
```

Therefore a plain-`j` or full-class divisor of this size cannot prove
`R_lead,Omega` is a p-unit by zero counting.  The surviving phase-aware
product route must do one of:

```text
1. construct a genuinely small degree-<5549 phase function for each orbit;
2. construct a Borcherds/Fitting/local-intersection formula proving the
   selected ordinary CM prime has zero local contribution;
3. prove the local module isomorphism directly:
   Fitt_0(coker T_lead,Omega)=A_Omega.
```

This is consistent with:

```text
p24/trace_frame_lead_divisor_support_boundary.md
p24/trace_frame_lead_phase_shape_boundary.md
p24/trace_frame_lead_local_unit_criterion.md
```

and narrows the Borcherds route: it cannot merely recognize a large
plain-`j` divisor; it must retain the non-genus beta/tensor phase or compute
the local intersection multiplicity directly.

## Formal Gate

The finite implication is recorded in:

```text
p24/lean/ZeroLemmaGate.lean
```

with:

```text
orbit_zero_impossible_from_pole_lt_orbit
pinned_trace_frame_plain_j_degree_not_below_orbit
p24_third_trace_half_class_degree_not_below_beta_orbit
```

Lean checks only the finite inequality gate.  The geometry input would still
be the construction of the relevant modular/class-field function and its pole
degree.
