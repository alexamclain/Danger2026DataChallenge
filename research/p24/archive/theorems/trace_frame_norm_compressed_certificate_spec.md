# Trace-Frame Norm-Compressed Certificate Spec

Date: 2026-06-05

This note states the smallest surviving certificate surface for the
trace-frame `L1` route.  It is the positive counterpart to the boundaries:

```text
literal orbit-algebra symbols are too large;
literal full beta-algebra inverses are too large;
ordinary coordinate Plucker products look generic;
plain-j and single-edge divisor explanations fail in small rows.
```

## p24 Constants

```text
p = 10^24 + 7
t = -1178414874616
h = 205880396014 = m*n
m = 66254 = 2*157*211
n = 3107441
ord_m(p) = 5460
ord_n(p) = 388430
gcd(ord_m(p), ord_n(p)) = 70
ord_n(p^5460) = 5549
H-packets = 8
nonzero beta orbits = 560 = 8*70
```

The trace-frame determinant uses:

```text
E = F_p(mu_m),             [E:F_p] = 5460
B/E degree = 5549
C/E degree = 179
dim_E W_axis = 368
I_lead = first 179 + first 179 + first 10 coordinates of C^3.
```

## Certificate Payload

With tensor-factor determinant-line equivariance, the finite payload for the
p-unit part can be:

```text
N_lead in E,
U_lead in E,
```

with verifier check:

```text
N_lead * U_lead = 1 in E.
```

Expanded into base-field slots this is:

```text
2 E-entries = 10920 Fp slots = 1.092e-8 * sqrt(p).
```

Without tensor-factor equivariance, carry `70` degree-8 norm values and
inverses:

```text
140 E-entries = 764400 Fp slots = 7.644e-7 * sqrt(p).
```

If only orbitwise reduced norms are available, carry all `560` nonzero orbit
norm values and inverses:

```text
1120 E-entries = 6115200 Fp slots = 6.1152e-6 * sqrt(p).
```

All three are far below `sqrt(p)`.  They differ only in how much arithmetic
descent/equivariance has been proved.

## Producer Soundness Theorem

The scalar payload is meaningful only with a producer theorem.  The strongest
form is:

```text
There exists a p-integral determinant-line section
  Xi_lead in K_m Q(zeta_n)^<p>
whose eight residues above p are p-unit multiples of the selected
leading trace-frame determinants in one scalar-extension tensor factor.

N_lead == Norm_{K_m Q(zeta_n)^<p> / K_m}(Xi_lead) mod p.
```

Together with tensor-factor equivariance:

```text
Delta_lead(packet, factor')
  = unit * sigma(Delta_lead(packet, factor))
```

this implies all `8*70` packet/factor leading determinants are nonzero.

The equivalent full beta-algebra statement is:

```text
A_all = O_E[Y]/(Y^n - 1)
delta_all = det(T_lead,all) in A_all
delta_all in A_all^*
Norm_{A_all/O_E}(delta_all)
  = D_0 * product_{Omega != 0} R_lead,Omega.
```

The p24 proof must supply the equality between the small scalar payload and
the actual determinant-line/reduced-norm object.  The finite verifier cannot
discover that equality from the two `E`-entries alone.

If the arithmetic proof produces the full beta-algebra norm directly, the
finite endpoint is even cleaner:

```text
G_all = Norm_{A_all/O_E}(delta_all)
G_all * U_all = 1 in E
=> no harmful beta orbit, including the zero orbit.
```

`TraceFrameBetaResultantGate.lean` records this as
`no_harmful_from_global_reduced_norm_inverse_payload`.  This scalar payload is
sub-sqrt; it is not the dense literal inverse polynomial in `B[Y]/(Y^n-1)`.
The scalar should still be regarded as an `E`-element: a direct pinned-row
probe found that the full beta product did not descend to the base field in
any of the `12` `D=-10919, m=12` full/tail rows tested.

## Lean Gates

The new integrated gate is:

```text
p24/lean/TraceFrameNormCompressedCertificateGate.lean
```

It checks the abstract finite implication:

```text
degree-8 norm nonzero
  => all representative packet determinants nonzero
  => tensor-factor equivariance makes every factor determinant nonzero
  => beta-orbit/tensor-factor coverage makes every beta orbit good
  => every covered harmful beta orbit is excluded.
```

2026-06-08 update: the same gate now also records the verifier-side inverse
payload:

