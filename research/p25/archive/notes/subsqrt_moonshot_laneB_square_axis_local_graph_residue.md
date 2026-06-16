# Subsqrt Moonshot Lane B Square-Axis Local Graph Residue

Date: 2026-06-12

## Result

The `C_169` graph-lift residual has an exact footprint on the actual
negative-trace local source cycle.

For the square-axis case:

```text
raw_order = 12675 = 25 * 507
quotient_order = 507 = 3 * 169
B = 25
```

The `18` residual quotient points are exactly the triangular comb:

```text
q = 43*(h+1) + 172*s + 9*t mod 507
h = 0,1,2
s = 0,1,2
t = 0..h
```

Observed:

```text
quotient_hits = 12675 / 12675
residual_raw_hits = 450 / 450
graph_q_count = 18 / 18
triangular_q_count = 18 / 18
raw_q_count = 18 / 18
q_sets_match = 1
class_rows = 18 / 18
h_q_counts = [3, 6, 9]
h_raw_counts = [75, 150, 225]
h_boundary_fibers = [[9], [6], [3]]
```

Each residual quotient class lifts to exactly `25` raw exponents:

```text
e = q + 507*k,  k = 0..24
```

and each such class is a product rectangle in the actual local data:

```text
one singleton mod677 C-source residue
times
one 25-element mod151 right-source coset
```

The local class list is:

```text
q=43:  right=1 a=10 b=9 h=0
q=86:  right=2 a=7  b=6 h=1
q=95:  right=2 a=10 b=6 h=1
q=129: right=0 a=4  b=3 h=2
q=138: right=0 a=7  b=3 h=2
q=147: right=0 a=10 b=3 h=2
q=215: right=2 a=11 b=9 h=0
q=258: right=0 a=8  b=6 h=1
q=267: right=0 a=11 b=6 h=1
q=301: right=1 a=5  b=3 h=2
q=310: right=1 a=8  b=3 h=2
q=319: right=1 a=11 b=3 h=2
q=387: right=0 a=12 b=9 h=0
q=430: right=1 a=9  b=6 h=1
q=439: right=1 a=12 b=6 h=1
q=473: right=2 a=6  b=3 h=2
q=482: right=2 a=9  b=3 h=2
q=491: right=2 a=12 b=3 h=2
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_local_graph_residue_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_local_graph_residue_gate.py
```

Observed:

```text
square_axis_local_graph_residue_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_local_graph_residue_gate
```

## Consequence

The square-axis boundary residual is now a fully local target:

```text
18 classes modulo 507
25 raw exponents per class
450 raw positions total
```

This is a better producer-facing object than an abstract `C_169` mask.  A
candidate modular-unit or CM-Artin source should be tested against the
triangular comb directly: it must select exactly those `q` classes, and its
raw lift must be one `mod677` singleton times one `mod151` right coset for each
class.

The next positive arithmetic target is therefore not just:

```text
make the C_13 trace-shadow
```

but:

```text
make the triangular exponent comb q = 43*(h+1) + 172*s + 9*t mod 507
and lift each q class through the 25-element mod151 coset.
```

The base-`43` digit selector form of the same comb is recorded in:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_digit_selector.md
```
