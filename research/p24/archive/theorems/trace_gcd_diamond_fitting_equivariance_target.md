# Trace-GCD Diamond/Fitting Equivariance Target

Date: 2026-06-06

This note separates the current p24 trace-GCD theorem into:

```text
equivariance transport  +  representative p-unit nonvanishing.
```

The split matters because the right-unit symmetry should not be asked to prove
nonvanishing.  Its job is only to transport p-unitness between determinant
lines.

## Product-Algebra Setup

Let

```text
A_211 = F_p[mu_211]
      = R_O0 x R_O1 x ... x R_O6
```

where `O0={0}` and `O1,...,O6` are the six length-35 Frobenius orbits on
`Z/211Z`.  The diamond/right-unit automorphism

```text
<2> : zeta_211 -> zeta_211^2
```

fixes `O0` and cycles:

```text
O1 -> O2 -> O3 -> O4 -> O5 -> O6 -> O1.
```

The finite bookkeeping is:

```text
p24/trace_gcd_unit2_orbit_compression_audit.py
p24/diamond_support_transport_audit.py
p24/lean/UnitOrbitGate.lean
```

The support-transport audit checks the representative row

```text
delete O4, tail O1, prefix O2,O3,O5,O6
```

under the unit `2` action.  It verifies that deleted and tail orbits cycle
through all six nonzero Frobenius orbits, every transported prefix still has
four orbit blocks, and every transported size-16 tail window remains
Frobenius-contiguous in the target factor.  After one full unit cycle, the
tail returns to `O1` with Frobenius rotation start `17`, so the theorem must
be phrased with internal Frobenius rotations rather than literal residue-set
equality.

## Determinant-Line Statement

For each right orbit `O`, let

```text
B_O : K_O -> T_O
Xi_O = det(B_O)
```

be the p-integral block-cycle/Fitting operator and determinant-line section
attached to the actual p24 trace-GCD prefix kernel and selected tail window.

The desired diamond-equivariance theorem is:

```text
For each nonzero O, the diamond action gives p-integral isomorphisms

  d_K,O : K_O  -> K_{2O}
  d_T,O : T_O  -> T_{2O}

such that

  B_{2O} o d_K,O = d_T,O o B_O

up to the canonical p-integral determinant-line trivializations.
```

Equivalently, on determinant lines:

```text
Xi_{2O} = epsilon_O * Xi_O,
epsilon_O in O_p^*.
```

This is the exact p-unit-scale statement.  It does **not** say the printed
scalars are literally equal.

## Consequence

If the theorem above is proved, then:

```text
Xi_O1 in O_p^*
  => Xi_O2,...,Xi_O6 in O_p^*.
```

Together with the fixed orbit:

```text
Xi_O0 in O_p^*,
```

the finite verifier payload becomes:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

namely four base-field elements.  The Lean handoff is:

```text
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

which proves:

```text
fixed orbit p-unit
+ one representative p-unit
+ six p-unit determinant-line transition factors
=> all seven orbit p-units
=> no translated Schubert/Fitting bad event.
```

The same Lean gate now records the single-step determinant transport handoff:

```text
punit_arrow_from_commuting_integral_det_transport
```

If `Xi_2O = transition_O * Xi_O` and
`transition_O = det(d_T,O) * det(d_K,O)^(-1)` with both determinant factors
p-units, then p-unitness of `Xi_O` implies p-unitness of `Xi_2O`.
It also checks the finite rotation identity

```text
p24_unit2_six_steps_is_frobenius_rotation17
```

matching the support audit's final tail rotation start `17`.

It also records:

```text
4 < 14 < sqrt(10^24+7).
```

## What Remains After Equivariance

The equivariance theorem would reduce the arithmetic nonvanishing problem to
two p-unit statements:

```text
v_p(Xi_O0(x_p24)) = 0,
v_p(Xi_O1(x_p24)) = 0.
```

In linearized trace-GCD language these are:

```text
Xi_O0 = Res_p-lin(P_{K_0}, T_0),
Xi_O1 = Norm_O1(Res_p-lin(P_{K_t}, T_t)).
```

The corresponding theorem target is:

```text
p24/trace_gcd_two_linearized_resultant_target.md
```

Those are still genuine selected-prime local-intersection theorems.  They
must be proved either by:

```text
1. direct Fitting invertibility of B_O0 and B_O1 after reduction mod p; or
2. a phase-aware Borcherds/Fitting product formula whose local value is a
   p-unit at the selected ordinary CM point.
```

The current local criterion is:

```text
p24/trace_gcd_ordinary_fitting_disjointness_criterion.md
p24/lean/TraceGcdOrdinaryFittingCriterionGate.lean
```

## Why The Scale Factor Matters

The pinned actual-CM row gives a warning:

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

There, a right unit swaps the two nonzero right Frobenius orbits.  The actual
orbit norms are p-units, but they are not equal:

```text
literal_equal_edges=0/4
punit_ratio_edges=4/4
```

So the correct theorem is determinant-line equivariance up to p-unit
transition factors.  A literal equality theorem is false even in the faithful
small row.

## Proof Checklist

To prove the diamond-equivariance theorem, one must construct the p24
determinant-line object from universal data rather than from arbitrary printed
coordinates:

```text
1. the full product algebra A_211, not one selected factor R_O;
2. diamond-equivariant Lang/Fourier bases over the p-integral model;
3. prefix kernels as kernels of diamond-transported full-block trace maps;
4. tail windows as diamond-transported subbundles, allowing Frobenius rotation
   inside a target factor;
5. determinant-line comparison of B_O and B_{2O};
6. proof that the comparison scalar has p-adic valuation zero.
```

Items 1-5 are structural equivariance.  Item 6 is denominator hygiene; it is
expected from prime-to-level and ordinary good reduction, but it must be made
explicit in the producer proof.

The structural theorem is now isolated in:

```text
p24/full_product_determinant_line_equivariance_theorem.md
p24/full_product_determinant_transport_toy.py
```

The theorem states that a full `A_211` p-integral construction with functorial
prefix kernels and transported tail subbundles gives commuting squares
`B_2O d_K = d_T B_O`; taking top exterior powers then gives the determinant
line relation above.  The toy checks this relation, including the p24
six-step internal Frobenius rotation closure, and rejects literal determinant
equality as the invariant.

The denominator-hygiene half is now isolated in:

```text
p24/diamond_transport_unit_criterion.md
p24/diamond_transport_unit_denominator_audit.py
p24/diamond_support_transport_audit.py
p24/lean/TraceGcdDiamondEquivarianceGate.lean
```

The finite criterion is:

```text
epsilon_O = det(d_T,O) * det(d_K,O)^(-1)
```

is a p-unit once the source and target transport determinants are p-units;
then `Xi_{2O} = epsilon_O * Xi_O` transports p-unitness by
`punit_arrow_from_commuting_integral_det_transport`.
The p24 audit records that the visible denominators

```text
2, 7, 30, 35, 156, 157, 211, 5460, 66254, h
```

are all prime to `p`.  Therefore the remaining diamond work is structural:
construct the p-integral transports and identify the determinant-line
comparison.

After this checklist, the only remaining hard arithmetic is the two-orbit
local p-unit theorem above.
