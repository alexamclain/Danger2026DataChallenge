# P25 v2 Arithmetic Baseline Audit

Updated: 2026-06-16

## Purpose

Verify the p25 arithmetic constants used by the production run and theorem
lanes: target prime, `k`, admissible traces, odd parts, trace discriminants,
order conductors, and order class groups.

This is not a theorem lane. It is the cheap baseline check that guards the
transfer matrix and all H0/conductor-39/exact-P routing.

## Pages Read

- `concepts/transfer-matrix.md`
- `evidence/lane_A_cm_lang_transfer.md`
- `evidence/lane_C_low_moment_w_axis.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 research/p25/archive/gates/p25_v2_arithmetic_baseline_audit_gate.py
```

The gate returned `p25_v2_arithmetic_baseline_audit_rows=1/1`.

## Target

```text
p = 10000000000000000000000013
p mod 8 = 5
sqrt_floor = 3162277660168
k = 42
```

Here `k=42` is the minimum `v2(p+1-t)` among the Pomerance-admissible p25
traces, matching the active halving depth target.

## Trace Rows

```text
t = 5808037298190
  v2(p+1-t) = 42
  odd_part = 2273736754431 = 3^2 * 601 * 420361759
  Delta = -6266702742833805022723952
  |Delta| = 2^4 * 7 * 1199351729 * 46652455412449
  D_K = -391668921427112813920247
  order conductor f = 4
  h(Delta) = 907242623448 = 2^3 * 3 * 7 * 17^2 * 37 * 505027
  class group = C_226810655862 x C_2 x C_2

t = 1409990787086
  v2(p+1-t) = 50
  odd_part = 8881784197 = 11 * 13 * 1543 * 40253
  Delta = -38011925980332602215628656
  |Delta| = 2^4 * 11 * 2465641 * 2910709 * 30093907049
  D_K = -2375745373770787638476791
  order conductor f = 4
  h(Delta) = 2397272743184 = 2^4 * 11 * 13620867859
  class group = C_299659092898 x C_2 x C_2 x C_2

t = -2988055724018
  v2(p+1-t) = 42
  odd_part = 2273736754433 = 17 * 5503 * 24304783
  Delta = -31071522990163265817935728
  |Delta| = 2^4 * 7 * 11 * 13 * 1493 * 1299417385618536931
  D_K = -1941970186885204113620983
  order conductor f = 4
  h(Delta) = 999672108288 = 2^8 * 3 * 7 * 17 * 107 * 151 * 677
  class group = C_62479506768 x C_2 x C_2 x C_2 x C_2
```

## Checks

```text
p_mod_8_ok = 1
sqrt_floor_ok = 1
k_ok = 1
trace_rows_ok = 3/3
fundamental_discriminants_ok = 3/3
order_conductors_ok = 3/3
pari_available = 1
pari_class_groups_ok = 1
p25_v2_arithmetic_baseline_audit_rows=1/1
```

## Verdict

The transfer-matrix arithmetic baseline is stable. All three admissible traces
have the recorded `v2` and odd parts; all three trace discriminants have
conductor `4`; and local PARI `quadclassunit` confirms the order class numbers
and class groups used by the CM/Lang, low-moment, and W-axis postmortems.
