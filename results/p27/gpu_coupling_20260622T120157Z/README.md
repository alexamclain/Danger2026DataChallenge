# p27 GPU Recurrence-Coupling Telemetry, Gates 3..12

Target prime:

```text
p = 1000000000000000000000000103
```

This bounded A40 run tested whether the selected quadratic-gate signs in the
recurrence domain show repeatable sign-word lift after normalizing by raw
X1(16) source draws.  It is telemetry, not a production certificate search.

Run shape:

- GPU: NVIDIA A40, CUDA `sm_86`
- Seed orders: `identity`, `splitmix`
- Raw source draws: 100,000,000 per seed order
- Gate range: 3..12
- Short sign-word buckets: up to 6 bits

Summary:

| seed order | raw draws | recurrence rows | gate-12 survivors | target/source draw | target/s | mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| identity | 100,000,000 | 6,256,372 | 5,972 | 0.00005972 | 352.88 | 0 |
| splitmix | 100,000,000 | 6,249,614 | 6,188 | 0.00006188 | 366.07 | 0 |

The formula telemetry validated cleanly: `B=sqrt(A+2)` was available for every
recurrence row, `formula_unavailable=0`, `materialize_fail=0`, and
`actual_mismatch=0` in both seed orders.

Interpretation:

- Per-gate plus rates are close to independent half-gates.
- Pairwise tables are intentionally labeled `censored_or_degenerate`, because
  later signs are only observable after earlier selected plus gates.
- No heldout bucket met the residual promotion bar.  The largest all-plus
  heldout residual lift was about `1.028x`, well below `1.25x`.
- The raw-source-normalized result supports the kill interpretation for this
  probe depth: sign words thin like independent half-gates.

Primary machine-readable files:

- `coupling_rows.jsonl`
- `coupling_bucket_rows.jsonl`
- `coupling_pair_rows.jsonl`
- `coupling_lag_rows.jsonl`
- `coupling_sample_rows.jsonl`
