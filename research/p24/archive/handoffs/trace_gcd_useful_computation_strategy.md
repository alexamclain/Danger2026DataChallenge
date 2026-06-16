# Trace-GCD Useful Computation Strategy

Date: 2026-06-06

Context cleanup entrypoints:

```text
p24/00_CURRENT_CONTEXT.md
p24/00_THEOREM_ATTEMPTS_LEDGER.md
p24/00_ROUTE_MAP.md
```

Read those first on future turns before opening broader p24 notes.

Computation is still useful, but only as a theorem microscope.  It should be
used to falsify proposed identities cheaply, calibrate against smaller actual
CM rows, and keep the finite certificate gates honest.  It should not be used
to enumerate a p24 class set, run a sqrt-scale search, or wait on bandwidth
when no new mathematical statement is being tested.

## Useful Computation

The useful lanes are:

```text
1. tiny split finite-field identities:
   verify exact algebraic rewrites such as
   product_t Delta(t) = Res(Y^d - 1, f) = det(m_f);

2. small actual-CM regression:
   test candidate Chow/Fitting/Borcherds identities on rows where the class
   set is small enough to enumerate in seconds;

3. p24-local invariant arithmetic:
   compute residue degrees, Frobenius orbits, support growth, valuation
   prerequisites, and payload accounting;

4. fast negative controls from Sutherland/DANGER3 data:
   test verifier-side selectors and branch labels, while remembering these are
   Montgomery triple datasets rather than direct CM trace-GCD fibers;

5. parallel subagent sweeps:
   split independent theorem candidates across small rows, but require every
   positive signal to graduate to an exact identity or p-unit theorem.
```

The pattern is:

```text
idea -> exact small statement -> seconds-scale falsifier -> theorem refinement
```

not:

```text
idea -> larger search -> hope the p24 row appears
```

## Current Experiment Priority

The answer to "is computation useful now?" is yes, but only for these
bounded theorem tests:

```text
1. factorized decimated trace-frame Schubert gate:
   verify the exact p24 dimensions
     A=158, B=210, prefix target=358, forced intersection=10,
   and keep the formal prefix/intersection/tail implications Lean-checked.

2. two-resultant actual-CM holdout:
   test Xi_O0 plus one nonzero crossed norm plus p-unit transport;
   expected useful signature:
     selected_two_punit_groups=4/4
     punit_transport_edges=8/8
     literal_equal_nonzero_edges=0/8
     naive_base_polynomial_groups=0/4.

3. Moore/residual determinant-line bridge:
   test that trace-GCD Fitting, trace-pairing, and residual Moore products
   detect the same p-unit event, including forced dependent controls.

4. full coinvariant tail gate:
   test that the fixed `140+16` resultant is equivalently one square
   class-field coinvariant map `R^4 + C_tail -> E/(tau_R-1)E`, including a
   forced control where the tail lies inside the prefix span, and an
   actual-CM determinant-line bridge from this square map to the trace-pairing
   and residual-product certificates.

5. crossed coinvariant norm gate:
   test that the nonzero representative orbit is the crossed/block-cycle norm
   of transported square coinvariant maps, including a forced singular local
   map, and check the same block-cycle identity on the two actual-CM rows
   used by the two-resultant holdout.

6. embedded-tower coefficient/Kummer complexity:
   test whether a proposed selected-chain producer has low-degree or
   low-recurrence structure on small complete CM cycles; current expectation
   remains negative except for forced tautological coefficients.  The
   multi-orbit Kummer ambiguity gate adds a specific guardrail: for the p24
   `211` layer, six independent Kummer orbit/minpoly payloads still need
   cross-orbit phase glue.  The glue-complexity scan then checks the repaired
   invariants `T_a/T_1^a`; current small actual-CM rows show full
   interpolation degree, so the glue is payload data, not a cheap formula in
   the parent period.

7. DANGER3 selector negative controls:
   test Montgomery-prefix character gates as constant-factor orientation
   filters, not as direct CM-fiber producers.

8. phase-divisor identity holdout:
   test whether a proposed phase/Borcherds unit dictionary recognizes the
   determinant-line phase vector before full-rank interpolation, and keep a
   determinant-zero control to reject coordinate/Kummer-only payloads.

9. simple-root/different boundary:
   check that split squarefree CM class-polynomial roots and Hensel-simple
   ordinary embeddings do not imply determinant-line p-unitness.

10. selected-tail tensor-factor transport:
    test whether the corrected residual-tail determinant has uniform
    zero/nonzero status across scalar-extension tensor factors; expect
    p-unit determinant-line scaling, not literal equality in arbitrary
    prefix-kernel bases.

11. visible LRS/MSRD shortcut falsifier:
    test whether natural-coordinate RS-tail columns already have a
    rational-normal/Reed-Solomon signature; expect rejection, which means any
    useful LRS theorem must provide an explicit p-unit block equivalence or use
    the full 210-column object.

12. full Plucker-chart visible GRS invariant:
    when the selected `156` columns are a basis, encode the omitted `54`
    columns by the `156 x 54` Plucker-ratio chart; a visible scalar GRS/MDS
    explanation would make the entrywise inverse chart rank at most `2`.

13. block/skew Cauchy displacement-rank candidate:
    replace the scalar entrywise-inverse test by the operator identity
    `A C - C B = R S`; scalar Cauchy has rank-one displacement, block
    resolvents have small Sylvester displacement rank, and random charts fail.

14. Plucker displacement handoff:
    prove the finite bridge from a low-rank full-column operator boundary
    `T S = S A + E_s`, `T O = O B + E_o` to low-rank chart displacement
    `A C - C B`; reject post-fit operators as non-certificate evidence.

15. RS-tail cyclic operator boundary:
    use the common cyclic/Lang shift on the six full right blocks; the four
    selected full blocks and one omitted full block contribute no boundary,
    while the split tail block contributes exactly two cut edges.

16. RS-tail frequency-defect selected-basis gate:
    diagonalize the cyclic/Lang shift and prove the selected basis before
    forming the Plucker chart; the finite gate reduces the determinant to
    19 ordinary local Plucker p-units, 16 defect tail residues, and a
    16x16 Fourier/Vandermonde p-unit.  The finite implication and p24 counts are
    Lean-checked in `p24/lean/TraceGcdFrequencyDefectGate.lean`.  The newest
    finite compression packages those local checks as cyclic resultants once
    the CM/Lang sections `P_24,T_24,S_24` are identified; the descent guardrail
    requires semilinear Frobenius-compatible local values and a Frobenius-
    stable defect support.  For p24, stable size-16 supports have exactly two
    types: `35` pure length-4 supports and `1225` mixed supports with four
    fixed frequencies.  The useful next arithmetic split is proving fixed
    frequencies ordinary versus identifying the mixed support explicitly.  The
    fixed-frequency ordinary gate pins this down to the local condition
    `rank(P_a,tau_a)=rank(P_a)` at the seven fixed frequencies.  The
    fixed-frequency annihilator bridge rewrites that as the trace-dual
    inclusion `Ann(P_a) subset Ann(tau_a)`, separating it from the prefix
    Plucker p-unit condition.  The relation-section/cyclic-syzygy gates then
    package the seven relations as one identity over `F_p[y]/(y^7-1)`, while
    warning that post-fit interpolation is not an intrinsic CM/Lang proof.  The
    Cramer/Bezout refinement makes the certificate surface
    `D*T = sum N_j*P_j` with `D in R_7^*`, so the denominator unit is exactly
    the fixed-prefix Plucker input and the full vector identity carries the
    no-fixed-defect content.

17. actual-CM full Plucker-chart and frequency-profile boundaries:
    check whether the available smaller actual-CM rows contain a nontrivial
    selected-basis calibration row for that full chart; current rows do not, so
    they cannot yet validate or falsify the visible-GRS/Cauchy invariant.
    The matching frequency-profile audit also finds that current rows are not
    p24-like local-gate calibrations: tail-only rows are too small, and the
    prefix-plus-tail singular controls have too many tail residue frequencies.
```

