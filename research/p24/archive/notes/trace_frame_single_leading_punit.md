# Trace-Frame Single Leading P-Unit

Date: 2026-06-05

This note records a denominator-free alternative to the four-factor Schubert
surface.  The factorized route is still useful for proof search, but the full
leading Plucker determinant is the cleanest object for determinant-line
descent.

## Leading Object

For one H-packet tensor factor over:

```text
E = F_p(mu_m)
C/E has degree 179
B/C has degree 31
dim_E W_axis = 368
```

the fixed leading coordinate is:

```text
Top_3,lead = first 179 + first 179 + first 10 coordinates of C^3.
```

Let:

```text
Delta_lead(a) in E
```

be the `368 x 368` determinant of `Top_3,lead` on the fixed ordered axis
basis in H-packet `a`.

The finite certificate condition is simply:

```text
Delta_lead(a) != 0 for every H-packet a.
```

This implies the trace-frame axis map is injective in every packet, and hence
rules out the harmful DANGER3 packet collapse.

The finite global-norm implication is Lean-checked in:

```text
p24/lean/TraceFrameLeadingNormGate.lean
```

## Why This Avoids Tail Denominators

The factorized Schubert split writes, after choosing compatible bases:

```text
Delta_lead = Delta_prefix * Delta_tail
```

where:

```text
Delta_prefix:
  the first 358 rows have full rank on W_axis;

Delta_tail:
  the first 10 tail rows separate K_2=ker(Top_2|W_axis).
```

But constructing `Delta_tail` directly can introduce denominators from a
packetwise kernel basis.  The full leading determinant is a fixed exterior
coordinate and needs no kernel-basis construction.

Moreover, nonzero `Delta_lead` already forces the prefix/tail shape:

```text
rank(prefix) < 358
  => rank(prefix plus 10 tail rows) <= 357 + 10 = 367
  => Delta_lead = 0.
```

Thus:

```text
Delta_lead != 0
  => rank Top_2(W_axis)=358
  => the selected 10 tail rows are injective on K_2.
```

The tiny finite-field model:

```text
p24/trace_frame_lead_prefix_tail_toy.py
```

checks the same shape with `3 + 1 = 4` rows.

The plain-`j` divisor-support boundary for this leading determinant is:

```text
p24/trace_frame_lead_divisor_support_boundary.md
p24/trace_frame_lead_divisor_support_scan.py
p24/trace_frame_lead_phase_shape_boundary.md
p24/trace_frame_lead_phase_shape_scan.py
```

It finds the expected Frobenius packet periodicity in moving small rows, but
no simple low-degree or small-Heegner-supported divisor in the selected
`j`-coordinate.  The follow-up phase-shape scan also finds no low-bidegree
single-edge relation.  Thus the p-unit proof should remain genuinely
packet/crossed-product aware.

The crossed-product formulation for the same leading determinant is:

```text
p24/trace_frame_lead_crossed_product_norm.md
```

It rewrites the beta-shifted values of `Delta_lead` as Frobenius-orbit
reduced norms.  This keeps the full leading determinant as the denominator-free
object while exposing the same `8 H-packets * 70 tensor factors = 560`
orbit factors visible in the scalar-extension decomposition.

## Decomposition-Field Packaging

Let:

```text
K_m = Q(mu_m)
M   = Q(zeta_n)^<p>,        [M:Q]=8
S   = K_m M.
```

If the leading Plucker determinant is constructed equivariantly as a
determinant-line section over `S`, then there is:

```text
Xi_lead in S
```

whose eight residues above `p` are:

```text
unit(a) * Delta_lead(a),        unit(a) in E^*.
```

Therefore:

```text
Norm_{S/K_m}(Xi_lead) mod p != 0
  => Delta_lead(a) != 0 for every H-packet a.
```

With tensor-factor rank symmetry, this is a single degree-8 relative p-unit
target:

```text
Xi_lead is a p-unit at the selected prime over p.
```

