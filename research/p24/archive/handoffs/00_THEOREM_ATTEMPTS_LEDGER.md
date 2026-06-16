# p24 Theorem Attempts Ledger

Date: 2026-06-06

Purpose: prevent backtracking.  This is a theorem-level ledger, not a list of
every toy script.  A route marked discarded should not be retried unless a new
mathematical ingredient changes the stated failure mode.

Current theorem-route tally:

```text
live routes:                4
discarded/demoted routes:  21
total routes logged:       25
```

The script-level harness is broader; this file counts theorem candidates and
proof routes.

## Admissibility Caveat

The route count above is a research-theorem count, not a strict challenge-law
count.  The current `AndrewVSutherland/DANGER3` README and local
`p24/upstream_DANGER3/README.md` do not visibly state a no-CM restriction, but
this fork's top-level `README.md` does say the challenge is to find triples
"without exploiting supersingular curves or CM."  If that wording is binding,
the CM/Lang/Jacobi routes in this ledger are conditional diagnostics unless
they are recast as non-CM finite-field identities.  Do not let a future pass
silently count a CM selector as a final admissible p24 solution.

Latest strict/no-CM refresh: rerunning the exact trace-residue, mixed CRT, and
small additive-spectrum audits did not reopen a strict-admissible route.  Odd
trace residues can isolate the six target traces as an oracle, but the
generous modular-level proxy remains constant times `sqrt(p)`; small exact
data again shows no stable low-complexity `A`/`j` bucket.  This does not
change the theorem-route tally; it reinforces the existing discarded
trace-residue/filter family.

## External Sanity Check

`p24/00_DREW_SUTHERLAND_ASK_MEMO.md` packages the current expert-facing
question.  It is not a new theorem route; it asks whether the live
phase/section producer theorem is known, obstructed, or missing a standard
CM/class-field ingredient.  The memo should be used before asking an expert so
that the conversation stays focused on the selected unramified `157/211`
Hilbert-class phase and the auxiliary `R_179` / kernel-polynomial object,
rather than on the already-gated finite verifier.  As of 2026-06-08 it also
separates the Kubert-Lichtenbaum/Anderson literature signal from the still
missing p24 unramified Artin pullback, and includes the `W_axis`/
`L1` axis-injectivity scalar route as a focused p-unit/nonvanishing ask.

## Still Live

### Two-Resultant Certificate Surface

Status: live.

Claim shape:

```text
Xi_O0 in O_p^*
Xi_O1 in O_p^*
unit/diamond transport carries Xi_O1 around the other nonzero orbits
```

Verifier payload:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}
```

Why still live:

```text
selected_two_punit_groups=4/4
punit_transport_edges=8/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

Pointers:

```text
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/trace_gcd_two_resultant_holdout_audit.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
```

### Fixed-Orbit RS-Tail Determinant

Status: live.

Claim shape:

```text
det(Psi_RS) in O_p^*
Psi_RS : F_p^28 + K^28 + F_p^16 -> L
```

Current best theorem surface:

