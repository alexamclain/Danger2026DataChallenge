# Trace-Frame Schubert Equivariant Descent Target

Date: 2026-06-05

This is the next theorem needed after the packet-norm packaging in:

```text
p24/trace_frame_schubert_packet_norm.md
```

The finite zero/nonzero logic is Lean-checked in:

```text
p24/lean/SchubertEquivariantDescentGate.lean
```

The fixed-section versus packetwise-pivot boundary is illustrated by:

```text
p24/trace_frame_schubert_descent_toy.py
p24/trace_frame_lead_prefix_tail_toy.py
```

The issue is subtle: four packetwise determinant formulas with the same shape
do not automatically define four global decomposition-field elements.  The
determinants must descend through the packet Galois action as determinant-line
sections, up to explicit p-units.

## Theorem Candidate

Let:

```text
K_m = Q(mu_m)
M   = Q(zeta_n)^<p>,        [M:Q]=8
S   = K_m M
E   = F_p(mu_m).
```

For each Schubert factor:

```text
F in {A, B, AB, tail}
```

or for the single denominator-free leading factor:

```text
F = lead.
```

there is an intrinsic determinant-line section:

```text
delta_F in L_F(S)
```

where `L_F` is the one-dimensional determinant line associated to the
corresponding flag condition:

```text
A:
  selected Top_1 Plucker coordinate on A.

B:
  selected Top_2 Plucker coordinate on B_axis.

AB:
  selected quotient Plucker coordinate measuring
  Top_2(B_axis) modulo Top_2(A).

tail:
  selected residual-tail Plucker coordinate on K_2=ker(Top_2|W_axis),
  stated either as a determinant-line quotient or as a denominator-free
  block/Grassmannian minor.

lead:
  selected full leading Plucker coordinate using the first
  179 + 179 + 10 trace-frame coordinates.
```

For every decomposition-field automorphism `sigma_b in Gal(M/Q)` and every
packet label `a`, the packet residues satisfy:

```text
Delta_F(ba)
  = u_F(b,a) * sigma_b(Delta_F(a))
```

where:

```text
u_F(b,a) in E^*
```

is the determinant of the transported basis/flag trivialization.  In
particular, `u_F(b,a)` is a p-unit and cannot create or remove zeros.

After choosing one global trivialization of `L_F`, this equivariance produces
an element:

```text
Xi_F in S
```

whose eight residues are the packet determinants up to p-units.  Thus
`Norm_{S/K_m}(Xi_F)` has nonzero residue in `E` iff every packet determinant
`Delta_F(a)` is nonzero.

## Why Determinant Lines Matter

The Schubert factors are not arbitrary row-reduced determinants.  Arbitrary
packetwise pivots would not descend; they could change by denominators that
vanish in some packet.

The proof must use fixed flag data:

```text
the A/B axis split;
Top_1, Top_2, and the residual Top_3 head;
the degree-179 intermediate field C/E;
the selected normal or power basis of C;
the selected 10-coordinate head projection;
the tensor-factor representative, or the tensor-factor symmetry theorem.
```

These data must be defined over the same cyclotomic/class-field packet
algebra and transported by `Gal(M/Q)`.  Then changing packet is base change,
and determinant lines commute with base change.

A useful finite warning is the row `[x-1, x-2]` over a split product algebra.
At `x=1`, the first fixed minor vanishes and the second does not.  At `x=2`,
the second fixed minor vanishes and the first does not.  Packetwise Gaussian
elimination can choose a nonzero pivot in every packet, but no single fixed
minor is nonzero in every packet.  Such a spliced pivot product is not the
norm of a fixed determinant section.

## Tail Denominator Boundary

`Delta_tail` is the dangerous factor.  The practical `10 x 10` residual-tail
matrix is formed after computing:

```text
K_2 = ker(Top_2|W_axis).
```

A packetwise kernel basis can introduce denominators from the prefix minors.
For descent, use one of the following denominator-safe formulations:

