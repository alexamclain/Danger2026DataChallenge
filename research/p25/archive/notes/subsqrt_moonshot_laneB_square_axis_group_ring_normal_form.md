# Subsqrt Moonshot Lane B Square-Axis Group-Ring Normal Form

Date: 2026-06-12

## Result

The square-axis residual comb has a short group-ring normal form in
`Z[C_507]`.

Let:

```text
S = 1 + x^172 + x^344
X = x^43
Y = x^9
```

Then the `18` residual classes are exactly:

```text
S * (X + X^2 + X^2Y + X^3 + X^3Y + X^3Y^2)
```

Equivalently, this is a rectangle minus a borrow corner:

```text
S*(X + X^2 + X^3)*(1 + Y + Y^2)
-
S*(XY + XY^2 + X^2Y^2)
```

Observed:

```text
S_terms = [0, 172, 344]
seed_terms = [43, 86, 95, 129, 138, 147]
rectangle_seed_terms = [43, 52, 61, 86, 95, 104, 129, 138, 147]
borrow_seed_terms = [52, 61, 104]
product_count = 18 / 18
rectangle_count = 27 / 27
borrow_count = 9 / 9
collision_free = 1
subtraction_ok = 1
```

The residual product is:

```text
[43, 86, 95, 129, 138, 147,
 215, 258, 267, 301, 310, 319,
 387, 430, 439, 473, 482, 491]
```

The borrow corner is:

```text
[52, 61, 104, 224, 233, 276, 396, 405, 448]
```

Fourier zero profiles over the `507`-cycle:

```text
S:                zero_count = 2, zeros = [169, 338]
seed:             zero_count = 0
rectangle_seed:   zero_count = 2, zeros = [169, 338]
borrow_seed:      zero_count = 0
residual_product: zero_count = 2, zeros = [169, 338]
rectangle:        zero_count = 2, zeros = [169, 338]
borrow:           zero_count = 2, zeros = [169, 338]
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_group_ring_normal_form_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_group_ring_normal_form_gate.py
```

Observed:

```text
square_axis_group_ring_normal_form_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_group_ring_normal_form_gate
```

## Consequence

The square-axis residual is no longer an opaque `18`-class set.  It is a short
group-ring word:

```text
3-term orbit factor
times
6-term no-borrow seed
```

or, equivalently:

```text
27-term rectangle minus 9-term borrow corner
```

This is a plausible arithmetic producer target: a modular-unit or CM-Artin
candidate could try to build the rectangle and subtract the borrow corner.  The
Fourier profile also explains why frequency support alone is a weak filter:
the rectangle, borrow corner, and final residual all have the same two
`S`-factor zeros on the `507`-cycle.

The same word has a quotient-coordinate shift interpretation recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_quotient_shift_normal_form.md
```
