# P27 K-Line Fit Significance

Date: 2026-06-22

## Claim

K-line exact polynomial fits must be judged against family size.  The q863
exact cubics from the replay probe are expected interpolation, while an exact
d3 cubic or quartic in the promotion fields would be meaningful.

Random-sign model:

```text
expected exact fits ~= 2 * family_size / 2^rows
```

The factor `2` allows global polarity.  This is only a calibration, but it is
decisive enough to separate local interpolation from a real source candidate.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_fit_significance_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_kline_fit_significance_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_kline_fit_significance_probe.py \
  --small-primes 607,863,991,1471,1607,1847 \
  | tee research/p27/archive/probe_outputs/p27_kline_fit_significance_probe_20260622.txt
```

## Calibration Results

For `d3` monic cubics:

```text
q607:  rows=32, expected_exact=0.104
q863:  rows=24, expected_exact=76.62
q991:  rows=36, expected_exact=0.0283
q1471: rows=50, expected_exact=5.65e-6
q1607: rows=49, expected_exact=1.47e-5
q1847: rows=63, expected_exact=1.37e-9
```

This explains the replay pattern:

```text
q607 observed exact cubics = 0
q863 observed exact cubics = 58
q991 observed exact cubics = 0
```

q863 is not a paradox and not a source.  It is the expected behavior when the
candidate family is large and the row count is only `24`.

For `d3` monic quartics:

```text
q607:  expected_exact=63.2
q863:  expected_exact=66123
q991:  expected_exact=28.1
q1471: expected_exact=0.00832
q1607: expected_exact=0.0237
q1847: expected_exact=2.52e-6
```

So quartic fits in tiny fields are also not meaningful.  A quartic that
survives `q1471`, `q1607`, and especially `q1847` would be meaningful.

For `d4`, most small K-row sets are too small:

```text
q1471 d4 rows=28, monic cubic expected_exact=23.7
q1607 d4 rows=28, monic cubic expected_exact=30.9
q1847 d4 rows=45, monic cubic expected_exact=3.58e-4
```

This explains why q1471/q1607 d4 cubic fits are local artifacts unless they
also survive q1847 or a named d3 branch class.

## Decision Rules

Promote:

```text
d3 exact cubic/quartic in q1471/q1607/q1847
d4 exact relation only after d3 branch class is named, or if it survives q1847
branch-cover/genus extraction that gives genus <= 1 or a sourceable quotient
```

Demote:

```text
q863 exact cubics
q607/q863/q991 quartic fits
q1471/q1607 d4 cubics without q1847 or a named d3 class
near-miss best scores such as 31/32 or 34/36
```

Promotion-field result:
[P27 K-Line q1471 Cubic Promotion Screen](p27_kline_q1471_cubic_promotion_screen_20260622.md)
now applies this rule to the first promotion field.  It finds no exact `d3`
monic cubic over q1471.  Thus the cubic K-polynomial source shape is killed;
the remaining low-genus K-line possibility is quartic or a non-polynomial
branch class recovered by normalization.

## Interpretation

Positive:

```text
The promotion fields are now justified quantitatively.
An exact d3 low-degree K-line formula in q1471/q1607/q1847 would be highly
non-random and worth immediate CAS/expert attention.
```

Negative:

```text
Small-field low-degree fits are not enough for a source claim.
The K-line route still needs branch-cover/genus extraction, not more broad
coefficient scans.
```

## Continue / Kill

```text
continue = Magma/Sage branch-cover normalization over P1_K/P1_Sroot
continue = exact d3 low-degree tests only in promotion fields or with a named class
continue = use expected_exact calibration in future finite-field screens

kill = local q863 cubic formulas
kill = d4 low-row local fits as recurrence evidence
kill = production GPU work from any finite-field fit without promotion-field stability
```

```text
p27_kline_fit_significance_rows=1/1
```
