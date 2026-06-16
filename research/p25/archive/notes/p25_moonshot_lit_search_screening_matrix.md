# p25 Moonshot Literature Search Screening Matrix

Updated: 2026-06-13

## Purpose

Use this matrix to turn literature-search hits into finite p25 tests.  A paper
or identity is useful only if it suggests a producer for the already-audited
Lane B target, not merely a new description of the same shadow.

Current local contract:

- target quotient: `C_3 x C_169`, raw lift order `12675 = 25 * 507`
- accepted bridge: block-constant, kernel-trivial, support `150`
- quotient bridge: `S*X*Y^-2*(1 - X^2*Y^3)`
- Hilbert-90 corner: `K`-traced row-quadratic corner, primitive unit sign
  `eps`, branch coefficient `a`, row-labeled unit triangle
- theta/Jacobi shortcuts already killed: plain Jacobi logs, single theta edge,
  affine relabeling, sparse translated-edge repair, source-row shear, and the
  strict one-digit Gross-Koblitz carry-only twist
- Jacobi positive clue: the cyclic multi-digit Gross-Koblitz/Stickelberger
  signature for `N=507` and `N=12675` is positive exactly on the non-selected
  cells plus the selected anomaly `(2,1)`.  Its quadratic Frobenius-frequency
  projector flattens the Lucas coefficient anomaly to the all-one seed; it
  formally closes the square-axis raw-Y harness after adding the C13 fiber
  background.  Equivalently, the projector is the Lucas/no-borrow selected
  support times the odd Frobenius `p^2` half-orbit average.  More sharply, it
  is `O*(1-E)`, where `O` and `E` are the odd/even half-orbit averages.  It
  still needs an arithmetic unit-phase realization.  Additive averages
  `1, selected, O, E` do not span the anomaly; a product, delta, or equivalent
  resonance is required.  Barnes support screening now kills order-3-only HP
  product deltas, keeps the full `C_507` seed-exponent point delta `q=138`
  support-live, and kills `p^2` orbit-closed deltas as too large.  McCarthy's
  well-poised exceptional character delta is now numerically verified over
  `F_2029` as a theorem-level point-delta producer for `q_exp=138` before
  orbit closure, and its outer `S` image is verified to land on the existing
  raw-Y payload closure.  The naive HD/GK reflection precheck leaves a
  signed two-cell residue on `(1,2)` and `(2,1)`; semiprimitive cubic purity
  rewrites `U(169)` to `1`, but still leaves the signed scalar false positive,
  so reflection plus this unit rewrite remains too weak
- Robert shortcut already killed: literal x-only/even source tables under
  `(right,c)->(-right,-c)`
- Robert positive contract: coupled D-segment/K-trace support plus active
  C-side odd phase; neither piece alone is sufficient
- Robert phase obstruction: the active odd phase is not a plain `C_169`
  character or sign tag
- Robert quotient-edge contract: after the coupled `K` trace and `D` segment,
  the negative layer must be the positive layer translated by `(2,113)` in
  `C_3 x C_169`; raw representatives are exactly `T=(38,113)` plus the
  kernel trace class
- Robert translated-quotient skeleton: point quotient plus kernel trace is too
  small, inverse edge is the wrong orientation, even/squared edge
  symmetrizations expand to `225` raw cells, and omitting the kernel trace
  leaves all `25` kernel modes.  The live finite shape is exactly
  `base * K_trace * D_segment * (1 - T)`.  The visible quotient skeleton is
  rigid: `D=(1,3)` up to reversal and `T=(2,113)` are the only AP/edge
  factorization.  Raw representative freedom is exactly kernel gauge:
  forward and reversed segments have `25^3` valid raw choices each, and
  non-kernel right/C shifts fail.  The literal Kato/Robert finite-subgroup
  divisor quotient is killed because the required `D_segment` is not subgroup
  or subgroup-coset support

Primary harness files:

- `research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py`
- `research/p25/p25_laneB_square_axis_bridge_candidate_harness_gate.py`
- `research/p25/p25_laneB_robert_source_matrix_harness_gate.py`
- `research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py`
- `research/p25/p25_laneB_robert_kato_subgroup_support_falsifier_gate.py`
- `research/p25/p25_laneB_robert_x_difference_even_obstruction_gate.py`
- `research/p25/p25_laneB_robert_oriented_phase_contract_gate.py`
- `research/p25/p25_laneB_robert_c_phase_character_obstruction_gate.py`
- `research/p25/p25_laneB_robert_bridge_edge_quotient_contract_gate.py`
- `research/p25/p25_laneB_robert_translated_odd_quotient_skeleton_gate.py`
- `research/p25/p25_laneB_robert_translated_odd_quotient_rigidity_gate.py`
- `research/p25/p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py`
- `research/p25/p25_laneB_square_axis_bridge_theta31_source_shear_obstruction_gate.py`
- `research/p25/p25_laneB_square_axis_bridge_hilbert90_source_chain_corner_unit_triangle_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_carry_twist_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate.py`
- `research/p25/p25_laneB_square_axis_barnes_delta_support_gate.py`
- `research/p25/p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py`
- `research/p25/p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py`
- `research/p25/p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py`
- `research/p25/p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py`

