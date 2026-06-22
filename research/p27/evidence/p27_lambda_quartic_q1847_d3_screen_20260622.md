# P27 Lambda Quartic q1847 D3 Screen

Date: 2026-06-22

## Claim

The decisive q1847 monic-quartic lambda screen is negative:

```text
coordinate = lambda = -K^2/4
family = d3_on_lambda
exact_quartics = 0
```

This closes the remaining visible low-genus lambda support test in the
promotion field.  Lambda remains useful as a normalization coordinate, but the
sqrt-beating route now has to be actual K-level branch/class extraction with
the rational K-square stratum preserved.

## Artifacts

The existing fast quartic oracle is now coordinate-generic:

```text
research/p27/archive/gates/p27_quartic_chunk_fast.c
research/p27/archive/gates/p27_quartic_target_export.py
research/p27/archive/gates/p27_quartic_fast_shard_runner.py
```

It now accepts:

```text
--coordinate lambda
```

Target packet:

```text
research/p27/archive/fixtures/p27_lambda_lowgenus_targets_20260622.json
```

Run outputs:

```text
research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1847_d3_deg4_start0_count2000_20260622.txt
research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_smoke_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_10m_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_full_20260622/SUMMARY.txt
research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_full_20260622/lambda_1847_d3_on_lambda_rows.txt
```

## Validation

The C oracle was first checked against the Python lambda low-genus chunk
runner:

```text
q1847 d3_on_lambda degree 4
start = 0
count = 2000
Python exact_polynomials = 0
C exact_quartics = 0
```

Then a 10M-triple timing chunk was run:

```text
triples_scanned = 10000000
exact_quartics = 0
wall_seconds = 0.999667
wall_throughput_triples_per_second = 10003329.432
```

## Full Screen

```text
coordinate = lambda
field = 1847
family = d3_on_lambda
rows = 63
plus/minus = 45/18
total_triples = 6300872423
triples_scanned = 6300872423
polarity_-1_hits = 0
polarity_1_hits = 0
exact_quartics = 0
wall_seconds = 502.863578
wall_throughput_triples_per_second = 12529983.679
```

The exact quartic family tested was:

```text
chi(lambda^4 + a*lambda^3 + b*lambda^2 + c*lambda + d)
```

with both global polarities allowed and zeros rejected.

## Commands

Python/C smoke:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_lambda_lowgenus_chunk_probe.py \
  --field 1847 \
  --family d3_on_lambda \
  --degree 4 \
  --start 0 \
  --count 2000 \
  | tee research/p27/archive/probe_outputs/p27_lambda_lowgenus_chunk_probe_q1847_d3_deg4_start0_count2000_20260622.txt

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_fast_shard_runner.py \
  --coordinate lambda \
  --field 1847 \
  --family d3_on_lambda \
  --out-dir research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_smoke_20260622 \
  --workers 1 \
  --chunk-size 2000 \
  --max-triples 2000 \
  --sample-limit 8
```

Full q1847 screen:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_quartic_fast_shard_runner.py \
  --coordinate lambda \
  --field 1847 \
  --family d3_on_lambda \
  --out-dir research/p27/archive/probe_outputs/p27_quartic_lambda1847_d3_full_20260622 \
  --workers 10 \
  --chunk-size 50000000 \
  --sample-limit 16
```

## Interpretation

Positive:

```text
The lambda quartic question is now closed in the decisive field without GPU.
The generic fast quartic oracle can now validate B, K, and lambda target rows.
```

Negative for the moonshot:

```text
There is no visible monic quartic lambda d3 source in q1847.
Together with the cubic lambda kill, the low-genus lambda route is exhausted
through quartic in the promotion field.
```

This does not kill K/lambda entirely.  It kills the visible lambda-line
low-degree source model.  The remaining K/lambda work is:

```text
actual K-level branch class extraction
check whether any lambda-level class lifts to the rational K-square stratum
compute genus/support field degrees for the normalized K cover
```

## Continue / Kill

```text
continue = K-level branch/class extraction with K-square stratum preserved
continue = use lambda only as a normalization coordinate
continue = verify any future lambda hit with p27_lambda_lowgenus_verify.py

kill = monic cubic lambda support for d3
kill = q1847 monic quartic lambda support for d3
kill = lambda-only source promotion without K-square lift
kill = GPU lambda quartic production unless a new family or target appears
```

```text
p27_lambda_quartic_q1847_d3_screen_rows=1/1
```
