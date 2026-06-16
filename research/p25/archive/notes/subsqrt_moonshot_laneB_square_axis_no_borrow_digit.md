# Subsqrt Moonshot Lane B Square-Axis No-Borrow Digit Gate

Date: 2026-06-12

## Result

The square-axis digit selector is a tiny base-`3` no-borrow predicate.

Write:

```text
q = 43*m + 9*t
m = 4*s + h + 1
h,t in {0,1,2}
```

Then the selector is:

```text
selected(h,t) = 1 - floor((t + 2 - h) / 3)
```

Equivalently, it is `1` exactly when subtracting `t` from `h` has no borrow:

```text
t <= h
```

The matrices are:

```text
selector = [[1, 0, 0],
            [1, 1, 0],
            [1, 1, 1]]

borrow   = [[0, 1, 1],
            [0, 0, 1],
            [0, 0, 0]]
```

Observed:

```text
no_borrow_hits = 9 / 9
q_count = 18 / 18
selector_rank_f2 = 3
selector_rank_odd = 3
borrow_rank_f2 = 2
borrow_rank_odd = 2
mixed_second_differences = [1, 0, 1, 1]
total_degree_min = 4
bidegree_min = (2, 2)
```

The exact polynomial normal form on `h,t in {0,1,2}` is:

```text
1
- 3/2 * t
+ 1/2 * t^2
+ 13/4 * h*t
- 7/4 * h*t^2
- 5/4 * h^2*t
+ 3/4 * h^2*t^2
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_no_borrow_digit_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_no_borrow_digit_gate.py
```

Observed:

```text
square_axis_no_borrow_digit_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_no_borrow_digit_gate
```

## Consequence

The square-axis residual selector is now back in the same language as the
original carry problem:

```text
make a tiny no-borrow bit in the digit variables
```

This is a positive structural simplification.  But the obstruction is also
sharp: the selector is rank `3`, has mixed finite differences, and requires
total degree `4` / bidegree `(2,2)` as a polynomial in the digit variables.
So a producer cannot be only a linear digit filter, row-plus-column selector,
or proper congruence projection.

The next arithmetic target is to realize this no-borrow bit from a ray-local
CM-Artin or modular-unit construction while preserving the measured degree-`13`
Kummer obligation.

The corresponding short group-ring word, including the rectangle-minus-borrow
normal form, is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_group_ring_normal_form.md
```
