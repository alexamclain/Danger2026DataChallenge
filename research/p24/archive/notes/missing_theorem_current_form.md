# Missing Theorem Current Form

This note consolidates the current proof target after the relative-resolvent,
split-algebra, energy, Lean, and side-agent passes.

## Exact p24 Statement

For the best certificate-oriented third trace,

```text
h = 205880396014 = m*n
m = 66254
n = 3107441
ord_n(p) = 388430
(n-1)/ord_n(p) = 8
```

Let

```text
J_u(X) = sum_k j_{u+m*k} X^k,      0 <= u < m,
```

where the `j_i` are the selected embedded CM cycle over `F_p`.  For a
representative `a` of one of the eight nontrivial Frobenius orbits of
relative `H`-characters, let `f_a` be the minimal polynomial of `zeta_n^a`
over `F_p`.

The exact theorem needed to rule out a harmful dual-coset collapse is:

```text
gcd(f_a, J_0, J_1, ..., J_{m-1}) = 1
```

for each of the eight orbits.

Equivalently, the relative content vector

```text
(J_0 mod f_a, ..., J_{m-1} mod f_a)
```

is nonzero for each orbit.  A Bezout identity among these residues is the
finite-field certificate version.

The packetized small-CM analogue is checked in:

```text
p24/packetized_relative_content_scan.py
p24/packetized_relative_content_scan.md
```

This scan keeps CM roots in the base field, factors `Phi_n` over that field,
and tests `gcd(f_a,J_0,...,J_{m-1})` packet by packet without adjoining
relative roots of unity.  A 50-row run found:

```text
packet_rows=126
nonlinear_packets=82
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
```

A broader bounded run focused on higher small-CM packets found the same
pattern:

```text
rows=120
packet_rows=272
nonlinear_packets=178
content_failures=0
energy_zero_packets=0
packet_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This is evidence for the exact packet theorem target, not a proof.

The current scalar weakening is the partial-moment combination

```text
L1 = M0 + P2 + P157 + P211.
```

The useful p24 one-resultant target is

```text
Res(Phi_3107441, L1) != 0 mod p.
```

The finite-field zero lemma does not prove this scalar target.  A selected
`L1` zero gives only the relative `H` orbit of zeros, so divisor counting
would require correspondence degree `delta < 1`; see

```text
p24/l1_zero_lemma_boundary.md
```

The missing arithmetic input is therefore a selected-origin p-unit theorem,
or an explicit finite-field identity/embedded tower construction that selects
the target component without enumerating the full class set.

The sharper current form of that input is now the **axis-injectivity theorem**
recorded in

```text
p24/l1_axis_injectivity_theorem.md
```

For each packet factor `f_a | Phi_3107441`, define the 368-dimensional
base-field axis space

```text
W_axis = {a0 + g_2(r mod 2) + g_157(r mod 157) + g_211(r mod 211)}.
```

The theorem target is injectivity of

```text
T_a : W_axis -> F_p[X]/(f_a),
T_a(w) = sum_r w(r) F_r mod f_a,
F_r(X) = sum_k j_{n*r + m*k} X^k.
```

Equivalently, the 368 elements

```text
sum_r F_r,
sum_{r == 1 mod 2} F_r,
sum_{r == t mod 157} F_r,   1 <= t < 157,
sum_{r == t mod 211} F_r,   1 <= t < 211
```

are linearly independent over `F_p` inside the degree-388430 packet field.
This proves `L1 != 0` because the `L1` coefficient function is a nonzero
axis-supported weight.  Unlike the older translate-rank target, this
injectivity statement rules out selected-origin cancellation, not merely
identically zero translate families.

The new scan

```text
p24/l1_axis_injectivity_scan.py
```

found no eligible failures: all packets with `deg(f) >= dim(W_axis)` were
axis-injective in the tested windows, while every rank defect seen so far was
forced by the dimension bound `deg(f) < dim(W_axis)`.

The finite implication is Lean-checked in

```text
p24/lean/AxisInjectivityGate.lean
```

The open arithmetic theorem is now exactly this p24 axis-injectivity statement.
The current proof strategy is the direct-sum refinement in

```text
p24/l1_axis_direct_sum_proof_strategy.md
p24/axis_module_direct_sum_gate.md
p24/lean/AxisModuleDirectSumGate.lean
```

It splits axis injectivity into internal normality of the `2`, `157`, and
`211` axis blocks plus directness of their trace-zero parts over the common
constant line.  The new Lean gate checks the finite implication:

```text
component kernels trivial + four image spaces direct
  => full axis evaluation injective.
```

The p24 base-field module decomposition is especially compact:

```text
trivial module: 1 dimension
2-axis:         1 Frobenius orbit of size 1
157-axis:       1 Frobenius orbit of size 156
211-axis:       6 Frobenius orbits of size 35
```

So the 368 geometric axis frequencies form only nine Frobenius-stable modules
over `F_p`.  This accounting is reproducible via

```text
p24/l1_axis_frobenius_module_audit.py
```

The packet-field intersection audit

```text
p24/axis_packet_field_intersection_audit.py
```

adds:

```text
ord_157(p)=156,  gcd(156,388430)=2,   157-axis not in packet field;
ord_211(p)=35,   35 | 388430,         211-axis roots lie in packet field.
```

Thus the p24 direct-sum proof should probably treat the `211` and `157` axes
differently rather than as symmetric smooth factors.  The `211` fact gives a
useful character coordinate chart, but not an automatic base-field rank
equivalence.

A tempting stronger shortcut is false in small CM data: the component image
spans are not generally stable under packet-field Frobenius.  The boundary is
recorded in

```text
p24/axis_frobenius_stability_audit.py
p24/axis_frobenius_cocycle_boundary.md
```

The actual relation is

```text
sigma(G_s(eta)) = G_{p*s}(eta^p),
```

so the H-packet coordinate moves with the K-character coordinate.  Directness
must therefore be proved as a coupled K/H p-unit or by tensor-separating the
K-character roots before descent, not by ordinary Frobenius-module
nonisomorphism alone.  The formal scalar-extension descent gate is in

```text
p24/lean/ScalarExtensionGate.lean
```

The corrected tensor-rank target is recorded in

```text
p24/tensor_decomposition_accounting.py
p24/k_character_tensor_rank_scan.py
p24/k_character_tensor_rank_theorem.md
```

For p24, adjoining `E=F_p(mu_m)` gives `[E:F_p]=5460` and splits each
degree-388430 H-packet into `70` factors of degree `5549` over `E`.  Since
`5549 > dim(W_axis)=368`, a single tensor factor could carry the entire axis
rank certificate if the 368 K-character resolvents are E-linearly independent
there.

The one-factor refinement is tested by

```text
p24/k_character_tensor_factor_rank_scan.py
```

In small nonsplit rows, whenever a single tensor factor has enough dimension,
that factor already carries full axis rank.  For p24 the analogous tensor
factor degree is `5549`, comfortably above `368`.

The factor choice is not an additional datum.  Semilinear Frobenius permutes
the tensor factors and the selected axis frequency set, so all tensor factors
have the same axis rank.  This is recorded in

```text
p24/tensor_factor_rank_symmetry.md
```

The one-factor determinant can also be split into smooth component blocks:

```text
p24/k_character_tensor_factor_block_scan.py
p24/tensor_factor_block_directness.md
```

Small nonsplit data shows no dimension-unforced component-normality or
pair-directness failure, so the p24 tensor theorem can be phrased as
component block normality plus cross-block directness inside one degree-5549
factor over `F_p(mu_m)`.

This directness is not a formal K-eigenspace consequence inside one tensor
factor.  The obstruction is recorded in

```text
p24/tensor_factor_k_action_boundary.md
```

Dimension-bound small data has more nonzero distinct K-character resolvents
than the tensor factor dimension, so a single internal diagonal K-action on
that factor cannot exist.

The finite implication from a one-factor coordinate minor to the base packet
axis theorem is now Lean-checked in

```text
p24/lean/TensorFactorProjectionGate.lean
```

and summarized in

```text
p24/one_factor_certificate_chain.md
```

The coordinate-free version is the one-factor Moore determinant:

```text
p24/tensor_factor_moore_audit.py
p24/tensor_factor_moore_certificate.md
```

It asks for nonvanishing of

```text
det(R_s^(Q^j))_{s in S_axis, 0 <= j < 368}
```

inside the degree-5549 tensor factor over `E=F_p(mu_m)`.

Norm/Hermitian packaging has a boundary:

```text
p24/tensor_factor_norm_packaging_boundary.md
p24/tensor_factor_pairing_accounting.py
```

Coordinate minors are Pluecker-coordinate dependent.  The Moore determinant is
intrinsic for one-factor rank, while Hermitian inversion pairs tensor factors
`i` and `i+35` because `p^(ord_n(p)/2)=-1 mod n`.

The degree-5549 factor has a useful internal refinement:

```text
p24/tensor_factor_intermediate_accounting.py
p24/tensor_factor_subfield_trace_audit.py
p24/tensor_factor_intermediate_trace_split.md
```

Since `5549=31*179`, proper traces to the degree-31 and degree-179
intermediate fields can potentially certify component block normality.  The
dimension count rules out using only proper traces for the full axis
(`368 > 31+179`), but they fit the component blocks:

```text
constant + 2 + 157 has dimension 158 < 179
211 has dimension 210 = 31 + 179
```

The current refined theorem target is therefore: prove the relevant trace
maps are injective on these component spans, and prove cross-block directness
inside the full degree-5549 factor.

The stronger intermediate-field refinement is now the twisted trace-frame
target:

```text
p24/tensor_factor_twisted_trace_frame.md
p24/tensor_factor_twisted_trace_frame_audit.py
p24/tensor_factor_trace_period_identity.py
p24/tensor_factor_trace_period_identity.md
p24/trace_frame_decimated_period_certificate_target.md
p24/trace_frame_factorized_decimated_period_theorem.md
p24/trace_frame_relative_trace_normality_lemma.md
p24/trace_frame_relative_trace_normal_basis_toy.py
p24/subagent_decimated_period_synthesis.md
p24/tensor_factor_trace_annihilator_theorem.md
p24/tensor_factor_dual_basis_window_audit.py
p24/tensor_factor_top_coefficient_capacity.py
p24/tensor_factor_top_coefficient_block_split.md
p24/tensor_factor_relative_coefficient_profile.py
p24/tensor_factor_relative_coefficient_profile.md
p24/tensor_factor_top_coefficient_fourier_audit.py
p24/tensor_factor_top_coefficient_fourier.md
p24/tensor_factor_trace_frame_probability.py
p24/tensor_factor_trace_frame_probability.md
p24/lean/TraceFrameGate.lean
p24/lean/TraceFrameAnnihilatorGate.lean
```

Let `C=F_{Q^179}` and let `theta` be the packet-coordinate image in the chosen
factor.  Prove that the three-coordinate trace frame

```text
R_s |-> (
  Tr_{B/C}(R_s),
  Tr_{B/C}(theta R_s),
  Tr_{B/C}(theta^2 R_s)
)
```

has `E`-rank `368` on the selected axis set.  Since `3*179=537 > 368`, this
is dimensionally possible and shrinks the one-factor certificate surface from
degree `5549` to three degree-`179` trace coordinates.  The pinned
`D=-10919` row with `[B:E]=6=2*3` recovers full axis rank by the analogous
minimal twisted trace frames.

The trace coordinates have an explicit p24 period form.  If
`a=p^5460 mod n`, then `Tr_{B/C}` sums over the order-31 subgroup generated
by `a^179`; the full certificate is a `3 x 179` family of 31-term decimated
H-period sums.

Equivalently, using the perfect trace pairing on `B/C`, the theorem is:

```text
W_axis(B) ∩ span_C{1, theta, theta^2}^perp = {0}.
```

The annihilator has `C`-dimension `28`, so this is a structured
kernel-avoidance theorem rather than an arbitrary coordinate-rank statement.
In the random-subspace model, failure has leading probability `Q^-170` for
`Q=p^5460`; any actual failure would therefore need a structured CM
annihilator.

The coordinate-free finite certificate is nonvanishing of the exterior vector

```text
∧_{s in S_axis} T_3(R_s) in Exterior_E^368(C^3).
```

Any chosen `368 x 368` minor is only a Plucker coordinate of this object.

The dual-basis form gives an even more concrete finite identity: if `g` is
the degree-31 minimal polynomial of `theta` over `C`, multiply an axis image
`x` by `g'(theta)` and expand in the `C`-basis
`1,theta,...,theta^30`.  The trace-frame map is equivalent to the top three
relative coefficients (`theta^30, theta^29, theta^28`).  The p24 target is
that this top-coefficient map is injective on the 368-dimensional axis image.

