# P27 Lambda Monomial Recurrence Screen

Date: 2026-06-22

## Claim

The Belyi-normalized lambda line does not reveal a `d3/d4` recurrence through
its canonical monomial self-maps.

The K-line normalization is:

```text
lambda = -K^2/4
```

with branch set:

```text
{0, 1, infinity}
```

Although `lambda` is not a rational p27 source quotient by itself, a
lambda-level recurrence would still be a serious clue for K-level
branch-class extraction.  The probe tested fixed maps:

```text
phi = left_S3 o (lambda -> lambda^m) o right_S3
```

for `m=2..12`, with all six S3 branch symmetries on both sides.  No exact
forward or reverse `d3/d4` recurrence appears in q1471/q1607/q1847.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_lambda_monomial_recurrence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_lambda_monomial_recurrence_probe_q1471_q1607_q1847_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_monomial_recurrence_probe.py \
  --small-primes 1471,1607,1847 \
  --degrees 2,3,4,5,6,7,8,9,10,11,12 \
  --keep-best 10 \
  | tee research/p27/archive/probe_outputs/p27_lambda_monomial_recurrence_probe_q1471_q1607_q1847_20260622.txt
```

## Results

Forward `d4(lambda) = +/- d3(phi(lambda))`:

```text
q1471: best covered 4/28, best matches 3
q1607: best covered 5/28, best matches 4
q1847: best covered 9/45, best matches 7
```

Reverse `d3(lambda) = +/- d4(phi(lambda))`:

```text
q1471: best covered 7/50,  best matches 5
q1607: best covered 6/49,  best matches 4
q1847: best covered 10/63, best matches 6
```

These are small partial overlaps, not sourceable recurrences.

## Interpretation

Positive:

```text
This closes the canonical branch-dynamics recurrence family on P1_lambda.
It is a fixed Belyi-map test, not another low-degree coefficient fit.
```

Negative:

```text
No S3-conjugated lambda -> lambda^m map for m=2..12 relates d3 and d4.
Coverage is too low to be a sampler or recurrence.
Lambda remains a normalization aid, not a recurrence/source line.
```

The live K/lambda task remains:

```text
recover the actual K-level branch class with the rational K-square stratum remembered
compute genus / support field degrees
compare d4 only after the d3 class is named
```

## Continue / Kill

```text
continue = K-level branch-class/genus extraction with lambda as normalization
continue = use lambda only to mark branch values 0,1,infinity
continue = theorem-specified recurrence only outside PGL2/monomial Belyi dynamics

kill = lambda monomial Belyi recurrence lambda -> lambda^m for m=2..12
kill = lambda as standalone rational source for p27
kill = GPU sampler from lambda without a K-square lift
```

```text
p27_lambda_monomial_recurrence_screen_rows=1/1
```
