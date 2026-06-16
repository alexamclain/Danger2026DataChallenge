# Fixed-Frequency p24 Internal Trace Gaussian Functional Gate

Date: 2026-06-06

## Point

The codimension-one internal trace target can be written explicitly as a
Gaussian-period pairing.

For a relative packet polynomial:

```text
P(X)=sum_k c_k X^k,
```

and internal subgroup `<Q>` with `Q=p^5460 mod n`, the target is:

```text
sum_{r in <Q>} P(zeta_n^(a r)) = 0.
```

Equivalently:

```text
sum_k c_k * eta_{a k} = 0,
eta_t = sum_{r in <Q>} zeta_n^(t r).
```

So the next theorem is a weighted CM/Lang cancellation against the
degree-5549 Gaussian-period vector.

## Boundaries

This is not implied by relative augmentation/nonvanishing:

```text
Res(Phi_n, P) != 0
```

or by all primitive evaluations being nonzero.  The finite gate finds random
polynomials with all primitive evaluations nonzero and nonzero internal trace.

Conversely, internal trace zero does not imply packet vanishing; the gate
constructs polynomials with all primitive evaluations nonzero and trace zero.

So the target is exactly a weighted period cancellation, not a content theorem.

## Checked Gate

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/trace_gcd_fixed_frequency_p24_internal_trace_gaussian_functional_gate.py
```

Key output:

```text
orbit_trace_pairing_identity_failures=0
random_all_primitive_evals_nonzero_trace_nonzero=33/36
forced_trace_zero_and_all_primitive_evals_nonzero=36/36
p24_internal_q_generator=p^5460_mod_n=209035
p24_internal_degree=5549
p24_sample_gaussian_period_nonzeroes=8/8
nested_internal_trace_is_gaussian_period_pairing=1
augmentation_nonvanishing_does_not_imply_internal_trace_zero=1
internal_trace_zero_does_not_imply_packet_vanishing=1
p24_gaussian_period_weights_are_not_formally_zero=1
remaining_theorem_is_cm_lang_weighted_period_cancellation=1
```