The first two are the live trace-GCD producer microscopes.  The coding-theory
items are guardrails against confusing a seductive pattern with an embedded
class-field identity.

## Current Fast Harness

The current coordinator is:

```text
p24/trace_gcd_fast_falsifier_harness.py
```

It runs:

```text
operator-norm/product/resultant toy checks;
p24 exterior-support sanity check;
p24 principal/cyclotomic split audit;
p24 unit-2 right-orbit compression audit;
block-cycle/Fitting zero-detection with singular controls;
dual-sparse Lean gate, plateau-factor negative control, difference-DFT
bridge audit, lambda-profile bridge audit, lambda-plateau rowspace audit, and
leading/plateau determinant-ratio audit;
trace-pairing/subspace-polynomial bridge audit;
trace-pairing/subspace low-rank toy;
actual-CM square coinvariant determinant bridge audit;
Gaussian-DFT plus Reed-Solomon-tail fixed determinant toy and actual-CM audit;
RS-tail semilinear-core/Hilbert-90 descent toy for the fixed square
determinant;
actual-CM RS-tail Hilbert-90 fixed-column audit for the explicit `Psi_RS`
columns;
RS-tail trace-adjoint syndrome toy for the full fixed source;
RS-tail syndrome Moore/Schur split toy with prefix and quotient-tail controls;
RS-tail selected-block support-profile toy with prefix/tail defect controls;
RS-tail full Plucker-chart Cauchy toy using the omitted 54 columns;
RS-tail block/skew Cauchy displacement-rank toy replacing the scalar Cauchy
shadow by a Sylvester identity `A C - C B = R S`;
Plucker displacement handoff toy and Lean gate, recording that a low-rank
full-column operator boundary implies low-rank chart displacement only for
operators fixed before seeing the chart;
RS-tail cyclic-shift row-space and column-boundary toys, isolating the
rank-two residue from the split tail block;
RS-tail frequency-defect selected-basis gate, showing cyclic invariance plus
local Plucker/tail-residue p-units gives the selected basis before the Plucker
chart exists;
RS-tail basis-free frequency-defect gate, showing the same implication using
only local projection ranks and prefix-to-prefix-plus-tail rank jumps after
arbitrary local row-basis changes;
RS-tail frequency-resultant gate, packaging those local checks as cyclic
resultants with controls for Plucker zeros, tail-residue zeros, and wrong
defect support;
RS-tail cyclic-section descent gate, rejecting post-fit splitting-field
interpolants and requiring Frobenius-compatible local values plus stable
defect support;
RS-tail p24 defect-support accounting, showing stable size-16 supports are
exactly `35` pure length-4 supports plus `1225` mixed fixed/length-4 supports;
actual-CM basis-free frequency-section audit, showing current actual local
rank profiles are Frobenius-covariant but fail by wrong defect-support size;
RS-tail fixed-frequency ordinary gate, showing mixed supports still pass
descent and the tail Vandermonde gate, so the local fixed-frequency theorem
`tau_a in image(P_a)` is the actual reduction from 1260 supports to 35;
fixed-frequency annihilator bridge toy, showing `tau_a in image(P_a)` is
equivalent to every trace functional killing the fixed prefix also killing the
tail, while prefix full rank remains a separate Plucker gate;
fixed-frequency relation-section and cyclic 7-section syzygy toys, packaging
the seven fixed-frequency relations as coefficient sections over
`F_p[y]/(y^7-1)` and separating intrinsic construction from post-fit
interpolation;
fixed-frequency Cramer/Bezout toy, upgrading the cyclic syzygy to
`D*T = sum N_j*P_j` with a unit denominator and controls for projected-only
proofs and zero-divisor denominators;
fixed-frequency order-5 collapse toy, showing the fixed `a=5b` frequencies of
a length-35 right orbit are determined by seven order-5 collapsed sums, while
nonfixed frequencies are not;
fixed-frequency relation-shape index, showing the bounded local search finds
p24-like right components but no non-tail-only left source orbit suitable for
a clean actual-CM calibration row;
actual-CM full Plucker-chart boundary audit showing the current small rows do
not calibrate the nontrivial selected-basis chart;
actual-CM frequency-defect boundary audit measuring the local profile on the
same smaller rows and confirming that none currently instantiate the p24
frequency gate;
RS-tail visible LRS signature toy rejecting the natural-coordinate shortcut;
Lean gate for the trace-pairing/subspace bridge;
residual prefix/tail split audit and Lean gate;
residual Moore/Chow section toy;
residual Schur-complement pivot toy;
prefix relative-trace adjoint toy and Lean gate;
prefix additive Hilbert-90 nonintersection toy;
prefix trace-dual normal-basis coefficient toy;
prefix Gaussian-period normal-basis toy;
prefix Gaussian DFT scalar-extension boundary toy;
prefix target-unit scaling pitfall toy;
prefix tensor-component kernel-transversality toy;
prefix component Frobenius-bookkeeping toy;
prefix semilinear first-component kernel-core toy;
prefix semilinear descent-to-fixed-relations toy;
prefix semilinear fixed-adjoint syndrome toy;
prefix syndrome coordinate Moore-residual toy;
prefix syndrome-to-resultant kernel/tail bridge toy;
prefix syndrome-to-resultant finite Lean gate;
prefix coinvariant rectangular-Fitting Lean gate;
full prefix-plus-tail coinvariant square-map toy and Lean gate;
crossed coinvariant norm toy and Lean gate for one nonzero orbit;
actual-CM square coinvariant block-cycle skew-norm audit, opt-in with the
two-resultant holdouts;
exact p24 tensor-factor decimated trace-period schedule;
relative trace normal-basis toy with nonnormal controls;
factorized trace-frame Schubert accounting;
small-CM pinned prefix-intersection audit;
small-CM pinned leading-residual value audit;
lead/prefix/tail finite toy;
selected-tail normal-basis/resultant equivalence toy;
selected-tail tensor-factor Lean compression gate;
selected-tail tensor-factor equivariance holdout, opt-in;
Schubert descent toy showing fixed sections descend but packetwise pivots do
not;
Lean gates for leading norm, denominator-safe lead-plus-prefix packaging,
prefix intersection, residual tail, selected-tail crossed-product propagation,
selected-tail phase-producer zero-detection, selected-tail
Borcherds/local-intersection handoff, prefix-plus-selected-tail crossed-package
propagation, annihilator avoidance, Schubert equivariant descent, and
packet-norm packaging;
determinant-line basis-change invariance toy;
diamond/right-unit determinant-line scaling toy;
safe 14-field and conditional 4-field verifier schemas;
one pinned actual-CM orbit-norm miner.
```

