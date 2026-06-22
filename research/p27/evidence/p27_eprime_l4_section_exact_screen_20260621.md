# P27 E-Prime L(4O) Exact Section Screen

Date: 2026-06-21

## Claim

The next exact finite-field family after lines/two-line products is also
negative on the E-prime quotient.

On

```text
E': V^2 = U^3 + 4U
```

the probe exhaustively tested projective sections of `L(4O)`:

```text
a + bU + cU^2 + dV
```

against the descended `d3` bit on p27-signature fields.  A local exact formula
appears at q487, but it does not survive q599, q727, or q919.  Thus the d3
Kummer class is not explained by a single low-pole `L(4O)` section.

## Artifacts

Naive exact probe:

```text
research/p27/archive/gates/p27_eprime_l4_section_exact_probe.py
```

Bitset exact probe:

```text
research/p27/archive/gates/p27_eprime_l4_section_bitset_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_eprime_l4_section_exact_probe_q103_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_l4_section_exact_probe_q167_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_l4_section_exact_probe_q263_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_l4_section_bitset_probe_q487_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_l4_section_bitset_probe_q599_20260621.txt
research/p27/archive/probe_outputs/p27_eprime_l4_section_bitset_probe_q727_q919_20260621.txt
```

## Method

The bitset solver treats the constant coefficient `a` as an intersection of
shifted square/nonsquare masks.  For each chart of projective coefficient
space:

```text
d=1      : a,b,c free
d=0,c=1  : a,b free
d=c=0,b=1: a free
constant
```

it tests whether there exists an `a` such that every evaluated row has the
target squareclass, up to global polarity.

This gives an exact screen for a single section in the basis:

```text
1, U, U^2, V
```

It is not a random coefficient fit.

## Results

Small p27-signature fields q103, q167, and q263 are degenerate for this test:

```text
q103: no descended E' rows
q167: only 4 d3 rows after E', all one-sided
q263: 10 d3 and 10 d4 rows after E', both one-sided
```

q487 has a local artifact:

```text
q487 d3 rows after E' = 28, plus/minus = 16/12
q487 exact L(4O) sections = 33
examples are in the d=0,c=1 chart, i.e. quadratic polynomials in U
```

The artifact does not survive later p27-signature fields:

```text
q599 d3 rows after E' = 56, plus/minus = 18/38
q599 exact L(4O) sections = 0

q727 d3 rows after E' = 40, plus/minus = 24/16
q727 exact L(4O) sections = 0

q919 d3 rows after E' = 66, plus/minus = 30/36
q919 exact L(4O) sections = 0
```

For d4, these fields were one-sided after conditioning on d3, so they are not
used as a d4 falsifier here:

```text
q487 d4 rows = 16, one-sided
q599 d4 rows = 18, one-sided
q727 d4 rows = 24, one-sided
q919 d4 rows = 30, one-sided
```

## Interpretation

Positive:

```text
The exact L(4O) solver is fast enough for useful p27-signature guard fields.
It catches and demotes local artifacts such as q487.
The screen directly targets the E' quotient where d3 descends.
```

Negative:

```text
No single L(4O) section explains d3 across q599/q727/q919.
The local q487 quadratic-U fits are interpolation artifacts.
The first irreducible-conic-sized source family on E' is killed.
```

This narrows the E-prime route again.  A sqrt-beating structure now needs:

```text
1. normalization / branch-divisor extraction of the staged d3 curve J, or
2. a higher-degree but named Kummer/theta class on E', or
3. a recurrence relating d4 to d3 after d3's actual class is known.
```

## Continue / Kill

```text
continue = offline normalization/genus of J = Iclean + <reverse_z>
continue = exact divisor/Kummer-class extraction beyond L(4O)
continue = d4 comparison only after d3 class is named

kill = single L(4O) section as d3 source on E'
kill = q487 exact quadratic-U fits as promotion evidence
kill = another random low-pole fit without an extracted divisor class
```

```text
p27_eprime_l4_section_exact_screen_rows=1/1
```
