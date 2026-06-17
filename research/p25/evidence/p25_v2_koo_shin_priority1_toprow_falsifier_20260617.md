# P25 v2 Koo-Shin Priority-1 Top-Row Falsifier

Updated: 2026-06-17

Marker: `p25_v2_koo_shin_priority1_toprow_falsifier_rows=1/1`

## Purpose

Resolve the first row of the priority-1 source lookup capsule against the
local Koo-Shin 2010 paper. The question is narrow:

```text
Does Koo-Shin 2010 already contain a finite scalar-fixed divisor/additive
theorem for one legal H0/conductor-39 support-156 row with Norm_156(Y_507)
boundary?
```

The answer is no. Koo-Shin remains useful prior art, but not as the current
priority-1 closer.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `incoming/extracted/s00209-008-0456-9.pdf.extract.txt`
- `evidence/p25_v2_priority1_source_lookup_capsule_20260617.md`
- `evidence/p25_v2_priority1_divisor_additive_work_order_20260617.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_additive_normalizer_source_scan_20260616.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md`
- `evidence/p25_ksy_y_h0_koo_shin_source_clause_matrix_20260614.md`
- `evidence/p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_20260614.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_koo_shin_priority1_toprow_falsifier_gate.py
```

The gate returned `p25_v2_koo_shin_priority1_toprow_falsifier_rows=1/1`.

## Source Profile

The raw local extract contains the useful Koo-Shin surfaces we expected:

```text
Theorem 5.2
Lemma 6.1
Theorem 6.2
Corollary 7.3
Theorem 9.8
Theorem 9.10
Theorem 9.11
```

The same extract does not contain the current closer vocabulary:

```text
Norm_156
Y_507 / Y507
Hilbert-90 / Hilbert 90
period-156 / period 156
support-156
scalar-fixing
finite additive
additive identity
divisor identity
telescoping
basepoint
```

This absence is not a proof that no reformulation exists elsewhere, but it is
a sharp falsifier for treating Koo-Shin 2010 itself as already containing the
priority-1 theorem.

## Clause Rows

```text
theorem52_prime_level_constant_product
  useful_as          = rigidity and root-descent context
  priority1_missing = nonzero constant legal quotient-C4 row or scalar-fixed
                      finite row theorem
  decision           = reject_as_priority1_closer_keep_as_context

lemma61_distribution_formula
  useful_as          = full-fiber order/distribution support
  priority1_missing = one legal support-156 row plus finite scalar-fixing
                      identity
  decision           = helper_not_priority1_closer

theorem62_x1n_siegel_product_legality
  useful_as          = H0/conductor-39 source legality certificate
  priority1_missing = finite value/divisor/additive theorem for the legal row
  decision           = source_certified_value_theorem_missing

section7_ramanujan_value_evaluation
  useful_as          = example of value evaluation after a different generator
                      setup
  priority1_missing = one of the four legal H0/conductor-39 support-156 rows
  decision           = context_not_priority1_closer

section9_ray_class_generators
  useful_as          = class-field generator vocabulary
  priority1_missing = DANGER3 finite row identity with Norm_156(Y_507)
                      boundary
  decision           = context_not_priority1_closer
```

## Counts

```text
evidence_markers_ok = 8/8
raw_source_available = 1
present_surfaces = 7
absent_closer_terms = 15
clause_rows = 5
current_koo_shin_priority1_source_theorems = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_koo_shin_priority1_toprow_falsifier_rows=1/1
```

## Verdict

Koo-Shin 2010 should no longer be reread as a likely self-contained
priority-1 closer. Its live uses are:

```text
Theorem 6.2 source legality
Lemma 6.1 distribution/order support
Theorem 5.2 rigidity/root-descent context
Section 7 and Section 9 value/generator analogies
```

The first lookup row remains open only if a new theorem outside the currently
screened Koo-Shin 2010 clauses supplies the missing finite scalar-fixed
divisor/additive identity for one normalized legal support-156 row with
`Norm_156(Y_507)` boundary.
