# p24 Global Synthesis Handoff

Date: 2026-06-07

Purpose: give a fresh agent the benefit of the whole p24 research arc without
making them inhale the hundreds of exploratory files.  Read
`00_HANDOFF_INDEX_20260607.md` first, then this file after
`00_FRESH_EYES_SYNTHESIS_20260607.md`,
`00_FRESH_AGENT_HANDOFF_20260607.md`, `00_RETROSPECTIVE_SYNTHESIS_20260606.md`,
and `00_CURRENT_CONTEXT.md`, before opening route-specific notes.

If context is tight, the index plus `00_FRESH_EYES_SYNTHESIS_20260607.md` is
the intended restart pair.

## Executive Diagnosis

We have made real progress on the shape of a sub-sqrt certificate, but we do
not yet have the arithmetic producer theorem.  The verifier side is small; the
hard part is proving that the p24 selected CM/Lang packet has a special
p-unit or trace-zero identity.

The most important distinction:

```text
verifier surface: small and mostly formal;
producer theorem: still open and highly non-generic.
```

Do not mistake a small verifier for a completed certificate.  Almost every
failed branch failed because it supplied a small formal handoff without an
honest embedded CM/Lang producer.

Fixed data:

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
sqrt_floor = 10^12

E = F_p(mu_m), [E:F_p] = 5460
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7
```

The class group is cyclic and squarefree, but this only gives bookkeeping for
the `2,157,211,3107441` layers.  It does not select embedded child roots over
the split prime above `p`.

## What Would Count As Success

There are three realistic certificate surfaces.

### 1. Four-Field-Element Two-Resultant Surface

Payload:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

This is about `4e-12 * sqrt(p)`.

Missing producer theorems:

```text
det(Psi_RS) is a p-unit                 fixed orbit
Nrd_O(Phi_t) is a p-unit                one nonzero orbit
```

Then unit-2/diamond transport supplies the other nonzero orbits.  The finite
transport side is in good shape; the p-integral determinant-line producer is
still missing.

### 2. Fixed-Frequency H-Coset Surface

Verifier:

```text
156 left rows * 7 right H-cosets = 1092 scalar equations.
```

Compressed equivalent:

```text
48 independent equations = 42 mixed octic + 6 anchor equations.
```

This is not a sampling count.  It is a finite verifier interface for a tower
theorem.  The current sharpest theorem target on this branch is the
admissible Jacobi/internal-character theorem described below.

### 3. Selected-Chain Fallback

Finite payload:

```text
selected chain:      3107811 slots = 3.107811e-6 * sqrt(p)
full relative table: 3174011 slots = 3.174011e-6 * sqrt(p)
```

This is genuinely sub-sqrt for p24, but the producer is missing: one must
construct an embedded non-genus phase or selected recovery polynomial without
dense class-set enumeration.

## The Current Sharp Theorem

The most refined live theorem is on the fixed-frequency trace-GCD route.

After the right Gauss transform, the obstruction is:

```text
G_chi(X) = sum_r chi^{-1}(r mod 211) F_r(X)
F_r(X) = sum_k j_{r+m*k} X^k
```

The target is:

```text
Tr_{C/E}(Tr_{B/C}(Pi_chi G_chi)) = 0
```

for the six nontrivial right quotient characters.  Equivalently, after
`Tr_{B/C}`, the packet has no bidegree:

```text
C_7^nontrivial x {C/E trivial}.
```

That support condition is still too weak.  The current best positive theorem
is stronger:

```text
Tr_{B/C}(Pi_chi G_chi) lies in the rank-621 admissible C-axis
Jacobi-carry span on C_7 x C_179.
```

Admissible Jacobi carry:

```text
theta_{u,v}(t) = [ut] + [vt] - [(u+v)t]