Component capacity now suggests a split theorem:

```text
Top_1 injective on constant + 2 + 157    (dimension 158 < 179),
Top_2 injective on 211                   (dimension 210 < 2*179),
Top_3 injective on the full axis         (dimension 368 < 3*179).
```

The sharper factorized form is now pinned in:

```text
p24/trace_frame_factorized_decimated_period_theorem.md
```

It writes the selected leading `Top_3` coordinate as:

```text
179 prefix coordinates
+ 179 prefix coordinates
+ 10 residual-tail coordinates.
```

With:

```text
A = constant + 2 + 157,       dim_E A = 158
B = 211,                      dim_E B = 210
dim_E C^2 = 358
```

the prefix theorem is:

```text
rank Top_2(W_axis) = 358,
dim(Top_2(A) cap Top_2(B)) = 10.
```

The residual theorem is:

```text
pi_10 o b_28 : ker(Top_2|W_axis) -> E^10
is injective.
```

Equivalently, the missing arithmetic input is now four equivariant
decomposition-field Schubert p-units:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail in K_m Q(zeta_n)^<p>,
Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_F) mod p != 0.
```

For global descent, the denominator-safe variant is probably better:

```text
Xi_A, Xi_B, Xi_AB, Xi_lead in K_m Q(zeta_n)^<p>
```

where `Xi_lead` is the full selected `179+179+10` leading Plucker coordinate.
Then the residual-tail p-unit is inferred from:

```text
Delta_lead = Delta_prefix * Delta_tail
```

on the open prefix chart, rather than by treating a packetwise kernel basis as
global data.

The finite implication for this denominator-safe package is checked in:

```text
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
```

This is the current smallest proof-facing statement.  It does not replace the
`Top_3` theorem; it factorizes it into the prefix intersection and residual
tail p-unit surfaces where a class-field identity or divisor contradiction
would have to act.

The final line remains the certificate, but the first two are smaller
component-normality subtheorems plus a cross-block directness theorem in
`C^3`.

The top-coefficient map has an exact frequency-side identity:

```text
Top_k(R_s) = DFT_s(r |-> Top_k(J_r)).
```

Small rows show dense frequency support in every output coordinate, so this
does not collapse to a block-diagonal Vandermonde proof.  The theorem is a
vector-valued Fourier anti-annihilator statement for the quotient sequence
`Top_k(J_r)`.

For each CRT component `c`, the selected component frequencies are the DFT of
the marginal sequence

```text
a mod c |-> sum_{r == a mod c} Top_k(J_r).
```

The exact marginal-rank lemma is recorded in

```text
p24/tensor_factor_crt_marginal_rank_audit.py
p24/tensor_factor_crt_marginal_rank.md
p24/tensor_factor_marginal_annihilator_theorem.md
```

For

```text
M_{c,a}^{(k)} = sum_{r == a mod c} Top_k(J_r),
Delta_c^(k) = span{M_{c,a}^{(k)} - M_{c,0}^{(k)} : a != 0},
S_k = sum_r Top_k(J_r),
```

the DFT/root-of-unity layer is now completely formal:

```text
nontrivial c-block rank = dim Delta_c^(k),
constant-plus-c-block rank = rank{M_{c,a}^{(k)} : a mod c}.
```

Therefore the remaining p24 theorem is the marginal affine-rank/directness
statement:

```text
dim_E( E*S_1 + Delta_2^(1) + Delta_157^(1) ) = 158,
dim_E( Delta_211^(2) ) = 210,
dim_E( E*S_3 + Delta_2^(3) + Delta_157^(3) + Delta_211^(3) ) = 368.
```

The dense packet-coefficient operator is the arithmetic part.  Nonzero
marginals alone do not suffice; the theorem needs affine independence and
cross-component directness of these vector-valued packet sums.

Equivalently, prove nonvanishing of the three exterior products:

```text
Omega_1    in Exterior_E^158(C),
Omega_211  in Exterior_E^210(C^2),
Omega_3    in Exterior_E^368(C^3).
```

This is the deterministic version of the random-subspace heuristic: show that
the selected CM Plucker content is a p-unit, rather than estimating that a
random subspace would avoid the incidence divisor.

The Hermitian Schur-correction route has a sharper CS/coding-theory form:

```text
p24/hermitian_double_marginal_fourier.md
p24/hermitian_mixed_frobenius_orbit_audit.py
p24/hermitian_mixed_moore_circulant_theorem.md
p24/hermitian_mixed_lang_normality_audit.py
p24/hermitian_mixed_lang_normality_theorem.md
p24/hermitian_mixed_left_subfield_normality_audit.py
p24/hermitian_mixed_left_subfield_identity_toy.py
p24/hermitian_mixed_trace_dual_formula_toy.py
p24/hermitian_mixed_dual_trace_injectivity_toy.py
p24/hermitian_mixed_left_subfield_span_theorem.md
p24/hermitian_mixed_trace_intersection_theorem.md
p24/hermitian_mixed_resolvent_pairing_formula.md
p24/hermitian_mixed_resolvent_pairing_audit.py
p24/lean/MixedMooreGate.lean
p24/lean/MixedTraceDualGate.lean
p24/lean/MixedTraceIntersectionGate.lean
```

The mixed `157 x 211` centered double marginal is equivalent, after adjoining
roots of unity, to a `156 x 210` nonzero K-character Hermitian pairing matrix.
Because the Hermitian kernel is base-field valued, this matrix is a six-block
Moore/Frobenius-circulant matrix:

```text
ord_157(p)=156: one row orbit
ord_211(p)=35:  six column orbits
B_j(a,b)=b_j(b-a mod 35)^(p^a).
```

So the missing mixed-Schur theorem can be stated as:

```text
no nonzero skew-linearized convolution operator of p-degree < 156
annihilates all six p24 CM seed cycles.
```

This is the current best import from rank-metric/Gabidulin/PIT theory.  It
compresses the proof surface from a raw `156 x 210` determinant to an
interleaved skew-annihilator p-unit, but it does not by itself prove the
selected-prime p-unit.

The skew-annihilator criterion has a Lang-normality refinement.  For each
right orbit of length `R`, the semilinear shift

```text
T(s)_b = sigma(s_{b-1})
```

is trivialized by the Moore fixed-vector basis

```text
u_alpha(b)=sigma^b(alpha),       alpha in F_{p^R}.
```

After this change of coordinates, a mixed row orbit is an ordinary Moore
matrix.  For p24 the mixed-Schur theorem is therefore equivalent to:

```text
the 210 Lang-trivialized mixed Hermitian seed coordinates have
F_p-span dimension at least 156.
```

Since `gcd(156,35)=1`, these 210 transformed coordinates land in the left
character field:

```text
F_p(mu_157)=F_{p^156}.
```

The most compact finite-field target for the mixed Schur correction is now:

```text
dim_Fp span{210 transformed mixed Hermitian periods in F_{p^156}} = 156.
```

This asks for a tuple-span/Moore-minor p-unit theorem for 210 explicit
class-field periods, rather than a raw determinant or a generic rank-condenser
statement.  A single normal coordinate is not sufficient; the Moore rank is
the `F_p`-rank of the transformed tuple.

The transformed tuple has an intrinsic relative-trace formula.  If

```text
E = F_p(mu_157, mu_211),       L = F_p(mu_157),
S_j = H_{157,211}(1, v_j)      for the six 211-orbit representatives,
```

and `{delta_i}` is the `Tr_{F_p(mu_211)/F_p}`-dual basis to a right normal
basis, then the target is:

```text
dim_Fp span{Tr_{E/L}(delta_i * S_j) : 1 <= i <= 35, 1 <= j <= 6} = 156.
```

This is now the class-field-facing form of the mixed Schur theorem.

By trace duality on `L/F_p`, the same theorem is equivalent to injectivity of:

```text
L -> R^6,
lambda |-> (Tr_{E/R}(lambda * S_j))_{j=1..6}.
```

That is, no nonzero `lambda in F_p(mu_157)` is killed by all six relative
traces to `F_p(mu_211)`.

Equivalently, if

```text
W = span_R{S_1,...,S_6} subset E,
```

then:

```text
L ∩ W^perp = {0}
```

for the `E/R` trace pairing.  This is the local intersection form of the
mixed Schur theorem.  It matters that `dim_R W <= 6`; the proof cannot ask
for `W=E`, only for transversality of a large `R`-orthogonal complement with
the embedded `F_p`-space `L`.

The six periods are not opaque entries; they are mixed K-character resolvent
pairings:

```text
S_j = H_{157,211}(1,v_j) = <A_1,B_{v_j}>.
```

So the arithmetic theorem is a transversality statement for six pairings
between the left `157`-character resolvent and the six right `211`-orbit
resolvents.

The origin-stable coordinate packaging is now recorded in

```text
p24/tensor_factor_marginal_origin_action_audit.py
p24/tensor_factor_marginal_origin_product.md
p24/tensor_factor_marginal_beta_complexity.py
p24/tensor_factor_marginal_beta_complexity.md
p24/tensor_factor_beta_recurrence_audit.py
p24/tensor_factor_beta_recurrence_resultant.md
p24/tensor_factor_plucker_spectral_support.md
p24/tensor_factor_trace_coordinate_support_audit.py
p24/tensor_factor_trace_coordinate_support.md
p24/tensor_factor_marginal_random_support_audit.py
p24/tensor_factor_marginal_random_support.md
p24/tensor_factor_beta_support_audit.py
p24/tensor_factor_beta_support_boundary.md
```

For a chosen Plucker coordinate `P`, the product

```text
prod_{beta mod n} P(Omega_beta)
```

has origin-stable zero status.  Small rows show the expected alpha/beta
behavior, but this is a stronger coordinate p-unit target than intrinsic
nonvanishing of `Omega` at the selected origin.

The beta-support boundary is negative for generic compression: for the p24
tensor-factor orbit `O=<p^5460> mod n`, `O+O` misses only `16648` residues and
`O+O+O` is all of `Z/nZ`.  Thus the large exterior products can have full beta
character support; a proof cannot rely on a small-support recurrence shortcut.
The recurrence/resultant form remains a valid finite certificate surface, but
it only gives an asymptotic improvement if a chosen Plucker coordinate uses few
degree-`5549` spectral orbits.

Small CM-vs-random audits show the projected toy recurrence order is generic
for the determinant shape (`random_order_hist={7:40}`), so support collapse is
not presently a CM-specific explanation for nonvanishing.
For actual p24 trace-coordinate minors, six trace-coordinate cosets already
have full beta support in every tested random six-coordinate sample, while the
candidate minors select `158`, `210`, or `368` coordinates.  Thus ordinary
coordinate-minor recurrence compression is also not a visible speedup.

The first stable Plucker norm miner is recorded in:

```text
p24/tensor_factor_plucker_norm_miner.py
p24/tensor_factor_plucker_norm_miner.md
```

It enumerates ordinary trace-coordinate maximal minors in pinned toy rows and
compares beta-product norms against random tensor-factor controls.  The result
is also negative for the simplest norm-identity search: CM products are
nonzero but full-degree and random-looking, with no unusually small or
factorable base norms in the natural coordinates.  So a Plucker p-unit proof
must use an intrinsic exterior norm, a CM-adapted coordinate change, or a
full-support class-field identity rather than an obvious natural coordinate
minor product.

The intrinsic Hermitian norm route has a refined component boundary in:

```text
p24/hermitian_component_schur_audit.py
p24/hermitian_component_schur_boundary.md
```

Small `(4,3)` rows show nonsingular diagonal component blocks, so component
p-unit sublemmas are still plausible.  But the Schur correction
`det(full)/prod(det(blocks))` is nontrivial and varies with the split prime.
Thus the Hermitian packet norm target cannot be replaced by independent CRT
component determinants; the cross-component correction is an essential
selected CM p-unit.

The correction has an exact centered CRT double-marginal form:

```text
p24/hermitian_double_marginal_audit.py
p24/hermitian_double_marginal_formula.md
```

For the Hermitian kernel

```text
K(r,s)=Tr_packet(F_r(X)F_s(X^-1)),
```

each `U_c x U_d` axis block is the centered double marginal

```text
sum_{r==a mod c, s==b mod d} K(r,s)
 - row/column origin terms + origin term.
