# DANGER3 Pomerance Search Results

This fork records verified DANGER3 Pomerance triples for
`p = 10^26 + 67`, `p = 10^25 + 13`, `p = 10^23 + 117`, and
`p = 10^22 + 9`, plus the local Codex-assisted experimental work used to find
and verify them. This work was undertaken as part of a collaboration across
teams in DARPA's expMath program.

Curated research notes now live in:

- `research/p23/` for the p23 campaign and its supporting audits;
- `research/p24/` for the p24 research wiki and archived exploration;
- `research/p25/` for the p25 research wiki imported from the separate
  `pomerance-p25-run` workspace.
- `research/p26/` for the GPU throughput engineering report behind the p26
  run.

## p26 Result: GPU X1(16) Nonsplit Search

For

```text
p = 100000000000000000000000067 = 10^26 + 67
```

the GPU run found the triple:

```text
100000000000000000000000067 78462973492772865017160395 27732450411057582323409556
```

Equivalently:

```text
p  = 100000000000000000000000067
A  = 78462973492772865017160395
x0 = 27732450411057582323409556
```

The p26 hit used the same practical `X1(16)` nonsplit/halving family as p23
and p25, but ran through the CUDA port in `pomerance_cuda.cu`. The target has
`p mod 8 = 3`, so the GPU path uses the `p == 3 mod 4` square-root branch.

The successful RunPod RTX 6000 Ada run found the triple on 2026-06-20 after
139.934292088B X1(16) curves:

```text
successful GPU trials              = 139.934292088B
sqrt_floor(p)                      = 10000.000000000B
fraction of sqrt_floor(p)          = 0.013993429
speedup vs sqrt-floor trials       = about 71.46x
observed GPU rate near success     = about 51.997M candidates/sec
wall time to hit                   = 2691.21 seconds
```

The run was explicitly capped at 550B candidates and stopped early at the hit.
Reproducibility artifacts are in `results/p26/`.

## CUDA GPU Search

`pomerance_cuda.cu` is a GPU-compatible port of the production
`x16halvenonsplit` path. It is intentionally narrow: the generic 2-Sylow
search and exploratory diagnostic modes remain in `pomerance.c`.

Compile on an Ada-generation NVIDIA GPU with:

```sh
nvcc -O3 -std=c++17 -arch=sm_89 -o pomerance_cuda pomerance_cuda.cu
```

Example p26 run:

```sh
./pomerance_cuda 100000000000000000000000067 121 550000000000 x16halvenonsplit 1000000000
```

The automatic backend uses a specialized 96-bit field path for `p < 2^96`,
which covers p23, p25, and p26, and falls back to the generic 128-bit path for
larger supported primes.

## p25 Result: X1(16) Nonsplit Search

For

```text
p = 10000000000000000000000013 = 10^25 + 13
```

the run found the triple:

```text
10000000000000000000000013 5863342488035851054212447 9636258147581954669181726
```

Equivalently:

```text
p  = 10000000000000000000000013
A  = 5863342488035851054212447
x0 = 9636258147581954669181726
```

The p25 hit used the same practical family that worked for p23 and Jane Shi's
p24 result: Sutherland `X1(16)` prescribed torsion, a y-level nonsplit
Montgomery discriminant filter, and first-branch successive halving. The p25
target has `p mod 8 = 5`, so it did not need the p24 square-root patch for the
`p mod 8 = 7` case.

The successful 10-worker `x16halvenonsplit` run found the triple on
2026-06-18 at 02:32:33 PDT. The winning worker reported about 19.63B local
accepted candidates; reconstructing the aggregate across workers gives about
196.34B accepted candidates at the hit:

```text
successful run accepted trials       = 196.343915922B
sqrt_floor(p)                        = 3162.277660168B
fraction of sqrt_floor(p)            = 0.062089398
speedup vs sqrt-floor trials         = about 16.11x
```

Including an earlier partial no-hit production chunk that stopped without a
clean exhausted marker gives the full p25 practical campaign accounting:

