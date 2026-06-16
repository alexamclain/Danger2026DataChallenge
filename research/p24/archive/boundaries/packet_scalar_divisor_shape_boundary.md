# Packet Scalar Divisor-Shape Boundary

This note records a small diagnostic for the phase-aware Borcherds/product
formula route in:

```text
p24/agent_hermitian_punit_followup.md
```

## Question

If the Hermitian packet norm `Xi_a` is secretly a Borcherds or modular-unit CM
value, then on small CM torsors it might look like a special low-degree
function of the selected singular modulus `j_i`.

The diagnostic in

```text
p24/packet_scalar_divisor_shape_toy.py
```

rotates a complete CM cycle through all selected roots and computes

```text
value(j_i) = Res(f, scalar_poly(rotate_i(cycle)))
```

for a packet factor `f | Phi_n`.  It then asks for the minimal polynomial and
rational interpolation degree of this function in the plain `j` coordinate,
and compares with random values on the same root set.

This is not a proof against Borcherds products: a true Borcherds divisor could
have high degree.  It is a cheap test for a simple one-variable divisor shape.

## Hermitian Result

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packet_scalar_divisor_shape_toy.py \
  --scalar hermitian --random-controls 20 --max-packets 8 --include-linear
```

Output summary:

```text
D=-5000 h=30 m=6 n=5 deg=2:
  poly_degree=29, random=29.00
  rat_degree=15, random=15.00

D=-2239 h=35 m=7 n=5 deg=4:
  poly_degree=34, random=34.00
  rat_degree=18, random=17.05
  numerator_roots=2, numerator_roots_in_cm=0

D=-2239 h=35 m=5 n=7 deg=6:
  poly_degree=34, random=34.00
  rat_degree=17, random=17.00
```

So the selected Hermitian packet norm behaves like generic interpolation in
the plain `j` coordinate.  The one row with numerator roots had roots outside
the CM set, another generic-divisor warning.

Interpretation: a one-variable low-degree modular function of `j` is not
visible.  A successful Borcherds/product formula would need a genuinely
phase-aware higher-dimensional or high-degree divisor, not a simple function
of the selected singular modulus.

Equivalently, the tautological interpolating rational function does have a
divisor, but in the non-genus row its zeros are not supported on the tested CM
root set.  That is the wrong shape for an immediate Gross-Zagier/Schofer style
input: the divisor support looks generic unless a new theorem constructs the
packet phase directly in the principal part.

## Ordinary Autocorrelation Control

Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/packet_scalar_divisor_shape_toy.py \
  --scalar ordinary --random-controls 20 --max-packets 8 --include-linear
```

Output summary:

```text
all tested packets:
  poly_degree=0
  rat_degree=0
```

This is expected: ordinary autocorrelation energy is invariant under rotating
the CM cycle.  Its packet norm is a constant on the selected-root torsor.

This makes the ordinary scalar more natural from a global product/norm point
of view, but it is arithmetically weaker: small CM scans already show ordinary
energy can vanish in natural low-order packets, while the Hermitian scalar has
survived those tests.

## Boundary

The product-formula landscape now separates as follows:

```text
ordinary energy:
  global/shift-invariant and perhaps closer to symmetric product formulas,
  but vulnerable to cancellation;

Hermitian energy:
  positive in characteristic zero and empirically stronger,
  but selected-origin dependent and generic as a function of plain j.
```

Thus the phase-aware Borcherds route remains possible only in a sharper form:
construct a divisor retaining the non-genus packet phase directly, rather than
hoping the Hermitian packet norm is a low-degree function of `j`.

## L1 Companion

The analogous selected-origin diagnostic for the tower-native `L1` scalar is
recorded in:

```text
p24/l1_interpolation_shape_boundary.md
```

It shows the same kind of negative plain-`j` signal for `L1`: after the
expected `H`-periodicity of nonlinear packet norms, the values have generic
interpolation degree and no bounded rational relation below the generic
threshold.  This aligns the two live scalar routes: Hermitian and `L1` are
still plausible p-unit targets, but neither currently exposes a cheap
one-variable divisor formula.

A bounded rerun with `random_trials=5` found:

```text
rows=28
l1_rows=14
l1_rows_with_low_rational_degree=0
l1_rows_with_H_period_ok=12
l1_zero_norms=0
```

So the `L1` data continues to look like a selected-origin p-unit target, not a
hidden low-degree divisor identity.

The next local-coordinate escape hatch is tested in:

```text
p24/packet_scalar_edge_shape_boundary.md
```

There the scalar norm is viewed as a function of an oriented edge
`(j_i,j_{i+1})`.  In the small composite windows, `L1` and Hermitian again
show no below-interpolation bidegree relation.  Thus the surviving
phase-aware divisor route cannot be a bounded plain edge formula either.

## Heegner-Support Follow-Up

The sidecar suggested a stricter falsification test: if the tautological
interpolant is secretly a simple Borcherds input, its divisor roots should
look Heegner/cuspidal rather than generic.  I added:

```text
p24/phase_divisor_heegner_support_scan.py
```

Default command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=p24 python3 \
  p24/phase_divisor_heegner_support_scan.py
```

For the non-genus Hermitian row `D=-2239`, `q=2243`, `h=35`, `m=7`, `n=5`,
the minimal rational interpolant has:

```text
rational_degree=18
numerator_roots=[940, 1191]
denominator_roots=[141, 1711]
numerator_roots_in_target_cm=[]
heegner_discriminants_tested=60
heegner_roots_total=586
```

Scanning fundamental discriminants with `|D| <= 5000` and `h <= 40` found no
small Heegner support for those roots.  This does not rule out a deliberately
constructed high-degree phase-aware Borcherds divisor, but it closes the
simple explanation that the packet norm is already a low-complexity
Heegner-supported function of `j`.
