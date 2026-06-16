# Trace-GCD Low-Moment Truncated-Polynomial Gate

Date: 2026-06-07

The low-moment selector can be stated in a more class-field-facing way.
By Newton identities, the first `k` child power sums are equivalent to the
first `k` elementary symmetric coefficients of the child polynomial, because
the p24 characteristic is much larger than `26`.

Since the first elementary coefficient is the child sum, it is already the
parent period:

```text
e_1 = P_1 = parent.
```

Thus the producer target can be phrased as a truncated selected child
polynomial:

```text
first layer:  e_2, e_3, e_4      = 3 new coefficients
second layer: e_2, ..., e_26     = 25 new coefficients
selected path total              = 28 new coefficients
```

Script:

```text
p24/trace_gcd_low_moment_truncated_polynomial_gate.py
```

Lean gate:

```text
p24/lean/TraceGcdLowMomentTruncatedPolynomialGate.lean
```

Run:

```text
PYTHONPYCACHEPREFIX=/private/tmp/codex-pycache PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=p24 python3 p24/trace_gcd_low_moment_truncated_polynomial_gate.py

lean p24/lean/TraceGcdLowMomentTruncatedPolynomialGate.lean
```

Output summary:

```text
random_control=F_101_20_choose_10:
  newton_match=1
  power_matches=1
  elementary_matches=1

actual_cm_controls:
  D=-200:   newton_match=1, power_matches=1, elementary_matches=1
  D=-239:   newton_match=1, power_matches=1, elementary_matches=1
  D=-5000:  newton_match=1, power_matches=1, elementary_matches=1
```

Interpretation:

```text
low_power_sums_equivalent_to_truncated_child_polynomial_by_newton=1
first_coefficient_e1_is_the_parent_period=1
p24_low_moment_producer_can_target_28_new_child_polynomial_coefficients=1
selector_still_uses_30_constraints_including_parent_e1=1
```

This does not construct the coefficients.  It changes the construction target
from "28 higher relative traces" to the equivalent and more algebraic
"28 next coefficients of the selected child polynomials."
