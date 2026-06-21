# P27 E-Quotient Kummer Basis Screen

Date: 2026-06-21

## Claim

The descended d3/d4 bits on `E: W^2=X^3-X` are not explained by the named
torsion, 2-descent, and order-4/Hilbert-90 Kummer factors already present in
the p27 label-2 analysis.

```text
positive = d3 and d4 are quotient-level bits on E
negative = visible named E-basis products do not explain them
next = symbolic/function-field extraction of the actual E-level double covers
```

## Probe

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_equotient_kummer_basis_probe.py \
  --target 5000 \
  --heldout-target 5000 \
  --max-draws 1000000 \
  --small-primes 1087,1471,1607 \
  | tee research/p27/archive/probe_outputs/p27_equotient_kummer_basis_probe_20260621.txt
```

Basis:

```text
X, W, X-1, X+1,
X2+1, X2+2X-1, X2-2X-1,
S, S_conj, mt_linear, m0, mt_coeff, prefactor, L
```

This is the named structural basis from the residual elliptic quotient and the
order-4 lift, not an arbitrary rational-function search.

## P27 Train / Heldout Result

Train seed `20260621`:

```text
d3 rows = 5000
d4 rows after d3 = 2466
d3 exact_combos = 0
d4 exact_combos = 0
d3 best = 2572/5000 = 0.514400000, combo = -mt_coeff
d4 best = 1312/2466 = 0.532035685, combo = X2-2X-1
```

Heldout seed `20260622`:

```text
d3 rows = 5000
d4 rows after d3 = 2522
d3 exact_combos = 0
d4 exact_combos = 0
d3 heldout-best = 2640/5000 = 0.528000000, combo = m0*prefactor
d4 heldout-best = 1332/2522 = 0.528152260, combo = -L
```

The train-best products do not replicate:

```text
d3 train best on heldout = 2522/5000 = 0.504400000
d4 train best on heldout = 1280/2522 = 0.507533703
```

Interpretation:

```text
The apparent small lifts are in-sample artifacts or weak correlations, not a
stable source/recurrent character.
```

## Non-Degenerate Small Fields

The earlier tiny fields `607, 863, 991` made d4 constant after d3, so this
probe used non-degenerate fields where d4 has both signs:

```text
q=1087: d3 plus/minus = 40/32,  d4 plus/minus = 20/20
q=1471: d3 plus/minus = 112/88, d4 plus/minus = 56/56
q=1607: d3 plus/minus = 112/84, d4 plus/minus = 76/36
```

No exact named-basis product appears:

```text
q=1087: d3 exact = 0, d4 exact = 0
q=1471: d3 exact = 0, d4 exact = 0
q=1607: d3 exact = 0, d4 exact = 0
```

Small-field best rates are higher because the quotient row counts are small,
but the absence of exact products across non-degenerate fields is the decisive
screen.

## Interpretation

Positive:

```text
The problem is now localized: d3 and d4 are E-level quadratic/source
characters, not full compactD-fiber data.
```

Negative:

```text
They are not visible products of the currently named torsion/2-descent/H90
functions on E.
The existing structural basis does not give a direct sampler, recurrence, or
GPU filter beyond constant-factor prefix filtering.
```

## Concrete Next Tests

1. Function-field extraction:

```text
Use Magma/Sage to eliminate the compactD/T/branch variables and construct the
actual E-level double cover for d3.  Repeat for d4 after d3.
```

2. Divisor-class comparison:

```text
Compute the divisors/classes of the extracted f3 and f4 on E.  Test whether
f4 is a translate, pullback, Frobenius/CM image, or low-degree isogeny image of
f3.
```

3. Non-degenerate validation:

```text
Validate any proposed f3/f4 formula on p27 and on non-degenerate small fields
such as q=1087,1471,1607.  Do not use q=607/863/991 d4 constants as positive
recurrence evidence.
```

## Continue / Kill

```text
continue = symbolic/function-field extraction of f3/f4
continue = divisor/Kummer class comparison after extraction
continue = non-degenerate finite-field validation of any proposed recurrence

kill = visible named E-basis product for d3/d4
kill = marginal in-sample Kummer-basis lifts
kill = treating the current E-basis as a GPU sampler
```

## Linked Artifacts

- Gate: `research/p27/archive/gates/p27_equotient_kummer_basis_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_equotient_kummer_basis_probe_20260621.txt`
- Related: [P27 Reverse Source D4 Recurrence Screen](p27_reverse_source_d4_recurrence_20260621.md)
- Related: [P27 Reverse Source Quotient Screen](p27_reverse_source_quotient_screen_20260621.md)
- Related: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)

```text
p27_equotient_kummer_basis_screen_rows=1/1
```