```

This makes the current Hermitian theorem target more explicit: prove p-unit
status of the centered component marginals and the mixed centered
`157 x 211` Schur correction, then take the degree-8 packet norm.

The centered correction also has a character-pairing form:

```text
p24/hermitian_double_marginal_fourier_audit.py
p24/hermitian_double_marginal_fourier.md
```

After adjoining `mu_m`, centered marginal rank equals nonzero double-DFT rank.
Thus the `157 x 211` correction is equivalently a `156 x 210` mixed
nonzero K-character Hermitian pairing matrix.  This is now the cleanest
class-field-facing statement of the Schur correction p-unit.

The CS-theory translation is recorded in:

```text
p24/cs_ml_theory_imports.md
p24/cs_rank_condenser_theorem_status.md
```

In that language, the open theorem says the CM marginal generator is a
rank-condenser/subspace-evasive map for the structured CRT-axis code, with
`Omega_1`, `Omega_211`, and `Omega_3` as Plucker p-unit certificates.

The structured-code audit:

```text
p24/tensor_factor_marginal_cs_structure_audit.py
```

rules out the simplest off-the-shelf matrix explanation in the natural
trace-coordinate order.  On the pinned `D=-10919, m=12` tensor row, the CM
marginal matrices have full rank, but Toeplitz/Hankel and cyclic displacement
ranks are maximal and match random tensor-factor controls.  Therefore the
remaining CS-shaped input is a selected CM rank-condenser p-unit theorem or a
Moore/Gabidulin normality parent theorem, not a visible Cauchy/Toeplitz/GRS
determinant formula.

A stronger parent theorem is recorded in

```text
p24/rank_safe_axis_theorem_target.md
p24/relative_k_normality_parent_theorem.md
```

It asks for full `K`-rank of the complement fibers:

```text
F_0, ..., F_{66253}
linearly independent in F_p[X]/(f_a).
```

Since `66254 < 388430`, this is dimensionally possible and would immediately
imply axis injectivity.  The axis theorem remains the smaller certificate
surface, but full relative `K`-normality may be the more natural class-field
proof target.

The basis-free certificate form is the Moore determinant in

```text
p24/k_normality_moore_certificate.md
```

For `beta_r = F_r(zeta_a)`, prove

```text
det(beta_r^(p^s))_{0 <= r,s < 66254} != 0
```

in each packet field.  A failure would produce a nonzero `K`-weight vector
`w` with `f_a | sum_r w_r F_r(X)`.

After adjoining `mu_m`, the same theorem is rank of the full `K`-character
resolvents.  The split-character toy diagnostic is in

```text
p24/scalar_extension_rank_pitfall_toy.py
p24/k_character_rank_split_boundary.md
```

It found no dimension-possible rank defects in rows where `m | q-1`, but it
also showed that individual character nonvanishing is formally weaker than
rank: dimension-bound rows had every character resolvent nonzero while rank
was necessarily deficient.

For p24 this rank statement must be interpreted in the tensor scalar extension
of the packet field.  A single embedding into a larger splitting field would
collapse the rank information.

There is a second, packet-field-specific warning.  If a character transform has
coefficients in the packet field rather than in the base field, invertibility
over the packet field does not by itself preserve the `F_p`-span of coordinate
entries.  The minimal witness is

```text
p24/packet_field_dft_rank_warning_toy.py
```

over `F_4/F_2`, where an invertible packet-field matrix sends `(0,1)` to
`(1,alpha)` and raises the base-field coordinate span from `1` to `2`.

For components whose character roots live inside the packet field, the closer
diagnostic is

```text
p24/component_character_module_boundary.md
```

This is the toy analogue of the p24 `211`-axis.  In all dimension-possible
reported rows, the component Frobenius character modules had full rank and no
zero orbit.  These rows support the structure, but the p24 proof still has to
return to a base-field directness statement or to the Moore/tensor rank
statement.

The exact p24 K-character module decomposition over one H-packet field is in

```text
p24/packet_field_k_module_audit.py
```

It reports:

```text
full_mu_m_extension_over_packet_degree=78
axis over packet field:
  2-axis   = 1 orbit of size 1
  157-axis = 2 orbits of size 78
  211-axis = 210 orbits of size 1
