# Abstract Tower Morphism Payload Boundary

Date: 2026-06-06

This note separates two different meanings of "abstract tower data" in the
selected-chain route.

## Root Sets Are Not A Tower

The audit:

```text
p24/abstract_tower_fiber_map_scan.py
p24/abstract_tower_fiber_map_boundary.md
```

shows that split abstract root sets for degree `a` and degree `a*r` class
fields do not cheaply group themselves into relative fibers.  In the two
fundamental `h=30`, `a=5`, `r=3`, `n=2` rows tested, no balanced polynomial
map of degree `1` through `7` carried the `15` abstract fine roots onto the
`5` abstract parent roots.  The earlier rational search also found no maps of
degree `1` through `3`.

Thus a theorem cannot just hand us two split polynomials and call that a
tower.  It must provide the morphism/fiber relation.

## Honest Morphism Payload

For p24, the full relative-table morphism is:

```text
F_157(Z,Y): degree 157 in Y, coefficients degree < 2 in Z
F_211(Y,W): degree 211 in W, coefficients degree < 314 in Y
```

The non-monic coefficient count is:

```text
2*157 + 314*211 = 66568.
```

Including the top degree-2 equation and one selected recovery polynomial:

```text
2 + 66568 + 3107441 = 3174011.
```

Lean checks these counts in:

```text
p24/lean/PhaseLiftedTowerPayloadGate.lean
```

This full relative morphism payload is only slightly larger than the selected
chain:

```text
selected chain:       3107811
full relative table:  3174011
difference:             66200
```

Both are sub-sqrt finite surfaces for p24.  The difference is not verifier
size; it is producer honesty.

## Updated Theorem Alternatives

The selected-chain route can succeed in either of two class-set-free ways:

```text
1. selected-chain theorem:
   directly construct the selected degree-157 child, selected degree-211
   child, and selected degree-3107441 recovery;

2. relative-morphism theorem:
   construct the full embedded F_157 and F_211 tower morphisms, then one
   selected recovery fiber.
```

The second route is allowed by payload accounting.  It is not allowed to
construct those relations by enumerating the full `h` CM roots or by forming a
dense degree-`h` class polynomial.

## Consequence

The abstract-to-embedded Kummer-pairing idea needs this same morphism input.
Once the relative fibers are supplied, Kummer powers can be computed within
each fiber and compared to embedded child periods.  Without the morphism,
abstract Kummer powers are just another unpaired root-set construction.

The split-prime generator search adds that this relative fiber data is not
currently supplied by a short internal generator of the balanced complement:

```text
p24/complement_subgroup_generator_boundary.md
```

So the theorem target is now:

```text
construct embedded Kummer orbit/minpoly data with relative fibers,
or construct the full embedded relative morphism,
or bypass both with a phase-aware p-unit/divisor identity.
```
