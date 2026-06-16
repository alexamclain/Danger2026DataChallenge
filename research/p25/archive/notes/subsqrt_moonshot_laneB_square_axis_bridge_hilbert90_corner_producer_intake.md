# Lane B: Curved Hilbert-90 Corner Producer Intake

Date: 2026-06-14

Gate:
`research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py`

## Purpose

This is the theorem-facing intake for the smallest current square-axis bridge
producer target.  It composes four local facts:

```text
curved source-row Newton triangle
recorded half-bridge triangle edge
full order-25 K trace
raw D^3=Y relation
raw kernel trace shift D^3 - Y = (57,0)
primitive C_169 source motion
active C_169 projective lift (1,18,150)
quadratic C_13-to-C_169 fiber section
nonsplit C_169 carry transport
primitive unit-sign / branch row triangle
```

## Fixed Target

Canonical row triangle:

```text
q rows:      0, 172, 482
C_169 rows: 0, 3,   144
D rows:     0, 1,   386
```

Newton data:

```text
q newton      = (0, 172, 138)
C_169 newton  = (0, 3, 138)
D newton      = (0, 1, 384)
D edge images = (1 -> 172), (121 -> 25), (385 -> 310)
```

The K-invariant raw lift has support `75`; smaller order-`1` or order-`5`
K-subtraces are trace-correct but fail the raw K-boundary / `D^3=Y` relation.
The raw bridge factors also force a separate kernel trace and primitive
`C_169` motion:

```text
D^3 - Y_raw = (57,0)
D segment combined order = 12675
bridge edge combined order = 12675
sparse source-chain directions = 6
primitive C_169 direction rows = 6
right-order-3 gauge rows = 6
```

A cheap right-kernel gauge exists, but it does not remove the primitive
`C_169` Kummer cost.

The active quotient lift is also not just any primitive `C_169` lift:

```text
C_13 projective shadow = (1,2,10)
active C_169 lift      = (1,18,150)
inactive lifts         = 12
canonical fiber        = f(c0)=c0*(c0-3)
canonical row values   = (0,3,144)
canonical q values     = (0,172,482)
covariance rows        = 4
nonsplit carry needed  = 2
unit triangle rows     = 4
unit off-line rows     = (-1,-1)->1, (-1,1)->0, (1,-1)->0, (1,1)->2
unit off-line points   = (-1,-1)->(11,10), (-1,1)->(0,0),
                         (1,-1)->(0,0), (1,1)->(2,2)
```

So the candidate must realize the active nonsplit lift and the quadratic
fiber correction, not a Teichmuller lift, affine fiber gauge, or another
primitive lift with the same `C_13` shadow.  It must also transport the
quadratic fiber section with the actual nonsplit `C_169` carry law; split
`C_13 x C_13` no-carry transport fails on the two reversal rows.  Finally,
the primitive unit sign `eps` and branch coefficient `a` must force the
row-labeled triangle:

```text
cancel_row   = (3-eps)/2
neighbor_row = cancel_row-a
off_row      = cancel_row+a mod 3
off_line_x   = eps+a
```

A theorem cannot recover only roots or scalar data and then place the third
point passively in whichever source row fits.

## Candidate Classifier

```text
no_theorem_body:
  decision = reject_no_theorem_body

wrong_source_triangle:
  decision = reject_wrong_source_triangle

linearized_source_graph:
  decision = reject_linearized_source_graph

wrong_half_bridge_edge:
  decision = reject_wrong_half_bridge_edge

sparse_or_k5_subtrace:
  decision = reject_sparse_or_subtrace_k_lift

hidden_mode_relation_failure:
  decision = reject_raw_d3_y_relation_failure

raw_kernel_trace_omitted:
  decision = reject_raw_kernel_trace_omitted

c13_shadow_or_right_kernel_only:
  decision = reject_c13_shadow_or_right_kernel_only

generic_primitive_c169_lift:
  decision = reject_generic_primitive_c169_lift

teichmuller_or_affine_fiber_shortcut:
  decision = reject_teichmuller_or_affine_fiber_shortcut

split_no_carry_fiber_transport:
  decision = reject_split_no_carry_fiber_transport

passive_or_wrong_unit_triangle:
  decision = reject_passive_or_wrong_unit_triangle

curved_triangle_helper_only:
  decision = helper_only_curved_triangle_value_theorem_missing

curved_triangle_value_no_period156:
  decision = conditional_missing_period156_context

curved_triangle_period156_no_source:
  decision = conditional_finite_payload_without_source_theorem

curved_triangle_source_no_framing:
  decision = source_theorem_closed_policy_or_framing_missing

danger3_framed_no_same_j:
  decision = danger3_unblocked_cross_level_bridge_missing

same_j_bridge_no_x16:
  decision = cross_level_target_identified_specialization_missing

x16_surface_no_x0:
  decision = x16_surface_reached_halving_or_vpp_missing

concrete_A_x0_no_vpp:
  decision = extraction_ready_vpp_missing

official_vpp_verified:
  decision = submission_ready
```

## Counts

```text
row_count              = 21
rejected_rows          = 12
helper_only_rows       = 1
conditional_rows       = 2
finite_shape_rows      = 9
finite_value_rows      = 8
source_closing_rows    = 6
danger3_unblocked_rows = 5
cross_level_bridge_rows= 4
x16_surface_rows       = 3
extraction_ready_rows  = 2
submission_ready_rows  = 1
```

## Interpretation

The next producer theorem cannot merely mention a sparse quotient corner, a
line/AP, a generic one-cancellation edge, or a K-subtrace.  The accepted finite
shape is the curved Newton row triangle with the recorded half-bridge edge and
the full order-`25` K trace satisfying raw `D^3=Y`.  It must also account for
the raw kernel trace shift and the primitive `C_169` source motion; a
`C_13` shadow or cheap right-kernel gauge is not enough.  It must also select
the active projective lift `(1,18,150)` and the quadratic fiber law
`f(c0)=c0*(c0-3)`, transported with the nonsplit `C_169` carry law.  The
primitive unit sign and branch coefficient must also force the source-row
triangle, so passive third-point placement is rejected before the finite
value theorem boundary.

Even that finite shape is only a helper until it comes with a finite
value/divisor theorem, period-`156` context, arithmetic source proof,
DANGER3 framing, same-`j` bridge, X_1(16) extraction, concrete `x0`, and
official `vpp.py` verification.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_hilbert90_corner_producer_intake_gate.py
```

Marker:

```text
square_axis_bridge_hilbert90_corner_producer_intake_rows=1/1
```
