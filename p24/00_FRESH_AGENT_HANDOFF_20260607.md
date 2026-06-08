# p24 Fresh-Agent Handoff

Date: 2026-06-07

Purpose: compress the global state after the long exploration.  This is the
file to read when the research feels branchy.  It is deliberately structural:
what is proved, what failed, what composes, and where the remaining theorem
has to enter.

There are currently more than a thousand p24 files.  Do not reload them all.
Start with `00_HANDOFF_INDEX_20260607.md`, then use this file,
`00_FRESH_EYES_SYNTHESIS_20260607.md`,
`00_RETROSPECTIVE_SYNTHESIS_20260606.md`, `00_CURRENT_CONTEXT.md`,
`00_GLOBAL_SYNTHESIS_HANDOFF.md`,
`00_THEOREM_ATTEMPTS_LEDGER.md`, and `00_ROUTE_MAP.md` as the map.

If context is tight, read the index and
`00_FRESH_EYES_SYNTHESIS_20260607.md` first; that pair is now the compact
restart point.

## One-Sentence State

We have not found the certificate yet, but the live proof target has narrowed
from a vague CM-root selector to a concrete product-formula theorem for a
selected weighted packet on `C_7 x C_179`.

The small verifier is no longer the hard part.  The hard part is producing the
arithmetic identity that makes the selected CM/Lang packet land in the right
rank-621 subspace.

## Fixed Data To Keep In Working Memory

```text
p = 10^24 + 7
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441
sqrt_floor = 10^12

E = F_p(mu_m), [E:F_p] = 5460
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7
rho = p^780 has right quotient shift 6 mod 7
```

The class group is cyclic and squarefree.  This is useful for indexing the
`2,157,211,3107441` layers, but it does not select embedded child roots above
the split prime.  Root selection still needs a real embedded phase, norm, or
product formula.

## The Certificate Surfaces

### Surface 1: Four Field Elements

Best final payload if the producer theorems are proved:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

This is about `4e-12 * sqrt(p)`.

Missing arithmetic producers:

```text
fixed orbit:      det(Psi_RS) is a p-unit
nonzero orbit:    Nrd_O(Phi_t) is a p-unit
```

Diamond/unit-2 transport and finite determinant-line logic are in good shape,
but they are conditional on these p-unit producers.

### Surface 2: Fixed-Frequency H-Coset Verifier

Verifier interface:

```text
156 left rows * 7 right H-cosets = 1092 scalar equations
```

Compressed form:

```text
48 independent equations = 42 mixed octic + 6 anchor
```

This is not a sample count.  It is a finite handoff surface for a theorem about
the selected weighted packet.  The current rank-621/product-formula target
lives here.

### Surface 3: Selected-Chain Fallback

Payload scale:

```text
selected chain:      3107811 slots = 3.107811e-6 * sqrt(p)
full relative table: 3174011 slots = 3.174011e-6 * sqrt(p)
```

This is sub-sqrt for this `p`, but still lacks a producer that avoids dense
class-set enumeration.  Treat it as a fallback, not the main proof.

## Main Dependency Spine

The current strongest route is this implication chain:

```text
construct product-formula packet U(r,c)
  => raw identities for g(r,c)
  => selected-defect identities for f(r,c)=g(r,c)-g(r,0)
  <=> 632 Fourier conditions on C_7 x C_179
  <=> rank-621 admissible C-axis Jacobi span
  => no forbidden bidegrees C_7^nontrivial x {C/E trivial}
  => Tr_{C/E}(Tr_{B/C}(Pi_chi packet)) = 0 for six chi
  => right coboundary / product-coboundary finite handoff
  => H-coset verifier equations
```

The finite arrows in this chain are mostly gated by Python exact models and
Lean companion files.  The first arrow is the missing theorem.

Do not confuse the formal arrows with the arithmetic producer.  A fresh proof
must construct `U` or directly prove the equivalent identities for the actual
selected weighted packet.

## Current Missing Theorem In Its Cleanest Form

Let `g(r,c)` be the raw post-`Tr_{B/C}` packet on:

```text
C_7 x C_179
```

and let:

```text
f(r,c) = g(r,c) - g(r,0).
```

It is enough to prove:

```text
g(r,0)+g(-r,0)=A_0
g(r,c)+g(-r,-c)=A_1 for c != 0
sum_c g(r,c)-179*g(r,0)=B independent of r
```

Equivalently, for a multiplicative lift `U(r,c)=omega^g(r,c)`, prove:

```text
U(r,0)U(-r,0)=alpha_0
U(r,c)U(-r,-c)=alpha_1 for c != 0
prod_c U(r,c)/U(r,0)^179 = beta
```

This is the best current statement because it looks like a modular-unit,
elliptic-unit, Siegel/Ramachandra-unit, or CM-Lang product formula:

```text
constant pair-products + constant selected row-product ratio.
```

## Equivalent Fourier/Jacobi Form

For Fourier coefficients `F(a,b)` on `C_7 x C_179`, the same target is:

