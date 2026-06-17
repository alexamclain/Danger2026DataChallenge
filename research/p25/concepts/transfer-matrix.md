---
type: concept
status: active
updated: 2026-06-16
canonical: true
owner: llm
---

# Transfer Matrix

## Purpose

Carry the p24-to-p25 transfer map: which surfaces port, which only become
microscopes, and which are dead enough not to lead the frontier.

## Current Claim

The transfer picture is now stable enough to prioritize around it.

Target:

```text
p = 10000000000000000000000013
p mod 8 = 5
sqrt_floor = 3162277660168
k = 42
```

Admissible traces:

```text
t =  5808037298190   v2 = 42   odd_part = 2273736754431
t =  1409990787086   v2 = 50   odd_part = 8881784197
t = -2988055724018   v2 = 42   odd_part = 2273736754433
```

Working summary:

- The arithmetic baseline is now checked by a dedicated audit: `p mod 8 = 5`,
  `sqrt_floor = 3162277660168`, `k = 42`, the three admissible traces and odd
  parts, conductor-4 trace discriminants, and PARI order class groups all
  validate.
- Practical `x16halvenonsplit` transfers directly and remains the live search.
- H0 and mixed conductor 39 are the best first-pass source languages because
  the source objects are already certified, but their finite targets have now
  collapsed to one shared four-row product family.
- The H0 support microscope now has a compact finite target: one of four legal
  78-over-78 H0/H0-translate products, plus either a period-156 value theorem
  or a divisor/additive theorem with Hilbert-90 boundary to `Norm_156(Y_507)`.
- The conductor-39 support microscope now has a compact finite target:
  `U_chi = 1_{7<2>} - 1_{<2>}`, a legal sparse Hilbert-90 selector, and a
  support-156 Yang lift whose `(1 - Frob_p)` boundary is `Norm_156(Y_507)`.
- The Yang lift/descent boundary pass now makes the conductor-39 promotion
  ladder explicit: source word, level-507 Yang lift, H90 boundary, finite
  theorem. Stopping before the finite theorem is repair, not source closure.
- The unification pass verifies that the H0 and conductor-39 bullets above are
  the same support-156, 78-over-78 finite product target, seen through two
  source languages.
- Exact-P remains the high-payoff heavy route, now understood as a stronger
  upstream producer for the same unified H0/conductor-39 finite target.
- Literal p24 CM/Lang transfer is dead.
- Fixed-frequency/Jacobi and low-moment/W-axis still matter only as
  p25-specific support microscopes tied to H0, conductor 39, or exact-P.
- Twisted-H90 and curved-corner remain live only when a source already includes
  the exact object plus period-156 branch/root/telescoping context.
- The exact-P support microscope has now promoted one positive finite artifact:
  the 75 normalized-y atoms have disjoint theta2 support, forcing equal weights
  and killing nonuniform or missing-atom escapes.
- A second exact-P support pass promoted the finite theorem interface itself:
  the accepted anti-invariant product is rigid up to orientation/reversal and
  can be targeted as `C=(47,28), D=(22,3), K=(57,0), orientation`, or as an
  accepted period-156 theta2 divisor/additive payload.
- The exact-P-to-unified spine verifies the one-way ladder
  `75 -> 300 -> 12 -> 312 -> 156`: a compact exact-P theorem would feed the
  unified support-156 target, but the unified target alone does not recover
  exact-P.
- The reverse exact-P information-loss checkpoint makes that one-way boundary
  a routing rule: unified theorem hits go to extraction unless they also supply
  exact-P selector data, an accepted theta2 payload, or an explicit reverse
  reconstruction theorem.
- The exact-P minimal hook is now the heavy-route intake surface: compact
  `C,D,K,orientation`, exact equal-weight 75 atoms, accepted theta2 payload, or
  explicit reverse reconstruction theorem.
- The source-family router now freezes the literature policy: first ask for
  the unified divisor/additive theorem, accept exact `C4_1` selector data only
  when it comes with mixed row sign and the same finite theorem, accept only
  period-156 value support, and keep exact-P as heavy-route work unless a
  source already names the 75-atom theorem or bridge.
