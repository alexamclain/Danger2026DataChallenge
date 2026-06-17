# P25 v2 Source Snippet Intake

Updated: 2026-06-17

## Purpose

Provide a fast intake checklist for future paper snippets, expert replies, or
subagent reports.  The group-ring target is pinned; this page classifies
incoming snippets as source-stage closers, repair rows, rejects, or complete
submission payloads. Value-side snippets route through the promoted H0/Y507
period-156 compatibility screen. H90 selector snippets now also route through
the support lower bound: support below 12 is impossible for the current `W`,
and support 12 is useful only for the four legal mixed minimizers.
Exact-P snippets now also route through the minimal exact-P hook, so
normalized-y vocabulary, raw Kubert-Lang balance, wrong packets, nonuniform
atoms, ambient-period values, and unified-as-exact-P recovery claims have named
repair or reject rows. They also route through the exact-P orientation branch
router: branchless orientation words and theta2 values without period-156
branch context are repair rows, while wrong center, wrong `D`, or nonprimitive
`K` remains a reject. Character-language snippets now also route through the
quartic selector payload: exact `C4_1` selector plus finite theorem is a
source-stage shape, while selector-only, coarse phase/magnitude, phase without
row sign, and same-parity phase claims are repair or reject rows.
Those exact phase claims also pass the reciprocal-orientation screen: a
reciprocal row negates both the Hilbert-90 boundary and the `C4_1` phase, so
reciprocal phase with positive boundary is rejected and phase collisions with
the opposite oriented edge are repair rows until the row orientation/boundary
sign is fixed.
Exact power-value snippets now route all four p25 bijective power maps:
`R^3`, `R^5`, `R^13`, and `R^39` normalize by unique root recovery in
`F_p^*`; non-bijective power values still need branch/orientation/scalar data.
Conductor-39 norm-one quotient snippets now also route through the compact
`Q = prod_{h in <2>} E_{7h}/E_h` screen: `Q` value theorems with period-156
context or `Q^3` H90 finite theorems are support routes, while source-only,
boundary-only, primitive-power-only, and pure degree-6 norm claims remain
repair or reject rows.
The Q diagonal-normalization screen now adds the split/root follow-up:
`Q_antisym=m1+m4=m2+m8`, so Q-only diagonal value data is support, Q plus a
row quotient is still a square-root repair, Q plus an explicit oriented
diagonal split normalizes to one-edge intake, and wrong zero-boundary splits
are rejected.
The Q square payload router now separates exact finite value data from generic
square-root ambiguity: an exact scalar-fixed `F_p` value for the Q square
gives a bounded two-root row-value payload, while value-up-to-scalar or
sign-from-divisor/H90/phase claims are repair or reject rows. The Q square
extraction-boundary screen adds that those two row roots are not `vpp.py`
candidates until an extraction map supplies same-j/X_1(16)/halving data or
direct `(A,x0)` candidates.

## 2026-06-17 Sync Note

This page remains useful as the detailed snippet router, but the live theorem
classifier is now the source theorem acceptance automaton. Two later updates
supersede the older prose below:

```text
unique row powers = e in {3,5,13,39,75,169,507}
distribution/norm aggregate closure = repair_even_boundary_distribution_closure
matched aggregate route = normalize_matched_quotient_then_accept
```

Thus an exact row-labeled finite theorem for `R_m^75`, `R_m^169`, or
`R_m^507` routes through the same unique-power intake as `R_m^3`, `R_m^5`,
`R_m^13`, and `R_m^39`. Generic distribution, norm, vertex-sum, diagonal, or
all-four aggregate relation data remains repair unless a source also supplies
direct edge data, root/selector/scalar normalization, or an equivalent
one-row theorem.

