# P25 KSY-y Conductor-39 Source-Theorem Intake

Updated: 2026-06-14 11:00 PDT

## Purpose

After the Yang distribution-lift checkpoint, the first theorem target is:

```text
U_chi = -chi_3 * chi_13 on X_1(39)
Norm_156(Y_507) = distribution_lift_39_to_507(6 * U_chi)
```

This intake classifies future theorem/literature hits against that target.

## Accepted Shape

A conductor-`39` theorem hit must provide all of:

```text
verified theorem/proof body
legal source object U_chi, V_bal, W, the coset quotient 7<2>/<2>, the
12-step doubling-orbit norm of E_7/E_1, or a legal mixed sparse Hilbert-90
gauge on X_1(39)
full 12-step orbit if using the seed ratio; proper suborbits fail Yang/Yu legality
if using a sparse Hilbert-90 gauge, it must be one of the four legal mixed
support-12 gauges, not the all-positive/all-negative one-coset formal gauges
equivalently, sparse legal gauges are anti-invariant sign selectors on the
four Frobenius-orbit quotient and have zero mod-3 and mod-13 pushforwards
after Yang lift, a legal sparse gauge may be used as a support-156 level-507
Hilbert-90 potential H_s with (1-Frob_p)H_s = Norm_156(Y_507); one-coset
formal lifts are rejected despite having the same boundary
mixed tensor structure chi_3 tensor chi_13
Yang/Yu modular-unit legality
13-fiber Yang distribution to X_1(507)
coset Frobenius pairing, if using the compact quotient Q: Frob_p(Q)=Q^-1
Frobenius/Hilbert-90 descent, twisted trace, ratio, or equivalent boundary
finite-field value identity or divisor/additive theorem
```

For a value theorem, it must also include:

```text
period-156 branch/root/telescoping context
```

Then it still needs:

```text
DANGER3 finite-identity/non-CM framing
extraction algorithm for concrete (A, x0)
official vpp.py verification
```

## Regression Decisions

```text
snippet_only                         -> reject_no_theorem_body
prime13_projection_product           -> reject_loses_mixed_tensor
sparse_one_coset_standalone          -> reject_formal_sparse_gauge_without_boundary
mixed_unit_without_yang_lift         -> conditional_missing_yang_distribution_lift
mixed_unit_yang_without_descent      -> conditional_missing_frobenius_or_hilbert90_descent
mixed_unit_yang_descent_no_value     -> conductor39_source_identified_value_or_divisor_theorem_missing
finite_value_without_period156       -> conditional_missing_period_156_context
divisor_theorem_policy_missing       -> source_theorem_closed_policy_or_framing_missing
divisor_theorem_extraction_missing   -> danger3_unblocked_extraction_missing
divisor_theorem_ready_to_verify      -> ready_to_extract_and_verify_concrete_triple
submission_ready_control             -> submission_ready_verified_triple
```

## Counts

```text
conductor39_source_identified_rows = 8
theorem_source_closed_rows         = 4
danger3_unblocked_rows             = 3
extraction_ready_rows              = 2
submission_ready_rows              = 1
rejected_rows                      = 3
conditional_rows                   = 3
helper_only_rows                   = 1
```

## Local Gate

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py
```

Candidate classifier:

```sh
PYTHONPATH=research/p25 PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_ksy_y_conductor39_source_theorem_intake_gate.py \
  --candidate --name example --theorem-body --source-object U_chi \
  --emits-conductor39 --mixed-tensor --legal-unit --yang-lift \
  --descent --output-kind divisor-additive --finite-or-divisor
```

Expected marker:

```text
ksy_y_conductor39_source_theorem_intake_rows=1/1
```
