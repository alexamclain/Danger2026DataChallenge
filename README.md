# DANGER3 p22 Pomerance Search Handoff

This fork records a verified Pomerance triple for `p = 10^22 + 9` and a
small Codex-assisted performance branch derived from Ruehle's 2-Sylow
projection search.

The goal of this run was to find a Pomerance triple for `p = 10^22 + 9`.
The run found the triple

```text
10000000000000000000009 9992566338662824267458 3694769590833803032125
```

after 56,761.05 seconds on the successful worker, with about 58.65 billion
aggregate observed trials across 10 workers. The observed rate near success was
about 1.03M trials/sec aggregate across those workers, not single-threaded. A
same-machine single-thread benchmark against fresh upstream is recorded in
`results/p22-benchmark-comparison.txt`.

Reproducibility artifacts are in `results/`:

- `p22-success-summary.txt`
- `p22-verification.txt`
- `p22-worker07-tail.txt`
- `p22-benchmark-comparison.txt`
- `pomerance_10000000000000000000009.lean`

## Iteration Process

I started this as a Codex-assisted exploration of the DANGER3 challenge: first to understand the search space and verification criteria, then to see whether a practical run for `p = 10^22 + 9` was plausible on the machine I had available. The broader exploration included some guided-search ideas, but this public handoff keeps only the reproducible p22 result and the local performance fork.

My main contributions were framing the run as an operational search problem: I had one dedicated machine, persistent `tmux` sessions, and Codex available to inspect, modify, benchmark, and monitor the code over a long-running job. For `p = 10^22 + 9`, the basic search scale is `sqrt(p) ~= 100B` trials, and this program's conservative p22 budget was about `20*sqrt(p)/3 ~= 667B` trials. At an early observed aggregate rate around `0.95M` trials/sec, exhausting that budget would take about eight days, so I directed the effort toward increasing trials/sec rather than changing the mathematical search strategy. When the exploratory performance work showed a local lift of about 15%, I made the call that it was worth switching the production run to the optimized branch.

The approach that worked was not a new asymptotic algorithm. It was to build directly on Ruehle's 2-Sylow projection search, benchmark it carefully, and then iterate on small constant-factor improvements in the hot loop. The practical loop was:

1. inspect the existing implementation and verifier assumptions;
2. estimate the run budget from observed trials/sec;
3. make the run shardable across independent single-thread workers;
4. add fixed-budget benchmarking so changes could be compared directly;
5. optimize the u128 search path for the p22 case;
6. launch 10 independent single-thread workers, each on a separate random stream, under persistent `tmux` supervision;
7. keep a transparent status/job-manager view of active workers, observed rates, elapsed time, and success criteria;
8. verify the triple with the DANGER3 verifier, primality checking, and an independent doubling replay.

The status workflow mattered because this was a long-running randomized computation. A human needed to be able to answer, at any point, whether the workers were still alive, how many trials had been observed, what rate they were sustaining, whether any success condition had fired, and what evidence would count as "done."

The result is therefore best understood as Ruehle's search strategy plus a small Codex-assisted C performance fork, with Alexa directing the operating constraints, benchmark decisions, production-run management, and verification handoff. It took 

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
