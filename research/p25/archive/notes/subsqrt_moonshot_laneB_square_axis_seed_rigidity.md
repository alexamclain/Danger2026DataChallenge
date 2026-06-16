# Subsqrt Moonshot Lane B Square-Axis Seed Rigidity

Date: 2026-06-12

## Result

The known `3 x 6` factorization of the `18`-point residual leaves a six-term
no-borrow seed:

```text
[43, 86, 95, 129, 138, 147]
```

This gate exhaustively checks that the seed has no simpler hidden shortcut in
`C_507`:

```text
affine stabilizers: 1, namely (1, 0)
6-term arithmetic progression presentations: 0
2 x 3 collision-free sumset factorizations: 0
3 x 2 collision-free sumset factorizations: 0
```

The exhaustive `3 x 3` AP-rectangle check does find structure, but only the
expected no-borrow one.  There are `24` oriented presentations, grouped into
three rectangle completions:

```text
rectangle = [25, 34, 43, 77, 86, 95, 129, 138, 147]
borrow    = [25, 34, 77]

rectangle = [43, 52, 61, 86, 95, 104, 129, 138, 147]
borrow    = [52, 61, 104]

rectangle = [43, 86, 95, 129, 138, 147, 181, 190, 233]
borrow    = [181, 190, 233]
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_seed_rigidity_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/p25_laneB_square_axis_seed_rigidity_gate.py
```

Observed:

```text
square_axis_seed_rigidity_rows = 1 / 1
```

## Consequence

The seed is not an affine orbit, a six-term AP, or a disguised product
factor.  Its remaining compact description is precisely the lower-triangular
no-borrow part of a `3 x 3` AP rectangle.

This sharpens the producer contract:

```text
reject producers that explain the seed as a hidden affine/AP/product shortcut;
accept only producers that recover the lower-triangular no-borrow rectangle
and the three known AP-rectangle completions.
```

The preceding checkpoint is:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/subsqrt_moonshot_laneB_square_axis_sumset_factorization_rigidity.md
```