- The period-156 value source hook is now the value-side companion to that
  policy: Schertz/Shin/Scholl/Siegel-Robert leads must emit an arithmetic value
  theorem for one oriented support-156 edge, or an accepted period-156 theta2
  bridge. Ambient-value, field-generation, `mu_11` quotient, and direct Scholl
  `D=2` answers are repair or reject rows.
- The support-lane router now keeps Twisted-H90 and curved-corner as support
  surfaces routed through that period-156 value hook, not independent
  front-door lanes. Exact-P remains the separate heavy upstream route.
- The support-microscope router now adds generic Lane-B/Lane-C probes and the
  McCarthy square-axis endpoint to the same policy: continue only when a probe
  is tied to H0, conductor 39, exact-P, or a named theorem idea. The McCarthy
  endpoint is a sparse `e_138` theorem test object, not a front door.
- The theorem-review packet is the current handoff layer between the p25 wiki
  and an expert source check: four exact product rows, accepted
  divisor/additive, exact quartic-character, and period-156 value routes, six
  review questions, and explicit stop signs.
- The group-ring payload is the machine-checkable finite target beneath the
  review packet: the four rows are support-156 products on level 507 with
  coefficient `6`, one doubling orbit, and `Norm_156(Y_507)` boundary.
- The self-contained theorem statement is now the shortest expert-facing
  expression of that target: exact rows and hashes, three accepted
  source-stage presentations, source graph, edge-lattice rule, fourteen stop
  signs, and the downstream non-submission boundary.
- The source graph normal form is now the shortest source-language expression:
  the four legal rows are exactly the four oriented edges of a quotient-`C4`
  `K_{2,2}` graph; source answers about vertices, quotients, diagonals, row
  squares, or all-four aggregates are repair unless they select one edge.
- The edge lattice intake classifier sharpens that further: coefficient sum
  `1` gives the right `W` boundary scale, but a non-unit edge vector is still
  one edge plus nonzero boundary-zero lattice content and needs repair data.
- The edge projector denominator screen sharpens character/projector answers:
  the constant, row, column, and checkerboard projector basis reconstructs
  `4*edge`, and p25 has real `mu_4` ambiguity, so projector values need
  selected fourth-root/scalar data before intake.
- The partial projector selector screen handles two-edge answers: pair
  aggregates have `2W` boundary, pair differences have zero boundary, and pair
  plus difference reaches `2*edge`, still needing oriented square-root data.
- The row-orientation pass splits the full unit action cleanly: the doubling
  subgroup gives oriented legal rows, while its complement gives reciprocal
  legal rows requiring the opposite boundary sign before normalization.
- The rectangle-diagonal pass shows that broadening from one sparse row to a
  diagonal pair gives the broad quadratic aggregate with boundary `2W`, and
  all four rows give boundary `4W`. Those aggregates are repair/context, not
  source-stage closers, unless they recover one sparse `W`-boundary edge.
- The row-quotient pass shows all six legal-row quotients are boundary-zero
  Frobenius invariants; a diagonal aggregate plus its matching quotient
  recovers twice one legal row. This is a row-square bridge, not a source close,
  without halving/root/orientation data or a direct one-row theorem.
- The row-square root pass makes the previous line's obstruction explicit:
  square data leaves a constant sign ambiguity (`R` versus `-R`) invisible to
  divisor and Hilbert-90 boundary data, so doubled-`2W` row-square theorems are
  repair rows unless they name an oriented root.
- The coefficient-6 root-normalization pass records that exact lower-coefficient
  root theorems may be powered back to the current row, but extracting square
  or sixth roots from coefficient-6 data has sign ambiguity; scaled boundaries
  are not current-target statements unless they prove the coefficient-6 row.