```text
full 210-column selected/omitted chart C;
transported cyclic-shift blocks A,B;
low-rank displacement or exact graph/Riccati identity from two tail cut edges.
non-circular frequency-defect selected-basis gate before forming C, now in a
basis-free local projection-rank/rank-jump form.
H-coset fixed-frequency theorem `C P_H=0`, now with a live p24-specific
`p^780` factor-cycle candidate: semilinear covariance gives a nontrivial
Frobenius eigenspace, and descent to the `p^780`-fixed left field forces the
six nontrivial order-7 characters to vanish.  The descent must be complete
recombination over all 70 E-tensor idempotents; a representative factor or
single 7-cycle is insufficient.  The covariance must also be
Gauss-normalized; unnormalized additive-resolvent covariance is only the
Gauss-sum eigenvalue and does not force the divided `L`-projection to vanish.
Equivalent base-field form: for each right H-coset
`Q`, the uncentered marginal leakage
`D_Q(a)=sum_{b in Q}M(a,b)-|Q|M(a,0)` descends to the left-constant
component.  The pinned `D=-13319` marginal fails this in `6/6` slots, so
left descent is not generic.
Finally, the nontrivial covariance must be proved before descent/recombination:
after descent, idempotent components have trivial eigenvalue, so nontrivial
covariance is equivalent to the desired vanishing.  The final verifier
handoff is now exact: ordinary centering plus the six nontrivial `L`-valued
order-7 character sums is equivalent to the seven H-coset equations per left
coordinate, i.e. `936 + 156 = 1092` scalar coordinates.  The same
factor-cycle theorem now has an explicit twisted Hilbert-90 potential form:
on each of the ten length-7 quotient cycles, first produce the E-valued seed
by the nested internal trace
`Tr_{B/E}=Tr_{C/E} o Tr_{B/C}` of degrees `179` and `31`, then prove this
Gauss-normalized seed lies in `im(sigma-epsilon)=ker(Tr_epsilon)` by
constructing the CM/Lang potential.  On the raw relative factor cycle the
`p^780` action has order `38843 = 7*5549`, so applying the length-7 trace
before internal descent is invalid.  Stronger sufficient target: construct a
raw full-order CM/Lang coboundary `x=sigma(Y)-epsilon*Y`; the nested internal
trace commutes with this coboundary and supplies the quotient potential.
Finding `Y` only by Hilbert-90 inversion after trace zero is circular.  The
newer product-coboundary route reduces this raw coboundary target to two
arithmetic inputs on each packet term: left covariance
`sigma(T_{1,0,a})=alpha_a*T_{1,0,a}` and a matching right-resolvent
coboundary
`R_{chi,-a}=sigma(V_{chi,a})-(epsilon_chi/alpha_a)*V_{chi,a}`.  The
Leibniz/product rule is finite algebra, now checked both by toy gate and Lean;
the remaining theorem is construction of the matching right potential from
CM/Lang data.  The p24 twist is now pinned: in the raw convention
`chi_k(2)=zeta_7^k`, `p^780` fixes the left 157-frequency and has right
quotient shift `6`, so `alpha_a=1` and the needed product-coboundary twist is
`epsilon_k=zeta_7^k`.  A new boundary shows formal right-character covariance
has exactly this same eigenvalue, so it is the obstruction eigenspace of
`sigma-epsilon_k`; the right potential needs extra CM/Lang internal-trace
cancellation, not just covariance.  The positive finite replacement is:
matching right coboundary is equivalent to nested internal-trace zero, so the
next arithmetic theorem is `Tr_{B/E}(R_obstruction)=0` with
`Tr_{B/E}=Tr_{C/E} o Tr_{B/C}`, proved before Hilbert-90 inversion.  The
stage target is the final codimension-one trace
`Tr_{C/E}(Tr_{B/C}(R_obstruction))=0`; proving `Tr_{B/C}=0` is sufficient but
unnecessarily strong.  Equivalently, after expanding the obstruction as a
relative polynomial, prove the weighted Gaussian-period cancellation
`sum_k c_k eta_{ak}=0` with
`eta_t=sum_{r in <p^5460>} zeta_n^(tr)`.  The period-coset balance gate
inverts this functional: for the strong per-factor trace theorem, every
nonzero `<p^5460>`-coset in `F_n^*` must have weighted coefficient sum
`5549*c_0(chi)`, giving a precise 560-coset CM-sequence balance target.
After complete recombination over the `70` E-idempotents, this weakens to
the cleaner 8-coset target
`sum_{k in D} c_k(chi)=388430*c_0(chi)` for each nonzero `<p>`-coset.  This
is a `6*8=48` scalar compressed verifier across the six nontrivial right
quotient characters, split as `42` nontrivial octic quotient equations plus
`6` anchor equations, once the relevant coset sums and anchors are produced.
The recombined mixed-spectrum gate makes this split explicit: the `42`
nontrivial octic equations are the mixed sums
`sum_{k != 0} lambda(k) sum_r chi^{-1}(r mod 211) j_{r+m*k}=0`, while the
six trivial-octic equations are exactly the trace-defect anchors.  Thus the
live theorem is specific `C_7 x C_8` CM/Lang mixed-spectrum vanishing plus a
section-aware anchor, not an unnamed period-cancellation slogan.
The Lean recombined mixed-spectrum gate packages the same handoff as a formal
contract: given the finite quotient Fourier split, mixed-spectrum zero plus
anchor zero is equivalent to the eight recombined balance equations per right
character, with p24 counts `42+6=48` and `54` compressed values when `c_0` is
carried.
The affine quotient-profile gate gives the current preferred finite theorem
surface for the same target.  If `M_i(D)` is the right `H=<2^7>` coset profile
of a nonzero relative `<p>`-coset `D`, and `b_i` is the selected-child right
profile, the `48` equations are equivalent to offsets `gamma_D`, independent
of `i`, satisfying
`M_i(D)=388430*b_i+gamma_D`.  Mixed zero alone only says there is no
right/relative interaction; the anchors are exactly what ties the surviving
right profile to the selected child.  Thus the next arithmetic proof should
construct those column offsets, or an equivalent potential, from the specific
trace-GCD weighted CM/Lang packet.
The right-difference gate removes the offsets from the statement: the same
target is equivalent to
`M_{i+1}(D)-M_i(D)=388430*(b_{i+1}-b_i)` for each relative `<p>`-coset `D`.
The cyclic formulation has `56` redundant equations but `48` independent
ones, and the offsets are recovered afterward by right averaging.  This is
the preferred next proof target because it asks for equality of right
derivatives, which is the natural shape for an explicit CM/Lang potential.
The right-difference trace gate names the corresponding arithmetic object:
for `A_i(k)=sum_{r in H_i}j_{r+m*k}`, the adjacent difference polynomial
`P_i(X)=sum_k(A_{i+1}(k)-A_i(k))X^k` must satisfy
`Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n))=0`.  These seven degree-8 traces
have one cyclic dependency, hence again `48` independent equations.  This is
the current cleanest proof target.
The right-difference covariance-telescope gate then reduces those seven trace
zeros to two arithmetic inputs.  For
`T_i=Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_i(zeta_n))`, telescoping gives
`sum_i T_i=0`; if `T_{i+6}=rho(T_i)` and one anchor descends
`rho(T_0)=T_0`, then all seven `T_i` are equal and hence zero.  Negative
controls show covariance plus telescoping alone and descent plus telescoping
alone both leak.  The current proof target is therefore covariance of the
adjacent trace packet plus one descended adjacent-trace anchor.
The trace-covariance functorial gate reduces the covariance input to
pointwise CM/Lang Frobenius functoriality:
`P_{i+6}(zeta_n^(rho*a))=rho(P_i(zeta_n^a))`.  Since `rho mod n` is inside
the trace subgroup `<p>`, the decomposition-trace cosets are fixed and this
implies `T_{i+6}=rho(T_i)`.  If the multiplier were outside the trace
subgroup, the same pointwise covariance would only give permuted coset
covariance.  The only non-formal descent input left on this branch is
`rho(T_0)=T_0`.
The adjacent-anchor descent gate rewrites that last input as an order-7
projector theorem on the single trace value
`T_0=Tr_{Q(zeta_n)/Q(zeta_n)^<p>}(P_0(zeta_n))`.  Descent is equivalent to
the six nontrivial equations `Pi_k(T_0)=0`, `k=1,...,6`.  Finite controls
show both covariance+telescope without anchor and covariance+anchor without
telescope can leak, so this is a real arithmetic input, not a relabelled
counting check.
The adjacent-difference operator gate proves this is not a new independent
anchor surface: under p24 covariance, `T_0=(rho^6-1)Y_0`, and the difference
operator is invertible on all six nontrivial order-7 projector channels.
Thus adjacent-anchor descent is equivalent to right-axis equal-H-coset
descent.  The proof frontier is the same selected weighted profile theorem,
now with the finite-difference ambiguity removed.
The actual-CM adjacent-anchor boundary tests the same shape on
`D=-6719`, `q=6863`, `h=105`, `m=21=3*7`, `n=5`.  Adjacent H-coset trace
differences satisfy covariance and telescope, but the anchor descends in
`0/2` relative trace cosets.  This rules out the generic theorem
"actual CM covariance plus telescope implies adjacent anchor descent"; the
p24 proof must use the special trace-GCD weighted/selected packet.
The mixed-spectrum resolvent bridge expands these equations by two finite
Gauss transforms as weighted combinations of additive class resolvents
`R(v,a)`.  It proves the target is not a single class-character resolvent:
reduced normality of all additive resolvents neither proves nor refutes mixed
vanishing.  The remaining theorem therefore needs a genuine
Stickelberger/Jacobi-sum/CM-Lang relation among the resolvents.
The actual-CM mixed-spectrum boundary supplies a small real CM row with both
quotient axes nontrivial (`D=-4751`, `h=91=7*13`, right quotient `3`, relative
quotient `4`).  All `91` origin shifts fail the full mixed spectrum, anchor,
and recombined-balance targets.  Thus the desired identity is not generic
embedded-CM quotient structure; it must use the specific trace-GCD weighted
packet or an explicit potential.
The anchor equations are now rewritten as the six nontrivial right
quotient-character projections of the relative trace defect
`D_r=Tr_relative(j_{r+m*bullet})-n*j_r`; equivalently, that defect has equal
`H=<2^7>` coset sums on the right axis.  This is the preferred anchor theorem
surface.  Seven honest defect H-coset sums are enough for the verifier, and
the fuller quotient trace-average plus selected-child profile costs
`2*m=132508` field elements for p24, but both require producer honesty from an
embedded CM/Lang construction.
The
sharper internal-character
form is: for `Y_C=Tr_{B/C}(R_obstruction)`, the trivial `C/E` character
projection of `Y_C` is zero.  The order-7 quotient twist does not imply this,
because the twist disappears after the seven raw steps that define the
internal generator.  This is independent from augmentation/content
nonvanishing.  It is also not a generic raw-CM-period fact: the
`D=-5000`, `h=30=2*5*3` actual-CM boundary has `0/60` rotated/top raw period
packets with zero trivial `C` projection.  The proof must use the specific
right-obstruction/product-coboundary expression.  The right Gauss weighted
polynomial gate names that expression:
`R_{chi,-a}=tau(chi)*G_chi(zeta_n^{-a})`, with
`G_chi(X)=sum_r chi^{-1}(r mod 211)F_r(X)` and
`F_r(X)=sum_k j_{r+m*k}X^k`; fibers with `r=0 mod 211` vanish by character
orthogonality.  The live theorem is now internal trace zero for this specific
weighted CM polynomial, not for arbitrary weighted polynomials.  Since
`p^5460` fixes the right `211` axis, the internal trace does not average the
right H-cosets; equivalently, the internally traced `G_chi` right profile must
have zero order-7 multiplicative spectrum, i.e. equal H-coset sums.  The
seven-coset covariance/descent gate shows the exact sufficient theorem:
`p^780` covariance shifts the quotient by `6`, and descent of one anchor sum
to the `p^780`-fixed field then forces equality.  Under covariance, this
anchor descent is equivalent to zero order-7 spectrum; each input alone still
leaks.  The fixed-field refinement shows the exact fixed field has degree
`780=156*5`, so descent to `F_p(mu_157)` is sufficient but stronger than
needed.  Pure right H-periods remain nonfixed and leak.  The pinned actual-CM
right-axis covariance boundary shows the same problem in real CM data:
`D=-6719, q=6863, h=105, m=21=3*7, n=5` has formal additive covariance and
all four Gauss-normalized quotient projections are `rho`-fixed, but all four
are nonzero and `0/2` anchor cosets descend.  The left-paired repair also
fails on the same row: inserting either nontrivial left character still gives
`0/4` equal H-coset sums and `8/8` nonzero Gauss-normalized projections.
Thus the paired-potential theorem cannot be just ordinary left-character
pairing with right-axis covariance; it must use the trace-GCD weighted
product/section structure.  The paired-kernel gate now states that surviving
target exactly as six equations `A(Pi_k L_0)=0`: the H-trace leakage need not
vanish before pairing, but its six nonfixed projectors must lie in the
selected trace-GCD left kernel.  A separate DANGER-data boundary tests the hoped-for source from the strict 2-adic order condition: ten
materialized small Pomerance trace classes from `pp10` give `19` coprime
decompositions and `385` global child sections with zero anchor passes.
Thus neither Gauss-normalized covariance nor the DANGER trace congruence is
the missing anchor theorem.  The pinned actual-CM
right-combo boundary has `0/2` zero internal traces, and the weighted product
internal-trace boundary also has `0/2` zero product traces and `0/1` zero
recombined `<q>` traces, so this is not a generic consequence of right-combo
or product packet shape.  The right-combo anchor boundary isolates the anchor
equation in the pinned `n=5` row, where complete recombination has one
nonzero coset and no nontrivial quotient equations; the actual right-combo
`G_chi` analogue fails `sum_{k=1}^4 c_k=4*c_0`.  Thus the anchor equation is
not generic decomposition-field trace language.  The section scan checks all
`140` global origins in this row and finds `0/140` anchor passes, with `140`
distinct nonzero defects, so a better embedded section is not the missing
generic ingredient.  The
anchor-projector gate
now states the exact descent equations:
`Pi_k(Y_0)=(1/7) sum_{j=0}^6 omega^(-k*j) rho^j(Y_0)=0` for `k=1,...,6`.
The pure H-period anchor has all six nonfixed projectors nonzero, so these
six vanishings must come from the traced weighted CM polynomial itself.  The
projector-character bridge checks that, under the p24 shift `6`, these are
the same six nontrivial H-quotient character equations used in the `1092`
scalar payload.  The projector/internal-character target gate combines this
with the internal trace formulation: the missing theorem is now
`Tr_{C/E}(Tr_{B/C}(Pi_m(packet)))=0` for all six nontrivial projector
channels.  The right/C bidegree support gate sharpens this again: after the
`B/C` trace, the forbidden Fourier slots are precisely
`(right nontrivial, C/E trivial)`.  Because `gcd(7,179)=1`, avoiding those
slots is not a group-homomorphism artifact; it must be proved from the
selected weighted CM/Lang packet.  Random projected packets show this is not
formal.  The Stickelberger bidegree boundary checks the first
Jacobi-sum/Stickelberger shortcut against this same support condition: plain
cyclic Stickelberger on `C_(7*179)` and plain right-axis Stickelberger both
have `6/6` nonzero forbidden coefficients, even after centering.  Only a
deliberately `C/E`-centered product avoids the forbidden slots, so a
successful Jacobi/Stickelberger proof must construct that centering from the
selected weighted packet itself; the generic slogan is not the missing anchor
theorem.
The Jacobi-carry C-centering gate supplies a narrow positive replacement:
for `theta_{u,v}(t)=[ut]+[vt]-[(u+v)t]` on `C_7 x C_179`, a carry with one
right-trivial nontrivial `C/E` input kills all six forbidden bidegrees, while
generic Jacobi carries, pure-right partners, and C-cancelled sums still leak.
Thus the viable Jacobi theorem is now explicit: decompose the weighted
trace-GCD obstruction after `Tr_{B/C}` into C-axis Jacobi carry divisors.
The admissible Jacobi-carry span boundary corrects this to the termwise-safe
subfamily: the partner and `u+v` must keep nontrivial `C/E` component.  This
admissible span has p24 rank `621`; the broader C-axis family has rank `625`
but includes four leaky directions.  Therefore the preferred theorem is
membership in the rank-`621` admissible span, while a rank-`625` theorem needs
a separate four-direction leak-cancellation proof.
The admissible Jacobi spectral boundary gives that rank a better proof shape:
small exact models have `C/E`-trivial slice rank `1`, nontrivial `C/E` slice
rank `7`, conjugate `C/E`-pair rank `8` rather than `14`, and cumulative
increments `1,7,...,7,4`.  For p24 this is `1+7*88+4=621`.  So the live
Jacobi theorem should prove conjugate-`C/E` pair compatibility for the
selected weighted packet, not merely forbidden-support vanishing.
The admissible Jacobi dual-conditions gate makes that compatibility explicit:
in small exact models the rank-`621` span is exactly cut out by four Fourier
condition families on `C_7 x C_179`: six forbidden right-nontrivial
`C/E`-trivial coefficients vanish; `6*89` nontrivial-right conjugate-pair
skew equations hold; `89` right-trivial pair sums are tied to the global
constant; and three global pair-balance equations hold.  For p24 this is
`6+6*89+89+3=632` independent equations in ambient dimension `1253`, giving
solution dimension `621`.  This is now the most concrete theorem target for
the selected weighted packet after `Tr_{B/C}`.
The literal Jacobi-sum product probes then split this target further.  Honest
right-mixed admissible Jacobi sums supply the off-`C=0` pair-products and
already have constant selected row-product ratio on the six nonzero right
rows.  The only failure is the degenerate right-zero anchor, with exact defect
`delta_c=(q-2)^(-(c-1))`.  The newest anchor-correction gate proves in small
finite-field models that changing only `U(0,0)=J(1,1)=q-2` to
`U(0,0)/(q-2)=1` repairs both C-zero pair-products and selected row-product
ratios, exhaustively for the c=5,11,13 right-mixed admissible pairs:
`corrected_product_formula_rows=3/3` and
`anchor_scale_formula_rows=3/3`.  Thus the viable Jacobi theorem is now a
punctured Hasse-Davenport formula plus the selected trace-GCD/CM-Lang analogue
of one degenerate-anchor unit, not three unrelated global balances.
The symbolic Hasse-Davenport gate then removes finite-field summation from
this Jacobi algebra: for c=5,11,13,17,19 and p24 c=179, all admissible
right-mixed pairs satisfy the residue conditions making the `B_k` and
`A_kB_k` Gauss factors cancel in the selected row ratio.  It covers all
`189036` p24 pairs with `symbolic_producer_rows=6/6`.  The open theorem is
therefore the CM/Lang realization of the reduced packet, not the finite
Hasse-Davenport accounting.
The reduced-anchor fingerprint gate identifies the selected-defect footprint
of that realization: the raw single-anchor correction becomes the punctured
right-zero row, with `178` nonzero p24 entries and Fourier profile
`H(a,0)=178`, `H(a,b)=-1` for `b != 0`.  This vector deliberately leaks the
forbidden C-trivial bidegrees, so the theorem must produce it as the
degenerate correction paired with the raw punctured packet, not as an
independent admissible component.
The actual-CM admissible-span boundary rules out the generic version of that
theorem: the raw `D=-5000` projector row has `0/30` admissible-span origins,
and the pinned `D=-13319` row has `0/140` admissible-span origins for
right-combo resolvents, raw weighted coefficients, and selected-child defect
coefficients; all also have `0` broad-span origins.  Thus ordinary
embedded-CM/projector/right-combo/coefficient packet structure is not enough.
The live p24 branch must use the selected weighted trace-GCD packet or an
explicit CM/Lang decomposition.
The anchor-vs-C-centering boundary then closes the tempting repair that the
section-aware trace defect automatically supplies this centering.  In the
exact quotient model `C_7 x C_179 x C_31`, anchor zero can hold while the
forbidden `C/E`-trivial bidegree leaks (`32/32` controls), and
`C/E`-centering can hold while the selected-child anchor fails (`32/32`).
Thus selected-section subtraction can mask the forbidden bidegree; the proof
must control the selected child right profile, prove direct `C/E`-centering,
or prove the full affine profile identity.
Small actual-CM calibration is currently not available for this exact p24
geometry: the limited relation-shape index has no hits.
```