```text
1. F(a,0)=0 for a=1,...,6
2. F(a,b)+F(-a,-b)=0 for a != 0 and b up to C/E conjugate pairs
3. F(0,b)+F(0,-b)=lambda_179*F(0,0)
4. sum_{b>0}(F(-a,b)-F(a,b))=0 for a=1,2,3
```

where:

```text
lambda_179 = -1/89.
```

Counts:

```text
6 + 6*89 + 89 + 3 = 632 equations
ambient dimension = 7*179 = 1253
solution dimension = 621
```

Constructively, the same condition says the post-`Tr_{B/C}` packet lies in the
rank-621 admissible C-axis Jacobi-carry span.  The admissible carry is:

```text
theta_{u,v}(t) = [ut] + [vt] - [(u+v)t]

u right-trivial and C/E-nontrivial
v C/E-nontrivial
u+v C/E-nontrivial
```

The broader C-axis family has rank `625`, but has four leaky directions.  Use
rank `621` unless the proof explicitly cancels those four leaks.

## What Is Actually Proved

High-confidence finite/formal facts:

```text
admissible carries satisfy the four Fourier families;
four Fourier families <=> three value-side identities;
three value-side identities <=> rank-621 admissible span;
rank-621 admissible span => forbidden bidegrees vanish;
forbidden bidegree vanishing => final internal trace zero;
final internal trace zero gives the Hilbert-90/right-coboundary handoff;
matching right coboundary + left covariance gives product coboundary;
ordinary centering + six nontrivial characters gives the 1092 verifier.
```

Important exact numerical outputs:

```text
p24_admissible_c_axis_carry_rank_formula = 621
p24_broad_c_axis_carry_rank_formula = 625
p24_broad_minus_admissible_rank = 4
p24_dual_solution_dim = 1253 - 632 = 621
p24_zero_plus_inversion_rank = 7*89 + 6 = 629
p24_row_sum_extra_after_zero_plus_inversion = 3
```

The Lean files are scaffolding, not producer proofs.  Use them to make finite
handoffs airtight after a candidate arithmetic theorem has been stated.

## What Is Not Proved

Still missing:

```text
an explicit product-formula packet U(r,c);
a p-integral admissible Jacobi-carry decomposition of the selected packet;
a direct proof of the three raw identities for g(r,c);
p-unitness of det(Psi_RS);
p-unitness of one nonzero crossed norm Nrd_O(Phi_t);
a selected-chain recovery polynomial that avoids class enumeration.
```

The current work is therefore closer in formulation, not close enough to call
success.

## Negative Evidence That Should Change Future Search

The old branches did not fail randomly.  They all point to the same rule:

```text
generic CM structure is too weak; the selected weighted trace-GCD packet must
be used.
```

Known failures:

```text
abstract cyclic squarefree tower: no embedded child-root selector
generic CM covariance: gives eigenspaces, not zero
formal right-character covariance: obstruction eigenspace, not a potential
plain Stickelberger/right-axis Stickelberger: leaks forbidden bidegrees
generic Jacobi carries: leak unless in the admissible C-axis subfamily
anchor zero alone: can hold while C/E-trivial bidegrees leak
C/E-centering alone: can hold while selected-child anchor fails
selected defect alone: only forces f(r,0)=0
post-fit interpolation/operators: not intrinsic producer evidence
```

Actual-CM boundary data to remember:

```text
D=-4751: 0/91 full mixed/anchor/recombined-balance shifts
D=-5000: 0/60 raw packets with zero trivial C projection
D=-6719: covariance and telescope hold, anchor descent fails
D=-13319: right-combo/product internal traces and anchor fail
D=-13319 selected defects: 140/140 force C-zero fiber, 0/140 full identities
```

So a new theorem that says "for every embedded CM packet" is almost certainly
false.  A viable theorem must name the selected weighted trace-GCD packet, an
explicit CM/Lang unit, or a specific principal divisor.

## Facts That Now Compose

1. The selected defect is useful but incomplete.  It gives the C-zero fiber for
free, reducing the hard part to inversion complement plus three global
balances.

2. The admissible Jacobi DFT formula explains the magic constants.  In
particular `lambda_c=-2/(c-1)`, so `lambda_179=-1/89`, and conjugate skew
comes from sawtooth pair-sum cancellation.

3. The value-side rank split shows the proof can be separated:

```text
structural symmetry: 629 equations
three global balances: final 3 equations
```

This suggests two arithmetic sources: an involution/product complement for the
structural part, and a distribution/residue/product formula for the three
balances.

4. Literal finite-field Jacobi sums now explain only part of this split.  In
small `N=7c` probes, raw Jacobi sums
`J(chi^(u*t),chi^(v*t))` satisfy the off-`C=0` inversion pair-product
complement in every sampled admissible row, but they do not make the
selected row-product ratio constant.  The lone sampled row-ratio hit is the
right-trivial `(u,v)=(7,7)` case; the right-mixed samples have `0/7` row-ratio
hits in each small degree.

