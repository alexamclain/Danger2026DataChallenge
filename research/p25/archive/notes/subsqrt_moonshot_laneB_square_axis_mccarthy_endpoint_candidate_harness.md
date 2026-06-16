# p25 Lane B: McCarthy Endpoint Candidate Harness

Updated: 2026-06-13 13:08 PDT

## Purpose

The live Barnes/McCarthy target has been reduced to a sparse endpoint object on
`C_507`.  A theorem, hand calculation, or literature scout can now emit sparse
`q coeff` pairs in either of two equivalent forms:

```text
projector form:        e_138
unit-minus-one form:   U - 1 = (zeta_39^5 - 1) * e_138
```

The harness coalesces those pairs modulo `C_507`, checks the exact endpoint
shape over `F_2029`, and confirms that the accepted endpoint inherits the
already verified normalized raw-Y transport closure.

## Acceptance Shape

```text
coefficient field = F_2029
target_q_exp = 138
zeta_39^5 - 1 = 1375
(zeta_39^5 - 1)^-1 = 636
support(e_138) = 1
support(U - 1) = 1
order(U) = 39
DFT support(e_138) = 507
DFT support(U - 1) = 507
raw-Y transport closes = true
```

## Local Gate

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py
```

Positive-control candidate modes:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py \
  --sparse-projector <(printf '138 1\n')

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_endpoint_candidate_harness.py \
  --sparse-unit-minus-one <(printf '138 1375\n')
```

Observed:

```text
square_axis_mccarthy_endpoint_candidate_harness_rows=1/1
square_axis_mccarthy_endpoint_candidate_harness_candidate_rows=1/1
```

## Interpretation

This lowers the friction for theorem-first literature hits.  A scout no longer
needs to hand-build the raw `C_12675` object; it can emit the endpoint
projector or unit correction, and the harness will decide whether it is the
exact p25 object that the raw-Y gates accept.

Passing this harness is not an arithmetic producer proof.  It verifies only
that the proposed endpoint has the correct finite shape and raw-Y consequence.
