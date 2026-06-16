# Subsqrt Moonshot Lane B McCarthy Well-Poised Numeric Delta

Date: 2026-06-13

## Result

The McCarthy point-delta route now has a theorem-level finite-field numeric
check, not only a support contract.

Using McCarthy, *Transformations of Well-Poised Hypergeometric Functions over
Finite Fields*, Theorem 1.7:

```text
field: F_2029
character group order: 2028 = 4 * 507
auxiliary value field: F_20574061, where 20574061 = 5 * 2029 * 2028 + 1
n = 2
x = 2
A_1 = trivial
A_0 = omega^(4 * 138)
A_2(q_exp) = omega^(4 * q_exp), q_exp in C_507
```

The exceptional term is controlled by:

```text
delta(bar(A_0) * A_1 * A_2(q_exp))
```

so it should fire only at `q_exp=138`.  The numeric check evaluates
McCarthy's normalized finite-field hypergeometric functions and verifies:

```text
support_qexp(LHS - main_sum) = (138,)
support_qexp(exceptional_term) = (138,)
LHS - main_sum = exceptional_term for all 507 q_exp values
lower 1F0 factor at x=2 is 1
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_well_poised_numeric_delta_gate.py
```

Observed:

```text
delta_support = (138,)
transformed_difference_support = (138,)
exceptional_support = (138,)
theorem_mismatch_count = 0
square_axis_mccarthy_well_poised_numeric_delta_rows=1/1
```

## Consequence

This is the strongest Jacobi/Barnes-side positive artifact so far.  McCarthy's
well-poised exceptional term is a genuine finite-field point-delta producer for
the exact `q=138` anomaly seed before orbit closure.

This still is not a p25 certificate.  The next step is to map this point delta
into the p25 square-axis payload:

```text
q=138 -> outer S image {138,310,482}
then into the raw-Y / bridge harness with the deterministic C13 fiber background
```

Discard condition for the next step:

```text
the McCarthy parameter normalization introduces a dense scalar background
the point delta cannot be aligned with the p25 theta_3_1/raw-Y packet
the raw lift fails kernel-triviality, raw D^3=Y, or source graph constraints
```
