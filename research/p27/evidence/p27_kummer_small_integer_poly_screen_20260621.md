# P27 Kummer Small-Integer Polynomial Screen

Date: 2026-06-21

## Claim

The signed-doubling Kummer-line reduction is real, but it does not appear to be
explained by a compact small-integer cubic or quartic in `K`.

The screen tested one shared integer polynomial shape across the guard fields

```text
q = 1471, 1607, 1847
```

for both `d3` and `d4`, allowing an overall field-dependent polarity.  No
degree `3` or `4` polynomial with primitive coefficients in `[-8,8]` was exact
in all three fields.

This kills the most optimistic "small visible K-polynomial" version of the
Kummer-line lead.  It does not kill the K-line route; it says the next test
should be divisor/Kummer-class extraction or a more powerful exact finite-field
solver, not wider blind coefficient fitting.

## Probe

Gate:

```text
research/p27/archive/gates/p27_kummer_small_integer_poly_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kummer_small_integer_poly_probe_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kummer_small_integer_poly_probe.py \
  --small-primes 1471,1607,1847 \
  --degrees 3,4 \
  --bound 8 \
  --targets d3,d4 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_kummer_small_integer_poly_probe_20260621.txt
```

The tested formula shape is:

```text
chi(f(K)) = target
K = x([2]P) on E': V^2 = U^3 + 4U
f(K) = c0 + c1*K + ... + cd*K^d
primitive integer coefficients ci in [-8,8]
```

The same integer coefficients must work in all guard fields.  The screen
allows polarity to vary by field, since a rational scalar normalization may
have different squareclass in different finite fields.

## Results

Row counts:

```text
q=1471: d3 K rows = 50, d4 K rows = 28
q=1607: d3 K rows = 49, d4 K rows = 28
q=1847: d3 K rows = 63, d4 K rows = 45
```

Search size:

```text
degree 3 primitive coefficient tuples tested = 36,111
degree 4 primitive coefficient tuples tested = 640,593
```

Exact results:

```text
d3 degree 3 exact_all_fields = 0
d3 degree 4 exact_all_fields = 0
d4 degree 3 exact_all_fields = 0
d4 degree 4 exact_all_fields = 0
```

Best cross-field minimum rates:

```text
d3 degree 3 best min rate = 0.650793651
d3 degree 4 best min rate = 0.666666667
d4 degree 3 best min rate = 0.711111111
d4 degree 4 best min rate = 0.714285714
```

Representative best candidates:

```text
d3 degree 4:
  f = 5 + 7*K - 8*K^2 + 6*K^3 + 7*K^4
  q1471 34/50, q1607 33/49, q1847 42/63

d4 degree 4:
  f = 6 - 7*K - 4*K^2 + 7*K^3 + 4*K^4
  q1471 20/28, q1607 20/28, q1847 33/45
```

These are not promotion evidence: they are far from exact and no named
polynomial persists with theorem-level behavior.

## Interpretation

Positive:

```text
The K-line target is now screened for the first compact integer cubic/quartic
formulas that would have implied an elliptic source.
```

Negative:

```text
No small-integer degree 3/4 K-polynomial explains d3 or d4 across guard fields.
Increasing coefficient bounds blindly is unlikely to be the right next move.
No GPU sampler follows from this screen.
```

## Next Test

The next K-line test should be structural rather than another broad
small-coefficient sweep:

```text
1. Use Magma/Sage to extract the actual branch divisor/class on the K-line for d3.
2. Determine the minimal degree of a representative f3(K).
3. Repeat after d3 for d4 and compare f4(K) to f3(K) by a named K-line map.
```

Concrete expert/Magma ask:

```text
Given the finite set of K-line labels produced by the compactD source, recover
the double-cover branch divisor for d3 on P^1_K.  If the divisor has degree
3 or 4, produce the polynomial up to square and scalar; if it has higher
degree, compute the genus and look for a low-degree quotient or recurrence.
```

Promotion bar:

```text
An exact branch polynomial/class on q=1471 and q=1607 that either has degree
3/4 or gives a named recurrence/source relation for d4.
```

Kill condition:

```text
The K-line branch divisor is high degree/generic and f4 is an unrelated fresh
half-cover.
```

## Continue / Kill

```text
continue = Magma/Sage branch-divisor extraction on P^1_K
continue = exact finite-field solver for unrestricted degree 3/4 coefficients
           if it is framed as branch-divisor recovery, not random fitting
continue = compare d3/d4 branch divisors for recurrence

kill = small integer coefficient K-polynomials with degree <= 4 and bound <= 8
kill = GPU sampler from small K-polynomial screens
kill = widening coefficient bounds without a divisor/class reason
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_kummer_small_integer_poly_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_kummer_small_integer_poly_probe_20260621.txt`
- Parent: [P27 E-Prime Signed-Doubling Kummer Screen](p27_eprime_signed_doubling_kummer_screen_20260621.md)

```text
p27_kummer_small_integer_poly_screen_rows=1/1
```
