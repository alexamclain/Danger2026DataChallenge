# Trace-Frame Leading Phase-Recurrence Boundary

Date: 2026-06-06

This note tests another cheap phase-aware explanation for the leading
crossed-product p-unit theorem.

## Question

The leading determinant norm is not a low-degree function of plain `j`, and
not a low-bidegree function of one oriented edge.  A weaker possibility is:

```text
the phase-period sequence has unusually low linear recurrence complexity.
```

If true, the beta/origin product might be compressed by a small recurrence
norm rather than a full determinant-line p-unit theorem.

## Tool

The audit script is:

```text
p24/trace_frame_lead_phase_recurrence_audit.py
```

It:

```text
1. computes the leading determinant norm over every origin in a small CM row;
2. extracts the minimal period;
3. runs Berlekamp-Massey over F_q on one period repeated twice;
4. compares against random controls with the same period and nonzero status.
```

## Pinned Moving Row

For the moving `D=-10919, q=11243, m=4` trace-frame row:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_lead_phase_recurrence_audit.py \
  --D -10919 --q 11243 --ell 2 --m 4 \
  --factor-index 0 --subdegree 2 --random-trials 80
```

reported:

```text
value_count=156
period=13
orbit_size=12
distinct_period_values=13
zero_period_values=0
actual order=13
order_over_period=1.000000
connection=[1,0,0,0,0,0,0,0,0,0,0,0,0,-1]
characteristic_divides_T^period_minus_1=1
random order_hist={13: 80}
```

The sibling checks gave the same result:

```text
m=4, factor_index=1: order=13, random_order_hist={13:40}
m=3, factor_index=0: order=13, random_order_hist={13:40}
```

## Interpretation

The determinant norm has phase structure:

```text
period=13, orbit_size=12.
```

But its phase recurrence is generic for a nonzero period-13 sequence over
`F_11243`.  The only recurrence is the tautological periodicity:

```text
a_{t+13} = a_t.
```

So the low-recurrence phase shortcut is not visible in the relevant moving
trace-frame rows.

## Consequence

This closes a third easy phase route:

```text
plain-j low divisor degree;
single-edge low bidegree;
low linear recurrence in the phase period.
```

The surviving theorem remains determinant-line/local:

```text
R_lead,Omega is a p-unit
```

proved by a genuine phase-aware Fitting/Borcherds/local-intersection identity,
or by a direct proof that the orbit algebra map

```text
T_lead,Omega
```

is an isomorphism modulo the selected ordinary prime.
