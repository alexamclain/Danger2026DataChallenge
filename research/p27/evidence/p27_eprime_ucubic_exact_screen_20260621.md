# P27 E-Prime U-Cubic Exact Screen

Date: 2026-06-21

## Claim

The rational U-line cubic family on the E-prime quotient is also not the
p27 d3 source law.

On

```text
E': V^2 = U^3 + 4U
```

the probe exhaustively tested projective U-polynomials:

```text
a + bU + cU^2 + dU^3.
```

This is the next Kummer-line family after the killed `L(4O)` single-section
screen.  It catches several local exact artifacts, but they do not survive
larger p27-signature guard fields.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_eprime_ucubic_exact_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_eprime_ucubic_exact_probe_q487_q599_q727_q919_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_ucubic_exact_probe_q967_q1063_20260621.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_ucubic_exact_probe.py \
  --small-primes 487,599,727,919 \
  --min-rows 12 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_eprime_ucubic_exact_probe_q487_q599_q727_q919_20260621.txt
```

Follow-up:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_ucubic_exact_probe.py \
  --small-primes 967,1063 \
  --min-rows 12 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_eprime_ucubic_exact_probe_q967_q1063_20260621.txt
```

## Method

The solver uses the same shifted-squareclass bitset method as the `L(4O)`
screen.  It tests projective coefficient charts:

```text
d=1
d=0,c=1
d=c=0,b=1
constant
```

and treats the constant coefficient `a` as an intersection of allowed masks.
The result is exact over each finite field, not random scoring.

## Results

Local artifacts:

```text
q487 d3 rows after E' = 28, plus/minus = 16/12
q487 exact U-cubics = 13,745

q599 d3 rows after E' = 56, plus/minus = 18/38
q599 exact U-cubics = 1
  example: 431 + 583U + 83U^2 + U^3, polarity -1

q727 d3 rows after E' = 40, plus/minus = 24/16
q727 exact U-cubics = 745
```

Decisive non-survival:

```text
q919 d3 rows after E' = 66, plus/minus = 30/36
q919 exact U-cubics = 0

q967 d3 rows after E' = 68, plus/minus = 16/52
q967 exact U-cubics = 0

q1063 d3 rows after E' = 70, plus/minus = 32/38
q1063 exact U-cubics = 0
```

For d4, these fields are still one-sided after conditioning on d3, so this is
not a d4 falsifier.

## Interpretation

Positive:

```text
The exact U-cubic solver is fast on useful p27-signature fields.
It explains why small fields can look promising: local cubic interpolation is common.
```

Negative:

```text
The U-cubic family does not survive q919/q967/q1063.
The q599 single exact cubic and q727/q487 families are local artifacts.
The d3 source is not a rational U-line cubic character on E'.
```

This closes the nearest "maybe q487 just wanted one more U degree" loophole.
The E-prime route now points back to the actual staged curve:

```text
J = Iclean + <reverse_z>
```

and its normalized branch/Kummer class.

## Continue / Kill

```text
continue = offline normalization/genus of J
continue = exact divisor/Kummer-class extraction from the normalized d3 cover
continue = d4 comparison only after d3 class is named

kill = U-line cubic source on E'
kill = q487/q599/q727 exact U-polynomials as promotion evidence
kill = widening univariate U coefficient searches without a divisor-class reason
```

```text
p27_eprime_ucubic_exact_screen_rows=1/1
```
