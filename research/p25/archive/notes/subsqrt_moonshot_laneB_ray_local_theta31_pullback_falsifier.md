# Subsqrt Moonshot Lane B Ray-Local Theta31 Pullback Falsifier

Date: 2026-06-12

## Result

The p25 Lane B producer contract is now packaged as a single executable
candidate harness.

With no arguments, the harness runs the synthetic canonical control on the
first real negative-trace local source:

```text
right source: inert 151
C source:     split 677
quotient:     C_3 x C_13
B:            325
raw order:    12675
```

It accepts a future producer candidate as a raw vector:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py \
  --raw-y path/to/raw_y_values.txt
```

The file must contain `12675` integers.  Values are interpreted modulo the
selected case's quotient field.  The case can be selected explicitly:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py \
  --case square_axis_C3xC169 \
  --raw-y path/to/raw_y_values.txt
```

Supported synthetic controls:

```text
tiny_C3xC13
prime_axis_C3xC53
square_axis_C3xC169
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py
```

Default command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py
```

Observed synthetic control:

```text
source_coordinate_hits = 12675 / 12675
block_constancy_hits = 39 / 39
residue_rectangle_constancy_hits = 39 / 39
quotient_scale_hits = 39 / 39
zero_rectangle_hits = 21 / 21
carrying_rectangle_hits = 18 / 18
raw_carry_one_positions = 5850 / 5850
zone_carry_rectangles = {'zero': 0, 'one_hot': 3, 'two_hot': 6, 'all_rows': 9}
eigen_rank = 2
eigen_conjugacy = 1
eigen_support = (4, 9, 6)
C_13 Fourier support = 12 / 12
selected_defect_ok = 1
raw_product_ok = 1
kummer_degree_13 = 1
ray_local_theta31_pullback_rows = 1 / 1
```

Square-axis synthetic control:

```text
case = square_axis_C3xC169
source_coordinate_hits = 12675 / 12675
block_constancy_hits = 507 / 507
residue_rectangle_constancy_hits = 507 / 507
quotient_scale_hits = 507 / 507
zero_rectangle_hits = 255 / 255
carrying_rectangle_hits = 252 / 252
raw_carry_one_positions = 6300 / 6300
zone_carry_rectangles = {'zero': 0, 'one_hot': 42, 'two_hot': 84, 'all_rows': 126}
eigen_rank = 2
eigen_conjugacy = 1
eigen_support = (43, 126, 84)
C_169 Fourier support = 168 / 168
expected_kummer_degree = 13
kummer_descent_ok = 1
square_axis_boundary_residual:
  square_prediction_hits = 507 / 507
  residual_prediction_hits = 507 / 507
  residual_ones = 18 / 18
  residual_by_row = [6, 6, 6]
  residual_by_h = [3, 6, 9]
  residual_by_fiber = [0, 0, 0, 9, 0, 0, 6, 0, 0, 3, 0, 0, 0]
  boundary_positive_hits = 18 / 18
  boundary_zero_hits = 21 / 21
  nonboundary_zero_hits = 468 / 468
  residual_trace_hits = 39 / 39
  observed_q_count = 18 / 18
  observed_q_set_match = 1
  quotient_shift_set_match = 1
  quotient_shift_hits = 18 / 18
  quotient_shift_layers = [6, 6, 6]
  quotient_shift_h_counts = [3, 6, 9]
  quotient_shift_t_counts = [9, 6, 3]
  digit_rule_hits = 18 / 18
  no_borrow_hits = 18 / 18
  observed_residual_qs = [43, 86, 95, 129, 138, 147, 215, 258, 267,
                          301, 310, 319, 387, 430, 439, 473, 482, 491]
  quotient_shift_qs = [43, 86, 95, 129, 138, 147, 215, 258, 267,
                       301, 310, 319, 387, 430, 439, 473, 482, 491]
ray_local_theta31_pullback_rows = 1 / 1
```

## Consequence

This is the practical falsifier for proposed ray-local CM-Artin or modular-unit
pullbacks.  A candidate must satisfy all of the following before any global
certificate work is worth doing:

```text
embed on the actual inert-151 x split-677 local source;
be constant on all B=325 blocks / 25 x 13 residue rectangles;
trace to canonical theta_{3,1} up to one global nonzero scale;
select exactly the 18 carrying quotient rectangles and 5850 raw carry-one positions;
have rank-2 right-character payload;
obey E2 = -<-1>E1;
support the C-axis vector exactly on slots 4..9;
use every nontrivial C_13 Fourier character;
satisfy the selected-defect and raw product-formula checks;
keep the degree-13 Kummer anchor as an explicit obligation.
```

For the square-axis route, the same harness checks the larger `507`-rectangle
half-arc while retaining the measured degree-`13` Kummer anchor obligation.  It
also now reports the base-plus-boundary residual diagnostic from:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_boundary_residual.md
```

and the producer-facing graph/digit/no-borrow/quotient-shift diagnostics from:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_local_graph_residue.md
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_digit_selector.md
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_no_borrow_digit.md
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_quotient_shift_normal_form.md
```

This rules out producer attempts that only match a relabeled quotient, separate
the `151` and `677` local units, land on a rank-one or anti-invariant right
payload, use low-frequency C-axis data, assume an affine quotient compression,
miss the square-axis boundary residual trace-down, miss the triangular `q`
classes, miss the base-`43` no-borrow digit rule, fail the `D=(1,1)`,
`X=(1,127)`, `Y=(0,3)`, `D^3=Y` quotient-shift law, or silently absorb the
anchor by a sign/base-field shortcut.

The first checked producer-shadow obstruction is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_jacobi_log_shadow_obstruction.md
```

It rules out the naive strategy of taking discrete logs of the raw or
single-anchor-corrected Hasse-Davenport Jacobi packet, even after row-plus-column
normalization.
