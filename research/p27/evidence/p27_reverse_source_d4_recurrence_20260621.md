# P27 Reverse Source D4 Recurrence Screen

Date: 2026-06-21

## Claim

After conditioning on `compactD=-1` and d3 passing, the d4 bit also descends
to the residual elliptic quotient `E: W^2=X^3-X`.  This is real structure, but
the first recurrence screens do not yet produce a sqrt-beating law.

```text
positive = d3 and d4 are both quotient-level bits on E
negative = no p27 low-degree line source for d4
negative = small-field simple-transform recurrences are degenerate constants
next = identify and compare the actual E-level double covers for d3 and d4
```

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_reverse_source_d4_recurrence_probe.py \
  --target 5000 \
  --max-draws 1000000 \
  --small-primes 607,863 \
  --p27-line-bound 2 \
  | tee research/p27/archive/probe_outputs/p27_reverse_source_d4_recurrence_probe_20260621.txt
```

Supplementary tiny-field check:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_reverse_source_d4_recurrence_probe.py \
  --target 1000 \
  --max-draws 300000 \
  --small-primes 991 \
  --p27-line-bound 1 \
  | tee research/p27/archive/probe_outputs/p27_reverse_source_d4_recurrence_probe_q991_20260621.txt
```

The probe groups candidates by residual elliptic point `(X,W)`.  It records
the descended d3 bit, then only on d3-positive fibers records the descended d4
bit.  It also tests small line characters and, in small fields, obvious
elliptic transformations:

```text
id, negation, add rational 2-torsion, double, double plus rational 2-torsion
```

## P27 Result

On 5,000 p27 quotient fibers:

```text
d3_quotient_rows = 5000
d3_plus_E_points = 2466
d3_minus_E_points = 2534
d3_not_descended_to_E = 0

d4_quotient_rows_after_d3 = 2466
d4_plus_E_points_after_d3 = 1276
d4_minus_E_points_after_d3 = 1190
d4_not_descended_to_E = 0
d4_missing_on_E_orbit = 0
```

So d4 is again quotient-level.  It is not hidden in the compactD fiber, the
paired `T` roots, or the branch choice.

The p27 small-coefficient line screen is not a source:

```text
line_rows = 2466
small_coeff_lines_tested = 124
exact_lines = 0
best_good = 1310/2466 = 0.531224655
best_line = X - 1
```

The `0.531` score is not enough to promote; it is a small finite-sample lift
from a tiny line family, not an exact or held-out theorem shape.

## Small-Field Recurrence Warning

The small fields are useful for falsifying exact line characters, but the d4
recurrence screen is degenerate in these examples:

```text
q=607: d4_plus = 0,  d4_minus = 64, exact line = constant -1
q=863: d4_plus = 0,  d4_minus = 48, exact line = constant -1
q=991: d4_plus = 72, d4_minus = 0,  exact line = constant +1
```

Accordingly, the simple elliptic-transform recurrences in those small fields
are not promotion evidence.  They are explained by d4 being constant on the
tiny d3-positive locus, not by a nontrivial p27 recurrence.

## Interpretation

Positive:

```text
The all-plus tower bits are not random functions on the full label-2 fiber.
At least d3 and d4 descend to the same residual elliptic quotient E.
This makes an E-level divisor/theta/Kummer analysis more plausible and much
smaller than the full compactD/order-4 cover.
```

Negative:

```text
d4 still looks like a fresh half-cover on p27.
No low-degree p27 line character explains d4.
The small-field exact transform screens are degenerate and should not drive a
GPU sampler or theorem claim.
```

## Concrete Next Tests

1. E-level double-cover extraction:

```text
Derive explicit rational functions f3(X,W), f4(X,W) such that
  chi(f3) = d3 bit
  chi(f4) = d4 bit after d3
on the p27 quotient fibers.
Then compare their divisors/classes on E.
```

2. Non-line basis screen:

```text
Test a small principled basis from E divisors/torsion/theta functions, not an
unstructured line sweep.  The target is an exact function or a named cover,
not a marginal in-sample lift.
```

3. Larger validation field:

```text
Use Magma/Sage on a non-degenerate field where d4 is not constant to test
whether f4 is a translate/pullback of f3.  The q=607/863/991 constants are
not enough.
```

4. GPU telemetry framing:

```text
GPU prefix filters d1+d2+d3+d4 remain constant-factor unless the E-level
classes repeat or become sourceable by a low-cost walk.
```

## Continue / Kill

```text
continue = derive E-level f3/f4 and compare divisor classes
continue = search only named E-level theta/Kummer/torsion bases
continue = use larger non-degenerate Magma/Sage validation for recurrence

kill = compactD-fiber branch/T choice for d4
kill = degree-1 p27 line source for d4
kill = treating tiny-field constant d4 as recurrence evidence
kill = GPU sampler from d4 without an E-level source or recurrence
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_reverse_source_d4_recurrence_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_reverse_source_d4_recurrence_probe_20260621.txt`
- q991 output: `research/p27/archive/probe_outputs/p27_reverse_source_d4_recurrence_probe_q991_20260621.txt`
- Related: [P27 Reverse Source Quotient Screen](p27_reverse_source_quotient_screen_20260621.md)
- Related: [P27 Label-2 Alpha/Branch Recurrence Probe](p27_label2_alpha_branch_recurrence_20260621.md)

```text
p27_reverse_source_d4_recurrence_rows=1/1
```
