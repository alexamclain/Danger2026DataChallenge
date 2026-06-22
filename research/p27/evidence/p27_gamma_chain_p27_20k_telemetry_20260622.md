# P27 Gamma-Chain 20k Telemetry

Date: 2026-06-22

## Claim

The repeated A/B/K gamma-transition shape is real enough to keep as a CAS
class-comparison target, but a larger p27 sample does not promote it to a GPU
production source.

On `20k + 20k` p27 train/heldout samples, the selected gamma products remain
near ordinary half-gates, and the V4 phase links stay near `1/2`.  Late-gate
skews are not stable enough to treat as a source-normalized win.

## Probe

Probe:

```text
research/p27/archive/gates/p27_b_line_alpha_beta_phase_sequence_probe.py
```

Output:

```text
research/p27/archive/probe_outputs/p27_b_line_alpha_beta_phase_sequence_probe_p27_20k_20260622.txt
```

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=research/p27/archive/gates \
python3 -u research/p27/archive/gates/p27_b_line_alpha_beta_phase_sequence_probe.py \
  --small-primes '' \
  --p27-target 20000 \
  --p27-heldout-target 20000 \
  --seed 20260623 \
  --heldout-seed 20260624 \
  --max-draws 6000000 \
  --max-gate 10 \
  | tee research/p27/archive/probe_outputs/p27_b_line_alpha_beta_phase_sequence_probe_p27_20k_20260622.txt
```

## Sample Size

```text
train:
  sample_rows = 20000
  sample_x_draws = 158338
  unique_A_x5_B = 20000
  phase_records = 143372
  phase_links = 123128

heldout:
  sample_rows = 20000
  sample_x_draws = 159424
  unique_A_x5_B = 20000
  phase_records = 140176
  phase_links = 120064
```

## Gate Product Rates

The selected product `alpha_j*beta_j` is the gamma-class gate bit on the
materialized path.

```text
gate   train plus-rate   heldout plus-rate
3      0.499703          0.493635
4      0.500197          0.497582
5      0.489328          0.498785
6      0.526655          0.498376
7      0.509202          0.524429
8      0.487951          0.496894
9      0.530864          0.475000
```

This is not a compounding source shrink.  The late train/heldout deviations
move around and should be read as sampling/tail noise unless a named class
explains them.

## Phase-Link Rates

The pre-registered V4 link products remain near half.

```text
train aa/ab/ba/bb plus-rate ranges:
  gate3->4: 0.495353 / 0.506030 / 0.495353 / 0.506030
  gate4->5: 0.495553 / 0.501482 / 0.495553 / 0.501482
  gate5->6: 0.495254 / 0.502120 / 0.495254 / 0.502120
  gate6->7: 0.496069 / 0.497220 / 0.496069 / 0.497220
  gate7->8: 0.500000 / 0.497176 / 0.500000 / 0.497176
  gate8->9: 0.495659 / 0.496431 / 0.495659 / 0.496431

heldout aa/ab/ba/bb plus-rate ranges:
  gate3->4: 0.498186 / 0.502215 / 0.498186 / 0.502215
  gate4->5: 0.499898 / 0.507186 / 0.499898 / 0.507186
  gate5->6: 0.505073 / 0.493709 / 0.505073 / 0.493709
  gate6->7: 0.497455 / 0.503766 / 0.497455 / 0.503766
  gate7->8: 0.507278 / 0.500679 / 0.507278 / 0.500679
  gate8->9: 0.501367 / 0.500000 / 0.501367 / 0.500000
```

None of these clears a source-normalized promotion bar.  The state-conditioned
next-plus rates also wobble around half, with no stable heldout recurrence.

## Interpretation

Positive:

```text
The p27 path telemetry is now large enough to reject tiny 3k-sample mirages.
The gamma/V4 coordinates remain well-instrumented for a future GPU telemetry column.
The finite-field f4/f5 recurrence-shaped result is not contradicted by p27 data.
```

Negative:

```text
No immediate raw-source shrink appears on p27.
No alpha/beta phase word or state link is promoted.
The repeated gamma-transition shape is not a production sampler without CAS.
```

## Consequence

The current first-class test remains offline normalized class comparison:

```text
compare gamma_4^2 = V+2 over F_A(U,V)=0
against gamma_5^2 = W+2 over F_A(V,W)=0
on the selected components
```

GPU should only run bounded telemetry that emits these named coordinates with
raw-source denominators, or a direct sampler after CAS names a quotient,
coboundary, or recurrence.

GPU-scale follow-up:
[P27 GPU Recurrence-Coupling Telemetry](p27_gpu_recurrence_coupling_20260622.md).
An A40 run over `200M + 200M` raw source draws validates the formulas with
zero mismatches through gates `3..16`, but no heldout sign-word bucket clears
the promotion bar.  The largest all-plus residual lift is only `1.028x` at
gates `3..12` and `1.053x` in the gate-16 stretch, versus the `1.25x` bar.
This cleanly kills production GPU from the current gamma/sign-word buckets.

## Continue / Kill

```text
continue = CAS compare repeated gamma classes gamma_4 and gamma_5
continue = use GPU only for bounded named-coordinate telemetry
continue = keep Dplus fused/native pricing as the separate practical GPU ask

kill = large GPU production from gamma/phase buckets
kill = alpha/beta phase-word source claims after 20k train/heldout
kill = reading late train-only skews as recurrence evidence
```

## Linked Artifacts

- [P27 A/B/K F4/F5 Transition Count](p27_abk_f4_f5_transition_count_20260622.md)
- [P27 A/B/K F3/F4 Chart Count](p27_abk_f3_f4_chart_count_20260622.md)
- [P27 B-Line Alpha/Beta Phase Sequence Screen](p27_b_line_alpha_beta_phase_sequence_20260622.md)
- [P27 B-Line Phase-Word Source Screen](p27_b_line_phase_word_source_screen_20260622.md)

```text
p27_gamma_chain_p27_20k_telemetry_rows=1/1
```