Pointers:

```text
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
p24/trace_gcd_rs_tail_block_skew_cauchy_theorem_candidate.md
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
p24/trace_gcd_rs_tail_frequency_defect_gate_theorem.md
p24/trace_gcd_rs_tail_basis_free_frequency_gate_toy.py
p24/trace_gcd_fixed_frequency_class_character_expansion.md
p24/trace_gcd_fixed_frequency_actual_cm_right_combo_boundary.md
p24/trace_gcd_fixed_frequency_p24_factor_cycle_cancellation_candidate.md
p24/trace_gcd_fixed_frequency_p24_semilinear_factor_cycle_gate.md
p24/trace_gcd_fixed_frequency_p24_complete_factor_descent_gate.md
p24/trace_gcd_fixed_frequency_p24_gauss_normalization_boundary.md
p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_circularity_boundary.md
p24/trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate.md
p24/trace_gcd_fixed_frequency_p24_normalized_covariance_obstruction_gate.py
p24/trace_gcd_fixed_frequency_relation_shape_index.py
p24/trace_gcd_fixed_frequency_p24_covariance_descent_theorem.md
p24/trace_gcd_fixed_frequency_p24_idempotent_covariance_theorem.md
p24/trace_gcd_fixed_frequency_p24_pre_recombination_covariance_gate.md
p24/lean/TraceGcdSemilinearEigenDescentGate.lean
p24/lean/TraceGcdPreRecombinationCovarianceGate.lean
p24/trace_gcd_fixed_frequency_p24_character_payload_contract.md
p24/trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate.md
p24/trace_gcd_fixed_frequency_p24_nested_internal_trace_gate.md
p24/trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate.md
p24/trace_gcd_fixed_frequency_p24_product_coboundary_leibniz_gate.md
p24/trace_gcd_fixed_frequency_p24_matching_twist_bookkeeping_gate.md
p24/trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate.md
p24/trace_gcd_fixed_frequency_p24_right_coboundary_internal_trace_gate.md
p24/trace_gcd_fixed_frequency_p24_internal_trace_stage_target_gate.md
p24/trace_gcd_fixed_frequency_p24_internal_trace_gaussian_functional_gate.md
p24/trace_gcd_fixed_frequency_p24_period_coset_balance_gate.md
p24/trace_gcd_fixed_frequency_p24_recombined_mixed_spectrum_gate.md
p24/trace_gcd_fixed_frequency_p24_affine_profile_gate.md
p24/trace_gcd_fixed_frequency_p24_right_difference_gate.md
p24/trace_gcd_fixed_frequency_p24_right_difference_trace_gate.md
p24/trace_gcd_fixed_frequency_p24_right_difference_covariance_telescope_gate.md
p24/trace_gcd_fixed_frequency_p24_right_difference_trace_covariance_functorial_gate.md
p24/trace_gcd_fixed_frequency_p24_mixed_spectrum_resolvent_bridge.md
p24/trace_gcd_fixed_frequency_actual_cm_mixed_spectrum_boundary.md
p24/lean/TraceGcdRecombinedMixedSpectrumGate.lean
p24/lean/TraceGcdAffineProfileGate.lean
p24/lean/TraceGcdRightDifferenceGate.lean
p24/lean/TraceGcdRightDifferenceTraceGate.lean
p24/lean/TraceGcdRightDifferenceCovarianceTelescopeGate.lean
p24/lean/TraceGcdRightDifferenceTraceCovarianceFunctorialGate.lean
p24/trace_gcd_fixed_frequency_p24_internal_character_filter_gate.md
p24/trace_gcd_fixed_frequency_actual_cm_internal_character_boundary.md
p24/trace_gcd_fixed_frequency_p24_right_gauss_weighted_polynomial_gate.md
p24/trace_gcd_fixed_frequency_p24_right_axis_spectrum_gate.md
p24/trace_gcd_fixed_frequency_p24_right_axis_covariance_descent_gate.md
p24/trace_gcd_fixed_frequency_p24_right_axis_fixed_field_refinement_gate.md
p24/trace_gcd_fixed_frequency_p24_right_axis_anchor_projector_gate.md
p24/trace_gcd_fixed_frequency_p24_right_axis_projector_character_bridge.md
p24/trace_gcd_fixed_frequency_p24_projector_internal_character_target_gate.md
p24/trace_gcd_fixed_frequency_p24_right_c_bidegree_support_gate.md
p24/trace_gcd_fixed_frequency_p24_stickelberger_bidegree_boundary.md
p24/trace_gcd_fixed_frequency_p24_jacobi_carry_c_centering_gate.md
p24/trace_gcd_fixed_frequency_p24_jacobi_carry_span_boundary.md
p24/trace_gcd_fixed_frequency_p24_jacobi_carry_fourier_formula_gate.md
p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_spectral_boundary.md
p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_dual_conditions_gate.md
p24/trace_gcd_fixed_frequency_p24_dual_condition_source_map.md
p24/trace_gcd_fixed_frequency_p24_dual_conditions_value_side_gate.md
p24/trace_gcd_fixed_frequency_p24_value_identity_strength_gate.md
p24/trace_gcd_fixed_frequency_p24_selected_defect_value_producer_gate.md
p24/trace_gcd_fixed_frequency_p24_multiplicative_producer_dictionary_gate.md
p24/trace_gcd_fixed_frequency_p24_admissible_jacobi_decomposition_theorem.md
p24/trace_gcd_fixed_frequency_actual_cm_admissible_jacobi_span_boundary.md
p24/trace_gcd_fixed_frequency_actual_cm_value_identity_boundary.md
p24/trace_gcd_fixed_frequency_p24_anchor_vs_c_centering_boundary.md
p24/trace_gcd_fixed_frequency_actual_cm_projector_internal_character_boundary.md
p24/lean/TraceGcdAdmissibleJacobiDecompositionGate.lean
p24/lean/TraceGcdAdmissibleJacobiDualConditionsGate.lean
p24/lean/TraceGcdDualConditionsValueSideGate.lean
p24/lean/TraceGcdRightAxisAnchorDescentGate.lean
p24/trace_gcd_fixed_frequency_actual_cm_right_combo_internal_trace_boundary.md
p24/trace_gcd_fixed_frequency_actual_cm_product_internal_trace_boundary.md
p24/trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate.md
p24/lean/TraceGcdProductCoboundaryGate.lean
p24/lean/TraceGcdProjectorTracePipelineGate.lean
p24/trace_gcd_fixed_frequency_p24_projector_trace_pipeline_gate.md
```

