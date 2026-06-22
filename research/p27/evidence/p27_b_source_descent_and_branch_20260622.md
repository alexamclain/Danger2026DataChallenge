# P27 B-Source Descent And Branch Support

Date: 2026-06-22

## Claim

The B parameter is not an abstract square root.  On the residual label-2 source
it is the explicit rational quotient

```text
B = 8 X^2 / (X^2 - 1)^2,
A + 2 = B^2.
```

This is positive: after conditioning on legal `d2` rows, both `d3` and `d4`
descend to the B-line in p27 train/heldout and in q1607/q1847/q2087.  So the
right next theorem object is a Kummer character on a genus-0 B quotient.

The nearest simple branch-support versions are negative: the legal `d2` subset
inside the B core and the descended `d3` character are not products of up to
four rational linear factors in B.  The `d3` character is also not one
irreducible quadratic times up to two rational linear factors in any promotion
field.

## Artifacts

Probes:

```text
research/p27/archive/gates/p27_b_source_descent_probe.py
research/p27/archive/gates/p27_b_line_branch_support_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_b_source_descent_probe_p27_q1607_q1847_q2087_20260622.txt
research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_q1847_q2087_quad_20260622.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_source_descent_probe.py \
  --small-primes 1607,1847,2087 \
  --p27-target 6000 \
  --p27-heldout-target 6000 \
  --max-draws 1500000 \
  | tee research/p27/archive/probe_outputs/p27_b_source_descent_probe_p27_q1607_q1847_q2087_20260622.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_b_line_branch_support_probe.py \
  --small-primes 1607,1847,2087 \
  --max-weight 4 \
  --quadratic-d3 \
  | tee research/p27/archive/probe_outputs/p27_b_line_branch_support_probe_q1607_q1847_q2087_quad_20260622.txt
```

## Symbolic Identities

Using the residual source coordinate `X`:

```text
A = -2*(X^8 - 4X^6 - 26X^4 - 4X^2 + 1)/(X^2 - 1)^4
A + 2 = (8*X^2/(X^2 - 1)^2)^2
Bplus = 8*X^2/(X^2 - 1)^2
Bplus + 2 = 2*(X^2 + 1)^2/(X^2 - 1)^2
Bplus - 2 = -2*(X^2 - 2X - 1)*(X^2 + 2X - 1)/(X^2 - 1)^2
K = (X^4 - 6X^2 + 1)^2/(4*X*(X^2 - 1)*(X^2 + 1)^2)
```

The branch convention matches the K/A base parameterization:

```text
Bplus uses branch1:
  L = (B - 2)^4 / (8 B (B + 2)^2)

-Bplus uses branch0:
  L = -(B + 2)^4 / (8 B (B - 2)^2)
```

The probe found zero mismatches for `A+2=B^2`, branch `L=K^2`, and the core B
bucket on every p27 train/heldout and guard-field row.

## Descent Counts

On p27 train:

```text
Bplus_groups = 3000
Bplus_size_8 = 3000
Bplus_d3_plus_groups = 1494
Bplus_d3_minus_groups = 1506
Bplus_d4_plus_groups = 753
Bplus_d4_minus_groups = 741
```

On p27 heldout:

```text
Bplus_groups = 3000
Bplus_size_8 = 3000
Bplus_d3_plus_groups = 1526
Bplus_d3_minus_groups = 1474
Bplus_d4_plus_groups = 739
Bplus_d4_minus_groups = 787
```

Promotion fields:

```text
q1607:
  Bplus_groups = 49
  Bplus_size_16 = 49
  d3 plus/minus = 28 / 21
  d4 plus/minus = 19 / 9

q1847:
  Bplus_groups = 63
  Bplus_size_16 = 63
  d3 plus/minus = 45 / 18
  d4 plus/minus = 19 / 26

q2087:
  Bplus_groups = 57
  Bplus_size_16 = 57
  d3 plus/minus = 25 / 32
  d4 plus/minus = 18 / 7
```

There were no mixed `d3` groups and no mixed `d4` groups after `d3=+1` in
these tests.  Thus `d3` and `d4` descend at least to `Bplus`; they do not need
the finer `(B,K)`, `(B,Sroot)`, or source-orientation variables to be
well-defined.

## Branch-Support Screen

The B core contains all legal B values:

```text
q1607: core_B = 200, legal_B = 49, missing = 0
q1847: core_B = 230, legal_B = 63, missing = 0
q2087: core_B = 260, legal_B = 57, missing = 0
```

Rational-linear support up to four factors:

```text
d2 legal on core B:
  q1607: none weight <= 4
  q1847: none weight <= 4
  q2087: none weight <= 4

d3 on legal B:
  q1607: none weight <= 4
  q1847: none weight <= 4
  q2087: none weight <= 4
```

For `d3`, the probe also tested one irreducible quadratic times up to two
rational linear factors:

```text
q1607:
  irreducible_quadratics_tested = 1290421
  result = none

q1847:
  irreducible_quadratics_tested = 1704781
  result = none

q2087:
  irreducible_quadratics_tested = 2176741
  result = none
```

The `d4` small-field linear screen is not stable:

```text
q1607: local weight-3 rational-linear fit
q1847: none weight <= 4
q2087: different local weight-3 rational-linear fit
```

So `d4` should not be promoted from this screen.

## Interpretation

Positive:

```text
B is a real genus-0 quotient of the residual source, not just a fitted
coordinate.
d3 descends to B on the legal source.
d4 after d3 also descends to B in the tested samples.
This sharply focuses the moonshot: extract the Kummer class on P1_B.
```

Negative:

```text
The legal B-domain is not a product of <=4 rational linear branch factors.
The d3 bit is not a product of <=4 rational linear branch factors.
The d3 bit is not one irreducible quadratic times <=2 rational linear factors.
The visible low-degree B-line factor search is therefore killed.
```

## Next Test

The next first-class theorem/CAS target is:

```text
Compute the Kummer class for d3 on P1_B.
```

Concretely:

```text
B = 8 X^2/(X^2 - 1)^2
source covers:
  W^2 = X^3 - X
  T^2 = X(X^2+1)(X^2+2X-1)
  compactD = -1
  legal d2 source
descended target:
  d3(B)
```

Promotion requires one of:

```text
genus <= 1 quotient or sourceable walk
explicit branch divisor/Kummer class on B with degree small enough to sample
repeated coupling law that also explains d4/d5
```

Do not continue broad visible-factor guessing on B.  The next attempt should
use Magma/Sage/function-field divisor extraction, or a deliberately broader
branch-support search such as two irreducible quadratic factors only if it is
implemented as a structured Kummer-class computation rather than another
bucket scan.

## Continue / Kill

```text
continue = B-line Kummer class extraction for d3
continue = quotient/genus computation for the legal B cover
continue = test whether the extracted class recurs for d4/d5

kill = B-atom products as d3/d4 predictors
kill = rational-linear branch support of degree <= 4
kill = one irreducible quadratic plus <=2 rational linears for d3
kill = large GPU search from B without an extracted class or sampler
```

```text
p27_b_source_descent_and_branch_rows=1/1
```
