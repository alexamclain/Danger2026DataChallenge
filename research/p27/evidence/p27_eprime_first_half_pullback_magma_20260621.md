# P27 E-Prime First-Half Pullback Magma Smoke

Date: 2026-06-21

## Claim

Rewriting the K/S first-half layer in the 2-isogenous quotient coordinates
confirms that `E'` is the right extraction surface, but it does not by itself
lower the staged cover.

After eliminating `W` using

```text
E': V^2 = U^3 + 4U
U = X - 1/X
W = V*X^2/(X^2+1),
```

and saturating the known denominator divisors, the eta=`+1` first-half
pullback over q7 is still:

```text
dimension = 1
genus = 37
```

This matches the earlier raw K/S first-half genus.  The E-prime descent is
therefore a coordinate and quotient simplification, not a low-genus source by
itself.

## Artifacts

Magma fixture:

```text
research/p27/archive/fixtures/p27_eprime_first_half_pullback_saturated_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_eprime_first_half_pullback_saturated_q7_magma_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_first_half_pullback_saturated_q7_magma_20260621.html
```

Command:

```bash
curl -L -sS -A 'Mozilla/5.0' \
  --data-urlencode input@research/p27/archive/fixtures/p27_eprime_first_half_pullback_saturated_q7_magma.m \
  https://magma.maths.usyd.edu.au/calc/ \
  > research/p27/archive/probe_outputs/p27_eprime_first_half_pullback_saturated_q7_magma_20260621.html
```

## Method

The fixture works in variables:

```text
U, V, X, T, R, B
```

with equations:

```text
E'       : V^2 = U^3 + 4U
X lift   : X^2 - U*X - 1 = 0
T cover  : T^2 = X(X^2+1)(X^2+2X-1)
compactD : cleared version of X*R^2 = W(X^2+1)(m0+mt*T)
B cover  : cleared eta=+1 first-half equation
```

The substitution

```text
W = V*X^2/(X^2+1)
```

removes the residual `W` variable and makes the E-prime quotient explicit.
The fixture saturates by:

```text
bad = X*(X-1)*(X+1)*(X^2+1)*(T-2X^2)
```

These are the same denominator/projection divisors seen in the earlier K/S
first-half smoke, plus the `X^2+1` denominator introduced by the E-prime
coordinate.

## Result

Online Magma q7 output:

```text
EPRIME_PULLBACK_SAT_SCHEME 1 61 0
EPRIME_PULLBACK_SAT_CURVE 37 0
RESULT p27_eprime_first_half_pullback_saturated_q7 done
```

Interpretation:

```text
dimension = 1
saturated ideal basis size = 61
affine q7 points = 0
genus = 37
```

## Interpretation

Positive:

```text
The E-prime coordinate rewrite is executable as a compact Magma fixture.
The denominator saturation is explicit.
The result agrees with the earlier genus-37 first-half warning.
```

Negative:

```text
The E' quotient does not reveal a direct low-genus first-half source.
The genus-37 obstruction persists before adjoining the final reverse-source
variables z,Y.
```

This sharpens the next sqrt-beating test.  Do not ask merely whether the
first-half cover descends to `E'`; it does.  Ask for the actual `d3/d4`
double-cover branch/Kummer classes on `E'` and whether they share a low-genus
factor or recurrence.

## Continue / Kill

```text
continue = exact d3/d4 branch-divisor extraction on E'
continue = compare d3 and d4 Kummer classes after normalization
continue = seek a low-genus factor below the genus-37 staged cover

kill = E' first-half pullback as a direct low-genus source
kill = GPU sampler based only on the E' descent without a lower-genus factor
kill = broad visible branch-product scans already covered by prior screens
```

```text
p27_eprime_first_half_pullback_magma_rows=1/1
```