- The power/scalar ambiguity inventory separates value-power claims from
  root-of-unity scalar claims: exact cube, fifth, thirteenth, and thirty-ninth
  powers are uniquely invertible in `F_p^*`; square, fourth, eleventh,
  twenty-second, forty-fourth, 156th, and 780th powers need branch or scalar
  data. `mu_11`/`mu_44` ambiguity is real, but `mu_39` is not an `F_p` scalar.
- The power output-kind router keeps the previous line from being overused:
  exact finite power values can be rooted, but powered divisor/H90 boundary
  statements still need finite value/additive normalization. Boundary `eW` is
  not the current `W` boundary by itself.
- The constant-normalization pass generalizes the same issue: divisor/H90 data
  up to an unspecified `F_p^*` scalar is repair, not a source close, until the
  source fixes the finite value by additive/value normalization, period-156
  branch data, or equivalent finite framing.
- The norm-only descent pass separates dense period-norm data from the active
  sparse row: `Norm_156(Y_507)` has support `312`, legal descents have support
  `156`, and formal one-coset descents can share the boundary while failing
  the mixed-axis tests.
- The degree-6 value descent pass separates natural conductor-39 value
  language from a source close: primitive 13th and 39th roots first occur over
  degree 6, so `F_{p^6}` value/orbit data is repair unless it descends to
  `F_p` and selects one legal support-156 row, or supplies an equivalent H90
  ratio boundary.
- The post-theorem extraction router is the current guardrail against
  over-crediting a theorem hit: it separates source-stage progress from
  DANGER3 framing, same-`j` bridge, `X_1(16)` surface, halving, and `vpp.py`.
- The source-snippet intake is the current promotion gate for new literature or
  expert input: exact row/hash, arithmetic source theorem, period-156 context
  where needed, then extraction-router classification.
- The source-family gap matrix is now the compact literature boundary: seven
  inspected source families have useful vocabulary, Koo-Shin 2010 is the only
  one currently matching the one-edge source-object shape, and none supplies a
  scalar-fixed finite theorem, period-156 value theorem, exact-P upstream
  theorem, first-pass closer, or submission-ready row.
- The minimal expert ask is now the front-door theorem question: one exact
  oriented quotient-`C4` edge, arithmetic source theorem, `Norm_156(Y_507)`
  boundary, and either scalar-fixed finite divisor/additive data or
  support-period-156 value data.
- The extraction minimal hook is now the compact downstream acceptance
  boundary after any source-stage theorem or exact-P hook: DANGER3 finite
  framing, same-`j` `X_1(8112)` data, practical `X_1(16)` payload, halving or
  direct `x0`, and official `vpp.py` verification are still required.

## Decisive Evidence

- [Lane A CM/Lang transfer note](../evidence/lane_A_cm_lang_transfer.md)
  kills the literal p24 transfer.
- [V2 arithmetic baseline audit](../evidence/p25_v2_arithmetic_baseline_audit_20260616.md)
  verifies the target, traces, odd parts, discriminant factorizations,
  conductor `4` order data, and PARI class groups used by all transfer lanes.
- [Lane B fixed-frequency/Jacobi note](../evidence/lane_B_fixed_frequency_jacobi.md)
  leaves behind real quotient skeletons but not a producer.
- [Lane C low-moment/W-axis note](../evidence/lane_C_low_moment_w_axis.md)
  shows sub-sqrt payload counts but only theorem-shaped next steps.
- [Lane D strict practical improvement note](../evidence/lane_D_strict_practical_improvement.md)
  keeps the production mode anchored.
- [External source-theorem obligation matrix](../evidence/p25_ksy_y_external_source_theorem_obligation_matrix_20260614.md)
  prioritizes H0 and conductor 39 over exact-P as first asks.
- [V2 H0 theorem-interface contract](../evidence/p25_v2_h0_theorem_interface_contract_20260616.md)
  records the compact H0 product target, period-156/H90 requirements, and
  downstream same-`j` `X_1(8112)` payload.
- [V2 conductor-39 Yang/H90 interface contract](../evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md)
  records the compact support-156 conductor-39 target and its falsifiers.