The one aggregate exception is now explicit: an arithmetic theorem for `R^v`
plus an arithmetic theorem for the exact matched zero-lattice value
`R^(v - (sum v)e_m)` routes to one-row intake when `gcd(sum v,p-1)=1`.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/sprang.md`
- `sources/kubert-lang.md`
- `sources/schertz-scholl.md`
- `evidence/p25_v2_unified_group_ring_payload_20260616.md`
- `evidence/p25_v2_unified_theorem_review_packet_20260616.md`
- `evidence/p25_v2_value_divisor_source_family_router_20260616.md`
- `evidence/p25_v2_h0_y507_period156_compatibility_20260616.md`
- `evidence/p25_v2_post_theorem_extraction_router_20260616.md`
- `evidence/p25_v2_row_orbit_normalization_20260616.md`
- `evidence/p25_v2_row_orientation_reciprocal_normalizer_20260616.md`
- `evidence/p25_v2_koo_shin_distribution_noncloser_20260616.md`
- `evidence/p25_v2_theorem52_constant_span_obstruction_20260616.md`
- `evidence/p25_v2_rectangle_diagonal_aggregate_20260616.md`
- `evidence/p25_v2_row_quotient_invariant_bridge_20260616.md`
- `evidence/p25_v2_row_square_root_ambiguity_20260616.md`
- `evidence/p25_v2_constant_normalization_ambiguity_20260616.md`
- `evidence/p25_v2_norm_only_descent_ambiguity_20260616.md`
- `evidence/p25_v2_degree6_value_descent_ambiguity_20260616.md`
- `evidence/p25_v2_yang_lift_descent_boundary_contract_20260616.md`
- `evidence/p25_v2_conductor39_norm_one_quotient_route_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_coefficient6_root_normalization_20260616.md`
- `evidence/p25_v2_power_scalar_ambiguity_inventory_20260616.md`
- `evidence/p25_v2_power_output_kind_router_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_source_graph_normal_form_20260616.md`
- `evidence/p25_v2_edge_lattice_intake_classifier_20260616.md`
- `evidence/p25_v2_quartic_selector_payload_20260616.md`
- `evidence/p25_v2_quartic_reciprocal_orientation_20260616.md`
- `evidence/p25_v2_h90_support_lower_bound_20260616.md`
- `evidence/p25_v2_exactp_minimal_hook_20260616.md`
- `evidence/p25_v2_exactp_orientation_branch_router_20260616.md`

## Command

```bash
python3 research/p25/archive/gates/p25_v2_source_snippet_intake_gate.py
```

The gate returned `p25_v2_source_snippet_intake_rows=1/1`.

## Legal Payload Hashes

```text
m=1  eb5a86ae58b16b7e10706ac166d1f548aaccdfc677181a253119b6876e470d1e
m=2  97517200105db6e1f44e04e76977407615a88c8b4ca782fefec6cb2821e0a0e9
m=4  28b3e03228d428ac6474ff92eaefb1a9a7dfbfda8af2318812d5bca68e8958d6
m=8  ace1a01fa59701567225b8f781ffda2fe308aac41662f80439ace7a6cda7bf87
```

## Intake Decisions

```text
exact_divisor_additive_m1
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

period156_h0_y507_value_m2
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

exactp_upstream
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

source_legality_only
  decision = repair_source_legality_only
  missing  = finite value/divisor theorem

reciprocal_m8_minus_boundary
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

reciprocal_orientation_unspecified
  decision = repair_reciprocal_orientation_or_boundary_sign_missing
  missing  = explicit reciprocal orientation and -Norm_156 boundary, or rewrite
             as the oriented legal row

reciprocal_plus_boundary
  decision = reject_orientation_boundary_mismatch
  missing  = reciprocal product should carry the opposite Hilbert-90 boundary
             sign

theorem52_constant_product_repair
  decision = reject_theorem52_constant_span_repair
  missing  = nonzero constant-exponent vector in the legal quotient-C4 span

broad_quadratic_aggregate_boundary_2w
  decision = repair_broad_quadratic_aggregate_boundary_2w
  missing  = selector/factorization to one sparse edge with W boundary

all_four_rows_product_boundary_4w
  decision = repair_overdemand_square_of_broad_quadratic
  missing  = one legal support-156 row with W boundary is enough and still
             missing

row_quotient_boundary_zero
  decision = repair_boundary_zero_quotient_only
  missing  = one-row value/divisor theorem; quotient has zero H90 boundary

aggregate_plus_quotient_row_square
  decision = repair_row_square_bridge_halving_missing
  missing  = halving/root/orientation data selecting the legal row, or direct
             one-row theorem

row_square_value_theorem
  decision = repair_row_square_root_sign_missing
  missing  = explicit root/sign/orientation data selecting R rather than -R,
             or direct one-row theorem

row_square_with_h90_boundary_2w
  decision = repair_boundary_scale_and_root_sign_missing
  missing  = one-row W-boundary theorem plus explicit root/sign/orientation

