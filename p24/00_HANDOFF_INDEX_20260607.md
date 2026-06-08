# p24 Handoff Index

Date: 2026-06-07

Purpose: give a fresh agent the benefit of the whole p24 search without
loading the archive. Read this first, then load only the files named here.

## Current State

We do not have the final p24 certificate yet. We do have a much narrower
mathematical target than we started with:

```text
prove an explicit selected CM/Lang/Jacobi product identity after Tr_{B/C}
on C_7 x C_179, including one degenerate-anchor correction.
```

The verifier surface is small and the finite implication chain is strong. The
remaining risk is the arithmetic producer theorem, not the downstream checker.

## Read Order

Minimal queue:

```text
1. p24/00_HANDOFF_INDEX_20260607.md
2. p24/00_DREW_SUTHERLAND_ASK_MEMO.md
3. p24/00_FRESH_EYES_SYNTHESIS_20260607.md
4. p24/00_FRESH_AGENT_HANDOFF_20260607.md
5. p24/00_RETROSPECTIVE_SYNTHESIS_20260606.md
6. p24/00_CURRENT_CONTEXT.md
7. p24/00_THEOREM_ATTEMPTS_LEDGER.md
8. p24/00_ROUTE_MAP.md
```

Then, only if working the live theorem, read:

```text
p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_decomposition_theorem.md
p24/trace_gcd_fixed_frequency_jacobi_sum_punctured_hasse_davenport_theorem.md
p24/trace_gcd_fixed_frequency_jacobi_sum_symbolic_hd_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_fingerprint_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_adjacent_bridge_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_slice_decomposition_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_cyclotomic_divisor_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_diamond_norm_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_cyclic_vs_diamond_norm_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_elliptic_subgroup_divisor_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_polynomial_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_local_unit_criterion_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_resultant_avoidance_gate.md
p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_generator_invariance_gate.md
p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_final_curve_guardrail.md
p24/trace_gcd_fixed_frequency_reduced_anchor_kernel_section_pairing_guardrail.md
p24/trace_gcd_fixed_frequency_reduced_anchor_low_moment_pairing_window.md
p24/trace_gcd_low_moment_cm_selector_sweep.md
p24/trace_gcd_low_moment_sparse_relation_gate.md
p24/trace_gcd_low_moment_relative_trace_gate.md
p24/trace_gcd_low_moment_function_complexity_gate.md
p24/trace_gcd_low_moment_automatic_p1_entropy_gate.md
p24/trace_gcd_low_moment_truncated_polynomial_gate.md
p24/abstract_embedded_pairing_low_bidegree_scan.md
p24/trace_gcd_fixed_frequency_jacobi_anchor_kummer_descent_gate.md
p24/trace_gcd_p24_compressed_search_readiness.md
p24/p24_endofday_conditional_testing_20260607.md
p24/trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary.md
p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
p24/lean/TraceGcdJacobiAnchorCorrectionGate.lean
p24/lean/TraceGcdReducedAnchorAdjacentBridgeGate.lean
p24/lean/TraceGcdReducedAnchorSliceDecompositionGate.lean
p24/lean/TraceGcdReducedAnchorCyclotomicDivisorGate.lean
p24/lean/TraceGcdReducedAnchorDiamondNormGate.lean
p24/lean/TraceGcdReducedAnchorCyclicVsDiamondNormGate.lean
p24/lean/TraceGcdReducedAnchorEllipticSubgroupDivisorGate.lean
p24/lean/TraceGcdReducedAnchorKernelPolynomialGate.lean
p24/lean/TraceGcdReducedAnchorLocalUnitCriterionGate.lean
p24/lean/TraceGcdReducedAnchorResultantAvoidanceGate.lean
p24/lean/TraceGcdAdjacentAnchorCyclicDivisibilityGate.lean
p24/lean/TraceGcdReducedAnchorKernelGeneratorInvarianceGate.lean
p24/lean/TraceGcdReducedAnchorKernelFinalCurveGuardrail.lean
p24/lean/TraceGcdReducedAnchorKernelSectionPairingGuardrail.lean
p24/lean/TraceGcdReducedAnchorLowMomentPairingWindow.lean
p24/lean/TraceGcdLowMomentSparseRelationGate.lean
p24/lean/TraceGcdLowMomentRelativeTraceGate.lean
p24/lean/TraceGcdLowMomentAutomaticP1Gate.lean
p24/lean/TraceGcdLowMomentTruncatedPolynomialGate.lean
p24/lean/TraceGcdAnchorKummerDescentGate.lean
```

