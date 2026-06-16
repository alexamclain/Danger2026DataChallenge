# Trace-GCD Plucker-Kummer Payload

Date: 2026-06-05

This note records the corrected Kummer payload target after the coordinate
Kummer determinant boundary.

## Point

Coordinate Kummer p-units are too weak:

```text
all entries nonzero does not imply determinant nonzero.
```

But a Kummer power attached to the Plucker coordinate itself is exactly a
zero detector:

```text
Theta(t) = Delta(t)^r,
Theta(t) != 0  <=>  Delta(t) != 0.
```

Here:

```text
Delta(t) = det(P V_t A).
```

The exponent `r` is whatever relative Kummer exponent removes the cyclic
label ambiguity in the producer theorem.  The finite verifier does not care
about the exponent; it only needs:

```text
Delta(t)=0 => Theta(t)=0,
Theta(t) != 0.
```

## Toy

Added:

```text
p24/plucker_kummer_payload_toy.py
p24/lean/PluckerKummerGate.lean
```

The toy reuses the `D=-5000`, relative-degree-3 calibration tower and
contrasts:

```text
rank-one control:
  all_entry_kummers_nonzero=1
  determinant=(0,0)
  plucker_kummer=det^3=(0,0)

actual parent matrix:
  determinant=(962,665)
  plucker_kummer=det^3 nonzero
```

So the determinant-level Kummer payload has the desired zero-detection
property, while coordinate-level Kummers do not.

## p24 Payload Shape

For p24 one may replace the 211 value payload:

```text
Delta(t), Inv(t)
```

by a Plucker-Kummer payload:

```text
Theta(t), ThetaInv(t),
Theta(t) = unit(t) * Delta(t)^r,
```

with a producer theorem proving the equality or at least zero-detection.
This is not smaller than the current finite payload, but it may be more
natural for class-field construction because `Theta(t)` is invariant under
cyclic relabeling of the relevant tower layer.

This descent claim is an extra arithmetic condition.  It is automatic only
when the chosen Plucker coordinate is semi-invariant under the hidden cyclic
labeling.  If the cyclic action permutes different Plucker coordinates rather
than scaling one determinant line, then individual powers `Delta(t)^r` need
not descend; the safe invariant is an orbit product/norm.

The finite descent distinction is recorded in:

```text
p24/plucker_kummer_descent_toy.py
p24/lean/PluckerKummerDescentGate.lean
```

An actual-CM audit of the pinned trace-GCD row is recorded in:

```text
p24/lang_trace_gcd_plucker_kummer_descent_audit.py
p24/lang_trace_gcd_plucker_kummer_descent_boundary.md
p24/lang_trace_gcd_orbit_product_formula_audit.py
p24/lang_trace_gcd_orbit_product_formula_boundary.md
```

It reports that raw determinant values, and the tested nontrivial Kummer-like
powers, do not descend on the nontrivial Frobenius orbits.  Orbit products do.
Thus the safe p24 producer theorem should target orbit products/norms unless
it separately proves a semi-invariant Plucker coordinate.  The formula audit
also finds no small fixed-row equality or power relation among the actual
orbit products in the pinned row.

Similarly, the seven orbit-product form may use:

```text
Theta_O = prod_{t in O} Theta(t)
```

provided the producer proves:

```text
Delta(t)=0 => Theta_{orbit(t)}=0.
```

The Lean interface is:

```text
p24/lean/PluckerKummerGate.lean
p24/lean/PluckerKummerOrbitNormGate.lean
```

## Updated Producer Theorem

The direct Kummer route should now target:

```text
Construct Plucker-Kummer p-units Theta(t)
attached to the actual trace-GCD determinant
Delta(t)=det(P V_t A), not merely to the matrix entries or primitive
relative traces.
```

Equivalently:

```text
construct the Kummer powers of f_trace(zeta_211^t),
or construct the cyclic-algebra element whose evaluations are those powers,
and prove their orbit norm is a p-unit.
```

This is still a producer theorem, not a certificate.  Once supplied, the
finite verifier is sub-sqrt exactly as in the trace-GCD payload manifest.
