# Trace-Frame Selected-Tail Tensor-Factor Equivariance Boundary

Date: 2026-06-06

This note repeats the tensor-factor equivariance audit after the
selected-leading correction.  The old leading-minor check compared a fixed
full leading determinant across scalar-extension tensor factors.  The
corrected p24 surface is subtler: on a prefix chart it uses the selected-tail
determinant on the residual kernel

```text
K_2 -> selected coordinates in the next relative coefficient block.
```

The p24 compression theorem should therefore say:

```text
selected-tail determinant lines on scalar-extension tensor factors are
Frobenius transports of one another up to p-unit changes of trivialization.
```

It should not assert literal equality of the raw residual-tail determinants
computed from an ad hoc kernel basis.

## Audit

The audit script is:

```text
p24/trace_frame_selected_tail_tensor_factor_equivariance_audit.py
```

It checks compact CM rows where one packet factor splits after adjoining
`mu_m`.  For each scalar-extension tensor factor it computes:

```text
full leading determinant;
selected residual-tail determinant;
base norm of each determinant in the deterministic trivialization;
zero/nonzero status across tensor factors.
```

The tail determinant value is basis-dependent.  Its zero status is not.

## Pinned Rows

The `D=-10919, q=11243, h=156, m=12, n=13` axis row reports:

```text
subdegree=2:
  factors_covered=2/2
  full_zero_status_uniform=1
  tail_zero_status_uniform=1
  full_norm_equal=1
  tail_norm_equal=0
  selected_tail_transport_survives=1

subdegree=3:
  factors_covered=2/2
  full_zero_status_uniform=1
  tail_zero_status_uniform=1
  full_norm_equal=1
  tail_norm_equal=0
  selected_tail_transport_survives=1
```

The lower-rank projected targets on the same row also survive:

```text
target=constant_plus_4:
  selected_tail_transport_survives=1 for subdegree 2 and 3

target=constant_plus_3:
  selected_tail_transport_survives=1 for subdegree 2 and 3
```

Two compact rows from the leading-determinant equivariance note give the same
zero-status conclusion:

```text
D=-1559, q=2459, h=51, m=3, n=17:
  selected_tail_transport_survives=1 for subdegree 2 and 4

D=-2207, q=2243, h=39, m=3, n=13:
  selected_tail_transport_survives=1 for subdegree 2 and 3
```

2026-06-08 holdout refresh: a compact `axis` run with seed `20260610`,
`--max-cases 5 --max-h 180 --max-abs-D 40000 --max-n 180 --max-m 48
--q-stop 400000 --max-factor-degree 48 --max-extension-degree 10
--max-tensor-factor-degree 24`, returned `14` rows in `6` row-groups.  Every
group had uniform full and tail zero/nonzero status across the covered tensor
factors:

```text
D=-1559: subdegree 2 and 4 survived
D=-2207: subdegree 2 and 3 survived
D=-2591: subdegree 3 survived
D=-2687: subdegree 2 survived
```

In the proper residual-tail groups the tail norms again varied by tensor
factor, while zero status stayed uniform.  This reinforces the same boundary:
the p24 theorem should transport the selected determinant line up to p-units,
not assert equality of raw tail determinants in a chosen kernel basis.

In the one-full-block residual cases, tail norm equals full norm.  In the
proper partial-tail cases, tail norms often differ across the two tensor
factors even though the full determinant norms agree.

2026-06-08 component-target rerun: the pinned `D=-10919, m=12` row was rerun
with `axis`, `constant_plus_4`, and `constant_plus_3` together under seed
`20260611`.  It returned `12` rows in `6` row-groups.  Every group had:

```text
full_zero_status_uniform=1
tail_zero_status_uniform=1
selected_tail_transport_survives=1
full_norm_equal=1
```

The selected-tail raw norms differed across tensor factors in five of the six
groups; the only literal `tail_norm_equal=1` case was the one-block
`constant_plus_3, subdegree=3` row where tail equals the full determinant.
This is another direct warning that the p24 compression theorem must be
determinant-line p-unit transport, not equality of raw kernel-basis tail
determinants.

## Interpretation

This keeps the one-norm compression route alive, but it sharpens the theorem:

```text
Delta_tail(i') = u(i,i') * sigma(Delta_tail(i))
```

where `u(i,i')` is a p-unit on the selected-tail determinant line.

The audit specifically warns against the stronger false-looking statement:

```text
raw tail determinant norms are literally equal in every kernel-basis chart.
```

That equality is not stable in the proper residual-tail rows, and the failure
is expected: the prefix-kernel basis and selected-tail trivialization are part
of the determinant line.

## Certificate Consequence

If the determinant-line transport theorem is proved for the p24 selected-tail
line, then the 70 scalar-extension tensor factors reduce to one representative
p-unit target:

```text
one degree-8 selected-tail norm
  + tensor-factor p-unit transport
  => all 70 tensor-factor selected-tail norms are p-units.
```

Combined with the seven right-orbit crossed-product transport, this is the
cleanest currently visible path from the corrected selected-tail theorem to a
sub-sqrt payload.  It still requires the arithmetic producer:

```text
prove the representative selected-tail determinant-line norm is a p-unit at
the selected p24 ordinary CM prime.
```

## Commands

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_selected_tail_tensor_factor_equivariance_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --target axis --max-rows 40 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_selected_tail_tensor_factor_equivariance_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --target constant_plus_4 --target constant_plus_3 \
  --max-rows 80 --include-linear

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory \
  --include-selected-tail-tensor-factors
```
