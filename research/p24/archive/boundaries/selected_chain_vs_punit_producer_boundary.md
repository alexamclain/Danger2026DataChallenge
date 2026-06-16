# Selected Chain vs P-Unit Producer Boundary

Date: 2026-06-05

This note separates the two surviving ways to finish the p24 sub-sqrt route.

## Selected-Chain Producer

The newest finite artifact is the selected-chain decomposed tower:

```text
P_2(Z0) = 0
C_157,Z0(Y0) = 0
C_211,Y0(W0) = 0
R_W0(J0) = 0
```

with degrees:

```text
2, 157, 211, 3107441.
```

The coefficient count is:

```text
2 + 157 + 211 + 3107441 = 3107811
3107811 / sqrt(10^24+7) = 3.107811e-6.
```

This is the smallest clean `j`-producer artifact currently identified.  It is
recorded in:

```text
p24/phase_lifted_tower_certificate_spec.md
p24/phase_lifted_tower_certificate_toy.py
p24/phase_chain_certificate_verifier.py
p24/lean/PhaseLiftedTowerGate.lean
p24/lean/PhaseLiftedTowerPayloadGate.lean
p24/phase_lifted_payload_accounting_frontier.md
```

The toy now verifies the selected-chain artifact directly:

```text
selected_child_level=1_coeffs_ascending=[563, 777, 133, 1]
selected_chain_artifact_verify=1
toy_selected_chain_slots_excluding_monic=10
```

This route finishes the problem if one proves a producer theorem that outputs
the selected child polynomials and selected recovery polynomial embedded in
the conductor-2 `j` torsor.

The verifier skeleton checks the selected root chain, selected recovery root,
optional `j(A)`, and optional official DANGER3 x-only replay without touching
the full class set.

The payload gate also records the key negative bookkeeping point: the full
`h`-element class table is below fixed `sqrt(p)` for p24 but remains rejected
because it is not class-set-free and has sqrt-like asymptotic scale.

## P-Unit / Content Producer

The alternative is not to output the child/recovery polynomials at all.
Instead, prove a finite-field p-unit/content theorem that forces one of the
existing rank/resultant certificate surfaces:

```text
trace-frame selected Plucker p-unit;
L1 relative-content p-unit;
Hermitian packet norm p-unit;
centered-profile / centered-difference minor p-unit.
```

This can also beat sqrt because the finite verifier surfaces are tiny.
However, it produces a target `j` root only indirectly through the theorem's
implication chain.  The p-unit theorem must therefore be paired with the
post-`j` or post-`A` construction already recorded in:

```text
p24/post_j_root_to_triple_boundary.md
p24/post_cm_root_projection_boundary.md
```

## What Is Closed

The following shortcuts do not currently produce either route:

```text
low-degree parent-period formulas:
  informative relative coefficients were full-degree in small CM scans;

Kummer orbit-norm compression:
  the orbit norm is a nonzero/p-unit payload, not selected-child data;
  in the degree-3 toy, parent trace plus Norm(T_1^3) left 210 descending
  child-polynomial candidates;

low-norm recovery walk:
  no order-3107441 split-prime-power representative exists below norm 66254;

abstract bnrclassfield tower:
  split roots are unpaired with embedded j-periods;

plain-j or plain-edge interpolants:
  packet scalars have generic interpolation degree;

simple Heegner-supported divisor:
  phase scalar divisor roots look generic in the non-genus toy.
```

## Current Best Next Theorem

The selected-chain producer is the most literal route:

```text
construct one embedded non-genus child polynomial for the 157 layer,
then one for the 211 layer,
then one selected degree-3107441 recovery polynomial.
```

The equivalent Kummer normal form is recorded in:

```text
p24/relative_kummer_phase_normal_form.md
p24/kummer_orbit_minpoly_producer_frontier.md
p24/abstract_tower_fiber_map_boundary.md
p24/abstract_tower_morphism_payload_boundary.md
p24/complement_subgroup_generator_boundary.md
p24/tower_kummer_phase_complexity_boundary.md
p24/relative_kummer_orbit_norm_boundary.md
```

It replaces informative child-polynomial coefficients by primitive relative
Kummer powers `T_s^r`: one degree-156 Frobenius orbit for the 157 layer and
six degree-35 Frobenius orbits for the 211 layer.  This is the same phase
payload in a more class-field-shaped package, not a seedless selector or a
single norm per Frobenius orbit.  Small CM scans found no low-degree
parent-period formula for these Kummer powers, and the orbit-norm toy found
many false selected-child candidates when only the norm was fixed.

The p-unit producer is the most plausible proof route if a direct chain
producer remains inaccessible:

```text
construct a genuinely phase-aware norm/divisor whose p-unitness implies the
relative-content or Hermitian packet nonvanishing theorem.
```

The smallest base-field p-unit surface currently identified is the centered
profile:

```text
p24/centered_profile_payload_frontier.md
```

It asks for a p-unit proof of one `156 x 156` leading minor of the centered
Hermitian marginal.  An explicit matrix-plus-rank-witness payload is `57096`
field elements, and a direct determinant p-unit payload is only two scalars.

Both routes require new arithmetic input.  The selected-chain route asks for
explicit embedded class-field data; the p-unit route asks for a nonvanishing
theorem that retains the order-`3107441` phase rather than averaging it away.

The current clean separation is:

```text
Kummer Frobenius minpolys/orbits: selected-chain payload;
Kummer orbit norms: p-unit/nonzero payload only.
```

The abstract tower fiber audit adds a further warning: split abstract quotient
root sets do not cheaply group themselves into relative fibers, so a
Kummer-pairing producer must construct the tower morphism or work directly in
embedded phase coordinates.

The complement-generator audit adds that no low-norm split-prime-power word
inside `K` currently supplies those relative fibers.

The current consolidated theorem form is recorded in:

```text
p24/phase_theorem_current_form.md
p24/phase_chain_executable_frontier.md
p24/prescribed_trace_direct_route_boundary.md
```

It incorporates the selector-degree lower bound, tower-section obstruction,
relative-character-trace equivalence, and the trace-frame matrix-tree
boundary.

## Sutherland Decomposition Comparison

Sutherland's accelerated CM method gives the nearest published analogue to
this fallback surface.  In the notation of Algorithm 2, choosing the subgroup
`G` of order

```text
n = 3107441
```

gives an intermediate polynomial `V` of degree

```text
m = 66254
```

and a specialized recovery polynomial `U_y` of degree `n`.  The finite output
scale is exactly the selected-chain neighborhood:

```text
V plus U_y:          m+n = 3173695
full relative table:      3174011
selected chain:           3107811
```

So accelerated CM strongly validates the `m+n` decomposition as the correct
sub-sqrt fallback object.  It does not, by itself, finish the p24 goal: the
published algorithm still enumerates the relevant subgroup orbits of CM roots
at CRT primes in order to build/update `V` and the specialized `U_y` values.
That is an output/space decomposition, not yet a class-set-free embedded
phase producer.

The selected-chain route therefore has a sharper remaining theorem:

```text
produce the same selected embedded orbit data that accelerated CM would
accumulate by orbit enumeration, but do so from a structural
class-field/CM/Lang identity whose work and certificate scale with m+n rather
than with the full class set.
```

If this cannot be done, the p-unit route is the only remaining route to the
four-field-element payload.
