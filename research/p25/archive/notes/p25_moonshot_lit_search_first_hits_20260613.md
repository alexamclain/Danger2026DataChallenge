# p25 Moonshot Literature Search First Hits

Updated: 2026-06-13

## Status

Three subagent searches have returned useful leads:

- Hilbert-90 / anti-invariant finite-field producers.
- Ray-class / CM / modular-unit inert-split coupling.
- Hasse-Davenport / Jacobi mixed-correction identities.

These hits are not certificates.  They are candidate producer families to feed
through the p25 finite harnesses.

## Best Leads

### 1. Robert / Coates-Wiles Elliptic Units

Source:

- Karl Rubin, *Elliptic Curves with Complex Multiplication and the Conjecture
  of Birch and Swinnerton-Dyer*, section 7, elliptic units:
  https://swc-math.github.io/aws/1999/99RubinCM.pdf

Why it matters:

- Evaluating an elliptic unit built from inert `151` torsion at split `677`
  torsion is intrinsically coupled.  It is not obviously a separated
  right-trace-times-C selector.
- The `x(Q)-x(P)` product has a plausible route to a row-quadratic/K-traced
  corner, because the `x` coordinate pairs `P` and `-P`.
- The split-prime conjugate quotient is a natural anti-invariant bridge
  candidate.

First finite probe:

```text
Build finite residue table for x(Q)-x(P), with P in the inert 151 source and
Q in the split 677 source.  K-trace over the invisible C25 layer.  Reject if
row variation disappears, if the result is a separated axis hull, or if
1-Frob_C kills the C169 bridge.
```

Local harness target:

- `p25_laneB_robert_source_matrix_harness_gate.py --source-matrix`
- `p25_laneB_robert_sparse_source_candidate_harness_gate.py --sparse-source`
- `p25_laneB_robert_x_difference_even_obstruction_gate.py`
- `p25_laneB_robert_oriented_phase_contract_gate.py`
- `p25_laneB_robert_c_phase_character_obstruction_gate.py`
- `p25_laneB_robert_bridge_edge_quotient_contract_gate.py`
- `p25_laneB_square_axis_bridge_candidate_harness_gate.py --raw-candidate`
- source-mixed character payload must be `336`, not `0`

Completed local precheck:

```text
Literal x-only tables are inversion-even under (right,c)->(-right,-c), while
the p25 bridge is anti-invariant under the same involution.  A cyclotomic
x-coordinate degeneration has only one zero, dense quadratic-character mask,
and fails the bridge harness.
```

Decision:

- Do not pursue a symmetric x-only Robert table.
- Continue only with an oriented quotient, y/differential data, unit phase, or
  another sign-breaking mechanism that can supply the active C-side odd phase.
- The phase alone is not enough: separated right-trace-times-C orientation
  overproduces support and has zero mixed right/C payload.  The producer still
  needs the coupled D-segment/K-trace support.
- The active phase is not a plain `C_169` character or sign tag: `C_169` has
  odd order, and no 169th-root character can satisfy `chi(-c)=-chi(c)`.
  Orientation must come from a divisor quotient, conjugate-unit quotient,
  `y`/differential data, or another non-character identity.
- The required quotient/divisor edge is now explicit: after the coupled
  `K`-trace and `D` segment, the negative bridge layer is the positive layer
  translated by `(2,113)` in `C_3 x C_169`.  Raw representatives are exactly
  `(2,113),(5,113),...,(74,113)`, i.e. the recorded edge `T=(38,113)` plus
  the kernel trace class.  Pure C-side and pure right-side edge controls fail
  the source-matrix harness.
- Targeted lit-search refinement: the best Robert/Siegel objects are
  translated odd quotients, not x-only tables.  Promising first forms are
  `Dtheta(P+T)/Dtheta(P-T)` from Kato-Siegel theta functions and
  `y(P+T)/y(P-T)` or `wp'`/Siegel quotients from ray-class generators.  These
  are naturally anti-invariant under `P -> -P` and can aim directly at the
  quotient edge `(2,113)`.  First finite gate: compute the divisor/residue
  table on `C_75 x C_169`, kernel-trace it, require nonzero odd projection,
  and reject rank-one `C_169` separation.
