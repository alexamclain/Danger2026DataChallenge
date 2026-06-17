# P25 v2 KL Source-Split Local Scan

Updated: 2026-06-17

Marker: `p25_v2_kl_source_split_local_scan_rows=1/1`

## Purpose

Apply the new KL primitive-word source split to the local source extracts. The
scan is intentionally narrow: it looks for the exact six-term KL word,
three-term Hilbert-90 source chain, boundary-step language, or K-trace/theta2
bridge that would make the exact-P/KL route more than finite support.

## Pages Read

- `evidence/p25_v2_kl_primitive_word_source_split_20260617.md`
- `evidence/p25_v2_kubert_lang_selector_boundary_20260616.md`
- `evidence/p25_v2_exactp_theta2_lookup_row_status_20260617.md`
- `evidence/p25_v2_constructive_payload_source_scan_20260616.md`
- `sources/kubert-lang.md`
- `lanes/exact-p.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_kl_source_split_local_scan_gate.py
```

The gate returned `p25_v2_kl_source_split_local_scan_rows=1/1`.

## Source Rows

```text
ksy_1007_2307_normalized_y
  helper_terms = Siegel, ray class, normalized, wp, y-coordinate
  strong_hook_hits = none
  decision = helper_source_not_exact_kl_split_hook
  missing  = normalized-y/ray-class vocabulary but no exact KL primitive word,
             source chain, or K-trace/theta2 bridge

sprang_1801_poincare_kronecker
  helper_terms = theta, Kronecker, Eisenstein, Poincare, distribution
  strong_hook_hits = none
  decision = helper_source_not_exact_kl_split_hook
  missing  = D=2 theta/Kronecker support but no sparse p25 KL word or
             source-chain specialization

sprang_1802_derham
  helper_terms = theta, Kronecker, polylog, de Rham, Eisenstein
  strong_hook_hits = none
  decision = helper_source_not_exact_kl_split_hook
  missing  = de Rham/polylog support but no exact primitive word, boundary
             step, or K-trace/theta2 payload

koo_shin_2010_mathz
  helper_terms = Theorem 5.2, Theorem 6.2, Siegel, root of unity, distribution
  strong_hook_hits = none
  decision = helper_source_not_exact_kl_split_hook
  missing  = Siegel/distribution helper clauses but no exact KL source-split
             hook

koo_shin_ii_1007_2318
  helper_terms = ray class, Siegel, normal basis, Galois
  strong_hook_hits = none
  decision = helper_source_not_exact_kl_split_hook
  missing  = ray-class/Siegel context but no exact KL source-split hook
```

## Strong Terms Screened

```text
z^121, z^{121}, z^263, z^{263}
1-z^263, 1 - z^263
z^-121, z^{-121}
C_3 x C_169, C3 x C169
K_trace, K-trace
theta2, theta_2
boundary step
```

Generic `theta`, `Siegel`, `ray class`, distribution, Kronecker, or
normal-basis language was counted only as helper vocabulary.

## Counts

```text
raw_sources_available = 1
evidence_markers_ok = 4/4
exact_split_source_hooks = 0
helper_rows = 5
killed_as_exact_split_hooks = 5
current_kl_source_theorems = 0
current_exactp_source_theorems = 0
current_source_stage_closers = 0
p25_v2_kl_source_split_local_scan_rows=1/1
```

## Verdict

The new source split sharpens the exact-P/KL ask, but it is not hidden in the
local source extracts. KSY, Sprang, Koo-Shin 2010, and Koo-Shin II remain
helper/source-vocabulary layers unless a new citation or expert answer names
the exact oriented primitive word, or the three-term H90 source chain plus
unique boundary step, together with raw K-trace/theta2 period-156 bridge data.
