# Subsqrt Moonshot Lane B McCarthy q-Power Projection

Date: 2026-06-13

## Result

The `2029`th power in the powered McCarthy route is exactly the multiplicative
projection needed to remove the additive-root component, but it is not a field
Frobenius automorphism of the auxiliary value field.

The auxiliary value field is:

```text
F_20574061
20574061 - 1 = 5 * 2029 * 2028
```

The q-power map `x -> x^2029` on `F_20574061^*` has:

```text
kernel size = 2029
image size = 10140
```

On root groups:

```text
mu_2028 is fixed
mu_39 is fixed
mu_2029 is killed
mu_5 is sent to fourth power
```

For the McCarthy quotient target:

```text
R(138) = 1790844
ord(R(138)) = 39 * 2029
R(138) = zeta_39^5 * additive_root^1475
R(138)^2029 = zeta_39^5 = 12801419
ord(R(138)^2029) = 39
```

Control:

```text
q-power is multiplicative:
  (2*3)^2029 = 2^2029 * 3^2029

q-power is not additive:
  (2+3)^2029 = 18369750
  2^2029 + 3^2029 = 91572
```

Script:

```text
/Users/agent/Documents/Codex/pomerance-p25-run/research/p25/p25_laneB_square_axis_mccarthy_q_power_projection_gate.py
```

Command:

```sh
cd /Users/agent/Documents/Codex/pomerance-p25-run
PYTHONDONTWRITEBYTECODE=1 python3 \
  research/p25/p25_laneB_square_axis_mccarthy_q_power_projection_gate.py
```

Observed:

```text
quotient_character_exponent = 5
quotient_additive_exponent = 1475
quotient_reconstruction_ok = True
q_power_is_not_field_automorphism = True
q_power_is_character_projection_on_target = True
square_axis_mccarthy_q_power_projection_rows=1/1
```

## Consequence

This refines the remaining McCarthy/Barnes theorem target:

```text
wrong framing:
  apply a field Frobenius to a dense hypergeometric identity

right framing:
  first obtain a multiplicative unit quotient R(q)
  then apply the q-power projection on the quotient
  then use the determined coefficient normalization
```

The finite chain is now:

```text
R(q)-1 supported at q=138
R(138) = zeta_39^5 * additive_root^1475
R(q)^2029 - 1 supported at q=138
R(138)^2029 = zeta_39^5
transport to F_2029 and normalize by (zeta_39^5-1)^-1
raw-Y closure passes
```

The remaining debt is:

```text
justify that R(q) is an arithmetic unit quotient before q-power projection.
```

Discard condition:

```text
candidate relies on q-power as an additive/field-Frobenius operation
candidate applies q-power before producing a multiplicative quotient
candidate cannot separate the additive-root factor from the character-root
factor
```
