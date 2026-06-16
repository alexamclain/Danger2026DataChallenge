# One-Factor Certificate Chain

This note records the finite implication chain for the current tensor-factor
certificate surface.

## Objects

For one p24 H-character packet, let:

```text
A_a = F_p[X]/(f_a),          deg(f_a)=388430
E   = F_p(mu_m),             [E:F_p]=5460
A_a tensor E ~= product_{i=0}^{69} B_i
[B_i:E] = 5549
```

Let `W_axis` be the 368-dimensional axis space, equivalently the selected
K-character frequency set

```text
S_axis = {0} ∪ S_2 ∪ S_157 ∪ S_211.
```

The one-factor certificate chooses one factor `B_i` and one coordinate
projection

```text
P : B_i -> E^368.
```

The concrete finite certificate is:

```text
det(P(R_s)_{s in S_axis}) != 0 in E.
```

Here `R_s` denotes the K-character resolvent evaluated in `B_i`.

## Lean Gates

I added:

```text
p24/lean/TensorFactorProjectionGate.lean
```

It checks:

```text
coordinate projection after one tensor factor is injective
  => projection to that tensor factor is injective
  => the full tensor evaluation is injective.
```

Together with:

```text
p24/lean/ScalarExtensionGate.lean
p24/lean/AxisInjectivityGate.lean
```

the full finite implication chain is:

```text
one-factor 368x368 coordinate minor nonzero
  => tensor-extended axis evaluation injective
  => base packet axis evaluation injective
  => selected L1 packet value nonzero
  => packet content vector is not all zero
  => harmful DANGER3 packet collapse is ruled out.
```

The component direct-sum variant is checked by:

```text
p24/lean/AxisModuleDirectSumGate.lean
```

and documented in:

```text
p24/tensor_factor_block_directness.md
```

## Factor Choice

The chosen factor is not extra hidden data.  By semilinear Frobenius:

```text
R_s(eta)^p = R_{p*s}(eta^p),
```

and `S_axis` is stable under `s -> p*s mod m`.  Therefore all 70 tensor
factors have the same axis rank.  This is recorded in:

```text
p24/tensor_factor_rank_symmetry.md
```

Thus a full-rank certificate in any one factor proves full rank in every
factor and descends to the base packet.

## Current Arithmetic Target

The missing theorem is now exactly:

```text
For every one of the eight p24 H-character packets, the 368 selected
K-character resolvents have rank 368 in one/every degree-5549 factor
of A_a tensor F_p(mu_m).
```

Equivalently, provide a nonzero `368 x 368` minor in that factor, or prove an
intrinsic trace/Hermitian determinant whose nonvanishing implies the same
rank.

The preferred intrinsic form is now the one-factor Moore determinant recorded
in:

```text
p24/tensor_factor_moore_certificate.md
```

For `B/E` with `|E|=Q`, it asks for

```text
det(R_s^(Q^j))_{s in S_axis, 0 <= j < 368} != 0.
```

This is still not the final DANGER3 certificate, but it is a sharply bounded
certificate surface:

```text
8 packets * degree-5549 tensor factors * 368-dimensional axis surface,
```

instead of enumerating the class set of size

```text
h = 205880396014.
```