- Completed translated-quotient skeleton: `K_trace*(1-T)` alone is too small
  (`50` raw cells, `2` quotient cells), while
  `K_trace*D_segment*(1-T)` is exactly the bridge (`150` raw cells, `6`
  quotient cells).  The inverse edge has wrong orientation, even/squared edge
  symmetrizations expand to `225` raw cells, and omitting `K_trace` leaves all
  `25` kernel modes plus raw-relation failures.  The arithmetic producer must
  emit `D_segment + K_trace + translated odd edge` before any symmetrization.
- Completed quotient rigidity scan: on `C_3 x C_169`, the only visible
  factorizations are `base=(1,25), D=(1,3), T=(2,113)` and its reversal
  `base=(0,31), D=(2,166), T=(2,113)`.  A candidate cannot use a different AP
  segment or translated edge and hope to pass after the kernel trace.
- Completed raw-gauge scan: after the visible `D` segment and `T` edge are
  fixed, forward and reversed raw representatives each have `25^3` exact
  gauges by independently adding `K=(57,0)` to `base`, `D`, and `T`; simple
  non-kernel right/C shifts fail.  Candidate raw coordinates should be
  normalized only by this kernel gauge.
- Completed Kato/Robert subgroup-support falsifier: the literature quotient
  `rho_H(P+T)/rho_H(P-T)` has the right odd orientation, but literal finite
  subgroup support cannot supply the p25 `D_segment`.  Visible `D=(1,3)` has
  order `507`, raw `D=(22,3)` has order `12675`, and the raw positive layer has
  C-support `(25,28,31)` whereas any order-`75` subgroup has trivial
  C-projection.  Continue only with weighted `y`, `wp'`, Siegel/Klein,
  differential, or finite-difference quotient data.

Local harness target:

- `p25_laneB_robert_translated_odd_quotient_skeleton_gate.py`
- `p25_laneB_robert_translated_odd_quotient_rigidity_gate.py`
- `p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py`
- `p25_laneB_robert_sparse_source_candidate_harness_gate.py`
- `p25_laneB_robert_kato_subgroup_support_falsifier_gate.py`

Targeted sources:

- Lennart Sprang, *Algebraic de Rham realization of the elliptic polylogarithm*,
  Kato-Siegel theta divisor and differential formulas:
  https://arxiv.org/pdf/1802.04996
- Ja Kyung Koo, Dong Hwa Shin, and Dong Sung Yoon, ray class fields from
  torsion-point/Siegel quotients:
  https://mathsci.kaist.ac.kr/bk21/morgue/research_report_pdf/09-20.pdf
- Daniel S. Kubert and Serge Lang, Siegel/Klein unit generators:
  https://eudml.org/doc/162977
- Marco Streng, Klein/Siegel functions with odd root-level behavior:
  https://www.numdam.org/item/10.5802/ahl.160.pdf
- Reinhard Schertz, elliptic-unit ray-class quotient generators:
  https://www.numdam.org/item/JTNB_1997__9_2_383_0/

### 2. Siegel-Ramachandra / Kubert-Lang Modular Units

Sources:

- Daniel S. Kubert and Serge Lang, *Modular Units*:
  https://link.springer.com/book/10.1007/978-1-4757-1741-9
- Dong Hwa Shin, *Generation of class fields by Siegel-Ramachandra
  invariants*: https://arxiv.org/abs/1009.2253
- Ja Kyung Koo and Dong Sung Yoon, *Construction of ray class fields by
  smaller generators and applications*: https://arxiv.org/abs/1407.5713

Why it matters:

- Siegel functions already carry two torsion coordinates, so mixed vectors
  can couple the inert-right and split-C sources before reduction.
- Siegel-Ramachandra invariants use a lattice equation for the class, so the
  two local source axes need not separate as a product mask.
- Quotients of conjugate ray-class values are natural anti-invariant objects.

First finite probe:

```text
For a proposed exponent matrix M(r,c), subtract row/C marginals and project to
C anti-invariants.  Reject if the mixed projection is zero, if the raw lift is
not block-constant on C25, or if it fails the exact bridge candidate harness.
```

