# Subsqrt Moonshot Lane B Square-Axis Quotient-Shift Normal Form

Date: 2026-06-12

## Result

The group-ring normal form has a concrete meaning on the quotient coordinates
`C_3 x C_169`.

For:

```text
q = 169*right + 3*c
```

the group-ring steps act as:

```text
D = x^172 : (right, c) -> (right + 1, c + 1)
X = x^43  : (right, c) -> (right + 1, c - 42)
Y = x^9   : (right, c) -> (right,     c + 3)
```

and:

```text
D^3 = Y
```

The residual is exactly:

```text
{D^s X^(h+1) Y^t : s=0,1,2; h=0,1,2; t=0..h}
```

Observed:

```text
selected_count = 18 / 18
selected_qs_match = 1
layer_counts = [6, 6, 6]
h_counts = [3, 6, 9]
t_counts = [9, 6, 3]
shift_formula_hits = 18 / 18
local_shape_hits = 18 / 18
graph_hits = 18 / 18
rectangle_coord_count = 27 / 27
borrow_coord_count = 9 / 9
coordinate_subtraction_ok = 1
```

The selected quotient terms are:

```text
q=43:  s=0 h=0 t=0 right=1 c=127 a=10 b=9
q=86:  s=0 h=1 t=0 right=2 c=85  a=7  b=6
q=95:  s=0 h=1 t=1 right=2 c=88  a=10 b=6
q=129: s=0 h=2 t=0 right=0 c=43  a=4  b=3
q=138: s=0 h=2 t=1 right=0 c=46  a=7  b=3
q=147: s=0 h=2 t=2 right=0 c=49  a=10 b=3
q=215: s=1 h=0 t=0 right=2 c=128 a=11 b=9
q=258: s=1 h=1 t=0 right=0 c=86  a=8  b=6
q=267: s=1 h=1 t=1 right=0 c=89  a=11 b=6
q=301: s=1 h=2 t=0 right=1 c=44  a=5  b=3
q=310: s=1 h=2 t=1 right=1 c=47  a=8  b=3
q=319: s=1 h=2 t=2 right=1 c=50  a=11 b=3
q=387: s=2 h=0 t=0 right=0 c=129 a=12 b=9
q=430: s=2 h=1 t=0 right=1 c=87  a=9  b=6
q=439: s=2 h=1 t=1 right=1 c=90  a=12 b=6
q=473: s=2 h=2 t=0 right=2 c=45  a=6  b=3
q=482: s=2 h=2 t=1 right=2 c=48  a=9  b=3
q=491: s=2 h=2 t=2 right=2 c=51  a=12 b=3
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_quotient_shift_normal_form_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_quotient_shift_normal_form_gate.py
```

Observed:

```text
square_axis_quotient_shift_normal_form_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_quotient_shift_normal_form_gate
```

## Consequence

The short group-ring word is now a quotient-coordinate construction:

```text
three diagonal translates
of a slanted X/Y no-borrow seed
```

The relation `D^3 = Y` is the key structural clue.  The residual is built from
diagonal steps `D`, slanted steps `X`, and pure C-axis steps `Y`; the no-borrow
condition `t <= h` is exactly what keeps the selected points on the boundary
fibers `b = 9,6,3`.

This gives a sharper arithmetic target than a raw class list: look for a
ray-local producer that naturally supplies these quotient shifts and the
rectangle-minus-borrow selection among them.
