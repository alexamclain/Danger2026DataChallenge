# P27 Reverse Source Quotient Screen

Date: 2026-06-21

## Claim

The reverse-doubling d3/source bit descends cleanly to the residual elliptic
quotient `E: W^2 = X^3-X`, but it is not an exact low-degree line character on
that quotient.

This is a useful narrowing:

```text
positive = d3 bit is quotient-level, not full compactD-fiber data
negative = no cheap degree-1 line character/source on E
next = identify the actual non-line divisor/theta/Kummer class, or show it is generic
```

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_reverse_source_quotient_probe.py \
  --target 5000 \
  --max-draws 1000000 \
  --small-primes 607 \
  --p27-line-bound 2 \
  | tee research/p27/archive/probe_outputs/p27_reverse_source_quotient_probe_20260621.txt
```

The probe groups every label-2 compactD candidate by residual elliptic point
`(X,W)` and checks whether the next x-square / reverse-source bit is constant
on the four oriented candidates in that fiber.

It then tests:

```text
p27: small integer line characters a + bX + cW, |a|,|b|,|c| <= 2
q=607: every projective line character a + bX + cW over GF(607)
```

The finite-field line screen is a falsifier for a cheap quotient character, not
a broad search for arbitrary rational functions.

## P27 Descent Result

The bit descends perfectly on the sampled p27 quotient fibers:

```text
quotient_E_points = 5000
oriented_candidates = 20000
orbit_size_4 = 5000
quotient_rows = 5000
d3_plus_E_points = 2466
d3_minus_E_points = 2534
d3_not_descended_to_E = 0
```

Interpretation:

```text
The d3/reverse-source bit is invariant across the two T signs and the two
oriented label-2 candidates above the same residual E point.
```

This strengthens the quotient route: the next bit is not hidden in the full
compactD fiber.  It is a quadratic/source character on the residual elliptic
quotient, or on a small cover of it.

## Line Character Screen

The p27 small-coefficient sanity screen is flat:

```text
small_coeff_lines_tested = 124
exact_lines = 0
best_good = 2564/5000 = 0.512800000
best_line = 1 - X
```

The q=607 exhaustive projective line screen also finds no exact line:

```text
quotient_E_points = 128
d3_plus_E_points = 64
d3_minus_E_points = 64
projective_lines_tested = 369057
exact_lines = 0
best_good = 91/128 = 0.710937500
best_line = 6 + 178*X + W
```

The q=607 best line is not promotion evidence by itself; with only 128 quotient
rows, a high in-field score can be accidental.  The decisive part is the
absence of any exact projective line over `GF(607)`.  A global degree-1 line
character with good reduction at `607` would have appeared in that exhaustive
screen.

## Interpretation

Positive:

```text
The source bit descends to E, so an expert/Magma ask can work on the residual
elliptic quotient instead of the full compactD/order-4 fiber.
```

Negative:

```text
The descended bit is not a visible degree-1 line character on E.
The p27 small-coefficient lines are effectively flat.
Reverse doubling still does not give a cheap sampler or sqrt-beating recurrence.
```

## Concrete Next Tests

1. Divisor/theta/Kummer identification:

```text
Find the divisor class on E whose quadratic character is the descended d3 bit,
or prove that the associated double cover is generic for this purpose.
```

2. Source-cover genus/quotient:

```text
Build the E-level double cover represented by this descended bit and compute
genus, components, and maps.  A low-genus or isogenous cover could become a
direct source; a generic higher-genus cover kills this route as a moonshot.
```

3. Recurrence:

```text
Repeat the quotient grouping after d3 passes and ask whether d4 is governed by
the same E-level character after a named transformation.  A recurring character
would be the first real sqrt-beating shape; a fresh unrelated half-cover keeps
the route constant-factor only.
```

Status: first recurrence screen completed.  d4 also descends to `E`, but no
p27 degree-1 line character or non-degenerate small-field simple-transform
recurrence was found; see
[P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md).

## Continue / Kill

```text
continue = E-level divisor/theta/Kummer identification for the descended d3 bit
continue = Magma/Sage genus and quotient analysis of the E-level source cover
continue = recurrence test: does d4 reuse the same quotient character after a map?

kill = degree-1 line character source on E
kill = treating reverse doubling alone as a GPU sampler
kill = searching compactD-fiber branch/T choices for this bit
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_reverse_source_quotient_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_reverse_source_quotient_probe_20260621.txt`
- Follow-up: [P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md)
- Related: [P27 Reverse-Doubling Source Screen](p27_reverse_doubling_source_screen_20260621.md)
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)

```text
p27_reverse_source_quotient_screen_rows=1/1
```
