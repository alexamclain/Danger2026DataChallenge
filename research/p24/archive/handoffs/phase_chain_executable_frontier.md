# Phase-Chain Executable Frontier

Date: 2026-06-05

This note pins the selected-chain route as an executable verifier surface and
separates it from the still-missing producer theorem.

## Verifier Surface

The selected-chain certificate for the third strict trace carries:

```text
P_2(Z0) = 0
C_157(Y0) = 0
C_211(W0) = 0
R_W0(J0) = 0
optional J0 = j(A)
optional DANGER3 replay accepts (p,A,x0)
```

The dense coefficient count, excluding monic leading coefficients, is:

```text
2 + 157 + 211 + 3107441 = 3107811
3107811 / sqrt(10^24 + 7) = 3.107811e-6.
```

The executable verifier skeleton is:

```text
p24/phase_chain_certificate_verifier.py
```

Schema check:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/phase_chain_certificate_verifier.py --schema
```

It prints:

```text
expected_selected_chain_slots=3107811
expected_selected_chain_slots_over_sqrt=3.107811e-6
```

If the selected-chain route is supplied in Kummer form for the `211` layer,
the five glue invariants are five extension-field objects.  Conservatively
serializing them over `F_p` charges the `211`-layer Frobenius orbit degree
`35` for each object:

```text
3107811 + 5 extension objects = 3107816 extension-object slots
3107811 + 5*35 base coordinates = 3107986 base-field slots
3107986 / sqrt(10^24 + 7) = 3.107986e-6.
```

The finite implication is checked in:

```text
p24/lean/KummerCrossOrbitGlueGate.lean
```

The verifier is intentionally finite.  It does not prove that the supplied
polynomials are the actual embedded class-field polynomials.

## Producer Target

The missing producer theorem is:

```text
Construct one embedded degree-2 root,
one selected degree-157 child polynomial,
one selected degree-211 child polynomial,
and one selected degree-3107441 recovery polynomial
for the conductor-2 p24 CM torsor,
without enumerating the h = 205880396014 class set.
```

Equivalently, construct enough embedded relative non-genus class-character
traces/Kummer phase data for the `157` and `211` tower layers to pair the
selected recovery fiber with the actual `j` torsor.

The Kummer phrasing now has one explicit caveat:

```text
157 layer: one primitive-character Frobenius orbit, so K_s=T_s^157 selects
           the unordered child polynomial up to cyclic relabeling.
211 layer: six primitive-character Frobenius orbits, so six independent
           K_s=T_s^211 orbit/minpoly payloads leave cross-orbit phase
           ambiguity unless five relative phase-glue invariants, for example
           T_a/T_1^a, are supplied.
```

The ambiguity gate is:

```text
p24/relative_kummer_multi_orbit_ambiguity_gate.md
```

## Why Modular-Polynomial Recurrence Alone Does Not Produce It

The tempting recurrence idea is:

```text
use a split-prime modular polynomial to describe a long class-action cycle,
then eliminate the cycle variables seedlessly.
```

The current audit says this does not beat sqrt scale.  Running:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/seedless_cycle_resultant_audit.py
```

reports, for p24:

```text
full 23-generator closed cycle:
  log10 degree ~= 2.803531e11

index-314 subgroup cycle via ell=677:
  log10 degree ~= 1.855932e9

best decomposed shape if embedded invariants are already known:
  quotient degree = 66254
  recovery degree = 3107441
  largest degree / sqrt(p) = 3.107441e-6
```

Even the absurd lower bound for a seedless order-`3107441` closed cycle using
any prime-level correspondence is:

```text
log10 degree >= 9.354330e5,
```

which is still far above `sqrt(p)` scale.

So recurrence/resultant compression helps only after an embedded subgroup
projector or quotient invariant exists.  It does not itself supply the
missing phase.

## Exact Boundary

The selected-chain route succeeds if a theorem supplies:

```text
embedded relative class-character traces / Kummer constants
  -> for the 211 layer, cross-orbit phase glue if using Kummer powers
  -> selected child polynomials
  -> selected recovery polynomial
  -> selected conductor-2 j-root
  -> Montgomery A and x0 verified by DANGER3 replay.
```

It fails if the construction is only:

```text
abstract bnrclassfield roots,
unpaired quotient equations,
local path data under a split-prime correspondence,
closed universal cycle resultants,
or dense class-set / Hilbert-class-polynomial enumeration.
```

This is the same phase obstruction seen in the p-unit route.  The verifier is
ready; the missing work is still the embedded non-genus phase producer.

The direct fixed-trace/prescribed-order escape hatch is separately closed in:

```text
p24/prescribed_trace_direct_route_boundary.md
```

For fixed `p`, prescribing the DANGER3 order fixes the ordinary isogeny class,
and the three strict p24 traces have conductor `2` but fundamental
discriminants comparable to `p`.  Known fixed-field constructions therefore
return to the same large CM-root selection problem.

## Abstract Relative Fiber Prerequisite

The Kummer-pairing variant needs abstract relative fibers before it can compare
abstract and embedded Kummer powers.  The audit:

```text
p24/abstract_tower_fiber_map_scan.py
p24/abstract_tower_fiber_map_boundary.md
```

tested two fundamental `h=30`, `a=5`, `r=3`, `n=2` rows.  In both base-field
orientations for `D=-671` and `D=-815`, there was no balanced rational map of
degree `1`, `2`, or `3` from the degree-15 abstract roots to the degree-5
abstract parent roots.  So abstract quotient root sets remain unpaired even
before embedded `j` periods enter.

## Abstract-To-Embedded Pairing Falsifier

The decomposed-CM sidecar pointed to the key calibration:

```text
p24/abstract_embedded_graph_relation_scan.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/abstract_embedded_graph_relation_scan.py
```

In the `D=-2239`, degree-5 non-genus toy it compares abstract quotient roots
to embedded period sums.  The result:

```text
degA=1 degY=1:
  actual_success_matchings=0
  random_success_controls=0/20

degA=1 degY=2:
  actual_success_matchings=120
  random_success_controls=20/20

degA=2 degY=1:
  actual_success_matchings=120
  random_success_controls=20/20
```

So the first nontrivial abstract-to-embedded relations appear at the generic
interpolation threshold and are matched by random controls.  This supports
the boundary:

```text
abstract quotient roots do not come with a cheap embedded pairing relation
back to j.
```

Any proposed quotient-scale recurrence or class-field package should beat
this toy's random-control threshold before being trusted for p24.
