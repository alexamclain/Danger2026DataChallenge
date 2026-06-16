# Subsqrt Moonshot Lane B McCarthy Numeric Delta Raw-Y Bridge

Date: 2026-06-13

## Result

The numeric McCarthy point-delta now lands on the existing p25 square-axis
payload closure.

The chain checked is:

```text
McCarthy Theorem 1.7 over F_2029
  support_qexp(LHS - main_sum) = (138,)
  exceptional_support = (138,)

outer S image:
  (138,) -> (138,310,482)

GK/Frobenius projector anomaly terms:
  (138,310,482)

formal raw-Y closure:
  raw_y_length = 12675
  raw_y_nonzero = 6300
  ray_local_harness_ok = True
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py
```

Observed:

```text
mccarthy_support = (138,)
mccarthy_exceptional_support = (138,)
outer_s_image = (138,310,482)
frobenius_projected_anomaly_terms = (138,310,482)
raw_y_harness_ok = True
square_axis_mccarthy_numeric_delta_raw_y_bridge_rows=1/1
```

## Consequence

This is now the cleanest Jacobi-side positive artifact:

```text
arithmetic theorem-level point delta
  -> exact p25 anomaly orbit
  -> existing finite raw-Y payload closure
```

The remaining gap is no longer support geometry.  It is parameter
normalization and raw arithmetic realization:

```text
choose McCarthy parameters as an actual p25 Jacobi/Barnes unit phase
align the normalization with the theta_3_1/raw-Y packet
avoid dense scalar background
preserve kernel-trivial raw lift and raw D^3=Y relation
```

Discard condition:

```text
the required McCarthy normalization cannot be represented by the p25 local
source characters or introduces a dense scalar correction before raw-Y lift
```