Update: the pre-recombination covariance gate is only a conditional handoff.
The normalized covariance obstruction shows the natural Gauss-normalized
component covariance has trivial eigenvalue under the factor shift; a
nontrivial normalized covariance would force componentwise zero.  The live
target is back to the specific weighted internal-trace/right-coboundary
identity, not normalized covariance.

### Nonzero-Orbit Crossed Norm

Status: live.

Claim shape:

```text
Xi_O1 = Nrd_O(Phi_t) in O_p^*
```

Why still live: actual-CM holdouts support the crossed-product/block-cycle
norm identity; ordinary base-polynomial equality is false, but the crossed
norm survives.

Pointers:

```text
p24/trace_gcd_crossed_coinvariant_norm_target.md
p24/trace_gcd_crossed_coinvariant_norm_toy.py
p24/trace_gcd_actual_cm_square_coinvariant_block_cycle_audit.py
```

### Low-Moment / L1 Axis Content Selector

Status: live.

Claim shape:

```text
Low-moment selector:
  30 selector constraints identify the selected child fibers;
  P_1 is automatic on each of the two selected layers;
  producer burden is 28 higher relative traces / child coefficients.

L1 axis-content scalar:
  W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}
  dim W_axis = 368;
  for each f_a | Phi_3107441, deg(f_a)=388430,
  T_a : W_axis -> F_p[X]/(f_a) is injective.
```

