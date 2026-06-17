# P25 v2 Basis-Sensitive Anchor Sieve

Updated: 2026-06-17

Marker: `p25_v2_basis_sensitive_anchor_sieve_rows=1/1`

## Purpose

Put the latest row-anchor filters in the right order. A proposed p25 theorem
must first be placed in the correct object basis before coefficient sums,
power-map gcds, or period-branch tests mean anything.

This page is an intake sieve, not a source theorem. It prevents three current
mistakes:

```text
1. treating coefficient-sum-one nonunit row vectors as legal edges;
2. applying row-lattice gcd tests to exact-P 75-atom counts;
3. treating ambient-period values as selected period-156 row values.
```

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `lanes/exact-p.md`
- `evidence/p25_v2_edge_lattice_global_minimality_20260616.md`
- `evidence/p25_v2_row_value_reconstruction_basis_20260617.md`
- `evidence/p25_v2_common_scalar_anchor_filter_20260617.md`
- `evidence/p25_v2_exactp_75_anchor_bridge_filter_20260617.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`
- `evidence/p25_v2_period156_value_branch_contract_20260616.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_basis_sensitive_anchor_sieve_gate.py
```

The gate returned `p25_v2_basis_sensitive_anchor_sieve_rows=1/1`.

## Sieve Rows

```text
legal_unit_edge_row
  basis       = H0/conductor-39 four-row edge lattice
  selector    = coefficient vector is one of e1,e2,e4,e8
  scalar test = coefficient sum 1 and gcd(1,p-1)=1
  decision    = first_pass_source_stage_candidate_if_theorem_present

sum_one_nonunit_row_vector
  basis       = H0/conductor-39 four-row edge lattice
  selector    = coefficient sum 1 but L1 norm >= 3
  scalar test = common scalar is visible, but selector debt remains
  decision    = repair_edge_plus_zero_lattice_content

zero_lattice_or_quotient
  basis       = H0/conductor-39 four-row edge lattice
  selector    = coefficient sum 0
  scalar test = common F_p^* scalar is invisible
  decision    = transfer_only_not_first_anchor

row_labeled_unique_power
  basis       = H0/conductor-39 legal row value R_m
  selector    = one oriented legal row is named
  scalar test = gcd(e,p-1)=1 for e in {3,5,13,39,75,169,507}
  decision    = normalize_by_inverse_exponent_then_first_pass_intake

period156_row_value
  basis       = support-period-156 value with legal-row bridge
  selector    = canonical H0/Y507 or one legal row bridge is supplied
  scalar test = gcd(4^156-1,p-1)=1
  decision    = period_branch_normalized_first_pass_intake

ambient_period780_value
  basis       = ambient value without period-156 row branch
  selector    = no selected support-period-156 row branch
  scalar test = gcd(4^780-1,p-1)=11
  decision    = repair_eleven_branch_ambiguity

exactp_equal_weight_atoms
  basis       = exact-P normalized-y/theta2 75-atom basis
  selector    = C,D,K plus accepted orientation, or exact equal-weight atoms
  scalar test = not a row-lattice coefficient-sum test
  decision    = heavy_upstream_candidate_not_first_pass_row_shortcut

unified_support156_reverse_exactp
  basis       = unified H0/conductor-39 support-156 target
  selector    = one support-156 row theorem may route to extraction
  scalar test = does not reconstruct exact-P orientation or atoms
  decision    = route_unified_hit_to_extraction_not_exactp_recovery
```

## Counts

```text
evidence_markers_ok = 7/7
sieve_rows = 8
first_pass_candidate_rows = 3
repair_rows = 2
transfer_only_rows = 1
heavy_upstream_rows = 1
reverse_route_rows = 1
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_basis_sensitive_anchor_sieve_rows=1/1
```

## Verdict

The current intake order is now:

```text
1. Identify the object basis.
2. If it is a row-lattice claim, require a unit edge or paid zero-lattice debt.
3. If it is a row-power claim, require a named legal row and gcd(e,p-1)=1.
4. If it is a value claim, require support-period-156 branch data or additive
   normalization.
5. If it is exact-P, require C,D,K/orientation, equal-weight atoms, theta2
   payload, or an explicit reverse theorem.
6. Only after source-stage normalization should it route to DANGER3 framing
   and extraction.
```

This is the compact answer to "how close are we?" on the theorem side: the
finite target and filters are now sharp, but every accepted row still begins
with a missing arithmetic source theorem or an exact proof/construction.