Local harness target:

- `p25_laneB_square_axis_bridge_candidate_harness_gate.py --raw-candidate`
- `p25_laneB_square_axis_bridge_theta31_source_shear_obstruction_gate.py`
  should not explain the object as a source-row shear of canonical theta

### 3. Odd-Degree Self-Dual Normal Bases

Source:

- E. Bayer-Fluckiger and H. W. Lenstra Jr., *Forms in Odd Degree Extensions
  and Self-Dual Normal Bases*:
  https://pub.math.leidenuniv.nl/~lenstrahw/PUBLICATIONS/1990e/art.pdf

Why it matters:

- The `C_169` part is odd degree.  A self-dual normal basis gives a trace
  quadratic with diagonal Gram form, which is exactly the kind of structure
  needed for a `K`-traced row-quadratic corner.
- Tensoring with a quadratic anti-line `alpha^(p^39) = -alpha` is a plausible
  way to keep signed bridge support while ordinary trace cancels.

First finite probe:

```text
Construct the C169 Frobenius action with p^39 acting as inversion.  Compute a
trace Gram matrix on bridge-pair basis vectors after multiplying by an
anti-line alpha.  Reject if the signed Gram is zero, dense, rank-defective, or
equivalent to the unsigned hull by a basis change.
```

Local harness target:

- existing twisted-orientation / quadratic-sign gates
- bridge candidate harness raw mode if the basis construction emits a vector

### 4. Gauss Period / Optimal Normal Basis Sine-Cosine Splitting

Sources:

- Shuhong Gao and H. W. Lenstra Jr., *Optimal Normal Bases*:
  https://cr.yp.to/bib/1992/gao.pdf
- General Gauss-period normal-basis direction from Feisel, von zur Gathen,
  and Shokrollahi, *Normal Bases via General Gauss Periods*.

Why it matters:

- If `p^39` acts as inversion on a period orbit, then sine-like elements
  `zeta^i - zeta^-i` are anti-invariant while cosine-like elements
  `zeta^i + zeta^-i` are fixed.
- Product identities of cosine and sine terms can be sparse.  That is much
  closer to the signed bridge than a dense Hilbert-90 quotient operator.

First finite probe:

```text
Search period data r,H with -1 not in H, p^39 H = -H, full normality, and
quotient/orbit length 169.  Reject if the sine part collapses into a smaller
field or period products lose the six-point bridge support.
```

Local harness target:

- `p25_laneB_square_axis_bridge_subfield_descent_gate.py`
- `p25_laneB_square_axis_bridge_candidate_harness_gate.py --raw-candidate`

### 5. K2 / Tame-Symbol Coupling

Sources:

- Romyar Sharifi and Akshay Venkatesh, *Eisenstein cocycles in motivic
  cohomology*: https://www.math.ucla.edu/~sharifi/eisensymbol.pdf
- A. J. Scholl, *An introduction to Kato's Euler systems*:
  https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf

Why it matters:

- Steinberg symbols of Siegel/cyclotomic units couple two unit inputs before
  taking residues.
- Finite tame symbols are naturally mixed: the valuation of one entry weights
  the residue of the other.  This is a plausible mechanism for a residue-coset
  bridge that is not a separated axis hull.

First finite probe:

```text
Compute tame-symbol residues on the finite components supporting the row
corner.  Reject if both entries are units on every relevant component, if the
anti-invariant part is a Manin/Steinberg boundary, or if the finite mask has
zero mixed right/C character payload.
```

Local harness target:

- source-mixed character gate
- bridge candidate harness raw mode

### 6. Order `l^2` Jacobi Congruences

Sources:

- D. Shirolkar and S. A. Katre, *Jacobi sums and cyclotomic numbers of order
  `l^2`*, Acta Arithmetica 147 (2011), 33-49:
  https://doi.org/10.4064/aa147-1-2
- Paul van Wamelen, *Jacobi sums over finite fields*, Acta Arithmetica 102
  (2002), 1-20: https://eudml.org/doc/278848

Why it matters:

