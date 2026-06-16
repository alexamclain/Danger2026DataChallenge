# Subsqrt Moonshot Lane B McCarthy Power Cost Ledger

Date: 2026-06-13

## Result

The powered McCarthy quotient route is not killed by sub-sqrt size accounting.

The remaining arithmetic object is:

```text
(R(q)^2029 - 1) / (zeta_39^5 - 1)
```

where the coefficient normalization is already determined in `F_2029` by:

```text
(zeta_39^5 - 1)^-1 = 636
```

The conservative finite-payload cost ledger is:

```text
p = 10^25 + 13
sqrt_floor = 3162277660168
power exponent = 2029
binary exponentiation multiplications = 18

2029 * S-trace support          = 6087
2029 * quotient packet support  = 511308
2029 * dense C_507 twist space  = 1028703
2029 * raw-Y support            = 12782700
2029 * full raw order           = 25717575
```

The worst deliberately pessimistic bound is:

```text
25717575 < sqrt_floor
sqrt_floor // 25717575 = 122961
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_power_cost_ledger_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_power_cost_ledger_gate.py
```

Observed:

```text
finite_cost_below_sqrt = True
binary_power_tiny = True
scalar_normalization_determined = True
remaining_debt_is_arithmetic_not_size = True
square_axis_mccarthy_power_cost_ledger_rows=1/1
```

## Consequence

The powered McCarthy/Barnes route now has:

```text
finite support alignment: done
theorem-level numeric McCarthy delta: done
sparse multiplicative quotient: done
power descent to order 39: done
coefficient-field transport to F_2029: done
raw-Y closure after determined normalization: done
sub-sqrt cost accounting: done
```

The remaining debt is sharply stated:

```text
prove that the powered quotient R^2029, with normalization
(zeta_39^5 - 1)^-1, is a legitimate arithmetic producer before raw lift.
```

Continue condition:

```text
find a theorem-level Barnes/McCarthy/Hasse-Davenport/Gross-Koblitz identity
that produces the powered normalized quotient directly or justifies taking
the 2029th power as a bounded-cost unit operation
```

Discard condition:

```text
candidate requires dense enumeration beyond the conservative 2029*raw_order
candidate treats the normalization as arbitrary rather than determined
candidate cannot preserve singleton support under the power operation
```