```text
prior partial chunk accepted trials  = 266.467000000B
successful run accepted trials       = 196.343915922B
total campaign accepted trials       = 462.810915922B
fraction of sqrt_floor(p)            = 0.146353662
speedup vs sqrt-floor trials         = about 6.83x
```

Interpretation: the p25 result is another strong fixed-prime practical win
over the sqrt-scale search yardstick. The certificate came from the practical
`X1(16)` nonsplit/halving fleet; the parallel theorem-side research did not
produce the winning shortcut, but it substantially narrowed what a future
moonshot would need to prove.

Reproducibility artifacts are in `results/p25/`:

- `triple.txt`
- `p25-success-summary.txt`
- `p25-verification.txt`
- `p25-worker08-tail.txt`
- `pomerance_10000000000000000000000013.lean`

## p23 Result: X1(16) Nonsplit Search

For

```text
p = 100000000000000000000117 = 10^23 + 117
```

the run found the triple:

```text
100000000000000000000117 24163028207499560363686 64911014007772963770218
```

Equivalently:

```text
p  = 100000000000000000000117
A  = 24163028207499560363686
x0 = 64911014007772963770218
```

The successful method was a y-filtered nonsplit `X1(16)` first-branch halving
search:

1. sample curves from Sutherland's `X1(16)` prescribed-torsion construction;
2. map them to Montgomery form with a marked rational point of order 16;
3. pre-filter the `X1(16)` y-parameter to the nonsplit Montgomery
   discriminant class;
4. use first-branch successive halving in the cyclic nonsplit rational
   2-Sylow case.

The key y-level classifier used by the production run was:

```text
chi(A^2 - 4) = chi((y^2 - 2)(y^2 - 4y + 2)).
```

The final nonsplit shard found the triple after about 31.05B aggregate
accepted trials in just over 8 hours:

```text
successful shard trials       = 31.046588500B
sqrt_floor(p)                 = 316.227766016B
fraction of sqrt_floor(p)     = 0.098177933
speedup vs sqrt-floor trials  = about 10.19x
```

The full p23 discovery campaign also included an earlier all-`X1(16)` shard
that ran 50B aggregate accepted trials and missed. Charging that miss to the
campaign gives:

```text
full campaign trials          = 81.046588500B
fraction of sqrt_floor(p)     = 0.256291816
speedup vs sqrt-floor trials  = about 3.90x
```

Interpretation: this is a substantial fixed-prime win over the sqrt-scale
search yardstick. It is best understood as a literature-backed constant-factor
strategy, not by itself as a proof of asymptotic sub-sqrt scaling.

Reproducibility artifacts are in `results/p23/`:

- `triple.txt`
- `p23-success-summary.txt`
- `p23-verification.txt`
- `p23-worker03-tail.txt`
- `pomerance_100000000000000000000117.lean`

A curated research ledger is in `research/p23/`. Related later-stage research
material is now also tracked in `research/p24/` and `research/p25/`. The
source file `pomerance.c` now includes the p23 experimental `X1(16)` modes and
many diagnostic modes used to test alternatives before the nonsplit route
graduated to production.

## p22 Result: 2-Sylow Projection Search

This fork records a verified Pomerance triple for `p = 10^22 + 9` and a
small Codex-assisted performance branch derived from Ruehle's 2-Sylow
projection search.

The run found the triple:

```text
10000000000000000000009 9992566338662824267458 3694769590833803032125
```

after 15.77 hours on the successful worker, with about 58.65 billion
aggregate observed trials across 10 workers. The observed rate near success was
about 1.03M trials/sec aggregate across those workers, not single-threaded. A
same-machine single-thread benchmark against fresh upstream is recorded in
`results/p22/p22-benchmark-comparison.txt`.

Reproducibility artifacts are in `results/p22/`:

- `p22-success-summary.txt`
- `p22-verification.txt`
- `p22-worker07-tail.txt`
- `p22-benchmark-comparison.txt`
- `pomerance_10000000000000000000009.lean`

## Iteration Process