If context is tight, read only this index and
`p24/00_DREW_SUTHERLAND_ASK_MEMO.md` before choosing a narrow route.  The ask
memo is the most compact statement of the current missing theorem: selected
unramified `157/211` phase production, or an obstruction to such a bounded
selector.  If doing local proof work rather than external synthesis, read
`p24/00_FRESH_EYES_SYNTHESIS_20260607.md` next.  That note groups the failed
routes by failure mode, composes the Jacobi/Hasse-Davenport and
adjacent-anchor findings, records the diamond-norm residual candidate
`Phi_179(X)/(X-1)^178`, and separates the compressed verifier surface from the
still-missing producer.

Avoid reading all of `p24/`: current archive size is:

```text
files total:       1401
markdown notes:     582
python probes:      654
lean gates:         136
```

## Fixed Data

```text
p = 10^24 + 7
sqrt_floor = 10^12
t = -1178414874616
D_K = -652834595820939249713143
h = 205880396014 = 2 * 157 * 211 * 3107441
m = 66254 = 2 * 157 * 211
n = 3107441

E = F_p(mu_m), [E:F_p] = 5460
B/E degree = 5549 = 31 * 179
B/C degree = 31
C/E degree = 179
right quotient = C_7
rho = p^780 fixes the left 157-frequency and shifts the right quotient by 6
```

## Certificate Scales

```text
best conditional final payload:
  4 field elements:
  Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}

current fixed-frequency verifier:
  1092 scalar equations = 156 left rows * 7 right H-cosets
  compressed as 48 independent equations = 42 mixed octic + 6 anchor

selected-chain fallback:
  3107811 slots = 3.107811e-6 * sqrt(p)
```

The `1092` number is not a sample count and not the final payload size. It is
the finite H-coset verifier interface for the selected weighted packet.

## What Is Proved Or Strongly Gated

Finite/formal chain:

```text
raw product identities
  => selected-defect value identities
  <=> four Fourier families on C_7 x C_179
  <=> rank-621 admissible C-axis Jacobi span
  => forbidden C-trivial bidegrees vanish
  => final internal trace zero
  => right/product coboundary handoff
  => 1092 H-coset verifier equations
```

Key exact numbers:

```text
ambient dimension = 7 * 179 = 1253
dual condition count = 632
admissible span dimension = 621
broad C-axis span dimension = 625
leaky directions in broad span = 4
```

Latest cheap harness verification:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory

task_count=264
passed=264
failed=0
```

The new local-unit criterion gate is included in that sweep.  It records the
sharp finite local target:

```text
R_c(x)=Phi_c(x)/(x-1)^(c-1) is a unit iff x notin mu_c
K_H(T) is a unit iff T is neither O nor a nonzero point of H

p24 c = 179
forbidden cyclotomic anchor count = 179
```

Thus the producer obligation is now: construct the selected CM/Lang coordinate
or subgroup polynomial p-integrally, then prove its reduction avoids the
forbidden anchor/subgroup locus.

The resultant-avoidance bridge packages that post-producer check as one finite
algebra p-unit certificate.  If the selected coordinate is represented in
`F_q[T]/(M(T))` by `X(T)`, then:

```text
R_c(X) is a unit
  iff X(T)^c - 1 is a unit modulo M(T)
  iff Res(M(T), X(T)^c - 1) != 0
  iff a Bezout identity A*M + B*(X^c-1)=1 exists.

p24 c = 179
p24 forbidden polynomial degree = 179
p24 kernel polynomial degree = 89
```

So after a selected p-integral CM/Lang coordinate is produced, the reduced
anchor can be verified without enumerating or adjoining all `179` roots of
unity.

The adjacent-anchor target is also compressed one step further.  If the
single anchor's rho-orbit coordinates are written as
`A(y)=a_0+...+a_6 y^6`, then:

```text
rho(T_0)=T_0
  iff a_0=...=a_6
  iff A(y) is a scalar multiple of Phi_7(y)=1+...+y^6
  iff A(y) == 0 mod Phi_7(y).
```

Thus the six nontrivial anchor projectors are one cyclic divisibility check.
Together with pointwise covariance and telescoping, this proves the `48`
compressed right-difference equations once the selected CM/Lang adjacent
anchor polynomial has been produced.

Latest bounded p24-real split-cycle search:

```text
p24/composite_split_cycle_norm_gap_206498.md
p24/composite_split_cycle_ramified_norm_gap_206498.md

