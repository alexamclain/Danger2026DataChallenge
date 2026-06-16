# Hermitian Mixed Centered-Right Profile Theorem

This note removes the right cyclotomic coordinate basis from the current
mixed Schur target.

## Setup

For the mixed components `left=157`, `right=211`, let

```text
M(r,s)
```

be the Hermitian double marginal of the packet kernel.  For a nonzero left
frequency `u`, define the left-character profile

```text
G_s(u) = sum_r zeta_157^(u*r) M(r,s),      s mod 211.
```

For p24 we use the single left Frobenius orbit represented by `u=1`.

The mixed right DFT periods are

```text
S_v = H_{157,211}(1,v)
    = sum_s zeta_211^(v*s) G_s(1),
    1 <= v < 211.
```

The six periods `S_j` used in the trace-intersection theorem are one
Frobenius-orbit representative for each nonzero right frequency orbit.

## Centering Identity

The nonzero right DFT omits `v=0`, so it does not recover the absolute
profile `G_s`; it recovers the centered profile:

```text
G_s^0 = G_s - (1/211) * sum_t G_t.
```

The nonzero right Fourier transform is an invertible `F_p`-linear transform
between:

```text
centered right profiles {G_s^0 : s mod 211}
```

and

```text
nonzero right-frequency periods {S_v : 1 <= v < 211}.
```

After grouping the nonzero `v` into the six Frobenius orbits and taking
trace-dual right coordinates, the `F_p`-span in `L=F_p(mu_157)` is unchanged.

Therefore the p24 trace-dual span theorem is equivalent to:

```text
dim_Fp span{G_s^0 : s mod 211} = 156.
```

Equivalently, the subspace polynomial of the centered right profile is:

```text
A_G(X) = X^(p^156) - X.
```

## Why This Helps

The previous target used:

```text
Tr_{E/L}(delta_i * S_j)
```

and depended on a chosen right trace-dual basis.  The centered-profile target
uses only:

```text
one left K-character transform of the base-field Hermitian marginal kernel.
```

This is closer to a class-field/lattice theorem:

```text
the centered right marginal of the left 157-character packet is not contained
in any proper F_p-subspace of F_p(mu_157).
```

It is also a better norm-mining surface.  A pivot residual product for the
centered profile is directly a Moore-minor p-unit candidate for the profile,
without first choosing coordinates in `F_p(mu_211)`.

## Audit

I extended:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

with:

```text
centered_right_profile_rank
centered_profile_rank_match
centered_profile_subfield_failures
centered_base_rank
centered_base_profile_rank_match
```

Pinned actual-CM rows:

```text
D=-10919:
  rows=2
  tests=12
  centered_profile_rank_mismatches=0
  centered_profile_subfield_failures=0
  centered_base_profile_rank_mismatches=0
  max_centered_right_profile_rank=2

D=-8711:
  rows=2
  tests=12
  centered_profile_rank_mismatches=0
  centered_profile_subfield_failures=0
  centered_base_profile_rank_mismatches=0
  max_centered_right_profile_rank=2
```

These rows only have left orbit length `2`, so this is an equivalence and
convention check, not evidence for p24 rank `156`.

The first larger actual-CM stress rows are recorded in:

```text
p24/centered_marginal_rank_stress_audit.md
```

They verify the base/profile rank equivalence for a full nontrivial left
orbit of length `6`, and they expose the expected packet-degree obstruction
when packet degree is smaller than left degree.

## Current Missing Theorem

For p24, set

```text
G_s = sum_{r mod 157} zeta_157^r M(r,s),     s mod 211,
G_s^0 = G_s - average_t(G_t).
```

The missing theorem can now be stated as:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157).
```

This is equivalent to:

```text
L ∩ span_R{S_j}^perp = {0}
```

and to the subspace-polynomial identity for the `210` trace-dual coordinates,
but it is the most economical current class-field-facing formulation.

## Base-Field Marginal Rank Form

Since `G_s^0` is the left character transform of the base-field centered
double marginal, the profile theorem can be stated without any cyclotomic
extension.  Let

```text
C(r,s) = M(r,s) - M(r,0) - M(0,s) + M(0,0),
1 <= r < 157, 1 <= s < 211.
```

For p24, `p` is primitive modulo `157`, so the nontrivial left characters form
one Frobenius orbit.  Thus:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157)
```

