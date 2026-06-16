# CS Rank-Condenser Theorem Status

This note sharpens the CS/ML import after the marginal-rank reduction.

## Live Object

The p24 finite theorem is a deterministic rank-condenser statement.  For

```text
A_k(r)=Top_k(J_r(theta)) in C^k,
M_{c,a}^{(k)}=sum_{r == a mod c} A_k(r),
Delta_c^(k)=span_E{M_{c,a}^{(k)}-M_{c,0}^{(k)}},
```

the certificate asks for:

```text
dim_E( E*S_1 + Delta_2^(1) + Delta_157^(1) ) = 158,
dim_E( Delta_211^(2) ) = 210,
dim_E( E*S_3 + Delta_2^(3) + Delta_157^(3) + Delta_211^(3) ) = 368.
```

Equivalently, the CM marginal generator sends every nonzero CRT-axis
codeword away from the canonical trace-annihilator subspace.  In CS terms:

```text
structured source code      = CRT-axis weights
linear condenser            = w -> Top_k(sum_r w(r)J_r(theta))
bad subspace                = Top_k-annihilator
certificate                 = Plucker p-unit Omega_1, Omega_211, Omega_3
```

## Imports That Still Help

1. Rank condenser / subspace-evasive language.

This is the best conceptual import.  It gives the exact theorem shape:

```text
CM periods form a rank condenser for the CRT-axis source code.
```

It would beat sqrt scaling because the verifier would check one bounded
rank/p-unit certificate of formal degree roughly `m+n`, not enumerate
sqrt-`p` Montgomery prefixes or the full CM class set.

2. Algebraic complexity / PIT.

The three exterior products

```text
Omega_1, Omega_211, Omega_3
```

are determinant polynomials in CM period data.  PIT language says to prove
the determinant is not the zero polynomial; the selected-prime certificate
needs the stronger arithmetic lift:

```text
the chosen Plucker content is a p-unit at p=10^24+7.
```

This is useful because it points to norm/resultant packaging, not random
probability.

3. Rank-metric / Moore normality.

The stronger parent theorem is full relative `K`-normality:

```text
F_0,...,F_{m-1} independent in F_p[X]/(f_a).
```

Basis-free form:

```text
det(beta_r^(p^s))_{0 <= r,s < m} != 0.
```

This is a Moore determinant p-unit.  It is larger than the axis theorem, but
it may be more natural for a class-field normal-basis proof.

4. ML/statistical search as theorem discovery only.

ML can rank candidate minors, detect repeated low-height formulas, or cluster
near-failures in small CM rows.  It does not certify p24 unless the output
becomes an exact identity or a p-unit theorem.

## Structured-Code Shortcut Audit

I added:

```text
p24/tensor_factor_marginal_cs_structure_audit.py
```

It tests the actual CM marginal matrix against random tensor-factor controls
for:

```text
full rank;
maximal minors / small MDS-superregular support;
Toeplitz displacement rank;
Hankel displacement rank;
cyclic Toeplitz/Hankel displacement rank.
```

Pinned full-axis toy analogue:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/tensor_factor_marginal_cs_structure_audit.py \
  --only-D -10919 --only-m 12 --max-h 200 --max-abs-D 12000 \
  --max-n 80 --q-stop 200000 --max-extension-degree 8 \
  --max-factor-degree 20 --max-tensor-factor-degree 12 \
  --min-tensor-factor-count 2 --subdegree 3 --windows 2 \
  --target full --random-trials 80 --max-minors 20000
```

reported:

```text
cm_matrix:
  rows=6 cols=6 rank=6/6
  displacement=cyclic_hankel:6,cyclic_toeplitz:6,hankel:6,toeplitz:6
  maximal_minors tested=1 zero=0

random_controls:
  rank_hist={6:80}
  displacement_hists all {6:80}
  maximal_minor_zero_hist={0:80}
```

Pinned `constant + 4` one-window analogue:

```text
rows=4 cols=3 rank=3/3
displacement=cyclic_hankel:3,cyclic_toeplitz:3,hankel:3,toeplitz:3
maximal row minors tested=4 zero=0
random controls matched exactly
```

Pinned trace-zero component analogue:

```text
rows=2 cols=3 rank=2/2
displacement=cyclic_hankel:2,cyclic_toeplitz:2,hankel:2,toeplitz:2
maximal column minors tested=3 zero=0
random controls matched exactly
```

## Consequence

The audit rules out the most direct off-the-shelf structured-code shortcut in
the natural trace-coordinate order:

```text
not visibly Toeplitz/Hankel/cyclic low-displacement;
small superregular/minor success is random-generic at these field sizes.
```

So the useful CS import is not "identify this as a known GRS/Cauchy/Toeplitz
matrix and quote its determinant."  The remaining viable CS-shaped theorem is
arithmetic:

```text
the selected CM marginal generator is a rank condenser,
because its Plucker determinant/norm is a p-unit.
```

That remains compatible with the class-field tower route: find a finite-field
identity or embedded class-field norm formula for `Omega_1`, `Omega_211`, and
`Omega_3`, then prove the selected p24 prime does not divide it.

## Cheap Next Audits

The next useful data-driven tasks are not more random-rank checks.  They are:

```text
1. minor stability search:
   find a single coordinate minor that stays nonzero across many CM rows and
   is unusually sparse or low-height as an algebraic expression;

