# P27 E-Prime Low-Pole Random Screen

Date: 2026-06-21

## Claim

Moving from the residual elliptic curve

```text
E: W^2 = X^3 - X
```

to the 2-isogenous quotient

```text
E': V^2 = U^3 + 4U
```

is a real structural simplification, but a bounded random low-pole search on
`E'` did not reveal a source law for the descended `d3` or `d4` bits.

```text
positive = d3/d4 are now tested on the sharper E' quotient coordinates
negative = no exact low-pole section/product candidate on p27 or guard fields
next = exact function-field / divisor-class extraction, with Magma validation
```

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_eprime_lowpole_random_probe.py \
  --target 2000 \
  --heldout-target 2000 \
  --max-draws 500000 \
  --pole-bounds 5,7,9 \
  --trials 500 \
  --coeff-bound 3 \
  --small-primes 1471,1607 \
  | tee research/p27/archive/probe_outputs/p27_eprime_lowpole_random_probe_20260621.txt
```

The probe uses the Riemann-Roch basis on `E'`:

```text
L(nO): 1, U, U^2, ..., V, UV, ...
```

and tests small-integer section characters `chi(s)` plus product characters
`chi(s1*s2)`, which model rational-function squareclasses because
`chi(s1/s2)=chi(s1*s2)`.

## P27 Result

The p27 quotient rows did not collapse under the `E'` map in this random
sample, so the train/heldout row counts match the original quotient counts:

```text
d3 train rows = 2000
d3 heldout rows = 2000
d4 train rows after d3 = 992
d4 heldout rows after d3 = 1052
```

No exact candidates were found:

```text
d3 pole 5 exact_candidates = 0
d3 pole 7 exact_candidates = 0
d3 pole 9 exact_candidates = 0
d4 pole 5 exact_candidates = 0
d4 pole 7 exact_candidates = 0
d4 pole 9 exact_candidates = 0
```

Best p27 heldout scores after selecting on the train split:

```text
d3 pole 5 = 1032/2000 = 0.516000000
d3 pole 7 = 1045/2000 = 0.522500000
d3 pole 9 = 1032/2000 = 0.516000000

d4 pole 5 = 554/1052 = 0.526615970
d4 pole 7 = 556/1052 = 0.528517110
d4 pole 9 = 557/1052 = 0.529467681
```

These are not promotion evidence.  The train-best lifts mostly wash out on
heldout, and none are close to a theorem-shaped source.

## Guard Fields

The same screen ran on the non-degenerate guard fields `q=1471` and `q=1607`.
No exact candidate appeared at pole bounds `5`, `7`, or `9`:

```text
q1471 E' d3 rows = 100, d4 rows = 56, exact_candidates = 0
q1607 E' d3 rows = 98,  d4 rows = 56, exact_candidates = 0
```

Same-row best rates reached the `0.66` to `0.73` range in a few tiny guard
sets, but these are not promoted: the row counts are small, there is no
separate heldout field, exact line/two-line products on `E'` are already killed
over `q=1471` and `q=1607`, and the p27 heldout lift is weak.

## Interpretation

Positive:

```text
The E' quotient remains the best current structural lead.
The low-pole machinery now runs directly on the sharper quotient coordinates.
The right next validation surface is small-field exact algebra, not p27 random scoring.
```

Negative:

```text
Random low-pole sections/products on E' did not find f3 or f4.
The best p27 heldout lifts are too weak for a GPU sampler.
Small-field high rates are multiple-testing artifacts until an exact formula survives.
```

## Concrete Next Tests

1. Exact function-field extraction on `E'`:

```text
Derive the actual descended d3/d4 double covers over E' and compare their
divisor or Kummer classes.
```

2. Small-field Magma validation:

```text
Use the online Magma calculator in the p24 style for named formulas on
non-degenerate guard fields, preferably q=1471 and q=1607.
```

3. Smarter finite-field solver:

```text
If the next probe stays computational, make it exact and structured:
irreducible conics, divisor-class representatives, or a linear-algebra
squareclass solver on E', not another broad random coefficient sweep.
```

## Continue / Kill

```text
continue = E' function-field/divisor-class extraction
continue = online Magma validation for named small-field formulas
continue = exact finite-field solver on E' if tractable

kill = random low-pole section/product pilot on E' as a source
kill = GPU sampler from these marginal heldout lifts
kill = treating q1471/q1607 same-row high rates as promotion evidence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_eprime_lowpole_random_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_eprime_lowpole_random_probe_20260621.txt`
- Parent: [P27 E-Quotient Kernel-8 / 2-Isogeny Screen](p27_equotient_kernel8_2isogeny_screen_20260621.md)
- Related: [P27 E-Quotient Low-Pole Random Screen](p27_equotient_lowpole_random_screen_20260621.md)
- Related: [P27 E-Quotient Line-Product Screen](p27_equotient_line_product_screen_20260621.md)

```text
p27_eprime_lowpole_random_screen_rows=1/1
```