- This is the best Jacobi-side match for "degree `13` descent but not a
  `C_13` pullback."  The order-`l^2` data can be constrained by order-`l`
  cyclotomic/Dickson-Hurwitz data while still carrying order-`l^2` ideal
  information.
- Van Wamelen's root-of-unity reconstruction is directly relevant to fake
  descent: divisor and autocorrelation data can agree while an order-`169`
  moment/root choice still blocks a sparse correction.

First finite probes:

```text
Compare the induced order-169 data at n and n+13.  Reject if the quotient is
already a C13 pullback or only a root scalar on the anomaly coset.

Solve the order-169 moment/autocorrelation screen for the proposed sparse
correction.  Reject if the required correction violates the odd-e moment
condition sum k*a_k = 0 mod 169.
```

Local harness target:

- `p25_laneB_square_axis_imprimitive_lift_obstruction_gate.py`
- `p25_laneB_square_axis_bridge_candidate_harness_gate.py --raw-candidate`

### 7. Gross-Koblitz / Stickelberger Carry Probe

Sources:

- Benedict Gross and Neal Koblitz, *Gauss sums and the `p`-adic gamma
  function*: https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/gross_koblitz.pdf
- Keith Conrad, *Jacobi Sums and Stickelberger's Theorem*:
  https://kconrad.math.uconn.edu/articles/jacobistick.pdf

Why it matters:

- Gross-Koblitz valuations read Jacobi/Gauss sums through digit-sum carries.
  This matches the current p25 no-borrow/Lucas seed almost too well: the
  target support is no-borrow, but the all-one payload still has the
  `S*X^3Y` anomaly.

Completed local probe:

```text
The strict one-digit carry model has now been instantiated.  For digits
a=t, b=h-t mod 3, every product-preserving twist
(a,b)->(a+tau,b-tau) has carry zero at the anomaly cell (h,t)=(2,1).
Affine twists in (h,t) and (s,h,t) also have zero anomaly-positive hits.

The full cyclic Stickelberger/Gross-Koblitz signature is different.  For
N=507 and N=12675, with A=t*N/3 and B=(h-t mod 3)*N/3, the p-orbit carry
signature is positive exactly on (0,1),(0,2),(1,2),(2,1): the non-selected
cells plus the selected q-binomial anomaly.  It is zero on all selected
non-anomaly cells.

The quadratic Frobenius-frequency projector selected*(DC-ALT)/ord_N(p)
extracts exactly (2,1).  Subtracting it from the honest Lucas/binomial
payload [1,1,1,1,2,1] gives the all-one selected seed and the known 18-term
residual.

Equivalently, the projector is selected support times the odd Frobenius
p^2-half-orbit average.  Sharper still, let O and E be the odd and even
half-orbit averages.  The odd half-orbit average leaks onto the non-selected
top-row cells (0,1) and (0,2), and the even half-orbit marks exactly those
leaks while missing the anomaly.  Thus O*(1-E) extracts exactly (2,1).

The anomaly is not in the additive span of `1`, selected support, O, and E.
Adding a product term closes the span because
`anomaly = O*(1-E) = selected*O = O - O*E`.  So additive half-orbit averages
are a kill condition; the literature hit has to provide a product, reflection
sign, Barnes delta, or equivalent resonance.

The naive HD/GK reflection precheck on the Jacobi gamma divisor leaves a
signed two-cell residue:

```text
(1,2):  +234 * U(169)
(2,1):  -234 * U(169)
```

So reflection alone is also a kill condition.  The multiplication/unit step
has to remove `(1,2)` and account for the free `U(169)` symbol.

The semiprimitive cubic rewrite now removes the free symbol but not the false
positive.  Since `p == -1 mod 3`, `p^39 == -1 mod 507`, and `f=78=2*39`,
Gross-Koblitz/Davenport-Hasse purity gives `U(169)->1` and `U(338)->1`.
After this rewrite the residue is still:

```text
(1,2):  +234
(2,1):  -234
```

So semiprimitive purity alone is also a kill condition.  A further HD
triplication, endpoint, or quotient relation must remove `(1,2)`.

Adding the deterministic C13 fiber background to this corrected residual gives
the exact square-axis theta_3_1 quotient packet.  Its kernel-trivial raw lift
has length 12675, 6300 nonzero positions, and passes the existing ray-local
raw-Y harness.
```

