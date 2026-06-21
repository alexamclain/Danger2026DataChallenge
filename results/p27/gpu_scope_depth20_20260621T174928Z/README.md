# P27 GPU Scope Depth-20 Probe

RunPod RTX 4000 Ada promotion-bar probe for p27 search-space narrowing.

```text
p = 1000000000000000000000000103
target_depth = 20
trials = 50,000,000 accepted roots per mode per seed order
seed_modes = identity splitmix
modes = x16stratumprobe x16domainprobe x16ecoverprobe
```

Compact rows are in `scope_probe_rows.jsonl`.  `scope_probe_rows.jsonl.raw`
is the undeduplicated original produced by redirecting the full script output
inside `OUT_DIR`; the runner has since been patched to avoid that duplicate
collection path.

Aggregated over both seed orders:

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

Interpretation: the first-lift/domain condition is real accepted-root scope
narrowing at depth 20.  In raw source-draw terms, however, the lift is modest
because both narrowing modes need about twice as many source draws per accepted
root.  `x16ecoverprobe` remains the practical winner because it preserves the
accepted-root scope lift with much better GPU throughput than the independent
domain filter.