u is right-trivial and C/E-nontrivial;
v has nontrivial C/E component;
u+v has nontrivial C/E component.
```

The broad C-axis family has rank `625`, but includes four leaky directions.
Use the rank-`621` admissible span unless the proof naturally produces the
four leak-cancellation equations.

Spectral fingerprint of the admissible span:

```text
C/E-trivial slice rank:       1
nontrivial C/E slice rank:    7
conjugate C/E-pair rank:      8, not 14
cumulative increments:        1, 7, ..., 7, 4
p24 rank formula:             1 + 7*88 + 4 = 621
```

Fresh proof target:

```text
prove conjugate-C/E pair compatibility for the selected weighted packet.
```

Do not settle for only proving forbidden-support vanishing.

The newest useful sharpening is the dual Fourier form of this same target.
For Fourier coefficients `F(a,b)` on `C_7 x C_179`, admissible-span membership
is equivalent in small exact models to four families:

```text
1. F(a,0)=0 for a=1,...,6;
2. F(a,b)+F(-a,-b)=0 for nontrivial right a and conjugate C/E pairs b;
3. F(0,b)+F(0,-b)=lambda_179*F(0,0) for right-trivial C/E pairs;
4. sum_{b>0}(F(-a,b)-F(a,b))=0 for a=1,2,3.
```

For p24 this is:

```text
6 + 6*89 + 89 + 3 = 632 equations
1253 - 632 = 621 dimensional solution space.
```

So the best handoff theorem is now:

```text
prove these four Fourier condition families for the selected weighted packet
after Tr_{B/C}.
```

This is more actionable than a black-box "find a Jacobi decomposition" request.
The Lean companion
`p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean` records that this
input implies the existing verifier pipeline; it does not prove the CM
producer theorem.
The source map
`p24/trace_gcd_fixed_frequency_p24_dual_condition_source_map.md` attaches known
failure modes and plausible arithmetic sources to each of the four families.
The Jacobi-carry Fourier formula gate now explains these families for a single
admissible carry: `lambda_179=-1/89`, conjugate skew comes from sawtooth
pair-sum cancellation, and the three global balances come from vanishing on
the `C`-zero fiber.
The value-side gate gives the packet-facing equivalent target:

```text
1. C-row sums are independent of the right coordinate;
2. the packet vanishes on the C-zero fiber;
3. f(r,c)+f(-r,-c) is one constant for all c != 0.
```

This is equivalent to the `632` Fourier equations and is the best next form
for a direct CM/Lang proof.
Lean companion:
`p24/lean/TraceGcdDualConditionsValueSideGate.lean`.
The strength gate further splits the theorem:

```text
structural symmetry:
  f(r,0)=0 and f(r,c)+f(-r,-c)=constant for c != 0
  rank 629 for p24;

remaining balances:
  only three independent row-sum/global-balance equations.
