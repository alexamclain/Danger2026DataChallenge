# CS / ML Theory Imports

This note answers which CS or ML theory seems genuinely useful for the p24
certificate problem.

## Best Import: Coding Theory / Subspace Evasiveness

The current marginal theorem can be rephrased as:

```text
structured CRT-axis codeword w
  -> x_w = sum_r w(r) J_r(theta)
  -> Top_k(x_w)
```

has no nonzero kernel on the selected structured code.

That is exactly a **subspace-evasive** or **superregular generator matrix**
problem:

```text
image of a low-dimensional structured code avoids a fixed trace-annihilator
subspace.
```

Useful CS vocabulary:

```text
subspace-evasive set
rank condenser
MDS / superregular matrix
cyclic code minimum distance
rank-metric code / Gabidulin-style normality
list-decoding obstruction
```

The p24 form is not a random code, but these notions give the right proof
surface:

```text
prove that the CM marginal generator matrix is superregular
on the CRT-axis family, or prove it is a rank condenser for the
trace-annihilator tests.
```

This is the most promising import because it matches the theorem exactly,
not just heuristically.

## Algebraic Complexity / PIT

The exterior products

```text
Omega_1, Omega_211, Omega_3
```

are polynomial identities in the embedded CM marginal data.  The desired
certificate is:

```text
these determinant / exterior polynomials do not vanish modulo the selected p.
```

So algebraic complexity contributes:

```text
polynomial identity testing language;
hitting-set / rank-condenser analogies;
arithmetic-circuit factorization questions;
resultant/norm packaging of beta-shift Plucker coordinates.
```

The caution is that PIT proves generic nonzero; p24 needs selected-prime
nonzero.  The useful lift is therefore a **p-unit PIT certificate**:

```text
identify a determinant polynomial whose CM norm is not divisible by p.
```

## Additive Combinatorics / Uncertainty

The beta-product route asks about character support of beta-shifted Plucker
coordinates.  This imports:

```text
Donoho-Stark uncertainty;
sumset growth;
Fourier support of product/exterior representations.
```

The p24 support audit is mostly negative for compression:

```text
O = <p^5460> mod 3107441, |O|=5549
O+O misses only 16648 residues
O+O+O is all of Z/nZ
```

So additive combinatorics helps rule out easy low-support compression.  It
does not yet prove nonvanishing.

## Expander / Spectral Graph Theory

Class-group and isogeny graphs suggest an expander-mixing approach:

```text
CM orbit samples should look pseudorandom against low-complexity tests.
```

This could support a deterministic rank-condenser theorem if one can connect
Hecke/Brandt expansion to the exact finite-field trace-annihilator tests.

Current limitation:

```text
expansion gives average/equidistribution;
p24 needs selected-prime p-unit nonvanishing.
```

So this is plausible but not yet a certificate.

## ML: Useful For Search, Not For Proof

ML can help choose hypotheses:

```text
rank candidate minors by stability across small CM rows;
search for low-height formulas or hidden invariants;
use symbolic regression to propose Plucker/norm identities;
cluster failures to identify missing structure.
```

But ML cannot certify the p24 selected prime.  Any ML output must graduate to
one of:

```text
exact finite-field identity;
p-unit/norm theorem;
Lean-checked finite implication plus arithmetic nonvanishing proof.
```

## Practical Next CS-Theory Translation

The cleanest next theorem to try is:

```text
CM marginal generator is a rank condenser for the CRT-axis code:

for each k in {1,2,3}, every nonzero structured CRT-axis weight w
has Top_k(sum_r w(r) J_r(theta)) != 0
in the required split block.
```

Equivalently:

```text
the p24 marginal exterior products are Plucker p-units.
```

This imports the right CS intuition while keeping the final object arithmetic
enough to become a strict DANGER3 certificate.

## 2026-06-05 Structured-Code Audit

The follow-up status note is:

```text
p24/cs_rank_condenser_theorem_status.md
```

I added:

```text
p24/tensor_factor_marginal_cs_structure_audit.py
```

It treats the current CRT marginal rows as a code generator matrix and tests
for the most obvious off-the-shelf structure:

```text
MDS/open-cell maximal minors;
Toeplitz displacement rank;
Hankel displacement rank;
cyclic Toeplitz/Hankel displacement rank;
random tensor-factor controls with the same shape.
```

