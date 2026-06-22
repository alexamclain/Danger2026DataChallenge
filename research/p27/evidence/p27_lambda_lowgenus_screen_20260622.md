# P27 Lambda Low-Genus Screen

Date: 2026-06-22

## Claim

The lambda-line cubic source family is closed for the decisive `d3` bit, and
the q1847 monic-quartic promotion-field screen is now closed too.

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

Follow-up:
[P27 Lambda Quartic q1847 D3 Screen](p27_lambda_quartic_q1847_d3_screen_20260622.md)
then exhausts the exact monic quartic family in q1847 and also finds zero
hits.

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
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1847_d3_deg4_start0_count2000_20260622.txt
research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_full_20260622/SUMMARY.txt
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

## Quartic Test

The exact monic quartic family was then tested in the decisive q1847 field:

```text
chi(lambda^4 + a*lambda^3 + b*lambda^2 + c*lambda + d)
```

The existing chunk runner reduces this to `q^3` `(a,b,c)` chunks by
intersecting possible constants `d`, matching the K/B quartic workflow.

Expected exact counts for `d3_on_lambda` before the run:

```text
q1471 degree4: 8.32e-3
q1607 degree4: 2.37e-2
q1847 degree4: 2.52e-6
```

The q1847 full screen result is:

```text
triples_scanned = 6300872423
exact_quartics = 0
wall_seconds = 502.863578
wall_throughput_triples_per_second = 12529983.679
```

Thus the decisive q1847 low-genus lambda quartic clue is absent.  Smaller
q1471/q1607 quartic runs are now bookkeeping only unless a new theorem changes
the target family.

Reference run shape:

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
1847^3 = 6,300,872,423 coefficient triples before constant intersection
```

## Interpretation

Positive:

```text
The lambda low-genus screen now has frozen targets, verifier, and runners.
The decisive cubic family is closed locally in all three guard fields.
The q1847 quartic promotion-field screen is closed and negative.
```

Negative:

```text
No genus-1 cubic lambda source exists for d3.
No q1847 monic quartic lambda source exists for d3.
Lambda is still not a rational p27 source quotient by itself.
Any future lambda hit must be checked against the K-square lift before promotion.
```

## Continue / Kill

```text
continue = move to actual K-level branch-class extraction
continue = verify any future hit with p27_lambda_lowgenus_verify.py
continue = if a new lambda family hits, compute genus/sourceability and K-square lift

kill = monic cubic lambda d3 source
kill = q1847 monic quartic lambda d3 source
kill = lambda-only source promotion without K-square lift
kill = d4 lambda fits before d3 is named
```

```text
p27_lambda_lowgenus_screen_rows=1/1
```
