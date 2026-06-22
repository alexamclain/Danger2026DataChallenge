# P27 Label-2 Cyclic-Quartic Component Check

Date: 2026-06-21

## Claim

Online Magma validates the main geometric warning for the label-2/H90 route:
the eliminated cyclic-quartic model has a genus-17 main component.  The raw
projective model is not irreducible, so the correct small-field workflow is:

```text
projective closure -> reduced subscheme -> irreducible components -> genus
```

This does not kill the order-4/H90 lane, because the possible win is now the
`alpha` quotient/Prym decomposition of that genus-17 component.  It does kill
the softer hope that the eliminated cyclic-quartic model itself is secretly
low genus before quotienting.

## Artifact

Magma fixture:

```text
research/p27/archive/fixtures/p27_label2_cyclic_components_q1471_magma.m
```

Online outputs:

```text
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q607_magma_20260621.txt
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1471_magma_20260621.txt
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1607_magma_20260621.txt
```

Raw calculator responses:

```text
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q607_magma_20260621.html
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1471_magma_20260621.html
research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1607_magma_20260621.html
```

## Model

Use the residual elliptic curve and eliminated cyclic-quartic equation:

```text
E: W^2 = X^3 - X
T2 = X*(X^2 + 1)*(X^2 + 2X - 1)
mt = (X + 1)*(2WX + X^3 + X^2 - X - 1)
m0 = (X^2 + 1)*(X^2 + 2X - 1)*(WX + W + 2X^2)
Salpha = W*(X + 1) + 2X^2
```

The eliminated equation, after clearing the denominator in
`pref = W*(X^2+1)/X`, is:

```text
X^2*R^4
- 2*X*W*(X^2 + 1)*m0*R^2
+ 4*W^2*(X^2 + 1)^2*T2*Salpha^2 = 0.
```

## Online Magma Results

For `q=607`:

```text
RESULT p27_label2_cyclic_components_q607 2 true false
COMP 1 1 30 17 888
COMP 2 1 1 0 608
```

For `q=1471`:

```text
RESULT p27_label2_cyclic_components_q1471 2 true false
COMP 1 1 30 17 1656
COMP 2 1 1 0 1472
```

For `q=1607`, a p27-signature field with `q = 7 mod 16`:

```text
RESULT p27_label2_cyclic_components_q1607 2 true false
COMP 1 1 30 17 1608
COMP 2 1 1 0 1608
```

Interpretation:

```text
component 1 = degree-30 genus-17 main component
component 2 = degree-1 genus-0 projection / denominator artifact
```

The q=607 and q=1471 checks are retained as historical sanity checks.  The
q=1607 rerun is the promotion-field check after the guard-field signature
audit, because it matches p27's `q = 7 mod 16` 2-adic sign regime.

## Consequence

The second-gate cover should now be treated as genuinely genus 17 before the
order-4 quotient.  The next possible sqrt-beating test is narrower:

```text
compute D/<alpha>
extract alpha-equivariant Prym/Jacobian factors
derive an explicit cyclic-quartic character over E
test whether that character recurs or couples to d3/d4
```

Do not spend more effort asking whether the raw eliminated cyclic-quartic
model is low genus.  It is not, after reduction/decomposition including the
q1607 p27-signature field.

## Continue / Kill

```text
continue = Magma/Sage alpha quotient on the genus-17 component
continue = Prym/Jacobian decomposition respecting alpha
continue = explicit cyclic-quartic character over E, if quotient coordinates emerge

kill = treating compactD=-1 or the raw genus-17 component as a source
kill = direct genus check of the unreduced/projected model without component split
kill = GPU production use of compactD unless quotient or telemetry changes the rate
```

## Linked Artifacts

- H90 parent: [P27 Label-2 H90 / Order-4 Lift](p27_label2_h90_order4_lift_20260621.md)
- Genus parent: [P27 Label-2 Cover Genus And Recurrence Probe](p27_label2_cover_genus_recurrence_20260621.md)
- Fixture: `research/p27/archive/fixtures/p27_label2_cyclic_components_q1471_magma.m`
- Fixture: `research/p27/archive/fixtures/p27_label2_cyclic_components_q1607_magma.m`
- Output: `research/p27/archive/probe_outputs/p27_label2_cyclic_components_q607_magma_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1471_magma_20260621.txt`
- Output: `research/p27/archive/probe_outputs/p27_label2_cyclic_components_q1607_magma_20260621.txt`

```text
p27_label2_cyclic_components_magma_rows=3/3
```