full K orbit histogram = {1: 421, 78: 844}
```

A new sufficient determinant target is recorded in

```text
p24/trace_gram_axis_certificate.md
p24/hermitian_trace_gram_axis_certificate.md
```

The ordinary version asks for nonvanishing of the `368 x 368` trace Gram
matrix on the axis basis images.  This does not equal Moore rank for arbitrary
proper subspaces, and a broader small CM scan found a full-rank axis row with
degenerate ordinary trace Gram.  The Hermitian version replaces
`Tr(Y_i Y_j)` by `Tr(Y_i Y_j^(p^(d/2)))`; it rescued that row and better
matches p24 because the packet degree is even and the middle Frobenius is
H-character inversion.

The Hermitian structure scan found no free factorization:

```text
p24/hermitian_trace_gram_structure_scan.py
p24/hermitian_axis_lattice_primitivity.md
p24/hermitian_origin_invariance_theorem.md
p24/hermitian_axis_packet_norm_theorem.md
```

In eligible composite-`m` rows, the Hermitian Gram had full rank, but the
kernel was never difference-circulant and the CRT trace-zero blocks were not
mutually orthogonal.  This keeps the target as one coupled p-unit determinant,
best phrased as Hermitian-unimodularity of the selected axis lattice.

The remaining low-rank CRT-coupling hope is also false in small data:

```text
p24/hermitian_cross_block_rank_audit.py
p24/hermitian_cross_block_rank_boundary.md
```

The first broad scans only saw cross-block rank `1`, but those rows had a
component `2`.  Targeted rows with `m=12=4*3` and packet degrees large enough
for the axis have nontrivial `(4,3)` cross-block rank `2`, while the Hermitian
Gram stays full rank.  So the p24 determinant should be treated as genuinely
coupled, not as component determinants plus rank-one Schur corrections.

There is one simplification: the Hermitian determinant is invariant under
rotating the embedded CM origin.  An origin shift multiplies every packet
element by `X^(-beta)` and translates the axis coordinate; middle Frobenius
inverts `X^(-beta)`, so the Hermitian pairing cancels the monomial.  The
remaining theorem is packetwise, not originwise.

The eight packet determinants can also be packaged as one degree-8
decomposition-field norm:

```text
prod_a det(H_a) != 0 mod p
```

or, over `M^+`, `p ∤ Norm_{M^+/Q}(Delta_axis)`.  Small packet-norm scans show
the packet values are not generally equal, so this norm packaging is the right
compression, not a reduction to one representative packet.

There is a new coordinate-minor side target:

```text
p24/axis_coefficient_minor_audit.py
p24/axis_coefficient_minor_boundary.md
```

If a fixed coordinate projection after packet reduction is injective on
`W_axis`, then axis injectivity follows; this is now Lean-gated by
`injective_from_projected_eval`.  Small scans found no leading-minor failures,
including all-origin checks for `D=-8711` and `D=-10919` with `m=12=4*3`.
But this is a less invariant theorem target than the Hermitian determinant:
the coordinate minor is taken after reduction modulo `f_a`, so it still
depends on packet-level embedded class data, and its determinant values vary
with the CM origin.  It is a useful finite certificate shape, not yet a better
class-field norm.

The attempted Cauchy-Binet bridge back to the Hermitian determinant is recorded
in:

```text
p24/plucker_trace_form_audit.py
p24/plucker_trace_form_boundary.md
```

The first row with extra packet coordinates has a dense exterior expansion:
all `210` Pluecker coordinates are nonzero and thousands of off-diagonal
trace-form terms contribute.  So a leading-minor p-unit would prove axis
injectivity directly, but it does not currently prove the Hermitian
`Delta_axis` p-unit theorem.

The origin-action refinement is recorded in:

```text
p24/axis_minor_origin_action_audit.py
p24/axis_minor_origin_action_boundary.md
```

Pure `alpha` shifts are formal axis-basis changes, but pure `beta` shifts test
the leading minor after multiplication by `X^(-beta)`.  Thus an
origin-independent coefficient-minor theorem is best viewed as a cyclic
consecutive-Pluecker or superregularity statement for the selected CM axis
subspace in the packet power basis.

The random baseline in

```text
p24/cyclic_superregular_random_baseline.py
p24/cyclic_superregular_random_baseline.md
```

shows why this is not yet proof-like.  On `D=-8711`, random full-rank subspaces
failed some beta-shifted leading minor only `4/5000` times, near the `n/q`
heuristic.  For p24 the random failure scale would be about `3e-18` per
packet.  The route is therefore a concrete finite certificate surface, but it
still needs selected-prime CM arithmetic rather than random-generic evidence.

The origin-stable product version is now:

```text
p24/axis_sliding_window_product_audit.py
p24/axis_sliding_window_product_theorem.md
```

For each packet,

```text
Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a).
```

Beta origin shifts permute the factors, while alpha shifts multiply by an
axis-basis unit.  Small rows show the product varies only by sign and never by
zero/nonzero status.  Thus the coefficient-minor theorem can be stated
packetwise as `Pi_axis,a != 0`, or value-invariantly as `Pi_axis,a^2` a
p-unit.  It remains coordinate-dependent and has no known class-field norm
formula.

The sequence-complexity audit:

```text
p24/axis_sliding_window_sequence_complexity.py
p24/axis_sliding_window_sequence_complexity.md
```

shows no recurrence shortcut for this product.  On the first
extra-dimensional row `D=-8711`, the beta-minor sequence has full
Berlekamp-Massey complexity `11/11`, exactly like random subspaces.  The
product is therefore origin-stable but still high-order in the packet beta
phase.

The p24 exterior character-support audit:

```text
p24/exterior_character_support_audit.py
p24/exterior_character_support_boundary.md
```

computes the Frobenius packet orbit `H=<p> mod 3107441` and finds
`H+H = Z/3107441Z`, with at least `48343` ordered representations of every
residue.  Thus the exterior-power packet representation has full beta-character
support available; low character support cannot explain or compress
`Pi_axis,a`.

The full Grassmannian open-cell audit:

```text
p24/plucker_full_support_audit.py
p24/plucker_full_support_boundary.md
```

finds that the `D=-8711` CM axis subspace has all `210` coordinate Pluecker
minors nonzero, but `490/500` random subspaces do too.  Thus even the stronger
uniform-matroid/MDS condition looks generic at small scale, not CM-specific.

The zero-lemma boundary for the Moore parent theorem is recorded in

```text
p24/k_normality_fourier_zero_boundary.md
```

The condition `f_a | sum_r w_r F_r(X)` is a Fourier/character-packet zero, not
pointwise vanishing on many CM roots.  Thus the modular divisor-count zero
lemma does not apply directly.

The simplest finite-field identity shapes have now been tested negatively.
The `L1` interpolation diagnostic in

```text
p24/l1_interpolation_shape_boundary.md
```

shows no low-degree rational function of the selected `j` root after accounting
for the expected `H`-periodicity.  The Hermitian companion diagnostic in

```text
p24/packet_scalar_divisor_shape_boundary.md
```

shows the same generic plain-`j` interpolation behavior for the Hermitian
packet norm.  A surviving identity must therefore be phase-aware or
higher-dimensional, not a cheap one-variable selector.

The most tempting ray-class lift from the cached Siegel/Ramachandra
literature is also now separated:

```text
p24/ray_kernel_embedding_boundary.md
```

Small auxiliary ray kernels with `157` or `211` factors exist, but they are
vertical over level-1 `j`: the local ray kernel fixes the ordinary CM root and
only changes level structure.  Norms or quotients along that kernel therefore
construct ray-field units, not an embedded unramified Hilbert-class phase.

The uploaded small-prime DANGER3 data has also been rechecked:

```text
p24/upstream_near_square_dataset_boundary.md
```

For the small analogue `p=n^2+7`, `n==0 mod 8`, the published witnesses all
fall in the nonsplit zero-terminal branch, but the residual `A` and `x`
statistics remain broad and the simple Legendre labels split.  The data
supports a verifier-side branch constraint, not a new embedded CM selector.

Finally, the decomposed CM route has been refreshed:

```text
p24/decomposed_route_refresh.md
```

Its final degrees would be excellent (`66254` and `3107441`), but the
calibrated construction obtains those equations only after a seed embedded CM
root and full class-action cycle are available.  It remains a positive target,
not an operational certificate construction.

## Split-Algebra Form

Over the class field with `mu_n`, define

```text
Theta_a = sum_k zeta_n^(a*k) sigma^(m*k)(j_0).
```

Then

```text
P_u(a) = sigma^u(Theta_a),
sigma^m(Theta_a) = zeta_n^(-a) Theta_a.
```

After reduction at the selected split prime, the component of `Theta_a` at
`sigma^(u+m*l)P` is

```text
zeta_n^(-a*l) P_u(a).
```

Thus all relative fibers vanish iff `Theta_a` is zero in the entire split
class algebra modulo the selected cyclotomic prime.

The finite logic of this step is checked in Lean:

```text
p24/lean/RelativeResolvent.lean
```

The surrounding certificate implications are also checked in Lean:

```text
p24/lean/CertificateLogic.lean
```

This second file formalizes the abstract facts that an invertible finite
transform preserves all-zero vectors, a content/Bezout identity rules out an
all-zero packet, product nonvanishing is a sufficient but stronger certificate,
and energy nonvanishing rules out harmful vanishing once harmful vanishing is
known to force the energy scalar to be zero.

Lean is useful here because these are small finite-algebra/logical theorems.
It does not prove the p24 CM nonvanishing theorem; that is still the
arithmetic input.

## Scalar Sufficient Certificate

The first useful weakening from a vector certificate is the energy

```text
E_a = sum_u P_u(a) P_u(-a).
```

If `E_a != 0`, then the harmful event cannot occur.  This is only sufficient,
because nonzero fibers can cancel in the energy sum.

The same scalar has two equivalent forms:

```text
E_a = sum_d zeta_n^(a*d) C_d,
C_d = sum_i j_{i+m*d} j_i,
```

and

```text
sum_r R_{a+r*n} R_{-a-r*n} = m E_a.
```

So `E_a` is both a relative autocorrelation transform and the paired spectral
mass of the full dual coset.  This is an additive Parseval identity, not the
false coordinate-product shortcut.

It is also the Hermitian Gram scalar of the content vector:

```text
C(X) = sum_u J_u(X)J_u(X^-1).
```

This identity is useful but one-way only.  The note

```text
p24/energy_gram_isotropy_boundary.md
```

and toy

```text
p24/energy_isotropy_obstruction_toy.py
```

show that a nonzero relative-content vector can have zero Hermitian energy in
the packet algebra.  Thus energy nonvanishing is not a formal consequence of
the exact content theorem; it needs separate CM/autocorrelation arithmetic.

There is a better positive scalar obtained by pairing quotient fibers with
their inverse quotient coordinates.  If

```text
u* = -u mod m,
c(u) = (u+u*)/m,
```

then complex conjugation gives

```text
conj(P_u(a)) = zeta_n^(a*c(u)) P_{u*}(a),
```

and the Hermitian scalar

```text
H_a = sum_u zeta_n^(a*c(u)) P_u(a)P_{u*}(a)
```

is `sum_u |P_u(a)|^2` in characteristic zero.  Modulo `p`, `H_a != 0` is
another sufficient packet certificate.  This route is recorded in:

```text
p24/hermitian_energy_certificate.md
p24/complex_energy_positivity_boundary_toy.py
```

The packetized scan now tests this scalar too; the same 50-row run found:

```text
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