is equivalent to:

```text
rank_Fp C = 156.
```

This is the smallest purely finite-field formulation of the mixed Schur
correction:

```text
the centered 156 x 210 Hermitian marginal matrix has full row rank.
```

The cyclotomic, trace-dual, and subspace-polynomial forms are still useful for
proof search and certificate packaging, but the theorem itself is a
base-field marginal-rank p-unit.

The implicit dimension condition is:

```text
packet_degree >= 156.
```

For p24 the relevant Hermitian packet degree is `388430`, so this lower bound
is not the hard part.

## Relation To Relative Content

The selected-prime relative-content scans support nonzero packet/content
statements, but those are not enough to prove this profile theorem.  The
boundary is recorded in:

```text
p24/relative_content_to_mixed_rank_boundary.md
p24/content_vs_mixed_rank_boundary_toy.py
```

The toy gives a rank-one centered profile whose nonzero right Fourier
components are all nonzero:

```text
nonzero_right_frequency_count=5/5
profile_span_rank=1/5
```

So exact content must be strengthened to a frame/spanning theorem before it
can prove `rank_Fp C_{157,211}=156`.

This note therefore gives an alternative p-unit surface to the representative
leading-erasure determinant:

```text
centered-profile Moore determinant nonzero
  => span_Fp{G_s^0}=F_p(mu_157)
  => rank_Fp C_{157,211}=156.
```

It does not by itself prove the stronger delete-one/right-support theorem
that `L_rep` proves.  Its advantage is that it avoids right trace-dual basis
choices and may be more natural for a direct class-field or lattice argument.

The corresponding machine-readable manifest is:

```text
p24/p24_centered_profile_manifest.py
```

It names the leading candidate:

```text
M_profile_leading = det((G_s^0)^(p^i)) for 0 <= s,i < 156.
```

The finite implication is Lean-checked in:

```text
p24/lean/CenteredProfileGate.lean
```

The finite payload comparison is recorded in:

```text
p24/centered_profile_payload_frontier.md
p24/lean/CenteredProfilePayloadGate.lean
```

It checks that the explicit `156 x 210` matrix plus a `156 x 156` rank witness
uses `57096` field elements, still far below both `sqrt(p)` and the selected
chain payload.  A direct p-unit theorem for `Delta_C_leading` has only a
two-scalar finite payload.

## Trace-Gram Equivalent

For the full square window of `156` profile values, Moore nonvanishing is also
equivalent to nonvanishing of the trace-Gram determinant:

```text
Gamma_profile_leading =
  det( Tr_{L/F_p}(G_s^0 * G_t^0) )_{0<=s,t<156}.
```

In fact, if

```text
M_{i,s} = (G_s^0)^(p^i),
```

then

```text
Tr(G_s^0*G_t^0) = sum_i (G_s^0)^(p^i) (G_t^0)^(p^i),
```

so the Gram matrix is `M^T*M` and:

```text
Gamma_profile_leading = M_profile_leading^2.
```

This is a possible class-field/lattice hook: prove that the trace form
restricted to the leading centered-profile frame is nondegenerate.  The
equivalence is valid because the window has exactly the full field dimension.
It should not be confused with lower-dimensional Gram tests, which can be
strictly stronger over finite fields.

The identity toy and lower-dimensional boundary toy are:

```text
p24/centered_profile_moore_trace_gram_identity_toy.py
p24/centered_profile_trace_gram_toy.py
```

They report:

```text
trace_gram_equals_moore_square=1
trace_gram_punit_iff_moore_punit=1
square_rank_gram_mismatches=0
lower_independent_gram_singular=353/997
```

for `q=3, dim=8, trials=1000`.  So the full square Gram determinant is a
valid equivalent certificate for `M_profile_leading`, while lower-dimensional
Gram shortcuts remain unsafe.

## Base-Field Gram Formula

The trace-Gram determinant has an even more explicit base-field form.  Since
`p` is primitive modulo `157`,

```text
Tr_{L/F_p}(zeta^a) = -1 + 157*[a=0].
```

For centered left coefficient vectors, the `-1` part cancels.  Therefore if