On the pinned `D=-10919, m=12` tensor row, the CM matrices for the full
two-window axis target, the one-window `constant+4` target, and the one-window
trace-zero component target all have full rank.  But their Toeplitz/Hankel and
cyclic displacement ranks are maximal and exactly match random controls.

So the CS import is now sharper:

```text
use rank-condenser/PIT/Moore language to state the theorem,
not as evidence that the natural marginal matrix is a known
Toeplitz/Cauchy/GRS determinant in disguise.
```

The surviving route is a selected CM p-unit theorem for the Plucker content,
or a Moore/Gabidulin normality parent theorem with a class-field proof.

## 2026-06-06 Update: MDS/Superregularity Check

I reran the CS-structure audit on the pinned `D=-10919, m=12` tensor row for
the current two-window marginal target:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_marginal_cs_structure_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --only-m 12 \
  --max-n 200 --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --subdegree 3 --windows 2 \
  --target full --random-trials 40 --max-minors 1000
```

The full `constant+4+3` matrix is square `6 x 6` and full rank:

```text
rank=6/6
displacement=cyclic_hankel:6,cyclic_toeplitz:6,hankel:6,toeplitz:6
random rank_hist={6: 40}
```

The rectangular component checks are also superregular in the tested maximal
minor range:

```text
target=constant+4: rows=4, cols=6, maximal 4-minors tested=15, zero=0
target=4 trace-zero: rows=3, cols=6, maximal 3-minors tested=20, zero=0
target=constant+3: rows=3, cols=6, maximal 3-minors tested=20, zero=0
```

But the matching random tensor-factor controls have the same behavior:

```text
rank_hist full at capacity in 40/40 trials
maximal_minor_zero_hist={0: 40}
all Toeplitz/Hankel/cyclic displacement ranks maximal
```

So the MDS/superregular signature is real but generic at this scale.  It is a
good language for the theorem, not a proof source.  The arithmetic theorem
still has to explain why the selected CM specialization is a p-unit, or
replace the generic open-cell determinant by a class-field identity whose
nonvanishing is forced.

## 2026-06-05 Update: Trace-Frame Local Unit Form

For the current trace-frame/Fitting route, CS theory is useful only after it
becomes an exact arithmetic theorem:

```text
hidden MSRD/LRS:
  prove W_axis(B) subset C^31 is p-unit block-equivalent to a high-distance
  sum-rank code;

p-unit PIT:
  prove the named CM-weighted Schubert determinant is not divisible by the
  selected prime;

rank-condenser language:
  phrase the same theorem as the selected residual-tail nonintersection
  K_sel,Omega = {0}, where K_sel is W_axis cap F_28 plus the ten-coordinate
  tail-head condition.
