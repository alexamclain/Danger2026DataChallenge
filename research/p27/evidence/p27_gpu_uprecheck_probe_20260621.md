# P27 GPU U+2 Precheck Probe

Date: 2026-06-21

Target:

```text
p = 1000000000000000000000000103
```

CUDA source under test:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/pomerance_cuda.cu
```

New CUDA mode:

```text
x16uprecheckprobe
```

The mode uses the existing `u96` p27 nonsplit X1(16) source/root path, then
tests the exact prefix identity:

```text
chi(x_next) = chi(u + 2)
```

before `sqrt(w)` when the requested prefix depth still needs the next gate.
On a `chi(u+2) != +1` branch, it short-circuits the prefix depth as
`current_depth + 1`.

This relies on the nonsplit identity that after `d_j` is square exactly one
`w_j` branch is square.  The GPU survival rates below match the ordinary
prefix probe, which is the practical consistency check.

## Compile

Pod/GPU:

```text
RunPod pod tnhwchopm8t286
NVIDIA RTX 6000 Ada Generation
CUDA 12.8, sm_89
```

Compile:

```text
nvcc -O3 -std=c++17 -arch=sm_89 -Xptxas=-v -o pomerance_cuda_p27_uprecheck pomerance_cuda.cu
```

The `x16uprecheckprobe` kernel compiled with:

```text
registers = 88
stack frame = 56 bytes
spill stores/loads = 0/0
```

## Depth 8 A/B

Baseline:

```text
./pomerance_cuda_p27_uprecheck 1000000000000000000000000103 \
  121 50000000 x16stratumprobe 50000000 0 256 1 u96 \
  seed=mixed target_depth=8 bucket_bits=0
```

Result:

```text
accepted_roots = 50000000
elapsed = 1.355s
rate = 36.89M accepted roots/sec
depth>=8 survivors = 3124310
depth>=8 rate = 0.062486200
```

U+2 precheck:

```text
./pomerance_cuda_p27_uprecheck 1000000000000000000000000103 \
  121 50000000 x16uprecheckprobe 50000000 0 256 1 u96 \
  seed=mixed target_depth=8
```

Result:

```text
accepted_roots = 50000000
elapsed = 1.669s
rate = 29.96M accepted roots/sec
depth>=8 survivors = 3122698
depth>=8 rate = 0.062453960

uplus_checks = 76538920
uplus_pass = 32794866
uplus_reject = 43744054
short_circuit = 21872027
w_sqrt_calls = 37479888
w_sqrt_success = 24984860
```

Effective depth-8 survivors/sec:

```text
baseline = 2.31M/sec
u+2 precheck = 1.87M/sec
effective lift = 0.81x
```

## Depth 10 A/B

Baseline:

```text
./pomerance_cuda_p27_uprecheck 1000000000000000000000000103 \
  121 50000000 x16stratumprobe 50000000 0 256 1 u96 \
  seed=mixed target_depth=10 bucket_bits=0
```

Result:

```text
accepted_roots = 50000000
elapsed = 1.477s
rate = 33.85M accepted roots/sec
depth>=10 survivors = 780903
depth>=10 rate = 0.015618060
```

U+2 precheck:

```text
./pomerance_cuda_p27_uprecheck 1000000000000000000000000103 \
  121 50000000 x16uprecheckprobe 50000000 0 256 1 u96 \
  seed=mixed target_depth=10
```

Result:

```text
accepted_roots = 50000000
elapsed = 1.796s
rate = 27.84M accepted roots/sec
depth>=10 survivors = 780021
depth>=10 rate = 0.015600420

uplus_checks = 84733516
uplus_pass = 36303912
uplus_reject = 48429604
short_circuit = 24214802
w_sqrt_calls = 37473252
w_sqrt_success = 24981434
```

Effective depth-10 survivors/sec:

```text
baseline = 528.8k/sec
u+2 precheck = 434.3k/sec
effective lift = 0.82x
```

## Thread Shape

For `x16uprecheckprobe`, `target_depth=8`, `20M` accepted roots:

```text
threads=128  rate=30.08M accepted roots/sec
threads=256  rate=29.96M accepted roots/sec on the 50M run
threads=384  rate=27.12M accepted roots/sec
threads=512  rate=28.82M accepted roots/sec
```

The best tested shape is `128` threads/block, but it remains slower than the
ordinary prefix probe at `256` threads/block.

## Interpretation

The `u+2` identity is exact and it does shrink the continuation scope: each
successful use identifies about half of the current prefix rows as unable to
pass the next x-square gate.  For a staged search, this is the important
mathematical fact: the rows outside the `chi(u+2)=+1` stratum do not need to be
carried forward for that next prefix depth.

The negative result is narrower.  This particular GPU implementation does not
turn the scope shrink into a wall-clock win when it is used as an independent
per-gate precheck.  The extra Legendre work costs more than the avoided
`sqrt(w)` calls for fixed prefix depths 8 and 10.

Promotion decision:

```text
scope shrink is real: about one half per u+2 gate
do not promote this independent-Legendre implementation as the production path
keep the code/telemetry as a costed scope-shrink result
continue looking for a direct source or recurrence coupling many chi(u_j+2)
bits, not independent per-gate Legendre checks
```

```text
p27_gpu_uprecheck_probe_rows=1/1
```