In a low-order scan that included known small CM failure regimes, ordinary
energy had natural packet failures but Hermitian energy did not:

```text
packet_rows=70
energy_zero_packets=2
packet_norm_zero_packets=2
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

This makes Hermitian energy the preferred scalar certificate target, although
not a formal consequence of content nonzero.

The stronger individual-fiber product certificate is now known to be too
strong as a general CM theorem.  A broader natural relative-resolvent scan
found no harmful all-fiber collapse but did find one individual zero fiber:

```text
D=-1336, q=1777, ell=5, h=12, m=2, n=6
individual_zero_fiber_count=1
harmful_a_count=0
```

This is recorded in:

```text
p24/relative_product_too_strong_scan.md
```

So product nonvanishing can still be a p24-specific sufficient certificate,
but it should not be treated as the expected theorem.  Exact content or the
Hermitian packet scalar remain better targets.

The low-moment projection package is now another compact target:

```text
M_e(X) = sum_u u^e J_u(X)
prove gcd(Phi_3107441, M_0, M_1) = 1 mod p.
```

This is a sufficient exact-content certificate: if all `J_u` vanished in a
packet, both moments would vanish.  The single complement trace `M_0` is not
a general theorem.  Pinned failures include:

```text
D=-899 q=281 h=14 m=2 n=7:
  residues at one factor are [-69,69], so M0=0 but M1!=0.

D=-216 q=103 h=6 m=2 n=3:
  first_nonzero_moment=1.
```

The early-exit search in

```text
p24/moment_pair_failure_search.py
```

found no `{M_0,M_1}` failures in the current bounded windows:

```text
complement non-origin: tested_packets=545, m0_failures=1
contiguous non-origin: tested_packets=810, m0_failures=2
complement origin scan: tested_packets=1204, m0_failures=0
contiguous origin scan: tested_packets=1565, m0_failures=0
```

This is not a linear-algebra theorem: for `m>=3`, nonzero vectors can have
zero first two moments.  It is a compact p24-specific p-unit target, not yet a
construction of the embedded moment polynomials.

The two-moment target is now best phrased as a relative augmentation-jet
theorem:

```text
p24/relative_augmentation_order_theorem.md
p24/relative_augmentation_order_scan.py
```

For a packet factor `f_a | Phi_n`,

```text
V_a(Y) = sum_u (J_u mod f_a) Y^u.
```

Then `{M_0,M_1}` asks that no nonzero packet polynomial has a double zero at
`Y=1`, i.e. `V_a in (Y-1)^2 => V_a=0`.  This is stronger than exact content
but weaker than relative normality.  It also separates the constructive
`M_0` complement trace from the safer first-order `K`-augmentation jet.

A further tower-construction refinement is now recorded in:

```text
p24/crt_partial_moment_tower_boundary.md
p24/augmentation_crt_derivative_toy.py
p24/crt_partial_moment_projection_scan.py
```

Because

```text
m = 66254 = 2 * 157 * 211,
```

one might hope to write the first moment `M_1` as a CRT sum of partial
moments over the three smooth factors.  The exact result is more delicate:

```text
M_1 = CRT_M_1 - m*C,
```

where `C` is a carry moment depending jointly on all three CRT components.
The naive CRT identity is false over `F_p`; the toy `m=6` run reports
`naive_crt_linear_reconstruction_ok=0` but
`carry_corrected_reconstruction_ok=1`.

This produces a new safe projection-family target:

```text
gcd(Phi_3107441, M_0, P_2, P_157, P_211) = 1 mod p,
```

where each `P_c` is the partial first moment after tracing out all complement
factors except the factor of size `c`.  The construction degrees are:

```text
n*2   = 6214882
n*157 = 487868237
n*211 = 655670051
sum   = 1149753170 = 0.001149753 * sqrt(10^24).
```

So this is the first augmentation-style target whose additional projections
are visibly aligned with the smooth embedded tower.  It still needs the
selected-prime p-unit/content proof.

The projection family now has a one-scalar packaging:

```text
L_1 = M_0 + P_2 + P_157 + P_211.
```

The principal singular modulus still has coefficient `1`, while every other
complement-coordinate coefficient is between `1` and `368`.  Hence the
characteristic-zero principal dominance argument survives with only a
`log(368)` loss.  Bounded toy scans found no `L_1` packet zeros:

```text
p24/crt_partial_moment_linear_combo_scan.py