- [V2 Yang lift / descent boundary contract](../evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md)
  records the source-word, Yang-lift, H90-boundary, finite-theorem promotion
  ladder.
- [V2 H0 / conductor-39 unified target](../evidence/p25_v2_h0_conductor39_unified_target_20260616.md)
  verifies that H0 and conductor 39 share one finite target family.
- [V2 exact-P theorem-interface contract](../evidence/p25_v2_exactp_theorem_interface_contract_20260616.md)
  records the compact accepted exact-P target and its falsifiers.
- [V2 exact-P to unified target spine](../evidence/p25_v2_exactp_to_unified_target_spine_20260616.md)
  records exact-P as a one-way upstream producer route into the unified target.
- [V2 reverse exact-P information loss](../evidence/p25_v2_reverse_exactp_information_loss_20260616.md)
  records why the unified target cannot be promoted back to exact-P without
  extra selector structure.
- [V2 exact-P minimal hook](../evidence/p25_v2_exactp_minimal_hook_20260616.md)
  records the compact exact-P source ask and exact-P near-miss routing.
- [V2 unified submission/extraction contract](../evidence/p25_v2_unified_submission_extraction_contract_20260616.md)
  records the downstream DANGER3 ladder and verifies that no current theorem
  payload is submission-ready.
- [V2 unified source-theorem gap](../evidence/p25_v2_unified_source_theorem_gap_20260616.md)
  records that the first-pass H90/gauge/Yang/product layers are saturated and
  the remaining gap is arithmetic, not combinatorial.
- [V2 conductor-39 doubling-orbit minimality](../evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md)
  records that the source seed `E_7/E_1` requires the full 12-step doubling
  norm; no proper suborbit is a legal standalone shortcut.
- [V2 unified value/divisor interface](../evidence/p25_v2_unified_value_divisor_interface_20260616.md)
  records the accepted source-stage theorem rows and the common near-miss
  falsifiers.
- [V2 value/divisor source-family router](../evidence/p25_v2_value_divisor_source_family_router_20260616.md)
  records which source families are still live and kills broad rereads.
- [V2 period-156 value source hook](../evidence/p25_v2_period156_value_source_hook_20260616.md)
  records the compact value-side source intake rule and confirms zero current
  period-156 value theorems.
- [V2 support lane router](../evidence/p25_v2_support_lane_router_20260616.md)
  records that Twisted-H90 and curved-corner are support surfaces routed
  through the period-156 hook, while exact-P remains the separate heavy route.
- [V2 support microscope router](../evidence/p25_v2_support_microscope_router_20260617.md)
  records that generic Lane-B/Lane-C probes and the McCarthy endpoint remain
  attached support microscopes, not independent first-pass front doors.
- [V2 unified theorem review packet](../evidence/p25_v2_unified_theorem_review_packet_20260616.md)
  records the compact expert-review statement for the remaining first-pass
  arithmetic theorem gap.
- [V2 unified group-ring payload](../evidence/p25_v2_unified_group_ring_payload_20260616.md)
  records the algebraic payload and stable hashes for the four finite rows.
- [V2 self-contained theorem statement](../evidence/p25_v2_self_contained_theorem_statement_20260616.md)
  records the shortest expert handoff for the exact theorem target, now
  including graph and lattice intake rules.
- [V2 source graph normal form](../evidence/p25_v2_source_graph_normal_form_20260616.md)
  records the quotient-`C4` `K_{2,2}` source graph for the four legal rows.
- [V2 edge lattice intake classifier](../evidence/p25_v2_edge_lattice_intake_classifier_20260616.md)
  records the coefficient-sum boundary rule for edge combinations.
- [V2 edge projector denominator](../evidence/p25_v2_edge_projector_denominator_20260616.md)
  records the character/projector denominator-4 screen for one-edge recovery.
- [V2 partial projector selector](../evidence/p25_v2_partial_projector_selector_20260616.md)
  records the two-edge, pair-difference, and doubled-edge selector screen.