5. The row-ratio failure is now localized.  For right-mixed Jacobi sums, the
selected row-product ratio is constant on the six nonzero right rows; only
the right-zero anchor differs.  The anchor defect is universal across sampled
admissible pairs for each `c`, with exact finite-field formula
`delta_c=(q-2)^(-(c-1))`; it is not a small root-of-unity multiplier and has
no `c`-th root in the sampled value field.  Therefore a Jacobi-sum proof
should aim for a Hasse-Davenport punctured-right theorem plus a genuine
selected-anchor correction.

The newest literal Jacobi gate identifies that correction exactly in the
finite-field model: normalize only `U(0,0)=J(1,1)=q-2` by `(q-2)^(-1)`.
This single anchor change repairs both C-zero pair-products and the selected
row-product ratio exhaustively for the c=5,11,13 right-mixed admissible
probes.  For p24, the missing object is the selected trace-GCD/CM-Lang
analogue of this degenerate-anchor unit after `Tr_{B/C}`.

6. The right-difference/telescope route probably belongs to the anchor/global
balances, not to the entire 632-equation system.  This is the cleanest place
to compose old covariance work with the new Jacobi picture.

7. The product-coboundary/Hilbert-90 machinery is formal after internal trace
zero.  Do not try to find the Hilbert-90 potential first; that is circular
unless the product formula already gives trace zero.

8. CS/ML imports are mostly useful for the determinant/rank-condenser side,
not for certifying the CM product formula.  They can propose minors or hidden
rank condensers, but any result must become a p-unit or exact finite-field
identity.

## Best Next Proof Program

Try to construct `U(r,c)` explicitly.

A plausible mathematical shape is:

```text
U(r,c) = quotient/product of Siegel, Ramachandra, elliptic, or CM-Lang units
         indexed by the selected right coordinate r and internal C coordinate c
```

The theorem should be proved at the divisor/product-formula level:

```text
inversion divisor cancellation
  => U(r,c)U(-r,-c) is constant off c=0

C-axis distribution relation or residue theorem
  => prod_c U(r,c)/U(r,0)^179 is constant in r
```

Then specialization at the selected prime above `p` should give the additive
identities for `g`.

The proof has to check p-integrality.  A beautiful divisor identity that
introduces a denominator divisible by the selected prime does not certify the
DANGER instance.

## Useful Computation Now

Computation should be a theorem microscope:

```text
materialize faithful small two-axis selected weighted analogues;
report the four Fourier-family residuals separately;
report the value-side residuals separately;
test whether right-difference traces equal the three global balances;
mine candidate unit/divisor exponents from positive small cases;
use exact symbolic/rational arithmetic where possible.
```

Avoid:

```text
full p24 class-set enumeration;
generic actual-CM rows without the selected trace-GCD weighting;
support-only checks;
large jobs whose output is only another pass/fail bit;
post-fit sections presented as producer evidence.
```

## Lean Use Now

Lean is productive for the finite implication chain:

```text
product identities => value identities;
value identities => four Fourier families;
four Fourier families => admissible span;
admissible span => forbidden-support zero;
forbidden-support zero => internal trace zero;
internal trace zero => verifier handoff;
payload count inequalities.
```

Lean is not likely to discover the CM product formula.  Use it once the theorem
statement is sharp enough that all objects are explicit.

## Minimal Fresh-Agent Read Queue

Read in this order:

```text
1. p24/00_HANDOFF_INDEX_20260607.md
2. p24/00_FRESH_AGENT_HANDOFF_20260607.md
3. p24/00_RETROSPECTIVE_SYNTHESIS_20260606.md
4. p24/00_CURRENT_CONTEXT.md
5. p24/00_GLOBAL_SYNTHESIS_HANDOFF.md
6. p24/00_THEOREM_ATTEMPTS_LEDGER.md
7. p24/00_ROUTE_MAP.md
8. p24/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.md
9. p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.md
10. p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
11. p24/trace_gcd_fixed_frequency_p24_dual_condition_source_map.md
12. p24/trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate.md
13. p24/trace_gcd_fixed_frequency_jacobi_sum_product_formula_probe.md
14. p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_defect_theorem.md
15. p24/trace_gcd_fixed_frequency_jacobi_sum_anchor_correction_gate.md
16. p24/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md
17. p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.md
18. p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.md
19. p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.md
20. p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.md
21. p24/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.md
22. p24/lean/TraceGcdJacobiAnchorCorrectionGate.lean
23. p24/lean/TraceGcdReducedAnchorAdjacentBridgeGate.lean
24. p24/lean/TraceGcdReducedAnchorSliceDecompositionGate.lean
25. p24/lean/TraceGcdDualConditionsValueSideGate.lean
26. p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
```

Open older route files only when one of these notes points to them.

## Current Confidence

Closer:

```text
the goal is closer as a mathematical statement;
the finite verifier and equivalence stack are much cleaner;
the failure boundaries now strongly constrain the search.
```

Still uncertain:

```text
we do not yet have the product formula or p-unit producer;
generic CM data argues against any easy universal theorem;
success likely requires a new explicit CM/Lang unit identity or an equivalent
finite-field identity for this selected packet.
```

The next high-value move is proof synthesis around the multiplicative target,
not another broad branch.