Latest run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
    --workers 4 --skip-spectral --no-danger3-inventory
```

reported:

```text
task_count=155
passed=155
failed=0
identity_mismatches=0
p24 support full by k=3
unit-2 cycles the six nonzero p24 right orbits
conditional unit-2 verifier payload has 4 field elements
p24 tensor factor: 70 degree-5549 factors over F_p(mu_66254)
p24 decimated trace frame: B/C degree 31, C/E degree 179, 537 coordinates for rank 368
relative trace normality: theta normal in B/E implies order-31 trace periods normal in C/E
factorized Schubert dimensions: forced_intersection_dim=10, residual_tail_dim=10
factorized surface: one-factor all-H F_p slots = 4.76828352e-3 * sqrt(p)
all-70-factor surface remains 0.3337798464 * sqrt(p)
packet-norm theorem surface: 4 relative degree-8 p-units with tensor symmetry
lead/prefix/tail toy: full lead nonzero forces prefix rank and tail injectivity
small-CM prefix audit: component_full=1, intersection_minimal=1, prefix_max_rank=1
small-CM leading audit: nonzero_determinant_rows=2, zero_det_norms=0
Schubert descent toy: fixed sections descend and packetwise spliced pivots do not
denominator-safe Lean gate: Xi_A, Xi_B, Xi_AB, Xi_lead exclude harmful packets
dual-sparse uncertainty finite gate passes
plateau subspace touches all seven right factors
cyclic difference is p-unit diagonal on nonzero right DFT coordinates
lambda profile, right periods, and Lang coordinates share zero conditions
lambda-plateau rowspace bridge has no nonvacuous small-row proof yet
leading/plateau determinant ratios vary in the square holdout
trace-GCD leading determinant and Moore residual product detect the same p-unit event
low-rank bridge toy confirms dependent coordinates make residual product zero
actual-CM square coinvariant determinant equals the trace-pairing determinant up to the trace Gram unit
Gaussian DFT diagonalizes full prefix blocks while the selected tail is an RS subspace
trace-pairing/subspace bridge finite implication is Lean-checked
residual product splits as prefix product times quotient-tail product
residual product equals the Moore/Chow section, with quotient tail images P_U(t_i)
quotient-tail Moore nonzero is equivalent to a Schur complement after a prefix pivot
prefix rank equals the rank of the relative-trace adjoint R^k -> L
prefix adjoint injectivity is equivalent to avoiding the Hilbert-90
coboundary space `(tau_R - 1)E`
prefix quotient rank equals trace-dual normal-basis coefficient rank
p24 right field has a type-6 Gaussian normal basis
Gaussian right-cycle DFT must stay in `L tensor F_p(mu_35)` to preserve rank
Gaussian DFT units cannot be divided out columnwise as base scalars
Gaussian tensor components require kernel transversality, not rank profiles alone
Gaussian tensor components rotate frequencies by p^r mod 35 and conjugate coefficients
first component kernel is large; prefix theorem is zero semilinear T-core
zero semilinear T-core is equivalent to no nonzero fixed relation in F_p^28+K^28
fixed relation injectivity is equivalent to syndrome surjectivity L -> F_p^28+K^28
syndrome surjectivity is equivalent to nonzero Moore residual product of 140 L-elements
the 140 syndrome p-unit leaves a 16-dimensional kernel; the tail resultant must separate it
the syndrome/tail handoff is Lean-checked as a finite implication
prefix quotient map has a rectangular maximal-minor/Fitting p-unit target
full 140+16 fixed resultant is equivalent to a square coinvariant p-unit
nonzero representative is a crossed norm of transported square coinvariant maps
block-cycle Fitting determinants detect local singular tail maps
diamond transports preserve p-unitness but not literal determinant equality
pinned actual-CM orbit norms: nonzero_orbits=6, zero_or_bad_orbits=0
principal Hilbert Frobenius identity but cyclotomic semilinear motion remains
selected-tail tensor-factor compression finite implication is Lean-checked
RS-tail frequency-defect gate proves the selected basis before the Plucker
chart, while cyclic-invariant failing controls show the local p-unit gates are
necessary
RS-tail basis-free frequency gate proves the same selected-basis implication
from projection-rank/rank-jump gates, so the CM/Lang proof does not need a
friendly frequency basis
RS-tail frequency-resultant gate packages the local Plucker and defect
tail-residue checks as cyclic resultants once the CM/Lang sections are known
RS-tail cyclic-section descent gate rejects post-fit splitting-field
interpolants and requires semilinear Frobenius compatibility
p24 defect-support accounting shows descent alone leaves 1260 stable size-16
supports: 35 pure length-4 supports and 1225 mixed supports
fixed-frequency ordinary gate shows mixed supports survive descent/Vandermonde;
the no-fixed-defect theorem is exactly tail-inside-prefix at fixed frequencies
fixed-frequency annihilator bridge recasts tail-inside-prefix as
Ann(prefix) subset Ann(tail), the proof-facing trace-adjoint target
fixed-frequency cyclic syzygy gate packages the seven relations over
F_p[y]/(y^7-1), but post-fit interpolation remains non-proof evidence
fixed-frequency Cramer/Bezout gate sharpens that package to one unit
denominator plus four numerator sections over F_p[y]/(y^7-1)
fixed-frequency order-5 collapse gate explains why the fixed relation can be
tested/proved in the 7-part without a primitive 35th root
fixed-frequency symmetry boundary shows right centering plus sign symmetry
forces only the trivial fixed frequency, not the six nontrivial order-7 ones
fixed-frequency order-7 augmentation gate shows that the stronger six-orbit
augmentation plus `P_4=y^{-2}T` would give an explicit no-fixed syzygy
fixed-frequency order-7 coset dictionary identifies that augmentation with
vanishing of all characters of the `C_7` quotient of `(Z/211Z)^*`; ordinary
centering is only the trivial quotient character
fixed-frequency order-7 character-projection gate identifies the exact
right-profile theorem: the nontrivial augmentation components are nonzero
Gauss sums times `sum_{s != 0} chi_k(s)^(-1)G_s`, and a centered random
profile can still have all six nontrivial components nonzero
fixed-frequency multiplicative-resolvent bridge identifies the same
vanishings as orthogonality against six right order-7 multiplicative
resolvents, and rejects the Frobenius-only proof mirage because the Gauss-sum
factor carries the nontrivial `p^156` eigenvalue
fixed-frequency class-character expansion gate rewrites the target as the
relative packet product sum `sum_a T_{1,0,a}R_{chi,-a}`, so the next theorem
must prove packet cancellation or stronger termwise right-combo vanishing
fixed-frequency p24 raw/product-coboundary gates sharpen the useful
computation target: construct a raw full-order CM/Lang coboundary before
trace-zero inversion, or prove left covariance plus the matching
right-resolvent coboundary
`R_{chi,-a}=sigma(V_{chi,a})-(epsilon_chi/alpha_a)*V_{chi,a}`.  The formal
Leibniz identity then supplies the raw product coboundary; wrong twists and
random right factors fail in the finite model.  The p24 twist bookkeeping
gate fixes the raw convention to `alpha=1` and `epsilon_k=zeta_7^k` for
`chi_k(2)=zeta_7^k`.  The right-coboundary obstruction gate shows formal
right-character covariance has that same eigenvalue, so it is the obstruction
to `sigma-epsilon_k`, not the desired potential.  Useful computation should
now test CM/Lang internal-trace cancellation, not this covariance shortcut.
The internal-trace gate makes this exact: matching right coboundary is
equivalent to nested internal-trace zero, after which Hilbert-90 inversion is
formal rather than circular.  The stage-target gate further shows the proof
should target `Tr_{C/E}(Tr_{B/C}(...))=0`, not the much stronger
`Tr_{B/C}=0`.  The Gaussian-functional gate identifies this target as
`sum_k c_k eta_{ak}=0`; it is weighted period cancellation, not relative
content/nonvanishing.  The right Gauss weighted-polynomial gate names the
obstruction as `tau(chi)*G_chi(zeta_n^{-a})`, and the right-axis spectrum
gate observes that `p^5460` fixes the right `211` axis, so internal trace
does not average the seven H-cosets.  The newest right-axis
covariance/descent gate gives the useful finite theorem to prove for the
internally traced `G_chi` profile: `p^780` shifts the seven cosets by `6`;
covariance plus descent of one anchor sum to the `p^780`-fixed field
forces equal H-coset sums, while covariance alone and descent alone both leak
order-7 spectrum.  Under covariance, that anchor descent is equivalent to the
target vanishing.  The fixed-field refinement says this exact field has
degree `780=156*5`; `F_p(mu_157)`-descent is stronger than necessary, and
pure right H-periods are covariant but still leak.  The anchor-projector gate
spells this fixedness out as six nontrivial rho-eigenprojector vanishings
`Pi_k(Y_0)=0`; a split `F_8863` pure-period control shows all six raw
H-period projectors are nonzero.  The projector-character bridge verifies
the p24 index map `m -> 6m mod 7`, so these are exactly the six nontrivial
H-quotient character equations in the `1092` scalar payload.  The
projector/internal-character target gate combines this with the nested
trace target: after `Tr_{B/C}`, each nontrivial projector channel must have
zero trivial `C/E` component.  The actual-CM projector/internal-character
boundary rules out the generic projector shortcut: in the `D=-5000`,
`h=30=2*5*3` calibration, all `30/30` nontrivial top-projected packets have
nonzero final internal trace.  The actual-CM product/internal-trace boundary
also rules out generic weighted-product cancellation: the pinned
`D=-13319, m=28=4*7, n=5` analogue has `0/2` zero product internal traces
and `0/1` zero recombined `<q>` product traces.
Lean now
formalizes the seven-coset
implication, so the remaining work is arithmetic construction of covariance
and this no-trivial-`C` statement for the traced weighted `G_chi` packet.
The Lean projector-trace pipeline gate now composes the next formal layer:
if those six projected final internal traces vanish, then matching right
coboundaries, product coboundaries, nontrivial character payload zeroes, and
the `1092` H-coset verifier follow by finite algebra.  Computation should
therefore test or illuminate the projected weighted-packet trace identity
itself, not re-check the handoff chain.
fixed-frequency order-7 H-coboundary gate rewrites the same theorem as an
additive Hilbert-90 potential for `H=<2^7>`:
`G_s=Y_s-Y_{2^7s}`.  This is the next useful tower-native object to test or
construct; ordinary centering is not enough.
fixed-frequency H-Bezout operator gate makes the potential deterministic:
prove `e_HG=0`, then `Y=UG` with
`U=(1/30)sum_{i=0}^{29}(29-i)T^i`; no sampling is needed for `Y`.
fixed-frequency paired-potential boundary shows the exact target is the
paired `L`-profile potential.  A full right-resolvent potential before
Hermitian pairing is sufficient but stronger than needed.
fixed-frequency H-coboundary base-field boundary rewrites the exact target as
row-wise vanishing of the seven multiplicative Gaussian-period column sums of
the centered `156 x 210` mixed marginal matrix; a pinned actual-CM analogue
has coset-sum rank `2`, so this identity is not generic
fixed-frequency H-coset selector boundary shows the nontrivial quotient
selectors have full additive right Fourier support (`210/210` nonzero
frequencies), so the H-coboundary proof must be a full Gaussian-period
cancellation, not a sparse support shortcut
fixed-frequency order-7 rank-compatibility gate shows augmentation adds six
equations beyond centering while still leaving a `203`-dimensional right
subspace, so it is compatible with the `156`-rank fixed square
fixed-frequency unit-symmetry boundary rejects the naive diamond shortcut:
multiplier invariance would force quotient-character vanishing, but the
pinned actual-CM analogue has nonzero quotient projection and `18`
multiplier-invariance failures
fixed-frequency relation-shape index finds p24-like right components in the
bounded scan but no non-tail-only left source orbit, so no clean small
actual-CM calibration row has been found for the `right_len=35` relation
actual-CM frequency-profile audit measured the current smaller rows:
frequency_profile_gate_rows=0/10 and clean_p24_like_shape_rows=0/10, so the
available rows remain boundary evidence rather than positive calibration
actual-CM basis-free section audit measured the same rows:
rank_profile_frobenius_covariant_rows=10/10, basis_free_section_candidate_rows=0/10,
and prefix_tail_wrong_defect_size_rows=4/4, so the obstruction is support size
rather than descent
```

With the opt-in actual-CM unit-action falsifier:

```text
--include-actual-cm-unit-action
```

the harness reports:

```text
passed=13
failed=0
literal_equal_edges=0/4
punit_ratio_edges=4/4
```

With the opt-in two-resultant holdout audit:

```text
--include-two-resultant-holdouts
```

the harness previously reported the optional payload clean; with the current
task list this command enumerates the additional order-7 gates, and the
optional payload was not rerun in the latest focused verification:

```text
task_count=155
passed=not_rerun_in_latest_focused_pass
failed=0
selected_two_punit_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
block_cycle_matches=12/12
block_cycle_full_rank_detection_matches=12/12
square_coinvariant_block_cycle_is_skew_reduced_norm=1
```

This is now the best actual-CM theorem microscope for the compressed route:
it tests the pinned `D=-13319` row and the independent `D=-26759` holdout,
and it phrases the evidence as fixed resultant plus one nonzero crossed norm,
p-unit transport, and the square-map block-cycle form of the nonzero skew
reduced norm.

The 2026-06-06 rerun also inventoried the local Sutherland/DANGER3 files:

```text
pp10.txt      236264 lines
pp12.txt.gz   3083880 lines
pp16A.txt.gz  4713069 lines
pp20.txt      82023 lines
pp24.txt.gz   1077869 lines
```

Those files remain useful as negative/control data for selector hypotheses,
not as direct trace-GCD CM fibers.

This supports the current boundary:

```text
the operator/global-resultant packaging is exact,
small actual-CM phase/Fitting structure is real,
but p24 has full exterior right-frequency support,
so sparse Fourier compression is not the theorem.
```

The current positive-size actual-CM norm microscope is:

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
p24/trace_gcd_actual_cm_orbit_norm_mining.md
```

