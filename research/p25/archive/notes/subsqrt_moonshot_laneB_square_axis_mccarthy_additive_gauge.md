# Subsqrt Moonshot Lane B McCarthy Additive Gauge

Date: 2026-06-13

## Result

The powered McCarthy target is stable under representative additive-character
gauge changes.

In the numeric McCarthy gates, Gauss sums are evaluated in `F_20574061` using
an auxiliary additive character.  Replacing:

```text
psi(x) -> psi(u*x)
```

for `u in F_2029^*` changes Gauss sums by the standard law:

```text
g_u(A) = conjugate(A)(u) * g_1(A)
```

The gate checks this transform law for all `2028` character exponents for the
representative gauges:

```text
u = 1, 2, 13, -1
```

It then evaluates the McCarthy quotient on the h=2 seed row:

```text
q = 129, 138, 147
```

For every checked gauge:

```text
R(129) = 1
R(138) = 1790844
R(147) = 1
R(138)^2029 = 12801419 = zeta_39^5
ord(R(138)) = 79131
ord(R(138)^2029) = 39
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_additive_gauge_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_additive_gauge_gate.py
```

Observed:

```text
all_gauss_transforms_ok = True
target_ratio_gauge_stable = True
target_projection_gauge_stable = True
off_target_ratios_stay_one = True
additive_gauge_not_obstruction = True
square_axis_mccarthy_additive_gauge_rows=1/1
```

## Consequence

The powered McCarthy target is not an artifact of the chosen auxiliary
additive character.

This strengthens the theorem target:

```text
produce a multiplicative unit quotient R(q)
project by q-power to kill the additive-root component
normalize by the determined transported coefficient
close raw-Y
```

The remaining debt is still:

```text
justify the multiplicative unit quotient and q-power projection as arithmetic
producer operations before raw lift.
```

Discard condition:

```text
candidate works only for one additive-character gauge
candidate depends on changing the off-target ratios away from 1
candidate violates the Gauss transform law for g_u(A)
```
