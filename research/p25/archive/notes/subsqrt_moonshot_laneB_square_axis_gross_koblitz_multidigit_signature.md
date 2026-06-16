# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Multi-Digit Signature

Date: 2026-06-13

## Result

The strict one-digit carry-twist model is dead, but the full cyclic
Gross-Koblitz/Stickelberger carry signature gives a positive Jacobi-side clue.

For `N=507` and `N=12675`, lift the local order-3 product exponents by

```text
A = t * N/3
B = (h - t mod 3) * N/3
```

and compute the carry sequence

```text
floor(((p^i A mod N) + (p^i B mod N)) / N),
0 <= i < ord_N(p).
```

The p25 orders are:

```text
ord_507(p) = 78
ord_12675(p) = 780
```

The positive carry cells are exactly:

```text
(0,1), (0,2), (1,2), (2,1)
```

That is the desired valuation mask: all non-selected cells plus the selected
q-binomial anomaly `(h,t)=(2,1)`.  All selected non-anomaly cells have zero
cyclic carry signature.

## Key Values

For `N=507`:

```text
(0,1): sum 78
(0,2): sum 78
(1,2): sum 39
(2,1): sum 39
```

For `N=12675`, the same signature is repeated ten times:

```text
(0,1): sum 780
(0,2): sum 780
(1,2): sum 390
(2,1): sum 390
```

The anomaly orbit remains:

```text
138, 310, 482
```

## Interpretation

This revives the Jacobi lane in a narrow form.  The one-digit local carry was
too weak because it ignored the full `p`-orbit.  The multi-digit cyclic
signature separates the anomaly exactly at the valuation-support level.

But this is not yet a producer:

```text
valuation mask != unit phase
valuation mask != all-one finite payload
valuation mask != raw candidate vector
```

The next Jacobi probe should add a Hasse-Davenport, Gross-Koblitz unit quotient,
Greene/Barnes-delta, or equivalent phase mechanism and then emit a raw vector
for the bridge candidate harness.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate.py
```