## Screening Rows

| Lane | Literature Hit Must Supply | First Local Falsifier | Positive Artifact |
| --- | --- | --- | --- |
| Hilbert-90 anti-invariant producer | A finite-field or divisor construction with a semilinear sign local system: ordinary `p^39` trace may vanish, but a pairwise-odd line survives and can carry equal weights on the three `S=172` bridge pairs. | Test whether the proposed half-orbit support is block-constant on the raw `C_25` trace and whether it gives the signed bridge rather than the unsigned hull. | Raw candidate vector for `profile_candidate(...)`, or a quotient word proving the signed pairwise-odd bridge without dense scalar repair. |
| Hasse-Davenport / Jacobi mixed correction | An identity beyond plain logs and beyond a strict one-digit carry valuation. It must change the packet, not just an edge or coordinate shear, and must plausibly cancel the `q*S*X^3Y` anomaly while keeping the all-one no-borrow/Lucas support. The cyclic multi-digit signature and its quadratic Frobenius projector already give a formal quotient-level anomaly correction whose kernel-trivial lift passes the square-axis raw-Y harness. The missing piece is arithmetic realization as an HD/GK/Barnes unit phase, preferably the even/odd half-orbit interaction `O*(1-E)`. Additive half-orbit averages are too weak; the hit must supply a product, delta, reflection sign, or equivalent resonance. Barnes support screening says an order-3-only HP product delta is too broad, while a full `C_507` seed point delta `q=138` remains support-viable; McCarthy's well-poised exceptional term now numerically realizes the single `q_exp=138` transformed-difference delta over `F_2029` and maps to the existing raw-Y payload closure. Naive HD/GK reflection gives a signed `(1,2)/(2,1)` residue; semiprimitive cubic purity removes the free `U(169)` symbol but not the `(1,2)` false positive. | Feed the induced packet or correction through the theta edge/direction/source-shear/carry-twist/multi-digit-signature/Frobenius-projector/half-orbit/interaction/linear-span/Barnes-support/McCarthy-delta/gamma-reflection/semiprimitive-unit/raw-Y screens; reject if it is a canonical theta packet plus shear, a strict carry-only twist, a support-only valuation, additive even/odd averaging without product interaction, odd-half-orbit leakage without even-half-orbit cancellation, order-3-only HP line support, `p^2` orbit-closed delta support, reflection-only signed two-cell gamma residue, semiprimitive unit cleanup with the `(1,2)` scalar still present, a formal projector with no unit phase, or a dense scalar-balance representative. | Normalize McCarthy parameters as an actual p25 Jacobi/Barnes unit phase whose point delta survives as the raw-Y / bridge payload without dense scalar background, while preserving kernel-triviality, raw `D^3=Y`, and source graph constraints. |
| Ray-class / CM / modular-unit inert-split coupling | A product formula or divisor relation coupling the inert/ray-local right source (`151`) to the split C-axis source (`677`), not a split-prime-only class quotient or x-only even table. It must supply both the coupled D/K support and active C-side odd orientation, and the orientation cannot be a plain `C_169` character. The finite quotient edge must be `(2,113)` modulo the `C_25` kernel trace. For translated odd quotients, the live skeleton is `base*K_trace*D_segment*(1-T)`, not a point quotient or even edge, the quotient AP/edge is rigid, and raw representative freedom is only kernel gauge. Literal Kato/Robert subgroup-divisor support is killed; a live hit must be weighted/non-subgroup, such as `y`, `wp'`, Siegel/Klein, differential, or finite-difference quotient data. | Check rectangle constancy, right/C mixed character payload, source mask coupling, inversion parity, oriented-phase contract, C-character obstruction, bridge-edge quotient contract, translated-odd-quotient skeleton, AP/edge rigidity, raw-gauge class, sparse-source intake, and Kato subgroup-support falsifier; reject separated right-trace-times-C selectors, pure-C shadows, literal x-only tables even under `(right,c)->(-right,-c)`, point quotients without `D_segment`, C-side phases without coupled support, scalar-normalized C-character tags, pure C-side or pure right-side edge controls, inverse edges, even/squared edge symmetrizations, missing kernel trace, alternate visible AP/edge factorizations, non-kernel raw representative shifts, and literal subgroup/coset support for the required `D_segment`. | Explicit source-coordinate mask or raw divisor values whose normalized trace matches the bridge and has all `336` mixed right/C characters, preferably emitted as `base*K_trace*D_segment*(1-T)` from a weighted Kato-Siegel, `y`, `wp'`, differential, Siegel/Klein, or finite-difference quotient using the recorded `D` and `T`, with raw coordinates normalized only by kernel gauge. |