fixed all-ones scan:
  packet_rows=516
  lambda_ones_failures=0
```

So the current sharp scalar theorem target is:

```text
Res(Phi_3107441, L_1) != 0 mod p.
```

This would imply the projection-family gcd and hence exact packet content,
while keeping all non-`M_0` construction degrees in the `n*2`, `n*157`,
`n*211` tower layers.

The character-support audit:

```text
p24/l1_character_support_audit.py
p24/l1_height_divisibility_audit.py
p24/l1_selected_origin_zero_scan.py
p24/l1_punit_boundary.md
```

adds the necessary caveat.  `L_1` is still an `H`-character eigenvector, so a
selected zero propagates through the `n*ord_n(p)` H/Frobenius conjugates.  But
it is not `K`-trivial:

```text
K-character support size = 368
K-translation orbit size = 66254
```

Thus `L_1` does not live in the clean degree-`n` quotient field of the
complement trace `M_0`.  It is a better tower-native construction target, not
a better quotient-field p-unit package.  The p-adic proof must either control
the selected embedded K-origin or prove the nonvanishing through the
intermediate `2`, `157`, and `211` layers directly.

The new height audit confirms:

```text
dominance_margin_L1=2.538350e12
packet_pdiv_log=n*ord_n_p*log_p=6.670257e13
packet_room_ratio=9.186594e10
```

So `L_1` is nonzero in characteristic zero and selected zeros still force a
large H/Frobenius p-adic divisibility block, but the archimedean room is far
too large to prove p-unitness.  The selected-origin toy scan shows the pinned
`D=-899` `M_0` failure is rescued by `L_1`, and no `L_1` selected-origin
zeros appeared in the bounded 392-row scalar window.

The exact Hermitian random-model scale is recorded in:

```text
p24/hermitian_isotropy_probability_audit.py
```

For one p24 packet the scalar is modeled by a Hermitian form on `F_{Q^2}^m`,
where

```text
Q = p^194215,
m = 66254.
```

The random failure probability is about `Q^-1`, and the audit reports:

```text
log10_zero_probability≈-4.661160e6
log10_union_bound_8_packets≈-4.661159e6
```

But this scalar still does not factor through quotient periods alone:

```text
p24/hermitian_internal_character_boundary.md
p24/hermitian_not_quotient_period_invariant_toy.py
```

The toy gives two datasets with identical quotient periods `[1,1]` and
different Hermitian packet values `96` and `88`.  So the degree-`m` quotient
period polynomial cannot determine the Hermitian certificate; nontrivial
relative `H`-character data is still required.

The characteristic-zero positivity does not by itself give the selected-prime
p-unit theorem.  The height audit

```text
p24/hermitian_energy_height_gap_audit.py
```

reports for the third target:

```text
log_one_decomposition_prime_norm_bound = 1.971942e18
one_prime_bound_over_log_p = 3.568349e16
```

so a crude archimedean norm argument cannot rule out divisibility at one
prime above `p`.

The characteristic-zero nonvanishing is nevertheless very strong.  The
principal-dominance theorem

```text
p24/hermitian_principal_dominance_theorem.md
p24/hermitian_principal_dominance_audit.py
```
shows that `P_0(a)` contains the unique principal singular modulus and that
this term dominates the rest of the fiber.  The audit reports:

```text
p0_dominance_margin=2.538350e12
log_Hermitian_embedding_lower=1.015340e13
```

Thus the only remaining issue for the Hermitian scalar is selected-prime
divisibility, not characteristic-zero vanishing.

The stronger prime-relative-normality/product theorem has now been stress
tested by selected-prime scans:

```text
p24/relative_resultant_selected_prime_scan.py
p24/relative_resultant_selected_prime_scan.md
p24/principal_fiber_punit_boundary.md
```

The first bounded run was encouraging:

```text
packet_rows=361
prime_packet_rows=204
coord_zero_packets=0
expected_prime_coord_zero_packets_random=0.517802
```

The origin-rotation symmetry is now separated in
`p24/relative_origin_shift_invariance.md`: shifting the class-cycle origin
only permutes fibers and multiplies by powers of `X`, so origin shifts do not
give independent coordinate-zero tests.  The pinned composite `n=6`
product-failure row still has coordinate-zero packets on every origin as a
consistency check.  Since p24 has prime recovery length `n=3107441`, the
selected-prime p-unit theorem

```text
Res(Phi_3107441, J_u) != 0 mod p  for all u
```

remains a clean sufficient target, although stronger than exact content and
still unproved.  Conceptually, this is the same as proving the principal
relative fiber `P_0(a)` is a p-unit at every split prime above `p`; the
principal fiber is the coordinate with the strong characteristic-zero
dominance proof, but requiring every split prime turns it into the
all-coordinate finite-field statement.

A later multi-splitting stress run found a prime-`n` coordinate failure:

```text
p24/prime_relative_normality_counterexample.md

D=-956 q=3307 ell=5 h=15 m=5 n=3 deg=1
coord_zero=1 content_zero=0 hermitian_zero=0
```

Thus prime recovery length alone cannot prove product nonvanishing.  The p24
statement

```text
Res(Phi_3107441, J_u) != 0 mod p  for all u
```

is still a valid sufficient p24-specific certificate target, but it is no
longer a plausible general theorem.  Exact content and Hermitian p-unitness
remain the better theorem targets.

The exact-content/Hermitian selected-prime follow-up is recorded in:

```text
p24/packetized_content_selected_prime_scan.py
p24/packetized_content_selected_prime_scan.md
```

On the pinned prime-`n` product counterexample

```text
D=-956 q=3307 h=15 m=5 n=3,
```

every origin has a product coordinate failure, but:

```text
content_failures=0
energy_zero_packets=0
energy_norm_zero_packets=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

A bounded multi-splitting scalar window also found:

```text
packet_rows=481
content_failures=0
hermitian_zero_packets=0
hermitian_norm_zero_packets=0
```

So the product shortcut is now separated cleanly from the two surviving
certificate targets.

The low-moment packaging route is also sharpened in:

```text
p24/moment_lambda_bad_values_scan.py
p24/moment_lambda_packaging_boundary.md
p24/lean/MomentLambdaGate.lean
```

It confirms that the pinned product counterexample has no `{M0,M1}` failure,
while fixed one-lambda projections can fail for unlucky small lambdas in toy
windows.  Therefore the robust compact target is:

```text
gcd(Phi_3107441, M0, M1) = 1 mod p,
```

with a one-resultant `M0 + lambda*M1` certificate available only after a
finite safe-lambda choice.

For construction, the tower-native variant is now preferable:

```text
L1 = M0 + P2 + P157 + P211.
```

The refreshed selected-prime scans in

```text
p24/l1_punit_boundary.md
p24/crt_partial_moment_linear_combo_scan.py
p24/l1_selected_origin_zero_scan.py
```

show:

```text
pinned D=-956 product-counterexample row:
  lambda_ones_failures=0;

broader selected-prime fixed-all-ones window:
  packet_rows=579
  family_failures=0
  lambda_ones_failures=0;

selected-origin L1 window:
  l1_zero_rows=0
  l1_selected_origin_zeros=0.
```

Thus the most constructive surviving scalar target is:

```text
Res(Phi_3107441, L1) != 0 mod p.
```

It uses only the smooth complement-factor partial moments and avoids the CRT
carry term in the literal `M1`.

The packet-factor shape is now separated in:

```text
p24/relative_packet_factor_vanishing_shape.md
p24/relative_packet_factor_shape_scan.py
```

A vanishing

```text
J_u mod f_a = 0
```

kills one Frobenius orbit of primitive relative characters.  It is not full
primitive vanishing and it does not force a constant fiber, a proper period,
or a short recurrence.  The known composite CM failures `D=-1336`,
`D=-656`, and `D=-1028` all have full/near-full Berlekamp-Massey complexity,
distinct coefficients, no proper period, and no trivial-character zero.  Thus
the proof target cannot be reduced to an elementary recurrence or
imprimitive-period exclusion.  It must use arithmetic p-unitness or
selected-prime CM anti-concentration.

## Closed Correspondence Zero-Lemma Shortcut

A conditional finite-field zero-lemma route would have worked if the
order-`3107441` recovery class had a correspondence representative of degree
below

```text
m = 66254.
```

The known class

```text
2 * 463 * 223^(-1)
```

has the right order but `X0` index

```text
311808 = 4.706252 * m.
```

The audit

```text
p24/low_norm_order3107441_search.md
```

then checked that this is not a squarefree-search artifact: using all split
rational primes up to `66254`, there is no signed split-prime-power ideal
word of norm at most `66254` with class index `66254`; including the ramified
prime `599` still gives no hit.

So the divisor-counting zero-lemma route is closed for ordinary split
correspondence representatives.  A future positive result would need either a
nonstandard lower-pole representative of the same class, the Hermitian p-unit
theorem, or the exact relative-content certificate.