Without tensor-factor symmetry, it becomes:

```text
70 degree-8 relative p-unit targets,
```

one for each scalar-extension tensor factor.

## Cost

The explicit single-leading matrix surface per H-packet is:

```text
368 x 368 = 135424 E-entries.
```

For one tensor factor and all eight H-packets:

```text
1083392 E-entries
= 5915320320 F_p slots
= 5.91532032e-3 * sqrt(p).
```

For all 70 tensor factors:

```text
414072422400 F_p slots
= 0.4140724224 * sqrt(p).
```

This is larger than the factorized four-Schubert matrix surface but still
comfortably sub-sqrt.

The Toeplitz/translate-minor normal form gives a smaller selected-origin
encoding of the same matrix surface.  Once the p-integral normal-form theorem
is supplied, a verifier can reconstruct the selected matrix from the cyclic
`m`-symbol:

```text
m = 66254 E-entries per H-packet/tensor factor.
```

The corresponding selected-origin payload is:

```text
one tensor factor, all eight H-packets:
  2893974720 F_p slots
  = 2.89397472e-3 * sqrt(p);

all 70 tensor factors:
  202578230400 F_p slots
  = 0.2025782304 * sqrt(p).
```

But this compression does not extend to a literal beta-orbit table.  A symbol
over one nonzero beta-orbit algebra would have:

```text
66254 * 5549 = 367643446 E-entries,
```

which is already:

```text
2.00733321516 * sqrt(p)
```

Fp slots for one orbit.  Thus the crossed-product theorem must be supplied as
a compressed reduced-norm/class-field identity, not by listing orbit-algebra
symbols.  See:

```text
p24/trace_frame_selected_minor_certificate_spec.md
p24/trace_frame_selected_minor_certificate_accounting.py
```

## Relation To The Four-Factor Route

The four-factor surface:

```text
Delta_A, Delta_B, Delta_AB, Delta_tail
```

is smaller as an explicit matrix verifier and more informative for proof
search.  The single-leading surface:

```text
Delta_lead
```

is safer for descent because it is a fixed Plucker coordinate and does not
require packetwise kernel bases.

The best current proof architecture is therefore:

```text
1. use the single leading determinant for decomposition-field descent;
2. prove its p-unitness either directly, or by a denominator-safe product
   identity involving prefix and tail determinant-line sections;
3. use the factorized Schubert split only after the objects are fixed globally.
```

## Missing Arithmetic

This note does not prove the p-unit theorem.  It narrows the theorem to:

```text
For the selected p24 CM trace-frame axis, the equivariant leading Plucker
element Xi_lead in K_m Q(zeta_n)^<p> has nonzero relative norm modulo p.
```

That is one relative degree-8 p-unit statement, and it is currently the
cleanest denominator-free target for a phase-aware class-field identity,
divisor contradiction, or modular-unit construction.  The naive plain-`j`
divisor and single-edge routes are disfavored by the small scans above.

In crossed-product language, the same missing arithmetic is:

```text
the beta-zero factor D_0 and all 560 nonzero R_lead,Omega are p-units.
```

With tensor-factor rank symmetry this compresses back to the single
degree-8 relative norm above; without that symmetry it becomes 70 such
degree-8 norms, one for each scalar-extension tensor factor.

The compact tensor-factor equivariance audit:

```text
p24/trace_frame_tensor_factor_equivariance_boundary.md
p24/trace_frame_tensor_factor_equivariance_audit.py
p24/lean/TraceFrameTensorFactorEquivarianceGate.lean
```

supports the symmetry side of this compression: in the tested rows, split
tensor factors have the same leading determinant base norm and the same fixed
pivot shape.  It remains an external p-integral determinant-line theorem for
p24, not a consequence of the finite Lean gates.

The integrated norm-compressed certificate surface is recorded in:

```text
p24/trace_frame_norm_compressed_certificate_spec.md
p24/lean/TraceFrameNormCompressedCertificateGate.lean
```
