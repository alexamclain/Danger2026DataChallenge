# Actual-CM Adjacent-Anchor Boundary

Date: 2026-06-07

## Point

The adjacent-anchor descent theorem should not be treated as a generic CM
period fact.  On the small actual-CM row

```text
D=-6719, q=6863, h=105, m=21=3*7, n=5,
```

`rho=q^2` fixes the left component and shifts the right quotient by `2` modulo
the order-3 quotient.  The internal relative trace has two cosets.

For the adjacent differences of the internally traced H-coset rows:

```text
T_i = Y_{i+1} - Y_i,
```

the formal covariance and telescope identities hold, but the anchor
`T_0` is not rho-fixed in either relative trace coset.

## Checked Boundary

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_actual_cm_adjacent_anchor_boundary.py
```

Key markers:

```text
adjacent_difference_covariance_failures=0
adjacent_difference_telescope_zero=2/2
adjacent_anchor_descended=0/2
adjacent_anchor_nonzero=2/2
adjacent_differences_all_zero=0/2
covariance_telescope_do_not_force_adjacent_anchor_in_actual_cm=1
actual_cm_adjacent_anchor_descent_not_generic=1
p24_needs_specific_trace_gcd_adjacent_packet=1
```

## Consequence

The live p24 theorem must prove rho-fixedness of the selected trace-GCD
adjacent packet.  Ordinary actual-CM covariance plus telescoping is not enough.