divisor_only_with_h90_boundary
  decision = repair_constant_normalization_missing
  missing  = additive/value normalization or finite framing fixing the F_p^*
             scalar

value_up_to_fp_scalar
  decision = repair_constant_normalization_missing
  missing  = specified scalar, branch/root/telescoping context, or normalized
             value

period_norm_identity_only
  decision = repair_norm_only_h90_descent_missing
  missing  = legal support-156 Hilbert-90 descent selecting one row

dense_unit_character_norm_value
  decision = repair_norm_only_row_selection_missing
  missing  = selected legal 78-over-78 product row and finite theorem for that
             row

norm_with_formal_one_coset_descent
  decision = reject_boundary_control_not_source_object
  missing  = proper-axis pushforward failure; not the mixed conductor-39
             source object

norm_one_Q_value_theorem_with_period156_context
  decision = route_through_period156_value_source_hook
  missing  = period-156 value source hook, then downstream DANGER3 framing and
             extraction

explicit_Q3_hilbert90_preimage_with_finite_theorem
  decision = normalize_h90_preimage_then_apply_source_snippet_intake
  missing  = same theorem data after legal Hilbert-90 descent normalization

q_diagonal_value_only
  decision = support_diagonal_aggregate_selector_missing
  missing  = boundary-zero split/orientation data or direct one-edge theorem

q_plus_row_quotient_without_root
  decision = repair_oriented_square_root_missing
  missing  = halving/root/orientation data after reaching twice one edge

q_plus_explicit_oriented_diagonal_split
  decision = normalize_to_one_edge_then_apply_source_snippet_intake
  missing  = same theorem data after explicit oriented diagonal-split
             normalization

q_wrong_zero_boundary_split
  decision = reject_zero_boundary_wrong_edge
  missing  = split data must recover one of m1,m2,m4,m8 with the current
             oriented boundary

q_square_exact_fp_value
  decision = repair_extraction_map_missing_after_two_root_row_payload
  missing  = two F_p row roots exist; DANGER3 framing and
             same-j/X_1(16)/halving or direct A,x0 extraction map still
             missing

q_square_value_up_to_scalar
  decision = repair_scalar_and_root_orientation_missing
  missing  = specified scalar before the two-root payload is concrete

q_square_sign_from_divisor_h90_or_phase
  decision = reject_sign_invisible_to_current_invariants
  missing  = constant sign has zero divisor/H90 boundary and does not alter
             exponent-character data

coset_selector_or_Q_source_only
  decision = repair_finite_value_divisor_theorem_missing
  missing  = finite value/divisor theorem for Q, Q^3, Q^6, or the selected Yang
             lift

Q6_boundary_only
  decision = repair_additive_or_value_normalization_missing
  missing  = scalar-fixed finite value/additive data, not just the Hilbert-90
             boundary

primitive_U_chi_power_only
  decision = repair_yang_lift_descent_and_finite_theorem_missing
  missing  = Yang lift, Hilbert-90 descent, and finite theorem for the selected
             row

pure_character_degree6_norm
  decision = reject_pure_character_degree6_norm_cancels
  missing  = Frobenius alternation makes the degree-6 norm zero

boundary_only
  decision = repair_boundary_only
  missing  = finite value/divisor identity for one legal row

ambient_value_no_period156
  decision = repair_value_without_period156_context
  missing  = canonical H0/Y507 period-156 branch/root/telescoping context

ambient780_mu11_power_only
  decision = repair_mu11_power_or_quotient_not_value
  missing  = actual period-156 branch/root/telescoping data selecting one F_p
             value

degree6_value_orbit_without_descent
  decision = repair_degree6_orbit_without_descent
  missing  = conjugate/norm descent back to F_p or Hilbert-90 ratio boundary

primitive_root_expression_degree6_only
  decision = repair_degree6_orbit_without_descent
  missing  = conjugate/norm descent back to F_p or Hilbert-90 ratio boundary

degree6_norm_without_selected_row
  decision = repair_descent_without_selected_legal_row
  missing  = legal support-156 row selection after descent

mixed_unit_without_yang_lift
  decision = repair_yang_lift_missing
  missing  = level-507 Yang lift to the support-156 product

