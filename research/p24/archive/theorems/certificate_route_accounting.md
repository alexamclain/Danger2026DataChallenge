# p24 Certificate Route Accounting

Date: 2026-06-05

This note compares the three current finite certificate surfaces.

Tool:

```text
p24/certificate_route_accounting.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/certificate_route_accounting.py
```

## Shared Scale

```text
p = 10^24 + 7
sqrt_floor = 1000000000000
h = 205880396014
m = 66254
n = 3107441
m+n = 3173695
(m+n)/sqrt(p) = 3.173695e-6
```

## Trace-GCD Right Resultant

Finite verifier:

```text
right = 211
ord_211(p) = 35
tail_window = 16
finite_value_count = 211
orbit_product_count = 7
verifier_values/sqrt(p) = 2.11e-10
```

But the generic Pluecker expansion has:

```text
binom(35,16) = 4059928950
generic exterior support = 211.
```

Conclusion:

```text
smallest verifier,
hardest embedded producer.
```

It needs the actual `Delta_t` values, Pluecker coefficients, or a direct
p-unit theorem for the cyclic resultant.

## L1 Partial-Moment Resultant

Finite/construction shape:

```text
packet_degree = ord_3107441(p) = 388430
axis_dim = 368
partial_degrees = [6214882, 487868237, 655670051]
n plus partial layers = 1152860611
visible_degree/sqrt(p) = 1.152860611e-3
packet_degree/axis_dim = 1055.516
```

Conclusion:

```text
best visible tower construction,
but still has selected-origin p-unit gap.
```

It needs a theorem proving:

```text
Res(Phi_3107441, L_1) != 0 mod p
```

or the stronger axis-injectivity theorem for the 368-dimensional
axis-supported coefficient space in every degree-388430 packet.

The current best version of that stronger theorem is the annihilator form:

```text
gcd(Ann_a, Phi_1 Phi_2 Phi_157 Phi_211) = 1
```

for every H-packet `a`, where `Ann_a` records the K-character factors killed
by the selected packet vector.  See:

```text
p24/l1_axis_annihilator_theorem.md
```

### Trace-Frame Selected Plucker Refinement

The current best finite surface inside the `L1` route is:

```text
p24/trace_frame_selected_plucker_certificate.md
p24/trace_frame_selected_plucker_accounting.py
```

It tensors a degree-388430 H-packet with:

```text
E = F_p(mu_m),       [E:F_p] = ord_m(p) = 5460.
```

The packet splits into:

```text
70 tensor factors, each of degree 5549 over E.
```

Using the degree-179 subfield of one factor, the selected trace-frame target
has dimension:

```text
3*179 = 537.
```

The axis dimension remains:

```text
368.
```

So the coordinate-free certificate is:

```text
Omega_top3 in Exterior_E^368(C^3),   Omega_top3 != 0.
```

A finite verifier can name one Plucker coordinate:

```text
delta_I != 0 in E,    |I|=368.
```

There are:

```text
binom(537,368) ~= 10^143.820126
```

possible coordinates, so the coordinate `I` is part of the certificate or
must come from a class-field identity.  This is now the smallest `L1` axis
verifier surface: one named Plucker coordinate per H-packet, rather than a
raw degree-388430 packet-rank certificate.

The leading-prefix refinement in:

```text
p24/trace_frame_leading_plucker_pivot_theorem.md
p24/trace_frame_plucker_pivot_audit.py
```

now gives a canonical coordinate candidate:

```text
I_lead = first 368 coordinates of C^3 = 179 + 179 + 10.
```

So the current `L1` theorem target is no longer an arbitrary selected
coordinate but:

```text
delta_lead != 0 in E
```

for each of the eight H-packets, or a degree-8 decomposition-field product of
the eight leading coordinates.

For the factorized Schubert version, the degree-8 product is naturally
relative over `K_m=Q(mu_m)`: the four elements

```text
Xi_A, Xi_B, Xi_AB, Xi_tail in K_m Q(zeta_n)^<p>
```

have residues in `E=F_p(mu_m)`, one per H-packet.  Nonzero relative norms to
`K_m` compress the H-packet direction:

```text
32 packetwise Schubert p-units
  -> 4 relative degree-8 p-units     (with tensor-factor symmetry)
2240 local tensor-factor p-units
  -> 280 relative degree-8 p-units   (without tensor-factor symmetry)
```

See:

```text
p24/trace_frame_schubert_packet_norm.md
p24/trace_frame_schubert_equivariant_descent.md
p24/lean/SchubertEquivariantDescentGate.lean
p24/lean/TraceFrameSchubertPacketNormGate.lean
```

