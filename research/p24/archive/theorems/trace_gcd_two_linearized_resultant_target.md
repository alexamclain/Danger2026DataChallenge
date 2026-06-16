# Trace-GCD Two Linearized Resultant Target

Date: 2026-06-06

This note sharpens the remaining p24 trace-GCD theorem after the
unit-2/diamond compression.

## Why This Note Exists

The conditional 4-field payload is:

```text
Xi_O0, Xi_O0^{-1}, Xi_O1, Xi_O1^{-1}.
```

But the two entries have different arithmetic shapes:

```text
Xi_O0 = one fixed linearized trace-GCD resultant;
Xi_O1 = a degree-35 Frobenius/crossed norm of linearized trace-GCD resultants.
```

So the proof target should not be phrased as two unrelated determinant
scalars.  It should be phrased as:

```text
one fixed p-linearized resultant p-unit
+ one degree-35 resultant norm p-unit.
```

## Fixed Orbit

For the fixed right orbit `O0={0}`, the trace-GCD prefix is:

```text
B = {O2,O3,O5,O6}
```

and the tail is:

```text
T = first 16 Lang/trace-dual coordinates of O1.
```

Let `K_0` be the common kernel of the four full prefix trace blocks.  The
fixed resultant is:

```text
Res_0 = Res_p-lin(P_{K_0}, T),
```

where `P_{K_0}` is the monic p-linearized subspace polynomial of `K_0`.
Equivalently, after choosing any `F_p`-basis of `K_0`,

```text
Res_0 = det(T|K_0)
```

up to a p-unit determinant-line factor.

The fixed-orbit theorem is:

```text
Res_0 in O_p^*.
```

This is equivalent to:

```text
dim K_0 = 16
and T is injective on K_0.
```

Equivalently, after the trace-pairing/subspace-polynomial bridge, the
all-coordinate residual product of the selected `140+16` leading Lang
coordinates is a p-unit:

```text
p24/trace_gcd_residual_product_punit_theorem.md
p24/trace_gcd_trace_pairing_subspace_bridge.md
```

## Nonzero Orbit

For a nonzero Frobenius orbit

```text
O1 = {t0, p*t0, ..., p^34*t0} subset Z/211Z,
```

let `K_t` be the transported prefix kernel and let `T_t` be the transported
tail window.  Define:

```text
Res_t = Res_p-lin(P_{K_t}, T_t).
```

The nonzero orbit scalar is the crossed/Frobenius norm:

```text
Xi_O1 = Norm_O1(Res)
      = product_{t in O1} Res_t
```

with the usual determinant-line p-unit convention.  In block-cycle language
this is the determinant of the semilinear cyclic Fitting operator built from
the tail-on-kernel matrices.

The nonzero-orbit theorem is:

```text
Norm_O1(Res) in O_p^*.
```

This detects every bad local resultant in the orbit:

```text
Res_t = 0 for some t in O1
  => Norm_O1(Res) = 0.
```

Equivalently, the product over the degree-35 orbit of the transported
all-coordinate residual products is a p-unit.

## Diamond Compression

If the diamond/unit-2 determinant-line equivariance theorem is proved, then:

```text
Norm_O1(Res) in O_p^*
  => Norm_O2(Res),...,Norm_O6(Res) in O_p^*.
```

Together with `Res_0 in O_p^*`, this gives all seven orbit p-units.

The finite gates are:

```text
p24/lean/TraceGcdLinearizedResultantNormGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
p24/lean/TraceGcdDiamondEquivarianceGate.lean
```

The executable payload schema is:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```

## What Must Be Proved Arithmetically

The current missing theorem is therefore:

```text
1. construct the p-integral family of prefix kernels K_t and tail maps T_t
   over the full 211-product algebra;

2. prove the diamond/unit-2 action transports this family up to p-unit
   determinant-line factors;

3. prove Res_p-lin(P_{K_0}, T_0) is a p-unit at the selected ordinary prime;

4. prove the degree-35 Frobenius/crossed norm
      Norm_O1(Res_p-lin(P_{K_t}, T_t))
   is a p-unit at the selected ordinary prime.
```

This is sharper than the seven independent orbit-norm theorem and more
intrinsic than a raw list of determinants.

The structural part of items 1-2 is stated in:

```text
p24/full_product_determinant_line_equivariance_theorem.md
```

and its finite determinant-line consequence is tested by:

```text
p24/full_product_determinant_transport_toy.py
```

## Proof Directions

The fixed resultant might be approachable through:

```text
prefix-kernel class-field trace pairing;
subspace-polynomial normality of K_0;
local intersection of the fixed Chow/Fitting divisor.
```

The nonzero orbit norm is more likely to need:

```text
crossed-product/Fitting reduced norm;
phase-aware Borcherds product for the orbit Chow divisor;
or a norm identity in the 35-dimensional right factor.
```

The existing small actual-CM tests support the finite shape but also warn
against overstrong simplifications:

```text
p24/trace_gcd_actual_cm_orbit_norm_miner.py
p24/trace_gcd_actual_cm_unit_action_falsifier.py
p24/trace_gcd_two_resultant_holdout_audit.py
p24/trace_gcd_phase_unit_dictionary_boundary.md
```

In particular, right-unit symmetry preserves p-unitness only up to
determinant-line scale; it does not make printed resultant/norm scalars
literally equal.

The newest holdout audit tested the two-resultant theorem surface on the
pinned `D=-13319` row and the independent `D=-26759` holdout:

```text
selected_two_punit_groups=4/4
all_nonzero_groups=4/4
punit_transport_edges=8/8
literal_equal_nonzero_edges=0/8
split_norm_matches=12/12
naive_base_polynomial_groups=0/4
```

Thus the small-data evidence now supports the exact compressed observable:

```text
fixed resultant p-unit
+ one nonzero crossed norm p-unit
+ p-unit transport.
```

It simultaneously rejects the two easiest false shortcuts:

```text
literal unit-invariance of printed orbit norms;
ordinary base-field resultant descent for the nonzero orbit.
```

The proof-route synthesis is recorded in:

```text
p24/trace_gcd_two_resultant_proof_route_synthesis.md
p24/trace_gcd_semilinear_fitting_nonintersection_attack.md
p24/trace_gcd_two_resultant_theorem_manifest.py
```