I started this as a Codex-assisted exploration of the DANGER3 challenge: first to understand the search space and verification criteria, then to see whether a practical run for `p = 10^22 + 9` was plausible on the machine I had available. The broader exploration included some guided-search ideas, but this public handoff keeps only the reproducible p22 result and the local performance fork.

My main contributions were framing the run as an operational search problem: I had one dedicated machine, persistent `tmux` sessions, and Codex running GPT 5.5 available to inspect, modify, benchmark, and monitor the code over a long-running job. For `p = 10^22 + 9`, the basic search scale is `sqrt(p) ~= 100B` trials, and this program's conservative p22 budget was about `20*sqrt(p)/3 ~= 667B` trials. At an early observed aggregate rate around `0.95M` trials/sec, exhausting that budget would take about eight days, so I directed the effort toward increasing trials/sec rather than changing the mathematical search strategy. When the exploratory performance work showed a local lift of about 15%, I made the call that it was worth switching the production run to the optimized branch.

## Performance Engineering Optimizations

The changes made by GPT 5.5 were performance improvements inside the same 2-Sylow projection strategy:

- **Special-case the odd-parts pattern.** For this `p`, the valid odd parts are:

  ```text
  m, 2m + 1, 2m - 1
  ```

  Ruehle's generic loop does a scalar multiplication separately for each odd part. This fork reuses related Montgomery ladder computations so it avoids some repeated work.

- **Avoid expensive random `% p` reductions.** Upstream creates random 128-bit values and reduces them modulo `p`. `%` on `u128` can be costly, so this fork uses masked rejection sampling to generate values below `p`.

- **Stop the doubling check earlier.** Upstream checks up to `k + 10` doublings after projection. For this case, the possible 2-adic depths tell us we only need to check up to the actual maximum depth for each odd part, often `k` or `k + 1`.


## Workflow
The approach that worked was not a new asymptotic algorithm. It was to build directly on Ruehle's 2-Sylow projection search, benchmark it carefully, and then iterate on small constant-factor improvements in the hot loop. The practical loop was:

1. inspect the existing implementation and verifier assumptions;
2. estimate the run budget from observed trials/sec;
3. make the run shardable across independent single-thread workers;
4. add fixed-budget benchmarking so changes could be compared directly;
5. optimize the u128 search path for the p22 case;
6. launch 10 independent single-thread workers, each on a separate random stream, under persistent `tmux` supervision;
7. keep a transparent status/job-manager view of active workers, observed rates, elapsed time, and success criteria;
8. verify the triple with the DANGER3 verifier, primality checking, and an independent doubling replay.

The status workflow mattered because this was a long-running randomized computation. I needed to be able to answer, at any point, whether the workers were still alive, how many trials had been observed, what rate they were sustaining, whether any success condition had fired, and what evidence would count as "done."

The result is therefore best understood as Ruehle's search strategy plus a GPT 5.5 authored C performance fork, with Alexa directing the operating constraints, benchmark decisions, production-run management, and verification handoff. One iteration was enough to achieve this result, I suspect there are additional gains to be had with this approach.

# Hardware
Benchmarks and the p22 production run were performed on a Mac mini with an Apple M4 chip, 10 CPU cores (4 performance, 6 efficiency), and 16 GB memory, running macOS 26.5.

The original upstream README continues below.

# Pomerance Triple Search