- [V2 row orientation / reciprocal normalizer](../evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md)
  records the oriented/reciprocal split of the full unit action.
- [V2 rectangle diagonal aggregate](../evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md)
  records the `m1*m4 = m2*m8` broad quadratic aggregate, its `2W` boundary,
  and the all-four `4W` over-demand.
- [V2 row quotient invariant bridge](../evidence/p25_v2_row_quotient_invariant_bridge_20260616.md)
  records the boundary-zero legal-row quotients and the aggregate-plus-quotient
  row-square bridge.
- [V2 row square root ambiguity](../evidence/p25_v2_row_square_root_ambiguity_20260616.md)
  records the sign/root obstruction for row-square theorem shapes.
- [V2 coefficient-6 root normalization](../evidence/p25_v2_coefficient6_root_normalization_20260616.md)
  records the usable lower-coefficient root normalizations and the remaining
  root/sign and scaled-boundary obstructions.
- [V2 power/scalar ambiguity inventory](../evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md)
  records p25's `F_p^*` power-map kernels and which root-of-unity scalar
  ambiguities exist over `F_p`.
- [V2 power output-kind router](../evidence/p25_v2_power_output_kind_router_20260616.md)
  records the intake distinction between exact finite power values and powered
  divisor/H90 boundary statements.
- [V2 constant normalization ambiguity](../evidence/p25_v2_constant_normalization_ambiguity_20260616.md)
  records the scalar-normalization obstruction for divisor/H90 or value data
  only specified up to `F_p^*`.
- [V2 norm-only descent ambiguity](../evidence/p25_v2_norm_only_descent_ambiguity_20260616.md)
  records the dense-norm versus legal-descent obstruction for period-norm
  theorem shapes.
- [V2 degree-6 value descent ambiguity](../evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md)
  records the degree-6 value/orbit versus explicit `F_p` descent obstruction.
- [V2 post-theorem extraction router](../evidence/p25_v2_post_theorem_extraction_router_20260616.md)
  records the route from theorem hit to practical certificate.
- [V2 source-snippet intake](../evidence/p25_v2_source_snippet_intake_20260616.md)
  records the accept/repair/reject decisions for future source snippets.
- [V2 source-family gap matrix](../evidence/p25_v2_source_family_gap_matrix_20260616.md)
  records which inspected source families are nearest to the current theorem
  target and what each one still lacks.
- [V2 minimal expert ask](../evidence/p25_v2_minimal_expert_ask_20260616.md)
  records the shortest yes/no theorem question and immediate repair/reject
  routing for expert answers.
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
  records the shortest post-theorem checklist and keeps current
  extraction-ready and submission-ready rows at zero.

## Open Blockers

- No transfer row has yet yielded a source-stage closing theorem.
- The theorem microscopes still need exact arithmetic producers or nonvanishing
  theorems, not just favorable counts.
- The unified H0/conductor-39 target still needs one finite value/divisor
  theorem for a legal support-156 product with H90 boundary, plus downstream
  DANGER3 framing and extraction.
- Selector/gauge/product-normal-form search is saturated for the first-pass
  target; repeating it is not progress without a new arithmetic theorem.
- Proper conductor-39 doubling suborbit shortcuts are falsified by Yang/Yu
  legality unless a source theorem explicitly repairs the failed boundary.
- Source-stage progress now means one of the value/divisor interface accepted
  rows; source legality, boundary-only, selector/gauge, ambient-value, and
  finite-payload-only claims are not progress by themselves.
- Conductor-39 source-word or Yang-lift snippets should be checked against the
  Yang lift/descent boundary contract before being treated as first-pass
  progress.
- Broad source-family rereading is no longer a transfer lane; a source lead
  must already match the router's accepted theorem rows or provide a falsifier.
- Value-side source leads should pass through the period-156 value source hook
  before any lane priority changes.
- Expert feedback should be routed through the review packet before changing
  lane priorities.
- Finite product snippets should be checked against the group-ring payload
  before being treated as the current H0/conductor-39 target.
