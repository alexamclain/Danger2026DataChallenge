# Subsqrt Moonshot Lane B McCarthy Power Descent

Date: 2026-06-13

## Result

The sparse McCarthy quotient can be made character-valued by a natural power
descent.

From the unit-quotient gate:

```text
R(q) = LHS(q) / main_sum(q)
support(R(q)-1) = (138,)
ord(R(138)) = 39 * 2029
```

Since `R(q)=1` off the anomaly, taking powers preserves singleton support
unless the exceptional value becomes `1`.

The useful descent is:

```text
support(R(q)^2029 - 1) = (138,)
R(138)^2029 = zeta_39^5
ord(R(138)^2029) = 39
outer S image = (138,310,482)
```

Controls:

```text
R(138)^39 has order 2029
R(q)^39 - 1 is still supported at (138,), but keeps the additive component
R(q)^(39*2029) - 1 is zero everywhere
R(138)^2029 - 1 has full auxiliary-field order 20574060
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_power_descent_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_descent_gate.py
```

Observed:

```text
additive_power_support = (138,)
additive_power_target_value = 12801419
additive_power_target_order = 39
additive_power_zeta39_exponent = 5
additive_power_minus_one_order = 20574060
power_descent_preserves_singleton = True
power_descent_character_valued = True
square_axis_mccarthy_power_descent_rows=1/1
```

## Consequence

This is now the sharpest McCarthy/Barnes-side positive artifact:

```text
theorem-level quotient:
  R(q)-1 supported at q=138

power descent:
  R(q)^2029 character-valued
  R(138)^2029 = zeta_39^5

p25 payload:
  q=138 -> S image (138,310,482)
  existing raw-Y closure already passes
```

The remaining debt is no longer the additive-root component itself; it can be
killed by power descent.  The remaining debt is:

```text
justify/cost the 2029th power before raw lift
avoid arbitrary scalar normalization of zeta_39^5 - 1
connect the powered quotient to the p25 raw-Y coefficient field
preserve the explicit S trace and kernel-trivial raw lift
```

Continue condition:

```text
candidate explains R^2029 as a legitimate powered unit quotient or gives an
equivalent order-39 quotient directly
```

Discard condition:

```text
candidate needs R^39 or another branch that leaves additive order 2029
candidate normalizes zeta_39^5 - 1 by an arbitrary auxiliary-field scalar
candidate loses singleton support before the S trace/raw-Y lift
```
