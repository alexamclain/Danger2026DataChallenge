# p27 GPU Recurrence-Coupling Telemetry, Gates 3..16

Target prime:

```text
p = 1000000000000000000000000103
```

This was the cheap stretch run after the gates 3..12 probe.  It uses the same
raw X1(16) source denominator and extends selected quadratic-gate telemetry to
gate 16.

Run shape:

- GPU: NVIDIA A40, CUDA `sm_86`
- Seed orders: `identity`, `splitmix`
- Raw source draws: 100,000,000 per seed order
- Gate range: 3..16
- Short sign-word buckets: up to 8 bits

Summary:

| seed order | raw draws | recurrence rows | gate-16 survivors | target/source draw | target/s | mismatches |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| identity | 100,000,000 | 6,256,372 | 434 | 0.00000434 | 25.62 | 0 |
| splitmix | 100,000,000 | 6,249,614 | 430 | 0.00000430 | 25.42 | 0 |

The formula telemetry again validated cleanly: `B=sqrt(A+2)` was available for
every recurrence row, `formula_unavailable=0`, `materialize_fail=0`, and
`actual_mismatch=0` in both seed orders.

Interpretation:

- Gates 13..16 are necessarily thinner, so their plus rates have larger
  sampling noise.  The paired identity/SplitMix totals still land near the
  independent expectation.
- No heldout bucket met the residual promotion bar.  The largest all-plus
  heldout residual lift was about `1.053x`, below the required `1.25x`.
- Count-lift deviations for observed 8-bit sign words were about 1% in
  heldout, consistent with independent thinning rather than a reusable
  recurrence-coupled bucket.

Primary machine-readable files:

- `coupling_rows.jsonl`
- `coupling_bucket_rows.jsonl`
- `coupling_pair_rows.jsonl`
- `coupling_lag_rows.jsonl`
- `coupling_sample_rows.jsonl`