Why still live:

```text
low-moment default sweep:         19/19 unique within degree bound
low-moment wider sweep:           65/65 unique within degree bound
low-moment bounded larger sweep: 134/134 unique within degree bound
end-of-day low-moment controls:  218/218 and 103/103

moment-pair falsifier rerun:
  complement: 416 packets, no {M0,M1} pair failure
  contiguous: 648 packets, no {M0,M1} pair failure

L1 axis-injectivity rerun:
  wider eligible: 191/191 injective, no L1 zeros
  all-origin eligible: 630/630 injective, no L1 zeros

tensor-factor refinement:
  A_a tensor F_p(mu_m) splits into 70 factors B_i/E
  [B_i:E] = 5549 > dim W_axis = 368
  Lean descent: one factor injective => base packet injective
  tensor factor-rank scan: 130 rows, no full tensor axis failures,
    6/6 one-factor dimension-possible rows have a full axis factor
  tensor block scan: 130 rows, no unforced block/pair/full failures
```

Finite certificate scale:

```text
low-moment parent-field function surface:
  2*4 + 314*26 = 8172 coefficients = 8.172e-9 * sqrt(p)

L1 axis rank surface across all eight packets:
  8 * 368 * 388430 = 1143537920 < 10^12 = sqrt_floor(p)

sharper L1 tensor-factor theorem surface:
  one Moore determinant of size 368 in a degree-5549 E-factor,
  E = F_p(mu_m), [E:F_p] = 5460
```

