# P27 Lambda Low-Genus Screen

Date: 2026-06-22

## Claim

The lambda-line cubic source family is now closed for the decisive `d3` bit.
The remaining bounded low-genus lambda test is monic quartic support, which is
GPU-sized in the promotion fields.

The coordinate is:

```text
lambda = -K^2/4
```

Earlier lambda screens killed split degree `<=4` branch divisors and monomial
Belyi recurrences.  This screen adds exact all-monic cubic support:

```text
chi(lambda^3 + a*lambda^2 + b*lambda + c)
```

with global polarity allowed.  Exhausting all `q^2` `(a,b)` chunks and
intersecting constants gives zero exact cubics for `d3_on_lambda` in
q1471/q1607/q1847.

## Artifacts

Target packet:

```text
research/p27/archive/fixtures/p27_lambda_lowgenus_targets_20260622.json
```

Packet generator:

```text
research/p27/archive/gates/p27_lambda_lowgenus_target_packet.py
```

Verifier:

```text
research/p27/archive/gates/p27_lambda_lowgenus_verify.py
```

Chunk runner:

```text
research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1471_d3_deg3_full_20260622.txt
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1607_d3_deg3_full_20260622.txt
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1847_d3_deg3_full_20260622.txt
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1471_d3_deg3_start0_count2000_20260622.txt
```

## Target Rows

The frozen packet records:

```text
q1471 d3_on_lambda: rows=50, plus=28, minus=22
q1607 d3_on_lambda: rows=49, plus=28, minus=21
q1847 d3_on_lambda: rows=63, plus=45, minus=18

q1471 d4_on_lambda_after_d3: rows=28, plus=14, minus=14
q1607 d4_on_lambda_after_d3: rows=28, plus=19, minus=9
q1847 d4_on_lambda_after_d3: rows=45, plus=19, minus=26
```

## Commands

Generate packet:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_target_packet.py \
  --small-primes 1471,1607,1847 \
  --families d3_on_lambda,d4_on_lambda_after_d3 \
  > research/p27/archive/fixtures/p27_lambda_lowgenus_targets_20260622.json
```

Full cubic screens:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py \
  --field 1471 --family d3_on_lambda --degree 3 \
  --start 0 --count 2163841 \
  | tee research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1471_d3_deg3_full_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py \
  --field 1607 --family d3_on_lambda --degree 3 \
  --start 0 --count 2582449 \
  | tee research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1607_d3_deg3_full_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py \
  --field 1847 --family d3_on_lambda --degree 3 \
  --start 0 --count 3411409 \
  | tee research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1847_d3_deg3_full_20260622.txt
```

## Results

```text
q1471 d3 cubic: tuples_scanned=2163841, exact_polynomials=0
q1607 d3 cubic: tuples_scanned=2582449, exact_polynomials=0
q1847 d3 cubic: tuples_scanned=3411409, exact_polynomials=0
```

Random-sign expected exact counts:

```text
q1471 d3 cubic: 5.65e-6
q1607 d3 cubic: 1.47e-5
q1847 d3 cubic: 1.37e-9
```

So a stable cubic would have been highly meaningful; none exists.

## Remaining Quartic Test

The exact monic quartic family is still open:

```text
chi(lambda^4 + a*lambda^3 + b*lambda^2 + c*lambda + d)
```

The existing chunk runner reduces this to `q^3` `(a,b,c)` chunks by
intersecting possible constants `d`, matching the K/B quartic workflow.

Expected exact counts for `d3_on_lambda`:

```text
q1471 degree4: 8.32e-3
q1607 degree4: 2.37e-2
q1847 degree4: 2.52e-6
```

Thus a q1847 quartic hit would be a real low-genus clue, but it would still be
diagnostic until it lifts to the rational K-square stratum.

GPU/C run shape:

```bash
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py \
  --field 1847 \
  --family d3_on_lambda \
  --degree 4 \
  --start <chunk_start> \
  --count <chunk_count>
```

Full q1847 degree-4 work size:

```text
1847^3 = 6,300,985,823 coefficient triples before constant intersection
```

## Interpretation

Positive:

```text
The lambda low-genus screen now has frozen targets, verifier, and chunk runner.
The decisive cubic family is closed locally in all three guard fields.
The remaining quartic family is concrete and GPU-sized, not vague.
```

Negative:

```text
No genus-1 cubic lambda source exists for d3.
Lambda is still not a rational p27 source quotient by itself.
A quartic hit must be checked against the K-square lift before promotion.
```

## Continue / Kill

```text
continue = GPU/C exact monic quartic screen for q1847 d3_on_lambda
continue = verify any hit with p27_lambda_lowgenus_verify.py
continue = if quartic hits, compute genus/sourceability and K-square lift
continue = otherwise move to actual K-level branch-class extraction

kill = monic cubic lambda d3 source
kill = lambda-only source promotion without K-square lift
kill = d4 lambda fits before d3 is named
```

```text
p27_lambda_lowgenus_screen_rows=1/1
```