The Atkin-Lehner near miss is also recorded in:

```text
p24/atkin_zero_window_boundary.md
```

Even granting the full quotient by the Atkin-Lehner group, the best tested
index-314 layer has `delta_AL=339 > 314`; index `422` and the desired
`66254` layer are farther away or absent.

## Positive Tower Target

The best constructive theorem target remains the embedded third-trace tower.
The first non-genus obligation is now isolated in:

```text
p24/degree157_refinement_target.md
```

It asks for an embedded degree-`157` child relation over the genus layer:

```text
G / <g^2>          degree 2
G / <g^(2*157)>    degree 314
relative degree    157
```

The root-of-unity extension is cheap:

```text
ord_157(p) = 156.
```

The missing part is the embedded pairing to the `j`-torsor, i.e. computing the
nontrivial relative traces for this unramified non-genus layer without class
enumeration.

For p24, this scalar target halves the extension degree of each packet:

```text
p^(388430/2) == -1 mod 3107441,
E_a = E_-a,
energy packet degree = 194215.
```

There are still eight packets; the sign identification is already inside each
Frobenius orbit.

The packet-norm reformulation packages these eight checks into a degree-8
decomposition-field p-unit statement.  Let

```text
E^+ = Q(zeta_n + zeta_n^-1),
M^+ = (E^+)^<p>.
```

For p24,

```text
[E^+ : M^+] = 194215,
[M^+ : Q]   = 8.
```

If

```text
Xi_E = Norm_{E^+/M^+}(E_1),
```

then the eight finite-field packet norms are the residues of `Xi_E` at the
eight primes of `M^+` above `p`.  Thus the scalar energy certificate is
equivalent to proving

```text
p does not divide Norm_{M^+/Q}(Xi_E).
```

This sharper target is recorded in:

```text
p24/decomposition_field_packet_norm_theorem.md
p24/cyclotomic_packet_norm_toy.py
```

The ordinary-energy scalar has now also been checked in characteristic zero:

```text
p24/ordinary_energy_principal_dominance_audit.py
```

Its `C_0` term contains `j_0^2`, which dominates every shifted
autocorrelation term.  So ordinary energy is not demoted because of complex
cancellation; it is demoted because small finite-field packets show full-orbit
p-adic cancellation.  The packet scalar divisor-shape audit also shows the
contrast: ordinary packet norms are shift-invariant constants on the CM torsor,
while Hermitian packet norms behave generically as functions of selected `j`.

The scan

```text
p24/relative_energy_certificate_scan.py
```

checks the autocorrelation and Parseval identities on small natural CM cycles.
A 100-case run found:

```text
quotient_rows=317
characters_tested=1268
harmful_total=0
energy_zero_total=0
expected_random_energy_zeros=0.576654
```

This is supportive, but not a proof; the main value is the scalar theorem
target.

The recurrence-compression version of this idea is checked in:

```text
p24/relative_energy_recurrence_boundary.md
p24/relative_autocorrelation_complexity_scan.py
```

The toy autocorrelation sequences have full DFT support in the tested rows and
mostly full Berlekamp-Massey complexity, so no bounded recurrence shortcut is
visible.

The ordinary Hecke-moment version is recorded in:

```text
p24/hecke_autocorrelation_boundary.md
p24/hecke_autocorrelation_toy.py
p24/agent_brandt_energy_sidecar.md
p24/agent_brandt_energy_probe.py
```

Unoriented Hecke walk moments determine the product autocorrelations by a
triangular/Chebyshev inversion, but this still requires recovery-scale
moments to evaluate high-order energy packets.  The exact Brandt bookkeeping
identity

```text
C_d = Tr(J * P_{m*d} * J * P_{-m*d})
```

is true, but assumes the oriented class-action permutation `P_{m*d}` is
already available.  Ordinary Brandt/Hecke matrices and plain modular
resultants compute orientation packets, not the p24 singleton class
`2*463*223^(-1)` and its order-`3107441` powers.

## Why The Divisor Route Does Not Close

James's Riemann-Roch sidecar gives a correct conditional theorem:

```text
if a nonzero modular function F_a with pole degree < m evaluates to P_u(a)
at the m quotient CM points, then harmful vanishing is impossible.
```

The obstruction is the degree of the natural representative:

```text
zeros needed:       m = 66254
natural pole scale: n = 3107441
```

Constructing a low-pole representative would itself be the missing embedded
non-genus relative-period primitive.

## Why Statistics Do Not Close

Socrates's content sidecar identifies the same exact invariant:

```text
C_a(X) = gcd(f_a, J_0, ..., J_{m-1}).
```

Random models make harmful vanishing astronomically unlikely, and small CM
data shows no high-order natural failures.  But artificial vectors and small
low-order CM failures prove the statement cannot be pure linear algebra or
pure split ordinary CM structure.

The finite-field/coding side-agent sharpened this boundary: cyclic-code
minimum-weight theorems fail in artificial examples, and small ordinary CM
reduced-normality failures such as `D=-216` and `D=-300` show that split CM
alone does not imply unit resolvents.  Therefore any usable theorem must use
the p24 selected-prime, high-order non-genus arithmetic, or directly prove
the packet norm/content unit statement.

The missing arithmetic input is therefore:

```text
prove a p-adic unit/noncontainment statement for the relative content ideal
of the selected p24 singular modulus.
```

Stronger reduced normality of the selected singular modulus would imply it,
but known tools prove only characteristic-zero nonvanishing, not unit status
at this particular split prime.

Carver's trace-formula sidecar sharpened the literature boundary:

```text
p24/agent_traceformula_energy_sidecar.md
```

Known Zagier/Bruinier-Funke/Choi trace formulas handle global or
genus-character traces; Gross-Zagier/Schofer/Borcherds/Lauter-Viray product
formulas handle symmetric norms or valuations; relative trace formula methods
give complex toric-period identities.  None supplies a selected-prime
`p`-adic unit certificate for the order-`3107441` non-genus energy.

The Hermitian follow-up sharpens the only visible product-formula route:

```text
p24/agent_hermitian_punit_followup.md
```

One would need a phase-aware Borcherds product `Psi_a` whose CM value is the
degree-8 Hermitian packet norm `Xi_a` up to p-units, with principal part chosen
so the Schofer/Lauter-Viray local term at the selected ordinary split prime
`p` is zero.  If such a divisor were explicit, the local valuation formula
would prove `Xi_a` is a p-unit.  The obstruction is that known product formulas
do not construct the order-`3107441` phase-aware divisor; symmetric norms
discard exactly the packet phase needed here.

The divisor-shape diagnostic

```text
p24/packet_scalar_divisor_shape_toy.py
p24/packet_scalar_divisor_shape_boundary.md
```

adds a finite-field warning: on the `D=-5000` and `D=-2239` toy torsors,
Hermitian packet norms have generic polynomial/rational interpolation degree
as functions of the selected `j`, while ordinary autocorrelation packet norms
are degree-0 constants because they are shift-invariant.  Thus the Hermitian
scalar is empirically stronger but not a simple one-variable modular function;
a product-formula proof would need an explicitly phase-aware divisor.

## Current Route Assessment

The theorem has become narrower:

```text
prove eight relative content gcds are 1,
or prove the degree-8 decomposition-field ordinary-energy packet norm is a p-unit,
or, preferably, prove the degree-8 decomposition-field Hermitian-energy
packet norm is a p-unit.
```

This is a real improvement over full class enumeration, but no sub-sqrt
certificate follows yet.  The live positive route would be a new explicit
phase-aware trace formula, relative trace formula, or p-adic unit theorem for
these high-order non-genus relative periods.

## First Odd Layer Calibration

The first odd non-genus layer can be isolated in two useful ways.

The tower version asks for the relative degree-`157` child polynomial above the
degree-`2` genus parent:

```text
G / <g^2>             degree 2
G / <g^(2*157)>       degree 314
relative degree       157
```

The direct split-prime version uses `ell=2897`:

```text
order([2897]) = 1311340102
index([2897]) = 157
Gamma0(2897) degree proxy = 2898
```

The direct version is a clean first-odd-layer theorem toy, but not the best
certificate route:

```text
seeded proxy = 2898 * 1311340102 = 3800263615596
              = 3.800264 * sqrt(p)
```

The balanced oriented composite target remains better:

```text
quotient degree = 66254
recovery degree = 3107441
seeded proxy = 968924963328 = 0.968925 * sqrt(p)
```

Small tower analogues support the exact missing primitive.  For
`D=-5000, q=1259, h=30=2*3*5`, the degree-`3` child relation above the genus
parent exists and is tiny once the embedded `j`-cycle is known.  Its Fourier
side is exactly the relative class-character trace on the odd quotient.  But
the relation is built from the embedded cycle; abstract tower degrees alone do
not produce it.

The non-genus `D=-2239, q=2243, h=35` control shows that an abstract degree-5
quotient and the embedded period quotient can both split over the same finite
field while having no affine or Mobius set pairing.  Thus the missing p24
theorem cannot be replaced by a bare abstract class-field quotient.

