# P27 E-Quotient Low-Pole Random Screen

Date: 2026-06-21

## Claim

A bounded low-pole random search on the residual elliptic quotient did not find
an explicit small `f3` or `f4` source function.  This is not a proof of
absence; it is a practical falsifier for the nearest small-function route after
the named Kummer basis failed.

```text
tested = small-integer sections of L(nO), plus products of two sections
result = no exact p27 candidate, no strong stable heldout lift
next = symbolic/function-field elimination, or a faster finite-field solver
```

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_lowpole_random_probe.py \
  --target 2000 \
  --heldout-target 2000 \
  --max-draws 500000 \
  --pole-bounds 5,7 \
  --trials 200 \
  --coeff-bound 3 \
  --small-primes 1087,1471 \
  | tee research/p27/archive/probe_outputs/p27_equotient_lowpole_random_probe_20260621.txt
```

The probe uses the Riemann-Roch basis on `E: W^2=X^3-X`:

```text
L(nO): 1, X, X^2, ..., W, XW, ...
```

and tests:

```text
section characters: chi(s)
product / rational-function characters: chi(s1*s2)
```

with small integer coefficients in `[-3,3]`.  Products model the squareclass
of a quotient `s1/s2`, since `chi(s1/s2)=chi(s1*s2)`.

## P27 Result

Train seed `20260621`, heldout seed `20260622`:

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
d4 pole 5 exact_candidates = 0
d4 pole 7 exact_candidates = 0
```

Best p27 heldout scores:

```text
d3 pole 5 train-best on heldout = 1037/2000 = 0.518500000
d3 pole 7 train-best on heldout = 1055/2000 = 0.527500000
d4 pole 5 train-best on heldout = 556/1052 = 0.528517110
d4 pole 7 train-best on heldout = 567/1052 = 0.538973384
```

These are not promotion evidence.  They are small, noisy lifts from a
200-trial pilot, not exact functions or stable theorem-shaped recurrences.

## Small Fields

Non-degenerate fields `q=1087` and `q=1471` were also screened.  Their row
counts are small, so high-looking rates are expected from random trials:

```text
q=1087: d3 rows = 72,  d4 rows = 40
q=1471: d3 rows = 200, d4 rows = 112
```

No exact candidate appeared in the pilot.  The small-field rates are useful
only as smoke tests that the low-pole machinery runs on non-degenerate fields,
not as evidence of a p27 recurrence.

## Interpretation

Positive:

```text
The low-pole screen is now executable and tied to the same p27 quotient rows as
the d3/d4 descent probes.
```

Negative:

```text
The nearest low-pole section/product route did not reveal f3 or f4.
The best p27 heldout lifts are too weak to drive a GPU sampler or theorem ask.
Pure Python large-prime Legendre scoring is slow for large random sweeps.
```

## Concrete Next Tests

1. Symbolic/function-field extraction:

```text
Use Magma/Sage to eliminate T, branch, and compactD variables and produce the
actual E-level double covers.  This is now preferred over more random search.
For small-field validation, the online Magma calculator is acceptable in the
same style as the p24 checks; reserve heavier local tooling for the larger
elimination/search pass.
```

2. Faster finite-field solver, if continuing computational extraction:

```text
Precompute Legendre/parity tables on non-degenerate small fields and implement
linear algebra / indexed search over L(nO) sections.  Use p27 only for final
validation of a named candidate, not for broad random scoring.
```

3. Validation standard:

```text
Promote only an exact f3/f4 formula, a stable heldout lift with a named
function, or a divisor/Kummer class relation.  Do not promote marginal random
pilot lifts.
```

## Continue / Kill

```text
continue = Magma/Sage function-field elimination for E-level f3/f4
continue = faster finite-field extraction on q=1087,1471,1607 if needed

kill = small random low-pole pilot as a source by itself
kill = p27 broad random scoring in pure Python
kill = GPU sampler from these marginal heldout lifts
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_equotient_lowpole_random_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_equotient_lowpole_random_probe_20260621.txt`
- Related: [P27 E-Quotient Kummer Basis Screen](p27_equotient_kummer_basis_screen_20260621.md)
- Related: [P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md)

```text
p27_equotient_lowpole_random_screen_rows=1/1
```