Its broad scan mode is opt-in.  A one-minute broad PARI pass with small class
sizes produced no positive-size rows before being stopped, so this script is
kept pinned by default to avoid turning theorem testing into a search.

The current right-unit overcompression falsifier is:

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
p24/trace_gcd_actual_cm_unit_action_falsifier.md
```

On the same pinned actual-CM row, the unit `3 mod 7` swaps the two nonzero
right orbits.  The actual orbit norms are nonzero but not literally equal:

```text
literal_equal_edges=0/4
punit_ratio_edges=4/4
```

Thus the p24 unit-2 theorem must prove determinant-line equivariance up to
p-unit scale.  It must not claim equality of printed scalar representatives.

The finite algebra shape of that equivariance is checked by:

```text
p24/block_cycle_fitting_zero_detection_toy.py
p24/trace_gcd_diamond_equivariance_toy.py
p24/trace_gcd_diamond_fitting_equivariance_target.md
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
p24/lean/TraceGcdLinearizedResultantNormGate.lean
```

The toy reports:

```text
punit_edges=600/600
determinant_mismatches=0
singular_zero_mismatches=0
```

This proves no arithmetic input, but it guards the exact determinant-line
handoff that the p24 class-field proof should instantiate.

The resulting two-resultant arithmetic target is:

```text
p24/trace_gcd_two_linearized_resultant_target.md
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/trace_gcd_two_resultant_holdout_audit.py
```

It names the two remaining p-units as one fixed linearized resultant and one
degree-35 Frobenius/crossed norm of linearized resultants.

The current status of the requested nonvacuous rowspace stress test is:

```text
p24/trace_gcd_nonvacuous_rowspace_search_status.md
```

A bounded 30-second scan found actual-CM low-rank controls, but not a clean
p24-shaped nonvacuous containment case.  The observed failures were either
under-coordinate after deletion or noncoprime in the left/right orbit degrees.

The holdout audit reports:

```text
selected_two_punit_groups=4/4
all_nonzero_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

