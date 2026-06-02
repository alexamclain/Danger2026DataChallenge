# Prescribed-Torsion Scaling Barrier

Date: 2026-06-02 PDT

Purpose: decide whether generic prescribed torsion from the standard modular
curve literature can become a true sub-sqrt scaling method, or whether it is
only a fixed-p constant-factor tactic unless a special tower/trace primitive is
found.

## Short Conclusion

Generic `X1(N)` prescribed torsion is not the asymptotic path.

```text
fixed N        -> constant-factor density improvement only
growing N      -> needs N to grow with p
generic X1(N)  -> sampling degree/gonality grows roughly like N^2
density gain   -> roughly N
```

So a direct one-parameter `X1(N)` sampler loses asymptotically if `N` is grown
by standard plane-model root finding. This does not invalidate the active p23
run. It says the current `X1(16)`/nonsplit strategy is a credible practical
p23 constant-factor improvement, while a real scaling story must use a
non-generic primitive:

```text
1. a cheap section of the X1(2^m) tower;
2. a curve-level trace-v2 / volcano-altimeter label;
3. an exact trace-residue/root-squareclass pullback.
```

## Literature Anchors

Sutherland constructs optimized equations for `X1(N)` and applies them over
finite fields to generate elliptic curves with prescribed torsion:

```text
Andrew V. Sutherland,
"Constructing elliptic curves over finite fields with prescribed torsion",
Mathematics of Computation 81 (2012), 1131-1147.
https://arxiv.org/abs/0811.0296
```

The same line of work is represented by Sutherland's `X1(N)` equation tables:

```text
https://math.mit.edu/~drew/X1_altcurves.html
https://math.mit.edu/~drew/X1_optcurves.html
```

Those tables list birational plane equations and low-degree maps to `P^1`.
They are not arbitrary bad coordinates; the optimized table says the maps
match the Derickx-van Hoeij gonality upper bounds for `N <= 40`.

Gonality references:

```text
Dan Abramovich,
"A linear lower bound on the gonality of modular curves",
https://arxiv.org/abs/alg-geom/9609012

Maarten Derickx and Mark van Hoeij,
"Gonality of the modular curve X1(N)",
Journal of Algebra 417 (2014), 52-71.
https://arxiv.org/abs/1307.5719

Mark van Hoeij and Hanson Smith,
"A Divisor Formula and a Bound on the Q-gonality of the Modular Curve X1(N)",
https://arxiv.org/abs/2004.13644
```

## Scaling Calculation

For the p23 search, the rare event is:

```text
v2(#E(Fp)) >= 39
```

Sampling from `X1(2^a)` forces a rational point of order `2^a`. Under the
trace-equidistribution heuristic, this buys about a `2^a` density factor
versus unconstrained random curves. This is why fixed `X1(16)` is useful.

But for asymptotic sub-sqrt scaling, a fixed `a` is insufficient:

```text
sqrt(p) / 2^a = still Theta(sqrt(p))
```

To improve the exponent, the prescribed level must grow:

```text
2^a ~= p^epsilon
```

Let:

```text
N = 2^a
```

The standard index formula gives:

```text
[SL2(Z) : Gamma1(N)] = N^2 * product_{ell|N}(1 - ell^-2)
```

For `N = 2^a` this is:

```text
[SL2(Z) : Gamma1(2^a)] = (3/4) * N^2
```

Abramovich's theorem gives gonality bounded below linearly in modular-curve
index. Thus, for `X1(2^a)`:

```text
gonality(X1(2^a)) = Omega(N^2)
```

This means there is no bounded-degree or merely linear-degree rational
parameter that samples arbitrary growing `X1(2^a)` points.

If a generic one-parameter sampler fixes a coordinate and solves the fiber,
its fiber degree is governed by this same growth. The density gain is about
`N`, while the generic fiber/rootfinding burden grows like `N^2`. Net:

```text
generic prescribed-torsion ladder worsens as N grows
```

## Local Degree Evidence

Sutherland's `X1_altcurves` table shows the first visible rungs:

```text
N     deg_x   deg_y
16       2       3
24       5       6
32      11      10
48      22      19
64      42      40
128    168     161
```

The power-of-two rows are especially telling:

