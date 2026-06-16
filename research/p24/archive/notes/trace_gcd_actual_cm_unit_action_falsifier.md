# Trace-GCD Actual-CM Unit-Action Falsifier

Date: 2026-06-06

This note records a small actual-CM test for the right-unit equivariance
theorem boundary.

## Script

```text
p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

Run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_actual_cm_unit_action_falsifier.py
```

The script reuses the pinned actual trace-GCD row:

```text
D=-13319, q=13463, h=140, m=28, n=5,
left=4, right=7, q mod right=2.
```

Frobenius has two nonzero right orbits:

```text
[1,2,4] and [3,6,5].
```

The right unit `3 mod 7` swaps them.

## Output

The actual Fitting orbit norms are:

```text
omitted=0:
  O1 norm=2515
  O3 norm=603

omitted=1:
  O1 norm=9495
  O3 norm=6085
```

Therefore:

```text
literal_equal_edges=0/4
punit_ratio_edges=4/4
```

## Interpretation

This falsifies the overstrong shortcut:

```text
right-unit action makes printed orbit norms literally equal.
```

The actual theorem needed for p24 is weaker and invariant:

```text
right-unit action carries determinant lines to determinant lines
with p-unit transition factors.
```

Under that theorem, p-unit nonvanishing propagates around the unit orbit even
though the printed scalar representatives can differ by nontrivial units.
This is exactly the distinction recorded in:

```text
p24/right_unit_equivariance_theorem.md
p24/trace_gcd_unit2_orbit_compression_boundary.md
p24/lean/UnitOrbitGate.lean
```

The experiment is useful because it prevents the proof target from drifting
toward a false equality theorem while preserving the viable p-unit-scale
equivariance theorem.
