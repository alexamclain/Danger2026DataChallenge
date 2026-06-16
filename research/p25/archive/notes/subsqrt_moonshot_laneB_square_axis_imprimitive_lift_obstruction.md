# Subsqrt Moonshot Lane B Square-Axis Imprimitive-Lift Obstruction

Date: 2026-06-12

## Result

The `C_3 x C_169` square-axis target is not just a lifted `C_3 x C_13`
producer.

The square-axis mask has a useful `C_13` trace shadow:

```text
sum over each C_169 residue class mod 13 = 6 + C_13 half-arc bit
trace_down_C13_shadow_hits = 39 / 39
```

But it is not a pullback from `C_13`:

```text
period_13_hits = 313 / 507
period_13_failures = 194
constant_residue_classes = 0 / 39
```

Every residue class modulo `13` is mixed, so no row/residue fiber is constant.

The character support confirms the same thing:

```text
scalar_support = 1 / 1
pure_lift_support = 12 / 12
pure_nonlift_support = 156 / 156
mixed_lift_support = 24 / 24
mixed_nonlift_support = 312 / 312
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_imprimitive_lift_obstruction_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_imprimitive_lift_obstruction_gate.py
```

Observed:

```text
square_axis_imprimitive_lift_obstruction_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_imprimitive_lift_obstruction_gate
```

## Consequence

This clarifies the square-axis opportunity:

```text
C_169 keeps a C_13 trace shadow;
the anchor descent still costs only degree 13;
but the half-arc itself needs a genuine 13-adic refinement.
```

So a square-axis producer cannot be just:

```text
a C_13 producer inflated along C_169 -> C_13;
a function constant on residue classes modulo 13;
a Fourier payload supported only on characters lifted from C_13.
```

The live `C_169` question is sharper now: can a ray-local CM-Artin or
modular-unit object produce the primitive/non-lifted `13^2` refinement while
retaining the easy degree-`13` anchor descent?

The positive fiber-alphabet refinement is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_fiber_alphabet.md
```

It records that the non-lifted square-axis refinement uses only six length-13
fiber words, with fiber weight equal to `6` plus the `C_13` trace-shadow bit.
