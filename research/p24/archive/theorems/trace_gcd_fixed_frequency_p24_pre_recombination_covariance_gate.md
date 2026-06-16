# Fixed-Frequency p24 Pre-Recombination Covariance Gate

Date: 2026-06-06

## Point

Status update: this is now a **conditional handoff**, not the preferred
arithmetic target.  The follow-up obstruction gate

```text
p24/trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate.md
```

shows that the natural Gauss-normalized covariance has trivial eigenvalue
under the same factor shift.  Therefore a nontrivial normalized covariance
would be a componentwise-zero theorem, much stronger than the H-coset target.
The current preferred target is the specific weighted internal-trace/right
coboundary identity.

The surviving order-7/H-coset proof route needs the covariance identity in the
right order.

The useful theorem is not:

```text
the recombined character projection is L-valued,
therefore it has a nontrivial rho-eigenvalue.
```

That is circular.  Once the projection has been recombined into
`L = F_p(mu_157)`, `rho=p^780` fixes it.  A nontrivial eigenvalue at that
stage is equivalent to already knowing the projection is zero.

The conditional theorem packaged here would be:

```text
1. before recombination, decompose the Gauss-normalized trace-resolvent
   contribution into the 70 E-idempotent factors;
2. prove the component covariance under delta -> delta+10 with the nontrivial
   order-7 twist;
3. then recombine all 70 components to the original L-valued projection.
```

The finite consequence is:

```text
pre-recombination component covariance
+ complete recombination/descent
+ trivial fixed/eigenspace intersection
=> six nontrivial character projections vanish
=> the 1092 H-coset scalar equations follow after centering.
```

## Lean Gate

Added:

```text
p24/lean/TraceGcdPreRecombinationCovarianceGate.lean
```

It proves the abstract handoff:

```text
ComponentCovariance
CompleteRecombination
ComponentCovarianceGivesPacketEigen
FixedBy rho packetSum
FixedEigenspaceIntersectionZero twist
------------------------------------------------
packetSum = 0
```

and the character-family version for all six nontrivial right quotient
characters.

The p24 counts are also pinned:

```text
70 = 10 * 7
936 = 6 * 156
1092 = 7 * 156 = 156 + 6 * 156
```

## What Remains Arithmetic

The gate does not prove the missing CM/Lang identity.  After the normalized
covariance obstruction, this should not be treated as the live dependency
unless one can really prove componentwise vanishing.  The safer live theorem is:

```text
for the actual p24 weighted packet, the nested internal trace of the specific
G_chi obstruction vanishes, so Hilbert 90 gives the matching right coboundary.
```

This is narrower than the earlier order-7 augmentation wording and avoids two
false shortcuts already checked elsewhere:

```text
formal unnormalized additive covariance only moves the Gauss sum;
post-recombination nontrivial covariance is circular.
```

So this file remains a useful finite implication, but the proof route has
shifted to the internal-trace/coboundary target.