So computation is now pointing toward the semilinear Fitting theorem, not a
plain `F_p[Y]` resultant or a literal unit-invariance formula.

The newest dual-sparse bridge microscope is:

```text
p24/trace_gcd_difference_dft_bridge.md
p24/trace_gcd_difference_dft_bridge_audit.py
p24/trace_gcd_lambda_profile_bridge.md
p24/trace_gcd_lambda_profile_bridge_audit.py
p24/trace_gcd_lambda_plateau_rowspace_audit.py
p24/trace_gcd_lambda_plateau_det_ratio_audit.py
p24/centered_plateau_factor_support_audit.py
p24/lean/TraceGcdDualSparseBridgeGate.lean
```

The actual-CM audit reports:

```text
dft_difference_mismatches=0
nonzero_multiplier_failures=0
direct_rowspace_equal=0/1
lambda_fourier_trace_mismatches=0
lang_reconstruction_mismatches=0
lang_zero_equivalence_failures=0
rowspace_containment_failures=0
nonvacuous_containments=0
vacuous_full_leading_rank=10/10
both_nonzero=2/2
rowspace_equal=2/2
distinct_nonzero_ratios=2
plateau_subspace_dim=54
nonzero_factor_blocks=7/7
```

Thus the coordinate identity

```text
DFT_right(P_b - P_{b-1})_v
  = (1 - zeta_right^v) * DFT_right(P_b)_v
```

