# p25 Moonshot Targeted Lit Search Contracts

Updated: 2026-06-13

Result artifact:

```text
research/p25/p25_moonshot_targeted_lit_search_results_20260613.md
```

## Current Missing Bridge

The strongest Jacobi-side formal target is no longer a vague mixed correction.
For the square-axis `C_3 x C_169` quotient, the Gross-Koblitz carry data gives
odd and even Frobenius `p^2` half-orbit averages:

```text
O support = (0,1), (0,2), (2,1)
E support = (0,1), (0,2), (1,2)
```

Thus:

```text
O*(1-E) = indicator((h,t) = (2,1))
```

and the outer `S` layer gives exactly:

```text
{138, 310, 482}
```

The finite payload is closed after adding the deterministic `C_13` fiber
background: the kernel-trivial raw lift has length `12675`, support `6300`,
and passes the ray-local raw-Y harness.  The missing step is arithmetic
realization of `O*(1-E)` as an actual unit phase or identity.

## Scout Contracts

### A. Hasse-Davenport / Gross-Koblitz Unit Phase

Find an identity that realizes the even/odd half-orbit interaction as a unit
quotient, not merely as a valuation or support statement.

Required output:

- citation URLs and exact theorem/equation names
- proposed mapping to `O*(1-E)`
- first finite falsifier or gate command
- continue/kill recommendation

Kill if the result only explains Stickelberger support, only gives a strict
one-digit carry, or cannot distinguish the odd leakage cells `(0,1),(0,2)`
from the anomaly `(2,1)`.

### B. Finite Hypergeometric / Barnes Delta

Find a finite-field hypergeometric, Greene, Helversen-Pasotto, or Barnes-delta
collapse whose resonance can fire on the single anomaly cell or on the same
even/odd orbit-parity interaction.

Required output:

- citation URLs and exact theorem/equation names
- resonance condition and mapping to the `X^3Y` anomaly
- first finite falsifier or gate command
- continue/kill recommendation

Kill if the delta term fires on any selected non-anomaly cells, if the product
part is only dense scalar balancing, or if the identity reduces to a plain
Jacobi-log shadow.

### C. Robert / Siegel / KSY Anti-Invariant Unit

Find a CM elliptic-unit, Siegel-Ramachandra, Kubert-Lang, divisor quotient,
`y`/differential, or conjugate-unit mechanism that produces the exact raw
anti-invariant K-traced product, up to the now-recorded gauge/orientation
freedom.

```text
raw C = (47,28)+aK or -C=(28,141)+aK
raw D = +/-(22,3)+bK
K     = primitive multiplier of (57,0)
a,b mod 25
```

Accepted orientation branches:

```text
C,  y(A)/y(-A) -> theta2 inverse
C,  y(-A)/y(A) -> theta2
-C, y(A)/y(-A) -> theta2
-C, y(-A)/y(A) -> theta2 inverse
```

Required output:

- citation URLs and exact theorem/object names
- how the object emits the raw center, oriented D segment, primitive K trace,
  and product orientation
- whether the emitted object is divisor/additive data, finite-field unit
  values, or a differential identity; value-level hits must also explain
  period-156 theta2 fixedness/telescoping, not only the ambient period-780
  orbit
- first finite falsifier or gate command
- continue/kill recommendation

Kill if the object separates into right-trace times C-axis selector, is even
under simultaneous source inversion, supplies only a scalar C-character, uses a
nonprimitive K, or shifts `C`/`D` outside the kernel-gauge plus D-reversal
contract.

## Local Gates

```sh
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_half_orbit_interaction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_gross_koblitz_projector_raw_y_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_source_matrix_harness_gate.py \
  --source-matrix PATH

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_bridge_edge_quotient_contract_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_reflection_orientation_contract_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_certificate_router_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_raw_orientation_value_route_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_theorem_hit_router_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_primary_source_exactness_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_siegel_formula_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_context_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_theorem_legality_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closure_theorem_template_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_clause_audit_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_primary_source_anchor_packet_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_period_value_upgrade_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_exact_product_intake_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_claim_intake_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_danger3_framing_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_source_parameter_hygiene_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_mixed_graph_obligation_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_submission_extraction_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_robert_ksy_theta2_kubert_lang_ksy_y_closing_theorem_obligation_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_primary_source_scout_packet_gate.py

PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_ksy_exact_p_primary_source_scout_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_kubert_lang_mixed_graph_primary_source_scout_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_kronecker_d2_primary_source_scout_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_siegel_robert_period_value_primary_source_scout_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_danger3_framing_extraction_primary_source_scout_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_post_scout_moonshot_reduction_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_exact_divisor_lane_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_sprang_source_split_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_ksy_source_split_gate.py

PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_priority1_theorem_query_packet_gate.py
```

## Subagents

Future lit scouts should be artifact-gated, not time-gated: one theorem
surface, one source-clause target, one local command/falsifier, and a
continue/kill recommendation.  Broad relevance searches are killed unless they
return a candidate that routes through the source-claim, exact-product,
period-value, source-parameter, mixed-graph, or DANGER3-framing intake gates
above.  For Kubert-Lang/Siegel hits, the minimum useful payload is now exact
row-labeled pairs, quotient reflection-center data, or the raw K-traced product;
`C169` projection and KL congruences alone are screens, not products.
For anything claiming to finish the theorem side, run the closing-theorem
obligation gate.  For anything claiming to finish the challenge side, run the
submission-extraction gate or provide a concrete `(p,A,x0)` that passes
official `vpp.py`.  For anything claiming to be a useful literature scout,
route it through `p25_ksy_y_primary_source_scout_packet_20260613.md`: one
source handle, one positive payload, one first falsifier, one local gate/probe,
and a continue/kill recommendation.

```text
HD/GK unit phase: Harvey 019ec239-3f5a-7960-8d6b-37ea560a75bd complete
Barnes/hypergeometric: Hilbert 019ec239-3fa4-7380-b4b0-be57836e90a5 complete
Robert/Siegel: Planck 019ec239-3fd6-7bc2-a5c2-d90930a4c003 complete
```
