# P25 v2 Koo-Shin II First-Pass Source Scan

Updated: 2026-06-16 07:31 PDT

## Purpose

Screen the locally available Koo-Shin sequel extract, `1007.2318`, against the
current v2 first-pass theorem asks. The goal was not to reread the paper
broadly, but to decide whether it can supply either the H0 closer or the mixed
conductor-39 closer that Koo-Shin 2010 did not supply.

## Pages Read

- `frontier.md`
- `sources/koo-shin-ii-1007-2318.md`
- `sources/koo-shin-2010.md`
- `lanes/h0.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_h0_conductor39_canonical_frontier_pass_20260616.md`

## Probes

Source text used in the private live-run incoming layer:

```text
incoming/extracted/1007.2318v1.pdf.extract.txt
```

Commands:

```bash
rg -n -i "Hilbert|period.?156|Norm.?156|Y_?507|level.?507|507" \
  incoming/extracted/1007.2318v1.pdf.extract.txt

rg -n -i "divisor|additive|distribution|finite.?field|value theorem|evaluate|evaluation" \
  incoming/extracted/1007.2318v1.pdf.extract.txt

rg -n "507|156|Norm_156|Y_507|U_chi|V_bal|chi_39|chi_3|chi_13|C_3|C_169|H0|H_0" \
  incoming/extracted/1007.2318v1.pdf.extract.txt

rg -n "N = 39|N=39|level 39|/Gamma11\\(39\\)|X1\\(39\\)|39\\)" \
  incoming/extracted/1007.2318v1.pdf.extract.txt

rg -n -i "Hilbert-90|Hilbert 90|period-156|period 156|finite-field|finite field|additive identity|divisor identity|source theorem|ray class|Siegel|Kubert|Lang|Theorem|Corollary" \
  incoming/extracted/1007.2318v1.pdf.extract.txt
```

Observed:

- `507`, `Norm_156`, `Y_507`, `U_chi`, `V_bal`, `chi_39`, `chi_3`,
  `chi_13`, `C_3`, `C_169`, `H0`, and `H_0` had no mathematical hits. The
  only `156` hit was part of a large polynomial coefficient, not a period.
- `N = 39`, `level 39`, `X1(39)`, and related conductor-39 labels had no hits.
- `Hilbert-90`, `period 156`, `finite-field`, `additive identity`, and
  `divisor identity` had no hits.
- The positive material is ray-class/Siegel-function context: ring class
  invariants, normal bases, and algebraic integer generators.

## Verdict

Koo-Shin II `1007.2318` is background context, not a first-pass p25 closer.

H0:

```text
decision = kill_koo_shin_ii_as_h0_closer
reason   = no exact H0 product, no period-156/H90 boundary, no finite
           divisor/additive theorem
```

Conductor 39:

```text
decision = kill_koo_shin_ii_as_conductor39_closer
reason   = no mixed U_chi/W object, no chi_3 tensor chi_13 structure, no
           Yang-lift/descent finite theorem
```

## Recommendation

Do not use `1007.2318` as a front-door H0 or conductor-39 source. Keep it as
citation-chain and ray-class/Siegel context only. The next source/literature
ask should remain the narrow H0 or mixed conductor-39 theorem shape, not a
general Koo-Shin sequel reread.