split_prime_logs=9265
exhaustive_signed_prime_power_products_norm_le_206497
  index_66254: none
ramified_prime=599 included
exhaustive_signed_split_or_ramified_prime_power_products_norm_le_206497
  index_66254: none
```

This closes the gap below the known recovery representative
`2 * 463 * 223^(-1)` of norm `206498`; no smaller signed
split-prime-power representative for the order-`3107441` recovery class was
found in that model, even after adding the ramified prime `599`.

Latest low-moment selector testing:

```text
focused p24 entropy gate:
  first layer 4 moments, second layer 26 moments, total 30
  random F_101 control: 1820 -> 20 -> 1 candidates by degrees 1,2,3
  D=-5000 tower: degree-1 power sum already selects both top children

actual-CM sweep, default:
  rows=19
  rows_all_unique_within_degree_bound=19
  rows_unique_at_degree_one=14
  rows_unique_no_later_than_random_entropy=16

actual-CM sweep, wider:
  rows=65
  rows_all_unique_within_degree_bound=65
  rows_unique_at_degree_one=43
  rows_unique_no_later_than_random_entropy=52

actual-CM sweep, end-of-day widened:
  rows=218
  rows_all_unique_within_degree_bound=218
  rows_unique_at_degree_one=131
  rows_unique_no_later_than_random_entropy=173

actual-CM sweep, additional end-of-day control:
  rows=103
  rows_all_unique_within_degree_bound=103
  rows_unique_at_degree_one=65
  rows_unique_no_later_than_random_entropy=82

sparse-relation dictionary:
  equal low-moment subsets are disjoint signed relations on the moment curve
    after canceling overlap
  Newton identities forbid reduced collisions of size <= k
  p24 first layer with k=4 only needs to rule out relation sizes 5..157
  p24 second layer with k=26 only needs to rule out relation sizes 27..211
  union entropy still favors 4+26 moments:
    first_layer_union_over_two_parents_log10=-2.522422
    second_layer_union_over_314_parents_log10=-4.721562

  relative-trace constructor target:
  child power sums are relative traces Tr(Y^d) of quotient-period powers
  D=-5000 tower verifies Newton recovery from all relative-degree traces
    and degree-1 uniqueness in the toy
  p24 selected-path nominal target is 30 selected relative traces
  two P1 values are automatic from the selected parent chain
  p24 genuinely new higher selected relative traces = 28
  P1 still remains an anti-collision/verifier constraint:
    higher-only entropy is positive at p24 scale
    first layer higher-only log10 collisions = 21.176548
    second layer higher-only log10 collisions = 16.781509
  small-CM controls: higher moments have full interpolation degree for all
    tested parent_count >= 3 rows
  parent-field moment-function surface is 8172 coefficients

  truncated child-polynomial dictionary:
  by Newton identities the 30 low power-sum constraints are equivalent to
    the first 30 elementary coefficients in the two selected child layers
  e1 on each layer is the parent period and is already carried
  p24 producer can target 28 new coefficients:
    first layer e2..e4 = 3
    second layer e2..e26 = 25
  selector still uses the two parent/e1 constraints
```

Latest producer-facing selected-prime controls:

```text
relative_resultant_selected_prime_scan, widened with origin shifts:
  packet_rows=23906
  unique_packet_rows_ignoring_origin=1248
  coord_zero_packets=0
  distinguished_zero_packets=0
  content_zero_packets=0

relative_resultant_selected_prime_scan, additional end-of-day control:
  packet_rows=12211
  unique_packet_rows_ignoring_origin=755
  coord_zero_packets=0
  distinguished_zero_packets=0
  content_zero_packets=0

packetized_content_selected_prime_scan, same window:
  packet_rows=23906
  unique_packet_rows_ignoring_origin=1248
  coord_zero_packets=0
  content_failures=0
  energy_zero_packets=0
  hermitian_zero_packets=0

relative_packet_factor_shape_scan:
  zero_hits=0
  prime_zero_hits=0
  composite_zero_hits=0

upstream DANGER3 pp24 small-prime control:
  pp24.txt.gz ends at p=16777213 and contains no p=10^24+7 candidate
  direct point-count recovery for p<30000:
    rows=3243, misses=0
    trace-bucket ranks={0:328, 1:2371, 2:544}
    for p congruent to p24 mod 64:
      n=104, ranks={0:13, 1:83, 2:8}
  simple residue filters mod m<=128 look like small-sample artifacts, not a
    robust p24 lower-bucket filter.