```

For a raw packet `g` and selected defect `f(r,c)=g(r,c)-g(r,0)`, the latest
producer target is:

```text
g(r,0)+g(-r,0)=A_0
g(r,c)+g(-r,-c)=A_1 for c != 0
sum_c g(r,c)-179*g(r,0) is independent of r.
```

These raw identities are equivalent to the three value-side identities for
`f`.
Multiplicatively, for `U(r,c)=omega^g(r,c)`, this is:

```text
U(r,0)U(-r,0)=alpha_0
U(r,c)U(-r,-c)=alpha_1 for c != 0
prod_c U(r,c)/U(r,0)^179 = beta.
```

This is the best product-formula-shaped target.

## What The Failures Actually Teach

The failures are not noise.  They point to the same structural conclusion:

```text
the selected weighted trace-GCD packet must be special.
```

### Not Enough: Abstract Class-Field Tower

Cyclicity and squarefreeness remove subgroup ambiguity, but they do not choose
embedded roots over the split prime.  Child roots are torsors.  The odd
`157` and `211` layers need non-genus embedded phase data.

Useful remnant: cyclicity is good bookkeeping for subquotients and Frobenius
actions, not a root selector.

### Not Enough: Generic CM Geometry

Small actual-CM rows repeatedly fail the desired identities:

```text
D=-4751 mixed-spectrum row:       0/91 full mixed/anchor/balance shifts
D=-5000 internal-character row:   0/60 raw packets with zero trivial C
D=-6719 covariance row:           covariance holds, anchor descent fails
D=-13319 right-combo/product row: internal traces and anchor fail
```

Even coefficient-side variants fail:

```text
D=-13319 right-combo resolvents:       0/140 admissible-span origins
D=-13319 raw weighted coefficients:    0/140 admissible-span origins
D=-13319 selected defects c_k-c_0:     0/140 admissible-span origins
```

Thus "ordinary embedded CM plus weighted coefficients" is not enough.
The value-side diagnostic sharpens this: selected defects can force the
`C`-zero fiber, but still give `0/140` inversion-complement and row-sum
origins.  So section subtraction alone does not supply the structural
symmetry.

The literal Jacobi-sum probe sharpens the positive side: raw finite-field
Jacobi sums in small `N=7c` models do supply the off-`C=0` pair-product
complement, but they do not supply the selected row-product ratio in the
right-mixed cases.  The only sampled row-ratio hit is right-trivial
`(u,v)=(7,7)`.  Thus Jacobi sums are a plausible source for inversion
complement, while the three global balances still need a separate C-axis
distribution or selected correction.

The row-ratio miner localizes that correction.  In right-mixed Jacobi-sum
samples, all six nonzero right rows already have the same selected
row-product ratio; the only mismatch is the right-zero anchor.  The anchor
defect is universal across sampled admissible pairs for each `c`, with exact
finite-field formula `delta_c=(q-2)^(-(c-1))`, but it is not a `mu_(7c)`,
`mu_7`, or `mu_c` multiplier.  So the best Jacobi route is now: prove a
Hasse-Davenport punctured-right theorem, then prove that the selected
trace-GCD anchor supplies the universal non-cyclotomic correction.

The next gate makes the literal finite-field correction explicit.  Replacing
only `U(0,0)=J(1,1)=q-2` by `U(0,0)/(q-2)=1` repairs both the C-zero
pair-products and the selected row-product ratio in all right-mixed
admissible Jacobi packets for the exhaustive c=5,11,13 checks.  Thus the p24
theorem should look for the selected
trace-GCD/CM-Lang analogue of one degenerate-anchor unit, not three unrelated
global balance identities.

### Not Enough: Frobenius/Covariance Alone

The p24 action `rho=p^780` is important:

```text
rho fixes the left 157-character;
rho shifts the right quotient by 6 mod 7;
raw relative order is 38843 = 7*5549.
```

But covariance alone puts objects in a nontrivial eigenspace.  It does not
make them zero.  Descended covariance after recombination is often circular:
nontrivial covariance after descent can be equivalent to vanishing.

Useful remnant: covariance plus one honest descended anchor would force the
seven H-coset sums equal.  The anchor is the arithmetic input.

### Not Enough: Formal Right-Character Covariance As Potential

For `chi_k(2)=zeta_7^k`, the matching product-coboundary twist is:

```text
epsilon_k = zeta_7^k.
```

The formal right resolvent has the same eigenvalue, so it lies in the
obstruction eigenspace of `sigma - epsilon_k`, not in its image.  A matching
right potential requires genuine internal trace cancellation.

Useful remnant: if nested internal trace zero is proved, Hilbert-90 supplies
the potential formally.

### Not Enough: Plain Stickelberger/Jacobi Slogans

Plain cyclic Stickelberger and plain right-axis Stickelberger leak in all six
forbidden bidegrees.  Generic Jacobi carries also leak.  C-axis carries only
work in the admissible subfamily above.

Useful remnant: admissible Jacobi carries give the first real positive
support/rank shape.

### Not Enough: Trace-Only Or Anchor-Only Compression

The anchor and the internal `C/E`-centering are distinct.  In the exact
`C_7 x C_179 x C_31` model:

```text
anchor zero can hold while forbidden C/E-trivial bidegree leaks;
C/E-centering can hold while selected-child anchor fails.
```

The selected child/section matters.

### Not Enough: Post-Fit Linear Algebra

Many finite identities are easy after seeing the data: interpolation,
post-fit displacement operators, arbitrary splitting-field sections, or fake
equal H-coset sums.  These are rejected unless the construction is intrinsic,
Frobenius-compatible, and tied to the embedded CM/Lang packet.

## Potential Compositions Worth Rechecking

These are the places where old facts may compose with the current theorem.

### A. Admissible Jacobi Span + Right-Difference Trace

The right-difference route says the 48 compressed equations are equivalent to
trace-zero of adjacent difference polynomials:

```text
P_i(X) = sum_k (A_{i+1}(k)-A_i(k)) X^k
Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n)) = 0.
```

The Jacobi spectral fingerprint says the missing structure is conjugate
`C/E` pair compatibility.  A promising composition is:

```text
express adjacent differences as the conjugate-pair part of the admissible
Jacobi decomposition.
```

If this works, it may replace a black-box rank-621 membership proof with an
explicit pairwise trace identity.

### B. p^780 Covariance + Admissible Jacobi Pair Compatibility

Covariance gives:

```text
T_{i+6} = rho(T_i)
```

Telescoping gives:

```text
sum_i T_i = 0.
```

The missing anchor is `rho(T_0)=T_0`.  The admissible Jacobi theorem might
force this anchor by removing the trivial `C/E` component after `B/C` trace.
The old anchor-vs-C boundary warns that this is not automatic; the selected
child profile must still be controlled.

### C. Fixed-Frequency Augmentation + Internal Character Filter

Earlier fixed-frequency work reduced no-fixed-defects to an order-7
augmentation identity over:

```text
R_7 = F_p[y]/(y^7-1).
```

The internal-character theorem is also a six-nontrivial-character vanishing.
It may be the same order-7 augmentation seen after internal `B/C` trace.  A
fresh agent should check whether the admissible Jacobi pair compatibility
implies the old augmentation identity, or conversely whether the augmentation
identity supplies the missing right-axis projector vanishings.

### D. Paired-Kernel Criterion + Admissible Span

The paired-kernel criterion says the right H-trace leakage need not vanish
before pairing; it is enough that the six nonfixed projectors land in the
selected left kernel:

```text
A(Pi_k L_0)=0, k=1,...,6.
```

The admissible Jacobi span is stronger than forbidden-support zero.  It may
give a structured reason for those six leakage vectors to land in the left
kernel even if the raw right-resolvent potential is too strong.

### E. Two-Resultant Surface + Fixed-Frequency Theorem

The two-resultant surface wants p-unitness of `det(Psi_RS)` and one crossed
norm.  The fixed-frequency H-coset theorem is currently being developed as a
way to prove the fixed determinant.  If a Jacobi/internal-trace identity is
proved, check whether it gives:

```text
fixed-frequency tail-in-prefix relations
=> no fixed defects
=> det(Psi_RS) p-unit.
```

This is the path from the 1092 verifier interface back to the 4-field-element
certificate surface.

## Useful Computation From Here

Computation is useful, but only as a theorem microscope.

High value:

```text
1. Materialize faithful selected weighted packets in small two-axis analogues.
2. Test rank-621 admissible-span membership and broad-rank leak coordinates.
3. Mine positive cases for conjugate-C-pair formulas.
4. Test whether adjacent-difference traces are exactly the conjugate-pair
   compatibility equations.
