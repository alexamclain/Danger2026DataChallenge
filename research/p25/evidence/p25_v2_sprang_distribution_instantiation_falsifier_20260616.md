# P25 v2 Sprang Distribution Instantiation Falsifier

Updated: 2026-06-16

## Purpose

Test the tempting upgrade after the Sprang theta2 intake: maybe Sprang's
general distribution relation already instantiates the accepted p25
theta2/theta2-inverse finite payload. This pass keeps the answer narrow.

## Sources Read

- `incoming/extracted/sprang_1801_05677/PaperEisensteinPoincare.tex`
- `evidence/p25_v2_theta2_period156_support_contract_20260616.md`
- `archive/gates/p25_laneB_robert_ksy_theta2_arithmetic_producer_contract_gate.py`

The gate falls back to the arXiv `1801.05677` e-print if the local extract is
absent.

## Command

```bash
PYTHONDONTWRITEBYTECODE=1 \
  python3 research/p25/archive/gates/p25_v2_sprang_distribution_instantiation_falsifier_gate.py
```

The gate returned
`p25_v2_sprang_distribution_instantiation_falsifier_rows=1/1`.

## Positive Support

Sprang's distribution theorem is real and useful support:

```text
distribution_theorem_present = yes
full_kernel_torsion_sum_present = yes
full_d_torsion_corollary_present = yes
d_not_coprime_to_6_support = yes
```

The relevant Sprang shape is a full trace/distribution identity over
`alpha in ker(psi)` and `beta in E'^vee[D']`, plus the full `D`-torsion
corollary for the Kronecker section.

## Falsifier

The accepted p25 theta2 finite interface is not a full torsion trace. It is one
of these sparse outputs:

```text
source_factor_tuple = base*K_trace*D_segment*(1-T)
sparse_theta2_divisor
sparse_theta2_inverse_divisor
compact_ksy_theta2
```

The Sprang source does not name or select:

```text
source_names_sparse_factor_tuple = no
source_names_p25_bridge = no
source_names_compact_ksy_payload = no
direct_instantiation_closers = 0
```

So the distribution relation is not, by itself, the missing arithmetic
producer. A proof would still have to specialize Sprang's full trace language
down to the p25 sparse quotient packet or factor tuple, with the exact
orientation/branch data.

## Verdict

```text
decision = sprang_distribution_is_full_trace_support_not_sparse_theta2_instantiation
continue = only with a specialization selecting base, K_trace, D_segment,
           T edge, theta2/theta2^-1 direction, and p25 branch/orientation
kill = citing Sprang's full distribution relation as the p25 theta2 theorem
       without the sparse selector
p25_v2_sprang_distribution_instantiation_falsifier_rows=1/1
```
