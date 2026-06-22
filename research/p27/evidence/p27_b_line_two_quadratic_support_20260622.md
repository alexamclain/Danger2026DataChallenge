# P27 B-Line Two-Quadratic Support Screen

Date: 2026-06-22

## Claim

The descended `d3(B)` Kummer class on the p27 B-line is not supported by a
product of two monic irreducible quadratic branch factors in any of the three
p27-signature promotion fields `q=1607,1847,2087`.

This closes the most obvious remaining split degree-4 B-line branch-support
case after the earlier screens killed rational-linear support of weight `<=4`
and one irreducible quadratic times up to two rational linears.

It does not kill every degree-4 divisor on `P1_B`: irreducible quartic support
or cubic-plus-linear support would require a different extraction method.

## Artifacts

Updated probe:

```text
research/p27/archive/gates/p27_b_line_branch_support_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_twoquad_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1847_q2087_twoquad_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_branch_support_probe.py \
  --small-primes 1607 \
  --max-weight 4 \
  --quadratic-pair-d3 \
  | tee research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_twoquad_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_branch_support_probe.py \
  --small-primes 1847,2087 \
  --max-weight 4 \
  --quadratic-pair-d3 \
  | tee research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1847_q2087_twoquad_20260622.txt
```

## Method

For each field, the probe uses the legal B values and descended `d3` signs.
It enumerates every monic irreducible quadratic

```text
Q(B)=B^2+uB+v
```

and records the quadratic-character vector of `Q(B)` on the legal B rows.
Then it does a meet-in-the-middle search for two such vectors whose product
matches `d3(B)`, up to global polarity.

This is a structured Kummer-class screen on `P1_B`, not an unrestricted
coefficient fit.

## Results

`q=1607`:

```text
legal_B = 49
d3 plus/minus = 28 / 21
irreducible_quadratics_tested = 1,290,421
unique_quadratic_masks = 1,290,421
result = none_two_irreducible_quadratics
```

`q=1847`:

```text
legal_B = 63
d3 plus/minus = 45 / 18
irreducible_quadratics_tested = 1,704,781
unique_quadratic_masks = 1,704,781
result = none_two_irreducible_quadratics
```

`q=2087`:

```text
legal_B = 57
d3 plus/minus = 25 / 32
irreducible_quadratics_tested = 2,176,741
unique_quadratic_masks = 2,176,741
result = none_two_irreducible_quadratics
```

The same runs reproduced the previous rational-linear outcomes:

```text
d2 legal on core B: no rational-linear support of weight <=4
d3 on legal B: no rational-linear support of weight <=4
d4 after d3: unstable local weight-3 fits in q1607/q2087, none in q1847
```

## Interpretation

Positive:

```text
The B-line Kummer-class extraction target is sharper.
The missing split degree-4 case has a direct verdict across all promotion
fields.
```

Negative:

```text
d3(B) is not explained by two irreducible quadratic branch factors.
Together with prior screens, this kills the visible low-degree split-divisor
B-line path through the tested families.
```

Remaining:

```text
irreducible quartic support
cubic-plus-linear support
higher-degree or non-visible Kummer class
recurrence/coupling among f3(B), f4(B), ...
```

The next B-line test should be actual divisor/function-field extraction or a
CAS handoff that can compute the Kummer class, not another ad hoc factor
family unless it is tied to that extraction.

## Continue / Kill

```text
continue = B-line Kummer/divisor extraction for d3(B)
continue = compare extracted f3, f4, f5 classes if extraction succeeds
continue = CAS packet for irreducible quartic/cubic-plus-linear support only
           as part of function-field class extraction

kill = two-irreducible-quadratic support for d3(B)
kill = split low-degree B-line visible-factor search as a GPU reason
kill = using B buckets for production without an extracted source/sampler
```

```text
p27_b_line_two_quadratic_support_rows=1/1
```