Local harness target:

- `p25_laneB_square_axis_no_borrow_digit_gate.py`
- `p25_laneB_square_axis_q_binomial_twist_falsifier_gate.py`
- `p25_laneB_square_axis_gross_koblitz_carry_twist_gate.py`
- `p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate.py`
- `p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate.py`
- `p25_laneB_square_axis_gross_koblitz_half_orbit_gate.py`
- `p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py`
- `p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate.py`
- `p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py`
- `p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py`
- `p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py`

Decision:

- Kill the strict carry-only explanation.
- Keep the multi-digit Jacobi route alive as a formal quotient-level payload
  and raw-Y repair.  It still needs a Hasse-Davenport, Gross-Koblitz unit
  quotient, Barnes-delta, or equivalent phase mechanism that realizes the
  even/odd half-orbit interaction `O*(1-E)` arithmetically.
- Targeted lit-search refinement: build the formal normalized `Gamma_p`
  divisor on `Z/507`,
  `D = sum_{k=0}^{38} U(p^{2k+1}v) - sum_{k=0}^{38} U(p^{2k}v)`, reduce it
  using reflection plus Hasse-Davenport multiplication for `m=2,3,13`, and
  pass only if the residual is pure sign/Teichmuller data that is nontrivial
  only at `(2,1)`.  Reflection-only reduction currently leaves opposite
  `U(169)` residues on `(1,2)` and `(2,1)`.  Semiprimitive cubic purity removes
  the free symbol, but the next HD/GK step must still remove the `(1,2)` false
  positive scalar.

Targeted sources:

- Gross and Koblitz, Gross-Koblitz formula:
  https://annals.math.princeton.edu/1979/109-3/p06
- Robert, digit-cycle / Stickelberger formulation:
  https://www.numdam.org/article/RSMUP_2001__105__157_0.pdf
- McCarthy, Hasse-Davenport and `p`-adic gamma identities:
  https://www.math.ttu.edu/~mccarthy/publications/SuperRV.pdf
- Long-Ramakrishna-style reflection identities:
  https://arxiv.org/pdf/1611.10188
- Conrad, lifted Jacobi sums and Hasse-Davenport:
  https://kconrad.math.uconn.edu/blurbs/gradnumthy/LfunctionGaussJacobi.pdf

### 8. Greene / Helversen-Pasotto Finite Barnes Delta

Source:

- John Greene, *Hypergeometric functions over finite fields*:
  https://www.d.umn.edu/~jgreene/papers/Hypergeometric_Trans.pdf

Why it matters:

- The finite Barnes lemma can collapse a dense character average to a product
  plus a resonant delta correction.  The delta term has the right general
  shape for "one sparse anomaly layer", but it is useful only if the resonance
  fires exactly on `X^3Y`.

First finite probe:

```text
Encode X^3Y as the sole resonance ABCD=epsilon.  Reject if the delta fires on
any Lucas/no-borrow support terms or if the product part is a dense scalar
balance.
```

Targeted lit-search refinement:

```text
Run a support-only exponent test before evaluating Gauss sums.  Encode the
candidate product-delta or point-delta predicate on C_3 x C_169, average under
the p^2 orbit with the proposed odd/even carry weights, then apply the
O*(1-E) screen.  Pass only if support is exactly (h,t)=(2,1) and the outer
S-image is exactly {138,310,482}.
```

If the Helversen-Pasotto product delta fires on any other orbit member, kill
HP-only and test Greene/FLRST endpoint or point-delta terms before killing the
wider hypergeometric route.

Completed local support screen:

```text
order-3 HP product delta       -> killed
full C507 seed-exponent delta  -> support-live
p^2 orbit-closed delta         -> killed
```

The order-3 product deltas through `(2,1)` are all three-cell lines, so they
fire on two extra cells.  The full seed-exponent point delta `q=138`, where
`q=43*(h+1)+9*t`, fires exactly at `(2,1)` and has outer `S` image
`{138,310,482}`.  But closing that point under the full `p^2` orbit gives
`117` quotient classes after the `S` layer, so a viable identity must produce
the local `C_507` point/endpoint correction before orbit closure.

