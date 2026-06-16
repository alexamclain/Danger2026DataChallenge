# Probability Lift Agent Follow-Up

This note records the reusable result from the sidecar probability/statistics
pass after the axis and Hermitian theorem targets had stabilized.

## Certificate-Relevant Routes

The sidecar identified four probability-shaped routes that can become
deterministic only after they are converted into exact nonvanishing data.

1. Axis Moore / relative K-normality:

```text
T_a restricted to W_axis is injective,
or the stronger full K-fiber family is independent.
```

Certificate lift:

```text
Moore determinant nonzero,
coefficient minor nonzero,
or packet Bezout/content identity.
```

Evidence files:

```text
p24/axis_probability_data_sidecar.md
p24/relative_k_normality_parent_theorem.md
p24/component_character_module_boundary.md
```

2. Hermitian axis lattice p-unit:

```text
Delta_axis in M^+ has p-unit norm,
equivalently every Hermitian trace-Gram determinant is nonzero.
```

Certificate lift:

```text
p does not divide Norm_{M^+/Q}(Delta_axis).
```

Evidence files:

```text
p24/hermitian_isotropy_probability_audit.md
p24/hermitian_trace_gram_axis_certificate.md
p24/hermitian_axis_packet_norm_theorem.md
```

3. Sliding-window product p-unit:

```text
Pi_axis,a = prod_beta det(P_0 X^(-beta) V_a) != 0.
```

Certificate lift:

```text
Pi_axis,a^2 is an origin-independent p-unit.
```

Evidence files:

```text
p24/axis_sliding_window_product_theorem.md
p24/axis_sliding_window_sequence_complexity.md
p24/exterior_character_support_boundary.md
```

4. Relative content / harmful dual-coset exclusion:

```text
gcd(f_a, J_0, ..., J_{m-1}) = 1
```

for every primitive relative packet.

Certificate lift:

```text
literal packet Bezout identity,
or a divisor/zero lemma with a representative of pole degree below the
harmful packet window.
```

Evidence files:

```text
p24/agent_socrates_relative_content_sidecar.md
p24/frobenius_packet_testing_barrier.md
p24/dual_coset_annihilator_lemma.md
```

## Statistical Boundary

The sidecar agrees with the main theorem boundary:

```text
probability is useful only after it becomes a pointwise selected-prime
anti-concentration theorem or p-unit theorem.
```

Chebotarev, average equidistribution, random matrix heuristics, and
Schwartz-Zippel style tests explain why failures are unlikely, but they do
not certify the fixed prime `p=10^24+7`.

The sub-minute follow-up test on `D=-10919` is recorded in:

```text
p24/axis_sliding_window_sequence_complexity.md
```

It supports the sliding-window product p-unit route while further weakening
the hope for low-recurrence compression.