Failure mode still open:

```text
Low moments still need an intrinsic relative-trace producer and a CM
sparse-relation anti-collision theorem.  L1 axis injectivity still needs a
selected-prime p-unit / hyperplane-avoidance theorem for the p24 embedded
packet, now sharpened to a one-factor Moore determinant nonvanishing theorem.
These are theorem microscopes and sub-sqrt certificate surfaces, not completed
p24 certificate producers.
```

Pointers:

```text
p24/trace_gcd_low_moment_cm_selector_sweep.md
p24/trace_gcd_low_moment_sparse_relation_gate.md
p24/trace_gcd_low_moment_relative_trace_gate.md
p24/trace_gcd_low_moment_truncated_polynomial_gate.md
p24/relative_augmentation_order_theorem.md
p24/l1_punit_boundary.md
p24/l1_axis_injectivity_theorem.md
p24/lean/TraceGcdLowMomentSparseRelationGate.lean
p24/lean/TraceGcdLowMomentRelativeTraceGate.lean
p24/lean/AxisInjectivityGate.lean
```

## Discarded Or Demoted

### Cyclic Squarefree Tower As Seedless Root Selector

Status: demoted.

Failure mode: the p24 third-trace class group is cyclic and squarefree, so the
`2,157,211,3107441` subgroup tower is unique, but that does not choose
compatible roots above the split ordinary prime.  At each nontrivial relative
layer, a parent root has a child torsor rather than a canonical child.  The
order-2 genus layer is the only piece supplied by quadratic/genus data; the
odd `157/211` refinements still need embedded non-genus phase data.

