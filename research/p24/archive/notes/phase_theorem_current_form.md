# Phase Theorem Current Form

Date: 2026-06-05

This note consolidates the embedded class-field tower route after the
selector-degree and tower-section gates.

## Live Finite Surface

Use the third strict trace:

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014 = 2 * 157 * 211 * 3107441
G = Cl(O) cyclic
```

Let:

```text
G > K_1 > K_2 > H
[G:K_1] = 2
[K_1:K_2] = 157
[K_2:H] = 211
|H| = 3107441.
```

The selected-chain certificate surface is:

```text
top degree-2 root
selected degree-157 child polynomial
selected degree-211 child polynomial
selected degree-3107441 recovery polynomial
```

with coefficient count:

```text
2 + 157 + 211 + 3107441 = 3107811
3107811 / sqrt(p) = 3.107811e-6.
```

The full relative-table version is also sub-sqrt:

```text
2 + 2*157 + 314*211 + 3107441 = 3174011
3174011 / sqrt(p) = 3.174011e-6.
```

The finite implication is checked in:

```text
p24/lean/PhaseLiftedTowerGate.lean
p24/lean/PhaseLiftedTowerPayloadGate.lean
p24/lean/SelectorDegreeLowerBoundGate.lean
```

The executable verifier skeleton and the current recurrence/resultant
boundary are recorded in:

```text
p24/phase_chain_executable_frontier.md
p24/phase_chain_certificate_verifier.py
p24/phase_lifted_payload_accounting_frontier.md
```

## What Is Now Ruled Out

Bounded embedded selectors:

```text
p24/finite_field_selector_degree_theorem.md
p24/lean/SelectorDegreeLowerBoundGate.lean
```

A single embedded rational selector whose fiber contains an `H`-coset must
have degree at least `|H|`.  For the third trace this lower bound is
`3107441`, still sub-sqrt, but it rules out fixed-level shortcuts.

Seedless canonical child sections:

```text
p24/tower_section_obstruction.md
p24/lean/TowerSectionObstructionGate.lean
```

A `G`-equivariant child selector would force the parent stabilizer `K` to
fix the selected child, hence `K <= L`.  For a genuine refinement `L < K`,
this is impossible.

Low-degree parent-period formulas:

```text
p24/tower_phase_coefficient_complexity_boundary.md
```

After removing the forced trace coefficient, informative child-polynomial
coefficients had full interpolation degree in small CM tower rows.

Low-norm recovery correspondence:

```text
p24/low_norm_order3107441_search.md
```

No signed split-prime-power representative, even with the ramified genus
prime allowed, hits the order-`3107441` recovery class below the norm threshold
needed for the zero-lemma route.

Ordinary matrix-tree compression of the trace-frame determinant:

```text
p24/axis_crt_matrix_tree_factorization_boundary.md
p24/lean/MatrixTreeFactorizationObstructionGate.lean
```

CRT hypertree support is real, but the weights are Plucker/exterior weights,
not ordinary per-edge tree weights.

## Remaining Positive Theorem

The selected-chain producer must prove an embedded relative phase theorem.

For a parent coset `aK` and one refinement `L < K`, define child periods:

```text
y_{a u L} = sum_{l in L} j_{a u l}.
```

The unordered child polynomial is:

```text
C_{aK}(Y) = product_{u in K/L} (Y - y_{a u L}).
```

Equivalently, after choosing a cyclic coordinate on `K/L`, its coefficients
are determined by relative class-character traces:

```text
T_s(aK) = sum_{k in K} chi_s(k) j_{a k},      0 <= s < [K:L].
```

The trivial trace `T_0` is the parent period.  The nontrivial traces are the
missing non-genus phase.  The toy:

```text
p24/relative_tower_character_toy.py
```

checks this equivalence in the `D=-5000`, `h=30=2*3*5` calibration tower.

The same phase data can be repackaged in Kummer/Lagrange-resolvent form:

```text
p24/relative_kummer_phase_normal_form.md
p24/relative_kummer_reconstruction_toy.py
p24/relative_kummer_payload_accounting.py
p24/tower_kummer_phase_complexity_boundary.md
p24/relative_kummer_orbit_norm_boundary.md
```

For a prime layer of degree `r`, primitive relative resolvents `T_s` may be
replaced by Kummer powers `T_s^r`.  In the toy degree-3 layer, the parent trace
plus one primitive Kummer constant reconstructs the unordered child
polynomial; the cube-root ambiguity is only cyclic relabeling.  For p24 this
normal form has:

```text
157 layer: one Frobenius orbit of 156 Kummer constants
211 layer: six Frobenius orbits of 35 Kummer constants.
```

This repackages the selected child-polynomial payload but does not remove the
need for the oriented embedded phase.

The Kummer complexity scan found full interpolation degree for all tested
Kummer coordinates in small CM towers, so the current theorem target is the
direct construction of those Kummer powers, not a low-degree parent-period
formula for them.  The orbit-norm follow-up also found that a single
Frobenius orbit norm is not enough for selected-chain reconstruction; in the
degree-3 toy, fixing the parent trace and `Norm(T_1^3)` left 210 descending
child-polynomial candidates.  Such norms are useful only on the p-unit /
nonvanishing route unless paired with enough data to identify the Kummer
orbit itself.

The current Kummer-minpoly formulation is:

```text
p24/kummer_orbit_minpoly_producer_frontier.md
p24/abstract_tower_fiber_map_boundary.md
p24/abstract_tower_morphism_payload_boundary.md
p24/complement_subgroup_generator_boundary.md
```

It sharpens the distinction:

```text
Frobenius minpoly/orbit of K_s = selected-chain payload;
Norm(K_s) alone = p-unit/nonzero payload only.
```

The abstract tower fiber audit adds that split abstract degree-`a` and
degree-`a*r` root sets do not by themselves expose the relative fibers by
low-degree rational or polynomial maps in the tested `a=5`, `r=3` rows.
The honest fallback is to construct the full relative morphism itself; its
p24 morphism payload is `66568` coefficients before recovery and remains
sub-sqrt when paired with one selected recovery fiber.

The complement-generator audit shows that the relative fibers are not
currently reachable by a low-norm split-prime-power generator inside `K`.

Thus the exact theorem to prove is:

```text
Construct the embedded non-genus relative class-character traces for the
157 and 211 tower layers, and one selected degree-3107441 recovery polynomial,
without enumerating the full h-element CM torsor or constructing a degree-h
class polynomial.
```

The payload gate records the corresponding honesty condition as:

```text
sub-sqrt payload + class-set-free producer.
```

This is intentionally stronger than the fixed-instance inequality
`h < sqrt(p)`, because an `h`-scale table still has sqrt-like asymptotic
behavior in the CM family.

## Alternative Positive Theorem

The p-unit route remains possible:

```text
prove the trace-frame determinant-line/Fitting p-unit theorem
delta_all in A_all^*
```

or one of its equivalent norm-compressed forms.  This route bypasses explicit
child/recovery polynomials, but it still has to retain the same high-order
phase rather than averaging it away.

## Practical Next Tests

Small computation should now focus only on theorem candidates that produce
one of these two things:

```text
1. relative non-genus class-character traces / selected child polynomials;
2. a phase-aware p-unit determinant or norm.
```

More branch statistics, bounded Legendre gates, low-degree interpolation in
parent periods, or ordinary support compression are no longer promising
enough to spend real compute on.
