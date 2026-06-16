# p23 Transfer To p24 Scaling Audit

This note checks what survives from the successful p23 method when the target
is raised to

```text
p = 10^24 + 7
k = 40.
```

## What Transfers

The p23 method used a fixed `X1(16)` model, nonsplit Montgomery structure, and
the cyclic 2-Sylow branch-collapse fact.  The branch-collapse theorem still
applies:

```text
nonsplit Montgomery => rational 2-Sylow is cyclic
all rational halves have the same future halving depth
```

so first-branch halving is complete inside the nonsplit family.  This is a
good constant-factor implementation improvement.

The p24-congruence calibration also confirms the same basic behavior on a
small prime with the same residue pattern:

```text
calibration_prime = 57527
p_mod_8 = 7
accepted_x16 = 5000
nonsplit = 2486

nonsplit survive_depth_8  = 208/2486 = 0.083669
nonsplit survive_depth_12 = 28/2486  = 0.011263
nonsplit survive_depth_14 = 0/2486
```

## Why This Is Not A p24 Asymptotic Win

Fixed `X1(16)` prescribes only the first four bits of oriented 2-power
structure.  For p24, the verifier needs depth `40`, so the remaining tail is
still `36` bits.

The tower cost audit records the exact accounting:

```text
ordinary lift from X1(16) to X1(2^h):  2^(h-4)
residual tail to depth 40:             2^(40-h)
product:                               2^36
product/sqrt(p):                       0.06871948
```

That is a strong constant factor, not a smaller exponent.  To become a true
asymptotic speedup, a growing-level sampler must cost

```text
2^(beta*(h-4)) with beta < 1.
```

The exact small-field oriented-depth audit does not show such a sublinear
sampler.  On exact `p=n^2+7`, `n == 0 mod 8` calibration rows:

```text
aggregate_fitted_beta_x1 = 0.872407   (shallow, noisy rows)
aggregate_fitted_beta_x0 = 0.000000   (but X0 omits orientation)
```

Deeper/broader earlier runs in this folder put the oriented exponent near
one.  The current interpretation is unchanged:

```text
X1-oriented depth costs about one bit per bit;
X0 depth is cheap only because it forgets the verifier orientation.
```

## First-Lift Feature Scan

The first cover above the fixed `X1(16)` model is

```text
z^2 = (y - 1)(y^2 - 2)(y^2 - 2y + 2).
```

If p23's method hid a reusable tower phase label, low-degree norm characters
on this cover would be a natural place to see it.  A p24-congruence scan with
5000 accepted rows gave only constant lifts:

```text
base depth-12 rate = 120/5000 = 0.024
best bucket lift   = 1.293996
best capture       = 80/120 = 0.666667
```

This matches the previous larger scans: these labels can rebalance a shard by
constants, but do not expose the missing depth-growing tower section.

## Boundary

The p23 method remains operationally valuable as a fixed-level sampler and
branch simplifier.  It does not prove or supply the requested p24
asymptotic speedup.

A p24 improvement from this line would need a new growing-level section of
the `X1(2^h)` tower with overhead exponent `beta < 1`, or a p-specific label
that predicts the remaining Frobenius-fixed ray tail.  The current exact
calibrations do not show one.

Commands:

```text
python3 p24/x16_p24_calibration.py --samples 5000 --target-depth 18 --seed 20260604
/Users/agent/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  p24/partial_oriented_sampler_exponent_audit.py \
  --min-p 10000 --max-p 90000 --max-rows 4 --n-modulus 8 --n-residue 0 --fit-min-depth 4
python3 p24/x1_tower_mitm_cost_audit.py
python3 p24/x16_first_lift_p24_feature_scan.py \
  --accepted 5000 --target-depth 12 --depths 6 8 10 12 --seed 20260604 --report-top 12
```