is available up to p-units, and the lambda-level audit identifies the same
parameter through the centered profile, right periods, and Lang/Fitting
coordinates.  The direct rowspace shortcut is still false.  The remaining
theorem is now the nonvacuous plateau-vanishing/rowspace-containment
implication for that bad `lambda`, not a generic cyclic-code argument.

The verifier surface for this route is now explicit:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```

It reports:

```text
expected_payload_field_elements=4
expected_payload_over_sqrt_floor=4e-12
producer_honesty_required=1
diamond_equivariance_required=1
```

The first global-product miner is:

```text
p24/trace_gcd_global_product_miner.py
```

It found low-weight formulas for the isolated scalar `Pi_all` in the pinned
small row, but no corresponding phase-vector formulas.  The result is recorded
in:

```text
p24/trace_gcd_global_product_mining_boundary.md
```

This says global-product computation is useful mainly as a divisor-honesty
test.  Scalar matches alone should be treated as false leads.

## Sutherland Triple Data Negative Control

A sidecar-suggested bounded run on the local upstream full-triple file:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/full_small_triple_halving_audit.py \
  --source p24/upstream_DANGER3/pp12.txt.gz \
  --residue 7 --min-p 2048 --branch-depth 10 --max-prefix 8
```

reported:

```text
rows=539616
distinct_prefixes=12011
prefix_loglog_exponent=0.548752
low-degree x/s features near 0.500 capture after the branch explanation
inverse branch symbols near uniform beyond the terminal branch
conclusion=no growing statistical_or_algebraic_selector_was_detected
```

