# P25 v2 H0 / Conductor-39 Canonical Frontier Pass

Updated: 2026-06-16 07:24 PDT

## Purpose

Run the first v2 theorem-frontier pass from the reorganized cockpit, using only
canonical pages and the Koo-Shin 2010 source text. The question was whether the
currently supplied Koo-Shin 2010 paper can be promoted from source-legality
evidence to a source-stage closer for either H0 or mixed conductor 39.

## Pages Read

- `frontier.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `sources/koo-shin-2010.md`
- `evidence/p25_ksy_y_h0_koo_shin_source_clause_matrix_20260614.md`
- `evidence/p25_ksy_y_koo_shin_2010_theorem62_conductor39_unit_20260614.md`
- `evidence/p25_ksy_y_h0_conductor39_first_pass_theorem_triage_20260614.md`
- `evidence/p25_ksy_y_external_source_theorem_obligation_matrix_20260614.md`

## Probes

Source text used in the private live-run incoming layer:

```text
incoming/extracted/s00209-008-0456-9.pdf.extract.txt
```

Commands:

```bash
rg -n -i "Hilbert|period.?156|Norm.?156|Y_?507|level.?507|507" \
  incoming/extracted/s00209-008-0456-9.pdf.extract.txt

rg -n -i "divisor|additive|distribution|finite.?field|value theorem|evaluate|evaluation" \
  incoming/extracted/s00209-008-0456-9.pdf.extract.txt

rg -n "507|156|Norm_156|Y_507|U_chi|V_bal|chi_39|chi_3|chi_13|C_3|C_169" \
  incoming/extracted/s00209-008-0456-9.pdf.extract.txt

rg -n "N = 39|N=39|level 39|/Gamma11\\(39\\)|X1\\(39\\)|39\\)" \
  incoming/extracted/s00209-008-0456-9.pdf.extract.txt

rg -n -i "Hilbert-90|Hilbert 90|Hilbert ninety|period-156|period 156|finite-field|finite field|additive identity|divisor identity" \
  incoming/extracted/s00209-008-0456-9.pdf.extract.txt
```

Observed:

- `507`, `Norm_156`, `Y_507`, `U_chi`, `V_bal`, `chi_39`, `chi_3`,
  `chi_13`, `C_3`, and `C_169` had no mathematical hits. The only `156` hit
  was a page/header artifact.
- `N = 39`, `level 39`, `X1(39)`, and related exact conductor-39 labels had no
  direct source-text hits. The conductor-39 object remains a derived
  specialization of generic Theorem 6.2, not a named p25 theorem in the paper.
- `Hilbert-90`, `period 156`, `finite-field`, `additive identity`, and
  `divisor identity` had no direct hits.
- Theorem 6.2 gives a sufficient condition for a generic product of
  `g(t/N,0)(N tau)` to lie in `K(X1(N))`, with an order formula. This supports
  source legality, not finite value/divisor closure.
- Theorem 9.8 gives a ray-class invariant generator. This supports class-field
  context, not an exact H0 or mixed conductor-39 source-stage theorem.

## Verdict

Koo-Shin 2010 remains positive source-legality evidence and negative
source-closer evidence.

H0:

```text
decision = continue_lane_but_kill_koo_shin_2010_as_closer
reason   = no exact H0 finite divisor/additive theorem with Hilbert-90 boundary
ask      = exact legal H0/H0-translate product + arithmetic source theorem
           + divisor/additive output + H90 boundary to Norm_156(Y_507)
```

Conductor 39:

```text
decision = continue_lane_but_kill_koo_shin_2010_as_closer
reason   = no mixed U_chi/W finite divisor/additive theorem preserving
           chi_3 tensor chi_13 plus Yang lift/descent
ask      = mixed conductor-39 U_chi/W object + non-projection tensor structure
           + Yang lift + descent/H90 boundary + finite divisor/additive theorem
```

## Recommendation

Do not reread Koo-Shin 2010 broadly for p25 closure. Use it as a source
certificate and ask the next source/literature/expert question in the narrow
forms above.
