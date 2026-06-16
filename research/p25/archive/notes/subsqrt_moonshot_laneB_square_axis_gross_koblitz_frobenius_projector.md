# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Frobenius Projector

Date: 2026-06-13

## Result

The multi-digit Gross-Koblitz/Stickelberger signature contains a quadratic
Frobenius-frequency projector that extracts exactly the selected q-binomial
anomaly.

For `N=507` or `N=12675`, define:

```text
C(h,t) = sum_i carry_i(h,t)
A(h,t) = sum_i (-1)^i carry_i(h,t)
P(h,t) = selected(h,t) * (C(h,t) - A(h,t)) / ord_N(p)
```

On the p25 seed, this projector is:

```text
P(2,1) = 1
P(h,t) = 0 for every other seed cell
```

After the outer `S` layer, it gives exactly:

```text
S*X^3Y = {138, 310, 482}
```

## Payload Repair

The honest Lucas/binomial payload is:

```text
[1, 1, 1, 1, 2, 1]
```

Subtracting the Frobenius projector gives the all-one selected seed:

```text
binom(h,t) - P(h,t) = 1
```

on all six selected cells.  The lifted quotient terms are exactly the known
18-term residual:

```text
43, 86, 95, 129, 138, 147,
215, 258, 267, 301, 310, 319,
387, 430, 439, 473, 482, 491
```

## Interpretation

This is a stronger Jacobi-side positive artifact than the valuation mask alone:
the full p-orbit carry signature does not merely identify the anomaly support;
its quadratic Frobenius component supplies the finite correction that flattens
the Lucas coefficient anomaly.

It is still not a certificate.  A successful arithmetic producer must realize
this projector as a genuine Hasse-Davenport, Gross-Koblitz unit quotient,
Barnes-delta, or equivalent phase mechanism, then emit a raw candidate vector
that passes the bridge harness.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate.py
```
