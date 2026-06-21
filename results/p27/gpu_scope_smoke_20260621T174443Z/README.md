# P27 GPU Scope Smoke

RunPod RTX 4000 Ada smoke test for p27 search-space narrowing.

```text
p = 1000000000000000000000000103
target_depth = 18
trials = 5,000,000 accepted roots per mode per seed order
seed_modes = identity splitmix
modes = x16stratumprobe x16domainprobe x16ecoverprobe
```

Compact rows are in `scope_probe_rows.jsonl`.

Aggregated over both seed orders:

```text
mode              survivors  target_rate   target/source   survivors/sec  accepted_Mps
x16stratumprobe        698   0.00006980   1.79487e-05       353.252        5.061
x16domainprobe        1268   0.00012680   2.14414e-05       437.596        3.451
x16ecoverprobe        1294   0.00012940   2.20445e-05       597.856        4.620
```

Interpretation: both narrowing modes roughly double accepted-root survival at
depth 18.  `x16ecoverprobe` is the best current practical candidate because it
keeps most of that scope lift while retaining much higher throughput than the
independent domain filter.

