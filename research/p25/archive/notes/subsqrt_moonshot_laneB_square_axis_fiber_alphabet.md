# Subsqrt Moonshot Lane B Square-Axis Fiber Alphabet

Date: 2026-06-12

## Result

The `C_3 x C_169` target is not a `C_13` lift, but it has a compact
`13`-adic fiber alphabet.

Write:

```text
j = a + 13*b,  a,b in C_13.
```

For each fixed right row and residue `a`, the `b`-fiber is one of only six
binary words of length `13`.

Observed:

```text
unique_fiber_patterns = 6 / 6
pattern_weights = [6, 6, 6, 7, 7, 7]
pattern_counts = [4, 7, 10, 6, 3, 9]
rank_f2 = 6
rank_odd = 6
trace_weight_hits = 39 / 39
zero_trace_pattern_count = 3 / 3
one_trace_pattern_count = 3 / 3
```

The key law is:

```text
fiber weight = 6 + C_13 trace-shadow bit.
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_fiber_alphabet_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_fiber_alphabet_gate.py
```

Observed:

```text
square_axis_fiber_alphabet_rows = 1 / 1
conclusion = reported_p25_laneB_square_axis_fiber_alphabet_gate
```

## Consequence

This turns the square-axis target into a more concrete producer problem:

```text
not merely lift C_13;
place six rank-6 fiber words across the 39 C_13 trace-shadow slots;
retain the primitive/non-lifted C_169 character payload;
pay only the degree-13 Kummer anchor descent.
```

That is a better moonshot target than an unstructured `507`-point mask.  A
candidate square-axis CM-Artin or modular-unit producer should be tested first
for whether its local fibers land in this six-word alphabet with the correct
trace-shadow placement.

The exact placement law is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_fiber_placement_law.md
```

It records that the fiber word is the `C_13` half-arc row
`h = right - a mod 3`, plus a single boundary bit at `9 - 3h` exactly when the
`C_13` trace-shadow bit is `1`.
