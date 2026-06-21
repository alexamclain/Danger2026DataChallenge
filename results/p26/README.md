# DANGER3 p26 Result

This directory records a verified Pomerance triple found for

```text
p  = 100000000000000000000000067
A  = 78462973492772865017160395
x0 = 27732450411057582323409556
```

The result was found by the CUDA `x16halvenonsplit` port in
`pomerance_cuda.cu`. The search uses Sutherland `X1(16)` prescribed torsion, a
y-level nonsplit Montgomery discriminant filter, and first-branch successive
halving in the cyclic nonsplit rational 2-Sylow case.

The target has `p mod 8 = 3`, so this run exercises the CUDA fast square-root
path for `p == 3 mod 4`.

Successful run:

```text
GPU: RTX 6000 Ada
seed_offset: 121
max_trials: 550000000000
chunk_trials: 1000000000
backend: u96
blocks: 1136
threads: 128
claim_batch: 1
elapsed_to_hit: 2691.21 seconds
successful_trials: 139934292088
observed_rate_near_success: 51.996815M candidates/sec
```

Comparison to sqrt scale:

```text
sqrt_floor(p) = 10000000000000
successful run fraction of sqrt_floor(p): 0.013993429
successful run speedup versus sqrt-floor trials: about 71.46x
```

Files:

- `triple.txt`: one-line triple for DANGER3 `vpp.py`.
- `verification.txt`: independent replay, primality check, and DANGER3 verifier transcript.
- `worker.log`: full GPU run log.
- `worker-tail.txt`: final GPU run log tail.
- `p26-hit-replay-telemetry.log`: replay of the hit chunk with
  `POM_CUDA_HIT_TELEMETRY=1`, recording source `y`, root sheet, `D`,
  `first_w`, `V`, and draw counters.
- `pomerance_100000000000000000000000067.lean`: generated Lean certificate artifact.
