# Half-Level X0 Lift Sidecar

## Verdict

No-go for the proposed half-level `X0` shortcut, in the moduli-natural sense:
constructing `X0(2^h)` cyclic subgroup data with `h ~= 20` can give a cheap
stable 2-adic line, and in this congruence class it can even extend to deeper
`X0` data without a new density loss.  But it does not provide the missing
`X1`/x-only orientation.  Upgrading the half-level line to a strict DANGER3
point of order `2^40` requires the remaining `2^(40-h)` high bits of the
Frobenius eigenvalue `lambda = 1`; paying that tail brings the scale back to
`Theta(2^40) = Theta(sqrt(p))`.

For `p = 10^24 + 7`, `k = 40`, `h = 20`:

```text
[SL2(Z):Gamma0(2^20)] = 3*2^19 = 1,572,864 ~= 1.57*p^(1/4)
residual_tail = 2^(40-20) = 1,048,576
Gamma0(2^20)*residual_tail = 3*2^39 ~= 1.649*sqrt(p)
```

So the hoped-for `p^(1/4)` stage plus a free lift is not available; the lift is
the missing half of the square-root search.

The exact local tail count is recorded in:

```text
p24/x0_x1_tail_entropy_theorem.md
p24/x0_x1_tail_entropy_audit.py
```

Even if the half-level stage has already oriented the branch
`lambda == 1 mod 2^h`, there are `2^(k-h)` lifts to level `2^k` and only one
true `X1` lift.  For `h=20`, this is exactly `1048576` remaining choices.

## Frobenius equations

An `X0(2^h)` datum is an ordinary curve `E/F_p` plus a rational cyclic subgroup
`C_h` of order `2^h`.  On this subgroup Frobenius acts by an odd eigenvalue
`lambda mod 2^h`, and the other eigenvalue is `mu = p/lambda`.  Thus

```text
lambda*mu == p                         mod 2^h
t == lambda + mu == lambda + p/lambda  mod 2^h.
```

The verifier needs an x-only point of exact order `2^k`.  On the curve side,
this is the oriented condition

```text
lambda == 1 mod 2^k
```

or dually `mu == 1 mod 2^k`; on the twist side the same statement appears with
`-1`.  Equivalently, for the curve side,

```text
2^k | #E(F_p) = p + 1 - t,
```

with the split x-only adjustment already accounted for in the target traces.

For the DANGER residue `t == p+1 mod 2^a`, the `X0` eigenvalue equation factors:

```text
lambda^2 - (p+1)lambda + p == 0 mod 2^a
(lambda - 1)(lambda - p) == 0          mod 2^a.
```

Since `v2(p-1)=1`, this has four roots for `a >= 2`.  At `a = 20` they are:

```text
lambda  mu      v2(lambda-1)  v2(mu-1)
1       7       20            1
7       1       1             20
524289  524295  19            1
524295  524289  1             19
```

Only the first two are genuine level-20 `X1` orientations; the other two split
the 2-adic divisibility as `(19,1)` or `(1,19)`.  At `a = 40` the same pattern
is:

```text
lambda        mu             v2(lambda-1)  v2(mu-1)
1             1020608380935  40            1
1020608380935 1              1             40
549755813889  470852567047   39            1
470852567047  549755813889   1             39
```

Thus even the full `X0(2^40)` trace residue has non-`X1` orientations.  More
importantly for the half-level strategy, if a half-level oriented root is
written

```text
lambda = 1 + 2^h u mod 2^k,
```

then strict rational `2^k` torsion forces

```text
u == 0 mod 2^(k-h).
```

The half-level `X0` datum does not contain this `u` tail.  Recovering it is the
ray-orientation/X1 lift, not a byproduct of the cyclic subgroup.

## Why composing X0 chains does not help

Composing two rational cyclic `2^h` isogeny chains can at best move from
`X0(2^h)` data toward `X0(2^40)` data.  It still records a Frobenius-stable
line, not a generator fixed by Frobenius.  In 2-adic terms, it refines the line
on which Frobenius acts by some odd `lambda`; it does not force
`lambda == 1 mod 2^40`.

For this `p`, the local audits show that high-depth `X0` is not the scarce
condition anyway.  The image of

```text
lambda -> lambda + p/lambda mod 2^a
```

has size `2^(a-3)`, i.e. a constant `1/8` fraction of all trace residues, and
the small-field chain counts stabilize at `X0` density about `3/4` after depth
3.  What shrinks with depth is the oriented `X1`/x-only bucket.

The degree bookkeeping says the same thing.  If the first stage is
`X0(2^h)` and the second stage supplies only the missing high eigenvalue bits,
then even the generous lower-bound product is

```text
[SL2:Gamma0(2^h)] * 2^(k-h)
  = 3*2^(h-1) * 2^(k-h)
  = 3*2^(k-1)
  = [SL2:Gamma0(2^k)]
  = Theta(sqrt(p)).
```

If one instead first upgrades the half-level cyclic subgroup to a half-level
oriented generator, the orientation cover is

```text
phi(2^h)/2 = 2^(h-2),
```

and the remaining tail is still `2^(k-h)`, so the orientation part alone is

```text
2^(h-2) * 2^(k-h) = 2^(k-2) ~= 0.275*sqrt(p)
```

before accounting for how the curve/trace class was found.

## Light exact check

I reran the existing small exact audits without heavy enumeration:

```text
python3 p24/x0_orientation_audit.py
```

confirms the stable p24 pattern:

```text
a=20: X0 trace residues = 131072 / 1048576 = 0.125, target orientations = 4
a=40: X0 trace residues = 137438953472 / 1099511627776 = 0.125, target orientations = 4
```

and

```text
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py \
  --min-p 10000 --max-p 60000 --max-rows 3 --max-depth 12 --fit-min-depth 4
```

gives aggregate `X0` density fixed at about `0.749958` from depth 3 onward,
while the oriented `X1` density decays with depth:

```text
depth  x1_density   x0_density
4      0.37489515   0.74995806
8      0.03206144   0.74995806
12     0.00152851   0.74995806

aggregate_fitted_beta_x1 = 0.875625 on this tiny sample
aggregate_fitted_beta_x0 = 0.000000
```

The exact exponent estimate is noisy at these small fields, but the structural
signal is the desired one: `X0` depth is free because it omits orientation;
`X1` depth is where the bits are paid.

## Falsifiable lead

The only live lead in this shape would be a canonical selector on
`X0(2^h)` data that predicts the high tail `u` in

```text
lambda = 1 + 2^h u mod 2^k
```

with growing advantage over random, without itself being a degree
`2^(k-h)` ray-class/X1 function.  A small exact test would be:

1. enumerate small `p = n^2 + 7` rows;
2. condition on the curve or twist having an `X0(2^h)` chain and on the
   half-level DANGER residue;
3. scan candidate labels naturally attached to the chain, such as terminal
   `A' +/- 2`, quotient `j` values, low-degree characters of Velu/Landen
   branch parameters, or products along the chain;
4. measure whether the conditional probability of full `X1(2^k)` grows like a
   power of `2^(k-h)`.

The existing `x0_orientation_character_scan.py`, `ray_orientation_audit.py`,
`isogeny_chain_compression_audit.py`, and
`partial_oriented_sampler_exponent_audit.py` are negative for the visible
low-degree labels.  I do not see a concrete p24-compatible selector beyond
that falsification target.
