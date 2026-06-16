# P25 KSY-y: Post-Koo-Shin 2010 Reroute

Updated: 2026-06-14 08:04 PDT

## Result

The actual Koo-Shin 2010 Theorem `5.2` has been classified:

```text
decision = reject_prime_power_only_missing_mixed_lift
```

It is useful as prime-level Siegel-product rigidity and `l`-th-root descent,
but not as a direct p25 producer.

## New Queue

1. `sprang_kronecker_d2_exact_product_specialization`

   Continue first.  A D=2 Kronecker/Sprang theorem that emits exact `P` or
   theta2/theta2-inverse divisor data would close the theorem lane.

2. `kubert_lang_mixed_exponent_product_search`

   Continue second.  The exact packet and theta2 footprints pass the
   Kubert-Lang congruence screen at mixed levels `507` and `12675`; the missing
   piece is a theorem-legal mixed-level lift/product.

3. `ksy_normalized_y_exact_distribution`

   Continue only if upgraded from formula/generation language to exact
   product distribution over the 75 atoms.

4. `koo_shin_2010_theorem52_root_descent`

   Helper only.  Use after a mixed producer appears to control constants or
   roots; do not spend a lane trying to close from Theorem `5.2` alone.

5. `c169_or_prime_level_projection_closer`

   Kill.  Prime-level projection loses the `C_3` row graph and the
   `T=(2,113)` edge.

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_koo_shin_2010_reroute_gate.py
```

Marker:

```text
ksy_y_post_koo_shin_2010_reroute_rows=1/1
```
