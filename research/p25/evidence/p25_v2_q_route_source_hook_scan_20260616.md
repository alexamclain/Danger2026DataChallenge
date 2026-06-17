# P25 v2 Q Route Source Hook Scan

Updated: 2026-06-16

## Purpose

Apply the sharpened conductor-39 `Q` route to the local source corpus. This is
not a broad reread. It asks whether any source text in hand contains the exact
hooks now required for `Q` to help the p25 theorem front:

```text
Q = prod_{h in <2>} E_{7h}/E_h
Q^3 or Q^6 finite Hilbert-90 theorem data
Q diagonal plus pure quartic split
oriented root/sign or direct one-edge theorem
Norm_156(Y_507) / period-156 branch data
```

It also records false friends: generic `Q` in KSY means a quadratic form/CM
point, and generic splitting language in Sprang is not the p25 `Q` diagonal
split.

## Sources Read

- `incoming/extracted/s00209-008-0456-9.pdf.extract.txt`
- `incoming/extracted/1007.2307/ray_class_fields.tex`
- `incoming/extracted/1007.2318v1.pdf.extract.txt`
- `incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex`
- `incoming/extracted/sprang_1802_04996/deRhamRealization.tex`

## Pages Read

- `frontier.md`
- `lanes/conductor39.md`
- `evidence/p25_v2_q_route_selector_debt_20260616.md`
- `evidence/p25_v2_q_diagonal_normalization_20260616.md`
- `evidence/p25_v2_q_split_quartic_selector_20260616.md`
- `evidence/p25_v2_q_square_payload_router_20260616.md`
- `evidence/p25_v2_q_square_extraction_boundary_20260616.md`
- `evidence/p25_v2_constructive_payload_source_scan_20260616.md`
- `evidence/p25_v2_minimal_expert_ask_20260616.md`

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/archive/gates/p25_v2_q_route_source_hook_scan_gate.py
```

The gate returned `p25_v2_q_route_source_hook_scan_rows=1/1`.

## Source Rows

```text
koo_shin_2010_mathz
  helper_terms = Theorem 5.2, Theorem 6.2, product of Siegel functions,
                 distribution relation
  q_route_terms = none
  decision = no_q_route_hook_in_koo_shin_2010
  missing  = E_7/E_1 orbit norm, Q^3/Q^6 finite theorem, Q diagonal split,
             Norm_156(Y_507), or period-156 branch data

ksy_1007_2307_normalized_y
  helper_terms = ray class, Siegel, Klein forms, y_(0,1/N)
  q_route_terms = none
  collision_terms = Q=aX^2, theta_Q, beta_Q
  decision = q_symbol_collision_not_conductor39_q
  falsifier = local Q denotes a quadratic form/CM point, not the conductor-39
              quotient product

koo_shin_ii_1007_2318
  helper_terms = normal basis, ray class, Siegel, generator
  q_route_terms = none
  collision_terms = quadratic-form Q / theta_Q / beta_Q context
  decision = background_no_q_route_hook
  missing  = conductor-39 Q theorem or diagonal split/root data

sprang_1801_05677
  helper_terms = Kronecker theta, p-adic theta, distribution relation,
                 Kato-Siegel
  q_route_terms = none
  collision_terms = theta/distribution support vocabulary
  decision = theta_support_no_q_route_hook
  missing  = Q diagonal, quartic split, or period-156 row theorem

sprang_1802_04996
  helper_terms = de Rham, polylogarithm, Kronecker section, Kato-Siegel
  q_route_terms = none
  collision_terms = splitting, split, diagonal
  decision = split_word_collision_not_q_diagonal_split
  falsifier = generic splitting/diagonal language is not the Q diagonal plus
              pure quartic split
```

## Q Route Terms Screened

```text
E_7/E_1
E_{7h} / E_{7h}/E_h
7<2> / <2>
U_chi / V_bal
chi_39 / chi_3 / chi_13
Q^3 / Q^6
Q_antisym
m1+m4 / m1-m4 / m2+m8 / m2-m8
quartic split / pure quartic
Norm_156 / Y_507
period-156 / support-period-156
X_1(39) / Gamma_1(39)
```

## Counts

```text
raw_sources_available = 1
source_rows = 5
helper_rows = 5
q_route_term_rows = 0
collision_rows = 4
accepted_source_hook_rows = 0
source_stage_closers = 0
current_submission_ready = 0
```

## Verdict

```text
positive_artifact = local Q-route source-hook falsifier
continue_conductor39 = yes, but not through local Q-source language as written
accepted_future_hook = Q value/H90 theorem with period-156 data plus diagonal
                       split/root, or direct one-edge theorem
discard_condition = source lead only contains generic Q, generic split,
                    theta/distribution vocabulary, ray-class generation, or
                    source legality without conductor-39 Q route data
```

The local sources still support the surrounding vocabulary, but none currently
emits the conductor-39 `Q` route theorem data. The expert/literature ask should
therefore remain exact: `Q` diagonal plus pure quartic split plus oriented
root/sign, or a direct one-edge finite value/divisor theorem.
