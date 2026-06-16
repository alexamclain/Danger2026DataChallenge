# Trace-Frame Selected-Minor Certificate Spec

Date: 2026-06-05

This note states the finite verifier surface suggested by the
Toeplitz/translate-minor normal form.  It is not the missing arithmetic
theorem.  Its purpose is to make the exact certificate payload and the
remaining producer theorem visible.

## Normal-Form Assumption

For one H-packet and one scalar-extension tensor factor, the leading
trace-frame determinant is:

```text
Delta_lead = det(Top_3,lead(R_s))_{s in S_axis}
```

over:

```text
E = F_p(mu_m),      [E:F_p] = 5460
m = 66254
S_axis = {0} union nonzero 2-, 157-, and 211-axis frequencies in Z/mZ
|S_axis| = 368.
```

The Toeplitz normal form says that, after p-integral Fourier/coordinate
changes whose determinants are p-units, this same p-unit question is:

```text
det(c_{r-s})_{0 <= r < 368, s in S_axis} != 0
```

for a cyclic `m`-periodic CM symbol:

```text
c = (c_0,...,c_{m-1}) in E^m.
```

Thus the finite checker can reconstruct the selected `368 x 368` matrix from
`m=66254` field entries rather than receiving all `135424` entries.

This is a verifier normal form.  A producer theorem must still prove that the
symbol is the correct p-integral CM symbol and that the normal-form changes
are p-units at the selected prime.

## Certificate Payload

For the selected-origin version, the certificate can carry, for each covered
H-packet/tensor-factor representative:

```text
1. a length-66254 symbol c in E^m;
2. a determinant inverse u in E;
3. optional normal-form metadata naming the p-integral bases and p-unit
   Fourier/coordinate scalars.
```

The finite verifier performs:

```text
1. reconstruct M_{r,s} = c_{r-s mod m},
   rows r=0,...,367 and columns s in the fixed ordered S_axis;
2. compute delta = det(M) in E;
3. check delta * u = 1 in E;
4. use TraceFrameLeadingNormGate / TraceFrameBetaResultantGate hypotheses
   only for the already-proved finite implications.
```

If tensor-factor rank symmetry is proved, one tensor-factor representative
for all eight H-packets is enough.  Without that symmetry, the payload is
needed for all `70` tensor factors.

## Size Accounting

The static accounting script is:

```text
p24/trace_frame_selected_minor_certificate_accounting.py
```

It reports:

```text
selected_origin_matrix_surface:
  matrix_entries_over_E_per_packet_factor = 135424
  one_factor_all_H_packets_Fp_slots       = 5915320320
  all_70_factors_Fp_slots                = 414072422400

selected_origin_toeplitz_symbol_surface:
  symbol_entries_over_E_per_packet_factor = 66254
  one_factor_all_H_packets_Fp_slots       = 2893974720
  all_70_factors_Fp_slots                 = 202578230400
```

So the Toeplitz symbol surface is about half the raw leading-matrix surface:

```text
one tensor factor, eight H-packets:  2.89397472e-3 * sqrt(p)
all 70 tensor factors:              0.2025782304  * sqrt(p)
```

This is still comfortably sub-sqrt as a finite selected-origin verifier
surface.

## Beta-Orbit Boundary

The crossed-product/local-unit theorem is stronger.  It asks for p-unitness
over each nonzero beta-orbit algebra:

```text
A_Omega/E has degree 5549,
nonzero beta orbits = 560.
```

A literal Toeplitz symbol over every orbit algebra would cost:

```text
66254 * 5549 = 367643446 E-entries per nonzero orbit,
```

or:

```text
2.00733321516 * sqrt(p)
```

Fp slots for just one nonzero orbit.  Listing all nonzero orbits would be:

```text
1124.1066004896 * sqrt(p).
```

Therefore the beta-orbit route cannot be a literal table of orbit-algebra
symbols.  It must be a theorem or compressed norm certificate:

```text
R_lead,Omega = Norm_{A_Omega/E}(delta_Omega) is a p-unit
```

with the norm values, inverses, or a class-field identity supplied in
compressed form.

A literal inverse/Bezout witness in the full beta algebra is also too large.
For one beta algebra it would have:

```text
n * 5549 = 17243190109 E-entries
94147817995140 Fp slots
94.14781799514 * sqrt(p).
```

Multiplying this by the `70` tensor-factor representatives gives:

```text
6590.3472596598 * sqrt(p).
```

So the unit certificate cannot be a dense inverse in
`B[Y]/(Y^n-1)`.  It has to be reduced-norm/Fitting arithmetic.

Small CM inverse-witness experiments are recorded in:

```text
p24/trace_frame_beta_inverse_witness_boundary.md
p24/trace_frame_beta_inverse_witness_audit.py
```

The compressed-norm payload would be tiny if the matching theorem is known.
For all `560` nonzero orbit norms, carrying each norm value and its inverse
costs:

```text
2 * 560 = 1120 E-entries
6115200 Fp slots
6.1152e-6 * sqrt(p).
```

If the degree-8 decomposition-field descent is proved but tensor-factor
symmetry is not, the corresponding payload is:

```text
2 * 70 = 140 E-entries
764400 Fp slots
7.644e-7 * sqrt(p).
```

With tensor-factor symmetry it collapses to one value and one inverse in
`E`, i.e.:

```text
10920 Fp slots
1.092e-8 * sqrt(p).
```

These counts do not verify that the supplied scalars are the correct reduced
norms.  That matching is exactly the missing class-field/determinant-line
producer theorem.

The cleanest norm-compressed theorem candidate is the full beta-algebra
Fitting statement:

```text
A_all = O_E[Y]/(Y^n - 1)
delta_all = det(T_lead,all) in A_all
delta_all in A_all^*.
```

Its norm is:

```text
Norm_{A_all/O_E}(delta_all)
  = D_0 * product_{Omega != 0} R_lead,Omega.
```

This would imply every orbit factor is a p-unit, and the finite implication
is now abstractly covered by:

```text
p24/lean/TraceFrameBetaResultantGate.lean
```

The sidecar synthesis is:

```text
p24/subagent_selected_minor_norm_compression.md
```

The tensor-factor symmetry needed to shrink `70` degree-8 norm targets to one
degree-8 norm target is now tested in:

```text
p24/trace_frame_tensor_factor_equivariance_boundary.md
p24/trace_frame_tensor_factor_equivariance_audit.py
p24/lean/TraceFrameTensorFactorEquivarianceGate.lean
```

Small CM rows support equality of determinant base norms and pivot shapes
across split tensor factors, but the p24 p-integral equivariance theorem
remains external.

The resulting positive certificate surface is summarized in:

```text
p24/trace_frame_norm_compressed_certificate_spec.md
p24/lean/TraceFrameNormCompressedCertificateGate.lean
```

## Remaining Arithmetic

This spec reduces the certificate interface but not the producer problem.  A
successful proof still has to supply one of:

```text
1. a p-integral class-field identity producing the selected CM symbol c;
2. a p-unit row/column/block equivalence to an MSRD/Fourier-Chebotarev minor;
3. a divisor/Fitting-ideal theorem proving the selected Toeplitz minor avoids
   the selected prime;
4. a compressed reduced-norm theorem for all beta-orbit factors.
```

The key negative result from the accounting is:

```text
Toeplitz symbol compression is useful for selected-origin verification, but
literal beta-orbit symbol enumeration is already larger than sqrt(p).
```

So any asymptotic speedup must keep beta-orbit coverage theorem-level or
norm-compressed, not table-level.