```

These are not p24 certificates.  They are small-CM/finite-field evidence that
the current product/resultant packet target has no cheap selected-prime
counterexample or imprimitive recurrence escape in the widened test window;
the upstream small-prime triples likewise do not supply a direct p24 search
surface.

Latest abstract-to-embedded pairing stress test:

```text
p24/abstract_embedded_pairing_low_bidegree_scan.md

D=-2239, q=2243, quotient n=7:
  support 6 bidegree (2,1)/(1,2): 0/5040 matchings in both orientations
  support 9 bidegree (2,2): 5040/5040 matchings, same as random controls

summary:
  rows=16
  low_support_rows=8
  actual_low_support_rows_with_pairing=0
  random_low_support_control_hits=0

meaning:
  plain abstract quotient roots do not expose a below-generic bidegree phase
  pairing with embedded quotient periods in these non-genus controls.
```

## Latest Positive Clue

Literal finite-field Jacobi sums explain most of the live target. For
right-mixed admissible Jacobi packets with `N=7c`:

```text
off-C-zero pair-products work;
the selected row-product ratio is already constant on the six nonzero
  right rows;
only the right-zero anchor differs.
```

The exact defect is:

```text
delta_c = (q - 2)^(-(c - 1))
```

because:

```text
J(1,1)=q-2
J(1,lambda)=-1 for lambda nontrivial
```

The correction is exact in the finite-field model:

```text
U(0,0)=J(1,1)=q-2
U'(0,0)=U(0,0)/(q-2)=1
```

Changing only this one anchor repairs both the C-zero pair-products and the
selected row-product ratio, exhaustively for `c=5,11,13`. The symbolic
Hasse-Davenport gate then proves the punctured nonzero-row algebra without
finite-field summation, including all `189036` p24 right-mixed admissible
pairs for `c=179`.

An exhaustive scalar search now tries every replacement value `x` for the
single degenerate anchor in the small Jacobi value fields.  The only values
working for every right-mixed admissible packet are:

```text
x = +1 or x = -1.
```

So the anchor-side search space has collapsed to the `R_179` CM/Lang
realization plus a final sign normalization, not a large scalar search.

A follow-up factor search shows the reduced-anchor split should not be
realized as two independent base-field multiplicative factors.  Separating the
row-sum slice from the `R_c` residual requires a `c`-th root of the selected
anchor scalar; neither valid sign branch has that root in the small Jacobi
value fields.  The p24 proof should therefore use divisor/norm language or an
auxiliary extension whose final norm descends p-integrally.

The positive replacement is now gated.  In an auxiliary Kummer extension with
`beta^c=s`, the row-sum slice and `R_c` residual split; their product descends
to the base selected correction; and the selected correction forces the
`R_c` exponent to be `e=1`.  For p24, the live target is therefore:

```text
construct a p-integral auxiliary Kummer/norm/divisor realization of
R_179 = Phi_179(X)/(X-1)^178,
with exponent e=1 and final +/- sign normalization.
```

For p24, the remaining object is:

```text
identify the selected trace-GCD/CM-Lang analogue of the J(1,1)/(q-2)
degenerate-anchor unit after Tr_{B/C}.
```

The reduced-anchor / adjacent-anchor bridge makes the old covariance route
more precise.  The adjacent-anchor descent theorem sees the `C/E`-trivial
row-sum slice of the reduced anchor:

```text
A=(179-1)e_0 on C_7.
```

That slice has all six nontrivial right projectors nonzero, and adjacent
difference multiplies each by a nonzero scalar.  So the old adjacent-anchor
target is exactly cancellation of the reduced anchor's `b=0` leak, not a
separate arithmetic miracle.

The slice decomposition then separates what remains.  After the `b=0`
row-sum slice, the reduced anchor still has a `C/E`-nontrivial residual with
zero row sums and Fourier profile:

```text
H(a,0)=0,
H(a,b)=-1 for b != 0.
```

For p24 this residual has `7*(179-1)=1246` nonzero `C/E`-nontrivial Fourier
channels.  This part is invisible to the old adjacent-anchor theorem and must
come from the actual selected CM/Lang unit realization.

The newest divisor gate makes that residual concrete.  After multiplying by
`c`, the residual is the degree-zero principal divisor

```text
sum_{k != 0} [zeta_c^k] - (c-1)[1]
  = div(Phi_c(X)/(X-1)^(c-1)).