2. near-failure clustering:
   search dimension-eligible rows for unusually small pivot prefixes or
   repeated zero minor patterns, because those may reveal the hidden
   class-field obstruction;

3. p-unit norm packaging:
   compute small-row products of stable minors over origin/Frobenius orbits
   and test whether they match norms of simpler CM resolvents.
```

Any of these can productively use ML or symbolic regression, but only as a
way to propose an exact identity.

## Exterior-DFT Import Boundary

The centered right-translation determinant now has an exact exterior
character expansion:

```text
F(t) =
  sum_{S subset {1,...,r-1}, |S|=d}
    det(Q_s) det(zeta^(s*i)-1) zeta^(t*sum S).
```

This is the right algebraic-complexity/PIT language for the seven orbit
products.  It also tests the most direct component-character-module hope.
The audit in:

```text
p24/centered_marginal_exterior_dft_audit.py
p24/centered_marginal_exterior_dft_boundary.md
```

found full term support and full frequency support in pinned actual-CM rows:

```text
D=-6719:  subset_count=15, nonzero_term_count=15, support=7/7.
D=-13319: subset_count=20, nonzero_term_count=20, support=7/7.
D=-10919: subset_count=66, nonzero_term_count=66, support=13/13.
```

For p24 the raw exterior expansion has `binom(210,156) ~= 10^50.79` terms.
So this import sharpens the theorem, but it is not a standalone asymptotic
speedup unless a CM p-unit identity collapses the exterior polynomial or its
seven orbit products.

## New Useful Import: Frobenius-Skew Moore Blocks

The Hermitian mixed-character route now gives a concrete coding-theory
surface:

```text
p24/hermitian_mixed_frobenius_orbit_audit.py
p24/hermitian_mixed_moore_circulant_theorem.md
```

For a mixed double-DFT block

```text
H_{c,d}(u,v)=sum_{r,s} zeta_c^(u*r) zeta_d^(v*s) K(r,s),
```

base-field valuedness of `K` forces

```text
H(q^a*u0, q^b*v0)=H(u0, q^(b-a)*v0)^(q^a).
```

For p24 this turns the large `157 x 211` Schur block into one row Frobenius
orbit of length `156` against six column orbits of length `35`.  The raw
`156 x 210` determinant is therefore equivalent to a six-sequence
skew-linearized annihilator condition:

```text
sum_{a=0}^{155} x_a * b_j(b-a mod 35)^(p^a) = 0
for all j and b  =>  x=0.
```

This is the first CS import that materially changes the theorem statement.  It
suggests an interleaved Gabidulin/skew-PIT p-unit theorem rather than a generic
rank-condenser slogan.

Pinned `(4,3)` CM rows and a bounded small-CM scan verified the formal
Frobenius-orbit model:

```text
rows=3
orbit_blocks=27
frobenius_identity_failures=0
nonfull_possible_rank_blocks=0
```

The remaining proof is still arithmetic: prove that the actual CM seed cycles
avoid the skew-annihilator incidence divisor at the selected p24 prime.

## Centered Difference-Minor Condenser

The centered-profile route has now produced the cleanest concrete
rank-condenser scalar:

```text
p24/centered_marginal_difference_minor_theorem.md
p24/centered_marginal_leading_minor_audit.py
```

For the doubly-centered `156 x 210` mixed marginal `C`, define:

```text
Delta_C_leading =
  det(C(r,s))_{1 <= r <= 156, 1 <= s <= 156}.
```

This is the direct cyclic-code projection theorem:

```text
no nonzero dual trace word vanishes on the first 156 right-difference
positions.
```

Bounded actual-CM audits on `D=-13319`, `D=-6719`, and `D=-10919` found:

```text
full_rank_but_leading_zero_pairs=0.
```

This is exactly the productive CS import: not a generic MDS theorem, but a
specific consecutive-minor p-unit target for the selected class-field
marginal.  The remaining missing theorem is an arithmetic p-unit proof for
`Delta_C_leading` at `p=10^24+7`.

The same scalar has an exterior trace-form expression:

```text
Delta_C_leading =
  <wedge_left_differences, wedge_right_differences>_{wedge B}.