The beta-product/crossed-product refinement now has the same indexing as this
tensor split:

```text
560 nonzero beta orbits = 8 H-packets * 70 tensor factors.
```

See:

```text
p24/beta_orbit_tensor_factor_bridge.md
p24/trace_frame_lead_crossed_product_norm.md
```

This sharpens the stronger p-unit theorem to nonvanishing of the named
crossed-product reduced norms in the scalar-extension factors, rather than an
unstructured product over `n=3107441` beta shifts.

The leading-coordinate p-unit can now be read in the factorized Schubert form:

```text
p24/trace_frame_single_leading_punit.md
p24/trace_frame_factorized_schubert_punit.md
p24/trace_frame_factorized_schubert_certificate_spec.md
```

The denominator-free version is the single leading Plucker determinant
`Delta_lead`; its nonvanishing alone implies the leading trace-frame map is
injective.  The factorized explanation is `rank Top_2(W)=358` plus injectivity
of the 10-coordinate residual tail on `K_2=ker(Top_2|W)`.  This is the
smallest named trace-frame proof surface that still sees the cross-block
obstruction.

The leading crossed-product norm note shows that this determinant can be
tested/proved orbitwise:

```text
D_0 * product_{560 nonzero Omega} R_lead,Omega,
```

where the nonzero factors are the same `8*70` scalar-extension orbit factors.
Thus the current theorem target is no longer a raw beta product and no longer
a packetwise pivot product; it is p-unitness of fixed determinant-line reduced
norms.

The explicit matrix-entry verifier surface for the factorized Schubert route
is still sub-sqrt even after expanding `E=F_p(mu_m)` entries into base-field
slots:

```text
single leading Plucker, one tensor factor, all 8 H-packets:
  1083392 E-entries
  5915320320 F_p slots
  5.91532032e-3 * sqrt(p)

one tensor factor, all 8 H-packets:
  873312 E-entries
  4768283520 F_p slots
  4.76828352e-3 * sqrt(p)

all 70 tensor factors, all 8 H-packets:
  333779846400 F_p slots
  0.3337798464 * sqrt(p)
```

### Selected Toeplitz Symbol Surface

The Toeplitz/translate-minor normal form gives a smaller selected-origin
verifier surface for the same leading coordinate.  Instead of carrying the
raw:

```text
368 x 368 = 135424 E-entries
```

matrix for one H-packet/tensor factor, a verifier can reconstruct it from the
cyclic `m`-symbol:

```text
m = 66254 E-entries.
```

The accounting is:

```text
one factor, all 8 H-packets: 2893974720 Fp slots
  = 2.89397472e-3 * sqrt(p)

all 70 tensor factors: 202578230400 Fp slots
  = 0.2025782304 * sqrt(p)
```

This is about half the raw single-leading matrix surface, but it applies to
the selected-origin verifier only.  Literal beta-orbit symbols over
`A_Omega/E` would cost:

```text
66254 * 5549 = 367643446 E-entries per nonzero orbit
Fp_slots_per_nonzero_orbit = 2.00733321516 * sqrt(p)
all_nonzero_orbits = 1124.1066004896 * sqrt(p).
```

Therefore beta-orbit coverage must remain theorem-level or norm-compressed,
not a literal table of orbit-algebra symbols.  The explicit spec and audit
are:

```text
p24/trace_frame_selected_minor_certificate_spec.md
p24/trace_frame_selected_minor_certificate_accounting.py
```

A literal full beta-algebra inverse witness is also too large:

```text
n * 5549 = 17243190109 E-entries
94147817995140 Fp slots
  = 94.14781799514 * sqrt(p)
```

before duplicating across tensor-factor representatives.  This is now audited
in:

```text
p24/trace_frame_beta_inverse_witness_audit.py
```

If a class-field or determinant-line theorem supplies the reduced norms
directly, the norm payload is tiny:

```text
all 560 nonzero orbit norm values plus inverses:
  6115200 Fp slots
  = 6.1152e-6 * sqrt(p)

70 degree-8 relative values plus inverses:
  764400 Fp slots
  = 7.644e-7 * sqrt(p)

one symmetry-compressed degree-8 value plus inverse:
  10920 Fp slots
  = 1.092e-8 * sqrt(p)
```

These are verifier payload counts only; the theorem still has to prove that
the named scalars are the actual reduced norms of the selected leading
determinants.

The resulting positive certificate spec is:

```text
p24/trace_frame_norm_compressed_certificate_spec.md
p24/trace_frame_fitting_norm_status.md
p24/lean/TraceFrameNormCompressedCertificateGate.lean
```

The CRT-axis support expansion is now sharpened in:

