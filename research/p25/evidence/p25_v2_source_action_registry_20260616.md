# P25 v2 Source-Action Registry

Updated: 2026-06-16

## Purpose

Consolidate the post-v2 source-search state into one action registry. This is
not another source scan. It records which source actions remain live after the
Koo-Shin access closure, external Kubert-Lang and Schertz/Shin/Scholl
boundaries, Sprang theta2 intake, Q-route source scan, support-lane router, and
current source-snippet/expert-response intake rules.

## Pages Read

- `frontier.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_current_expert_response_rubric_20260616.md`
- `evidence/p25_v2_koo_shin_access_blocker_closure_20260616.md`
- `evidence/p25_v2_kubert_lang_external_source_boundary_20260616.md`
- `evidence/p25_v2_schertz_scholl_external_source_boundary_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`
- `evidence/p25_v2_q_route_source_hook_scan_20260616.md`
- `evidence/p25_v2_support_lane_router_20260616.md`
- `evidence/p25_v2_primitive_character_power_recheck_20260617.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_source_action_registry_gate.py
```

The gate returned `p25_v2_source_action_registry_rows=1/1`.

## Registry Rows

```text
first_pass_h0_conductor39
  status  = live_primary_theorem_ask
  action  = scalar-fixed finite divisor/additive theorem, or exact uniquely
            invertible power-value theorem, for one legal support-156 row with
            Norm_156(Y_507) boundary
  discard = source legality, boundary-only, selector-only, finite payload
            without source, ambiguous power value, or broad source-family reread

period156_h0_y507_value
  status  = live_support_theorem_ask
  action  = period-156 H0/Y507 value theorem with branch/root/telescoping or
            additive normalization
  discard = Schertz/Shin/Scholl generator language, ambient period-780 value,
            mu_11 quotient, or direct Scholl D=2 import

exactp_heavy_route
  status  = live_heavy_theorem_ask
  action  = exact 75-atom, compact C,D,K,orientation, primitive-word,
            mixed-selector, or theta2 payload theorem
  discard = KSY vocabulary, raw KL exponent balance, generic modular-unit
            generation, or branchless orientation

koo_shin_2010
  status  = stale_access_action_closed
  action  = accept only a new theorem-shaped Koo-Shin snippet through
            source-snippet intake
  discard = treating PDF/OCR retrieval as live or treating Theorem 5.2,
            Lemma 6.1, or Theorem 6.2 as finite p25 theorem without new clauses

sprang_d2_theta
  status  = support_only
  action  = exact p25 theta2/theta2-inverse divisor-additive specialization
            with period-156 bridge
  discard = broad D=2, p-adic theta, de Rham polylog, kernel distribution, or
            cohomology vocabulary

kubert_lang
  status  = support_only
  action  = exact primitive word, mixed C3 x C169 selector, or accepted theta2
            payload theorem
  discard = KL generator theory, generic unit generation, theorem-K
            congruence context, or C169 projection data

conductor39_q_route
  status  = support_only
  action  = finite Q value theorem with period-156 context, Q3 H90 theorem, or
            oriented diagonal split, or exact primitive-unit value theorem tied
            to one legal row
  discard = Q source-only, Q6 boundary-only, primitive-power-only, pure degree-6
            norm, U_chi/V_bal exponent relation only, or local generic Q
            language

twisted_h90_curved_corner
  status  = support_only
  action  = exact support-lane snippets routed through period-156 value hook
            and source-snippet intake
  discard = broad H90, norm, curved product, or unit-triangle vocabulary without
            exact source object and period-156 data
```

## Counts

```text
live_theorem_asks = 3
stale_actions_closed = 1
support_only_rows = 4
broad_reread_allowed_rows = 0
current_source_stage_closers = 0
current_submission_ready = 0
```

## Verdict

```text
positive_artifact = source-action registry after v2 source closures
continue = yes, but only with theorem-shaped snippets or expert answers
discard_condition = any broad reread request not already carrying one of the
                    accepted theorem hooks above
```

The source queue is now theorem-shaped. The remaining work is not to reread a
family broadly; it is to find, prove, or get an expert assessment of one of the
three live theorem asks.
