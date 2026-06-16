# Relative Kummer Phase Normal Form

Date: 2026-06-05

This note refines the selected-chain class-field tower target.  It does not
construct the p24 certificate, but it gives a more classical form of the
missing relative phase data.

## Cyclic Prime Layer

For one refinement layer `L < K` with prime degree

```text
r = [K:L],
```

write child periods above a parent `aK` as

```text
y_u = sum_{l in L} j_{a u l},        u in K/L.
```

After adjoining a primitive `r`th root of unity `zeta_r`, define relative
Lagrange resolvents:

```text
T_s(aK) = sum_{u in K/L} zeta_r^(s u) y_u,      0 <= s < r.
```

The trivial trace is the parent period:

```text
T_0 = sum_u y_u.
```

For a primitive character `s != 0`, the Kummer power

```text
K_s = T_s^r
```

is invariant under cyclic rotation of the child labels.  In a
one-Frobenius-orbit layer, the selected child polynomial can be packaged by
Kummer powers rather than by raw ordered relative traces.  In a multi-orbit
layer, Kummer powers also need cross-orbit phase glue.  A natural glue
invariant is `T_a/T_1^a` for one representative `a` of each non-base
Frobenius orbit.

## Toy Reconstruction

The script:

```text
p24/relative_kummer_reconstruction_toy.py
```

uses the same calibration tower as `relative_tower_character_toy.py`:

```text
D = -5000
q = 1259
h = 30 = 2 * 3 * 5
relative degree r = 3
```

For each top parent, it computes:

```text
T_0,
T_1,
K_1 = T_1^3.
```

Then it enumerates the three cube roots of `K_1`, pairs each with its
Frobenius conjugate, and applies inverse DFT.  The three choices descend to
the same unordered child polynomial:

```text
parent=0:
  recovered_child_lists are cyclic rotations
  recovered_polynomials=[(563,777,133,1)]
  true_polynomial_recovered=1

parent=1:
  recovered_child_lists are cyclic rotations
  recovered_polynomials=[(648,958,727,1)]
  true_polynomial_recovered=1
```

So in the toy:

```text
parent period + primitive Kummer constant
  <=> unordered relative child polynomial.
```

## p24 Accounting

The script:

```text
p24/relative_kummer_payload_accounting.py
```

reports:

```text
r=157: ord_157(p)=156, one Frobenius orbit of 156 primitive constants
r=211: ord_211(p)=35, six Frobenius orbits of 35 primitive constants
```

The number of primitive Kummer slots is:

```text
(157 - 1) + (211 - 1) = 366,
```

exactly the number of informative selected child-polynomial coefficients
after the forced trace coefficients are supplied by the parents.  This count
does not include the five cross-orbit glue invariants needed if the p24 `211`
layer is represented by Kummer powers instead of by its selected child
polynomial.

The selected-chain certificate count is unchanged:

```text
2 + 157 + 211 + 3107441 = 3107811
3107811 / sqrt(p) = 3.107811e-6.
```

## Consequence

This is a normal form, not a new selector.

It improves the theorem target from:

```text
construct selected child polynomials
```

to the more class-field-shaped statement:

```text
construct the relative Kummer powers T_s^r for the 157 and 211 layers,
with the correct embedded orientation and 211-layer cross-orbit phase glue,
plus the selected recovery polynomial.
```

The caveat is exactly the one already seen in:

```text
p24/order_l_kummer_phase_toy.py
```

Kummer powers depend on the oriented relative quotient action.  The unordered
period set alone can produce many possible Kummer constants.  Therefore the
Kummer form does not evade the tower-section obstruction; it names the phase
payload more algebraically.

The follow-up complexity scan:

```text
p24/tower_kummer_phase_complexity_scan.py
p24/tower_kummer_phase_complexity_boundary.md
```

also rules out the most direct additional simplification.  In bounded small
CM towers, every tested coordinate of `T_s^r` had full interpolation degree
as a function of the parent period; no low-degree or low-recurrence Kummer
phase formula appeared.

The orbit-norm follow-up:

```text
p24/relative_kummer_orbit_norm_toy.py
p24/relative_kummer_orbit_norm_boundary.md
```

shows that a single Frobenius orbit norm is also not enough for selected-chain
reconstruction.  In the degree-3 toy, fixing the parent trace and
`Norm(T_1^3)` leaves `210` descending child polynomials.  Orbit norms are
therefore p-unit/nonzero payloads, not selected child-polynomial payloads.

The sharper boundary is now recorded in:

```text
p24/kummer_orbit_minpoly_producer_frontier.md
p24/relative_kummer_multi_orbit_ambiguity_gate.md
p24/lean/PhaseLiftedTowerPayloadGate.lean
```

The finite selected-chain payload can equivalently be counted as:

```text
top degree-2 slots
+ two forced child-trace slots
+ 366 informative Kummer orbit/minpoly slots
+ 3107441 selected recovery slots
= 3107811.
```

For the p24 `211` layer, Kummer form also needs cross-orbit glue.  This is
five extension-field invariant objects.  If serialized conservatively as
base-field coordinates, each has Frobenius orbit degree `ord_211(p)=35`, so
the extra cost is `5*35=175` base-field slots and the Kummer-with-glue surface
is `3107811 + 175 = 3107986`.

Thus the class-field-shaped theorem target is specifically to construct the
embedded Frobenius minimal polynomials or orbit representatives of the Kummer
powers `T_s^r`, together with the cross-orbit phase glue in the 211 layer.
Norms alone are too compressed; arbitrary abstract roots are unpaired.

For the trace-GCD p-unit route, the finite nonvanishing bridge is isolated in:

```text
p24/relative_kummer_nonvanishing_bridge_toy.py
p24/lean/KummerNonvanishingGate.lean
p24/trace_gcd_kummer_nonvanishing_bridge.md
```

It shows that Kummer powers can certify nonzero relative DFT values, but the
actual p24 trace-GCD determinant still needs a structural zero-detection
theorem connecting determinant failure to Kummer failure.

## Updated Positive Route

A selected-chain producer may now output either:

```text
1. selected child polynomials of degrees 157 and 211; or
2. equivalent relative Kummer-power data:
   one degree-156 Frobenius orbit for the 157 layer,
   six degree-35 Frobenius orbits for the 211 layer,
   plus five 211-layer cross-orbit glue invariants such as T_a/T_1^a.
```

Both must be paired to the embedded conductor-2 `j` torsor and to one selected
degree-`3107441` recovery polynomial.  Abstract Kummer or `bnrclassfield`
data without this pairing is still insufficient.