The all-prefix near-square check:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/upstream_nearsquare_prefix_gate_audit.py \
  --c 7 --n-mod 8 --n-residue 0 --min-p 32768 --max-p 65536
```

reported:

```text
prime_rows=6
good_A_rows=7456
mean_good_A_over_sqrt=5.945777
dominant_gate_capture=0.493562
```

Thus the uploaded DANGER3 data does not expose a growing verifier-side
selector after the known branch gate.  It is still useful as a falsifier for
cheap Montgomery or ML-style residual selectors, but it does not replace the
phase-aware trace-GCD/Fitting nonintersection theorem.

## Calibration Scarcity

A useful p24 analogue would have a nonzero full-block prefix plus a square
tail-on-kernel determinant, mirroring the p24 `140+16` split.  A 2026-06-06
shape-only pass found candidates such as:

```text
D=-80471 h=455 q=523 m=65 n=7 components=[5,13]
left=5:L4 right=13:orbits[3,3,3,3]
full_blocks=1 tail=1.

D=-169991 h=693 q=719 m=99 n=7 components=[9,11]
left=11:L5 right=9:orbits[2,2,2,2]
full_blocks=2 tail=1.
```

But pinned actual-CM checks on those rows did not produce eligible Hilbert
splitting/full-cycle trace-GCD rows, and a bounded actual-CM scan found no
nonzero-prefix square-tail calibration row:

```text
timeout 45s python3 p24/lang_trace_gcd_kernel_audit.py ...
  rows=0

timeout 45s python3 p24/lang_trace_gcd_monodromy_basis_audit.py ...
  no eligible monodromy row found

timeout 45s python3 p24/lang_trace_gcd_spectral_scan.py ...
  rows=0
```

This does not weaken the p24 theorem.  It means faithful small analogues are
sparse, so computation should be treated as a falsifier for exact identities
and not as an open-ended hunt for a miniature p24 instance.

The newest example is the right-combo anchor boundary:

```text
p24/trace_gcd_fixed_frequency_actual_cm_right_combo_anchor_boundary.py
```

On the pinned `D=-13319, q=13463, m=28=4*7, n=5` row, `<q>` is all of
`F_5^*`, so the recombined period-coset balance has no nontrivial quotient
equations and is exactly the anchor equation
`sum_{k=1}^4 c_k=4*c_0`.  The actual right-combo `G_chi` analogue fails it.
This is a useful small-data result because it kills the shortcut
"right-combo plus decomposition-field trace language implies the anchor";
the p24 proof must use p24-specific weighted `G_chi` structure or construct
an explicit potential.

The companion finite algebra gate
`p24/trace_gcd_fixed_frequency_p24_anchor_trace_defect_gate.py` rewrites the
six p24 anchors as the nontrivial order-7 right spectrum of the relative trace
defect `Tr_relative(j_{r+m*bullet})-n*j_r`.  That is the useful object for the
next proof attempt.

The payload/accounting companion
`p24/trace_gcd_fixed_frequency_p24_trace_average_anchor_payload_gate.py` then
separates verifier size from producer honesty: seven honest defect H-coset
sums would verify the anchors, while the fuller trace-average plus
selected-child profile has size `132508`, still far below `sqrt(p)`.  This
does not solve the producer problem; it tells us exactly what kind of
embedded tower data would be enough.

The section-choice companion
`p24/trace_gcd_fixed_frequency_p24_section_choice_obstruction_gate.py` rules
out the tempting `m=66254` trace-only compression.  The same quotient trace
profile can pass or fail the anchor depending on the selected child section;
the pinned actual-CM row also has `0/5` globally shifted child anchors passing
and `5/5` distinct defects.  So the producer must be section-aware, or must
directly authenticate the seven defect H-coset sums.

The scale-discipline gate `p24/p24_subsqrt_scale_discipline_gate.py` keeps the
near-sqrt composite correspondence in its lane.  The selected-chain and full
relative-table surfaces are `3.1e-6 * sqrt(p)`, while the optimistic seeded
correspondence proxy is `0.968924963328 * sqrt(p)` and `3.1177e5` times
larger than the selected chain.  It is a constant-factor sqrt-scale route, not
the asymptotic speedup.

For the centered p-unit route,
`p24/centered_marginal_full_origin_phase_sensitivity_gate.py` shows that the
full-origin centered Chow product is not determined by unordered recovery
fibers.  Cyclic origin shifts preserve the product in the pinned actual-CM
row, but recovery-fiber shuffles change it in `8/8` controls.  Future
centered-product tests should therefore target a phase-aware Chow/Fitting
divisor or local-intersection formula, not fiber multiset summaries.
The companion
`p24/centered_marginal_full_origin_edge_shape_boundary.py` closes the first
bounded oriented-edge model: no bidegree-`<=4` polynomial or rational formula
in `(j_i,j_{i+1})` matches the centered determinant sequence in the pinned
row.
The short-path companion
`p24/centered_marginal_full_origin_path_shape_boundary.py` also finds no
subgeneric low total-degree formula in the two-edge path
`(j_i,j_{i+1},j_{i+2})` or three-edge path
`(j_i,j_{i+1},j_{i+2},j_{i+3})`.
The positive plumbing check
`p24/centered_marginal_orbit_fitting_block_cycle_audit.py` verifies that the
actual centered Schubert window matrices assemble into direct-sum and signed
block-cycle orbit Fitting determinants with exact zero detection.  The
crossed-product determinant line is therefore a valid target; computation is
now pointing at the arithmetic p-unit theorem for that section, not another
finite determinant identity.

## Non-Useful Computation

The following would not currently move the proof:

```text
enumerating O(sqrt(p)) candidates;
constructing all p24 CM roots directly;
expanding the binomial(35,16) Plucker sum without a new identity;
running broad random searches not attached to a named divisor/norm theorem;
streaming DANGER3 files looking for a selector unless the selector has a
specific finite-field prediction;
following the composite seeded correspondence as a success condition; it is
only a near-sqrt constant-factor proxy, not the requested asymptotic win.
summarizing the centered full-origin product by unordered recovery fibers
without an accompanying phase-aware divisor identity.
treating one bounded oriented edge `(j_i,j_{i+1})` as the centered full-origin
producer without a new higher-phase construction.
treating short adjacent paths as the centered full-origin producer without a
divisor-level reason; the current two-edge/three-edge low-degree tests are
negative.
```

## Best Next Computational Tests

The next cheap tests should be attached to the global Chow/Borcherds target:

```text
1. global-resultant identity mining:
   on small actual-CM rows, compute the full product
   Pi_all = product_t Delta(t) and test whether it matches any low-height
   class-field norm, modular unit, or phase-unit expression;

