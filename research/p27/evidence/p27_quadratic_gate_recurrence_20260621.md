# P27 Quadratic Gate Recurrence

Date: 2026-06-21

## Claim

The selected p27 halving tower has a simple repeated quadratic gate.

Once the path is in the all-plus square-root stratum, write:

```text
A = 2 - c^2
x = r^2
```

Then the next selected x-square gate is exactly:

```text
next_gate = chi(r^2 + c*r + 1)
```

The signs of `c` and `r` do not matter in the tested selected tower: all four
sign choices give the same squareclass.

Equivalently, each next gate is the conic condition:

```text
h^2 = r^2 + c*r + 1.
```

This is the first genuinely source-shaped recurrence found in the p27 work.
It does not by itself give the final certificate, but it gives a concrete
candidate for beating sqrt: source or parametrize a long chain of these conic
conditions while preserving the pullback to the legal X1(16)/compactD source.

## Artifacts

Pair resolvent probe:

```text
research/p27/archive/gates/p27_smap_pair_resolvent_probe.py
research/p27/archive/probe_outputs/p27_smap_pair_resolvent_probe_20260621.txt
```

Multi-gate recurrence probe:

```text
research/p27/archive/gates/p27_quadratic_gate_recurrence_probe.py
research/p27/archive/probe_outputs/p27_quadratic_gate_recurrence_probe_20260621.txt
```

Commands:

```bash
PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_smap_pair_resolvent_probe.py \
  --target 12000 \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_smap_pair_resolvent_probe_20260621.txt

PYTHONDONTWRITEBYTECODE=1 \
python3 -u research/p27/archive/gates/p27_quadratic_gate_recurrence_probe.py \
  --target 12000 \
  --max-gates 8 \
  --small-primes 1607,1847,2087 \
  | tee research/p27/archive/probe_outputs/p27_quadratic_gate_recurrence_probe_20260621.txt
```

## Derivation

From the S-map quartic, pair the roots using the square roots already present
after a successful gate:

```text
S^2 = x + 1/x + 2
E^2 = S^2 - 4
M = 2*S*E
```

One quadratic factor has:

```text
Y^2 + a1*Y + B
a1 = -2*S^2 + M.
```

For a quadratic pair with square product `B`, the common root squareclass is:

```text
chi(-a1 + 2*sqrt(B)).
```

In the natural variable `x=r^2`, this simplifies to:

```text
a1 = -4*(x + 1)/x
B  = -4*(A - 2)/x = 4*(2 - A)/x.
```

With `c^2=2-A` and `x=r^2`, this gives:

```text
chi(-a1 + 2*sqrt(B))
  = chi(r^2 + c*r + 1).
```

Thus the quartic root-squareclass is not opaque: it is the quadratic character
of a conic expression in the square-root coordinate.

## Results

Pair-resolvent screen:

```text
p27 train:
  rows = 6048
  sign_independent_resolvent = 6048
  B_square = 24192
  resolvent_matches_d4 = 6048

p27 heldout:
  rows = 6088
  sign_independent_resolvent = 6088
  B_square = 24352
  resolvent_matches_d4 = 6088

q1607/q1847/q2087:
  match_rate = 1.000000000 for every field
```

Multi-gate p27 train:

```text
gate3 rows = 12000, matches = 12000
gate4 rows = 6048,  matches = 6048
gate5 rows = 3032,  matches = 3032
gate6 rows = 1542,  matches = 1542
gate7 rows = 748,   matches = 748
gate8 rows = 390,   matches = 390
```

Multi-gate p27 heldout:

```text
gate3 rows = 12000, matches = 12000
gate4 rows = 6088,  matches = 6088
gate5 rows = 2986,  matches = 2986
gate6 rows = 1510,  matches = 1510
gate7 rows = 726,   matches = 726
gate8 rows = 342,   matches = 342
```

Promotion guard fields:

```text
q1607:
  gate3 rows = 784, matches = 784
  gate4 rows = 448, matches = 448

q1847:
  gate3 rows = 1008, matches = 1008
  gate4 rows = 720,  matches = 720

q2087:
  gate3 rows = 912, matches = 912
  gate4 rows = 400, matches = 400
```

All tested rows were sign-independent.

## Interpretation

Positive:

```text
The selected tower no longer looks like unrelated quartic root tests.
After A=2-c^2 and x=r^2, every next gate is the same conic character
chi(r^2+c*r+1).

This is a plausible source route: choose or parametrize chains satisfying
h_j^2 = r_j^2 + c*r_j + 1, then test whether the pullback to the legal
X1(16)/compactD starting surface has low enough complexity.
```

Still missing:

```text
The formula predicts the next gate but does not yet give r_next as a rational
function of c,r,h.
The legal X1(16)/compactD pullback has not been parametrized in the c/r/h
coordinates.
No production sampler has been implemented or benchmarked from this recurrence.
```

## Concrete Next Tests

```text
1. Derive the step map from (c,r,h) to a valid next square-root coordinate
   r_next, or prove that it still requires a fresh independent double cover.

2. Build a CAS fixture for the legal source pullback with A=2-c^2 and one or
   two conic gates h_j^2=r_j^2+c*r_j+1; compute dimension/genus/components.

3. Ask GPU agent for a bounded A/B only after the formula is implemented:
   compare normal halving-prefix evaluation against the quadratic-gate precheck
   using c=sqrt(2-A), r=sqrt(x), and chi(r^2+c*r+1).
```

## Continue / Kill

```text
continue = conic-chain source/pullback test
continue = derive r_next recurrence in c/r/h coordinates
continue = bounded GPU precheck only as cost telemetry

kill = treating the formula alone as sqrt-beating without a source/chain
kill = more quartic named-factor products for this gate
kill = broad coefficient searches not using A=2-c^2, x=r^2
```

```text
p27_quadratic_gate_recurrence_rows=1/1
```
