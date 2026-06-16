# Phase-Lifted Payload Accounting Frontier

Date: 2026-06-06

This note pins down the finite accounting distinction that matters for the
selected-chain tower route.  The point is not only that the verifier surface is
below `sqrt(p)`.  The producer must also be class-set-free.

## Three Payload Shapes

For the third strict p24 trace:

```text
p = 10^24 + 7
sqrt_floor(p) = 1000000000000
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254
n = 3107441
```

The selected-chain artifact carries only one root chain:

```text
top polynomial:             2
selected degree-157 child:  157
selected degree-211 child:  211
selected recovery:          3107441
total:                      3107811
```

The full relative-table artifact carries all children above each parent in the
quotient tower, but still only one recovery fiber:

```text
top polynomial:             2
degree-157 relation:        2*157       = 314
degree-211 relation:        314*211     = 66254
selected recovery:          3107441
total:                      3174011
```

The formal quotient-plus-recovery size is:

```text
m+n = 3173695
```

So the selected chain is smaller than the formal `m+n` count, and the full
relative table is only `316` slots larger.

## Why The Class Table Is Still Rejected

The literal class number is:

```text
h = 205880396014
```

For this fixed p24 instance, `h < sqrt(p)`.  That numerical accident must not
be confused with the requested speedup.  A dense class table still scales like
the class number, hence like `sqrt(p)` in the CM family.  It also violates the
working rule that the certificate not enumerate the class set.

So the finite contract has two parts:

```text
1. payload slots below sqrt(p);
2. producer is class-set-free.
```

Lean now checks this taxonomy in:

```text
p24/lean/PhaseLiftedTowerPayloadGate.lean
```

In particular it records:

```text
selected chain slots = 3107811
full relative table slots = 3174011
m+n slots = 3173695
informative child phase slots = 366
relative morphism slots = 66568
Kummer normal form slots = selected chain slots = 3107811
selected chain and full relative table are class-set-free shapes
full class table is rejected even though it is below fixed sqrt(p)
```

## The Missing Producer Theorem

The smallest surviving theorem is now:

```text
Construct a class-set-free embedded selected chain:

P_2(Z0) = 0,
C_157,Z0(Y0) = 0,
C_211,Y0(W0) = 0,
R_W0(J0) = 0,
```

where the polynomials are paired to the actual conductor-2 embedded `j` torsor,
not just to an abstract class-field tower.

Equivalently, construct the embedded non-genus relative class-character traces
or Kummer phase constants for the `157` and `211` layers, plus one selected
degree-`3107441` recovery polynomial, without traversing the `h` CM roots.

The Kummer normal form explains the child-phase payload:

```text
157 layer: 156 informative primitive constants
211 layer: 210 informative primitive constants
total:     366
```

This is a repackaging of the selected child-polynomial data.  It is not a
norm-only compression and it is not a seedless section.

The more precise Kummer target is recorded in:

```text
p24/kummer_orbit_minpoly_producer_frontier.md
p24/abstract_tower_morphism_payload_boundary.md
```

It says the selected-chain route needs Frobenius minimal-polynomial/orbit data
for `K_s = T_s^r`, not just orbit norms.

## Consequence For Computation

Useful computation should now test proposed producer mechanisms against the
two-part contract above.  A small-row experiment is relevant only if it can
answer one of these questions:

```text
Does the construction produce embedded phase data, not just abstract roots?
Does it pair the selected recovery fiber to the actual j torsor?
Does its data size remain selected-chain or full-relative-table scale?
Does it avoid class-set traversal in the producer?
```

If a computation merely confirms that a dense class table or Hilbert class
polynomial works, it is no longer evidence for the goal.