```

See:

```text
p24/centered_marginal_cauchy_binet_boundary.md
p24/centered_marginal_cauchy_binet_audit.py
```

Small actual-CM rows show that the Cauchy-Binet expansion is dense in the
natural packet power basis.  For example, the `D=-10919` degree-12 row has
`6160` nonzero terms and `5940` off-diagonal terms for a `3 x 3` leading
window.  Thus this route does not reduce to a product of separate left/right
coordinate minors without a new basis or a p-adic dominance theorem.

## Lang-Normality Compression

The skew-cyclic/Gabidulin condition can be compressed one step further:

```text
p24/hermitian_mixed_lang_normality_audit.py
p24/hermitian_mixed_lang_normality_theorem.md
```

For a right orbit of length `R`, the semilinear cyclic shift

```text
T(s)_b = sigma(s_{b-1})
```

has fixed vectors `u_alpha(b)=sigma^b(alpha)` with
`alpha in F_{q^R}`.  Changing coordinates by this Moore matrix turns each
mixed row orbit into an ordinary Moore matrix.  Therefore:

```text
row-orbit rank = min(left orbit length,
                    F_q-rank of transformed seed coordinates).
```

For p24 this says:

```text
210 transformed coordinates;
need F_p-rank at least 156.
```

The bounded audit verified the criterion on small CM rows:

```text
rows=3
left_orbit_tests=18
criterion_mismatches=0
full_left_orbit_rank_tests=18
```

The coprime-degree refinement is recorded in:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
p24/hermitian_mixed_left_subfield_identity_toy.py
p24/hermitian_mixed_trace_dual_formula_toy.py
p24/hermitian_mixed_dual_trace_injectivity_toy.py
p24/hermitian_mixed_left_subfield_span_theorem.md
```

For p24, `gcd(156,35)=1`, so the 210 transformed coordinates land in
`F_p(mu_157)=F_{p^156}`.  The exact target is:

```text
dim_Fp span{210 transformed coordinates} = 156.
```

The finite-field toy with `q=2`, `left=7`, `right=5` verified the coprime
left-subfield landing with zero failures:

```text
left_orbit_tests=40
left_subfield_failures=0
full_left_span_tests=29
```

This is now the cleanest CS import: a rank-metric tuple-span theorem for
explicit class-field periods.  Generic random-matrix heuristics are no longer
the statement; the statement is a concrete Moore-minor p-unit for 210
Lang-trivialized period coordinates.  Individual normality of one coordinate
is only diagnostic and does not imply full row rank.

The trace-dual toy verified the intrinsic coordinate formula:

```text
E = F_p(mu_157,mu_211), L = F_p(mu_157),
w_{j,i}=Tr_{E/L}(delta_i*S_j),
S_j=H_{157,211}(1,v_j).
```

Toy output:

```text
formula_tests=40
trace_dual_mismatches=0
left_subfield_failures=0
```

So the useful CS theorem is no longer about an arbitrary rank condenser; it is
about whether the relative-trace coordinate set of six explicit mixed
class-field periods spans the whole left character field.

The dual trace toy checked the equivalent injectivity statement:

```text
L -> R^6,
lambda |-> (Tr_{E/R}(lambda*S_j))_j.
```

Toy output:

```text
dual_tests=40
rank_mismatches=0
full_span_tests=29
dual_injective_tests=29
```

Six-right-orbit miniature:

```text
q=2, left=7, right=31
ord_7(2)=3, ord_31(2)=5, right_orbits=6
dual_tests=80
rank_mismatches=0
full_span_tests=80
dual_injective_tests=80
```

So the rank-condenser language has now collapsed to a concrete separation
theorem: six relative traces to the right character field separate all
nonzero left characters.

The same theorem has a trace-intersection form:

```text
W = span_R{S_1,...,S_6} subset E,
L ∩ W^perp = {0}
```

for the `E/R` trace pairing; see:

```text
p24/hermitian_mixed_trace_intersection_theorem.md
p24/lean/MixedTraceIntersectionGate.lean
```

This is an important boundary for importing CS intuition.  The six `S_j` do
not span `E` over `R`; they cut out an `R`-codimension-at-most-6 subspace, and
the theorem is that this large orthogonal complement misses the fixed
`F_p`-subspace `L`.

The periods have the resolvent-pairing form:

```text
S_j = <A_1,B_{v_j}>.
```

This is recorded in:

```text
p24/hermitian_mixed_resolvent_pairing_formula.md
p24/hermitian_mixed_resolvent_pairing_audit.py
```

The CS/rank-metric import is therefore now attached to explicit class-field
periods, not an abstract random linear map.

## Subspace-Polynomial Certificate Surface

The Lang/trace-dual target now has a canonical rank-metric packaging:

```text
C = { Tr_{E/L}(delta_i*S_j) : 1 <= i <= 35, 1 <= j <= 6 }
    subset L = F_p(mu_157).
```

