# X1(16) Nonsplit Depth Equals v2 Audit

Date: 2026-06-02 PDT

Purpose: sharpen the active nonsplit probability model.

The open question was:

```text
Do the p23 depth-12 to depth-20 nonsplit lift diagnostics say something about
true depth 39, or could they be an artifact of branch selection at shallow
depth?
```

Short answer:

```text
In the nonsplit X1(16) family, marked-point halving depth is exactly
v2(#E(Fp)). The branch-selection uncertainty is gone. The remaining uncertainty
is the curve-level high-v2 trace tail.
```

## Group-Theoretic Statement

For a Montgomery curve:

```text
E_A: v^2 = u^3 + A*u^2 + u
```

the point `(0,0)` is always a rational point of order 2. The other nonzero
2-torsion points are rational iff:

```text
A^2 - 4
```

is a square. Thus in the nonsplit case:

```text
chi(A^2 - 4) = -1
```

there is exactly one nonzero rational point of order 2, so the rational
2-Sylow subgroup is cyclic:

```text
E(Fp)[2^\infty] ~= C_{2^m}
```

where:

```text
m = v2(#E(Fp)).
```

The X1(16) sampler marks a point `P` of exact order 16. In a cyclic group
`C_{2^m}`, every exact order-16 point has the form:

```text
P = a * 2^(m-4) * G
```

for a generator `G` and odd `a`.

The equation:

```text
2^r Q = P
```

has a rational solution iff:

```text
r <= m - 4.
```

Therefore the largest marked-point depth reachable by rational halving is:

```text
4 + (m - 4) = m = v2(#E(Fp)).
```

Because the 2-Sylow is cyclic, any rational half of a rational point has the
same remaining divisibility depth. Thus first-branch halving and all-branch
halving have the same survival event in the nonsplit family.

## Exact Enumeration Helper

Added:

```text
scripts/x16_nonsplit_depth_equals_v2.py
```

The helper:

```text
1. enumerates the full accepted X1(16) marked-point stream over a small prime;
2. computes A(y) and both marked xP roots;
3. brute-counts #E(Fp) for each unique A;
4. computes v2(#E(Fp));
5. runs first-branch rational halving from the marked point;
6. reports depth-vs-v2 mismatches by split class.
```

Compile check:

```bash
python3 -m py_compile scripts/x16_nonsplit_depth_equals_v2.py
```

Status:

```text
PASS
```

## p = 3037

Command:

```bash
nice -n 19 python3 scripts/x16_nonsplit_depth_equals_v2.py \
  --p 3037 \
  --target-depth 16 \
  | tee runs/x16_nonsplit_depth_equals_v2_20260602/p3037_depth16.log
```

Result:

```text
rows = 3000
trace_cache_size = 521
split_class_counts = nonsplit:1528, split:1472
mismatches_depth_ne_v2 = nonsplit:0, split:1472
```

Nonsplit depth-v2 histogram:

```text
nonsplit depth=4  v2=4:  776
nonsplit depth=5  v2=5:  392
nonsplit depth=6  v2=6:  192
nonsplit depth=7  v2=7:   72
nonsplit depth=10 v2=10:  96
```

Split rows all had depth different from curve-level v2, as expected:

```text
split slack = v2 - depth ranges from 1 to 6
```

## p = 10357

Command:

```bash
nice -n 19 python3 scripts/x16_nonsplit_depth_equals_v2.py \
  --p 10357 \
  --target-depth 16 \
  | tee runs/x16_nonsplit_depth_equals_v2_20260602/p10357_depth16.log
```

Result:

```text
rows = 10504
trace_cache_size = 1795
split_class_counts = nonsplit:5216, split:5288
mismatches_depth_ne_v2 = nonsplit:0, split:5288
```

Nonsplit depth-v2 histogram:

```text
nonsplit depth=4  v2=4:  2648
nonsplit depth=5  v2=5:  1208
nonsplit depth=6  v2=6:   496
nonsplit depth=7  v2=7:   336
nonsplit depth=8  v2=8:   216
nonsplit depth=11 v2=11:  312
```

Again, every split row mismatched curve-level v2 because split curves have
non-cyclic rational 2-primary structure and the marked point can sit in a
less useful component.

## Interpretation For p23

This audit upgrades the active nonsplit model:

```text
The active nonsplit first-branch search is testing the event

  v2(#E(Fp)) >= 39

inside the X1(16) nonsplit family.
```

It is not merely testing a branch heuristic whose behavior might diverge after
depth 20. In the nonsplit family:

```text
depth_d survival  <=>  v2(#E(Fp)) >= d
```

for every depth `d`, including `d=39`.

What remains uncertain:

```text
the distribution of v2(#E(Fp)) at p23 inside the nonsplit X1(16) family.
```

The p23 depth-12/depth-14 branchstats are therefore estimates of the
curve-level high-v2 tail in the actual p23 family. They are not exact evidence
for the depth-39 tail, but they are measuring the right event.

## Operational Decision

Keep the active run:

```text
runs/p23_x16halvenonsplit_20260601_201436
```

No production change:

```text
Do not switch to all-branch halving.
Do not add branch selectors inside nonsplit.
Do not restart or hot-swap the active workers.
```

Probability-language update:

```text
When discussing nonsplit lift, say that branch-loss uncertainty is ruled out
by the cyclic 2-Sylow argument. The remaining prior uncertainty is trace/high
v2-tail calibration at p23.
```