```text
p24/axis_crt_fourier_support_boundary.md
p24/axis_crt_matrix_tree_factorization_boundary.md
```

It proves useful structure but also rules out the simplest matrix-tree
shortcut.  The nonzero Cauchy-Binet terms are CRT-axis hypertrees, yet the
actual weights violate the pair-sum identities required by any ordinary
per-edge factorization `c(B)=C*prod_{e in B}a_e`.  Therefore the missing
arithmetic input is still a Plucker-weighted p-unit theorem, not a standard
Laplacian tree polynomial evaluation.

## First-Trace Order-19 Quotient

The first strict trace gives the smallest visible non-genus quotient layer:

```text
t = 1020608380936
h = 278733727154 = 2 * 19 * 7335098083
ell = 19
index = 19
recovery degree = 14670196166
```

Finite payload:

```text
degree-19 quotient polynomial
one selected degree-14670196166 recovery polynomial
total non-leading coefficients = 14670196185
payload/sqrt(p) = 0.014670196185
```

This is worse than the third-trace decomposed tower by about four orders of
magnitude, but it still beats the p24 sqrt yardstick and is the cleanest
single-layer theorem experiment.  The finite implication is checked by:

```text
p24/first_trace_order19_certificate_spec.md
p24/lean/QuotientRecoveryCertificateGate.lean
```

The missing producer theorem is exactly the embedded non-genus phase problem:
construct the order-19 quotient root and the paired selected recovery fiber
for the actual conductor-2 CM torsor without enumerating the class set.

## Centered Difference Minor

Finite verifier:

```text
base matrix = 156 x 210
leading minor = 156 x 156
determinant_entries = 24336
entries/sqrt(p) = 2.4336e-8
origin_product_right_values = 211
```

Conclusion:

```text
cleanest base-field sufficient determinant,
but no embedded producer.
```

It needs a theorem proving the actual leading `156 x 156` centered
difference minor is a p-unit, or its 211 right-origin product is a p-unit.

## Current Choice

The route with the best chance of becoming a full sub-sqrt construction is
`L_1`, because its inputs are already decomposed into the `2`, `157`, and
`211` tower layers and the visible degree is about `0.00115 sqrt(p)`.

The route with the best finite verifier is trace-gcd, because the final check
is only a `211`-value/inverse certificate.  It is the best target if an
embedded formula for `A=T_i|K_0` or the Pluecker-Fourier coefficients is
found.

The centered difference minor should remain the fallback sufficient theorem:
it is the simplest base-field determinant statement, but it currently has the
least visible construction path.

## Phase-Lifted Decomposed Tower Surface

The pure decomposed-CM `j`-producer surface is now made explicit in:

```text
p24/phase_lifted_tower_certificate_spec.md
p24/phase_lifted_tower_certificate_toy.py
```

It uses:

```text
top polynomial degree 2;
relative relation degree 157 over 2 parents;
relative relation degree 211 over 314 parents;
one selected recovery polynomial degree 3107441.
```

The field-coefficient count, excluding monic leading coefficients, is:

```text
2 + 2*157 + 314*211 + 3107441 = 3174011
```

and therefore:

```text
3174011 / sqrt(p) = 3.174011e-6.
```

This is the cleanest finite artifact if an embedded class-field producer
theorem is found.  Its advantage over the older complement-trace relation is
that it carries one selected recovery polynomial instead of a dense `h`-slot
bivariate recovery table.  Its disadvantage is exactly the unresolved
arithmetic producer: the `157` and `211` relative phase relations and the
selected recovery polynomial must be paired to the embedded conductor-2
`j`-torsor without class-set enumeration.

If the arithmetic theorem is already phase-selective, the certificate can use
only the two selected child polynomials instead of full parent-relative
relations:

```text
2 + 157 + 211 + 3107441 = 3107811
3107811 / sqrt(p) = 3.107811e-6.
```

This is the smaller selected-chain surface represented by the Lean gate
`p24/lean/PhaseLiftedTowerGate.lean`.

## Post-Root Tail

Once any route supplies a strict target-trace Montgomery parameter `A`, the
remaining DANGER3 `x0` construction is not the asymptotic bottleneck.  For the
third trace:

```text
p + 1 - (-1178414874616)
  = 2^41 * 454747350887
verifier depth = 40
```

So the verifier point can be found by x-only projection by the odd part and
exact-depth trimming.  This is recorded in:

```text
p24/post_cm_root_projection_boundary.md
p24/post_cm_root_projection_toy.py
```

Therefore all three certificate surfaces above should be read as unmarked
CM-root / target-`A` producers.  Marking the `2^40` ray inside the class-field
construction would reintroduce the large `X1` orientation cover.
