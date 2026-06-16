# Subsqrt Moonshot Lane B McCarthy Normalization Density

Date: 2026-06-13

## Result

The McCarthy point-delta has positive p25 parameter alignment, but it is not a
standalone sparse local unit vector.

The p25 square-axis seed coordinate is:

```text
q = 43*(h+1) + 9*t mod 507
```

On the `3 x 3` seed grid:

```text
q = 138 selects exactly (h,t) = (2,1)
q = 138 mod 3 selects the whole h=2 row
q = 138 mod 169 selects exactly (2,1) on the seed grid
```

The outer `S` layer is:

```text
138 -> (138,310,482)
mod 169 values = (138,141,144)
```

so the full anomaly orbit still requires an explicit `S` trace; it is not one
single `C_169` delta.

The actual McCarthy theorem evaluation over `F_2029` gives:

```text
LHS support count = 507
main_sum support count = 507
LHS Fourier support count = 507
main_sum Fourier support count = 507

support(LHS - main_sum) = (138,)
exceptional_support = (138,)
exceptional_value_at_target = 2028
```

After scaling the singleton coefficient to `1`, its degree is `1`.  Forcing
degree zero by scalar balance adds:

```text
-1/507 = 40580 in F_20574061
```

to every `q_exp`, giving support `507/507`.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_normalization_density_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_normalization_density_gate.py
```

Observed:

```text
exact_seed_delta_cells = ((2,1),)
order3_shadow_cells = ((2,0),(2,1),(2,2))
outer_s_image = (138,310,482)
outer_s_is_single_order169_delta = False
sides_are_coordinate_dense = True
sides_are_fourier_dense = True
point_delta_requires_theorem_cancellation = True
scalar_balancing_is_dense = True
square_axis_mccarthy_normalization_density_rows=1/1
```

## Consequence

This refines the McCarthy/Barnes moonshot:

```text
positive:
  McCarthy parameters align exactly with the p25 anomaly seed.

negative:
  the singleton is produced by theorem-level cancellation of two dense
  hypergeometric packets.
  scalar-balancing the normalized delta alone is dense.
  the S layer is an additional trace, not hidden inside one C_169 delta.
```

The lane remains live, but only in a stricter form.  A certificate-shaped
producer must realize the McCarthy transformed difference, or an equivalent
unit identity, before raw lift.  It is not enough to use one McCarthy
hypergeometric value as the p25 raw unit vector.

Discard condition:

```text
candidate only supplies LHS or main_sum separately
candidate repairs degree by dense scalar background
candidate omits the explicit S trace needed for (138,310,482)
```
