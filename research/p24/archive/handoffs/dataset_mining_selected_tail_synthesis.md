# Dataset Mining For The Selected-Tail Target

Date: 2026-06-06

This note records what the local DANGER3/upstream and small-CM datasets say
after the selected-leading correction.  The data is useful for theorem
selection, not as a p24 computation.

## Sources Worth Mining

The local upstream DANGER3 data is already available under:

```text
p24/upstream_DANGER3/
```

with smaller-prime rows in:

```text
pp10.txt
pp12.txt.gz
pp16A.txt.gz
pp20.txt
pp24.txt.gz
```

The cheap p24 theorem microscopes that remain relevant are:

```text
p24/trace_frame_prefix_intersection_audit.py
p24/trace_frame_residual_tail_audit.py
p24/trace_frame_beta_product_resultant_audit.py
p24/packetized_content_selected_prime_scan.py
p24/l1_axis_injectivity_scan.py
```

The corrected theorem target is recorded in:

```text
p24/trace_frame_selected_lead_failure_module.md
p24/trace_frame_selected_tail_resultant_theorem.md
```

## What The Cheap Runs Say

The p24 arithmetic facts are stable:

```text
p = 1000000000000000000000007
is_prime = True
sqrt_floor = 1000000000000
v2(p+1) = 3
```

The tensor trace-period decomposition is:

```text
ord_m(p)=5460
ord_n(p)=388430
tensor_factor_count_over_E=70
tensor_factor_degree_over_E=5549
C_degree_over_E=179
B_degree_over_C=31
trace_cosets_partition_factor_orbit=True
coordinate_count_over_E=537
selected_axis_rank_target=368
```

The factorized Schubert accounting gives the dimensions now used by the proof:

```text
axis_dim=368
prefix_target_dim=358
forced_intersection_dim=10
residual_tail_dim=10
```

It also confirms that explicit matrix listing is already below sqrt(p), but the
desired certificate is the smaller arithmetic p-unit surface:

```text
single_leading_all_H_packets_Fp_slots_over_sqrt=5.915320320000e-03
one_factor_all_H_packets_Fp_slots_over_sqrt=4.768283520000e-03
punit_surface_requires_arithmetic_theorem_not_matrix_entry_listing=1
```

The upstream cheap-character scan over `pp16A` gives only constant-factor
capture:

```text
feature=A-2 capture=0.748937 approx_lift=1.497874
feature=A+2 capture=0.748937 approx_lift=1.497874
feature=A2-4 capture=0.502126 approx_lift=1.004251
conclusion=cheap_fixed_character_labels_show_only_constant_capture_lifts
```

So the upstream data does not suggest a seedless statistical selector capable
of producing the p24 certificate.  It is useful mainly as a guardrail against
overclaiming from branch features.

The small-CM residual-tail audit remains aligned with the selected theorem:

```text
rows=4
residual_rows=4
proper_partial_tail_rows=2
full_tail_rank_rows=4
leading_tail_failures=0
trace_dual_mismatch_rows=0
tail_annihilator_degree_mismatch_rows=0
tail_annihilator_image_rank_mismatch_rows=0
proper_frobenius_invariant_residual_rows=0
proper_full_qsupport_rows=2
```

Interpretation: in proper partial-tail rows, the residual image is not
Frobenius/subfield-stable, but the selected normal-head projection still
separates it.  This supports the theorem:

```text
det(A_T(b_28(k_j))^(Q^i))_{0 <= i,j < 10} is a p-unit.
```

It does not support a shortcut of the form "the residual image is stable, so
the selected head coordinate is automatic."

The prefix-intersection audit gives one positive and one negative small row:

```text
component_full=1 intersection_minimal=1 prefix_max_rank=1
component_full=0 intersection_minimal=0 prefix_max_rank=1
```

This reinforces the factorized theorem shape: prefix directness and residual
tail separation are separate p-unit inputs, not interchangeable consequences.

## Theorem Candidates Still Alive

1. **Direct selected-tail operator p-unit.**

```text
M_tail,Omega =
  det(A_T(b_28(k_j))^(Q^i))_{0 <= i,j < 10}
  in O_E^*
```

This is currently the cleanest target because it proves `K_sel,Omega={0}`
directly.

2. **Full-image subspace resultant.**

```text
dim_E b_28(K_2,Omega)=10
and
Res_q(A_U,Omega, A_T) in O_E^*
```

This is equivalent to the direct target only with the full-image hypothesis.

3. **Crossed-product beta norm.**

Small rows show beta products are cyclic resultants, but the interpolants are
dense and semilinear.  The viable statement is a crossed/Frobenius reduced norm
p-unit, not an ordinary sparse `E[Y]` resultant.

4. **Packet-content/Hermitian hierarchy.**

Coordinate product nonvanishing can fail in small prime-`n` data; exact content
or Hermitian scalar p-units are safer certificate surfaces.

## Cheap Commands

These commands produced the evidence above without p24-scale enumeration:

```text
PYTHONDONTWRITEBYTECODE=1 python3 p24/p24_arithmetic_audit.py
PYTHONDONTWRITEBYTECODE=1 python3 p24/tensor_factor_trace_period_identity.py
PYTHONDONTWRITEBYTECODE=1 python3 p24/trace_frame_factorized_schubert_accounting.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/upstream_prefix_character_scan.py \
  --min-p 32768 --max-p 65536 --residue 7 --top 4
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_residual_tail_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --scan-origins --max-rows 4 \
  --target constant_plus_4 --target constant_plus_3
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_frame_prefix_intersection_audit.py \
  --only-D -10919 --min-h 1 --max-h 200 --max-n 200 --max-m 40 \
  --max-factor-degree 20 --max-extension-degree 8 \
  --max-tensor-factor-degree 12 --max-top-count 4 \
  --include-linear --only-m 12 --max-cases 1
```