```text
1. determinant-line quotient:
   Delta_tail is a section of
   det(K_2)^vee tensor det(head_10)
   over the open Schubert chart where the prefix factors are p-units;

2. adjugate/Cramer numerator:
   build a global polynomial numerator whose denominator is a power/product
   of Delta_A, Delta_B, and Delta_AB;

3. full leading Plucker comparison:
   Delta_lead = Delta_prefix * Delta_tail,
   prove Delta_lead and Delta_prefix are both global p-units,
   then infer the tail p-unit.
```

The third formulation may be the cleanest for a formal proof because it avoids
constructing a packetwise kernel basis as primary data.  The factorized tail
still remains useful because it isolates the actual cross-block obstruction.

The single-leading formulation is recorded in:

```text
p24/trace_frame_single_leading_punit.md
p24/trace_frame_lead_divisor_support_boundary.md
p24/trace_frame_lead_phase_shape_boundary.md
p24/lean/TraceFrameLeadingNormGate.lean
```

It is denominator-free from the start.  Nonzero `Delta_lead` forces the prefix
rank and tail injectivity by the dimension count `358+10=368`; the toy
`trace_frame_lead_prefix_tail_toy.py` checks the corresponding `3+1=4`
finite-field model.

The divisor-support scan found a useful boundary: in moving lower-rank
trace-frame rows, the leading determinant norm has the expected Frobenius
packet period, but its rational interpolant in the plain selected `j`
coordinate has generic degree and no small-Heegner numerator support.  So the
descent/p-unit proof cannot be a plain low-degree `j`-divisor recognition
argument.  The oriented-edge scan also finds no low-bidegree relation in
`(j_i,j_{i+s})`.  The proof must therefore keep the non-genus packet phase at
the determinant-line or crossed-product level.

## Proof Skeleton

1. Work over the universal coefficient algebra `S=K_m M` before reducing
   modulo `p`.

2. Define the axis modules `A`, `B_axis`, and `W_axis=A+B_axis` as character
   submodules over `S`.  Their definitions use divisor classes of `m`, so
   they are transported functorially by decomposition-field Galois.

3. Define the trace-frame maps from the degree-5549 tensor factor through the
   degree-179 intermediate field.  Fix the basis/flag by a rule over `S`, not
   by packetwise finite-field pivoting.

4. Express `Delta_A`, `Delta_B`, `Delta_AB`, and either `Delta_tail` or
   `Delta_lead/Delta_prefix` as exterior-power coordinates relative to these
   fixed flags.

5. Prove base change compatibility:

```text
sigma_b(Top_i(packet a)) = transported Top_i(packet ba)
sigma_b(A_a) = A_ba
sigma_b(B_a) = B_ba
sigma_b(flag_a) = flag_ba
```

6. Take determinants.  Basis changes contribute only the explicit units
   `u_F(b,a)`.

7. Conclude that the eight packet residues are residues of four global
   determinant-line sections, hence four relative degree-8 packet norms.

## Arithmetic Theorem After Descent

Once descent is proved, the remaining p-unit theorem is:

```text
Norm_{S/K_m}(Xi_lead)
```

for the single-leading route, or:

```text
Norm_{S/K_m}(Xi_A),
Norm_{S/K_m}(Xi_B),
Norm_{S/K_m}(Xi_AB),
Norm_{S/K_m}(Xi_tail)
```

are nonzero modulo the selected prime of `K_m` over
`p = 10^24 + 7`.

If the denominator-free route uses `Delta_lead` and `Delta_prefix` instead,
the equivalent p-unit target is:

```text
Xi_A, Xi_B, Xi_AB, Xi_prefix, Xi_lead
```

with the implication:

```text
prefix p-units + lead p-unit => residual-tail p-unit.
```

This has one extra global scalar but may be easier to prove without circular
kernel-basis choices.

## False Strengthenings To Avoid

Do not replace this theorem with any of:

```text
same matrix dimensions imply global descent;
rank symmetry implies determinant-line equivariance;
packetwise row-reduction pivots are canonical;
component p-units force the residual tail;
ordinary beta orbit products collapse to a representative power.
```

Those statements are either unproved or already contradicted by the small
audits.  The safe theorem is determinant-line equivariance plus p-unit
nonvanishing of the resulting relative norms.
