# P25 v2 Affine Row Normal Form

Updated: 2026-06-17

Marker: `p25_v2_affine_row_normal_form_rows=1/1`

## Purpose

Give a deterministic intake rule for arbitrary products of the four legal rows
`(m1,m2,m4,m8)`. This generalizes the affine row-product classifier from named
examples to any row-exponent vector a source theorem or expert reply might
produce.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_basis_sensitive_anchor_sieve_20260617.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_affine_row_product_classifier_20260617.md`
- `evidence/p25_v2_current_theorem_kernel_20260617.md`
- `evidence/p25_v2_drew_kernel_review_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_affine_row_normal_form_gate.py
```

The gate returned `p25_v2_affine_row_normal_form_rows=1/1`.

## Normal Form

Let a finite theorem produce an exact value for

```text
R^v = R_1^a R_2^b R_4^c R_8^d
v = (a,b,c,d)
s = a+b+c+d
```

For any chosen target row `e_m`, define the matched quotient debt

```text
z_m = v - s*e_m.
```

Then `z_m` has coefficient sum zero, so it lies in the zero lattice generated
by

```text
q2_1 = (-1,1,0,0)
q4_1 = (-1,0,1,0)
q8_1 = (-1,0,0,1)
```

The exact identity is

```text
R^v / R^z_m = R_m^s.
```

This is why a full zero-lattice basis is stronger than needed for a specific
aggregate: the intake only needs the exact matched quotient value for that
`z_m`.

## Decisions

```text
s = 0:
  transfer-only quotient data; never the first absolute row anchor.

gcd(s,p-1) = 1 and z_m = 0:
  direct row-labeled unique power; route through the current theorem kernel.

gcd(s,p-1) = 1 and z_m != 0:
  route through the current theorem kernel only if the exact matched value
  R^z_m is also supplied.

gcd(s,p-1) > 1:
  even with R^z_m, the result is R_m^s and still carries root/scalar debt.
```

## Examples

Coordinates are `(m1,m2,m4,m8)`, targeting `m1`.

```text
direct_unit_row
  v=(1,0,0,0), s=1, z=(0,0,0,0)
  decision=direct_row_power

row_labeled_power_75
  v=(75,0,0,0), s=75, z=(0,0,0,0), gcd(75,p-1)=1
  decision=direct_row_power

unit_sum_nonedge_minus_q
  v=(2,-1,0,0), s=1, z=(1,-1,0,0)=-q2_1
  decision=matched_quotient_then_inverse_power

unit_power_nonedge_plus_q
  v=(2,1,0,0), s=3, z=(-1,1,0,0)=q2_1, gcd(3,p-1)=1
  decision=matched_quotient_then_inverse_power

zero_lattice_quotient
  v=(-1,1,0,0), s=0, z=(-1,1,0,0)=q2_1
  decision=transfer_only

nonunit_pair_sum
  v=(1,1,0,0), s=2, z=(-1,1,0,0)=q2_1, gcd(2,p-1)=2
  decision=matched_quotient_still_root_debt

all_four_product
  v=(1,1,1,1), s=4, z=(-3,1,1,1)=q2_1+q4_1+q8_1, gcd(4,p-1)=4
  decision=matched_quotient_still_root_debt
```

## Counts

The gate exhaustively checks all `625` vectors in `[-2,2]^4` against all four
target rows, giving `2500` target normal forms.

```text
direct_row_power = 8
matched_quotient_then_inverse_power = 1240
matched_quotient_still_root_debt = 912
transfer_only = 340
current_matched_zero_lattice_packets = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_affine_row_normal_form_rows=1/1
```

## Verdict

Any aggregate row-product answer should now be normalized before changing a
lane status. Unit-sum aggregates are promising only when the source also gives
the exact matched quotient value. Zero-sum aggregates transfer an existing
anchor but do not create one. Nonunit sums still need root/scalar repair.

This does not broaden the moonshot; it makes the Drew/source intake sharper by
forcing aggregate answers back through the current theorem kernel exactly when
the quotient and exponent data make that legitimate.
