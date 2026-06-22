# P27 Label-2 Alpha Projective Quotient Smoke

Date: 2026-06-21

## Claim

The explicit `alpha` map can be promoted from an affine formula to a
projective Magma automorphism on the genus-17 main component.  On a tiny
`q = 7 mod 16` smoke field, Magma verifies:

```text
main component genus = 17
projection to E: W^2 Z = X^3 - X Z^2 has degree 4
projection ramification degree = 32
alpha is a projective isomorphism
the generated automorphism group has order 4
```

The generic `CurveQuotient(G)` call still exceeds the online calculator time
limit, but the important quotient is already explicit: the quotient by
`alpha` is the residual elliptic curve `E`, with coordinates `(X,W,Z)`.

## Artifacts

Affine map-only fixture:

```text
research/p27/archive/fixtures/p27_label2_alpha_quotient_q23_magma.m
```

Projective quotient smoke fixture:

```text
research/p27/archive/fixtures/p27_label2_alpha_projective_quotient_q7_magma.m
```

Outputs:

```text
research/p27/archive/probe_outputs/p27_label2_alpha_quotient_q23_magma_20260621.txt
research/p27/archive/probe_outputs/p27_label2_alpha_projective_quotient_q7_magma_20260621.txt
```

Raw calculator responses:

```text
research/p27/archive/probe_outputs/p27_label2_alpha_quotient_q23_magma_20260621.html
research/p27/archive/probe_outputs/p27_label2_alpha_projective_quotient_q7_magma_20260621.html
```

## Affine q23 Result

The q23 affine fixture validates that Magma accepts the rational map interface:

```text
MAP_OK true true true true
```

It then exceeds the online time limit while trying to certify the affine
`iso`/quotient path.  That is a CAS-interface limitation, not a mathematical
negative.

## Projective q7 Result

The projective fixture homogenizes the eliminated cyclic quartic and the
alpha map.  It then selects the highest-degree projective component and asks
Magma for the projection to `E`, the alpha isomorphism, and the automorphism
group.

Output:

```text
PROJ_COMPS 3
PROJ_COMP 1 1 30 8
PROJ_COMP 2 1 1 8
PROJ_COMP 3 1 1 8
MAIN_IDX 1
MAIN_GENUS 17 8
E_PROJECTION_OK 1 8 true true
E_PROJECTION_DEGREE 4
RAMIFICATION_OK 32
ISO_OK true
AUT_GROUP_OK 4
```

The subsequent generic `CurveQuotient(G)` call exceeds the online calculator
time limit.  Since `alpha` fixes `(X,W,Z)` and the checked projection has
degree `4`, the quotient surface needed for the next theorem pass is already
the residual elliptic curve `E`.

## Interpretation

Positive:

```text
The explicit alpha map survives projective homogenization.
Magma certifies alpha as an automorphism on the genus-17 main component.
The alpha group has order 4.
The quotient coordinates are the residual elliptic curve E, via degree 4 projection.
The ramification degree is 32, matching Riemann-Hurwitz for genus 17 -> genus 1.
```

Negative / not promoted:

```text
This does not create a new source or sampler.
The alpha quotient is E itself, not a smaller surprise surface.
Online Magma's generic CurveQuotient is too slow here even for q=7.
```

## Consequence

The next useful math object is not `D/<alpha>` as an abstract quotient; that
part is explicit.  The live question is the cyclic-quartic character over
`E`, or equivalently the Prym/Kummer data of the degree-4 cover:

```text
C -> E
R^4 - 2*pref*m0*R^2 + 4*pref^2*T2*S^2 = 0
alpha^2 = R -> -R
```

To move toward a sqrt-beating result, extract the branch divisor / Kummer
class of this cover over `E`, then test whether that class recurs or couples
to the descended `d3`/`d4` classes on `E` or the 2-isogenous quotient `E'`.

Follow-up branch-class screen:
[P27 Alpha Branch-Class Screen](p27_alpha_branch_class_screen_20260621.md).
It shows that the visible branch squareclass is just `T2`, which is already
constant square on the active d3/d4 domains.  That kills alpha branch
discriminant fitting as the next route; the remaining task is actual d3/d4
cover extraction.

## Continue / Kill

```text
continue = compute branch divisor and cyclic-quartic/Kummer class over E
continue = compare that class with the d3/d4 E-level double-cover classes
continue = use offline Sage/Magma if Jacobian/Prym decomposition is needed

kill = spending online-Magma budget on generic CurveQuotient for this model
kill = treating alpha quotient alone as a sampler
kill = GPU promotion without recurrence/source or survivor-per-second lift
```

## Linked Artifacts

- Parent: [P27 Label-2 Alpha Eliminated-Map Probe](p27_label2_alpha_eliminated_map_20260621.md)
- Component check: [P27 Label-2 Cyclic-Quartic Component Check](p27_label2_cyclic_components_magma_20260621.md)
- H90 parent: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Branch follow-up: [P27 Alpha Branch-Class Screen](p27_alpha_branch_class_screen_20260621.md)
- Projective fixture: `research/p27/archive/fixtures/p27_label2_alpha_projective_quotient_q7_magma.m`
- Projective output: `research/p27/archive/probe_outputs/p27_label2_alpha_projective_quotient_q7_magma_20260621.txt`
- Affine fixture: `research/p27/archive/fixtures/p27_label2_alpha_quotient_q23_magma.m`
- Affine output: `research/p27/archive/probe_outputs/p27_label2_alpha_quotient_q23_magma_20260621.txt`

```text
p27_label2_alpha_projective_quotient_magma_rows=2/2
```
