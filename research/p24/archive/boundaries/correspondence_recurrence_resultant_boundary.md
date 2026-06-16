# Correspondence Recurrence And Resultant Boundary

This note closes a tempting variant of the split-cycle route:

```text
Maybe a low-order recurrence, fast power, or seedless resultant of a split
modular correspondence constructs the recovery polynomial without explicitly
computing class-character traces.
```

The conclusion is negative for the natural formulation.  Compactly writing a
long correspondence does not lower its geometric degree or give the subgroup
projector.  It either leaves all branches present, or it requires the same
whole-subgroup aggregation that defines the period.

## Setup

Let a split prime ideal act on the CM torsor by a generator `g`.  A desired
quotient by

```text
H = <g^m>
```

has periods

```text
y_r = sum_{k=0}^{n-1} j_{r + m*k}.
```

A local modular recurrence, such as repeated `Phi_ell` edges, can represent
paths

```text
j_i -> j_{i+1} -> ... -> j_{i+m}.
```

But this path data is not fixed by `H`.  It is a long edge or chain starting
at `j_i`, and the class group still translates the starting point through the
full orbit.

## Degree Accounting

A seedless fixed point of an `ell^r` correspondence has `X0` degree roughly

```text
psi(ell^r) = ell^r + ell^(r-1).
```

So "close the cycle by a resultant" has degree exponential in the class-order
length of the cycle.  A straight-line or recursive representation may use only
`O(log r)` or `O(r)` equations, but eliminating the hidden branches or picking
one horizontal CM cycle still pays the same correspondence degree unless an
embedded CM invariant is supplied.

For the third p24 target, the seedless degree audit gives:

```text
ell=23 full generator cycle:
  order = 205880396014
  log10 psi(23^order) ~= 2.803531e11

ell=677 index-314 cycle:
  order = 655670051
  log10 psi(677^order) ~= 1.855932e9

best embedded split if quotient periods are known:
  quotient degree = 66254
  recovery degree = 3107441.
```

Even the absurd lower bound "some prime-level correspondence generates the
order-`3107441` subgroup with `ell >= 2`" gives

```text
log10 degree >= 9.354330e5,
```

far above the `sqrt(p)` scale.

The script is:

```text
p24/seedless_cycle_resultant_audit.py
```

## Toy Calibration

The `D=-5000`, `h=30`, `ell=3` toy has a complete embedded CM torsor.  It is
small enough to compare local path data with whole subgroup periods.

The script

```text
p24/power_level_stabilizer_toy.py
```

tests moves `2,3,5,6,10,15`.  For every meaningful move, endpoint and path
invariants retain essentially the full class orbit, while the quotient degree
appears only after whole-subgroup aggregation:

```text
move=6:
  oriented_path_count=30
  distinct_path_sums=30
  component_count=6
  distinct_period_sums=6
  period_sum_polynomial_degree=6
```

The oriented composite analogue

```text
p24/oriented_composite_path_toy.py
```

models the p24 class `2 * 463 * 223^(-1)` by the toy move
`3 * 17^(-1)`.  Local oriented path values still have full orbit:

```text
distinct_path_sums=30
distinct_path_products=30
distinct_path_edge_pair_sums=30
```

Only whole oriented cycles give the quotient:

```text
component_count=6
component_sizes=[5]
distinct_period_sums=6
period_sum_polynomial_degree=6
```

The universal closed-cycle filter scan gives the seedless version of the same
warning:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/universal_cycle_sum_filter_scan.py \
  --max-cases 8 --max-h 35 --q-stop 300 --max-ell 11 --max-component-size 4
```

In every tested tiny row the CM component sums are contained in the universal
closed-cycle sums, but the universal correspondence has extra sums:

```text
rows=8
all_cm_sums_subset_universal=1
rows_with_extra_universal_sums=8
```

For example, `D=-87`, `q=103`, `ell=7`, `r=3` has `2` CM sums but `10`
universal cycle sums.  Thus a transfer/resultant formula for closed cycles
still overselects unless it includes a CM-order filter equivalent to `H_D` or
to the missing embedded trace formula.

## First-Trace Level-Power Warning

The first strict trace has a cleaner version of the same temptation: the split
prime over `2` generates the full class group, and the target quotient has
index `19`.  But level `2^19` data is a long edge, not an `H`-period.

The audit

```text
p24/order19_power2_level_audit.py
```

separates the degrees:

```text
X0(2^19) degree to j = 786432
horizontal edge class orbit = 278733727154
desired projector support = 14670196166
```

So a small map to `j` does not imply a large class stabilizer.  The quotient
appears only after applying the subgroup projector or the equivalent order-19
class-character traces.

## Boundary

Fast recurrence, binary powering, chain variables, and resultants are valuable
ways to represent a correspondence.  They do not by themselves change the
class-stabilizer:

```text
local chain data:     translated through the full CM orbit;
closed cycle equation: exponential correspondence degree;
whole-cycle period:   correct quotient, but needs subgroup aggregation.
```

For p24, a successful recurrence/resultant route must therefore specify the
same missing ingredient as the period route:

```text
a non-enumerative way to apply the high-order subgroup projector H, or
equivalently to compute the embedded non-genus 157/211 class-character traces.
```

Without that ingredient, correspondence recurrences are another presentation
of the same embedded class-field problem, not a certificate-scale speedup.