```

The full top-three statement `W_axis cap F_27={0}` is only a necessary
consequence of the selected-leading theorem; see
`p24/trace_frame_selected_lead_failure_module.md`.

Generic probability, learned predictors, and ordinary PIT are diagnostics:
they can suggest which determinant to test, but they do not certify the fixed
prime `p=10^24+7`.  The current small falsifier to add next, if we keep
probing the CS route, is a block-equivalence invariant comparison against
synthetic LRS/MSRD controls on the pinned `D=-10919, m=12` row.

## 2026-06-05 Update: Imports for the Paired 3B + 6T Surface

The live p24 certificate is now the paired mixed-Hermitian leading-erasure
surface:

```text
3 four-block prefix p-units B,
6 quotient-tail p-units T,
156 = 4*35 + 16.
```

For this surface the useful CS imports are more precise:

```text
rank-metric normality
subspace-polynomial annihilators
Moore determinant factorization
interleaved Gabidulin/skew-linearized systems
erasure-code language
deterministic rank condensers / subspace-evasive images
PIT with arithmetic p-unit lifting
```

The strongest import is rank-metric/subspace-polynomial theory.  The prefix
factor `B` says that four right trace packets span a `140`-dimensional
subspace of `L = F_p(mu_157)`.  The tail factor `T` says that the quotient
annihilator left after those four packets is killed by no nonzero vector in
the first `16` tail coordinates.  This is exactly the incremental
linearized-polynomial update

```text
P_new(X) = P(X)^p - P(c)^(p-1) P(X),
```

with the residual norms serving as Moore-minor witnesses.

Erasure-code language is also productive.  The six delete-one tests say that
the `156`-dimensional trace image `Phi(L) subset F_p^210` avoids six explicit
`54`-dimensional erasure spaces.  The paired manifest is a systematic
puncturing/shortening certificate: four complete packets plus a length-16 tail
recover the whole source after any one packet deletion.  This language makes
the optimality of three prefix factors transparent, but it does not collapse
the six tail factors by linear algebra alone.

Algebraic-complexity/PIT language remains useful only after arithmetic
lifting.  Generic PIT would say a determinant polynomial is not identically
zero.  The p24 certificate needs the stronger selected-prime statement:

```text
the named CM Moore residual products B and T are p-units at p=10^24+7.
```

So the CS theorem should be used to choose the determinant and formalize the
finite implication chain; class-field arithmetic must still prove the p-unit
nonvanishing.

ML is useful for theorem discovery, not certification.  The most productive
ML/statistical tasks are:

```text
rank stable residual norm products across small CM rows;
cluster failure patterns by discriminant/conductor/orbit data;
search for coordinate changes that make residual products low-height;
symbolically regress stable B/T products against class-field norms or
resultants.
```

Any ML output has to graduate to an exact finite-field identity, norm formula,
or selected-prime p-unit theorem before it helps the DANGER3 certificate.

The next theorem candidate imported from CS is therefore:

```text
For the six explicit mixed class-field right packets S_j, the paired
four-packet subspace-polynomial residuals have q-degrees 140 and the paired
tail residuals have quotient q-degree 16.  Equivalently, all 3 B and 6 T
Moore residual norm products in the manifest are p-units.
```

That is not an off-the-shelf coding theorem, but the coding-theory import
gives the cleanest possible finite statement for the arithmetic theorem.

## 2026-06-05 Update: Representative-Kernel Boundary

The unit-equivariant certificate surface has compressed further to one
representative leading p-unit:

```text
L_rep = B_rep*T_rep,
K = ker(a_2,a_3,a_5,a_6),
pi_16(a_1)|_K injective.
```

The relevant boundary note is:

```text
p24/representative_cs_theory_candidate_boundary.md
p24/representative_kernel_cs_boundary_audit.py
```

The audit records a deterministic p24 correction:

```text
dim_Fp K = 16 is not a subfield dimension of F_{p^156};
subfield dimensions are 1,2,3,4,6,12,13,26,39,52,78,156.
```

So a proof cannot literally identify `K` with `F_{p^16}` or a scalar multiple
of such a subfield.  A Frobenius-module theorem is not dimensionally ruled
out:

```text
x^156 - 1 over F_p has factor-degree histogram {1:2, 2:5, 4:36},
```

and there are many formal 16-dimensional Frobenius-invariant component sums.
Such a proof would need an exact component/norm identity, not just a field
tower slogan.

Small and p24-shaped random controls confirm that:

```text
prefix full rank does not imply tail injectivity;
random prefix kernels are not shift-stable;
tail injectivity is the genuine representative p-unit condition.
```

This keeps the CS import focused on rank-metric/subspace-polynomial language
and PIT-style norm packaging.  ML remains useful only for discovering stable,
equivariant residual norm identities that can be converted into exact
class-field p-unit statements.

## 2026-06-05 Update: Unit-Orbit Transversality Boundary

The right-unit action is a CS-style symmetry/compression tool, not a
nonvanishing theorem.  I added:

```text
p24/unit_orbit_transversality_toy.py
p24/unit_orbit_transversality_boundary.md
```

The toy model uses six blocks

```text
A_j = A D^j
```

and tests the p24 representative shape:

```text
four full blocks + one tail slice.
```

The identity action is cyclic-symmetric but makes all blocks identical, so it
fails transversality in every trial.  A permutation action often succeeds, but
not formally.  This proves a useful boundary for imported CS theory:

```text
equivariance can propagate one p-unit certificate around the six deletion
rows, but it cannot replace the arithmetic proof that L_rep != 0.
```

Thus group-action, orbit-design, and expander intuitions remain useful only
after they identify an exact determinant/norm/residual product.  The final
proof still has to be a selected-prime p-unit theorem or an equivalent
finite-field identity.

## 2026-06-05 Update: MSRD / LRS Candidate

The sharpest new CS import is a sum-rank distance formulation:

```text
if Phi(L) subset F_p^210 is block-equivalent to an
[210,156] linearized Reed-Solomon / MSRD code,
then d = 210 - 156 + 1 = 55.
```

The p24 bad support has size:

```text
35 + 19 = 54,
```

so MSRD distance would rule it out exactly.  This is recorded in:

```text
p24/msrd_lrs_import_boundary.md
p24/msrd_vs_mds_boundary.md
p24/msrd_metric_boundary.md
p24/lang_arc_strength_audit.py
p24/lang_arc_strength_boundary.md
```

Small actual-CM rows satisfy the stronger ordinary Moore-arc proxy, but random
baselines do too.  The metric caveat is important: `35+19=54` is an ordinary
scalar support count unless the arithmetic construction supplies an explicit
sum-rank expansion of total rank length 210.  Therefore the LRS/MSRD route is
viable only if the class-field construction proves a genuine metric-preserving
block equivalence or a support-specific skew-polynomial determinant p-unit
identity.

## 2026-06-05 Update: Block-Subspace Design Boundary

The coding-theory import has a useful intermediate formulation:

```text
six right Frobenius blocks W_j subset F_p(mu_157)
form the required support-specific array-code profile.
```

For p24 the representative theorem is exactly:

```text
dim span(W_2,W_3,W_5,W_6) = 4*35 = 140,
and the first 16 Lang coordinates from W_1 inject into the quotient.
```

This is recorded in:

```text
p24/lang_block_subspace_design_audit.py
p24/lang_block_subspace_design_boundary.md
```

I also added an explicit Lean numerical gate to:

```text
p24/lean/MixedSubspacePolynomialGate.lean
```

checking:

```text
prefixRank = 4*35 and tailAug = 16
=> full span in dimension 156.
```

Pinned actual-CM rows `D=-13319` and `D=-5444` satisfy the block-subset rank
profile, but random controls with the same block lengths succeed at the same
rate.  A shape-only `D=-26519` full-block-plus-tail family again disappears
when the actual CM-cycle/packet construction is required (`rows=0` for
`q=293,373`).

Thus the block-subspace import is the best finite theorem language after the
MSRD metric correction, but it still requires a selected arithmetic p-unit or
intersection theorem.

## 2026-06-06 Update: Strong-Rayleigh Boundary

The CRT-axis support matroid has the right Hodge/Lorentzian vocabulary, but
not the stronger real-stability property needed for a negative-dependence
certificate.  I added:

```text
p24/axis_crt_strong_rayleigh_obstruction_toy.py
p24/axis_crt_strong_rayleigh_obstruction_boundary.md
```

The toy constructs the abstract multipartite incidence basis polynomial.  The
smallest all-ones tripartite check is positive:

```text
parts=(2,2,2), bases=58, min_rayleigh_delta=87.
```

But the next tripartite analogue has an exact positive integer weighted
Rayleigh violation:

```text
parts=(2,2,3), bases=504,
rayleigh_delta
  = -7988395388171953562263529025459059314667521815134984779980.
