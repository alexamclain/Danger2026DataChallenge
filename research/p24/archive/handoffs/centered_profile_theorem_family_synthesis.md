# Centered Profile Theorem-Family Synthesis

Date: 2026-06-06

This note ranks the remaining theorem families for the centered-profile
certificate after the cyclic-resultant, plateau, affine-arc, and
transversality audits.

## Live Statement

The compact target is:

```text
Pi_C,right = prod_{t mod 211} Delta_C(t) != 0 mod p,
p = 10^24 + 7.
```

Equivalently, the seven Frobenius-orbit products of the cyclic
right-translation determinant sequence are p-units.  Equivalently, the p24
centered marginal point columns form a cyclic consecutive `157`-arc in
`A^156(F_p)`.

The finite implication is checked in:

```text
p24/lean/CenteredArcProductGate.lean
```

## 1. Phase-Aware Class-Field / Borcherds / Fitting P-Unit

Theorem shape:

```text
construct a p-integral class-field section Psi_C whose CM value is
Pi_C,right up to p-units, then prove v_p(Psi_C)=0 at the selected p24 prime.
```

What still needs proving:

```text
the centered Schubert/affine-arc divisor is the divisor of a phase-aware
class-field/Borcherds/Fitting section, and its selected local intersection
with the p24 CM point is zero.
```

Why it is viable:

```text
the origin-product theorem already packages the selected determinant into a
class-field-stable product, and the seven-orbit form is small enough to be a
real certificate surface.
```

Relevant files:

```text
p24/centered_marginal_phase_borcherds_target.md
p24/centered_marginal_chow_integral_model.md
p24/centered_marginal_crossed_product_fitting_target.md
p24/centered_marginal_difference_code_boundary.md
p24/centered_marginal_difference_mds_boundary.md
p24/centered_marginal_difference_geometry_boundary.md
p24/centered_marginal_plucker_kummer_descent_boundary.md
p24/centered_marginal_padic_filtration_boundary.md
p24/centered_marginal_full_origin_borcherds_gate.md
p24/centered_marginal_origin_norm_power_theorem.md
p24/centered_marginal_phase_unit_span_boundary.md
p24/centered_marginal_global_product_mining_boundary.md
p24/centered_marginal_holdout_rows_boundary.md
p24/centered_marginal_origin_product_theorem.md
p24/centered_marginal_cyclic_resultant_theorem.md
p24/trace_frame_borcherds_punit_boundary.md
p24/hermitian_padic_principal_boundary.md
```

This is currently the most proof-bearing path.
The elementary right-cyclotomic unit dictionary has now been tested and
misses the centered determinant sequence in the first actual-CM rows, so this
path needs a genuine Schubert/Fitting construction rather than a small
right-binomial product.
The scalar global-product miner found one low-weight coincidence and two
misses; without a divisor comparison, scalar-only matches are too weak to use
as a proof surface.
The most plausible positive instantiation is now the full-origin variant:
known CM product technology is more likely to see a full-origin norm, and the
origin covariance gives
`prod_all_origins = p-unit * Pi_C,right^975736474`.
The full-origin phase-sensitivity gate sharpens what such a theorem must
construct: unordered recovery fibers are not enough.  In the pinned
`D=-13319, q=13463, m=28, n=5` row, cyclic origin shifts preserve the product
but shuffling child order inside every recovery fiber changes the product in
`8/8` controls.
The oriented-edge shape boundary also rejects the simplest local norm model:
the same centered determinant sequence is not a bidegree-`<=4` polynomial or
rational function of one oriented edge `(j_i,j_{i+1})`.
The short-path boundary rejects the next local shortcut too: no subgeneric
low total-degree polynomial/rational formula appears in two-edge or three-edge
adjacent path coordinates on the same pinned row.
The centered orbit-Fitting block-cycle audit checks the positive finite
plumbing: actual Schubert window matrices assemble into direct-sum and
signed block-cycle orbit determinants with exact zero detection.  This keeps
the crossed-product Fitting object as the sharp theorem target, while
removing determinant assembly as a possible source of uncertainty.
The sharpest named object is the crossed-product Fitting determinant of the
orbit Schubert quotient maps `W_C -> H/B_t`; proving this determinant is a
p-unit is exactly the local-unit theorem.
The cyclic-difference reformulation turns plateaus into named coordinate
erasure supports, but the tested actual-CM difference rowspaces are still not
cyclic-shift stable, so BCH/cyclic-code theorems do not apply for free.
The full scalar-MDS strengthening also holds in small rows, but random
controls hold at the same rate; it is a broad possible theorem shape, not a
recognized arithmetic identity.
The visible GRS/rational-normal-curve test also matches zero-sum random
controls, so no low-degree projective model has been found for the difference
columns.
The determinant-level Kummer descent test also points to orbit norms rather
than individual powered determinants: no nontrivial small-CM right orbit
descended except at the trivial `q-1` exponent.
The structured p-adic-filtration audit also does not expose a natural
triangularization: power, Frobenius normal, and middle-Frobenius bases keep
full Pluecker support in the hard small rows, including an asymmetric
degree-`12` row.  Hermitian orthogonal bases do reduce the dense two-sided
Cauchy-Binet expansion to a diagonal Pluecker dot product, but all matched
Pluecker coordinates remain nonzero, so the same selected-prime p-unit theorem
is still required.  The finite handoff for a hypothetical local initial-layer
dominance theorem is isolated in `CenteredHermitianPluckerGate.lean`.
The new `D=-26759` holdout reinforces the same split: leading-minor and
origin/full-origin identities pass, while the asymmetric phase-varying row
still has only full-rank/random unit-dictionary recognition.