The follow-up graph-relation scan

```text
p24/abstract_embedded_graph_relation_scan.py
```

shows the next boundary: bidegree `(1,1)` relations do not pair the degree-5
toy roots, while `(1,2)` and `(2,1)` relations pair every matching even for
random root sets.  Thus plain low-bidegree existence above the interpolation
threshold is not meaningful; a successful p24 tower theorem needs a relation
below threshold, a canonical coefficient constraint, or a modular construction
that fixes the pairing.

The Gaussian-period multiplication-table variant is also now tested:

```text
p24/period_multiplication_table_scan.py
p24/period_multiplication_table_boundary.md
```

In the `D=-5000` and `D=-2239` quotient-period toys, the normal-basis
multiplication constants are dense and match random controls; there is no
visible sparse cyclotomic-number-style table that would compute the child
polynomial from cheap universal constants.

The comparison is recorded in:

```text
p24/direct_degree157_quotient_target.md
```

The sharper fixed-instance intermediate target is the `ell=677` component
quotient:

```text
order([677]) = 655670051 = 211 * 3107441
index([677]) = 314 = 2 * 157
Gamma0(677) proxy = 678
seeded proxy = 444544294578 = 0.444544 * sqrt(p)
```

This would already give a sub-sqrt p24 route if the 314 component sums of the
horizontal 677-isogeny graph could be constructed without the CM vertices.  It
is exactly the genus-plus-157 quotient `G/<g^314>`, so it is equivalent to the
first odd embedded tower theorem rather than a separate shortcut.

Details are recorded in:

```text
p24/ell677_component_quotient_boundary.md
```

The fixed-trace Montgomery gate has been sharpened in:

```text
p24/conductor2_nonsplit_gate.md
p24/conductor2_component_transfer_boundary.md
```

For strict traces with `t^2-4p=4D_K` and `D_K == 1 mod 8`, maximal-order
roots give split Montgomery parameters, while conductor-2/Frobenius-order
roots give nonsplit Montgomery parameters.  The p24 ring-class map
`Pic(Z+2O_K) -> Pic(O_K)` is an isomorphism, so this does not change the
`ell=677` class orders or quotient degrees.  It does clarify the final target:
construct the embedded component sums on the conductor-2/nonsplit branch, or
produce a fixed-trace root and explicitly pass the nonsplit/x-only gate.
Small scans show the descending `2`-isogeny transports odd-prime components
equivariantly but does not collapse the component-sum quotient; the
conductor-2 sums are different embedded period values, so this branch
correction does not itself provide the class-selector.

## Quotient-Factored Support Gate

The relative-content packet theorem is exactly sufficient for constructions
that have already descended to the quotient spectrum.  In finite Fourier
language, if an additive selector `A` satisfies:

```text
A * J = e_H * J
A and e_H are supported only on Q_H
J(zeta^s) != 0 for every s in Q_H
```

then cancellation on `Q_H` gives `A=e_H`.  This support gate is checked in:

```text
p24/lean/QuotientSupport.lean
```

and tested in:

```text
p24/quotient_spectrum_support_toy.py
```

The latest bounded toy run reported:

```text
rows=1600
nonquotient_factor_rows=1205
nonquotient_reduced_rows=0
quotient_factor_rows=395
quotient_reduced_rows=0
```

This does not prove the p24 certificate, but it cleanly separates the final
obligations:

```text
quotient-factored construction:
  prove the 28 Frobenius quotient packets are nonzero;

arbitrary sparse Hecke/projector construction:
  also prove the cyclic-code coset e_H + Ann(J) has no support < n,
  or prove the formula is supported on the quotient spectrum.
```

## Local Phase-Aware Boundary

The simplest finite-field identity shapes have now been tested negatively:

```text
p24/l1_interpolation_shape_boundary.md
p24/packet_scalar_divisor_shape_boundary.md
p24/packet_scalar_edge_shape_boundary.md
```

The first two show that `L1` and Hermitian packet norms behave generically as
plain one-variable functions of the selected `j` root.  The edge-shape scan
then tests the next local phase-aware coordinate, `(j_i,j_{i+1})`, and again
finds no below-interpolation bidegree relation for `L1` or Hermitian in the
small composite windows.

Thus the missing identity, if it exists, must involve longer/high-order phase
data rather than a bounded `j` or oriented-edge coordinate.  This keeps the
surviving theorem target focused on selected-prime p-unitness, phase-aware
Borcherds/Schofer input, or an embedded class-field tower relation that
actually applies the non-genus relative character projection.

The closest Atkin-Lehner zero-lemma miss has also been sharpened in:

```text
p24/ell677_linear_pole_boundary.md
```

For the `ell=677` first odd layer, the proxy `339=(677+1)/2` is not a usable
pole degree for the linear endpoint character traces that harmful content
collapse actually forces.  The best descended endpoint-linear pole degree is
`677`, while the zero-lemma window needs `<314`.

The finite-algebra toy

```text
p24/nonlinear_function_not_forced_toy.py
```

records why lower-degree nonlinear modular functions on `X0(677)^+` do not
automatically help: a character component can vanish for `j` but not for
`j^2`.  Any use of such a function would therefore be a new phase theorem,
not a formal consequence of relative-content collapse.

The packet-field rank diagnostic is recorded in:

```text
p24/hermitian_packet_rank_boundary.md
```

Small CM Hermitian packet vectors have maximal possible base-field span, but
the isotropy toy has a full-span vector with zero Hermitian energy.  Thus
rank/maximal-span alone cannot prove the selected-prime Hermitian p-unit
statement.

For `L1`, the analogous rank packaging is the `368`-dimensional axis support
of its `K`-character transform.  Proving this translate span has full rank
would only show that the translate family is not identically zero; it would
not prove that the selected `K` origin is nonzero.  That final step is still
selected-origin p-unitness/hyperplane avoidance.
## Subspace-Polynomial Restatement

The trace-dual/Lang-normality target has a canonical rank-metric packaging.
Let

```text
C = { Tr_{E/L}(delta_i * S_j) : 1 <= i <= 35, 1 <= j <= 6 }
    subset L = F_p(mu_157).
```

Let `A_C(X)` be the monic `p`-linearized subspace polynomial of the
`F_p`-span of `C`.  Then

```text
pdeg A_C = dim_Fp span(C).
```

Thus the p24 mixed Schur theorem is equivalent to the identity

```text
A_C(X) = X^(p^156) - X.
```

Equivalently, no nonzero `p`-linearized polynomial of `p`-degree `<156`
annihilates all `210` relative-trace coordinates.  This is recorded in:

```text
p24/hermitian_mixed_subspace_polynomial_certificate.md
p24/hermitian_mixed_subspace_polynomial_toy.py
p24/lean/MixedSubspacePolynomialGate.lean
```

This restatement may be more proof-friendly than selecting a coordinate
Moore minor: it is invariant under `F_p`-basis changes in `L` and turns the
missing theorem into one canonical class-field finite-field identity.

## Centered Right-Profile Restatement

The trace-dual coordinate set can be replaced by a centered right profile.
Let `M(r,s)` be the Hermitian double marginal for the mixed `157 x 211`
components and set:

```text
G_s = sum_{r mod 157} zeta_157^r M(r,s) in L=F_p(mu_157),
G_s^0 = G_s - average_t(G_t).
```

The nonzero right DFT periods `S_v=H_{157,211}(1,v)` are the Fourier
transform of the profile `G_s` with the `v=0` component omitted, so they are
equivalent to the centered profile.  Therefore the missing p24 theorem can be
stated as:

```text
span_Fp{G_s^0 : s mod 211} = F_p(mu_157).
```

This is recorded in:

```text
p24/hermitian_mixed_centered_right_profile_theorem.md
```

and audited by the centered-profile rank diagnostics in:

```text
p24/hermitian_mixed_left_subfield_normality_audit.py
```

Pinned actual-CM rows have zero centered-profile rank mismatches.  This is
currently the most economical class-field-facing formulation of the mixed
Schur theorem.

Because `p` is primitive modulo `157`, this profile statement is equivalent
to a purely base-field centered-marginal rank theorem.  With

```text
C(r,s)=M(r,s)-M(r,0)-M(0,s)+M(0,0),
1 <= r < 157, 1 <= s < 211,
```

the missing theorem is:

```text
rank_Fp C = 156.
```

Thus the mixed Schur correction can be certified by a p-unit maximal minor of
one `156 x 210` base-field matrix.  The centered-profile/subspace-polynomial
forms are equivalent packaging for finding or proving such a p-unit.

A stronger possible theorem is that every nonzero left twist has right-orbit
support at least `2`:

```text
#{j : Tr_{E/R}(lambda*S_j) != 0} >= 2.
```

This would imply that any five of the six right orbit packets already
separate `L`.  The toy support/delete-one audit is recorded in:

```text
p24/hermitian_mixed_right_orbit_support_theorem.md
p24/hermitian_mixed_orbit_support_toy.py
```
