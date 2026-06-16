# Lane A: p25 CM/Lang Transfer Check

Date: 2026-06-12

## Files inspected

- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_HANDOFF_INDEX_20260607.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_DREW_SUTHERLAND_ASK_MEMO.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_FRESH_EYES_SYNTHESIS_20260607.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_GLOBAL_SYNTHESIS_HANDOFF.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/00_THEOREM_ATTEMPTS_LEDGER.md`
- `/Users/agent/Documents/Codex/Danger2026DataChallenge/p24/strict_danger3_frontier.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/README.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/RESULT.md`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/LATEST_P25_RUN.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_084611/pids.txt`
- `/Users/agent/Documents/Codex/pomerance-p25-run/runs/p25_x16hn_20260612_084611/watch.log`

No worker logs were modified and no fleet process was touched.

## p24 transfer signature

p24's selected CM/Lang/Jacobi surface is not just "CM with smooth class
number".  The useful signature was:

```text
h = 2 * 157 * 211 * 3107441
m = 2 * 157 * 211
n = 3107441
ord_m(p) = 5460
ord_n(p) = 388430
gcd = 70
relative degree = ord_n/gcd = 5549 = 31 * 179
raw quotient = 7 * 31 * 179
post Tr_{B/C} packet = C_7 x C_179
W_axis dimension = 368 < 5549
```

That is the object behind the rank-621 admissible Jacobi span, the
degenerate-anchor correction, and the Moore/W_axis p-unit microscope.

## p25 trace facts

Computed with `sympy` plus `cypari2` `qfbclassno`/`quadclassunit`.  Here
`h` means the fundamental class number `h(D_K)`, matching the p24 convention;
all three p25 rows have order conductor `f=4`, and the ring-class number at
that conductor is `2*h`.

```text
p = 10000000000000000000000013
sqrt_floor = 3162277660168
k = 42
```

| trace t | v2(p+1-t) | D_K, f | h(D_K) factorization | class group | largest-prime split facts |
|---:|---:|---|---|---|---|
| 5808037298190 | 42 | `D_K=-391668921427112813920247`, `f=4` | `453621311724 = 2^2*3*7*17^2*37*505027` | `C_226810655862 x C_2` | `m=898212`, `n=505027`; `ord_m=816`, `ord_n=252513=3^2*28057`, `gcd=3`, `rel=84171=3*28057` |
| 1409990787086 | 50 | `D_K=-2375745373770787638476791`, `f=4` | `1198636371592 = 2^3*11*13620867859` | `C_299659092898 x C_2 x C_2` | `m=88`, `n=13620867859`; `ord_m=2`, `ord_n=6810433929=3^2*13*19*23*133201`, `gcd=1`, `rel=6810433929` |
| -2988055724018 | 42 | `D_K=-1941970186885204113620983`, `f=4` | `499836054144 = 2^7*3*7*17*107*151*677` | `C_62479506768 x C_2^3` | `m=738310272`, `n=677`; `ord_m=127200=2^5*3*5^2*53`, `ord_n=169=13^2`, `gcd=1`, `rel=169` |

Extra order facts:

```text
t=5808037298190:
  ord_7(p)=3, ord_17(p)=16, ord_37(p)=12, ord_505027(p)=252513=(505027-1)/2

t=1409990787086:
  ord_11(p)=1, ord_13620867859(p)=6810433929=(13620867859-1)/2

t=-2988055724018:
  ord_7(p)=3, ord_17(p)=16, ord_107(p)=106,
  ord_151(p)=75=(151-1)/2, ord_677(p)=169=(677-1)/4
```

## Transfer verdict

No p24-style selected `C_7 x C_179` CM/Lang/Jacobi producer surface appears
transferable to these three p25 traces.

Concrete blockers:

- Enumerating all `h=m*n` divisor splits for the three p25 class numbers gives
  zero splits with `7 | ord_n(p)/gcd(ord_m(p),ord_n(p))`; the p24 right
  `C_7` quotient is absent.
- The first trace has a half-order large class prime `505027`, but the natural
  relative degree is `84171 = 3*28057`, not `31*179` and not a small
  `C_7 x C_c` Jacobi packet.
- The second trace is dominated by one large half-order prime
  `13620867859`; the split is essentially `m=88` and a huge relative degree,
  with no `157/211`-style selected phase surface.
- The third trace is the only smooth-looking row, but the natural largest
  split gives `rel=169=13^2`.  That is a different cyclic-degree-169 object,
  not the p24 `C_7 x C_c` surface.  The natural W-axis analogue using
  factors `2,3,7,17,107,151` has dimension at least
  `1+1+2+6+16+106+150 = 282`, already larger than the degree-169 factor, so
  the one-factor Moore injectivity route is dead for that split.

## First falsifier / next command

Fast falsifier for literal p24 transfer:

```sh
python3 - <<'PY'
from sympy import divisors, factorint, n_order
from math import gcd
p = 10**25 + 13
Hs = {
    "t=5808037298190": 453621311724,
    "t=1409990787086": 1198636371592,
    "t=-2988055724018": 499836054144,
}
for tag, h in Hs.items():
    hits = []
    for n in divisors(h):
        if n in (1, h):
            continue
        m = h // n
        om = n_order(p % m, m)
        on = n_order(p % n, n)
        rel = on // gcd(om, on)
        if rel % 7 == 0:
            hits.append((n, m, rel, factorint(rel)))
    print(tag, "relative_rel_divisible_by_7_count=", len(hits), "first_hits=", hits[:3])
PY
```

Observed output: count `0` for all three traces.

If someone still wants a positive p25-specific CM side quest, the only narrow
candidate is the third trace's `n=677`, `rel=169` cyclic quotient.  That would
need a new `C_169` or `13^2` finite identity, not a p24 transfer.  Do not spend
main run CPU on it.

## Recommendation

Kill Lane A as a p24 CM/Lang/Jacobi transfer for the p25 run.  Continue the
main strict search fleet; keep only a low-priority paper note for the third
trace's degree-169 quotient if the run needs postmortem ideas.