- Reciprocal or outside-doubling product snippets should be checked against the
  row-orientation normalizer before being accepted, repaired, or rejected.
- Broad quadratic aggregate, diagonal-pair, or all-four-row snippets should be
  checked against the rectangle-diagonal aggregate screen before being treated
  as first-pass progress.
- Quotient or aggregate-plus-quotient snippets should be checked against the
  row quotient invariant bridge before being treated as first-pass progress.
- Row-square or doubled-`2W` snippets should be checked against the row square
  root ambiguity screen before being treated as first-pass progress.
- Lower-coefficient root snippets should be checked against the coefficient-6
  root-normalization screen before being treated as first-pass progress.
- Exact power-value or root-of-unity scalar snippets should be checked against
  the power/scalar ambiguity inventory before being treated as first-pass
  progress.
- Powered divisor/additive or H90-boundary snippets should be checked against
  the power output-kind router before being treated as first-pass progress.
- Divisor/additive snippets should be checked against the additive
  normalization contract before being treated as first-pass progress; the
  additive side must fix the finite value, not merely restate a divisor class
  or dense relation.
- Divisor/H90 or value snippets only specified up to an unspecified `F_p^*`
  scalar should be checked against the constant-normalization ambiguity screen
  before being treated as first-pass progress.
- Period-norm snippets should be checked against the norm-only descent
  ambiguity screen before being treated as first-pass progress.
- Degree-6 value/orbit snippets should be checked against the degree-6 descent
  ambiguity screen before being treated as first-pass progress.
- Theorem hits should be classified through the extraction router before they
  change practical-search or submission status.
- The extraction minimal hook is now the acceptance boundary after a theorem
  hit or exact-P hook; no lane currently supplies all required downstream
  payload clauses.
- New source evidence should pass through the snippet intake before changing
  lane state.
- Source-family work should start from the gap matrix: Koo-Shin 2010 is the
  nearest helper, but no inspected source currently closes the finite theorem
  gap.
- Expert-facing work should start from the minimal expert ask before opening
  lane archives; an answer must either match an accepted route or give a sharp
  falsifier for that exact theorem shape.
- Character/projector source answers should pass through the edge projector
  denominator screen before being treated as one-edge source theorems.
- Two-edge pair or pair-difference answers should pass through the partial
  projector selector before being treated as one-edge source theorems.
- Exact extraction from any source object to DANGER3 payload remains missing.
- The downstream ladder is defined: after a theorem hit we still need
  DANGER3 framing, same-`j` `X_1(8112)`, practical `X_1(16)` `A,xP16`,
  halving/direct `x0`, and official `vpp.py`.
- Dead p24 routes should not be replayed unless p25 arithmetic changes the
  recorded failure mode in a named artifact.
- Exact-P still needs an arithmetic source theorem; the finite rigidity and
  theorem-interface contract only sharpen what the theorem must produce. It is
  upstream of the unified target, not an independent downstream target.
- A unified theorem hit should not be counted as exact-P recovery unless it
  adds the missing `C,D,K,orientation`, 75-atom, theta2, or reverse-theorem
  payload.
- Exact-P source answers should pass through the minimal hook before changing
  heavy-route status.

## Next Reads

- [Practical search](../lanes/practical-search.md)
- [H0](../lanes/h0.md)
- [Conductor 39](../lanes/conductor39.md)
- [Exact P](../lanes/exact-p.md)
- [P24 prior art](../sources/p24-prior-art.md)

## Linked Artifacts

