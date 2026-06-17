# P25 v2 Quotient-H90 Idempotent Mechanism

Updated: 2026-06-16

## Purpose

Explain why the four mod-13 rectangle rows share the same Hilbert-90 boundary.
This turns the column-level pattern into a source-theorem mechanism:

```text
V_{o,e} = 6 * chi_3_row * (1_{oH} - 1_{eH})
```

where `oH` is one nonsquare order-3 coset and `eH` is one square order-3
coset in `(Z/13Z)^*/<3>`.

This is still not the missing arithmetic value/divisor theorem.  It is the
smallest current source-side object a theorem should preserve.

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_mod13_coset_rectangle_20260616.md`
- `evidence/p25_v2_mixed_signed_column_fingerprint_20260616.md`
- `evidence/p25_v2_unified_value_divisor_interface_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_quotient_h90_idempotent_mechanism_gate.py
```

The gate returned `p25_v2_quotient_h90_idempotent_mechanism_rows=1/1`.

## Mechanism

Let:

```text
H = <3> = (1, 3, 9)
(Z/13Z)^* / H ~= C4
Frob_p mod 13 = 10
10H = 4H
```

So Frobenius shifts the `C4` coset index by `2`.  Also:

```text
p mod 3 = 2
```

so Frobenius swaps the two `C_3` rows.  Combining the row flip with the
coset-index shift explains the common boundary:

```text
(1 - Frob_p) V_{o,e} = W
```

for every odd/even coset edge `V_{o,e}`.

## Legal Idempotent Differences

```text
m=1: odd plus = 7H, even minus = 4H
m=2: odd plus = 7H, even minus = H
m=4: odd plus = 2H, even minus = H
m=8: odd plus = 2H, even minus = 4H
```

All four have:

```text
support = 12
boundary = W
W support = 24
W coefficients = +/-6
```

## Controls

```text
same parity odd/odd:
  boundary = 0, not W

same parity even/even:
  boundary = 0, not W

broad quadratic character:
  support = 24
  boundary = 2W, not W
```

Thus the source object is neither a generic Hilbert-90 boundary nor the full
quadratic character.  It is a sparse quotient-`C4` idempotent difference.

## Routing Rule

A source theorem should now be classified as promising only if it can emit or
specialize to:

```text
one sparse odd/even C4 idempotent difference V_{o,e}
+ the conductor-39 row sign chi_3_row
+ Hilbert-90 boundary W = Norm_156(Y_507)
+ finite value/divisor theorem
```

Same-parity edges, full quadratic-character language, and boundary-only
claims are repair or reject rows.

## Verdict

```text
legal_rows_ok = 4/4
control_rows_ok = 3/3
source_theorem_in_hand = 0
direct_closer = 0
next = look for a finite divisor/additive or period-156 value theorem for one
       sparse quotient-C4 idempotent difference V_{o,e}
```
