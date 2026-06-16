# Abstract Tower Fiber Map Boundary

Date: 2026-06-06

This note tests a prerequisite for the abstract-to-embedded Kummer-pairing
idea.  Before comparing abstract Kummer powers to embedded Kummer powers, the
abstract quotient roots must be grouped into relative fibers.

## Question

In a small tower shape:

```text
h = a * r * n
a = parent quotient degree
r = prime child degree
```

PARI can produce abstract class-field equations for degree `a` and degree
`a*r` quotients.  Does the root set of the degree-`a*r` equation expose a
cheap map down to the degree-`a` roots?

The tested shape is the p24 analogue:

```text
a = 5
r = 3
n = 2
```

I searched for rational maps:

```text
P(x) / Q(x)
```

of degree `1`, `2`, and `3`, carrying the `15` abstract fine roots onto the
`5` abstract parent roots with exactly `3` preimages per parent.

The script is:

```text
p24/abstract_tower_fiber_map_scan.py
```

## Runs

Small control run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_tower_fiber_map_scan.py \
  --degrees 1 2 --random-controls 5 --random-combos 8 --max-found 2
```

Output summary:

```text
D=-671, q=1571:
  both base-field orientations:
    degree=1 maps_found=0 random=0/5
    degree=2 maps_found=0 random=0/5

D=-815, q=2111:
  both base-field orientations:
    degree=1 maps_found=0 random=0/5
    degree=2 maps_found=0 random=0/5
```

Polynomial scan:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_tower_fiber_map_scan.py \
  --degrees --polynomial-degrees 1 2 3 4 5 6 7 \
  --max-polynomial-tuples 500000 --max-found 1 --random-controls 0
```

Output summary:

```text
D=-671, q=1571:
  both orientations:
    polynomial_degree=1..7 polynomial_maps_found=0

D=-815, q=2111:
  both orientations:
    polynomial_degree=1..7 polynomial_maps_found=0
```

The earlier rational edge run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_tower_fiber_map_scan.py \
  --degrees 3 --random-controls 0 --random-combos 4 --max-found 1
```

also found no degree-3 balanced rational maps in either row.

## Interpretation

The result does not disprove an abstract Kummer-pairing theorem, but it rules
out the cheap version:

```text
abstract fine root
  -- low-degree rational map -->
abstract parent root.
```

Thus the proposed Kummer-pairing stress test has an additional hidden input:
it must first obtain the abstract relative fiber grouping by a class-field
tower construction, not merely by holding two split root sets.

This is the same obstruction in a sharper place:

```text
abstract quotient roots are unpaired even before the embedded j-periods enter.
```

## Consequence For The Selected-Chain Route

The positive theorem should not be stated as:

```text
take abstract degree-a and degree-a*r root sets, then pair them to embedded
Kummer data.
```

It must instead construct one of:

```text
1. an explicit embedded tower with relative fibers already paired;
2. a class-set-free abstract tower morphism plus an embedded comparison map;
3. a p-unit/divisor identity that bypasses root-set pairing entirely.
```

The Kummer orbit/minpoly target remains live, but the producer theorem must
include relative fiber data.  A bare `bnrclassfield` quotient package is still
not enough.

The payload accounting for the honest full relative morphism is recorded in:

```text
p24/abstract_tower_morphism_payload_boundary.md
p24/lean/PhaseLiftedTowerPayloadGate.lean
```