mixed_yang_without_h90_descent
  decision = repair_h90_descent_boundary_missing
  missing  = Hilbert-90 descent with boundary Norm_156(Y_507)

yang_h90_source_without_finite_theorem
  decision = repair_value_divisor_theorem_missing
  missing  = finite value/divisor theorem for the selected support-156 row

yang_lift_wrong_boundary
  decision = reject_yang_lift_boundary_or_target_mismatch
  missing  = legal mixed conductor-39 target with Norm_156(Y_507) boundary

coefficient2_exact_root_value
  decision = normalize_cube_power_then_apply_source_snippet_intake
  missing  = same theorem data after cubing to coefficient 6

coefficient3_exact_root_value
  decision = normalize_square_power_then_apply_source_snippet_intake
  missing  = same theorem data after squaring to coefficient 6

coefficient1_exact_root_value
  decision = normalize_sixth_power_then_apply_source_snippet_intake
  missing  = same theorem data after taking the sixth power to coefficient 6

coefficient6_root_without_orientation
  decision = repair_coefficient6_root_orientation_missing
  missing  = explicit oriented root/sign data; square and sixth roots have a
             two-element kernel

scaled_boundary_as_current_target
  decision = reject_boundary_scale_mismatch
  missing  = power back to the coefficient-6 row or prove the current boundary
             directly

exact_power3_value
  decision = normalize_unique_3rd_root_then_apply_source_snippet_intake
  missing  = same theorem data after unique cube-root recovery in F_p^*

exact_power5_value
  decision = normalize_unique_5th_root_then_apply_source_snippet_intake
  missing  = same theorem data after unique fifth-root recovery in F_p^*

exact_power13_value
  decision = normalize_unique_13th_root_then_apply_source_snippet_intake
  missing  = same theorem data after unique thirteenth-root recovery in F_p^*

exact_power39_value
  decision = normalize_unique_39th_root_then_apply_source_snippet_intake
  missing  = same theorem data after unique 39th-root recovery in F_p^*

square_power_value_without_branch
  decision = repair_power_kernel_orientation_or_branch_missing
  missing  = explicit orientation, branch, or scalar data selecting one root

eleventh_power_value_without_branch
  decision = repair_mu11_power_or_quotient_not_value
  missing  = actual period-156 branch/root/telescoping data selecting one F_p
             value

mu11_scalar_unspecified
  decision = repair_root_of_unity_scalar_missing
  missing  = explicit mu_11 scalar or branch data fixing the value

mu39_scalar_as_fp
  decision = reject_root_of_unity_not_in_fp
  missing  = mu_39 is not contained in F_p^* for p25

exact_power11_value_with_branch
  decision = normalize_selected_power_value_then_apply_source_snippet_intake
  missing  = same theorem data after branch/scalar-selected eleventh-root
             recovery

power_divisor3_with_value_normalization
  decision = normalize_power_divisor_with_value_data_then_apply_source_snippet_intake
  missing  = same theorem data after finite normalization and unique root
             recovery

power_divisor3_without_value
  decision = repair_power_divisor_value_normalization_missing
  missing  = finite value/additive normalization fixing the powered value
             before rooting

power_boundary3_as_current
  decision = reject_scaled_boundary_as_current_target
  missing  = powered boundary eW is not the current W boundary unless it
             powers back to the row

divisor_h90_no_additive_normalization
  decision = repair_additive_normalization_missing
  missing  = finite additive/value/basepoint/telescoping normalization fixing
             the F_p^* scalar

additive_relation_without_selected_row
  decision = repair_selected_row_missing
  missing  = legal support-156 row selection before applying the additive
             normalization

normalized_additive_after_basepoint
  decision = normalize_additive_value_then_apply_source_snippet_intake
  missing  = same theorem data after additive/value normalization

w_boundary_nonunit_edge_combination
  decision = repair_edge_plus_boundary_zero_lattice
  missing  = finite value for the boundary-zero lattice part or direct one-edge
             theorem

wrong_product_row
  decision = reject_wrong_or_nonlegal_product_row
  missing  = one of the four legal payload hashes

finite_payload_no_source
  decision = repair_missing_arithmetic_source_theorem
  missing  = arithmetic source theorem

legal_minimal_h90_preimage_only
  decision = repair_selector_only
  missing  = finite value/divisor theorem for the corresponding support-156
             Yang product

