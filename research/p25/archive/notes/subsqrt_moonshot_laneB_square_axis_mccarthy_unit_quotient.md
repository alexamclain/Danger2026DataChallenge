# Subsqrt Moonshot Lane B McCarthy Unit Quotient

Date: 2026-06-13

## Result

McCarthy's dense theorem cancellation has a sparse multiplicative quotient
form, but the exceptional value is not a direct character-valued p25 unit
phase.

Define:

```text
R(q) = LHS(q) / main_sum(q)
```

using the same McCarthy Theorem 1.7 specialization over `F_2029`:

```text
A_0 = omega^(4*138)
A_1 = 1
A_2(q) = omega^(4*q)
x = 2
```

The transformed main sum is nonzero for every `q in C_507`, and:

```text
support(R(q)-1) = (138,)
outer S image = (138,310,482)
```

So the theorem-level cancellation can be read multiplicatively as a point
quotient.

The coefficient debt is the obstruction:

```text
R(138) = 1790844 in F_20574061
R(138)-1 = 1790843
ord(R(138)) = 79131 = 39 * 2029
ord(R(138)-1) = 20574060
R(138) not in mu_507
R(138) not in mu_2028
ord(R(138)^39) = 2029
ord(R(138)^2029) = 39
```

Thus the sparse quotient carries a nontrivial additive-root component from the
auxiliary value field.  It is not a direct finite-character phase.

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_unit_quotient_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_unit_quotient_gate.py
```

Observed:

```text
main_zero_count = 0
quotient_minus_one_support = (138,)
quotient_target_order = 79131
quotient_minus_one_order = 20574060
quotient_in_507_roots = False
quotient_in_character_roots = False
quotient_has_additive_component = True
square_axis_mccarthy_unit_quotient_rows=1/1
```

## Consequence

This is the best current McCarthy/Barnes formulation:

```text
positive:
  theorem cancellation has a sparse unit-quotient shape.

negative:
  the exceptional quotient is not in the multiplicative character-root group.
  it has a 2029 additive-root component.
  R(138)-1 has full auxiliary-field multiplicative order.
```

Continue only if a further identity cancels the `2029` component, explains why
this auxiliary-field quotient descends to the p25 raw-Y coefficient field, or
replaces `R(q)` with an equivalent character-valued unit quotient.

Discard condition:

```text
candidate treats R(138) as a C_507/C_2028 character value
candidate ignores the additive-root component
candidate scales R(q)-1 by an arbitrary auxiliary-field scalar before raw lift
```
