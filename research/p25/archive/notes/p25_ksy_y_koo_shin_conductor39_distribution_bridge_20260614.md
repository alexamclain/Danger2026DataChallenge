# P25 KSY-y Koo-Shin Versus Conductor-39 Distribution Source

Updated: 2026-06-14 09:47 PDT

## Question

The Yang `Y_507` period norm has now been compressed to

```text
Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi)
U_chi = -chi_3 * chi_13 on X_1(39)
507 = 13 * 39
```

This asks whether the actual Koo-Shin 2010 Theorem `5.2`, already classified
as a prime-level Siegel-product/root-descent theorem, becomes a direct source
for p25 after the conductor-`39` descent.

## Result

It does not become a direct closer.

The live source is a genuinely mixed tensor:

```text
source level              = 39
target level              = 507
Yang lift length          = 13
U_chi support             = 24
mod 3 rows                = 2
mod 13 columns            = 12
row2 = -row1              = true
proper pushforwards       = 0
prime13 projection support = 0
mod3 projection support    = 0
```

So the prime-`13`/`C169` projection route erases the object instead of
producing it.  The missing theorem is not a prime-level product alone; it is a
mixed conductor-`39` theorem preserving the `chi_3` row sign, the `chi_13`
column character, and the Yang `13`-fiber lift.

## Koo-Shin Role

Koo-Shin 2010 Theorem `5.2` remains useful as context:

```text
prime_level_rigidity = 1
root_descent_helper  = 1
emits_mixed_tensor_source = 0
closes_distribution_source = 0
```

Use it after a separate mixed producer appears, for constant-product rigidity
or root descent.  Do not spend a direct lane trying to close p25 from
Theorem `5.2` alone.

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_koo_shin_conductor39_distribution_bridge_gate.py
```

Expected marker:

```text
ksy_y_koo_shin_conductor39_distribution_bridge_rows=1/1
```