2. divisor support audit:
   for each candidate product expression, factor numerator/denominator in the
   small row and check whether its zero divisor is the actual Chow divisor,
   not merely a correlated phase function;

3. local-intersection rehearsal:
   in a small row with a selected prime, compare valuation(Pi_all) with
   explicit bad-intersection counts to validate the Borcherds/Fitting handoff;

4. parallel candidate falsification:
   send independent subagents to try bounded product dictionaries, modular
   unit spans, and tensor/Chow determinant-line comparisons on the same small
   rows, then synthesize only exact survivors.
```

So the answer is yes: computation is useful for testing.  The constraint is
that every job should either falsify a theorem candidate in seconds or produce
an exact identity worthy of proof.

## Strong-Rayleigh Probability Boundary

The newest cheap falsifier is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/axis_crt_strong_rayleigh_obstruction_toy.py
```

It reports an exact positive integer Rayleigh violation for the `(2,2,3)`
complete tripartite incidence analogue:

```text
strong_rayleigh_violated=1
rayleigh_delta
  = -7988395388171953562263529025459059314667521815134984779980
```

This kills the support-level strong-Rayleigh/real-stability shortcut.  The
ordinary CRT-axis matroid still has useful Hodge/Lorentzian structure, but
probability theory does not supply the p24 p-unit noncancellation certificate
without an additional arithmetic identity.

The fast harness now includes this check:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory

task_count=155
passed=155
failed=0
```

The holdout-inclusive variant has this current task count; its optional
two-resultant payload was not rerun in the latest focused verification:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory \
  --include-two-resultant-holdouts

task_count=157
passed=not_rerun_in_latest_focused_pass
```

The opt-in phase-divisor identity holdout is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory \
  --include-phase-divisor-holdout

task_count=156
passed=not_rerun_in_latest_focused_pass
nonrandom_span_hits=0
full_rank_interpolation_hits=4
coordinate_payload_zero_detection_failure=1
```

The opt-in simple-root/different boundary is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory \
  --include-simple-root-boundary

task_count=156
passed=not_rerun_in_latest_focused_pass
class_polynomial_split_squarefree=1
zero_derivative_count=0
control_det_zero=1
```

The opt-in selected-tail tensor-factor holdout is:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fast_falsifier_harness.py \
  --workers 4 --skip-spectral --no-danger3-inventory \
  --include-selected-tail-tensor-factors

task_count=158
passed=not_rerun_in_latest_focused_pass
tail_zero_status_uniform=1 on D=-10919, D=-1559, D=-2207
selected_tail_transport_survives=1 on every checked group
proper residual-tail norm equality often fails
```

The selected-tail tensor-factor result is recorded in:

```text
p24/trace_frame_selected_tail_tensor_factor_equivariance_boundary.md
```

It sharpens the surviving theorem candidate to:

```text
Delta_tail(i') = p-unit * sigma(Delta_tail(i))
```

on the selected-tail determinant line.  If proved for p24, this reduces the
70 scalar-extension tensor factors to one representative selected-tail
p-unit target.
