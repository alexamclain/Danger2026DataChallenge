# GPU Throughput Report For P26

Date: 2026-06-20

This note records the GPU engineering work that made the p26 run practical. It
is an operations and performance report, not a new mathematical shortcut.

The verified p26 result is recorded in `results/p26/`.

## Session Goal Prompt

The GPU optimization and p26 run were carried out under this goal-mode prompt:

```text
Optimize the existing code so that a single GPU 550b search would run in as few hours as possible. You're authorized to start the pod when you need GPU tests and stop it when done. If the account runs out of money just stop there.
```

## Executive Summary

The CPU `x16halvenonsplit` path was ported to a narrow CUDA implementation
focused on the production `X1(16)` nonsplit first-branch halving search. On an
RTX 6000 Ada RunPod instance, the final p26 run sustained about 52M candidates
per second and found a verified triple after 139934292088 X1(16) curves.

The hit was early relative to the explicit 550B search budget. The engineering
result is that the GPU made a 550B p26 budget inexpensive and operationally
easy; the fact that this particular randomized search found a triple before
140B candidates should be interpreted as favorable luck inside that budget.

## Search Target

```text
p = 100000000000000000000000067 = 10^26 + 67
p mod 8 = 3
p mod 4 = 3
k = 44
sqrt_floor(p) = 10000000000000
```

The `p mod 4 = 3` condition matters because the CUDA path needs a fast modular
square-root branch. The p23 and p25 production targets used the `p mod 8 = 5`
branch; p26 exercises the `x = n^((p+1)/4)` square-root case.

## What Was Ported

The CUDA code deliberately ports only the hot production path:

```text
x16halvenonsplit
```

It does not attempt to port every diagnostic or exploratory mode in
`pomerance.c`. The generic 2-Sylow search, theorem-side probes, and research
diagnostics remain CPU-side.

The GPU path includes:

- Montgomery arithmetic for 128-bit primes.
- A specialized 96-bit field backend for `p < 2^96`.
- Device-side `X1(16)` construction, y-level nonsplit discriminant filtering,
  and first-branch halving.
- Fast square-root handling for `p == 5 mod 8` and `p == 3 mod 4`.
- Per-chunk progress logging and optional detailed stage counters.

For p23, p25, and p26, the automatic backend chooses the 96-bit implementation.

## Throughput Work

The main throughput choices were constant-factor engineering rather than a
change in the search distribution.

### Keep the GPU in integer arithmetic, not host orchestration

Candidate generation, modular arithmetic, square-root tests, discriminant
classification, and halving all run inside the CUDA kernel. The host launches
large chunks and copies back only compact counters and the first hit.

### Use a 96-bit backend for current targets

The current challenge primes fit below `2^96`. The specialized `U96` path
avoids the heavier generic `unsigned __int128` arithmetic in the main hot loop.
The final p26 run used:

```text
backend = u96
```

### Keep values in Montgomery form

The port keeps most repeated field operations in Montgomery form and avoids
unnecessary conversion back to standard representation in the hot path.

### Tune work claiming

The winning default uses:

```text
threads = 128
claim_batch = 1
blocks = SM_count * 8 for the u96 backend
```

For the RTX 6000 Ada run, this produced:

```text
SMs = 142
blocks = 1136
threads = 128
claim_batch = 1
```

This configuration kept the device saturated while limiting overclaim at chunk
and hit boundaries.

### Keep logging small

The full p26 production log is only about 11 KB. It records one progress line
per 1B-candidate chunk, plus the final hit and verification status. No large
candidate table or per-thread state is persisted.

The observed GPU memory footprint during the p26 run was about 436 MiB.

## Benchmark Ledger

Representative measurements from the session:

```text
CPU baseline, p23 path                 ~= 0.799M candidates/sec
RTX 4090, p23, best observed           ~= 48.53M candidates/sec
RTX 6000 Ada, p23 comparison, 1B run   ~= 51.36M candidates/sec
RTX 6000 Ada, p26 benchmark, 1B run    ~= 52.65M candidates/sec
RTX 6000 Ada, p26 production near hit  ~= 52.00M candidates/sec
```

The p23 RTX 4090 result was about 60.7x the single-CPU baseline. Comparing the
final p26 production rate to that same CPU baseline gives about 65.1x, though
that is not an apples-to-apples mathematical comparison because p23 and p26 use
different primes.

The p26 production run:

```text
start_utc = 2026-06-20T23:19:24Z
end_utc   = 2026-06-21T00:04:15Z
elapsed_to_hit = 2691.21 seconds
trials_at_hit  = 139934292088
rate_near_hit  = 51.996815M candidates/sec
```

At the observed rate, exhausting the full 550B cap would have taken about 2.94
hours. At the RunPod price used for this run, `$0.77/hr`, that full cap would
have cost about `$2.26` of compute. The actual early-hit compute cost was about
`$0.58`.