```text
N_lead * U_lead = 1 in E
  => N_lead != 0
  => all nonzero beta orbits are good
  => no harmful nonzero beta orbit,
```

abstracted as `all_beta_orbits_good_from_degree8_inverse_payload` and
`no_harmful_beta_orbits_from_degree8_inverse_payload`.  It also pins the p24
scale checks:

```text
560 = 8*70,
179+179+10 = 368,
2 E-entries = 10920 Fp slots < sqrt(p),
4 E-entries = 21840 Fp slots < sqrt(p),
1120 E-entries = 6115200 Fp slots < sqrt(p)
```

2026-06-08 guardrail: `no_harmful_all_beta_orbits_from_zero_gate_and_nonzero_inverse_payload`
now records the honest full-beta composition.  The degree-8 inverse payload is
used only on the `560` nonzero beta/tensor-factor orbits; the beta-zero orbit
must still be supplied by a separate `D_0` no-harmful/p-unit gate.

The same Lean gate now gives the four-element endpoint as
`no_harmful_all_beta_orbits_from_four_element_payload`:

```text
D_0 * U_0 = 1 in E
N_lead * U_lead = 1 in E
zero-harmful => D_0 = 0
nonzero determinant-line hypotheses for N_lead
=> no harmful beta orbit in {zero orbit} union {560 nonzero orbits}.
```

The supporting gates are:

```text
p24/lean/TraceFrameLeadingNormGate.lean
p24/lean/TraceFrameDenominatorSafeLeadGate.lean
p24/lean/TraceFrameTensorFactorEquivarianceGate.lean
p24/lean/TraceFrameBetaResultantGate.lean
p24/lean/BetaOrbitTensorFactorBridge.lean
p24/lean/TraceFrameAnnihilatorGate.lean
p24/lean/TraceFrameGate.lean
```

Lean does not prove the class-field p-unit theorem.  It prevents the finite
certificate logic from smuggling in a stronger or differently indexed claim.

## Why This Is The Surviving Surface

Rejected table surfaces:

```text
selected-origin Toeplitz symbol for all 70 factors:
  0.2025782304 * sqrt(p)      (sub-sqrt, but still table-like)

literal symbol over one nonzero beta-orbit algebra:
  2.00733321516 * sqrt(p)     (too large)

literal full beta inverse in B[Y]/(Y^n-1):
  94.14781799514 * sqrt(p)    (too large)
```

Rejected proof shortcuts:

```text
ordinary Fourier/Chebotarev uncertainty;
full reduced normality;
generic Toeplitz nonzero-symbol arguments;
principal diagonal dominance;
plain-j low-degree divisor support;
single oriented-edge low-bidegree relation;
ordinary coordinate Plucker norm mining.
```

Surviving theorem:

```text
selected-minor determinant-line p-unitness,
proved as a class-field/Fitting/reduced-norm identity.
```

The current tightened status is recorded in:

```text
p24/trace_frame_fitting_norm_status.md
p24/trace_frame_denominator_safe_fitting_attack.md
p24/trace_frame_beta_interpolant_support_boundary.md
p24/axis_crt_fourier_support_boundary.md
```

It separates the full leading determinant line, which is the canonical
Fitting/norm object, from residual-tail determinants, which remain useful
diagnostics but are basis-dependent as scalar payloads.  The support boundary
also rules out replacing the Fitting/norm theorem by a naive sparse
beta-interpolant certificate.  The CRT-axis support boundary identifies a
real support collapse to a spanning-hypertree polynomial, but not yet a
small enough or sign-controlled expression to finish the certificate.  The
p24 support estimate still has an explicit lower bound above `10^826` terms,
so the polynomial cannot be listed and must be controlled by a p-unit theorem.

## Relation To The DANGER3 Certificate

This is the p-unit certificate for the trace-frame `L1` route.  Once it is
proved, the leading trace-frame map is injective on every required
packet/factor, hence the harmful packet collapse in the decomposed CM
handoff is excluded.  The post-root DANGER3 tail remains the already-isolated
logarithmic step:

```text
j root -> Montgomery A -> x0.
```

See:

```text
p24/decomposed_certificate_handoff.md
p24/post_cm_root_projection_boundary.md
```

The remaining gap is purely arithmetic:

```text
construct/prove the p-integral determinant-line norm N_lead for the actual
p24 CM torsor without enumerating the class set.
```
