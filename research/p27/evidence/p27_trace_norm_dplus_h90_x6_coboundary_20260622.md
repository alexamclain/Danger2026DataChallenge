# P27 Trace/Norm Dplus H90-X6 Coboundary Probe

Date: 2026-06-22

## Claim

The simple H90/root coboundary bridge to the post-Dplus `x6` class is
negative.

After `Dplus`, the next selected class is:

```text
d3 = chi(x6)
```

and the H90 second layer is:

```text
rho^2 = A_eta = U_eta + z*W_eta.
```

This probe tests whether `chi(x6)` is a low-weight product of H90 atoms or
first-order branch divisors of the form `rho +/- atom`.  It finds no exact
weight-`<=3` product and no train pattern that holds out.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_h90_x6_coboundary_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_x6_coboundary_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_h90_x6_coboundary_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-y 0 \
  --max-weight 3 \
  --top 16 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_x6_coboundary_probe_20260622.txt
```

## Result

Train group:

```text
raw_y_draws = 131072
nonsplit_y = 65766
Dplus_y = 16485
Dplus_candidates = 16398
analyzed_y = 8199
chi_UplusA_+1 = 65592
target_+1 = 4149
target_-1 = 4050
```

Heldout group:

```text
raw_y_draws = 131072
nonsplit_y = 65470
Dplus_y = 16454
Dplus_candidates = 16122
analyzed_y = 8061
chi_UplusA_+1 = 64488
target_+1 = 3986
target_-1 = 4075
```

Feature profile:

```text
active_features = 59
constant_features = 12
exact_combo_weight_le_3 = none
```

The best train-ranked product collapses on heldout:

```text
combo = eps_v * rho_actual_plus_plus_one * rho_other_plus_plus_t
train   = 4287/8199 = 0.522868643
heldout = 3990/8061 = 0.494975809
```

The best heldout-looking listed product is also not meaningful:

```text
combo = -rho_actual_plus_minus_C * rho_actual_plus_plus_B * rho_actual_plus_plus_C
train   = 4255/8199 = 0.518965728
heldout = 4084/8061 = 0.506636894
```

The heldout majority baseline is already:

```text
d3 = -1 majority = 4075/8061 = 0.505520407
```

## Interpretation

Positive:

```text
The H90 branch variables and the post-Dplus x6 class are now tested on the
same production-style Dplus stream.
The previous identity chi(U+A)=+1 is reproduced on every analyzed branch.
```

Negative:

```text
No simple H90/rho coboundary predicts chi(x6).
No exact low-weight branch-atom product survives.
Train-only skews are small and vanish on heldout.
This does not justify a GPU H90/x6 bucket or branch-root product mode.
```

## Consequence

The Dplus-H90 route remains a CAS/class-comparison problem:

```text
compare the x6 Kummer class with A_eta on the normalized cover;
look for a quotient/Prym relation or prove the class is fresh;
do not run more finite-field H90/rho sign buckets without a named theorem.
```

For GPU, the only Dplus ask that remains current is still bounded fused/native
pricing plus telemetry.  It should not promote a production search from
`rho +/- atom`, `eta/U/W/rho`, or `x6` squareclass buckets.

## Continue / Kill

```text
continue = Dplus fused/native exchange-rate test with raw source denominators
continue = exact CAS comparison of the x6 Kummer class with A_eta
continue = A-level Kummer extraction as the main post-Dplus class surface

kill = simple H90/rho coboundary product as a d3 predictor
kill = GPU production from H90/x6 sign buckets
kill = more low-weight rho +/- atom finite-field scans absent a named divisor
```

```text
p27_trace_norm_dplus_h90_x6_coboundary_rows=1/1
```
