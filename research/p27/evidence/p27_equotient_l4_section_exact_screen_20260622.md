# P27 E-Quotient L(4O) Exact Section Screen

Date: 2026-06-22

## Claim

The nearest exact single-section family on the residual elliptic quotient is
negative.

On

```text
E: W^2 = X^3 - X
```

the probe exhaustively tested projective sections of `L(4O)`:

```text
a + bX + cX^2 + dW
```

against the descended `d3` bit, and against `d4` after conditioning on `d3`.
The p27-signature guard field `q1607` kills both non-degenerate families with
zero exact sections.

## Probe

Gate:

```text
research/p27/archive/gates/p27_equotient_l4_section_bitset_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_equotient_l4_section_bitset_probe_q487_q599_q727_q919_20260622.txt
research/p27/archive/probe_outputs/p27_equotient_l4_section_bitset_probe_q1607_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_l4_section_bitset_probe.py \
  --small-primes 487,599,727,919 \
  --families d3,d4 \
  --min-rows 12 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_equotient_l4_section_bitset_probe_q487_q599_q727_q919_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_l4_section_bitset_probe.py \
  --small-primes 1607 \
  --families d3,d4 \
  --min-rows 12 \
  --sample-limit 8 \
  | tee research/p27/archive/probe_outputs/p27_equotient_l4_section_bitset_probe_q1607_20260622.txt
```

The bitset solver treats the constant coefficient `a` as an intersection of
shifted square/nonsquare masks.  It tests these projective charts exactly:

```text
d=1       : a,b,c free
d=0,c=1   : a,b free
d=c=0,b=1 : a free
constant
```

## Results

For `d3`, all tested p27-compatible `q = 7 mod 16` fields are negative:

```text
q487  d3 rows = 56,  plus/minus = 32/24,   exact L(4O) sections = 0
q599  d3 rows = 112, plus/minus = 36/76,   exact L(4O) sections = 0
q727  d3 rows = 80,  plus/minus = 48/32,   exact L(4O) sections = 0
q919  d3 rows = 132, plus/minus = 60/72,   exact L(4O) sections = 0
q1607 d3 rows = 196, plus/minus = 112/84,  exact L(4O) sections = 0
```

For `d4`, the smaller fields are one-sided after conditioning on `d3`, but
`q1607` is non-degenerate and also negative:

```text
q487  d4 rows = 32,  one-sided
q599  d4 rows = 36,  one-sided
q727  d4 rows = 48,  one-sided
q919  d4 rows = 60,  one-sided
q1607 d4 rows = 112, plus/minus = 76/36, exact L(4O) sections = 0
```

## Interpretation

Positive:

```text
The residual E quotient remains the correct descent surface for d3/d4.
The exact bitset method is fast enough for q1607-scale p27-signature checks.
The original E quotient has no q487 local artifact, unlike the E' L(4O) test.
```

Negative:

```text
No single section a+bX+cX^2+dW explains d3 on q487/q599/q727/q919/q1607.
No single section a+bX+cX^2+dW explains non-degenerate d4 on q1607.
The cheap irreducible-conic-sized E source is killed.
```

This closes the specific gap left after the E line/two-line screen.  The live
E route is no longer "try the next obvious low-pole family"; it is extraction
of the actual double-cover/Kummer class, a higher named divisor class, or a
recurrence/source arising from the normalized cover.

## Continue / Kill

```text
continue = function-field extraction of the E-level d3/d4 double covers
continue = branch divisor / Kummer class computation on the normalized cover
continue = exact tests only when a named divisor class or recurrence is proposed

kill = single L(4O) section on E as d3 source
kill = single L(4O) section on E as d4 source in q1607
kill = more random low-pole fitting without a named extracted class
```

```text
p27_equotient_l4_section_exact_screen_rows=1/1
```
