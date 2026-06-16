# CM Simple-Root/Different Boundary

Date: 2026-06-06

This note closes another tempting p-adic shortcut.

## Question

The p24 prime is ordinary, split, unramified, and prime to all certificate
levels.  A natural hope is:

```text
the CM root is a simple root of the class polynomial mod p
  => the desired Schubert/Fitting determinant is a p-unit.
```

This is false as a theorem shape.  The simple-root/different unit says the CM
algebra is etale at the prime.  It does not say that a separate determinant
section avoids zero at the selected CM point.

## Pinned Actual-CM Check

The script:

```text
p24/cm_simple_root_different_boundary.py
```

uses the pinned actual-CM row:

```text
D=-13319
q=13463
h=140
m=28
pair=(4,7)
```

It checks:

```text
class_polynomial_degree=140
root_count_mod_q=140
class_polynomial_split_squarefree=1
zero_derivative_count=0
```

So every CM root is simple modulo `q`; the different is a unit at this
splitting prime.

Then it gives two controls.

First, the trivial section:

```text
X - j_0
```

vanishes at one simple CM root while:

```text
derivative_unit_at_zero_root=1.
```

Second, the Fitting-style determinant control from the phase-divisor holdout
has:

```text
actual_det_nonzero=1
actual_entries_all_nonzero=1
control_entries_all_nonzero=1
coordinate_power_nonzero=1
control_det_zero=1
```

Thus coordinate-level p-units and CM different p-units do not detect
determinant-line vanishing.

## Consequence

The selected-tail p24 theorem cannot be replaced by:

```text
H_D'(j) is a p-unit,
or the ring class algebra is split etale at p,
or the ordinary CM root is Hensel-simple.
```

Those facts are necessary local hygiene.  The proof still has to show that
the selected-tail Schubert/Fitting section itself is a p-unit, either by:

```text
1. a phase-aware divisor/local-intersection theorem for that section; or
2. a direct p-adic noncancellation theorem for the determinant line.
```

For the p24 target this means the local ordinary friendliness recorded in

```text
p24/trace_gcd_p24_local_intersection_invariants.md
```

is not the missing theorem.  The missing theorem remains the selected-tail
phase-aware determinant-line p-unit.