5. Test the four explicit Fourier condition families directly.
6. Formalize finite handoffs in Lean once the statement is precise.
```

Low value:

```text
1. Full p24 class-set enumeration.
2. Generic actual-CM rows without selected trace-GCD weighting.
3. Support-only tests that do not check admissible-span membership.
4. Post-fit interpolation or post-fit displacement operators.
5. Broad literature-style slogans unless they name the selected packet.
```

If compute is free, run many small analogues in parallel, but make the output
answer one of these questions:

```text
does the selected weighted packet lie in the admissible span?
what are the residual leak coordinates?
do conjugate C/E pairs satisfy a recognizable formula?
does the same formula imply the right-difference/anchor theorem?
```

## Lean Use From Here

Use Lean heavily for finite scaffolding:

```text
admissible decomposition => no forbidden bidegrees;
no forbidden bidegrees <=> final internal trace zero;
final internal trace zero => right coboundary;
right coboundary + left covariance => product coboundary;
ordinary centering + six characters => 1092 verifier equations;
rank/count/payload inequalities.
```

Do not use Lean as a discovery engine for the CM identity.  The useful pattern
is: discover a candidate theorem in mathematics/computation, then ask Lean to
make the handoff airtight.

## Recommended Read Order

For a fresh agent:

```text
1. p24/00_HANDOFF_INDEX_20260607.md
2. p24/00_FRESH_AGENT_HANDOFF_20260607.md
3. p24/00_RETROSPECTIVE_SYNTHESIS_20260606.md
4. p24/00_CURRENT_CONTEXT.md
5. p24/00_GLOBAL_SYNTHESIS_HANDOFF.md
6. p24/00_THEOREM_ATTEMPTS_LEDGER.md
7. p24/00_ROUTE_MAP.md
8. p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_decomposition_theorem.md
9. p24/trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate.md
10. p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary.md
11. p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.md
12. p24/trace_gcd_fixed_frequency_p24_dual_condition_source_map.md
13. p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
14. p24/trace_gcd_fixed_frequency_p24_value_identity_strength_gate.md
15. p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.md
16. p24/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.md
17. p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.md
18. p24/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md
19. p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.md
20. p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.md
21. p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.md
22. p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.md
23. p24/trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary.md
24. p24/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.md
25. p24/lean/TraceGcdJacobiAnchorCorrectionGate.lean
26. p24/lean/TraceGcdReducedAnchorAdjacentBridgeGate.lean
27. p24/lean/TraceGcdReducedAnchorSliceDecompositionGate.lean
28. p24/lean/TraceGcdDualConditionsValueSideGate.lean
29. p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
30. p24/lean/TraceGcdAdmissibleJacobiDecompositionGate.lean
```

Open older route files only when the synthesis says they are relevant.

## Do Not Reopen Without A New Ingredient

Avoid retrying:

```text
generic CM covariance;
plain Stickelberger;
generic Jacobi carries;
trace-only anchor compression;
post-fit sections or operators;
class-set enumeration;
abstract cyclic tower root selection;
ordinary left-character pairing as the whole proof.
```

Reopen only if the new ingredient is explicitly:

```text
selected weighted packet structure;
conjugate-C/E pair compatibility;
embedded CM/Lang potential;
p-integral determinant-line transport;
or a producer-sound selected recovery polynomial.
```

## Current Honest Status

We are not blocked and not done.

We are closer in formulation:

```text
the proof target is narrow, finite handoffs are mostly formal,
and the negative controls are informative.
```

We are still highly uncertain in proof:

```text
no actual CM/Lang producer for the selected weighted packet has been found.
```

The next agent should not branch randomly.  They should try to prove or
falsify the selected-packet conjugate-`C/E` pair compatibility theorem, and
then plug it into the already-built verifier pipeline.
