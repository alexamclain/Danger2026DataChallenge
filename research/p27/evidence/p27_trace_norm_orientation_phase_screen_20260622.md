# P27 Trace/Norm Orientation Phase Screen

Date: 2026-06-22

## Claim

The exact `D_plus` cover orientation signs are useful bookkeeping, but they do
not give a stable post-Dplus selector for the next selected gates.

This strengthens the earlier post-Dplus screen:

```text
Dplus = exact first-two-gate prefix
eps_h, eps_v = exact cover orientation phases
post-Dplus d3/d4 by orientation state = random-looking half-loss
```

So trace/norm `D_plus` remains a real algebraic narrowing target, but the
orientation phases should not be promoted as GPU buckets or a later-gate
recurrence.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_orientation_phase_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_orientation_phase_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_orientation_phase_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-rows 20000 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_orientation_phase_probe_20260622.txt
```

The probe reuses the production C-style `Dplus` stream from
`p27_trace_norm_post_dplus_probe.py`, then attaches the exact cover signs from
`p27_trace_norm_dplus_cover_probe.py`:

```text
t = y - 1
C = t^2 + 2t - 1
eps_h = chi(t)
eps_v = chi((t+1)C)
```

It also scores the named half-norm signs `H`, `VQ`, `T_line`,
`hcore_chi`, and `vcore_chi` against `d3` and `d4`.

## Counts

First seed group:

```text
seeds = 121,122
raw_y_draws = 131,072
nonsplit_y = 65,766
Dplus_y = 16,485
Dplus_candidates = 16,398
d3_+1 = 8,298
d3_-1 = 8,100
d4_+1 = 4,062
d4_-1 = 4,236
usable_rows = 16,398
```

Second seed group:

```text
seeds = 123,124
raw_y_draws = 131,072
nonsplit_y = 65,470
Dplus_y = 16,454
Dplus_candidates = 16,122
d3_+1 = 7,972
d3_-1 = 8,150
d4_+1 = 3,904
d4_-1 = 4,068
usable_rows = 16,122
```

## Orientation Tables

For `d3`, the four `(eps_h, eps_v)` buckets stay near half and the apparent
best state changes between seed groups:

```text
seeds 121,122:
  ++ 0.507352
  +- 0.508068
  -+ 0.494010
  -- 0.515046
  overall 0.506037

seeds 123,124:
  ++ 0.489247
  +- 0.474673
  -+ 0.513089
  -- 0.499249
  overall 0.494479
```

For `d4` after conditioning on `d3`, the same instability remains:

```text
seeds 121,122:
  ++ 0.451207
  +- 0.497593
  -+ 0.495635
  -- 0.513409
  overall 0.489515

seeds 123,124:
  ++ 0.486513
  +- 0.490649
  -+ 0.503710
  -- 0.476953
  overall 0.489713
```

Adding `T_line` creates eight smaller states and occasional higher rates, but
they do not replicate as a named bucket.  For example:

```text
seeds 121,122 d4:
  eps_h=+1,eps_v=-1,T_line=+1 0.527619
  eps_h=-1,eps_v=-1,T_line=+1 0.528517

seeds 123,124 d4:
  eps_h=-1,eps_v=+1,T_line=-1 0.536630
```

The high state moves between seed groups, which is the expected noise pattern.
The `H,VQ` and `hcore_chi,vcore_chi` tables are likewise near half.

## Interpretation

Positive:

```text
The actual D_plus cover orientation phases can now be attached to C-style rows.
Dplus again behaves as an exact two-gate prefix with no prefix failures.
The screen closes a tempting gap left by the low-weight character product test.
```

Negative:

```text
eps_h and eps_v do not predict d3 or d4 in a stable way.
H/VQ/T_line orientation buckets do not produce a heldout selector.
Any apparent state lift pays a 4-way or 8-way bucket denominator and falls far
below the raw-source promotion bar.
```

## Continue / Kill

```text
continue = trace/norm Dplus as an exact two-gate cover and quotient/Prym object
continue = search for a low-genus quotient or direct source that reaches beyond
           the first two selected gates
continue = use eps_h/eps_v only as diagnostic telemetry when already available

kill = eps_h/eps_v buckets as GPU production filters
kill = H/VQ/T_line orientation buckets as post-Dplus recurrence selectors
kill = treating the Dplus 4x conditional lift as evidence for late-depth law
```

## Linked Artifacts

- Prior post-Dplus screen: [P27 Trace/Norm Post-Dplus Screen](p27_trace_norm_post_dplus_screen_20260621.md)
- Dplus cover: [P27 Trace/Norm D_plus Cover](p27_trace_norm_dplus_cover_20260621.md)
- Source-orientation cost: [P27 Trace/Norm Source-Orientation Cover](p27_trace_norm_source_orientation_cover_20260621.md)
- Half-norm test card: [P27 Trace/Norm Half-Norm Test Card](p27_trace_norm_halfnorm_test_card_20260622.md)

```text
p27_trace_norm_orientation_phase_screen_rows=1/1
```
