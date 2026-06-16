# Trace-Frame Factorized Schubert Certificate Spec

Date: 2026-06-05

This is the current explicit certificate surface for the factorized
trace-frame route.  It does not prove the missing p-units.  It fixes what a
finite verifier would check if the arithmetic theorem supplies the relevant
CM trace-frame matrices or their p-unit determinants.

## Objects

For each of the eight p24 H-packets:

```text
A_a = F_p[X]/(f_a),        deg f_a = 388430
E   = F_p(mu_m),           [E:F_p] = 5460
A_a tensor_Fp E ~= product_{70} B_i
[B_i:E] = 5549
```

In one tensor factor `B/E`, use:

```text
C/E,        [C:E] = 179
B/C,        [B:C] = 31
W_axis = A + B_axis
```

where:

```text
A      = W_constant + W_2 + W_157,   dim_E A = 158
B_axis = W_211,                      dim_E B_axis = 210
dim_E W_axis = 368.
```

The leading trace-frame coordinate is:

```text
Top_3,lead = first 179 + first 179 + first 10 coordinates.
```

## Four P-Unit Factors

Per H-packet, the factorized certificate has four named p-unit obligations:

```text
Delta_A:
  Top_1 is injective on A.

Delta_B:
  Top_2 is injective on B_axis.

Delta_AB:
  Top_2(B_axis) maps with rank 200 modulo Top_2(A),
  equivalently dim(Top_2(A) cap Top_2(B_axis)) = 10.

Delta_tail:
  pi_10 o b_28 is injective on K_2 = ker(Top_2|W_axis).
```

Together they imply:

```text
Top_3,lead is injective on W_axis.
```

The finite implication is Lean-checked by:

```text
p24/lean/TraceFrameLeadingNormGate.lean
p24/lean/TraceFramePrefixIntersectionGate.lean
p24/lean/TraceFrameResidualTailGate.lean
p24/lean/TraceFrameAnnihilatorGate.lean
p24/lean/ScalarExtensionGate.lean
p24/lean/TensorFactorProjectionGate.lean
```

and then joins the existing axis/content gates.

## Explicit Matrix Surface

If a verifier checks matrix entries rather than a theorem-supplied scalar
p-unit, the natural matrix sizes over `E` are:

```text
Delta_A:     158 x 158     = 24964 entries
Delta_B:     210 x 210     = 44100 entries
Delta_AB:    200 x 200     = 40000 entries
Delta_tail:   10 x 10      =   100 entries
```

So per H-packet:

```text
109164 E-entries.
```

For all eight H-packets, using tensor-factor rank symmetry to avoid listing
all 70 scalar-extension factors:

```text
873312 E-entries
= 873312 * 5460 F_p slots
= 4768283520 F_p slots
= 4.76828352e-3 * sqrt(10^24+7).
```

Even the brute all-70-factor expansion remains sub-sqrt:

```text
61131840 E-entries
= 333779846400 F_p slots
= 0.3337798464 * sqrt(10^24+7).
```

The accounting script is:

```text
p24/trace_frame_factorized_schubert_accounting.py
```

## Proof-Surface Version

The matrix surface is only a finite verifier accounting.  The desired
mathematical finish is much smaller:

```text
single-leading version:
  prove Delta_lead is a p-unit in every H-packet.
```

This denominator-free surface is documented in:

```text
p24/trace_frame_single_leading_punit.md
```

The factorized proof-search version is:

```text
for each of the eight H-packets:
  prove Delta_A, Delta_B, Delta_AB, Delta_tail are p-units.
```

That is:

```text
32 named p-unit statements
```

The decomposition-field packet-norm packaging sharpens this further.  If the
single leading determinant, or the four Schubert determinants, are constructed
equivariantly over
`K_m M = Q(mu_m) Q(zeta_n)^<p>`, the eight packet residues of each factor are
the residues of one relative degree-8 element:

```text
Xi_lead
```

or:

```text
Xi_A, Xi_B, Xi_AB, Xi_tail in K_m M.
```

Then:

```text
Norm_{K_m M / K_m}(Xi_F) mod p != 0
  => Delta_F is nonzero in every H-packet.
```

So, with tensor-factor rank symmetry, the theorem surface is:

```text
1 relative degree-8 p-unit over K_m for the single-leading route,
or
4 relative degree-8 p-unit statements over K_m
```

instead of 32 packetwise p-unit statements.  See:

```text
p24/trace_frame_schubert_packet_norm.md
p24/trace_frame_schubert_equivariant_descent.md
p24/lean/SchubertEquivariantDescentGate.lean
p24/lean/TraceFrameSchubertPacketNormGate.lean
```

or, in the beta/tensor bridge without using tensor-factor rank symmetry:

```text
2240 factorwise p-unit statements = 32 * 70.
```

Even without tensor-factor symmetry, the same packet-norm packaging compresses
the H-packet direction:

```text
280 relative degree-8 p-unit statements = 4 * 70
```

The bridge:

```text
p24/beta_orbit_tensor_factor_bridge.md
```

identifies those 70 factorwise statements per H-packet with the nonzero
`E`-Frobenius beta-orbit crossed-product factors.

## Remaining Arithmetic Input

This spec is not a proof.  It says the asymptotic certificate surface is
already sub-sqrt if one can prove or produce the four p-units per H-packet.

The missing theorem is:

```text
For the selected p24 CM trace-frame construction at p=10^24+7, the four
equivariant decomposition-field Schubert elements Xi_A, Xi_B, Xi_AB, and
Xi_tail are p-units at the selected prime over p.
```

Small CM audits support the finite shape:

```text
p24/trace_frame_prefix_intersection_audit.py
p24/trace_frame_annihilator_kernel_audit.py
p24/trace_frame_residual_tail_audit.py
p24/trace_frame_leading_residual_value_audit.py
```

They also close weak theorem shapes:

```text
component nonvanishing alone is too weak;
ordinary beta norm collapse is false in toys;
sparse beta interpolants are not visible;
simple LRS/MSRD low-displacement structure is not visible.
```

The remaining route must be a phase-aware class-field p-unit, divisor
contradiction, or explicit split-cycle identity for these named Schubert
factors.
