# P25 v2 Constructive Payload Source Scan

Updated: 2026-06-16

## Purpose

Apply the constructive value payload contract to the local primary-source
corpus. This scan is narrower than a broad literature reread: it records
helper vocabulary, but a positive row requires p25-specific finite data that
can be evaluated or packetized.

The scan asks whether any local source emits one of the constructive payload
hooks:

```text
exact F_p row value
finite additive or telescoping formula
period-156 branch/root payload
exact product packet plus arithmetic source theorem
compact exact-P C,D,K,orientation packet
DANGER3 extraction payload
```

## Sources Read

- `incoming/extracted/s00209-008-0456-9.pdf.extract.txt`
- `incoming/extracted/1007.2307/ray_class_fields.tex`
- `incoming/extracted/1007.2318v1.pdf.extract.txt`
- `incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex`
- `incoming/extracted/sprang_1802_04996/deRhamRealization.tex`

## Pages Read

- `frontier.md`
- `sources/koo-shin-2010.md`
- `sources/koo-shin-yoon-1007-2307.md`
- `sources/koo-shin-ii-1007-2318.md`
- `sources/sprang.md`
- `evidence/p25_v2_constructive_value_payload_contract_20260616.md`
- `evidence/p25_v2_source_family_gap_matrix_20260616.md`
- `evidence/p25_v2_additive_normalizer_source_scan_20260616.md`
- `evidence/p25_v2_sprang_theta2_source_intake_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_constructive_payload_source_scan_gate.py
```

The gate returned `p25_v2_constructive_payload_source_scan_rows=1/1`.

## Source Rows

```text
koo_shin_2010_mathz
  helper_terms = Theorem 5.2, Theorem 6.2, product of Siegel functions,
                 distribution relation, root of unity,
                 generators of K(X1(N))
  p25_payload_terms = none
  decision = helper_source_not_constructive_payload
  missing  = exact p25 row value, product packet, period-156 payload, or
             DANGER3 extraction data

ksy_1007_2307_normalized_y
  helper_terms = normalization, ray class, Siegel, Lang-Schertz, Klein forms
  p25_payload_terms = none
  decision = exactp_vocabulary_not_constructive_payload
  missing  = compact C,D,K,orientation packet, exact 75-atom theorem, or
             period-156 bridge

koo_shin_ii_1007_2318
  helper_terms = normal basis, ray class, Siegel, generator, ring class,
                 Kronecker
  p25_payload_terms = none
  decision = background_source_not_constructive_payload
  missing  = one-edge theorem, exact p25 product packet, or period-156 value
             payload

sprang_1801_05677
  helper_terms = Eisenstein-Kronecker, Poincare, Kronecker theta,
                 p-adic theta, distribution relation, Kato-Siegel
  p25_payload_terms = none
  decision = d2_support_not_constructive_p25_payload
  missing  = exact theta2/theta2-inverse p25 payload, compact KSY packet, or
             period-156 branch data

sprang_1802_04996
  helper_terms = de Rham, polylogarithm, Kronecker section, Kato-Siegel,
                 distribution relation, dlog thetaD
  p25_payload_terms = none
  decision = derham_support_not_constructive_p25_payload
  missing  = evaluable p25 row or exact-P packet
```

## P25 Payload Terms Screened

```text
Norm_156 / Norm 156
Y_507 / Y507
period-156 / period 156
support-period / support period 156
C_75
C_169
C_3 x C_169
C,D,K / C, D, K
K_trace
D_segment
theta2 / theta_2 / theta2 inverse / theta2-inverse
75-atom / 75 atom
X_1(8112) / X1(8112)
A,x0 / (A,x0)
vpp.py
```

## Counts

```text
raw_sources_available = 1
source_rows = 5
helper_rows = 5
p25_payload_term_rows = 0
packetizable_source_payloads = 0
source_stage_closers = 0
current_submission_ready = 0
```

## Verdict

```text
positive_artifact = local constructive-payload source scan
continue_first_pass = yes, but not through these source texts as written
intake_rule = helper vocabulary is not enough; source text must name a p25
              constructive payload hook before promotion
discard_condition = source lead only repeats normalized-y, ray-class,
                    Siegel-product, Kronecker-theta, distribution, or
                    de Rham/Kato-Siegel support vocabulary
```

This is a sharper negative result than the additive-normalizer scan. The local
sources are still useful for vocabulary and source legality, but none currently
provides evaluable finite p25 data that can enter candidate-packet intake.
