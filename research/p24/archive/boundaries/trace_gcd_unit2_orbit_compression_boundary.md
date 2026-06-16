# Trace-GCD Unit-2 Orbit Compression Boundary

Date: 2026-06-06

This note isolates the finite right-unit symmetry that could shrink the
trace-GCD orbit-norm payload further if the arithmetic producer is
equivariant.

## Finite Audit

Script:

```text
p24/trace_gcd_unit2_orbit_compression_audit.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 python3 \
  p24/trace_gcd_unit2_orbit_compression_audit.py
```

Output:

```text
right=211
frobenius_multiplier=114
unit=2
orbit_count=7
orbit_lengths=[1, 35, 35, 35, 35, 35, 35]
unit_action_mapping={0: 0, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 1}
zero_orbit_fixed=1
nonzero_cycle=[1, 2, 3, 4, 5, 6]
nonzero_cycle_covers_all_nonzero_orbits=1
```

Thus multiplication by `2 mod 211` fixes the zero orbit and cycles the six
nonzero Frobenius orbits.

## Conditional Compression

If the arithmetic producer proves that unit-2 multiplication carries the
actual p24 determinant-line/Fitting section for one nonzero orbit to the next
one up to p-unit scaling, then:

```text
Pi_O1 is a p-unit
  => Pi_O2, Pi_O3, Pi_O4, Pi_O5, Pi_O6 are p-units.
```

Together with the fixed orbit:

```text
Pi_O0 is a p-unit,
```

the finite payload could shrink from:

```text
seven orbit products plus inverses = 14 F_p elements
```

to:

```text
fixed orbit product plus inverse
+ one nonzero representative product plus inverse
= 4 F_p elements.
```

If the producer proves the stronger global operator norm is honest, the
payload is still:

```text
global norm plus inverse = 2 F_p elements.
```

The finite implication is now also pinned in:

```text
p24/lean/UnitOrbitGate.lean
p24/lean/TraceGcdDiamondEquivarianceGate.lean
p24/lean/TraceGcdTwoOrbitCompressionGate.lean
```

which proves:

```text
fixed orbit p-unit
+ one representative p-unit on the six-cycle
+ p-unit-preserving arrows around the cycle
=> all seven orbit p-units.
```

It also records:

```text
4 < 14 < sqrt(10^24+7).
```

## Boundary

The finite orbit map is not the theorem.  The necessary arithmetic input is:

```text
the embedded 157/211 phase construction, Lang-coordinate choices, and
selected tail windows are equivariant under multiplication by 2, and the
induced determinant-line comparison has p-unit transition factors.
```

Without that input, the safe executable verifier remains:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py
```

checking all seven orbit norms.  The unit-2 compression is therefore a
producer-theorem opportunity, not a standalone certificate.

A small actual-CM warning test is:

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

On the pinned `right=7` row, a right unit swaps the two nonzero Frobenius
orbits.  The orbit norms remain p-units but are not literally equal:

```text
literal_equal_edges=0/4
punit_ratio_edges=4/4
```

So the p24 theorem should be stated with p-unit transition factors, not with
literal equality of scalar representatives.

The proof-facing target that separates equivariance from representative
nonvanishing is:

```text
p24/trace_gcd_diamond_fitting_equivariance_target.md
p24/trace_gcd_two_linearized_resultant_target.md
```

It reduces the unit-compressed route to:

```text
1. diamond-equivariant p-integral determinant lines with p-unit transition
   factors;
2. Xi_O0 and one nonzero representative Xi_O1 are p-units.
```

The executable compressed verifier schema is:

```text
p24/trace_gcd_orbit_norm_certificate_verifier.py --unit2-schema
```
