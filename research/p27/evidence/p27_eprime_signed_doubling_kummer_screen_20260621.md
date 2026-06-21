# P27 E-Prime Signed-Doubling Kummer Screen

Date: 2026-06-21

## Claim

The `d3` and `d4` quotient bits descend one step farther than the 2-isogenous
elliptic quotient `E'`.

On

```text
E': V^2 = U^3 + 4U
```

both bits are constant on signed `[2]` projection classes in every tested
non-degenerate guard field.  Equivalently, they descend to the Kummer-line
coordinate

```text
K = x([2](U,V)) = (U^2 - 4)^2 / (4*U*(U^2 + 4)).
```

This is the first positive quotient reduction after the plain `E'` screens:
the active source question is now on a line, not on the full elliptic quotient.

The first sourceable subcase is negative: neither `d3` nor `d4` is a quadratic
character of a degree-1 or degree-2 polynomial in `K` over
`q=1471,1607,1847`.  So the Kummer-line descent does not yet give a rational
source.  The next concrete sqrt-beating test is degree `3/4` on the K-line:
an exact cubic or quartic would give an elliptic source candidate.

## Probes

Group-projection probe:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_group_projection_probe.py \
  --small-primes 1471,1607,1847,1951,1999,2039,2063,2087,2111,2143,2207,2239 \
  --max-modulus 512 \
  --multipliers 2,4,8,16 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_eprime_group_projection_probe_20260621.txt
```

Kummer-line probe:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_double_kummer_line_probe.py \
  --small-primes 1471,1607,1847 \
  --max-degree 2 \
  --top 8 \
  | tee research/p27/archive/probe_outputs/p27_eprime_double_kummer_line_probe_20260621.txt
```

## Group Projection Result

Stable exact structure:

```text
signed [2] projection is exact for d3 in all 12 tested fields
signed [2] projection is exact for d4 in all 12 tested fields with d4 rows
```

Examples:

```text
q=1471 d3: signed mul=2, 50 non-singleton classes, mixed=0
q=1471 d4: signed mul=2, 28 non-singleton classes, mixed=0

q=1607 d3: signed mul=2, 49 non-singleton classes, mixed=0
q=1607 d4: signed mul=2, 28 non-singleton classes, mixed=0

q=1847 d3: signed mul=2, 63 non-singleton classes, mixed=0
q=1847 d4: signed mul=2, 45 non-singleton classes, mixed=0
```

Unstable extra structure:

```text
signed [4], [8], and [16] are exact in some fields but not others
some d4 exact projections occur only when d4 is constant in that small field
```

Interpretation:

```text
promote = signed [2] / Kummer-line descent
do not promote = stronger fixed [4]/[8]/[16] quotient as a stable theorem
```

## Kummer-Line Result

The Kummer descent has no mixed classes in the three main guard fields:

```text
q=1471 d3: E' rows 100 -> K rows 50, plus/minus = 28/22
q=1471 d4: E' rows 56  -> K rows 28, plus/minus = 14/14

q=1607 d3: E' rows 98  -> K rows 49, plus/minus = 28/21
q=1607 d4: E' rows 56  -> K rows 28, plus/minus = 19/9

q=1847 d3: E' rows 126 -> K rows 63, plus/minus = 45/18
q=1847 d4: E' rows 90  -> K rows 45, plus/minus = 19/26
```

Exact degree screens:

```text
q=1471: d3 degree1 exact=0, degree2 exact=0
q=1471: d4 degree1 exact=0, degree2 exact=0

q=1607: d3 degree1 exact=0, degree2 exact=0
q=1607: d4 degree1 exact=0, degree2 exact=0

q=1847: d3 degree1 exact=0, degree2 exact=0
q=1847: d4 degree1 exact=0, degree2 exact=0
```

Best near misses:

```text
q=1471 d3 degree2 best = 43/50
q=1471 d4 degree2 best = 27/28

q=1607 d3 degree2 best = 42/49
q=1607 d4 degree2 best = 27/28

q=1847 d3 degree2 best = 50/63
q=1847 d4 degree2 best = 39/45
```

The q1471/q1607 d4 `27/28` scores are not promotion evidence.  They are not
exact, and the named polynomials differ between fields.

## Interpretation

Positive:

```text
d3 and d4 descend from E' to the signed-doubling Kummer line.
The next function-field extraction target is one-variable: K=x([2]P).
This is a genuine simplification of the cover-class problem.
```

Negative:

```text
No degree-1 or degree-2 K-polynomial character gives d3 or d4.
No rational source follows from the Kummer-line descent alone.
No GPU sampler follows yet: signed [2] is a structural quotient, not a
measured source-space shrink.
```

## Next Test

Run an exact degree `3/4` Kummer-line extraction:

```text
Find f3(K), f4(K) with deg(f) in {3,4} such that
  chi(f3(K)) = d3
  chi(f4(K)) = d4 after d3
on q=1471,1607,1847.
```

Promotion bar:

```text
An exact cubic or quartic surviving at least q=1471 and q=1607.
```

Why this matters:

```text
z^2 = cubic(K) or quartic(K) is genus 1, so an exact result would give an
elliptic source candidate for the next all-plus gate.
```

Kill condition:

```text
No exact low-degree K-polynomial through degree 4 on non-degenerate guard
fields, or exact formulas that do not persist across fields.
```

If degree `3/4` is negative, move to divisor/Kummer class extraction on the
K-line or a Magma/Sage model of the associated higher-genus double cover.

## Continue / Kill

```text
continue = exact degree 3/4 K-polynomial screen on K=x([2]P)
continue = Magma/Sage divisor-class extraction on the Kummer line
continue = compare f3 and f4 as K-line branch divisors if exact formulas appear

kill = plain E' line/two-line/low-pole scans as the front-door route
kill = degree <=2 K-polynomial/rational source
kill = stronger [4]/[8]/[16] signed projection unless it survives as a named
       K-line formula across guard fields
kill = GPU sampler from signed [2] alone
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_eprime_group_projection_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_eprime_group_projection_probe_20260621.txt`
- Gate: `research/p27/archive/gates/p27_eprime_double_kummer_line_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_eprime_double_kummer_line_probe_20260621.txt`

```text
p27_eprime_signed_doubling_kummer_screen_rows=1/1
```
