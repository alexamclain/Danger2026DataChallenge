# P25 v2 External Distribution-Relation Scout

Updated: 2026-06-17

Marker: `p25_v2_external_distribution_relation_scout_rows=1/1`

## Purpose

Classify one narrow external literature cluster against the live p25 theorem
hooks: Siegel-unit distribution relations, Beilinson-Kato modular-symbol
distributions, Kato-Siegel theta functions, and Kubert-Lang modular-unit
generator/distribution theory.

This is not another broad source search. The question was whether this cluster
already supplies one of the accepted p25 hooks:

```text
one scalar-fixed support-156 row theorem
one row-labeled unique-power theorem
one support-period-156 H0/Y_507 value theorem
one exact-P/theta2 upstream packet
```

It does not. The cluster is support/repair until a source adds a p25 row label,
`Norm_156(Y_507)` boundary, scalar-fixed finite `F_p` payload, and downstream
normalization/extraction bridge.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_local_source_hook_coverage_audit_20260617.md`
- `evidence/p25_v2_external_source_delta_20260617.md`
- `evidence/p25_v2_kato_siegel_divisor_scout_20260617.md`

## External Sources Checked

- [On distribution relations of polylogarithmic Eisenstein classes](https://arxiv.org/pdf/2309.10938)
- [Modular Symbols with Values in Beilinson-Kato Distributions](https://arxiv.org/html/2311.14620v2)
- [Notes on Kato-Siegel functions](https://swc-math.github.io/notes/files/01MazurPW.pdf)
- [Kubert-Lang, Modular Units](https://link.springer.com/book/10.1007/978-1-4757-1741-9)

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_external_distribution_relation_scout_gate.py
```

The gate returned `p25_v2_external_distribution_relation_scout_rows=1/1`.

## Rows

```text
polylog_eisenstein_distribution_2025
  useful = integral distribution relations for Eisenstein classes
  missing = one legal support-156 row, Norm_156(Y_507) boundary,
            scalar-fixed finite F_p payload
  decision = support_distribution_relations_not_p25_row_theorem

beilinson_kato_modular_symbol_distributions
  useful = Siegel distribution and Manin-relation framework
  missing = row label in {1,2,4,8}, finite additive/value specialization,
            DANGER3 extraction bridge
  decision = support_k_theory_distribution_not_finite_row_payload

kato_siegel_theta_function_notes
  useful = canonical theta_D divisor and isogeny compatibility
  missing = p25 row selector, D=2-compatible period-156 branch,
            explicit finite value or additive normalizer
  decision = repair_divisor_distribution_not_scalar_fixed_value

kubert_lang_modular_units
  useful = modular-unit generator and distribution theory
  missing = exact p25 selector, arithmetic source theorem,
            scalar or branch normalization
  decision = support_generators_not_selected_finite_identity
```

## Counts

```text
source_rows = 4
source_urls_ok = 1
decisions_ok = 1
missing_clauses_ok = 1
support_rows = 3
repair_rows = 1
current_source_stage_closers = 0
p25_v2_external_distribution_relation_scout_rows=1/1
```

## Verdict

Continue, but do not promote distribution-relation language by itself. This
source cluster gives real framework vocabulary for divisors, isogeny
compatibility, distribution relations, modular symbols, and Eisenstein
classes. It still lacks the p25-specific finite object.

The next acceptable use of this cluster must supply one of:

```text
scalar-fixed finite theorem for one legal support-156 row
row-labeled uniquely invertible finite power value
support-period-156 H0/Y_507 value theorem with branch/root/telescoping
exact-P/theta2 packet with the accepted bridge
```

Anything weaker stays support or repair.
