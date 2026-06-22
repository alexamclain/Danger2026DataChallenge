# P27 Trace/Norm Dplus H90 Payload Screen

Date: 2026-06-22

## Claim

The named H90 second-layer payload does not give a cheap post-Dplus predictor
for `d3` or `d4` on C-style p27 rows.

The tested payload was:

```text
A_eta = U_eta + z*W_eta
rho^2 = A_eta
```

On rows already conditioned by `Dplus`, all tested `A_eta` squareclasses are
tautologically square:

```text
A_actual = +1
A_actual_conj = +1
A_other_plus = +1
A_other_minus = +1
```

The remaining non-tautological signs (`eta`, `U_eta`, `W_eta`, opposite-eta
variants, and deterministic square-root orientations) do not hold out as
predictors.  This kills the cheap GPU telemetry/source shortcut from the H90
payload.  The only remaining Dplus-H90 route is an actual Kummer/cover-class
comparison with `d3`, not another sign-bucket screen.

## Probe

Gate:

```text
research/p27/archive/gates/p27_trace_norm_dplus_h90_payload_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_payload_probe_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_trace_norm_dplus_h90_payload_probe.py \
  --seed-groups '121,122;123,124' \
  --chunks 0,1 \
  --tids 0:64 \
  --draws-per-thread 512 \
  --max-rows 20000 \
  --max-weight 3 \
  --top 12 \
  | tee research/p27/archive/probe_outputs/p27_trace_norm_dplus_h90_payload_probe_20260622.txt
```

## Counts

Train group:

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
```

Heldout group:

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
```

The H90 payload squareclasses are tautological on both groups:

```text
train:
  h90_A_actual_+1 = 16,398
  h90_A_actual_conj_+1 = 16,398
  h90_A_other_plus_+1 = 16,398
  h90_A_other_minus_+1 = 16,398

heldout:
  h90_A_actual_+1 = 16,122
  h90_A_actual_conj_+1 = 16,122
  h90_A_other_plus_+1 = 16,122
  h90_A_other_minus_+1 = 16,122
```

## Heldout Screen

For `d3`, the best low-weight H90 payload product on train does not hold out:

```text
best train combo = U_actual
train = 8380/16398 = 0.511037931
heldout = 8052/16122 = 0.499441757
```

For `d4`, the best train combo also collapses:

```text
best train combo = -eta * U_other
train = 4300/8298 = 0.518197156
heldout = 3978/7972 = 0.498996488
```

The best heldout-looking listed `d4` product is still not a promotion:

```text
combo = U_actual * W_other
train = 4242/8298 = 0.511207520
heldout = 4064/7972 = 0.509784245
```

That is below the heldout majority baseline for `d4=-1`:

```text
heldout d4 majority = 4068/7972 = 0.510286001
```

No exact H90 payload product of weight `<=3` was found for either `d3` or
`d4`.

## Interpretation

Positive:

```text
The H90 payload formulas are instrumented on the production-style Dplus rows.
The tautological squareclass behavior is now explicit.
The cheap sign/orientation telemetry path is closed by heldout data.
```

Negative:

```text
A_eta signs do not predict d3/d4; they are already paid by Dplus.
U/W/eta/root-orientation products do not beat heldout majority baselines.
There is no GPU-promotable H90 bucket from this screen.
```

## Next Test

The next Dplus-H90 test must be a real cover-class comparison:

```text
compute or model the d3 Kummer class on E_h90(z)
compare it to A_eta = U_eta + z*W_eta
test equality, recurrence, or Prym relation at the divisor/function-field level
```

Do not run more low-weight H90 sign screens unless a new theorem names a
specific finite-field class.

Bridge update:
[P27 Trace/Norm Dplus A-Descent Bridge](p27_trace_norm_dplus_a_descent_20260622.md)
shows that post-Dplus `d3` and `d4` descend to whole `A` fibers in three p27
seed groups, with zero mixed `A` groups.  Therefore the practical class
comparison should first route through the normalized A-line Kummer classes.
The H90 model remains useful only if it identifies the same A-level class,
gives a lower-genus quotient, or supplies a direct Dplus source.

Sharper bridge update:
[P27 Trace/Norm Dplus H90-X6 Coboundary Probe](p27_trace_norm_dplus_h90_x6_coboundary_20260622.md)
tests the post-Dplus `d3=chi(x6)` class directly against simple H90 atoms and
first-order `rho +/- atom` branch divisors.  There is no exact weight-`<=3`
product, and the best train skew falls to heldout noise.  This kills the
cheap H90-root coboundary bucket version of the comparison.

## Continue / Kill

```text
continue = exact d3 Kummer/divisor extraction on E_h90(z)
continue = compare d3 cover class with A_eta
continue = route post-Dplus d3/d4 comparison through A-level Kummer extraction
continue = GPU only for a named d3/A_eta telemetry class

kill = H90 payload signs as a production GPU filter
kill = low-weight products of eta,U,W,rho orientations
kill = simple rho +/- atom coboundary products as d3 predictors
kill = treating A_eta squareclass as new information after Dplus
```

## Linked Artifacts

- H90 branch class: [P27 Trace/Norm Dplus H90 Branch Class](p27_trace_norm_dplus_h90_branch_class_20260622.md)
- H90 quartic model: [P27 Trace/Norm Dplus H90 Quartic Model](p27_trace_norm_dplus_h90_quartic_model_20260622.md)
- H90/x6 coboundary: [P27 Trace/Norm Dplus H90-X6 Coboundary Probe](p27_trace_norm_dplus_h90_x6_coboundary_20260622.md)
- Post-Dplus screen: [P27 Trace/Norm Post-Dplus Screen](p27_trace_norm_post_dplus_screen_20260621.md)
- Orientation screen: [P27 Trace/Norm Orientation Phase Screen](p27_trace_norm_orientation_phase_screen_20260622.md)
- GPU handoff: [P27 GPU Dplus-Native Source Handoff](p27_gpu_dplus_native_source_handoff_20260622.md)

```text
p27_trace_norm_dplus_h90_payload_screen_rows=1/1
```