Completed McCarthy well-poised delta contract: the exceptional term
`delta(A_0^-1*A_{n-1}*A_n)` is a full-character linear condition.  Tuning
`a_0-a_{n-1}-a_n=138 mod 507` gives pre-closure support exactly `(138,)` and
outer `S` image `(138,310,482)`.

Completed McCarthy numeric delta check: over `F_2029`, with character group
order `2028=4*507`, `n=2`, `x=2`, `A_1` trivial, `A_0=omega^(4*138)`, and
`A_2(q_exp)=omega^(4*q_exp)`, Theorem 1.7 gives
`support_qexp(LHS-main_sum)=(138,)`, `exceptional_support=(138,)`, and
`theorem_mismatch_count=0`.  This is now a real finite-field point-delta
producer before orbit closure.

Completed McCarthy raw-Y bridge: the singleton maps under the outer `S` layer
to `(138,310,482)`, exactly the GK/Frobenius projected anomaly terms, and the
formal raw-Y closure has length `12675`, support `6300`, and passes the
ray-local harness.  The remaining issue is parameter normalization as an
actual p25 local unit phase, not support geometry.

Local harness target:

- `p25_laneB_square_axis_q_binomial_twist_falsifier_gate.py`
- `p25_laneB_square_axis_barnes_delta_support_gate.py`
- `p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py`
- `p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py`
- `p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py`
- bridge candidate harness raw mode

Targeted sources:

- Helversen-Pasotto / Sole, finite Barnes first lemma:
  https://www.cambridge.org/core/services/aop-cambridge-core/content/view/7C613ED7568AE9F24BC8F7DCFA58C8B9/S0008439500013035a.pdf/barnes_first_lemma_and_its_finite_analogue.pdf
- McCarthy, finite-field well-poised hypergeometric transformations:
  https://www.math.ttu.edu/~mccarthy/publications/Hyp%20Trans.pdf
- Greene, finite-field hypergeometric functions:
  https://www.d.umn.edu/~jgreene/papers/Hypergeometric_Trans.pdf
- Fuselier, Long, Ramakrishna, Swisher, and Tu:
  https://arxiv.org/pdf/1510.02575
- Li and Soto-Andrade, finite Barnes identities and `GL(2)`:
  https://eudml.org/doc/152567

## Priority

1. McCarthy well-poised point-delta mapping: sharpest current Jacobi-side
   positive artifact, now numerically producing the `q_exp=138` singleton
   before orbit closure and landing on the existing raw-Y payload closure.
   Next normalize the McCarthy parameters as an actual p25 local unit phase.
2. Gross-Koblitz / Hasse-Davenport half-orbit interaction: still live, but
   semiprimitive unit cleanup alone leaves the `(1,2)` false-positive scalar.
3. Robert elliptic units: best shot at a genuinely coupled finite object.
4. Siegel-Ramachandra / mixed Siegel units: best shot at a raw modular-unit
   harness.
5. Greene / Barnes-delta resonance beyond McCarthy: keep only if it maps to the
   same point-delta or supplies the raw payload without dense scalar repair.
6. Anti-invariant trace-zero linear algebra: best diagnostic for whether the
   bridge can be produced by a signed local system before full CM arithmetic.
7. K2/tame-symbol route: keep as a sharper residue mechanism if direct unit
   values stay too dense.

## Current Next Probe

Run the half-orbit interaction literature-to-finite microscope first:

```text
find a Hasse-Davenport, Gross-Koblitz, Barnes-delta, or finite-field
hypergeometric identity whose finite reduction realizes the even/odd
half-orbit interaction O*(1-E), then emit either a raw Y[e] vector or a
dedicated unit-phase gate that proves the same interaction before raw-Y.
```

In parallel or immediately after, keep the Robert elliptic-unit microscope on
the now-explicit source-matrix contract: recover coupled D-segment/K-trace
support plus a non-character oriented divisor/unit quotient phase.  The
self-contained anti-invariant trace-zero diagnostic remains a theorem
microscope, not yet an arithmetic producer.
