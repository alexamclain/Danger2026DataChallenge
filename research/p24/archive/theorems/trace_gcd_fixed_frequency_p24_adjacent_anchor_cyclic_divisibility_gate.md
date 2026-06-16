# p24 Adjacent-Anchor Cyclic-Divisibility Gate

Date: 2026-06-07

This note compresses the adjacent-anchor descent target one step further.

The adjacent-anchor descent gate asks for one anchor

```text
T_0
```

to be fixed by the order-7 `rho` action.  If the rho-orbit coordinates are
written as a degree `<7` cyclic polynomial

```text
A(y)=a_0+a_1 y+...+a_6 y^6,
```

then:

```text
rho(T_0)=T_0
  iff a_0=a_1=...=a_6
  iff A(y) is a scalar multiple of Phi_7(y)=1+y+...+y^6
  iff A(y) == 0 mod Phi_7(y).
```

So the six nontrivial rho-projectors are equivalent to one cyclic remainder
modulo `Phi_7`.

## Checks

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_fixed_frequency_p24_adjacent_anchor_cyclic_divisibility_gate.py
```

Expected summary:

```text
fixed_iff_phi7_divisible_rows=512/512
projectors_zero_iff_phi7_divisible_rows=512/512
random_phi7_divisible=0/512
random_projector_zero=0/512
forced_fixed_phi7_divisible_rows=512/512
forced_nonfixed_not_phi7_divisible_rows=512/512
p24_single_adjacent_anchor_projectors=6
p24_single_adjacent_anchor_cyclic_remainder_degree=6
single_anchor_descent_iff_phi7_divisibility=1
six_projectors_compress_to_one_cyclic_remainder_mod_phi7=1
adjacent_anchor_divisibility_is_finite_algebra_not_the_cm_lang_producer=1
```

Lean proof-contract scaffold:

```text
p24/lean/TraceGcdAdjacentAnchorCyclicDivisibilityGate.lean
```

## Interpretation

This does not construct the selected adjacent-trace anchor.  It sharpens the
remaining descent theorem to a single base-field cyclic identity:

```text
A(y) ≡ 0 mod Phi_7(y).
```

Together with pointwise covariance and telescoping, this proves the `48`
compressed right-difference equations.
