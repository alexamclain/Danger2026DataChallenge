# Fixed-Frequency Actual-CM Right-Combo Boundary

Date: 2026-06-06

## Point

The class-character expansion leaves a tempting stronger theorem:

```text
R_{chi,-a} = sum_v chi(v) T_{0,v,-a} = 0
for every relative packet character a.
```

This would imply the required packet product sum vanishes term by term.

## Boundary

The pinned actual-CM analogue

```text
D=-13319, q=13463, h=140, m=28=4*7, n=5
```

has a nontrivial right quotient character on the right component `7`.  In this
row all primitive relative right-combos are nonzero, and the packet projection
itself is nonzero.  Therefore termwise right-combo vanishing is not a generic
CM-packet identity.

This does not disprove the p24 theorem.  It says the p24 proof should target
the exact packet cancellation

```text
sum_a T_{1,0,a} R_{chi,-a} = 0
```

or else exhibit a genuinely p24-specific extra structure that is absent in the
pinned analogue.

## Check

The boundary is:

```text
p24/trace_gcd_fixed_frequency_actual_cm_right_combo_boundary.py
```

It verifies:

```text
left packet traces nonzero:              4/4
right multiplicative packet combos:      4/4 nonzero
product terms:                           4/4 nonzero
packet projection:                       nonzero
right-neutral control combos:            zero
```
