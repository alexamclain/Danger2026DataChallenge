# P27 GPU Scope Probe

Date: 2026-06-21

## Purpose

Test search-space narrowing, not just raw throughput, for the p27 first-lift
source candidates on actual GPU infrastructure.

The CUDA probe compared:

```text
baseline: x16stratumprobe
domain filter control: x16domainprobe
elliptic-cover source: x16ecoverprobe
```

Target:

```text
p = 1000000000000000000000000103 = 10^27 + 103
target_depth = 18
trials = 5,000,000 accepted roots per mode per seed order
seed_order = identity, splitmix
GPU = NVIDIA RTX 4000 Ada Generation
container = runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04
```

The RunPod pod was stopped after the runs.

## Artifacts

Depth-18 smoke JSONL:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/results/p27/gpu_scope_smoke_20260621T174443Z/scope_probe_rows.jsonl
```

Depth-20 promotion-bar JSONL:

```text
/Users/agent/Documents/Codex/2026-06-20/if-i-have-c-code-that/work/Danger2026DataChallenge/results/p27/gpu_scope_depth20_20260621T174928Z/scope_probe_rows.jsonl
```

The CUDA binary hash on the pod was:

```text
a97c9ac80d41ace9621a214ebda9244a2180cf31a79141a2f07fca8e17a1a3d8
```

## Depth-18 Smoke Result

Per seed order:

```text
seed      mode              survivors  target_rate   target/source   survivors/sec  accepted_Mps  rate_lift  source_lift  sec_lift
identity  x16stratumprobe        390   0.000078000  2.00579e-05       392.838         5.036       1.000      1.000        1.000
identity  x16domainprobe         672   0.000134400  2.27304e-05       463.753         3.451       1.723      1.133        1.181
identity  x16ecoverprobe         632   0.000126400  2.15365e-05       584.203         4.622       1.621      1.074        1.487
splitmix  x16stratumprobe        308   0.000061600  1.58395e-05       313.277         5.086       1.000      1.000        1.000
splitmix  x16domainprobe         596   0.000119200  2.01528e-05       411.430         3.452       1.935      1.272        1.313
splitmix  x16ecoverprobe         662   0.000132400  2.25523e-05       611.500         4.619       2.149      1.424        1.952
```

Aggregated over identity and splitmix:

```text
mode              survivors  target_rate   target/source   survivors/sec  accepted_Mps
x16stratumprobe        698   0.00006980   1.79487e-05       353.252        5.061
x16domainprobe        1268   0.00012680   2.14414e-05       437.596        3.451
x16ecoverprobe        1294   0.00012940   2.20445e-05       597.856        4.620
```

## Depth-20 Promotion-Bar Result

The follow-up run used:

```text
target_depth = 20
trials = 50,000,000 accepted roots per mode per seed order
```

Per seed order:

```text
seed      mode              survivors  target_rate   target/source   survivors/sec  accepted_Mps  rate_lift  source_lift  sec_lift
identity  x16stratumprobe        802   0.000016040  7.32740e-06       122.803         7.656       1.000      1.000        1.000
identity  x16domainprobe        1572   0.000031440  7.50413e-06       148.465         4.722       1.960      1.024        1.209
identity  x16ecoverprobe        1672   0.000033440  7.98990e-06       228.122         6.822       2.085      1.090        1.858
splitmix  x16stratumprobe        736   0.000014720  6.72577e-06       112.412         7.637       1.000      1.000        1.000
splitmix  x16domainprobe        1496   0.000029920  7.13867e-06       140.559         4.698       2.033      1.061        1.250
splitmix  x16ecoverprobe        1524   0.000030480  7.27979e-06       206.620         6.779       2.071      1.082        1.838
```

Aggregated over identity and splitmix:

```text
mode              survivors  target_rate   target/source   survivors/sec  accepted_Mps
x16stratumprobe       1538   0.00001538   7.02662e-06       117.601        7.646
x16domainprobe        3068   0.00003068   7.32136e-06       144.502        4.710
x16ecoverprobe        3196   0.00003196   7.63478e-06       217.337        6.800
```

Aggregate lifts versus raw nonsplit baseline:

```text
mode              accepted-root survival  target/source  survivors/sec
x16domainprobe          1.995x              1.042x          1.229x
x16ecoverprobe          2.078x              1.087x          1.848x
```

## Interpretation

This supports the CPU read that the p27 first-lift/domain condition is real
accepted-root scope narrowing.  In accepted-root terms, both `x16domainprobe`
and `x16ecoverprobe` roughly double depth-20 survival versus raw nonsplit
baseline on both seed orders.

For actual GPU work, `x16ecoverprobe` is the better first candidate in this
implementation: it preserved the scope lift while keeping much more throughput
than the independent domain Legendre filter.  At depth 20, aggregated
survivor/sec was about `1.85x` baseline for ecover versus about `1.23x`
baseline for the domain filter.

In source-draw terms, the first-lift source is a smaller win than accepted-root
rate alone suggests, because the ecover sampler spends extra source draws to
materialize accepted roots.  At depth 20, aggregated target-per-source-draw
lift was about `1.09x` for ecover and `1.04x` for domain.  So the cleanest
positive statement is: the first-lift/domain condition halves the accepted-root
continuation space, but it is not yet a large raw-source-space shrink.

This does not prove sqrt beating.  It is a one-bit source/filter improvement.
The live next GPU/math question remains whether a second-gate or later-gate
source law can be sampled directly, rather than repeatedly paying a random
factor of about `1/2`.

## Next GPU Step

The next practical GPU run should test a second-gate source, not merely repeat
the first-gate ecover result:

```text
candidate = ecover plus a cheap second-gate/direct-source criterion
target_depth = 20 or 22
trials = 50M to 100M per mode, enough for >=1000 target survivors
```

Promotion bar:

```text
future source candidates should improve target/source lift by at least 1.25x
with >=1000 compared survivors, not only improve accepted-root survival.
```