support12_h90_preimage_boundary_control
  decision = reject_boundary_control_not_source_object
  missing  = proper-axis pushforward failure; only the four mixed support-12
             minimizers are legal

support_below_12_h90_selector
  decision = reject_h90_support_below_lower_bound
  missing  = orbitwise Hilbert-90 lower bound forces support at least 12

ksy_normalized_y_vocabulary_only
  decision = repair_exact_selector_theorem_missing
  missing  = compact C,D,K,orientation packet or exact equal-weight 75-atom
             theorem

raw_kubert_lang_exponent_balance_only
  decision = repair_theta2_intake_missing
  missing  = accepted theta2/theta2-inverse divisor-additive payload or
             compact KSY theta2 certificate

exactp_branchless_orientation_word
  decision = repair_exactp_orientation_branch_missing
  missing  = one of the four raw center/reverse branches and theta2/theta2^-1
             output

exactp_theta2_value_without_period156_context
  decision = repair_period156_branch_selection_missing
  missing  = period-156 theta2 fixedness, branch/root, or telescoping context

wrong_exactp_packet
  decision = reject_wrong_exactp_payload
  missing  = compact exact-P packet C=(47,28), D=(22,3), primitive K=(57,0),
             with accepted orientation

nonuniform_or_missing_exactp_atoms
  decision = reject_by_finite_geometry_rigidity
  missing  = finite geometry forces the exact equal-weight 75-atom payload

exactp_ambient_period780_value_only
  decision = repair_period156_branch_selection_missing
  missing  = period-156 branch/root/telescoping context or divisor/additive
             normalization

unified_theorem_as_exactp_recovery
  decision = repair_reverse_selector_structure_missing
  missing  = exact-P C,D,K,orientation, equal-weight 75-atom selector theorem,
             period-156 theta2 payload, or explicit reverse reconstruction
             theorem

quartic_selector_finite_theorem
  decision = source_stage_win_danger3_framing_missing
  missing  = DANGER3 finite-identity / non-CM framing

exact_quartic_selector_without_value_theorem
  decision = repair_value_divisor_theorem_missing
  missing  = scalar-fixed finite value/divisor theorem for the selected row

coarse_quartic_phase_or_magnitude_only
  decision = repair_quartic_edge_selection_missing
  missing  = exact row-antisymmetric C4_1 phase selecting one legal edge

quartic_phase_without_row_sign
  decision = repair_mixed_tensor_missing
  missing  = row-antisymmetric mixed tensor structure for the conductor-39
             source row

same_parity_quartic_phase
  decision = reject_zero_boundary_wrong_edge
  missing  = same-parity edges have zero W boundary or the wrong mixed tensor
             target

quartic_phase_boundary_sign_unspecified
  decision = repair_reciprocal_orientation_or_boundary_sign_missing
  missing  = oriented row data or reciprocal row with -Norm_156 boundary

quartic_phase_collision_as_different_edge
  decision = repair_phase_orientation_collision
  missing  = boundary sign/orientation data distinguishing reciprocal row
             from the opposite oriented edge

quartic_reciprocal_phase_plus_boundary
  decision = reject_orientation_boundary_mismatch
  missing  = reciprocal phase carries -Norm_156 boundary, not the positive
             boundary

full_submission
  decision = submission_ready
  missing  = none
```

## Counts

```text
evidence_markers_ok = 31/31
source_stage_closing_shapes = 6
direct_submission_shapes = 1
current_source_stage_closers = 0
current_submission_ready = 0
```

## Verdict

Normalize row presentations through
`evidence/p25_v2_row_orbit_normalization_20260616.md`, then use this intake
before promoting any new source or expert answer:

```text
1. After normalization, does it match one of the four legal payload rows or the
   exact-P upstream bridge?
2. Does it supply an arithmetic source theorem, not only legality or a finite
   computation?
3. If it is a reciprocal/outside-doubling presentation, does it include the
   reciprocal orientation and `-Norm_156(Y_507)` boundary sign, or can it be
   rewritten as an oriented legal row?
4. If it invokes Koo-Shin Theorem 5.2, does it avoid the constant-span
   obstruction rather than multiplying powers of the four legal rows?
5. If it is stated in character language, does it give the exact
   row-antisymmetric `C4_1` phase, not only one sign, magnitude, quadratic
   component, or boundary-visible component?