Let `A_C(X)` be the monic `p`-linearized subspace polynomial of
`span_Fp(C)`.  Standard linearized-polynomial theory gives:

```text
pdeg A_C = dim_Fp span(C).
```

Therefore the p24 mixed theorem is equivalent to:

```text
A_C(X) = X^(p^156) - X.
```

or equivalently no nonzero `p`-linearized polynomial of `p`-degree `<156`
annihilates all `210` trace-dual mixed coordinates.

This is currently the most compact CS import:

```text
rank-metric normality / subspace polynomial / Moore determinant p-unit.
```

Terminology caveat: the p24 object is an interleaved rank-support/full
Moore-rank condition, not a standard length-`210` Gabidulin MRD code.

Added:

```text
p24/hermitian_mixed_subspace_polynomial_certificate.md
p24/hermitian_mixed_subspace_polynomial_toy.py
p24/lean/MixedSubspacePolynomialGate.lean
```

The six-right-orbit miniature

```text
q=2, left=7, right=31, trials=20
```

reported:

```text
subspace_tests=40
degree_rank_mismatches=0
vanish_failures=0
full_span_tests=40
full_field_annihilator_tests=40
forced_low_rank_degree_mismatches=0
```

So the finite algebraic certificate shape is verified on the toy model and
low-rank controls.  The remaining p24 work is proving the class-field identity
`A_C(X)=X^(p^156)-X`, not just sampling rank.

The same subspace-polynomial diagnostic is now integrated into the actual-CM
left-subfield audit.  The bounded small-CM window:

```text
rows=3
tests=18
annihilator_degree_mismatches=0
annihilator_vanish_failures=0
zero_residual_norms=0
missing_pivot_norm_products=0
full_field_annihilator_tests=18
max_pivot_count=2
```

again verifies conventions only; the tested left orbit length is `2`, not
`156`.

The residual profile gives a concrete ML/statistics search target: stable
pivot prefixes or stable residual norm products would identify a specific
Moore-minor p-unit candidate.

## Trace-Frame Sum-Rank Erasure Import

The newest trace-frame formulation has a cleaner sum-rank code surface:

```text
p24/trace_frame_flag_transversality_theorem.md
p24/trace_frame_sum_rank_erasure_theorem.md
p24/tensor_factor_relative_block_erasure_audit.py
```

After multiplying by `g'(theta)` and expanding over the degree-31 extension
`B/C`, the p24 axis image is an `E`-linear code:

```text
W_axis(B) subset C^31,
dim_E W_axis(B)=368,
dim_E C=179.
```

The current certificate only needs the top-three block projection

```text
W_axis(B) -> C^3
```

to be injective.  The stronger CS import says that every `3`-block projection
is injective, equivalently that no nonzero word is supported on `28` relative
coefficient blocks.  In sum-rank terms it would follow from:

```text
d_sumrank(W_axis) > 28*179 = 5012.
```

The Singleton bound is:

```text
d <= 31*179 - 368 + 1 = 5182.
```

So an MSRD/LRS identification of this relative coefficient code would prove
the trace-frame theorem with room to spare.

The pinned `D=-10919` tensor audit tested all dimension-sufficient relative
block subsets available in the small analogue:

```text
rows=5
targets=44
subset_tests=102
subset_failures=0
top_failures=0.
```

The static p24 accounting is:

```text
p24/trace_frame_sum_rank_erasure_accounting.py
p24/trace_frame_sum_rank_erasure_accounting.md

three_block_subset_count=4495
singleton_distance=5182
needed_distance=5013
distance_slack=169
```

A random baseline for the same small shapes also had zero failures in `200`
trials per shape:

```text
p24/tensor_factor_relative_block_erasure_random_baseline.py
```

So this is a useful import because it changes the proof question from one
coordinate accident to an erasure-distance theorem.  It is not proof-like
evidence by itself: the p24 work is to identify a real class-field/LRS/MSRD
equivalence or prove the selected erasure Plucker coordinate is a p-unit.

I also added a simple LRS-signature audit for the relative coefficient
generator matrix:

```text
p24/tensor_factor_relative_block_structure_audit.py
p24/trace_frame_lrs_signature_boundary.md
```

On the pinned `D=-10919, m=12` axis analogue, the natural matrix matched
random controls exactly for block ranks, pair ranks, and
Toeplitz/Hankel/cyclic displacement ranks.  The displacement ranks were
maximal in both intermediate-field choices:

```text
subdegree=2: all displacement ranks 6
subdegree=3: all displacement ranks 6
```

So there is no visible off-the-shelf Toeplitz/Hankel/cyclic/LRS structure in
the natural relative coefficient basis.  A successful MSRD route would need a
non-obvious class-field block equivalence.  The selected top-three p-unit
remains the smaller finite certificate surface.
