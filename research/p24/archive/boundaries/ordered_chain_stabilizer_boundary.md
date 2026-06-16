# Ordered Chain Stabilizer Boundary

This note closes a subtle variant of the composite target:

```text
Maybe plain X0(206498) loses the sign of 2 * 463 * 223^(-1), but an ordered
chain of 2-, 223-, and 463-isogenies could retain the orientation cheaply and
therefore expose the degree-66254 quotient.
```

The ordered chain does retain the sign data.  It still does not apply the
subgroup projector.

## Setup

Let a cyclic class group be

```text
G = <g>,       |G| = h.
```

Let a finite ordered correspondence word `W` be a list of split-prime moves

```text
w_0, w_1, ..., w_{L-1} in G.
```

At a CM vertex `j_i`, the ordered path value sees the finite tuple

```text
(j_{i+w_0}, j_{i+w_1}, ..., j_{i+w_{L-1}}),
```

possibly through a symmetric or rational function of that tuple.

For the p24 composite target, the relevant net move is

```text
a = 2 * 463 * 223^(-1),
```

with

```text
index(a) = 66254,
order(a) = 3107441.
```

## Lemma

A finite ordered path invariant is fixed by a class translation `t in G` only
if translating every offset in the finite support of the path leaves that
support and its labels unchanged:

```text
{w_0+t, ..., w_{L-1}+t} = {w_0, ..., w_{L-1}}
```

with the same ordered/labeled structure, or with the same structure after the
explicit symmetries that the invariant forgets.

For a generic finite path whose support is a proper subset of `G`, this
stabilizer is trivial.  In particular, retaining the orientation of a short
chain normally gives a full `h`-orbit of path values, not the desired
`h/order(a)=66254` quotient.

To get the quotient by `<a>`, the support must be invariant under translation
by `a`.  A nonempty finite subset of the cyclic `<a>` orbit with that
invariance is the whole `<a>` orbit.  Therefore the quotient path support has
size at least

```text
order(a) = 3107441.
```

This is the same subgroup aggregation as the period/recovery polynomial.

## Toy Calibration

The toy

```text
p24/oriented_composite_path_toy.py
```

uses `D=-5000`, where `h=30`.  The oriented product

```text
3 * 17^(-1)
```

has move `24`, index `6`, and order `5`.  Local ordered-path invariants have
full orbit:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_path_edge_pair_sums=30
```

Only whole oriented-cycle aggregation collapses to the quotient:

```text
component_count=6
distinct_period_sums=6
period_sum_polynomial_degree=6
```

The companion theorem

```text
p24/partial_orbit_invariance_theorem.md
```

checks the same fact for partial windows: window lengths `1..4` along the
order-5 move keep `30` distinct window polynomials.  Coarser sums/products can
have incidental collisions in the high twenties, but they do not collapse to
the quotient count `6`; the full length `5` window is the first one that does.

## Degree Consequence

The degree audit

```text
p24/composite_orientation_degree_tradeoff.py
```

separates orientation cost from subgroup aggregation:

```text
plain X0(206498):
  correspondence_degree = 311808,
  recovery = 102940198007,
  loses the good index;

binary sign labels:
  correspondence_degree = 2494464,
  recovery = 3107441,
  preserves the intended sign choice but still needs the full subgroup
  aggregation/recovery;

full point/Gamma1 marking:
  far above sqrt(p).
```

So ordered sign data is not the missing theorem.  It is at best an input to a
still-needed relative period construction.

## Current Boundary

A successful use of the oriented composite must construct one of:

```text
1. the H-period quotient directly;
2. the degree-3107441 recovery polynomial above one quotient root;
3. the relative non-genus class-character data for the 157 and 211 quotient
   phases.
```

A finite ordered chain of the small prime factors gives oriented local path
data, but not a large class-group stabilizer.  It does not by itself beat the
sqrt barrier.
