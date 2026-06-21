# GPU Source-Stratum Probe For P26

Date: 2026-06-21

This note records the first follow-up test of the hypothesis that the early p26
GPU hit might have exposed a useful `X1(16)` source stratum, rather than merely
landing early inside a randomized search budget.

## Code Added

`pomerance_cuda.cu` now has three related analysis features:

- `-DPOM_CUDA_HIT_TELEMETRY=1` enables richer hit logging without slowing the
  default production search build.
- `x16stratumprobe` runs a bounded-depth GPU probe instead of a full hit search.
- Optional arguments support `seed=mixed|identity|splitmix`, `start_chunk=N`,
  `start_trial=N`, `target_depth=N`, `bucket_bits=N`, and `focus_bucket=N`.

The default production build keeps the original fast `u96` search kernel shape:

```text
u96 production kernel, default build: 66 registers, no spills
u96 production kernel, telemetry build: 88 registers, no spills
```

So production searches should use the default build, and replay/diagnostic runs
should use the telemetry build only when the extra hit fields matter.

## Hit Replay Telemetry

The original p26 run found:

```text
p  = 100000000000000000000000067
A  = 78462973492772865017160395
x0 = 27732450411057582323409556
```

Using `start_chunk=139`, the telemetry build replayed only the hit chunk and
recovered the same verified triple in 17.65 seconds.

The replay logged:

```text
seed_offset=121
chunk_nonce=139
tid=54163
raw_draw_count=40930
local_draw_count=26351
root_index=0
q_sheet=0
compactD=d1b7949c9c197659
y=64812415469854269851232773
root_x=48276554802230722202920041
xP16=60651682281716172464088664
first_w=15400924470879271160683427
V=23234196395824796332620513
D=30099400759640349946656938
```

The replay's absolute `trial_index` was not identical to the original run. This
is expected: candidate claim order is controlled by GPU atomics, so the absolute
claim index is not stable across builds or runs. The stable reconstruction
fields are the seed/chunk/thread/draw telemetry and the source field elements.

At `bucket_bits=6`, the hit's compact probe bucket is:

```text
bucket=16
q_sheet=0
key=16
```

The replay log is stored at:

```text
results/p26/p26-hit-replay-telemetry.log
```

## Probe Design

The probe mode samples valid `X1(16)` nonsplit roots, then follows the first
halving branch only up to a target depth such as 24 or 26. It records aggregate
survival rates by compact source buckets.

The current bucket is deliberately a fast diagnostic hash, not a canonical
mathematical invariant:

```text
bucket = q_sheet || low_bits(hash(D, first_w, V, y))
```

Each run is split into a prefix half and a held-out half. Buckets are selected
by prefix lift and judged by held-out lift. A bucket is promotion-ready only if
its held-out depth-24 or depth-26 lift is at least 1.25x and it has at least
100 held-out survivors.

## Paired Seed-Order Probes

The first 100M depth-24 probes were useful only as a smoke test:

```text
identity depth 24:  76 / 100000000 survivors
splitmix depth 24: 124 / 100000000 survivors
```

Those counts are too small for interpretation.

The 1B depth-26 probes produced:

```text
identity depth 26: 216 / 1000000000 survivors
splitmix depth 26: 248 / 1000000000 survivors
mixed    depth 26: 260 / 1000000000 survivors
```

None of the prefix-selected buckets cleared the held-out promotion bar.

The probe logs are stored under:

```text
research/p26/probes/
```

## Hit Bucket Check

The hit bucket, `bucket=16`, was checked in both a control chunk and the actual
hit chunk.

Control chunk, `start_chunk=0`, mixed seed order:

```text
global depth-26 heldout rate: 0.000000284
bucket 16 prefix: 1 / 3906753, lift 1.085
bucket 16 heldout: 3 / 3908148, lift 2.703
promotion: no
```

The held-out lift is numerically high there, but it is based on only three
survivors, far below the 100-survivor bar.

Hit chunk, `start_chunk=139`, mixed seed order:

```text
global depth-26 heldout rate: 0.000000228
bucket 16 prefix: 0 / 3906922, lift 0.000
bucket 16 heldout: 1 / 3906205, lift 1.123
promotion: no
```

So the hit's own compact bucket does not look elevated in the hit chunk.

## Interpretation

This first test does not support a usable seed law. It also does not support the
specific coarse bucket `q_sheet || hash(D, first_w, V, y)` as the hidden source
stratum behind the early p26 hit.

The result is still useful. We can now:

- replay a specific chunk cheaply with `start_chunk`;
- recover hit-local source telemetry;
- run paired identity/splitmix/mixed seed-order probes;
- test a proposed bucket against prefix and held-out data.

For now, the conservative interpretation is that the p26 hit was favorable luck
inside a cheap GPU budget. If there is a real `X1(16)` source stratum to learn,
it is finer than this first compact bucket or depends on a different invariant.

## Next Tests If Pursuing

Useful next steps would be:

- log individual depth-24 or depth-26 survivor rows for a bounded sample;
- compare exact hit-neighborhood rows against matched controls, rather than
  only compact hash buckets;
- define mathematical labels for `V`, `D`, q-sheet, and first halving signs;
- add a direct sampler once a label has held-out lift, instead of relying on
  seed order.

Until then, no search budget should be reallocated on the assumption that this
seed/stratum signal is real.