```text
G_s^0 = sum_r a_{r,s} zeta^r,       sum_r a_{r,s}=0,
```

then

```text
Tr(G_s^0*G_t^0) = 157 * sum_r a_{r,s} a_{-r,t}.
```

For the leading profile window, with `A_lead=(a_{r,s})` and `J_inv` the
permutation `r -> -r mod 157`,

```text
Gamma_profile_leading = 157 * A_lead^T * J_inv * A_lead.
```

So the centered-profile p-unit can be stated entirely over the base field:

```text
det(A_lead^T * J_inv * A_lead) != 0 mod p.
```

Because the columns of `A_lead` are centered, dropping one left-residue row
gives coordinates on the zero-sum hyperplane.  In those coordinates the
inversion pairing has determinant `157`, so if `D_profile_leading` is the
`156 x 156` determinant after dropping row `r=0`, then:

```text
det(A_lead^T * J_inv * A_lead) = 157 * D_profile_leading^2.
```

Thus the centered-profile branch can be reduced to one ordinary base-field
minor:

```text
D_profile_leading != 0 mod p.
```

This is recorded in:

```text
p24/centered_profile_trace_gram_basefield_formula.md
p24/centered_profile_trace_formula_toy.py
p24/centered_profile_base_minor_identity_toy.py
```

The toy verifies the formula and the need for centering:

```text
trace_formula_mismatches=0
noncentered_formula_mismatches=100
```

## Difference-Minor Sufficient Route

There is an even more direct sufficient scalar on the `156 x 210` centered
marginal itself.  With

```text
C(r,s) = M(r,s) - M(r,0) - M(0,s) + M(0,0),
1 <= r < 157, 1 <= s < 211,
```

define

```text
Delta_C_leading = det(C(r,s))_{1 <= r <= 156, 1 <= s <= 156}.
```

Then:

```text
Delta_C_leading != 0 mod p
  => rank_Fp C = 156
  => rank_Fp C_{157,211}=156.
```

This scalar is not equivalent to `D_profile_leading`: it uses the first
`156` right-difference columns `G_s-G_0`, not the first absolute centered
profile window.  Its advantage is that it is a visible square minor of the
base-field marginal matrix.  The route is recorded in:

```text
p24/centered_marginal_difference_minor_theorem.md
p24/centered_marginal_leading_minor_audit.py
```

Small actual-CM rows `D=-13319`, `D=-6719`, and `D=-10919` showed no case
where the centered marginal had full applicable row rank but the leading
minor vanished.

## Normal-Frame Route

There is a second sufficient proof shape:

```text
the profile span contains the full Frobenius orbit of one normal element of L.
```

Then the profile span is all of `L`.  This is weaker data than proving a
specific leading Moore minor, but it has a crucial extra hypothesis:

```text
normal coordinate + Frobenius-orbit containment.
```

A normal coordinate alone is not enough.  The boundary toy:

```text
p24/centered_profile_normal_frame_toy.py
```

reports:

```text
normal_orbit_rank=8/8
profile_rank_with_one_normal_coordinate=1/8
profile_one_step_stability_defect=1
frobenius_closure_rank=8/8
```

This mirrors the actual-CM stress boundary in
`p24/centered_marginal_rank_stress_audit.md`: a centered-profile value can be
normal while the profile span is not Frobenius-stable and not full.  A
normal-frame proof for p24 must therefore prove orbit containment/stability,
not merely exhibit a normal `G_s^0`.

## Stronger Support Candidate

The dual trace statement may admit a stronger form: every nonzero
`lambda in L` has at least two nonzero right-orbit traces

```text
Tr_{E/R}(lambda*S_j).
```

This would mean any five of the six right orbit packets already separate `L`.
The candidate and its toy support/delete-one audits are recorded in:

```text
p24/hermitian_mixed_right_orbit_support_theorem.md
```

In centered-profile terms, this is a cyclic-code avoidance theorem for the
scalar trace family

```text
f_lambda(s)=Tr_{L/F_p}(lambda*G_s^0).
```

The original theorem says no nonzero `lambda` gives the zero word; the
stronger theorem says no nonzero `lambda` gives a word supported on a single
nontrivial right Frobenius orbit in Fourier space.
