# P27 K-Line Affine Recurrence Screen

Date: 2026-06-21

## Claim

The reduced K-line does not give a `d4`-from-`d3` recurrence through the
sourceable degree-one families:

```text
K -> a*K + b
K -> a/K + b
```

Over the p27-signature promotion fields `q = 7 mod 16`, the only full-coverage
affine map is identity, and it scores exactly like raw `d4` bias.  The
reciprocal-affine family has no full-coverage map in q1607, q1847, or q2087.
The q2039 identity exactness is explained by the already-known constant-`d4`
local degeneration.

This closes a real loophole between the killed Lattes/Belyi maps and full
branch-class extraction: a stable affine or reciprocal-affine recurrence would
have let later gates reuse the same K-line character without another
independent half-loss.

## Artifacts

Probe:

```text
research/p27/archive/gates/p27_kline_affine_recurrence_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q607_smoke_20260621.txt
research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q1471_stress_20260621.txt
research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q1607_q1847_q2039_q2087_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_affine_recurrence_probe.py \
  --small-primes 607 \
  --limit 5 \
  | tee research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q607_smoke_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_affine_recurrence_probe.py \
  --small-primes 1607,1847,2039,2087 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q1607_q1847_q2039_q2087_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_kline_affine_recurrence_probe.py \
  --small-primes 1471 \
  --limit 8 \
  | tee research/p27/archive/probe_outputs/p27_kline_affine_recurrence_probe_q1471_stress_20260621.txt
```

## Method

For fixed nonzero `a`, every covered pair determines:

```text
b = K_d3 - a*K_d4
```

So the exact screen counts all maps in `O(q * #d3 * #d4)` rather than scoring
`q^2` maps directly.  Both global polarities are allowed:

```text
d4(K) =  d3(phi(K))
d4(K) = -d3(phi(K))
```

where `phi(K)` is either `a*K+b` or `a/K+b`.

## Results

Promotion fields:

```text
q1607:
  d3 K rows = 49, d4 K rows = 28
  affine full coverage maps = 1
  best affine full coverage = identity, 19/28 = raw d4 majority
  reciprocal full coverage maps = 0
  best reciprocal coverage = 6/28

q1847:
  d3 K rows = 63, d4 K rows = 45
  affine full coverage maps = 1
  best affine full coverage = identity, 26/45 = raw d4 majority
  reciprocal full coverage maps = 0
  best reciprocal coverage = 7/45

q2087:
  d3 K rows = 57, d4 K rows = 25
  affine full coverage maps = 1
  best affine full coverage = identity, 18/25 = raw d4 majority
  reciprocal full coverage maps = 0
  best reciprocal coverage = 6/25
```

Degenerate promotion-signature field:

```text
q2039:
  d4 K rows = 19, all d4 targets are +1
  affine identity is full exact only because d4 is constant
  reciprocal full coverage maps = 0
```

Stress fields:

```text
q607:
  affine identity is full exact with opposite polarity
  reciprocal 4/K is full exact
  this is the known small-field/Belyi artifact

q1471:
  reciprocal 4/K has full coverage, but scores 14/28
  affine identity also scores 14/28
  no full exact affine or reciprocal-affine map
```

## Interpretation

Positive:

```text
The exact screen is broad enough to include ordinary affine recurrences and
reciprocal-affine/Belyi-like recurrences.
The q607 and q1471 stress behavior matches the existing guard-field story.
```

Negative:

```text
No stable q=7 mod 16 affine K-line recurrence maps d4 to d3.
No stable q=7 mod 16 reciprocal-affine recurrence maps d4 to d3.
The only full-coverage promotion-field map is identity, and it is raw bias.
```

The K-line remains the best reduced coordinate, but the next live work is the
actual branch divisor / Kummer class / genus extraction.  Do not spend GPU or
agent time searching degree-one K-line buckets or rational map restarts.

## Continue / Kill

```text
continue = branch-class/genus extraction over P1_K or P1_Sroot
continue = irreducible cubic/quartic class recovery if it is not blind fitting
continue = compare d4 only after a stable d3 branch class is named

kill = K-line affine recurrences K -> a*K+b
kill = K-line reciprocal-affine recurrences K -> a/K+b
kill = q607/q1471 stress-field affine positives as p27 promotion evidence
kill = GPU bucket/restart search from degree-one K-line maps
```

```text
p27_kline_affine_recurrence_rows=1/1
```