- [Lane A evidence](../evidence/lane_A_cm_lang_transfer.md)
- [Lane B evidence](../evidence/lane_B_fixed_frequency_jacobi.md)
- [Lane C evidence](../evidence/lane_C_low_moment_w_axis.md)
- [Lane D evidence](../evidence/lane_D_strict_practical_improvement.md)
- [V2 H0 theorem-interface contract](../evidence/p25_v2_h0_theorem_interface_contract_20260616.md)
- [V2 conductor-39 Yang/H90 interface contract](../evidence/p25_v2_conductor39_yang_h90_interface_contract_20260616.md)
- [V2 Yang lift / descent boundary contract](../evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md)
- [V2 H0 / conductor-39 unified target](../evidence/p25_v2_h0_conductor39_unified_target_20260616.md)
- [V2 exact-P theorem-interface contract](../evidence/p25_v2_exactp_theorem_interface_contract_20260616.md)
- [V2 exact-P to unified target spine](../evidence/p25_v2_exactp_to_unified_target_spine_20260616.md)
- [V2 reverse exact-P information loss](../evidence/p25_v2_reverse_exactp_information_loss_20260616.md)
- [V2 exact-P minimal hook](../evidence/p25_v2_exactp_minimal_hook_20260616.md)
- [V2 unified submission/extraction contract](../evidence/p25_v2_unified_submission_extraction_contract_20260616.md)
- [V2 unified source-theorem gap](../evidence/p25_v2_unified_source_theorem_gap_20260616.md)
- [V2 conductor-39 doubling-orbit minimality](../evidence/p25_v2_conductor39_doubling_orbit_minimality_20260616.md)
- [V2 unified value/divisor interface](../evidence/p25_v2_unified_value_divisor_interface_20260616.md)
- [V2 value/divisor source-family router](../evidence/p25_v2_value_divisor_source_family_router_20260616.md)
- [V2 period-156 value source hook](../evidence/p25_v2_period156_value_source_hook_20260616.md)
- [V2 unified theorem review packet](../evidence/p25_v2_unified_theorem_review_packet_20260616.md)
- [V2 unified group-ring payload](../evidence/p25_v2_unified_group_ring_payload_20260616.md)
- [V2 self-contained theorem statement](../evidence/p25_v2_self_contained_theorem_statement_20260616.md)
- [V2 source graph normal form](../evidence/p25_v2_source_graph_normal_form_20260616.md)
- [V2 edge lattice intake classifier](../evidence/p25_v2_edge_lattice_intake_classifier_20260616.md)
- [V2 row orientation / reciprocal normalizer](../evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md)
- [V2 rectangle diagonal aggregate](../evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md)
- [V2 row quotient invariant bridge](../evidence/p25_v2_row_quotient_invariant_bridge_20260616.md)
- [V2 row square root ambiguity](../evidence/p25_v2_row_square_root_ambiguity_20260616.md)
- [V2 coefficient-6 root normalization](../evidence/p25_v2_coefficient6_root_normalization_20260616.md)
- [V2 power/scalar ambiguity inventory](../evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md)
- [V2 power output-kind router](../evidence/p25_v2_power_output_kind_router_20260616.md)
- [V2 additive normalization contract](../evidence/p25_v2_additive_normalization_contract_20260616.md)
- [V2 constant normalization ambiguity](../evidence/p25_v2_constant_normalization_ambiguity_20260616.md)
- [V2 norm-only descent ambiguity](../evidence/p25_v2_norm_only_descent_ambiguity_20260616.md)
- [V2 degree-6 value descent ambiguity](../evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md)
- [V2 post-theorem extraction router](../evidence/p25_v2_post_theorem_extraction_router_20260616.md)
- [V2 source-snippet intake](../evidence/p25_v2_source_snippet_intake_20260616.md)
- [V2 source-family gap matrix](../evidence/p25_v2_source_family_gap_matrix_20260616.md)
- [V2 minimal expert ask](../evidence/p25_v2_minimal_expert_ask_20260616.md)
- [V2 extraction minimal hook](../evidence/p25_v2_extraction_minimal_hook_20260616.md)
- [V2 edge projector denominator](../evidence/p25_v2_edge_projector_denominator_20260616.md)
- [V2 partial projector selector](../evidence/p25_v2_partial_projector_selector_20260616.md)
- [Legacy transfer-matrix note](../archive/notes/p25_transfer_matrix_legacy_20260616.md)