A fast search algorithm for finding Pomerance triples $(p, A, x_0)$, developed for the [data challenge](https://github.com/AndrewVSutherland/DANGER3) at the [DANGER: Data, Numbers, and Geometry](https://www.birs.ca/events/2026/5-day-workshops/26w5525) workshop at BIRS, April 6–10, 2026.

The challenge was to find a Pomerance Triple for $10^19+51$, which was an order of magnitude larger than the known world record. The code found the triple
```
10000000000000000051 238792350205097889 9647351248508855176
```
after around 400 seconds and 3.8 billion tries.

## Background 

A **Pomerance triple** is a triple of integers $(p, A, x_0)$ where $p$ is an odd prime, $A$ and $x_0$ are nonneg integers less than $p$ with $A \not\equiv \pm 2 \pmod{p}$, such that doubling the projective point $(x_0 : 1)$ on the Montgomery curve $By^2 = x^3 + Ax^2 + x$ exactly $k$ times yields a $Z$-coordinate congruent to zero modulo $p$. Here $k$ is the least integer with $2^k > q + 1 + 2\lfloor\sqrt{q}\rfloor$, where $q = \lfloor\sqrt{p}\rfloor$.

The challenge is to find a Pomerance triple with $p$ as large as possible without exploiting supersingular curves or CM.

See Andrew Sutherland's [DANGER3 repository](https://github.com/AndrewVSutherland/DANGER3) for the full problem definition, verification scripts, and precomputed data.

The solution was vibe-coded with Claude Opus 4.6 with extended thinking. It took 12 iterations to get this working code. The initial challenge also asked to beat the $\sqrt{p}$-scaling, which this code does not achieve. It won the challenge via a very fast C implementation of the algorithm and using performance improvements like the 2-Sylow projection. 

## Algorithm

The search uses **2-Sylow projection** to achieve $O(1/\sqrt{p})$ success probability per random trial:

1. **Precompute candidate odd parts.** For each group order $N = 2^k m$ in the Hasse interval $[p+1-2\sqrt{p},\; p+1+2\sqrt{p}]$ with $2^k \mid N$, record the odd part $m$.
2. **Random search.** For each random $(A, x_0)$, compute the scalar multiple $[m](x_0 : 1)$ via the Montgomery ladder, projecting the point into the 2-Sylow subgroup of $E(\mathbb{F}_p)$.
3. **Doubling chain.** Double the projected point repeatedly. If $Z$ hits zero at step $k$, extract the affine $x$-coordinate and verify.

Without the projection step, the success probability would be $O(1/p)$ per trial (requiring $\sim p$ trials). The projection makes any point on a curve with the right group order work, reducing the search to $\sim\sqrt{p}$ trials.

## Building

Requires a C compiler with `__uint128_t` support (GCC or Clang on x86-64 / ARM64).

**Multi-threaded (recommended):**

```bash
gcc -O3 -fopenmp -o pomerance pomerance.c -lm
```

**Single-threaded:**

```bash
gcc -O3 -o pomerance pomerance.c -lm
```

**macOS (Homebrew GCC):**

```bash
brew install gcc
gcc-14 -O3 -fopenmp -o pomerance pomerance.c -lm
```

## Usage

```bash
./pomerance <prime> [seed_offset] [max_trials]
```

The argument is a decimal integer. If it is not prime, the program finds the next prime. The program automatically selects u64 arithmetic for $p < 2^{63}$ and u128 arithmetic for $p < 2^{127}$.

The optional `seed_offset` argument changes the PRNG stream, which is useful for sharded runs. The optional `max_trials` argument overrides the heuristic trial budget, which is useful for fixed-budget benchmarking.

**Examples:**

```bash
./pomerance 1000000000000037            # 16 digits, u64, ~seconds
./pomerance 10000000000000000051        # 20 digits, u64, ~minutes
./pomerance 1000000000000000000117      # 22 digits, u128, ~hours
```

**Output:** On success, the program prints the triple in the format expected by Sutherland's [`vpp.py`](https://github.com/AndrewVSutherland/DANGER3/blob/main/vpp.py) verifier:

```
p A x0
```

To verify a result:

```bash
python3 vpp.py p A x0
```

## Performance

The search requires $\sim\sqrt{p}$ random trials, each consisting of a Montgomery ladder scalar multiplication plus $k \approx \frac{1}{2}\log_2 p$ doublings.

| Target $p$ | Arithmetic | Trials/s (48 cores) | Expected time |
|---|---|---|---|
| $10^{15}$ | u64 | ~9M | <1s |
| $10^{19}$ | u64 | ~9M | ~1 min |
| $10^{20}$ | u128 | ~1M | ~1 hr |
| $10^{30}$ | u128 | ~1M | ~years |

For $p > 2^{127}$, a GMP-based implementation would be needed. On the other hand, $\sqrt{2^{127}}\approx10^{19}$, which would take 100,000 years.

## License

MIT
