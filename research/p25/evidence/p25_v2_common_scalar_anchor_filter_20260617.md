# P25 v2 Common-Scalar Anchor Filter

Updated: 2026-06-17

Marker: `p25_v2_common_scalar_anchor_filter_rows=1/1`

## Purpose

Make the first-anchor obstruction mechanical. The four legal
H0/conductor-39 row values can all be multiplied by a common unknown scalar
without changing quotient-only data. A proposed theorem creates the first
absolute row anchor only when its finite value breaks that common-scalar
symmetry.

This page is not a source theorem. It is an intake filter for future expert
answers, source snippets, or proof attempts.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md`
- `evidence/p25_v2_fpstar_branch_factorization_20260617.md`
- `evidence/p25_v2_extended_unique_power_intake_20260617.md`
- `evidence/p25_v2_zero_lattice_transfer_contract_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_common_scalar_anchor_filter_gate.py
```

The gate returned `p25_v2_common_scalar_anchor_filter_rows=1/1`.

## Arithmetic Check

```text
p - 1 = 10000000000000000000000012
factorization = 2^2 * 11 * 23 * 9881422924901185770751
```

For a finite product/value claim whose exponent-vector has coefficient sum
`d`, a common rescaling of all four rows by `c in F_p^*` rescales the claimed
value by `c^d`. Therefore:

```text
gcd(d, p - 1) = 1     exact value can fix the common scalar
gcd(d, p - 1) > 1     root/branch ambiguity remains
d = 0                 quotient/zero-lattice data never fixes the first scalar
```

The period-value side has the analogous branch test:

```text
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

## Filter Rows

```text
zero_lattice_or_quotient
  coefficient_sum = 0
  decision        = transfer_only_never_first_anchor
  reason          = common F_p^* scalar is invisible

direct_one_edge
  coefficient_sum = 1
  decision        = anchors_common_scalar_if_source_theorem_present
  reason          = one exact scalar-fixed row value is the missing anchor

pair_diagonal_or_q_square
  coefficient_sum = 2
  gcd             = 2
  decision        = two_root_payload_not_anchor
  reason          = oriented square root/sign is still missing

projector_or_all_four_edge
  coefficient_sum = 4
  gcd             = 4
  decision        = four_root_or_selector_repair
  reason          = fourth-root/scalar selection and row selector are still due

q6_or_sixfold_boundary
  coefficient_sum = 6
  gcd             = 2
  decision        = boundary_repair_not_anchor
  reason          = two branches remain and source-side selector is missing

unit_power_values
  exponents       = 3, 5, 13, 39, 75, 169, 507
  gcd             = 1 for each exponent
  decision        = anchors_after_inverse_exponent_if_exact_and_row_labeled
  reason          = exact finite value plus row label can recover R_m

mu11_ambiguous_power
  coefficient_sum = 11
  gcd             = 11
  decision        = eleven_branch_repair
  reason          = branch/scalar selection is still missing

support_period156_value
  branch_gcd      = gcd(4^156 - 1, p - 1) = 1
  decision        = unique_period_branch_if_source_supplies_exact_payload
  reason          = uniqueness helps only after a real source theorem and row bridge

ambient_period780_value
  branch_gcd      = gcd(4^780 - 1, p - 1) = 11
  decision        = ambient_eleven_branch_repair
  reason          = period-156 branch/root/telescoping or additive normalization is missing
```

## Counts

```text
evidence_markers_ok = 7/7
anchor_filter_rows = 9
scalar_fixing_rows = 3
transfer_only_rows = 1
root_or_branch_debt_rows = 5
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_common_scalar_anchor_filter_rows=1/1
```

## Verdict

The missing first anchor can now be screened by one rule:

```text
An exact finite theorem fixes the common row scalar only if its coefficient
sum, or its period branch exponent, is invertible modulo p - 1.
```

This promotes three shapes as real anchor candidates if a source theorem
supplies the finite payload:

```text
direct one-edge value/additive identity
exact row-labeled unit-power value, including powers 75, 169, or 507
support-period-156 value with the legal-row bridge
```

It also keeps quotient/zero-lattice, pair/diagonal/Q-square, projector,
sixfold boundary, `mu_11`, and ambient-period-780 answers out of source-stage
promotion until their specific scalar/root/branch debt is paid.
