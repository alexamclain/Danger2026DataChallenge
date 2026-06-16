# P25 KSY-y H0 Translate Boundary/Value Ambiguity

Updated: 2026-06-14 15:40 PDT

## Purpose

After the Koo-Shin 6.2 screen, the active H0 products are legal source
objects.  The remaining question is not legality; it is whether a theorem has
actually selected the finite value or divisor identity strongly enough to avoid
the old branch ambiguity.

## Arithmetic

```text
support period      = 156
ambient period      = 780
gcd(4^156 - 1, p-1) = 1
gcd(4^780 - 1, p-1) = 11
ord_39(p)           = 6
sqrt(-39) in F_p    = no
```

So the selected support-period route has a unique `F_p^*` branch, while the
ambient-period shadow keeps a `mu_11` ambiguity.  Direct shortcuts using a
primitive order-39 root in `F_p` or a `sqrt(-39)` scalar are rejected.

## Rows

```text
1. Koo-Shin 6.2 + H0 boundary only
   decision = source_certified_value_or_divisor_missing
   closes   = no
   missing  = finite-field value/divisor theorem for one exact H0 product

2. Ambient/bare H0 value branch
   decision = conditional_missing_period_156_context
   closes   = no
   missing  = period-156 branch/root/telescoping context

3. Support-period-156 H0 value
   decision = source_theorem_closed_policy_or_framing_missing
   closes   = source stage only
   missing  = DANGER3 finite-identity/non-CM framing

4. H0 divisor/additive identity
   decision = source_theorem_closed_policy_or_framing_missing
   closes   = source stage only
   missing  = DANGER3 finite-identity/non-CM framing

5. Finite payload without source theorem
   decision = conditional_finite_payload_without_source_theorem
   closes   = no
   missing  = challenge-legal arithmetic source theorem

6. Direct F_p order-39 root shortcut
   decision = reject_direct_Fp_order39_root_shortcut
   closes   = no
   missing  = primitive 39th roots first occur over degree 6

7. sqrt(-39) scalar shortcut
   decision = reject_sqrt_minus39_scalar_shortcut
   closes   = no
   missing  = sqrt(-39) is not in F_p

8. Degree-6 norm descent bare value
   decision = conditional_value_theorem_missing_period156_context
   closes   = no
   missing  = period-156 branch/root/telescoping context
```

## Counts

```text
row_count                  = 8
source_certified_only_rows = 1
ambient_mu11_rows          = 1
branch_unique_rows         = 2
source_closing_rows        = 2
conditional_rows           = 3
rejected_shortcut_rows     = 2
submission_ready_rows      = 0
```

## Interpretation

This is the current H0 source-side fork:

```text
boundary only                     -> not enough
ambient/bare finite value          -> not enough
period-156 finite value theorem    -> closes source stage
divisor/additive identity          -> closes source stage
direct order-39 or sqrt(-39) trick -> rejected
```

After either source-closing row, the next wall is still DANGER3 framing,
cross-level extraction to `X_1(16)`, and official `vpp.py`.

## Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_h0_translate_boundary_value_ambiguity_gate.py
```

Marker:

```text
ksy_y_h0_translate_boundary_value_ambiguity_rows=1/1
```
