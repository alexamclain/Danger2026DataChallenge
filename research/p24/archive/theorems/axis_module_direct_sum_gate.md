# Axis Module Direct-Sum Gate

This note records the current theorem refinement after the Hermitian,
coefficient-minor, probability, and module-decomposition passes.

## Formal Gate

I added:

```text
p24/lean/AxisModuleDirectSumGate.lean
```

It Lean-checks the following finite implication using only core Lean.
Write the axis source as

```text
W_axis = C0 ⊕ U_2 ⊕ U_157 ⊕ U_211
```

where `C0` is the constant line and `U_c` is the trace-zero part of the
`c`-axis.

For one packet, let

```text
E_i : component_i -> A_a
```

be the four component evaluation maps into the packet field, and let `sum4`
be packet-field addition of their images.  If:

```text
1. each E_i has trivial kernel;
2. E_0(C0), E_2(U_2), E_157(U_157), E_211(U_211)
   are a direct sum inside A_a;
3. evaluation respects component differences;
```

then the full axis evaluation

```text
T_a : W_axis -> A_a
```

is injective.

This separates the arithmetic theorem into internal component normality plus
cross-component directness.  It is exactly the proof shape suggested by:

```text
p24/l1_axis_direct_sum_proof_strategy.md
p24/component_character_module_boundary.md
p24/packet_field_k_module_audit.py
```

## p24 Module Accounting

For the p24 third trace:

```text
m = 66254 = 2 * 157 * 211
n = 3107441
packet_degree = ord_n(p) = 388430
```

The base-field axis dimension is:

```text
1 + (2-1) + (157-1) + (211-1) = 368.
```

Over one H-packet field, the character accounting is asymmetric:

```text
2-axis:   1 orbit of size 1
157-axis: 2 orbits of size 78
211-axis: 210 orbits of size 1
```

Equivalently:

```text
ord_157(p)=156, gcd(156,388430)=2
ord_211(p)=35, 35 | 388430
```

So the `211` roots of unity already live in the packet field, while the
`157`-axis needs a degree-78 scalar extension over the packet field.  The
direct-sum gate keeps this asymmetry visible instead of hiding it in a single
368-by-388430 rank statement.

## The New Arithmetic Target

For every one of the eight H-character packets, prove:

```text
E_0(C0) ⊕ E_2(U_2) ⊕ E_157(U_157) ⊕ E_211(U_211)
```

inside the packet field, and prove each component map has trivial kernel.

This implies:

```text
module directness
  => axis injectivity
  => selected L1 nonvanishing
  => exact packet content is nonzero
  => harmful DANGER3 packet collapse is ruled out.
```

## Why This Is Progress

The previous live sufficient theorem was:

```text
det Hermitian_368x368 != 0
```

or an origin-dependent coefficient-minor product.  The new gate gives a
tower-native target:

```text
constant line + smooth trace-zero class-field layers remain direct after
reduction at the selected p24 prime.
```

It is still open, but it is a more explicit embedded class-field statement:
prove selected-prime directness of the degree-`2`, degree-`157`, and
degree-`211` smooth-axis layers after the H-character packet projection.

## Evidence Boundary

The existing scans support this shape but do not prove it:

```text
composite-m all-origin eligible axis scan:
  packet_rows=162
  injective_rows=162
  block_internal_failure_rows=0
  pair_directness_failure_rows=0
  cross_directness_failure_rows=0

component character-module scan:
  dimension_possible_rows=63
  full_module_rows=63
  dimension_possible_internal_failure_rows=0
  zero_orbit_rows=0
```

This should now be the preferred theorem statement when trying to build an
explicit embedded class-field tower: do not try to select a single CM root
directly; prove the smooth trace-zero layer images are direct in the finite
H-packet field.

## Frobenius Shortcut Boundary

The direct-sum target is not automatic from nonisomorphic Frobenius modules.
The audit

```text
p24/axis_frobenius_stability_audit.py
p24/axis_frobenius_cocycle_boundary.md
```

shows that component image spans are not generally stable under packet-field
Frobenius.  The character values satisfy

```text
sigma(G_s(eta)) = G_{p*s}(eta^p),
```

not `G_{p*s}(eta)`.  Thus the H-packet coordinate contributes a cocycle, and
the proof must control the coupled K/H phase rather than only the abstract
K-axis Frobenius modules.

The valid replacement is scalar-extension descent:

```text
p24/lean/ScalarExtensionGate.lean
```

If the K-character diagonalized axis map is injective after adjoining
independent K-character roots, then the original base-field axis map is
injective.  The hard theorem is the extended rank itself, not the descent.
