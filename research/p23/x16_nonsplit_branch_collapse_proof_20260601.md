# X1(16) Nonsplit Branch-Collapse Proof

Generated locally: 2026-06-01

Purpose: explain the repeated p23 diagnostic observation:

```text
y-filtered nonsplit X1(16): first_survive = all_survive
```

This is not merely a sampling accident through the tested depths. It follows
from the group structure of nonsplit Montgomery curves.

## Montgomery Split Class

For the Montgomery curve

```text
E_A: v^2 = u^3 + A*u^2 + u
```

the nonzero rational point `(0,0)` is always a point of order 2. The other
nonzero 2-torsion points are the roots of:

```text
u^2 + A*u + 1 = 0
```

Thus:

```text
split    iff A^2 - 4 is square     => E[2](Fp) has rank 2
nonsplit iff A^2 - 4 is nonsquare  => E[2](Fp) = {O, T}
```

where `T = (0,0)`.

Any finite abelian 2-group with exactly one nonzero element of order 2 is
cyclic. Therefore the rational 2-Sylow subgroup of a nonsplit Montgomery curve
is cyclic.

## Halving Fibers In The Nonsplit Case

Let `H` be the rational 2-Sylow subgroup. In the nonsplit case:

```text
H ~= C_{2^m}
```

for some `m`, and `T` is the unique element of order 2.

If a rational point `Q` has a rational half, then the rational halves differ by
the rational 2-torsion point `T`. In Montgomery `u`-coordinates, adding `T`
sends:

```text
u -> 1/u
```

because the line through `(u,v)` and `(0,0)` has slope `v/u`, and the third
intersection has x-coordinate `1/u`.

So a successful x-only halving step in the nonsplit case produces exactly the
reciprocal pair of child x-coordinates:

```text
u_child and 1/u_child
```

## Future Divisibility Is Branch-Independent

The key cyclic-group fact:

```text
If Q has r future rational halvings in a cyclic 2-group, then every rational
half of Q has r-1 future rational halvings.
```

Proof sketch:

Take a cyclic generator `G` of `H`. If `Q` has `r` future halvings, then

```text
Q = 2^r*S
```

for some rational `S` in `H`. Let `R` be any rational half of `Q`. Then:

```text
2*R = Q = 2*(2^{r-1}*S)
```

so

```text
R - 2^{r-1}*S
```

is rational 2-torsion. In the nonsplit case this difference is either `O` or
`T`. Since `H` is cyclic and `Q` has `r` future halvings, the group exponent is
large enough that `T` is also divisible by `2^{r-1}`. Therefore `R` is
divisible by `2^{r-1}`.

So all rational halves of `Q` have the same future halving depth. Choosing
the "first" rational half cannot lose a future-valid path in the nonsplit
family.

## Diagnostic Consequence

For y-filtered nonsplit X1(16) samples:

```text
first_branch_survives_to_depth_d  iff  some_branch_survives_to_depth_d
```

and for surviving curves the all-branch frontier grows as exact powers of two
in x-coordinates until it reaches the tested cap or the top of the 2-Sylow
chain.

This explains the fresh p23 depth-20 holdout:

```text
notes/x16_nonsplit_branch_depth20_holdout_20260601.md

two paired 100k-seed p23 nonsplit diagnostics:
  first_survive = all_survive at every logged depth through 20
  all-branch frontier sizes = 2, 4, 8, ..., 65536
```

## Operational Consequence

This strengthens the current production choice:

```text
keep the active y-filtered nonsplit X1(16) first-branch shard running
```

It also rules out a class of tempting follow-ups:

```text
Within the nonsplit family, full all-branch halving and branch-selection
heuristics cannot improve survival over first-branch halving. They only add
cost, unless the sampler leaves the nonsplit/cyclic 2-Sylow setting or the
goal changes to a different curve family.
```

The remaining ways to improve the active search are therefore not local branch
selectors. They are:

```text
1. better filtering for traces or deeper 2-adic structure before halving,
2. a cheaper way to sample higher prescribed 2-power torsion,
3. a faster nonsplit/X1(16) sampling kernel,
4. or a different literature-backed family with materially higher target
   hazard per unit time.
```