Replacement: use cyclicity as tower bookkeeping only.  Either construct
embedded relative child polynomials/non-genus class-character traces, or stay
with the trace-GCD p-unit route and prove the embedded determinant section.

Pointers:

```text
p24/cyclic_class_tower_selector_obstruction.md
p24/cyclic_class_tower_selector_obstruction.py
p24/lean/CyclicTowerSectionObstructionGate.lean
```

### Class-Set Enumeration Or Sqrt-Scale Search

Status: discarded.

Failure mode: violates the requested asymptotic goal.  It may produce data but
not the sub-sqrt certificate.

Do not retry as the main route.

### Seven Independent Nonzero-Orbit Certificates

Status: demoted.

Failure mode: too large and misses unit-transport structure.  The better
surface is one fixed p-unit plus one nonzero crossed norm plus transport.

Replacement: two-resultant certificate surface.

### Ordinary Base-Polynomial Descent For Nonzero Orbits

Status: discarded.

Failure mode: actual-CM holdouts give

```text
literal_equal_nonzero_edges=0/8
naive_base_polynomial_groups=0/4
```

The nonzero theorem is genuinely semilinear/crossed-product.

Pointer:

```text
p24/trace_gcd_two_resultant_proof_route_synthesis.md
```

### Simple Root / Different / Squarefree Split Shortcut

Status: discarded.

Failure mode: split squarefree class-polynomial roots and Hensel-simple
ordinary embeddings do not imply determinant-line p-unitness.  A determinant
zero control survives these hypotheses.

Pointer:

```text
p24/trace_gcd_useful_computation_strategy.md
```

### Visible Natural-Coordinate LRS/GRS Signature

Status: discarded.

Failure mode: natural RS-tail columns do not have the visible
rational-normal/Reed-Solomon signature.  Synthetic visible GRS passes; random
RS-tail-shaped coordinates reject the shortcut.

Replacement: hidden block/skew equivalence or full 210-column Plucker chart.

Pointers:

```text
p24/trace_gcd_rs_tail_visible_lrs_signature_toy.py
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
```

### Selected-Block Support Profile As A Proof

Status: demoted to compatibility check.

Failure mode: the selected block dimensions `35,35,35,35,16` can be direct
without exposing a hidden LRS/MSRD theorem.  Random direct controls pass too.

Keep only as a falsifier for bad ansatzes.

Pointer:

```text
p24/trace_gcd_rs_tail_block_support_profile_toy.py
```

### Scalar Visible Cauchy / Entrywise-Inverse Rank As The Full Theorem

Status: demoted.

Failure mode: scalar Cauchy is only the visible GRS shadow.  The useful
replacement is block/skew displacement with fixed arithmetic operators.

Replacement:

```text
A C - C B = low rank
```

or the exact shift graph/Riccati identity.

Pointers:

```text
p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
```

### Current Small Actual-CM Rows As Full-Chart Evidence

Status: demoted to boundary evidence.

Failure mode: tail-only rows make the chart condition automatic, and
prefix-plus-tail rows are singular before the selected columns form a basis.

Do not cite these rows as positive evidence for the full Plucker chart.

Pointer:

```text
p24/trace_gcd_actual_cm_full_plucker_chart_boundary.py
```

### Frobenius-Only H-Coset Proof

Status: discarded.

Failure mode: `p^156` fixes the left `157` frequency and acts nontrivially on
the right order-7 quotient, but the relevant orbit augmentation lies in
`L(mu_211)`, not in `L`.  The nontrivial Frobenius eigenvalue is carried by the
Gauss-sum factor `tau(chi)`, so the divided projection
`sum_s chi(s)^(-1)G_s` can be nonzero while semilinear covariance holds.

Replacement: prove the actual mixed-resolvent orthogonality
`<A_1, sum_v chi(v)B_v>=0` for the six right order-7 multiplicative
resolvents.

Equivalent current form: prove the right-kernel inclusion `C P_H=0`, where
`P_H` is the `210 x 7` H-coset indicator matrix.  A stronger fixed-left
multiplier invariance under `p^156 mod 211` would imply this inclusion because
it cycles the seven H-cosets, but it is only a sufficient fantasy symmetry;
full rank and ordinary centering still leave a six-dimensional H-leak in the
finite control.

Pointer:

```text
p24/trace_gcd_fixed_frequency_multiplicative_resolvent_bridge.md
p24/trace_gcd_fixed_frequency_p24_character_payload_contract.md
p24/trace_gcd_fixed_frequency_p24_internal_trace_then_hilbert90_gate.md
p24/trace_gcd_fixed_frequency_p24_nested_internal_trace_gate.md
p24/trace_gcd_fixed_frequency_p24_raw_coboundary_transfer_gate.md
p24/trace_gcd_fixed_frequency_p24_twisted_hilbert90_payload_gate.md
p24/trace_gcd_fixed_frequency_h_kernel_inclusion_gate.md
```

### Post-Fit Displacement Operators

Status: discarded.

Failure mode: low-rank displacement can be manufactured by fitting operators
after seeing the chart.  Operators must be fixed by the CM/Lang construction.

Pointer:

```text
p24/trace_gcd_plucker_displacement_handoff_toy.py
```

### Probability / Strong-Rayleigh / Real-Stability Shortcut

Status: discarded.

Failure mode: the CRT-axis support matroid violates the needed
Strong-Rayleigh behavior.  Hodge/Lorentzian intuition may still orient
questions, but it does not prove p-unit noncancellation.

Pointers:

```text
p24/axis_crt_strong_rayleigh_obstruction_toy.py
p24/axis_crt_strong_rayleigh_obstruction_boundary.md
```

