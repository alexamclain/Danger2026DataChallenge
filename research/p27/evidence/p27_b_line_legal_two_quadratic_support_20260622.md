# P27 B-Line Legal-Domain Two-Quadratic Support Screen

Date: 2026-06-22

## Claim

The legal B-domain inside the core B bucket is not supported by a product of
two monic irreducible quadratic branch factors in any of the three
p27-signature promotion fields `q=1607,1847,2087`.

This is distinct from the previous `d3(B)` two-quadratic screen.  That screen
killed a split degree-4 explanation of the next selected bit on legal B.  This
screen kills the analogous split degree-4 explanation for the legal B subset
itself.

Together, they remove the nearest low-degree split-divisor B-line sampler:

```text
core B bucket -> legal B domain -> d3(B)
```

is not explained by rational-linear support of weight `<=4`, by one
irreducible quadratic plus up to two linears for `d3`, by two irreducible
quadratics for `d3`, or by two irreducible quadratics for the legal domain.

## Artifacts

Updated probe:

```text
research/p27/archive/gates/p27_b_line_branch_support_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_legal_twoquad_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1847_q2087_legal_twoquad_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_branch_support_probe.py \
  --small-primes 1607 \
  --max-weight 4 \
  --quadratic-pair-legal \
  | tee research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_legal_twoquad_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_branch_support_probe.py \
  --small-primes 1847,2087 \
  --max-weight 4 \
  --quadratic-pair-legal \
  | tee research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1847_q2087_legal_twoquad_20260622.txt
```

## Method

For each field, rows are the core B values.  The target bit is:

```text
0 if B is legal
1 if B is in the core bucket but not legal
```

The probe enumerates every monic irreducible quadratic

```text
Q(B)=B^2+uB+v
```

and records its squareclass vector on the core B rows.  It then uses
meet-in-the-middle to test whether a product of two such vectors matches the
legal-domain bit, up to global polarity.

## Results

`q=1607`:

```text
core_B = 200
legal_B = 49
irreducible_quadratics_tested = 1,290,421
unique_quadratic_masks = 1,290,421
result = none_two_irreducible_quadratics
```

`q=1847`:

```text
core_B = 230
legal_B = 63
irreducible_quadratics_tested = 1,704,781
unique_quadratic_masks = 1,704,781
result = none_two_irreducible_quadratics
```

`q=2087`:

```text
core_B = 260
legal_B = 57
irreducible_quadratics_tested = 2,176,741
unique_quadratic_masks = 2,176,741
result = none_two_irreducible_quadratics
```

The runs also reproduce the rational-linear baseline:

```text
d2/legal on core B has no rational-linear support of weight <=4
```

## Interpretation

Positive:

```text
The B-line sourceability question is now more sharply delimited.
The legal-domain obstruction is tested separately from the d3(B) obstruction.
```

Negative:

```text
The legal B-domain is not a split degree-4 Kummer character built from two
irreducible quadratic branch factors.
```

The remaining B-line route is therefore not a simple low-degree split-divisor
sampler.  It must be one of:

```text
irreducible quartic / cubic-plus-linear support found by actual extraction
higher-degree or non-visible Kummer class
low-genus quotient of the full legal source cover
recurrence/coupling among f3(B), f4(B), f5(B), ...
```

## Continue / Kill

```text
continue = Magma/Sage normalization of the legal/d3 B-line cover
continue = branch divisor/support-degree extraction over P1_B
continue = compare f3,f4,f5 if a tractable class is recovered

kill = legal-domain two-irreducible-quadratic support
kill = split low-degree B-line sampler from current visible branch families
kill = GPU production from B buckets without a source or recurrence
```

```text
p27_b_line_legal_two_quadratic_support_rows=1/1
```
