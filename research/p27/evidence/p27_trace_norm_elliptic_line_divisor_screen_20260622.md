# P27 Trace/Norm Elliptic Line-Divisor Screen

Date: 2026-06-22

## Claim

The first visible divisor family on the trace/norm elliptic quotient does not
explain the remaining line selector and is not a GPU source-narrowing candidate.

On the quotient

```text
C: b^2 = 16 - a^4
E: v^2 = u^3 - u
u = 4/a^2
v = 2b/a^3
```

the bounded screen checked the `L(3O)`-type line divisors:

```text
vertical: u - c
affine:   v + m*u + c
```

for `m,c in [-4,4]`.

## Artifacts

Gate:

```text
research/p27/archive/gates/p27_trace_norm_elliptic_line_divisor_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_elliptic_line_divisor_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_elliptic_line_divisor_probe.py \
  --seed-groups 'train:121,122;heldout:123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 256 \
  --bound 4 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_elliptic_line_divisor_probe_20260622.txt
```

## Result

Train sample:

```text
raw_draws = 65536
domain_records = 65504
target_records = 32458
candidate_count = 90
domain exact_count = 0
target exact_count = 0
domain best_lift = 1.009
target best_lift = 1.019
```

Heldout sample:

```text
raw_draws = 65536
domain_records = 65446
target_records = 32662
candidate_count = 90
domain exact_count = 0
target exact_count = 0
domain best_lift = 1.009
target best_lift = 1.011
```

The best heldout target candidate was `vertical_u_-4` with:

```text
selected = 16620
selected_plus = 8436
target_per_source = 0.128723144
```

This is noise-scale and well below the `1.25x` raw-source promotion bar.

## Interpretation

Positive:

```text
The C -> E map and target normalization are stable on fresh heldout samples.
The visible elliptic-line divisor family is now explicitly bounded.
```

Negative:

```text
No exact squareclass appears among vertical or affine line divisors.
No heldout lift is large enough to justify a GPU source/sampler pass.
The trace/norm identity, if real, is not a small visible L(3O) divisor.
```

## Continue / Kill

```text
continue = non-visible theta/additive/Hilbert-90 identity on C/E
continue = direct Dplus sampler/source only if it avoids raw-y rejection
continue = test named finite-field squareclass proposals, not broad line scans

kill = vertical u-c line-divisor explanation for domain_line or T_line
kill = affine v + m*u + c explanation for |m|,|c| <= 4
kill = GPU production filter from small elliptic-line divisor buckets
```

```text
p27_trace_norm_elliptic_line_divisor_screen_rows=1/1
```
