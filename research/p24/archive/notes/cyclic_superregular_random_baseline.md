# Cyclic Superregular Random Baseline

This note tests whether the coefficient-minor route is showing special CM
structure or mostly generic finite-field behavior.

## Question

For the axis subspace `V` inside a packet algebra `F_q[X]/(f)`, the
origin-independent leading-minor condition is:

```text
det(P_0 X^(-beta) V) != 0
```

for all relevant `beta`, where `P_0` projects to the first `dim(W_axis)`
packet coordinates.  This is the cyclic consecutive-Pluecker /
superregularity formulation from:

```text
p24/axis_minor_origin_action_boundary.md
```

For a random `r`-dimensional subspace of a `d`-dimensional packet over `F_q`,
one fixed `r x r` projected minor should vanish with probability about `1/q`.
For `n` beta shifts, the union-bound heuristic is about:

```text
n/q.
```

## Audit

I added:

```text
p24/cyclic_superregular_random_baseline.py
```

It compares the actual CM axis subspace with random full-rank subspaces in the
same packet field.

Targeted row:

```text
D=-8711, q=8747, h=132, m=12=4*3, n=11
factor_degree=10, axis_dim=6
```

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/cyclic_superregular_random_baseline.py \
  --only-D -8711 --random-trials 5000 \
  --max-cases 1 --max-h 200 --max-abs-D 10000 \
  --max-prime-quotients 12 --max-composite-quotients 30 \
  --min-n 3 --max-n 80 --q-stop 400000 \
  --max-splitting-primes 1 --max-axis-dim 12 \
  --max-factor-degree 20 --include-linear --require-composite-m
```

reported:

```text
cm_axis:
  beta_tests=11
  beta_zero_count=0
  beta_distinct_values=11

random_baseline:
  subspaces_with_any_beta_zero=4
  beta_zero_total=4
  empirical_failure_rate=0.000800
  empirical_zero_rate_per_beta=0.000073
  heuristic_any_failure_n_over_q=0.001258
```

The random failure rate is small and close to the naive `n/q` scale.

## Consequence

Small-data success of the cyclic leading-minor condition is not proof-like:
random subspaces usually pass at these field sizes.  For p24 the random
heuristic is even more extreme:

```text
n/p ~= 3.1e6 / 1e24 ~= 3e-18
```

per packet, so a random model would predict the leading-minor certificate to
hold almost certainly.

That is useful intuition, but not a certificate.  The missing theorem remains
a selected-prime CM arithmetic statement:

```text
the actual CM axis subspace avoids the cyclic consecutive-minor divisor
modulo the selected p24 prime.
```

Equivalently, for each packet `a`, the coefficient-minor route should prove
the p-unit status of the sliding-window product

```text
Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a),
```

or at least the one beta/window attached to a constructible embedded origin.
This product is the coefficient-minor analogue of `Delta_axis`, but it is
coordinate-dependent and not presently tied to a class-field norm formula.

The coefficient-minor route is therefore a concrete finite certificate shape,
not yet an asymptotic proof.