### Matrix-Tree / CRT Hypertree Factorization Shortcut

Status: demoted.

Failure mode: support can look tree-like, but coefficients remain mixed
Plucker/exterior weights and do not collapse to a standard matrix-tree
p-unit theorem.

Pointer:

```text
p24/axis_crt_matrix_tree_factorization_boundary.md
```

### DANGER3 Montgomery Data As Direct CM Fibers

Status: discarded as a producer.

Failure mode: Sutherland/DANGER3 data are useful fast negative controls and
orientation filters, but they are not direct CM trace-GCD rows for p24.

Pointer:

```text
p24/upstream_DANGER3/README.md
```

### Low-Degree Embedded-Tower / Selector Polynomial

Status: demoted.

Failure mode: the balanced quotient degree is still `66254`, and small scans
do not reveal a low-degree or low-recurrence selector except tautological
coefficient encodings.

Pointers:

```text
p24/embedded_selector_theorem_attempt.md
p24/cm_subfield_tower_boundary.md
p24/class_field_tower_phase_audit.md
```

### Phase / Borcherds / Kummer Coordinate Payload Alone

Status: demoted.

Failure mode: coordinate or phase payloads can miss determinant-line
p-unitness; determinant-zero controls survive coordinate-level certificates.
The selected-chain Kummer normal form also has a sharper finite caveat:
relative Kummer powers select the unordered child polynomial in a
one-Frobenius-orbit layer, but not in a multi-orbit layer.  The p24 `211`
layer has `ord_211(p)=35`, hence six primitive-character orbits, and the
ambiguity gate leaves `211^(6-1)=418227202051` cross-orbit phase choices
after global cyclic shift.  So six independent `211`-layer Kummer orbit
minpolys are not a child selector unless a producer also supplies cross-orbit
phase glue.

Replacement: determinant/Plucker line p-unit theorem, possibly with Kummer
descent only after the determinant line is identified.
For the selected-chain route, the corrected replacement is: `157`-layer
Kummer orbit data plus either `211` selected-child data, full relative morphism
data, or six `211` Kummer orbits together with explicit cross-orbit glue
invariants such as `T_a/T_1^a`.  The finite handoff and conservative
base-field `3107986` slot count are Lean-checked in
`KummerCrossOrbitGlueGate.lean`; the same gate also records the `3107816`
extension-object count.
The glue-complexity scan is negative for a low-degree parent formula:
`8/8` glue coordinates were full-degree in the cheap run, and `15/15` were
full-degree in the parent-count-forced run.  The same scan's Frobenius descent
audit found `21/21` and `45/45` glue values at full Frobenius degree, with
`0` proper descents (`3/3` and `13/13` in the nonsplit subrows).  Thus the
glue invariant is a valid payload target, not currently evidence of a hidden
simple formula or smaller-subfield descent.

Pointers:

```text
p24/centered_marginal_plucker_kummer_descent_boundary.md
p24/trace_gcd_plucker_kummer_payload.md
p24/relative_kummer_multi_orbit_ambiguity_gate.md
p24/lean/KummerCrossOrbitGlueGate.lean
p24/tower_kummer_glue_complexity_boundary.md
p24/trace_gcd_useful_computation_strategy.md
```

### Ordinary Toeplitz / Selected-Minor Norm Compression

Status: demoted.

Failure mode: selected matrices touch too many symbol positions; ordinary
norm collapse or small Toeplitz support does not isolate the p24 p-unit.

Pointers:

```text
p24/trace_frame_toeplitz_support_boundary.md
p24/subagent_selected_minor_norm_compression.md
```

### Global Product Mining / Orbit Norm Mining

Status: demoted to evidence.

Failure mode: small actual-CM orbit norms are nonzero in checked rows, but
this is not a proof of the p24 p-unit theorem and does not replace the
crossed-product determinant identity.

Pointer:

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
```

### Lean As Discovery Engine

Status: discarded.

Failure mode: Lean is useful only once the theorem statement is clear.  It
should formalize finite gates, dimension counts, and determinant implications,
not search for the missing CM p-unit identity.

Pointer:

```text
p24/lean/README.md
```

### Formal Right-Character Covariance As Right Potential

Status: discarded.

Failure mode: for the p24 raw convention `chi_k(2)=zeta_7^k`, formal
Frobenius covariance of the right multiplicative resolvent has eigenvalue
`epsilon_k=zeta_7^k`, exactly the matching twist needed by the product
coboundary.  Thus it lies in the obstruction eigenspace of
`sigma-epsilon_k`, not in the image.  The opposite twist would be a coboundary
but is the wrong product twist.  Pure cyclotomic degree-5549 internal periods
are nonzero in the split-prime audit, so this cannot be repaired by
cyclotomic orthogonality alone.

Replacement: prove genuine CM/Lang internal-trace or packet cancellation that
removes the matching-twist obstruction before invoking Hilbert-90.

Pointer:

```text
p24/trace_gcd_fixed_frequency_p24_right_coboundary_obstruction_gate.md
```

### Trace-Only Anchor Compression

Status: discarded.

Failure mode: the quotient trace profile
`T_r=Tr_relative(j_{r+m*bullet})` does not determine the anchor equations.
The same trace profile can pass or fail depending on the selected child
section in the trace defect `T_r-n*j_r`.  In the pinned actual-CM analogue,
all five global child shifts give distinct anchor defects and none passes.

Replacement: keep the section-aware `T_r,S_r=j_r` profile, or prove an
embedded CM/Lang theorem that directly authenticates the seven defect
H-coset sums.

Pointer:

```text
p24/trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate.md
```

## Rule For Future Work

Before reopening one of the discarded routes, write down the new ingredient
that changes its failure mode.  If there is no new ingredient, stay on the
live two-resultant plus fixed RS-tail chart route.
