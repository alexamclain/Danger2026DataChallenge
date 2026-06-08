# p24 Dual Conditions Value-Side Gate

Date: 2026-06-07

## Point

The four dual Fourier families are the clean verifier-facing target, but an
arithmetic proof of the selected weighted packet is more likely to see
value-side identities.

For a packet function:

```text
f : C_7 x C_179 -> K
```

the four Fourier families with:

```text
lambda_179 = -1/89
```

are equivalent to three value-side conditions.

## Three Value-Side Conditions

### 1. C-Row Sums Are Independent Of Right Coordinate

For every `r in C_7`:

```text
sum_c f(r,c)
```

is independent of `r`.

This is the value-side form of:

```text
F(a,0)=0, a=1,...,6.
```

### 2. C-Zero Fiber Vanishes

For every `r in C_7`:

```text
f(r,0)=0.
```

This packages the three global pair-balance equations together with the
right-trivial normalization.

### 3. Inversion-Complement Is Constant Off The C-Zero Fiber

There is a single constant `kappa` such that for all `c != 0`:

```text
f(r,c) + f(-r,-c) = kappa.
```

This is the value-side form of the conjugate-skew equations and the
right-trivial pair-sum normalization.

For an admissible C-axis Jacobi carry, this constant is the product degree
`N=7*c` in the integral model.

## Consequence

The selected-packet theorem can now be targeted without Fourier language:

```text
After Tr_{B/C}, the selected weighted packet f on C_7 x C_179 has
equal C-row sums, vanishes on the C-zero fiber, and has constant
inversion-complement off that fiber.
```

That is equivalent to the `632` Fourier equations and therefore to membership
in the rank-`621` admissible span.

The Lean companion records the formal handoff from these three identities to
the existing verifier pipeline:

```text
p24/lean/TraceGcdDualConditionsValueSideGate.lean
```

It now has two equivalent producer-facing entrances:

```text
RobertProducerObligations
ReducedJacobiCarryObligations
```

It now also has the sharper current theorem-contract entrance:

```text
UnramifiedTwistedJacobiProducerObligations
```

This splits the surviving proof into:

```text
unramifiedTwistSelectsPostBCQuotient;
heckeRatioGivesArtinCoordinatePullback:
  postBCQuotientGeneratedByRho;
  localDataMakesRatioUnramifiedFiniteOrder:
    sameInfinityType;
    sameFiniteLocalTypeOnKilledConductorPart;
    killedLocalRayPartHasNoPostBCCharacterSupport;
    ratioFactorsThroughUnramifiedPostBCQuotient;
  axisValuesDetermineRatioOnRho:
    ratioMatchesRightAxisSelector;
    ratioMatchesCAxisSelector;
selectedTraceGcdEqualsTwistedJacobiPacket;
twistedReducedCarry satisfies the three reduced-carry identities.
```

The first item is now a finite p24 gate in the symbolic Jacobi file: the
unramified class-character twist has exact post-`B/C` order `1253` and axes
`7` and `179`.  The `postBCQuotientGeneratedByRho` sub-item is also finite:
the image of `rho` generates the cyclic quotient, so matching the ratio value
on `rho` determines the whole quotient character.  The remaining arithmetic
sub-items are now explicitly local: matching infinity type, matching finite
local type on the killed conductor/ray part, factoring through the unramified
post-`B/C` quotient, matching the selector on the two axes, and the
packet-identification statement.  The killed local/ray part has order
coprime to `1253`, so it has no character support on the selector axes.  The
two axis checks imply the `rho` check because
`rho = (rho^179)^2 * (rho^7)^128` in the post-`B/C` quotient.  Once these are
proved, the symbolic Jacobi gate supplies the three value-side identities and
Lean carries them to the verifier.

This is likely the best packet-facing version of the missing theorem.  It
separates three arithmetic inputs:

```text
1. row-sum descent / C/E-centering;
2. section-aware C-zero fiber vanishing;
3. anti-Hermitian or product-formula complement law.
```

## Check

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.py

lean p24/lean/TraceGcdDualConditionsValueSideGate.lean
```

Observed:

```text
value_dual_equivalence_random_checks=3/3
value_dual_rank_matches=3/3
admissible_carries_satisfy_value_conditions=3/3
random_controls_reject_both=3/3
```

No p24 class set or CM root enumeration is used.