## 2. Rank-Metric / Moore / LRS/MSRD Equivalence

Theorem shape:

```text
prove the actual centered right-profile coordinate family is p-unit
equivalent to a scalar MDS/full-arc object, or to a genuine sum-rank
LRS/MSRD code whose distance excludes 54-supported bad words.
```

The p24 numerology is exact:

```text
bad plateau complement support = 211 - 157 = 54,
Singleton threshold = 210 - 156 + 1 = 55.
```

What still needs proving:

```text
an explicit p-unit coordinate/block equivalence to the rank-metric object,
or direct p-unitness of the named cyclic-window Moore/subspace-polynomial
determinants.
```

Relevant files:

```text
p24/msrd_lrs_import_boundary.md
p24/msrd_metric_boundary.md
p24/centered_plateau_lang_support_boundary.md
p24/lang_block_subspace_design_boundary.md
p24/centered_marginal_full_arc_boundary.md
```

This is the best CS import, but it still requires a CM arithmetic
identification.  The centered plateau support audit now shows why:
after right Fourier/Lang normalization, the bad plateau subspaces touch every
transformed coordinate block in small analogues.  The p24-shape factor audit
is sharper: for `right=211,left=157` and `ord_211(q)=35`, the `54`-dimensional
bad plateau subspace projects surjectively to each of the six degree-35 right
orbit blocks.  Thus support-distance alone does not exclude them; one still
needs Schubert-subspace avoidance.

## 3. Weighted Chebotarev / Fourier-Superregular Minor

Theorem shape:

```text
use the exterior right-character expansion of Delta_C(t) and prove the
actual CM-weighted Fourier minor is a p-unit, or find p-unit changes of
basis reducing it to an ordinary Chebotarev/GRS minor.
```

What still needs proving:

```text
the singular-moduli spectral twist must either become row/column scaling
after a CM-adapted normalization, or satisfy a new weighted Chebotarev
noncancellation theorem for this exact twist.
```

Relevant files:

```text
p24/centered_marginal_exterior_dft_boundary.md
p24/centered_marginal_cyclic_code_boundary.md
p24/centered_marginal_projective_geometry_boundary.md
p24/trace_frame_toeplitz_schur_boundary.md
```

This remains viable only if a new normalization is found; the natural
coordinates have full support and random-like projective geometry.

## 4. Pointwise Anti-Concentration / Zero-Count

Theorem shape:

```text
for every nonzero dual lambda, prove the scalar word lambda(P_b) has no
157-term cyclic plateau.
```

What still needs proving:

```text
a selected-prime deterministic zero-count bound strong enough to give zero
bad plateaus, not merely an average or random-subspace probability.
```

Relevant files:

```text
p24/centered_marginal_plateau_uncertainty_boundary.md
p24/centered_marginal_transversality_boundary.md
p24/probability_lift_agent_followup.md
```

This is useful language, but plain uncertainty and random-rank heuristics are
not proof mechanisms here.

## Current Ranking

The highest-value next proof work is:

```text
1. phase-aware p-unit/Fitting divisor for Pi_C,right;
2. explicit p-unit LRS/MSRD or Moore-window equivalence;
3. CM normalization of the weighted Fourier/Chebotarev minor.
```

The transversality baseline explains why the theorem should be true, but the
certificate still needs one exact arithmetic nonvanishing theorem.
