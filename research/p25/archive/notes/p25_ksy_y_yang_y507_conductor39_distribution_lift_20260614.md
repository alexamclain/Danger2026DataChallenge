# P25 KSY-y Yang Y_507 Conductor-39 Distribution Lift

Updated: 2026-06-14 09:41 PDT

## Result

The level-`507` period norm of Yang's `Y_507` is exactly the `13`-fiber
distribution lift of the primitive mixed conductor-`39` unit:

```text
507 = 13 * 39
U_chi = -chi_3 * chi_13 on X_1(39)
Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi)
```

Equivalently, each nonzero residue `a mod 39` in `6*U_chi` expands to the
constant fiber

```text
a, a+39, a+2*39, ..., a+12*39 mod 507.
```

The support and coefficient counts scale cleanly:

```text
6*U_chi support                 = 24
6*U_chi coefficient counts      = (-6,12), (6,12)
distribution-lift support       = 312
Norm_156(Y_507) support         = 312
lift/Norm coefficient counts    = (-6,156), (6,156)
```

The executable gate verifies:

```text
lift_length = 13
lifted_equals_period_norm = 1
period_norm_equals_six_lifted_primitive = 1
all_fibers_constant = 1
```

## Interpretation

This converts the previous level-`507` period-norm object into a smaller
source target: a primitive legal mixed character unit on `X_1(39)`, followed
by Yang distribution from level `39` to level `507`.

The unit is still genuinely mixed:

```text
U_chi(r) = -chi_3(r) * chi_13(r)
```

so proper conductor-`3`, proper conductor-`13`, projection-only, pullback-only,
or additively separated explanations remain rejected.

## Boundary

This is a serious compression of the source side, not a completed p25
certificate.  The missing clauses are still:

```text
finite-field value or divisor theorem for the source object
period/branch/descent context that survives Frobenius anti-invariance
DANGER3 extraction of concrete (A, x0)
official vpp.py verification
```

The practical recommendation is to aim source theorems at `U_chi` on `X_1(39)`
plus Yang distribution to `X_1(507)`, and reject level-`507` stories that do
not descend to this 13-fiber lift.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_yang_y507_conductor39_distribution_lift_gate.py
```

Expected marker:

```text
ksy_y_yang_y507_conductor39_distribution_lift_rows=1/1
```
