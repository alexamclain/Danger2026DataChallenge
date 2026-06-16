# Subsqrt Moonshot Lane B Square-Axis Gross-Koblitz Half-Orbit Projector

Date: 2026-06-13

## Result

The Frobenius projector has an arithmetic-facing half-orbit form.

For the cyclic Gross-Koblitz carry signature `c_i`, split the `p`-orbit into
even and odd powers:

```text
even_avg = sum_j c_{2j}   / (ord_N(p)/2)
odd_avg  = sum_j c_{2j+1} / (ord_N(p)/2)
```

For `N=507`:

```text
p mod N = 218
ord_N(p) = 78
ord_N(p^2) = 39
p^39 = -1 mod 507
```

For raw `N=12675`:

```text
p mod N = 5288
ord_N(p) = 780
ord_N(p^2) = 390
p^390 = 7099 mod 12675
```

Even though the raw half-power is not `-1`, the raw and quotient half-orbit
averages agree on the seed cells.

## Projector Law

The odd half-orbit average has support:

```text
(0,1), (0,2), (2,1)
```

The even half-orbit average has support:

```text
(0,1), (0,2), (1,2)
```

Multiplying the odd average by the Lucas/no-borrow selected support leaves
exactly:

```text
(2,1)
```

and after the outer `S` layer:

```text
138, 310, 482
```

## Consequence

This is the cleanest finite target so far for a Jacobi/GK arithmetic producer:

```text
projector = selected * odd Frobenius p^2-suborbit average
```

The caveat is important.  The odd half-orbit average alone leaks onto the two
non-selected top-row cells `(0,1)` and `(0,2)`.  A real HD/GK/Barnes unit phase
must couple the odd half-orbit with the Lucas/no-borrow selector, not merely
produce an odd-half-orbit valuation.

## Command

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_gate.py
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_gate.py
```