```text
X1(32):  degree_y = 10
X1(64):  degree_y = 40
X1(128): degree_y = 161
```

After `N=32`, doubling `N` roughly quadruples the map degree. This is the
expected `N^2` shape, and it is consistent with the gonality barrier rather
than a removable implementation accident.

## Local Cost Evidence

### X1(16)

`X1(16)` is cheap because the local model reduces to a quadratic/discriminant
sampler. The active nonsplit p23 workers run at roughly:

```text
0.108M accepted trials/s per worker
1.080M accepted trials/s aggregate
```

### First X1(16) -> X1(32) gate

The first lift condition is:

```text
H(y) = (y - 1)(y^2 - 2)(y^2 - 2y + 2)
```

The cover `z^2 = H(y)` is genus 2 over p23. Direct d-gate variants were
production-negative:

```text
plain nonsplit       ~= 0.1165M/s
nonsplit + d-gate    ~= 0.0665M/s
d-gate-skip variant  ~= 0.0653M/s
```

So even the first special lift did not cheaply capture the next rung.

Backing note:

```text
notes/x16_first_d_y_gate_20260601.md
```

### Generic X1(32)

The p23 C root-existence cost floor for Sutherland's `FFFc32` model:

```text
samples = 5000 random x-fibers
fiber_rate = 1854.779/s = 0.001854779M/s
root_fibers = 3111/5000 = 0.622200
root_gcd_seconds_per_fiber = 5.368e-4
```

Compared with one active nonsplit worker:

```text
0.108M/s / 0.001855M/s ~= 58x
```

This is root-existence only. A full sampler still has to extract roots, map to
Tate normal form, convert the marked point to Montgomery coordinates, filter,
and run the halving chain.

Backing note:

```text
notes/x1_32_c_rootbench_20260602.md
```

### X1(24) -> order48

`X1(24)` plus a half-step can stack rational 3-torsion and 2-power torsion,
but it still needs degree-6 finite-field rootfinding and a quartic half test.
The holdouts showed at most a modest per-candidate lift:

```text
ideal odd-trace lift <= 1.5x
optimistic total hazard lift versus active nonsplit ~= 2x to 4x
```

To compete, the sampler would need to run at roughly 25% to 50% of the active
nonsplit accepted-candidate rate, which is implausible under the current
generic-rootfinding path.

Backing note:

```text
notes/x1_24_order48_trace_torsion_probe_20260601.md
```

## What This Rules Out

Ruled out as a route to asymptotic improvement:

```text
generic direct X1(2^a) sampling by optimized plane-model fiber rootfinding
```

Ruled out as the next p23 production shard:

```text
generic X1(32)
generic X1(24)->order48
generic X1(48)
```

Reason:

```text
the fixed-level density gain is real but too small to pay the generic
rootfinding cost; the growing-level generic ladder has the wrong asymptotic
cost shape.
```

## What Remains Alive

The barrier is not a theorem against all higher-torsion methods. It is a
barrier against generic one-parameter `X1(N)` sampling.

Still alive:

```text
1. Special 2-power tower section
   A recursive or biased finite-field procedure that samples deeper
   `X1(2^a)` levels using only cheap square-root-level operations and without
   carrying an exponential halving frontier.

2. Trace-v2 / volcano-altimeter selector
   A curve-level label that predicts `v2(#E(Fp))` cheaply enough to filter
   X1(16) or X0(32) samples before deep halving.

3. Exact trace-residue/root-squareclass pullback
   A low-degree exact predicate that keeps the p23 target trace residues and
   rejects non-target residues without generic point counting.
```

The active nonsplit result actually sharpens the second direction:

```text
inside nonsplit X1(16), marked-point depth = v2(#E(Fp))
```

So the missing production-positive mathematical object is now very concrete:

```text
a cheap exact or high-capture label for high curve-level v2(#E)
```

## Operational Decision

No production change.

```text
keep active y-filtered nonsplit X1(16) running while decision=keep_waiting
if hit, independently verify
if clean 50B miss, launch guarded direct-y nonsplit follow-on
do not launch generic X1(32), X1(24), or X1(48)
```

This closes the "maybe generic prescribed torsion will scale" question, but it
keeps the special tower/trace-selector questions open.
