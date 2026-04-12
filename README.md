# Pomerance Triple Search

A fast search algorithm for finding [Pomerance triples](https://github.com/AndrewVSutherland/DANGER3) $(p, A, x_0)$, developed for the data challenge at the [DANGER: Data, Numbers, and Geometry](https://www.birs.ca/events/2026/5-day-workshops/26w5525) workshop at BIRS, April 6–10, 2026.

The challenge was to find a Pomerance Triple for $10^19+51$, which was an order of magnitude larger than the known world record. The code found the triple
```
10000000000000000051 238792350205097889 9647351248508855176
```
after around 400 seconds and 3.8 billion tries.

## Background 

A **Pomerance triple** is a triple of integers $(p, A, x_0)$ where $p$ is an odd prime, $A$ and $x_0$ are nonneg integers less than $p$ with $A \not\equiv \pm 2 \pmod{p}$, such that doubling the projective point $(x_0 : 1)$ on the Montgomery curve $By^2 = x^3 + Ax^2 + x$ exactly $k$ times yields a $Z$-coordinate congruent to zero modulo $p$. Here $k$ is the least integer with $2^k > q + 1 + 2\lfloor\sqrt{q}\rfloor$, where $q = \lfloor\sqrt{p}\rfloor$.

The challenge is to find a Pomerance triple with $p$ as large as possible without exploiting supersingular curves or CM.

See Andrew Sutherland's [DANGER3 repository](https://github.com/AndrewVSutherland/DANGER3) for the full problem definition, verification scripts, and precomputed data.

The solution was vibe-coded with Claude Opus 4.6 with extended thinking. It took 12 iterations to get this working code. The initial challenge asked to beat the $\sqrt{p}$-scaling, which this code does not achieve. It won the challenge via a very fast C implementation of the algorithm and using small tricks like the 2-Sylow projection. 

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
./pomerance <prime>
```

The argument is a decimal integer. If it is not prime, the program finds the next prime. The program automatically selects u64 arithmetic for $p < 2^{63}$ and u128 arithmetic for $p < 2^{127}$.

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
| $10^{15}$ | u64 | ~8M | <1s |
| $10^{19}$ | u64 | ~8M | ~1 min |
| $10^{20}$ | u128 | ~1M | ~1 hr |
| $10^{30}$ | u128 | ~1M | ~years |

For $p > 2^{127}$, a GMP-based implementation would be needed.

## License

MIT
