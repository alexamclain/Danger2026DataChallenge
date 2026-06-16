# P25 KSY-y Sprang Even-D Specialization Contract

Updated: 2026-06-13 22:39 PDT

## Purpose

Koo-Shin remains blocked on full-text retrieval, so the priority-1 divisor lane
falls back to the open Sprang/Kronecker source family.  This note records the
current exact boundary: Sprang gives a real even-`D` surface, but the available
clauses do not yet instantiate the p25 mixed `C/D/K` product or theta2 payload.

Target product:

```text
P = prod_{j=-1..1} prod_{k=0..24} y(C+jD+kK)/y(-C-jD-kK)
C = (47,28), D = (22,3), K = (57,0)
```

## Source Rows

```text
Sprang 1801 even-D omega surface
  source = https://arxiv.org/abs/1801.05677
  local = /tmp/p25_lit_scout/1801.05677/PaperEisensteinPoincare.tex:771-777,1019-1027
  positive = omega^D / Kronecker-section construction does not require 6
             coprime to D; when D is coprime to 6 it agrees with dlog theta_D
  missing = exact p25 P or theta2/theta2^-1 divisor data
  verdict = conditional_even_d_surface_not_exact_product

Sprang 1801 Kronecker distribution
  source = https://arxiv.org/abs/1801.05677
  local = /tmp/p25_lit_scout/1801.05677/PaperEisensteinPoincare.tex:1714-1798
  positive = general Kronecker-section distribution over isogeny kernels and
             D-torsion translations
  missing = specialization selecting C=(47,28), D=(22,3), K=(57,0), equal
            weights, orientation, and mixed graph
  verdict = conditional_distribution_not_p25_mixed_graph

Sprang 1802 Kato-Siegel comparison
  source = https://arxiv.org/abs/1802.04996
  local = /tmp/p25_lit_scout/1802.04996/deRhamRealization.tex:1105-1182
  positive = D-variant and distribution relation persist
  blocker = comparison with Kato-Siegel theta_D is stated for D prime to 6
  verdict = reject_direct_theta_d2_import_keep_even_d_variant

Sprang 1802 de Rham Eisenstein formula
  source = https://arxiv.org/abs/1802.04996
  local = /tmp/p25_lit_scout/1802.04996/deRhamRealization.tex:1627-1711
  positive = differential/cohomology formula using Kato Eisenstein series
  missing = finite multiplicative normalized-y product or period-156 value
            identity
  verdict = reject_cohomology_formula_as_direct_product
```

## Completed Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_sprang_even_d_specialization_contract_gate.py
```

```text
source_evidence_rows        = 4
even_d_surface_rows         = 1
distribution_rows           = 1
prime_to_6_blocked_rows     = 1
cohomology_output_rows      = 1
direct_closing_rows         = 0
conditional_rows            = 2
rejected_rows               = 2
hypothetical_closing_rows   = 1
all_rows_have_missing_clause = 1
```

Marker:

```text
ksy_y_sprang_even_d_specialization_contract_rows=1/1
```

## Verdict

Sprang is not killed.  The even-`D` Kronecker-section lane remains the best
open fallback to Koo-Shin for a divisor/additive theorem.  But the current
source clauses only give the surface: additive distribution, D-variant
Kronecker sections, and de Rham Eisenstein/cohomology formulas.  A closing
Sprang hit must still emit exact p25 `P`, exact theta2/theta2-inverse divisor
data, or the compact `C=(47,28), D=(22,3), K=(57,0)` theorem payload with
orientation.
