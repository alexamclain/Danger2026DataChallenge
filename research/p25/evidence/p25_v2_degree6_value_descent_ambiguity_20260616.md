# P25 v2 Degree-6 Value Descent Ambiguity

Updated: 2026-06-16

## Purpose

Make the value-side degree-6 ambiguity explicit for H0/conductor-39 source
snippets.  A conductor-39 value formula naturally may live over `F_{p^6}` for
`p = 10^25 + 13`; that is not a source-stage close unless the source also gives
descent back to the selected `F_p` support-156 row, or an equivalent
Hilbert-90 ratio boundary.

This is a classifier, not a theorem.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_norm_only_descent_ambiguity_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_degree6_value_descent_ambiguity_gate.py
```

The gate returned `p25_v2_degree6_value_descent_ambiguity_rows=1/1`.

## Arithmetic Contract

```text
p mod 3 = 2
p mod 13 = 10
p mod 39 = 23
ord_3(p) = 2
ord_13(p) = 6
ord_39(p) = 6
p^3 = -1 mod 39
sqrt(-39) in F_p = no
gcd(4^156 - 1, p - 1) = 1
gcd(4^780 - 1, p - 1) = 11
```

Consequences:

```text
primitive 3rd roots first appear over degree 2
primitive 13th and 39th roots first appear over degree 6
direct F_p order-39 root shortcuts are unavailable
sqrt(-39) scalar shortcuts are unavailable
support-period-156 value roots are unique in F_p^*
ambient-period-780 values still have mu_11 ambiguity
```

## Decisions

```text
degree6_value_with_explicit_fp_descent
  decision = normalize_value_descent_then_apply_source_snippet_intake
  missing  = same theorem data after explicit F_p descent and row selection

degree6_value_orbit_without_descent
  decision = repair_degree6_orbit_without_descent
  missing  = conjugate/norm descent back to F_p or Hilbert-90 ratio boundary

primitive_root_expression_degree6_only
  decision = repair_degree6_orbit_without_descent
  missing  = conjugate/norm descent back to F_p or Hilbert-90 ratio boundary

degree6_norm_without_selected_row
  decision = repair_descent_without_selected_legal_row
  missing  = legal support-156 row selection after descent

degree6_selected_row_without_period156_or_h90
  decision = repair_period156_or_h90_context_missing
  missing  = support-period-156 branch/root/telescoping context or H90 boundary

direct_fp_order39_root_shortcut
  decision = reject_direct_fp_order39_or_sqrt_minus39_shortcut
  falsifier = ord_39(p)=6 and sqrt(-39) is not in F_p

sqrt_minus39_scalar_shortcut
  decision = reject_direct_fp_order39_or_sqrt_minus39_shortcut
  falsifier = ord_39(p)=6 and sqrt(-39) is not in F_p
```

## Counts

```text
normalize_rows = 1
repair_rows = 4
reject_rows = 2
current_source_stage_closers = 0
```

## Verdict

Degree-6 value language is a useful source hint, not a close.  The acceptable
normalization is:

```text
degree-6 formula/orbit
+ explicit descent to F_p
+ selected legal support-156 row
+ period-156 branch/root/telescoping context or H90 boundary
-> source-snippet intake
```

Anything weaker is repair unless it tries to choose an order-39 root or
`sqrt(-39)` directly in `F_p`, in which case it is rejected.
