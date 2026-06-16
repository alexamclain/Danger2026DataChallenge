# p24 Right-Difference Covariance-Telescope Gate

Date: 2026-06-07

## Point

The adjacent right-difference trace target has one extra formal structure:
the seven adjacent differences telescope.

Let

```text
T_i = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n))
```

for the seven adjacent right-difference polynomials `P_i`.  Since

```text
sum_i P_i = 0,
```

we have

```text
sum_i T_i = 0.
```

The p24 `rho=p^780` action shifts the right `H=<2^7>` quotient by `6 mod 7`.
Thus the exact finite sufficient theorem is:

```text
T_{i+6} = rho(T_i)      for all i
rho(T_0) = T_0
sum_i T_i = 0
----------------------
T_i = 0                for all i.
```

The proof is short: covariance plus the descended anchor makes all seven
`T_i` equal; the telescoping sum then gives `7*T_0=0`, and `7` is invertible
modulo `p`.

## Why This Helps

This avoids constructing a huge additive Hilbert-90 potential for the
`<p>`-trace of order `388430`.  The proof target is now two small arithmetic
inputs:

```text
1. covariance of the seven adjacent trace values under rho;
2. one anchor descent/fixedness statement.
```

The third input, telescoping, is formal from the definition of adjacent
differences.

## Guardrails

The finite gate checks the negative controls:

```text
covariance + telescoping alone can be nonzero;
descent + telescoping alone can be nonzero;
covariance + descent only gives equal values until telescoping is used.
```

So the theorem is not being smuggled in by one condition.  All three pieces
matter.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_right_difference_covariance_telescope_gate.py
```

Key markers:

```text
p24_rho_right_shift_mod7=6
positive_covariance_failures=0
positive_sum_zero=96/96
positive_all_equal=96/96
positive_all_zero=96/96
covariance_plus_telescope_nonzero=96/96
covariance_plus_telescope_anchor_not_descended=96/96
descent_plus_telescope_nonzero=96/96
descent_plus_telescope_covariance_fails=96/96
covariance_plus_descent_without_telescope_nonzero_equal=96/96
covariance_plus_anchor_descent_plus_telescope_forces_trace_zero=1
```

## Updated Proof Target

For the seven adjacent right-difference trace values

```text
T_i = Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n)),
```

prove the arithmetic covariance and anchor descent:

```text
T_{i+6} = rho(T_i),
rho(T_0) = T_0.
```

Then `T_i=0` follows formally from telescoping.  This is currently the
smallest proof target for the `48` compressed equations.