```

For p24, the candidate residual unit is:

```text
R_179(X) = Phi_179(X)/(X-1)^178.
```

This is now checked for `c=5,11,13,17,19,179`; the remaining arithmetic input
is the selected CM/Lang specialization and p-integrality theorem.

The diamond-norm gate sharpens the divisor statement: the denominator-cleared
`R_179` residual is the diamond norm over `(Z/179Z)^*` of the single one-point
divisor `[zeta_179]-[1]`.  This is a 178-term unit/diamond norm, not the
cyclic `C/E` trace norm.

The cyclic-vs-diamond norm gate closes the nearest false implementation:
ordinary cyclic translations of `[zeta_c]-[1]` telescope to the trivial
divisor/product `1`, while diamond multipliers give the nontrivial `R_c`
residual.  For p24 this separates the cyclic orbit of size `179` from the
diamond orbit of size `178`; a producer using the cyclic `C/E` trace norm
would erase the selected-anchor residual.

The elliptic-subgroup divisor gate corrects the producer wording if the
realization is through elliptic/Siegel units: `[P]-[O]` is not a principal
elliptic divisor for nonzero torsion `P`.  The whole odd subgroup divisor
`sum_{Q in H, Q != O}[Q]-(c-1)[O]` is principal because its degree and
Abel-Jacobi sum are zero.  For p24 this means the live target is a direct
p-integral CM/Lang specialization of the `178`-zero subgroup/diamond divisor,
or a descended cyclotomic coordinate; not an individual elliptic one-point
factor.

The kernel-polynomial gate makes that subgroup divisor explicit.  For odd
cyclic `H`, the monic polynomial
`K_H(x)=prod_{Q in (H\{O})/{+-1}}(x-x(Q))` has divisor
`sum_{Q != O}[Q]-(c-1)[O]`.  It was checked on small finite elliptic curves
for `c=5,7,11,13,17,19` and formally for `c=179`; for p24
`deg K_H=89` and the pole order is `178`.  The squared kernel polynomial is
the Vélu `x`-denominator shape, but the unsquared `K_H` is the reduced-anchor
residual target.

Latest p24 sharpening: `p mod 179 = 77`, `ord_179(p)=89`, and
`-1 notin <p>`.  Thus the `178` diamond exponents split into two reciprocal
Frobenius half-orbits of degree `89`, and the inversion quotient is one
real-cyclotomic object.  With `S_0=2`, `S_1=Y`,
`S_{k+1}=Y*S_k-S_{k-1}`,

```text
Psi_179(Y)=1+sum_{k=1}^{89}S_k(Y),
Phi_179(X)=X^89 Psi_179(X+X^{-1}).
```

An ephemeral finite-field check over the actual `F_p` found `Psi_179`
irreducible: `gcd(Psi_179,Y^p-Y)=1` and
`Y^(p^89)=Y mod Psi_179`.  Therefore a future selected inversion-coordinate
producer can certify the nontrivial forbidden roots by one degree-`89`
resultant `Res(M, Psi_179(Y))`, instead of the oriented primitive-root part of
the degree-`179` test against `X^179-1`.  The basepoint/denominator condition
remains separate: `Psi_179(2)=179`, so this real-cyclotomic resultant does not
detect `X=1` or the elliptic `O` pole.

The Kummer split also simplifies after reduction.  Since `ord_179(p)=89` and
all named p24 finite-field degrees (`1,4,156,5460,5460*179,5460*5549,31,179`)
are nonzero modulo `89`, none contains `mu_179` and
`gcd(179,p^d-1)=1` for those fields.  The `179`th-power map is therefore a
multiplicative automorphism in the actual reduction fields, so the anchor
row-sum / residual split can use the unique `179`th root after a selected
producer is supplied.  This is a finite certificate/testing simplification,
not the missing p-integral producer.

The same degree fact collapses the local-unit check if the selected coordinate
is already in those named reductions:

```text
X^179=1 in F_{p^d}, d in {1,4,156,5460,5460*179,5460*5549,31,179}
  iff X=1.
