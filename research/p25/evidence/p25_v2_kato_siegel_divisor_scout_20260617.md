# P25 v2 Kato-Siegel Divisor-Source Scout

Updated: 2026-06-17

Marker: `p25_v2_kato_siegel_divisor_scout_rows=1/1`

## Purpose

Run one narrow external-source pass against the live primary row ask. The
question was whether the Kato-Siegel / modular-unit literature already gives
the missing p25 theorem:

```text
one legal support-156 row R_m
+ arithmetic source theorem
+ Norm_156(Y_507) boundary
+ scalar-fixed finite F_p value/additive payload
```

Verdict: Kato-Siegel functions are the closest framework found in this pass,
because they supply canonical modular units with prescribed divisors and norm
compatibility. They do not, as inspected here, supply the row-selected p25
finite value/additive payload. This is a useful repair row, not a source-stage
closer.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_live_theorem_ask_packet_20260617.md`
- `evidence/p25_v2_constructive_value_payload_contract_20260616.md`
- `evidence/p25_v2_source_snippet_intake_20260616.md`
- `evidence/p25_v2_additive_normalization_contract_20260616.md`
- `evidence/p25_v2_source_stage_normalization_spine_20260617.md`

## External Sources Checked

- A. J. Scholl, *An introduction to Kato's Euler systems*:
  `https://www.dpmms.cam.ac.uk/~ajs1005/preprints/euler.pdf`
- A. Landesman et al., *Modular Symbols with Values in Beilinson-Kato Distributions*:
  `https://arxiv.org/pdf/2311.14620`
- Ja Kyung Koo, Gilles Robert, Dong Hwa Shin, Dong Sung Yoon, *On Siegel invariants of certain CM-fields*:
  `https://arxiv.org/pdf/1508.05602`
- A. Beeson, *Roots of Modular Units*:
  `https://www.sas.rochester.edu/mth/people/faculty/tucker-amanda/assets/pdf/roots_of_modular_units.pdf`
- D. Kubert and S. Lang, *Units in the Modular Function Field. II. A full Set of Units*:
  `https://eudml.org/doc/162791`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kato_siegel_divisor_scout_gate.py
```

The gate returned `p25_v2_kato_siegel_divisor_scout_rows=1/1`.

## Source Rows

```text
scholl_kato_siegel_functions
  useful = canonical Kato-Siegel functions with prescribed divisors and norm
           compatibility
  gap    = does not select the p25 support-156 row or give finite F_p
           scalar/value data
  route  = repair_divisor_theorem_not_finite_row_payload

beilinson_kato_distribution_note
  useful = constructs functions with explicit torsion-point divisors using
           Kato-Siegel functions
  gap    = divisor construction is not an evaluable p25 row value and warns
           against overclaiming canonical form
  route  = repair_divisor_only_not_source_stage_close

koo_robert_shin_yoon_siegel_invariants
  useful = records Siegel-Ramachandra invariant value and class-field/Galois
           action language
  gap    = class-field generation/special-value language is not the p25
           support-156 finite row theorem
  route  = support_value_framework_not_p25_hook

beeson_roots_of_modular_units
  useful = bounds the level of a modular-unit root when such a root is again
           modular
  gap    = root-level control does not choose the p25 row root/sign or finite
           scalar
  route  = support_root_guardrail_not_closer

kubert_lang_units
  useful = anchors modular-unit generator theory and full-set vocabulary
  gap    = generator theory alone does not emit the row-specific finite theorem
  route  = support_generator_framework_not_closer
```

## The Close-But-Not-Enough Point

The closest theorem-shape is the Kato-Siegel divisor theorem: it can provide a
canonical modular unit with a prescribed divisor, and related work uses
Kato-Siegel functions to manufacture torsion-point divisor functions. For p25,
that still stops before the live source-stage row.

The missing extra clauses are:

```text
row label in {m=1,2,4,8} or an equivalent normalized row
Norm_156(Y_507) boundary for that row
finite F_p value, finite additive formula, basepoint, telescoping product, or
  period-156 branch/root payload fixing the scalar
challenge-legal arithmetic source theorem specialized to the p25 row
```

In other words, a future citation to Kato-Siegel functions should be accepted
only if it supplies the p25 specialization and finite payload. A citation that
stops at prescribed divisors or norm compatibility is now a named repair row.

## Counts

```text
evidence_markers_ok = 5/5
primary_external_sources_checked = 5
divisor_source_theorems_found = 1
finite_p25_row_value_theorems_found = 0
current_source_stage_closers = 0
current_submission_ready = 0
p25_v2_kato_siegel_divisor_scout_rows=1/1
```

## Verdict

Continue the first-pass row theorem search, but classify generic Kato-Siegel
or modular-unit divisor citations as repair unless they add the finite p25
row payload. The best follow-up ask is now sharper:

```text
Can the Kato-Siegel canonical divisor function be specialized to one of the
four p25 support-156 rows with Norm_156(Y_507) boundary and an explicit finite
F_p value/additive/telescoping normalization?
```