6. If the exact phase is reciprocal or misoriented, does it include oriented
   row data or boundary sign? Reciprocal phase with positive boundary is
   rejected.
7. If it proves the broad quadratic aggregate, a diagonal pair, or all four
   rows, does it also select or factor to one sparse edge with the original
   `W` boundary?
8. If it proves a row quotient, or combines a diagonal aggregate with a row
   quotient, does it also provide the halving/root/orientation data needed to
   select one legal row?
9. If it proves a row square or doubled-boundary row-square theorem, does it
   include explicit root/sign/orientation data selecting the oriented legal
   row?
10. If it gives divisor plus H90 boundary but only up to an unspecified
   `F_p^*` scalar, does it supply additive/value normalization or finite
   framing fixing that scalar?
11. If it gives only the dense period norm or its value, does it also give a
   legal support-156 Hilbert-90 descent selecting one row?
12. If a descent uses a formal one-coset boundary control, reject it unless it
   repairs the mixed-axis pushforward failure. If it uses the compact
   conductor-39 quotient `Q`, require a `Q` value theorem with period-156
   context or a finite theorem for the H90 preimage `Q^3`; `Q` source-only,
   `Q^6` boundary-only, primitive-power-only, and pure degree-6 norm claims
   stay repair/reject rows. If it uses the Q diagonal projection
   `m1+m4=m2+m8`, require an explicit oriented split/root or direct one-edge
   theorem before source-stage promotion. If it gives an exact scalar-fixed
   `F_p` value for the resulting Q square, route it as a bounded two-root
   row-value payload with extraction map still missing; value-up-to-scalar or
   sign-from-invariants claims are repair/reject rows.
13. If it is ambient-period-780 value data, does it select an actual
   period-156 branch rather than only an 11th power or `mu_11` quotient?
14. If it is degree-6 value data, does it descend to `F_p` and select one
    legal support-156 row, or provide an equivalent Hilbert-90 ratio boundary?
15. If it is conductor-39 source language, does it include the Yang lift,
    Hilbert-90 descent/boundary, and finite value/divisor theorem rather than
    stopping at source identification?
16. If it is a lower-coefficient root theorem, does it give exact data that can
    be powered back to the coefficient-6 current row?
17. If it extracts a square or sixth root from coefficient-6 data, does it
    provide oriented root/sign data?
18. If it gives an exact power value, is the power map bijective on `F_p^*`
    for p25? Cube, fifth, thirteenth, and thirty-ninth powers can be uniquely
    rooted; square, fourth, eleventh, twenty-second, forty-fourth, 156th, and
    780th powers need branch/orientation/scalar data.
19. If it invokes a root-of-unity scalar, is that scalar group actually in
    `F_p`? `mu_11` and `mu_44` ambiguities are real repair rows, while `mu_39`
    as an `F_p` scalar is rejected.
20. If it gives a powered divisor/additive or H90-boundary theorem, does it
    also include finite value/additive normalization? Exact power values can be
    rooted; powered boundary data alone is not a current-row theorem.
21. If it says "divisor/additive," does the additive side actually fix the
    `F_p^*` scalar by finite additive/value/basepoint/telescoping data?
22. If value-side, does it include canonical H0/Y507 period-156
    branch/root/telescoping context?
23. If it is stated as a source-graph edge combination, is it exactly one unit
    edge? Coefficient sum `1` gives the right boundary scale but non-unit
    vectors are still edge plus boundary-zero lattice content.
24. If it is stated as an H90 selector, does it respect the support lower
    bound and then pass the legal mixed-minimizer screen? Support below 12 is
    impossible; nonlegal support-12 preimages are boundary controls.
25. If it is stated as exact-P, does it satisfy the minimal exact-P hook:
    compact C,D,K with one of the four accepted orientation branches, exact
    equal-weight 75-atom theorem, accepted theta2/theta2-inverse payload with
    period-156 context, or explicit reverse reconstruction theorem?
26. If source stage closes, route it through the post-theorem extraction router.
```

A snippet that fails one of those checks may still be useful context, but it is
not a source-stage close.

For expert answers rather than raw source snippets, use
`evidence/p25_v2_current_expert_response_rubric_20260616.md`; it adds the
repair/reject and extraction-progress rows needed for conversation routing.