```

Thus nontrivial `mu_179` avoidance is automatic on the named class-field side;
only the basepoint/denominator condition remains.  The degree-`89`
`Psi_179` resultant is still the right check for an auxiliary
real-cyclotomic/inversion-coordinate producer whose residue algebra may
contain the nontrivial roots.

If the selected CM/Lang producer identifies the corrected degenerate-anchor
value as `x=+/-1` and the Kummer descent scalar as
`s=(q-2)/x`, then this remaining basepoint condition also collapses after
reduction: `s=±2 mod p`, so `s != 1`; any named-field `beta` with
`beta^179=s` must satisfy `beta != 1`.  The unique roots of `±2` in `F_p`
were checked explicitly and are non-`1`.  Thus the local-unit proof would be
complete once the producer supplies the selected p-integral coordinate, the
corrected-anchor sign, and the Jacobi `q-2` Kummer scalar identification.

The kernel-generator-invariance gate corrects the candidate count.  The
oriented one-point divisors have `178` diamond conjugates and their
x-coordinates have `89` sign-paired choices, but all generator choices for a
fixed selected subgroup give the same `K_H`.  Conditional on constructing that
selected p-integral CM/Lang subgroup polynomial, the remaining deterministic
surface is just the two anchor signs with forced Kummer exponent `e=1`.

The kernel-final-curve guardrail prevents a wrong computation: for the selected
p24 trace, `179` does not divide `#E(F_p)`, and `t^2-4p` is a nonsquare modulo
`179`.  Thus the final curve has no `F_p`-rational `179`-torsion and no
`F_p`-rational `179`-isogeny/Vélu kernel polynomial.  The `K_H` target is an
auxiliary CM/Lang or cyclotomic quotient object, not a final-curve subgroup
enumeration.

The kernel-section-pairing guardrail prevents the opposite overread of the
same compression.  Generator choices collapse only after a selected auxiliary
fiber/section is already fixed.  For p24, choosing a degree-157 child from
314 quotient roots has `log10 binomial(314,157) = 93.176548`, and a single
trace/sum constraint still leaves random-scale ambiguity about `10^69`.
The producer still needs section pairing, relative class-character traces, an
embedded relative morphism, or an equivalent phase-aware CM/Lang identity.

Rechecking the classical Siegel/Ramachandra/Robert unit route against the
new `R_179` residual does not remove this obstruction.  Ray-unit
distribution relations collapse ray-kernel/congruence directions, while the
p24 `157` and `211` phases are conductor-one unramified Hilbert-class layers.
The refreshed `ray_kernel_distribution_audit.py` output still has
`ell_divides_mod_ell_kernel=0` for `ell=157,211`, and the tested squarefree
levels `157*211`, `2*157*211`, `223*463`, and `2*223*463` have no `157` or
`211` in their local unit parts.  Thus classical units can describe/certify
the residual once the selected auxiliary fiber is known; they do not select
that embedded fiber for free.

The finite selector lower-bound gate is the positive boundary.  It says any
single invariant constant on the third target's recovery coset must have
degree at least `3107441`; Lean verifies that
`3107441 < sqrt_floor(p)=10^12` and that the selected-chain payload
`2+157+211+3107441` is still sub-sqrt.  Therefore the surviving route is a
growing-degree embedded recovery object of degree about `3107441`, or an
equivalent p-unit/divisor identity, not a bounded-level Weber/Siegel/ray
shortcut.

Fresh rerun of the relative-coset recovery toy keeps the same boundary:
one degree-`|H|` coset polynomial recovers a target root after phase
selection, but the distinct coset polynomials are conjugate over the quotient
field and their product is the full class polynomial.  The p24 height audit
still says the third-trace degree `3107441` is only `3.107441e-6*sqrt(p)`,
but its principal-conjugate log-height proxy is about `5.08e12`; even a
`1/28` class-invariant height factor leaves about `1.81e11`.  So ordinary
complex/CRT computation of one coset polynomial is not the sub-sqrt producer;
the missing ingredient is direct mod-p embedded quotient phase or the
p-unit/divisor identity.

Latest centered p-unit route check: the phase-divisor holdout on the pinned
`D=-13319, q=13463, m=28, pair=(4,7)` row found
`nonrandom_span_hits=0`, `full_rank_interpolation_hits=4`,
`target_misses=2`, and `coordinate_payload_zero_detection_failure=1`.
Thus bounded right-binomial/Heegner phase-unit dictionaries are either misses
or full-rank interpolation, and coordinatewise/Kummer-only nonzero payloads
do not certify the determinant line.  In contrast, the centered
orbit-Fitting block-cycle audit still passes with zero mismatches:
orbit products equal both direct-sum and signed block-cycle Fitting
determinants, and singular controls zero exactly.  The live object is
therefore the phase-aware Schubert/Fitting determinant section, with a local
p-unit/nonintersection theorem, not an entrywise unit product.

The local Fitting criterion and p24 local invariant audits were refreshed:
Lean compiles `TraceGcdOrdinaryFittingCriterionGate.lean`, `p` is split
ordinary/unramified and prime to all certificate levels, and the selected
prime above `p` is principal on the Hilbert/ring-class side.  But that
principal Frobenius fixes the whole class torsor and does not pick a root;
Frobenius still has orders `156` on `zeta_157` and `35` on `zeta_211`.
Therefore ordinary base-polynomial descent remains false; the honest payload
is the semilinear crossed-product orbit norm/Fitting determinant.