```

So strong-Rayleigh/real-stable positivity cannot prove the p24 CRT-axis
Plucker noncancellation even at the support level.  This leaves Lorentzian
matroid language as useful structure, not as a selected-prime certificate.

The surviving CS/probability imports are exactly:

```text
p-unit PIT for the named determinant;
explicit p-unit block equivalence to MSRD/LRS;
phase-aware local-intersection/product formula;
ML/data mining only when it proposes an exact identity with holdouts.
```

## 2026-06-06 Update: RS-Tail Syndrome Moore Surface

A sidecar synthesis of the current RS-tail adjoint theorem reached the same
boundary: the productive import from coding theory is Moore/Gabidulin
language for a named determinant, not an off-the-shelf MSRD shortcut.

The fixed-orbit target is:

```text
syndrome : L -> F_p^28 + K^28 + F_p^16 is surjective.
```

After choosing an `F_p`-basis of `K`, this is equivalent to a single Moore
determinant for the 156 explicit column elements:

```text
Delta_156(C_RS) != 0.
```

The sharper split is:

```text
Delta_140(C_prefix) != 0,
Delta_16(P_prefix(W_0),...,P_prefix(W_15)) != 0.
```

An LRS/MSRD theorem would still be valuable, but only after constructing an
explicit p-unit block equivalence from the actual CM columns to a genuine
sum-rank evaluation code.  Without that equivalence, probability/ML remains
an identity-mining tool: it can suggest pivot orders, low-height residual
products, or norm formulas, but it cannot certify the selected p24 p-unit.

The finite split controls are now recorded in:

```text
p24/trace_gcd_rs_tail_syndrome_moore_schur_toy.py
p24/trace_gcd_rs_tail_semilinear_core_theorem.md
```

## 2026-06-06 Update: Visible LRS Shortcut Rejected

The selected square object has block dimensions `35,35,35,35,16`, and the
cheap necessary gate is only block directness:

```text
rank(prefix)=140,
rank(prefix + tail16)-rank(prefix)=16.
```

That gate is useful for killing bad ansatzes, but a pass is only
compatibility.  Once the selected `140+16` columns form a direct sum, arbitrary
p-unit row changes plus block changes leave little moduli for an off-the-shelf
MSRD conclusion.

A still cheaper shortcut would be that the natural coordinates already look
like a rational-normal/GRS model.  The new toy checks adjacent Hankel ranks of
the coordinate columns: synthetic rational-normal columns pass, while
RS-tail-shaped random columns with the same finite bookkeeping fail.  This
demotes the visible-coordinate LRS route.  The surviving coding-theory route
must either construct an explicit class-field p-unit block equivalence, or use
the unused `54` columns in the full `210`-column fixed-source object to expose
a genuine Plucker/cross-ratio invariant.

The next full-object visible-GRS invariant is the Plucker chart.  If the
selected `156` columns are a basis, the omitted `54` columns give a
`156 x 54` matrix of Plucker ratios.  For a visible scalar GRS/MDS code this
chart is scaled Cauchy, so its entrywise inverse has rank at most `2`; the toy
detects this for rational-normal columns and row/column-scaled variants, while
random full-source charts fail.  This is a real unused-column modulus, but it
still only rules out visible scalar GRS.  Hidden LRS/MSRD would need a
block/skew version of this chart or the actual class-field block equivalence.
The sharper block/skew Cauchy candidate is the Sylvester displacement identity
`A C - C B = R S`, where `A` and `B` must be transported CM/Lang operators and
`R S` has small rank.  Scalar Cauchy is the rank-one special case; the
entrywise-inverse rank test is only its scalar shadow.
The displacement handoff reduces the chart theorem to a full-column operator
boundary: for `X=[S O]` and `C=S^{-1}O`, equations
`T S = S A + E_s`, `T O = O B + E_o` imply
`A C - C B = S^{-1}(E_o - E_s C)`.  This is useful only when `A,B,T` come from
the arithmetic construction; post-fit operators can make random charts pass.
For the RS-tail split there is now a concrete operator candidate imported from
the coding-theory view: the common cyclic/Lang shift on the six right blocks.
The wholly selected blocks and the wholly omitted block are shift-stable; only
the split tail block crosses the selected/omitted boundary, giving exactly two
rank-one cut maps in the toy model.
The actual-CM boundary audit also checks the current smaller rows and finds no
nontrivial selected-basis calibration row for this full chart, so those rows do
not yet validate or falsify the Cauchy/Plucker theorem candidate.

Recorded in:

```text
p24/trace_gcd_rs_tail_block_support_profile_toy.py
p24/trace_gcd_rs_tail_full_plucker_chart_cauchy_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_displacement_toy.py
p24/trace_gcd_rs_tail_block_skew_cauchy_theorem_candidate.md
p24/trace_gcd_plucker_displacement_handoff_toy.py
p24/lean/TraceGcdPluckerDisplacementHandoffGate.lean
p24/trace_gcd_rs_tail_shift_displacement_boundary_toy.py
p24/trace_gcd_rs_tail_cyclic_operator_boundary_toy.py
p24/trace_gcd_actual_cm_full_plucker_chart_boundary.py
p24/trace_gcd_rs_tail_visible_lrs_signature_toy.py
p24/lean/TraceGcdFullCoinvariantTailGate.lean
```
