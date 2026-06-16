# Subsqrt Moonshot Lane B Square-Axis Sumset Factorization Rigidity

Date: 2026-06-12

## Result

The `18`-point square-axis residual has no unrelated small collision-free
sumset factorization in `C_507`.

Every nontrivial factorization of an `18`-point set has a factor of size `2`
or `3`, up to swapping factors.  Exhaustively checking normalized `2 x 9` and
`3 x 6` factorizations gives:

```text
2 x 9 factorizations: 0
3 x 6 factorizations: 3
```

The three `3 x 6` factorizations are exactly the same `S`-orbit factorization,
seen from one of its three layers:

```text
small = [0, 163, 335]
large = [387, 430, 439, 473, 482, 491]

small = [0, 172, 335]
large = [215, 258, 267, 301, 310, 319]

small = [0, 172, 344]
large = [43, 86, 95, 129, 138, 147]
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_sumset_factorization_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_sumset_factorization_rigidity_gate.py
```

Observed:

```text
residual_points = 18 / 18
two_by_nine = 0
three_by_six = 3
expected_three_by_six = 3
square_axis_sumset_factorization_rigidity_rows = 1 / 1
```

## Consequence

The residual cannot be explained as a different small product set.  The only
small product structure is:

```text
S orbit factor
times
the 6-term no-borrow seed
```

This sharpens the producer target:

```text
reject alternate 2x9 or 9x2 product explanations;
reject unrelated 3x6 or 6x3 product explanations;
keep only producers that explain the S orbit and the no-borrow seed itself.
```

The preceding relation-space checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_relation_space_convolution_rank.md
```
