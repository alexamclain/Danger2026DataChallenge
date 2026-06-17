# P25 v2 Unified Source-Theorem Gap

Updated: 2026-06-16

## Purpose

Check whether the unified H0/conductor-39 target still has hidden
combinatorial freedom, or whether the remaining gap is genuinely arithmetic.

This pass wraps the existing Hilbert-90, sparse Yang-lift, and product
normal-form gates.  It is meant to prevent more drift into selector/gauge
searches once those choices have already been saturated.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `concepts/transfer-matrix.md`
- `evidence/p25_v2_h0_conductor39_unified_target_20260616.md`
- `evidence/p25_v2_unified_submission_extraction_contract_20260616.md`
- `evidence/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_hilbert90_boundary_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_sparse_hilbert90_yang_lift_20260614.md`
- `archive/notes/p25_ksy_y_yang_y507_conductor39_sparse_h90_product_normal_form_20260614.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_unified_source_theorem_gap_gate.py
```

The gate returned `p25_v2_unified_source_theorem_gap_rows=1/1`.

## Saturated Layers

The source-side group-ring layers are now saturated:

```text
Hilbert-90 boundary:
  h90_orbit_rows = 4
  h90_total_min_support = 12

Sparse Yang lift:
  legal_sparse_lift_count = 4
  formal_one_coset_lift_count = 2
  min_legal_lifted_potential_support = 156
  balanced_lifted_potential_support = 312

Product normal form:
  legal_product_rows = 4
  quotient_representatives = (1, 2, 4, 8)
  canonical_stabilizer = (1, 16, 22)
  legal_rows_are_one_orbit = yes
  legal_rows_are_78_over_78 = yes
  formal_one_coset_controls_rejected = yes
```

The formal one-coset controls have the right Frobenius boundary but fail the
mixed-axis tests, so they are not live theorem targets. The legal rows are one
doubling orbit of support-156, 78-over-78 products.

## Layer Verdict

```text
source_legality:
  status = satisfied
  next = do not reprove source legality unless a new theorem route depends on it

hilbert90_boundary:
  status = satisfied_not_closer
  next = turn boundary into a finite value/divisor theorem

legal_sparse_yang_lift:
  status = satisfied_not_closer
  next = prove a value/divisor identity for one legal support-156 potential

unified_product_normal_form:
  status = satisfied_not_closer
  next = source theorem must hit one of the four legal rows

source_stage_value_or_divisor_theorem:
  status = missing
  next = finite value/divisor theorem with Norm_156(Y_507) boundary

submission_extraction:
  status = missing
  next = DANGER3 framing, same-j X1(8112), X1(16), halving/x0, vpp.py
```

## Meaning

There is no evidence of useful hidden selector or gauge freedom left in the
first-pass target.  Source legality, Hilbert-90 boundary, sparse selector,
Yang lift, and product normal form are positive artifacts, but they are not
source-stage closers.

The next theorem-stage win must add an arithmetic statement:

```text
finite value/divisor theorem
for one legal support-156 product
with boundary Norm_156(Y_507)
```

Equivalently, an incoming source theorem may use H0 language or conductor-39
language, but it has to add the value/divisor identity.  A different gauge,
one-coset sparse potential, product rewrite, or boundary-only claim is now a
falsified shape unless it also supplies that theorem.

## Verdict

```text
continue_first_pass = yes
hidden_selector_or_gauge_freedom_remaining = no
current_source_theorem_rows = 0
remaining_gap = finite arithmetic value/divisor theorem for one legal
                support-156 product with Norm_156(Y_507) boundary
falsifier_for_next_attempt = reject any proposal that only changes
                             gauge/selector/product normal form without
                             adding a value/divisor theorem
```