The latest selected-Schubert/local-intersection pass adds four guardrails.
First, CM simple-root/different p-units and random Schubert transversality
are only hygiene/motivation.  Second, an exterior toy has determinant
cancellation despite all fixed coefficients and Plucker coordinates being
nonzero, so coordinatewise Kummer/Plucker p-units are insufficient.  Third,
the pinned actual-CM norm triangle verifies that scalar orbit products,
block-cycle Fitting determinants, and split norms agree while naive
base-polynomial descent fails.  Fourth, the phase-coordinate scan confirms
right-phase descent in the pinned row but p24 has full right exterior support
by subset size `3`; the safe theorem is still seven orbit Chow/Fitting norms,
not one hidden support orbit.

Latest determinant-bridge check: the residual Moore/Chow toy, the
Schur-complement toy, and the actual-CM trace-pairing/subspace audit all pass
with zero event mismatches.  They identify the trace-gcd determinant,
trace-pairing matrix, residual Moore product, Chow/Fitting section, and
Schur-complement pivot as equivalent representatives of the same local p-unit
target.  Thus the missing theorem may be stated as either trace-gcd
nonvanishing or Moore/Fitting p-unitness; do not reopen these equivalences as
separate branches.  The open arithmetic task is to prove a selected prefix
Moore p-unit and quotient-tail Moore/Schur p-unit, or an equivalent
phase-aware Schubert/Fitting nonintersection theorem, at the actual p24 CM
point.

The fixed-orbit producer has a sharper two-part statement after the latest
prefix/RS-tail checks.  Existing normal-basis and Gaussian-period gates show
that the prefix factor can be phrased as rank `140` of the trace-dual
coefficients
`Tr_{E/L}(eta_i * H_{157,211}(1,v_j))`, where `eta_i` is the type-6 Gaussian
normal basis of `F_p(mu_211)/F_p` and `j in {2,3,5,6}`.  Existing RS-tail
audits show the remaining `16` columns are exactly the quotient-tail
Schur/Moore factor after a p-unit prefix pivot.  A widened metric-aware
orbitwise Schur falsifier over `20` actual small-CM rows found no
`tail_zero`, `schur_fail`, Gram zero, or right-class mismatch.  This is still
not a p24 proof: singular controls in the same audits show the split is
faithful but not dimension-forced.

The prefix half has the cleanest current proof surface.  After scalar
extension to `K=F_p(mu_35)`, the Gaussian DFT target decomposes into four
Frobenius-shifted components.  The true condition is not component rank but
zero intersection of the twisted kernels.  Equivalently, with first component
map `M_0 : K^{35*4} -> L` and
`T(x)_{b,j}=x_{p^{-1}b,j}^p`, prove
`core_T(ker M_0)=0`.  Semilinear descent makes this equivalent to no nonzero
fixed relation in `F_p^28 + K^28 -> L`, to surjectivity of the fixed-adjoint
syndrome `L -> F_p^28 + K^28`, and to nonzero Moore residual for its `140`
coordinate elements.  Existing toys and Lean gates compile/pass for each
finite equivalence; the missing part is the arithmetic p-unit theorem for the
actual CM Gaussian frequency table.

The prefix-to-tail bridge is also finite-clean.  Prefix syndrome surjectivity
gives a `16`-dimensional residual kernel; the tail p-unit is exactly the
statement that the `16` RS-tail coordinates are injective on that kernel, or
equivalently that
`Delta_16(P_prefix(T_tail))` is nonzero after applying the p-linearized
annihilator of the prefix span.  The full fixed-orbit p-unit is therefore the
product of two named p-units:
`Norm(Delta_140(C_prefix))` and
`Norm(Delta_16(P_prefix(T_tail)))`.  The existing bridge toy and Lean gate
pass and include dependent-prefix and bad-tail controls.

The compressed-search readiness gate records the operational consequence:
the deterministic p24 residual product has `178` terms, but after passing to
the subgroup kernel polynomial those are not `178` generator candidates.  The
old p23 `X1(16)` nonsplit sampler is not a p24 fallback because `p mod 8 = 7`,
while that sampler requires `p mod 8 = 5`.  Without the selected p-integral
CM/Lang subgroup kernel polynomial, there is no honest compressed root search
to run.

