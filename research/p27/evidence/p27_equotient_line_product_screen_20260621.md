# P27 E-Quotient Line-Product Screen

Date: 2026-06-21

## Claim

The descended `d3` and `d4` characters are not explained by a product of two
projective-line characters on the residual elliptic quotient
`E: W^2 = X^3-X`.

```text
tested = exhaustive two-line products over small fields
result = q=1471 kills both d3 and d4 two-line products
next = irreducible conic / function-field extraction, not reducible conic
```

This sharpens the low-pole negative.  The previous random screen sampled
small sections of `L(nO)`; this screen exactly exhausts one especially natural
subclass: reducible conics, i.e. products of two projective lines
`a + bX + cW`.

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_line_product_probe.py \
  --small-primes 607,1087,1471 \
  --families d3,d4 \
  --pair-limit 4 \
  | tee research/p27/archive/probe_outputs/p27_equotient_line_product_probe_20260621.txt
```

For each finite field the probe:

```text
1. enumerates compactD=-1 label-2 candidates,
2. groups them by residual E point (X,W),
3. records the descended d3 and d4 characters,
4. computes the zero-free signature of every projective line,
5. asks whether target = line_1 * line_2, allowing both polarities.
```

In bit language, the two-line test is exact:

```text
signature(line_1) XOR signature(line_2) = target
```

or the same equation with the full-mask polarity flip.

## Results

`q=607` is useful for `d3` but has the known `d4` constant degeneracy:

```text
q607 d3 rows = 128, plus/minus = 64/64
q607 d3 projective lines tested = 369057
q607 d3 exact two-line pairs = 0

q607 d4 rows = 64, plus/minus = 0/64
q607 d4 exact pairs are constant-square degeneracies
```

`q=1087` is non-degenerate but the `d4` row count is only `40`:

```text
q1087 d3 rows = 72, plus/minus = 40/32
q1087 d3 projective lines tested = 1182657
q1087 d3 exact two-line pairs = 0

q1087 d4 rows = 40, plus/minus = 20/20
q1087 d4 exact two-line pairs = 9
```

The `q=1087` d4 hits are not promotion evidence.  With only `40` rows and
about `1.14M` zero-free line signatures, accidental XOR hits are plausible and
must be checked in a larger non-degenerate field.

`q=1471` is the decisive small-field check here:

```text
q1471 d3 rows = 200, plus/minus = 112/88
q1471 d3 projective lines tested = 2165313
q1471 d3 zero-free lines = 1889913
q1471 d3 exact two-line pairs = 0

q1471 d4 rows = 112, plus/minus = 56/56
q1471 d4 projective lines tested = 2165313
q1471 d4 zero-free lines = 2006509
q1471 d4 exact two-line pairs = 0
```

The q=1471 result kills the reducible-conic/two-line explanation for both
`d3` and `d4` in the current quotient model.

## Interpretation

Positive:

```text
The screen is exact on its finite fields, not random.
It gives a crisp falsifier for one low-degree divisor class.
It also explains the q1087 d4 hits as a small-row coincidence, not a source.
```

Negative:

```text
No product of two projective lines explains d3 in q607, q1087, or q1471.
No product of two projective lines explains d4 in the decisive q1471 field.
Best one-line scores remain high in small fields but not exact.
```

This means a sqrt-beating source is unlikely to be a visible reducible conic
on `E`.  The next structure test should move to either:

```text
1. irreducible conics / low-degree plane sections with exact small-field
   linear algebra, or
2. symbolic function-field extraction of the actual E-level double covers.
```

The online Magma calculator is suitable for small-field validation of any
candidate formula emitted by those next tests.

## Continue / Kill

```text
continue = exact irreducible-conic screen over q=1471 if cheap enough
continue = Magma/Sage extraction of E-level f3/f4 covers and divisor classes
continue = online Magma validation for named small-field formulas

kill = reducible conic / product of two projective lines as the source
kill = treating q1087 d4 exact pairs as evidence
kill = GPU sampler from two-line signatures
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_equotient_line_product_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_equotient_line_product_probe_20260621.txt`
- Related: [P27 E-Quotient Low-Pole Random Screen](p27_equotient_lowpole_random_screen_20260621.md)
- Related: [P27 E-Quotient Kummer Basis Screen](p27_equotient_kummer_basis_screen_20260621.md)
- Related: [P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md)

```text
p27_equotient_line_product_screen_rows=1/1
```