## Immediate Kill Conditions

Reject a literature hit if its finite reduction is only one of:

- ordinary trace or Frobenius averaging of the bridge
- plain Jacobi-log / Hasse-Davenport shadow
- single finite difference of the canonical `theta_{3,1}` packet
- affine, diamond, Frobenius, product-affine, or source-row-shear relabeling
- sparse translated sum of canonical theta edges
- strict one-digit Gross-Koblitz carry-only twist for the `X^3Y` anomaly
- multi-digit Gross-Koblitz valuation support, odd half-orbit support, or
  formal even/odd half-orbit interaction with no arithmetic unit phase or raw
  candidate vector
- additive linear combinations of `1`, selected support, odd half-orbit, and
  even half-orbit with no product, reflection, delta, or equivalent resonance
- order-3-only Barnes/Helversen-Pasotto product deltas, which have line support
  through the anomaly, or any delta first closed under the full `p^2` orbit
- naive HD/GK reflection-only gamma residue, which leaves both `(1,2)` and
  `(2,1)` with opposite free `U(169)` coefficients
- semiprimitive cubic unit cleanup alone, which removes `U(169)` but leaves the
  signed `(1,2)` false-positive scalar
- McCarthy/Barnes exceptional terms that leak outside the single `q=138`
  support before the outer `S` layer
- literal Robert x-only table or any scalar function even under simultaneous
  source inversion
- active C-side orientation applied only to a separated axis hull, without the
  coupled D-segment/K-trace support
- scalar-normalized `C_169` character, root-of-unity phase, or sign tag as the
  whole active orientation
- pure C-side `(0,113)` or pure right-side `(38,0)` bridge-edge controls
  instead of the coupled quotient edge `(2,113)` modulo the kernel trace
- translated quotient point edges without `D_segment`, inverse edge orientation,
  even/squared edge symmetrizations, or missing `K_trace`
- alternate visible AP segment or translated edge in the Robert/Siegel skeleton
  instead of `D=(1,3)` up to reversal and `T=(2,113)`
- non-kernel raw representative changes for base, `D`, or `T`; only kernel
  gauge `K=(57,0)` is allowed
- literal Kato/Robert finite-subgroup divisor support for `D_segment`, since
  the required visible/raw `D` segment is not a subgroup or subgroup coset
- separated right-kernel trace times a C-axis selector
- dense scalar balancing or row-constant selected-kernel repair
- proper `C_13` pullback of the `C_169` target
- sign-only Legendre/quartic tag on the existing local source residues

## First Probe Template

For any promising identity, instantiate a finite vector or quotient mask and
```text
source:
identity:
finite object:
expected raw length:
expected quotient support:
expected raw support:
kernel mode prediction:
does it force the row-labeled unit triangle:
first command/probe:
continue_or_kill:
```

Preferred first commands:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_ray_local_theta31_pullback_falsifier_gate.py \
  --case square_axis_C3xC169 \
  --raw-y PATH

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_bridge_candidate_harness_gate.py \
  --raw-candidate PATH

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_source_matrix_harness_gate.py \
  --source-matrix PATH

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_sparse_source_candidate_harness_gate.py \
  --sparse-source PATH

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_x_difference_even_obstruction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_oriented_phase_contract_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_c_phase_character_obstruction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_bridge_edge_quotient_contract_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_skeleton_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_rigidity_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_translated_odd_quotient_raw_gauge_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_kato_subgroup_support_falsifier_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_carry_twist_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_multidigit_signature_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_frobenius_projector_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_linear_span_obstruction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_barnes_delta_support_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_delta_contract_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_numeric_delta_raw_y_bridge_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_semiprimitive_unit_rewrite_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_gamma_reflection_precheck_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py
```

If the object is not yet a raw vector, make a small dedicated gate that prints
one `..._rows=1/1` marker and exits nonzero on mismatch.