A bounded generic `pomerance_probe` p24 smoke run checked `1000000` trials in
`7.67s` at about `0.130M` trials/sec/core and found no hit.  It confirms this
lane is only a lottery/throughput baseline, not an end-of-day route to the
asymptotic result.

## Negative Evidence To Respect

Do not restart these branches unless a new ingredient directly addresses the
listed failure:

```text
abstract cyclic squarefree class tower:
  gives unique subgroup layers but no embedded child-root selector
  widened fiber-map controls found no degree <= 2 rational maps and no
    degree <= 3 polynomial maps pairing abstract tower roots before embedding

generic CM covariance:
  gives eigenspaces, not zero

formal Hilbert-90 inversion:
  is circular unless trace zero is proved first

plain Stickelberger or broad Jacobi-carry slogans:
  leak forbidden C-trivial bidegrees

anchor-only or C/E-centering-only statements:
  can pass independently while the full target fails

actual-CM generic rows:
  repeatedly fail the mixed/anchor/recombined identities

bounded-level ray/Siegel/Ramachandra distribution:
  collapses ray kernels, not the unramified 157/211 Hilbert-class phases;
  surviving selectors must pay growing degree at least 3107441

bounded phase-unit dictionaries / coordinatewise Kummer payloads:
  fail the phase-divisor holdout or reduce to interpolation; determinant-line
  Fitting p-unitness remains necessary
```

Latest selected-chain/tower boundary:

```text
abstract_tower_fiber_map_scan, D=-671 and D=-815 controls:
  rational map degrees 1,2: maps_found=0 in both orientations
  polynomial degrees 1,2,3: polynomial_maps_found=0 in both orientations
  random controls: 0/30

meaning:
  even abstract roots are unpaired by small universal fiber maps before
  embedding; the selected-chain verifier still needs a genuine embedded
  phase theorem rather than cyclic tower labels.
```

Actual-CM boundary markers:

```text
D=-4751:   0/91 full mixed/anchor/recombined-balance shifts
D=-5000:   0/60 raw packets with zero trivial C projection
D=-6719:   covariance and telescope hold, anchor descent fails
D=-13319:  right-combo/product internal traces and anchors fail;
           no universal degree-<5 base/value-field relative-coordinate
           multiplier repairs the anchor across all 140 sections
D=-13319 selected defects:
            140/140 force C-zero fiber
              0/140 satisfy full identities
```

## Facts Worth Recombining

The strongest possible synthesis right now is:

```text
old right-difference/covariance branch:
  T_{i+6}=rho(T_i), sum_i T_i=0, missing rho(T_0)=T_0

new Jacobi/Hasse-Davenport branch:
  punctured nonzero-right rows already balance;
  one degenerate right-zero anchor cancels delta_179

possible composition:
  adjacent-anchor descent is cancellation of the C/E-trivial row-sum slice
  of the Jacobi right-zero degenerate-anchor normalization.
```

This composition is worth proving or falsifying before opening unrelated new
branches.

## Computation Policy

Computation is useful only as a theorem microscope:

```text
test named finite identities at small c;
separate the four Fourier-family residuals;
separate the three value-side residuals;
mine candidate unit/divisor exponents for the selected anchor;
use the reduced-anchor adjacent bridge as a check that the `b=0` slice matches
  the old right-difference anchor.
```

Avoid large jobs whose output is just another pass/fail bit. CPU is cheap, but
context is not.

## Lean Policy

Lean is productive for the finite handoff:

```text
product identities => value identities;
value identities => Fourier families;
Fourier families => admissible span;
admissible span => forbidden-support zero;
internal trace zero => coboundary/verifier handoff.
```

Lean is not expected to discover the CM/Lang unit. Use it once the theorem
objects are explicit enough to formalize.

## First Next Move

The finite bridge to the old adjacent-anchor route is now tested.  The next
move is to prove or falsify this arithmetic statement:

```text
The p24 selected weighted trace-GCD packet after Tr_{B/C} is the
specialization/log/divisor of a reduced Jacobi/CM-Lang packet whose punctured
Hasse-Davenport product formula gives the six nonzero right rows, and whose
single degenerate anchor supplies exactly the selected right-zero correction.
```

If that statement is true, the search space drops from sqrt(p)-scale
enumeration to a constant-size arithmetic identity plus the existing finite
verifier. If it is false, the next synthesis should explain which part fails:
punctured nonzero rows, selected anchor realization, p-integrality, or the map
from reduced Jacobi packet to the actual trace-GCD packet.
