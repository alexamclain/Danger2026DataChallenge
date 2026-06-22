# P27 Lambda Branch-Divisor Screen

Date: 2026-06-21

## Claim

The Belyi-normalized K-line coordinate is useful, but the nearest genus `<=1`
lambda-line source family is negative for the decisive `d3` bit.

The screen tested exact double-cover selectors of the form:

```text
z^2 = f(lambda)
lambda = -K^2/4
deg_lambda(f) <= 4
```

where the branch divisor splits over each guard field into rational linear
factors and irreducible quadratic factors.  This extends the earlier K-line
degree `<=4` branch-divisor test, because degree `4` in `lambda` has degree
`8` in `K`.

## Probe

Gate:

```text
research/p27/archive/gates/p27_lambda_branch_divisor_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d3_20260621.txt
research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d4_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_lambda_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d3 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d3_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_lambda_branch_divisor_probe.py \
  --small-primes 1471,1607,1847 \
  --targets d4 \
  --max-degree 4 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d4_20260621.txt
```

## Results

### d3

There are no exact `d3` divisors in this family over the guard fields:

```text
q=1471 d3 exact divisors = none
q=1607 d3 exact divisors = none
q=1847 d3 exact divisors = none
```

Search sizes:

```text
q=1471 d3:
  lambda rows = 50
  linear atoms = 1421
  irreducible quadratic atoms = 1081185
  distinct degree-2 side masks = 2088676

q=1607 d3:
  lambda rows = 49
  linear atoms = 1558
  irreducible quadratic atoms = 1290421
  distinct degree-2 side masks = 2501768

q=1847 d3:
  lambda rows = 63
  linear atoms = 1784
  irreducible quadratic atoms = 1704781
  distinct degree-2 side masks = 3293435
```

### d4

The later bit again shows why `d4` must not be promoted before `d3` is named:

```text
q=1471 d4: degree-3 exact lambda divisors found
q=1607 d4: degree-3 exact lambda divisors found
q=1847 d4 exact divisors = none
```

Interpretation:

```text
The q1471/q1607 d4 fits are local interpolation artifacts.
They do not define a stable recurrence or source.
```

## Interpretation

Positive:

```text
The Belyi coordinate lambda is now executable in the same guard-field workflow.
The split low-degree branch-divisor family is decisively testable.
```

Negative:

```text
No genus <=1 lambda source with branch support split into degree 1/2 factors
explains the decisive d3 bit.
No GPU sampler follows from this lambda-line family.
```

The canonical lambda branch-dynamics recurrence is now negative too:
[P27 Lambda Monomial Recurrence Screen](p27_lambda_monomial_recurrence_screen_20260622.md).
It tests S3-conjugated maps `lambda -> lambda^m` for `m=2..12` and finds no
exact forward or reverse `d3/d4` recurrence in q1471/q1607/q1847.  The best
forward coverages are only `4/28`, `5/28`, and `9/45`.

The monic cubic low-genus family is now closed as well:
[P27 Lambda Low-Genus Screen](p27_lambda_lowgenus_screen_20260622.md).
It exhausts all exact `chi(lambda^3+a lambda^2+b lambda+c)` candidates for
`d3_on_lambda` in q1471/q1607/q1847 and finds zero exact cubics.  The remaining
bounded lambda source screen is monic quartic support, which is GPU-sized.

What remains:

```text
monic quartic lambda support
non-split higher-degree branch support
actual Magma/Sage normalization and genus computation from the source cover
```

## Next Test

Do not widen coefficient bounds blindly.  The next useful move is still the
branch-class computation:

```text
1. Normalize the d3 source cover over P^1_lambda.
2. Compute branch divisor degree and support field degrees.
3. Compute genus and compare d4 only after d3 is named.
4. Promote only if genus <=1, or if a named recurrence/sourceable walk appears.
```

Kill condition:

```text
The recovered d3 branch class has high/generic degree and d4 is an unrelated
fresh half-cover.
```

## Continue / Kill

```text
continue = Magma/Sage branch-class extraction over lambda
continue = exact monic quartic lambda support as the remaining bounded low-genus screen
kill = split degree <=4 lambda branch divisors for d3
kill = S3-conjugated lambda monomial recurrences for m=2..12
kill = monic cubic lambda support for d3
kill = q1471/q1607-only d4 lambda fits as recurrence evidence
```

## Linked Artifacts

- Parent: [P27 Kummer Belyi Structure Probe](p27_kummer_belyi_structure_probe_20260621.md)
- Probe: `research/p27/archive/gates/p27_lambda_branch_divisor_probe.py`
- Output: `research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d3_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_lambda_branch_divisor_probe_d4_20260621.txt`

```text
p27_lambda_branch_divisor_screen_rows=1/1
```