## Interpretation Of The Early Hit

The p26 result should not be read as evidence that every p26-scale target will
fall within 140B candidates.

The hit came at:

```text
139934292088 / 550000000000 = 25.44% of the explicit budget
139934292088 / 10000000000000 = 1.39934292088% of sqrt_floor(p)
```

That is comparatively early. The practical interpretation is:

- the `X1(16)` nonsplit/halving route gives a useful fixed-prime search
  distribution;
- the GPU port made very large budgets cheap enough to try;
- this specific p26 run got lucky inside the chosen randomized budget.

A no-hit result after 550B candidates would not have falsified the method, and
this early hit does not prove an asymptotic sub-square-root algorithm. It is a
strong fixed-prime practical outcome.

## Seed Order And Source-Stratum Follow-Up

The early p26 hit is not enough evidence for a usable seed law. It is, however,
worth treating as a possible clue that seed order may have accidentally exposed
a real `X1(16)` source stratum that should be learned and sampled directly.

Future GPU-agent runs should log enough telemetry to distinguish seed-order
effects from source-stratum effects. For every hit, and for selected near-hit
controls, record:

- `seed_offset`
- `chunk_nonce`
- thread id
- raw and local draw counts
- source `y`
- root index
- `root_x` / `xP16`
- `A`
- `x0`
- first halving witness `first_w`
- `V`
- `D`
- `compactD`
- q-sheet or equivalent sheet label

The comparison matrix should include:

- identity seed order versus SplitMix seed order;
- hit-neighborhood windows versus matched controls;
- prefix behavior versus held-out behavior.

Promotion bar:

- held-out depth-24 or depth-26 lift should be at least 1.25x;
- require at least 100 compared survivors before treating the signal as real;
- require a direct way to sample or restart into the winning stratum, rather
  than only changing seed order.

In short: the next target is not "pick better seeds" by itself. The stronger
target is to identify whether a real `X1(16)` source stratum is being exposed
by the seed order, then sample that stratum directly.

Follow-up: `gpu-stratum-probe_20260621.md` records an initial GPU probe of this
idea. It recovered hit-local telemetry, compared identity/splitmix/mixed seed
orders, and did not find a held-out-promoted compact source bucket.

## Cloud Operations

RunPod pods were preferable to serverless for this experiment because the job
is stateful, benefits from SSH/tmux supervision, and needs ordinary filesystem
logs. The useful operational pattern was:

1. Start a pod with an Ada-generation GPU.
2. Copy the CUDA source to `/workspace`.
3. Compile with `nvcc`.
4. Run the search inside `tmux`.
5. Stream compact progress logs.
6. Copy the final log locally.
7. Stop the pod immediately after completion.

The successful p26 run used an RTX 6000 Ada pod after RTX 4090 inventory was
unavailable. The CUDA source compiled with:

```sh
/usr/local/cuda-12.8/bin/nvcc -O3 -std=c++17 -arch=sm_89 -Xptxas=-v \
  -o p26_opt pomerance_cuda_p26.cu
```

The p26 production command was:

```sh
./p26_opt 100000000000000000000000067 121 550000000000 \
  x16halvenonsplit 1000000000
```

## Why Not TPU

TPUs were not pursued. The hot loop here is branchy modular integer arithmetic
with rejection sampling, Legendre/square-root tests, Montgomery operations, and
early exits. That is a poor fit for TPU tensor units compared with a CUDA GPU
running integer-heavy kernels.

## Current Limitations

- The CUDA program is intentionally narrow and implements only
  `x16halvenonsplit`.
- Supported fast square-root cases are `p == 5 mod 8` and `p == 3 mod 4`.
- The code supports the current primes through the `u96` path and has a generic
  128-bit backend for larger supported primes, but performance work so far
  focused on `p < 2^96`.
- The log is an audit trail, not a full checkpoint system. A future
  `start_trial` or `start_chunk` argument would make exact resume after
  interruption cleaner.
- Multi-GPU sharding was not needed for p26, but independent seed offsets
  should make it straightforward operationally.

## Next Throughput Ideas

Potential follow-ups:

- Add explicit resume offsets so long searches can restart without replaying
  completed chunks.
- Add a small benchmark harness that records device name, register count,
  blocks, threads, claim batch, chunk size, and rate in a machine-readable
  table.
- Revisit the generic 128-bit path before larger primes become the dominant
  target.
- Test H100/L40S/Ada variants when available, with the same benchmark harness.
- Explore whether additional Montgomery-domain reuse can cut a few more
  multiplications from the y-to-A construction.

## Reproducibility Pointers

- CUDA source: `pomerance_cuda.cu`
- Verified p26 result: `results/p26/triple.txt`
- GPU run log: `results/p26/worker.log`
- Verifier transcript: `results/p26/verification.txt`
- Lean certificate: `results/p26/pomerance_100000000000000000000000067.lean`
